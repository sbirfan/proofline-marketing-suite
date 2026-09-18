"""Bounded public HTTP fetching with explicit, provenance-rich outcomes."""

from __future__ import annotations

import ipaddress
import socket
import ssl
import time
from collections.abc import Callable
from contextlib import AbstractContextManager
from dataclasses import dataclass
from http.client import HTTPMessage
from typing import IO, Protocol, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from ..models import FetchObservation, ObservationStatus

DEFAULT_USER_AGENT = (
    "SVG-AI-Marketing-Audit/0.2 (+https://github.com/sbirfan/svgai-marketing-suite)"
)
Resolver = Callable[..., object]


class UnsafeAddressError(ValueError):
    """Raised when a target resolves outside the public Internet."""


class Opener(Protocol):
    def open(self, request: Request, timeout: float) -> AbstractContextManager[HttpResponse]: ...


class HttpResponse(Protocol):
    headers: HTTPMessage

    def getcode(self) -> int: ...

    def geturl(self) -> str: ...

    def read(self, amount: int) -> bytes: ...


@dataclass(slots=True)
class FetchResult:
    observation: FetchObservation
    body: bytes | None = None


def validate_public_url(url: str, *, resolver: Resolver = socket.getaddrinfo) -> None:
    """Reject non-HTTP targets, credentials, and non-global destination addresses."""
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"} or not parts.hostname:
        raise UnsafeAddressError("unsupported_url")
    if parts.username or parts.password:
        raise UnsafeAddressError("embedded_credentials")
    hostname = parts.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise UnsafeAddressError("non_public_address")
    try:
        literal = ipaddress.ip_address(hostname)
    except ValueError:
        try:
            resolved = resolver(hostname, parts.port or 443, type=socket.SOCK_STREAM)
        except socket.gaierror as error:
            raise URLError(error) from error
        addresses = cast(list[tuple[int, int, int, str, tuple[object, ...]]], resolved)
        if not addresses:
            raise URLError("dns_no_results") from None
        candidates = {str(item[4][0]) for item in addresses}
    else:
        candidates = {str(literal)}
    if any(not ipaddress.ip_address(address).is_global for address in candidates):
        raise UnsafeAddressError("non_public_address")


class ValidatingRedirectHandler(HTTPRedirectHandler):
    def __init__(self, validator: Callable[[str], None], chain: list[str]) -> None:
        super().__init__()
        self.validator = validator
        self.chain = chain

    def redirect_request(
        self,
        request: Request,
        file_pointer: IO[bytes],
        code: int,
        message: str,
        headers: HTTPMessage,
        new_url: str,
    ) -> Request | None:
        resolved = urljoin(request.full_url, new_url)
        self.validator(resolved)
        self.chain.append(resolved)
        return super().redirect_request(request, file_pointer, code, message, headers, resolved)


class SafeHttpClient:
    def __init__(
        self,
        *,
        timeout: float = 15.0,
        max_bytes: int = 5_000_000,
        user_agent: str = DEFAULT_USER_AGENT,
        enforce_public_addresses: bool = True,
        resolver: Resolver = socket.getaddrinfo,
        opener: Opener | None = None,
    ) -> None:
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.user_agent = user_agent
        self.enforce_public_addresses = enforce_public_addresses
        self.resolver = resolver
        self._opener = opener

    def _validate(self, url: str) -> None:
        if self.enforce_public_addresses:
            validate_public_url(url, resolver=self.resolver)
            return
        parts = urlsplit(url)
        if parts.scheme not in {"http", "https"} or not parts.netloc:
            raise UnsafeAddressError("unsupported_url")

    def fetch(self, url: str, *, accepted_types: tuple[str, ...] = ()) -> FetchResult:
        started = time.monotonic()
        redirect_chain = [url]
        try:
            self._validate(url)
            request = Request(
                url,
                headers={"User-Agent": self.user_agent, "Accept-Encoding": "identity"},
            )
            opener = self._opener or build_opener(
                ValidatingRedirectHandler(self._validate, redirect_chain)
            )
            with opener.open(request, timeout=self.timeout) as response:
                status = response.getcode()
                final_url = response.geturl()
                if redirect_chain[-1] != final_url:
                    redirect_chain.append(final_url)
                content_type = response.headers.get_content_type()
                encoding = response.headers.get_content_charset() or "utf-8"
                if accepted_types and not any(
                    content_type.startswith(value) for value in accepted_types
                ):
                    return self._result(
                        url,
                        started,
                        ObservationStatus.FETCH_FAILED,
                        http_status=status,
                        final_url=final_url,
                        content_type=content_type,
                        encoding=encoding,
                        reason="unexpected_content_type",
                        redirect_chain=redirect_chain,
                    )
                length_header = response.headers.get("Content-Length")
                try:
                    declared_length = int(length_header) if length_header else None
                except ValueError:
                    declared_length = None
                if declared_length is not None and declared_length > self.max_bytes:
                    return self._result(
                        url,
                        started,
                        ObservationStatus.FETCH_FAILED,
                        http_status=status,
                        final_url=final_url,
                        content_type=content_type,
                        content_length=declared_length,
                        encoding=encoding,
                        reason="response_too_large",
                        redirect_chain=redirect_chain,
                    )
                body = response.read(self.max_bytes + 1)
                if len(body) > self.max_bytes:
                    return self._result(
                        url,
                        started,
                        ObservationStatus.FETCH_FAILED,
                        http_status=status,
                        final_url=final_url,
                        content_type=content_type,
                        content_length=len(body),
                        encoding=encoding,
                        reason="response_too_large",
                        redirect_chain=redirect_chain,
                    )
                result = self._result(
                    url,
                    started,
                    ObservationStatus.OBSERVED,
                    http_status=status,
                    final_url=final_url,
                    content_type=content_type,
                    content_length=len(body),
                    encoding=encoding,
                    redirect_chain=redirect_chain,
                )
                result.body = body
                return result
        except HTTPError as error:
            status = error.code
            if status in {404, 410}:
                state = ObservationStatus.NOT_FOUND
                reason = "http_not_found"
            elif status in {401, 403, 407, 429}:
                state = ObservationStatus.BLOCKED
                reason = "crawler_access_denied"
            else:
                state = ObservationStatus.FETCH_FAILED
                reason = "http_error"
            return self._result(
                url,
                started,
                state,
                http_status=status,
                reason=reason,
                redirect_chain=redirect_chain,
            )
        except UnsafeAddressError as error:
            return self._result(
                url,
                started,
                ObservationStatus.BLOCKED,
                reason=str(error),
                redirect_chain=redirect_chain,
            )
        except ssl.SSLCertVerificationError:
            return self._result(
                url,
                started,
                ObservationStatus.FETCH_FAILED,
                reason="tls_verification_failed",
                redirect_chain=redirect_chain,
            )
        except TimeoutError:
            return self._result(
                url,
                started,
                ObservationStatus.FETCH_FAILED,
                reason="timeout",
                redirect_chain=redirect_chain,
            )
        except URLError as error:
            reason = "network_error"
            if isinstance(error.reason, ssl.SSLCertVerificationError):
                reason = "tls_verification_failed"
            elif isinstance(error.reason, socket.gaierror):
                reason = "dns_error"
            return self._result(
                url,
                started,
                ObservationStatus.FETCH_FAILED,
                reason=reason,
                redirect_chain=redirect_chain,
            )
        except ValueError:
            return self._result(
                url,
                started,
                ObservationStatus.FETCH_FAILED,
                reason="invalid_url",
                redirect_chain=redirect_chain,
            )

    @staticmethod
    def decode(body: bytes, encoding: str | None = None) -> str:
        charset = encoding or "utf-8"
        try:
            return body.decode(charset, errors="replace")
        except LookupError:
            return body.decode("utf-8", errors="replace")

    @staticmethod
    def _result(
        url: str,
        started: float,
        status: ObservationStatus,
        *,
        http_status: int | None = None,
        final_url: str | None = None,
        content_type: str | None = None,
        content_length: int | None = None,
        encoding: str | None = None,
        reason: str | None = None,
        redirect_chain: list[str] | None = None,
    ) -> FetchResult:
        elapsed = int((time.monotonic() - started) * 1000)
        return FetchResult(
            FetchObservation(
                url=url,
                status=status,
                http_status=http_status,
                final_url=final_url,
                content_type=content_type,
                content_length=content_length,
                encoding=encoding,
                reason=reason,
                elapsed_ms=elapsed,
                redirect_chain=redirect_chain or [url],
            )
        )
