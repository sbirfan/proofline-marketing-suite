"""Bounded HTTP fetching with TLS verification and explicit failure states."""

from __future__ import annotations

import socket
import ssl
import time
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener

from ..models import FetchObservation, ObservationStatus

DEFAULT_USER_AGENT = (
    "SVG-AI-Marketing-Audit/0.1 (+https://github.com/sbirfan/svgai-marketing-suite)"
)


@dataclass(slots=True)
class FetchResult:
    observation: FetchObservation
    body: bytes | None = None


class SafeHttpClient:
    def __init__(
        self,
        *,
        timeout: float = 15.0,
        max_bytes: int = 5_000_000,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.timeout = timeout
        self.max_bytes = max_bytes
        self.user_agent = user_agent
        self._opener = build_opener()

    def fetch(self, url: str, *, accepted_types: tuple[str, ...] = ()) -> FetchResult:
        started = time.monotonic()
        request = Request(
            url,
            headers={"User-Agent": self.user_agent, "Accept-Encoding": "identity"},
        )
        try:
            with self._opener.open(request, timeout=self.timeout) as response:
                status = response.getcode()
                final_url = response.geturl()
                content_type = response.headers.get_content_type()
                if accepted_types and not any(content_type.startswith(t) for t in accepted_types):
                    return self._result(
                        url,
                        started,
                        ObservationStatus.FETCH_FAILED,
                        http_status=status,
                        final_url=final_url,
                        content_type=content_type,
                        reason="unexpected_content_type",
                    )
                length_header = response.headers.get("Content-Length")
                if length_header and int(length_header) > self.max_bytes:
                    return self._result(
                        url,
                        started,
                        ObservationStatus.FETCH_FAILED,
                        http_status=status,
                        final_url=final_url,
                        content_type=content_type,
                        reason="response_too_large",
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
                        reason="response_too_large",
                    )
                result = self._result(
                    url,
                    started,
                    ObservationStatus.OBSERVED,
                    http_status=status,
                    final_url=final_url,
                    content_type=content_type,
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
            return self._result(url, started, state, http_status=status, reason=reason)
        except ssl.SSLCertVerificationError:
            return self._result(
                url, started, ObservationStatus.FETCH_FAILED, reason="tls_verification_failed"
            )
        except TimeoutError:
            return self._result(url, started, ObservationStatus.FETCH_FAILED, reason="timeout")
        except URLError as error:
            reason = "network_error"
            if isinstance(error.reason, ssl.SSLCertVerificationError):
                reason = "tls_verification_failed"
            elif isinstance(error.reason, socket.gaierror):
                reason = "dns_error"
            return self._result(url, started, ObservationStatus.FETCH_FAILED, reason=reason)
        except ValueError:
            return self._result(url, started, ObservationStatus.FETCH_FAILED, reason="invalid_url")

    @staticmethod
    def decode(body: bytes, content_type: str | None = None) -> str:
        del content_type
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
        reason: str | None = None,
    ) -> FetchResult:
        elapsed = int((time.monotonic() - started) * 1000)
        return FetchResult(
            FetchObservation(
                url=url,
                status=status,
                http_status=http_status,
                final_url=final_url,
                content_type=content_type,
                reason=reason,
                elapsed_ms=elapsed,
            )
        )
