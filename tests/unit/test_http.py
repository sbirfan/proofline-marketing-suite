from email.message import Message
from urllib.error import HTTPError

from proofline_marketing.crawler.http import SafeHttpClient, validate_public_url
from proofline_marketing.models import ObservationStatus


class RaisingOpener:
    def __init__(self, status: int) -> None:
        self.status = status

    def open(self, request, timeout):
        del timeout
        raise HTTPError(request.full_url, self.status, "test", {}, None)


class FakeResponse:
    def __init__(
        self,
        url: str,
        body: bytes,
        content_type: str = "text/html; charset=iso-8859-1",
        declared_length: int | None = None,
    ) -> None:
        self.url = url
        self.body = body
        self.headers = Message()
        self.headers["Content-Type"] = content_type
        if declared_length is not None:
            self.headers["Content-Length"] = str(declared_length)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def getcode(self) -> int:
        return 200

    def geturl(self) -> str:
        return self.url

    def read(self, amount: int) -> bytes:
        return self.body[:amount]


class StaticOpener:
    def __init__(self, response: FakeResponse) -> None:
        self.response = response

    def open(self, request, timeout):
        del request, timeout
        return self.response


def test_access_denied_is_not_reported_as_absence() -> None:
    client = SafeHttpClient(opener=RaisingOpener(403), enforce_public_addresses=False)

    result = client.fetch("https://example.test/robots.txt")

    assert result.observation.status is ObservationStatus.BLOCKED
    assert result.observation.http_status == 403
    assert result.observation.reason == "crawler_access_denied"


def test_http_not_found_is_distinct() -> None:
    client = SafeHttpClient(opener=RaisingOpener(404), enforce_public_addresses=False)

    result = client.fetch("https://example.test/sitemap.xml")

    assert result.observation.status is ObservationStatus.NOT_FOUND
    assert result.observation.reason == "http_not_found"


def test_private_address_is_blocked_before_network_access() -> None:
    client = SafeHttpClient()

    result = client.fetch("http://127.0.0.1/admin")

    assert result.observation.status is ObservationStatus.BLOCKED
    assert result.observation.reason == "non_public_address"


def test_embedded_credentials_are_blocked() -> None:
    client = SafeHttpClient()

    result = client.fetch("https://user:password@example.com/")

    assert result.observation.status is ObservationStatus.BLOCKED
    assert result.observation.reason == "embedded_credentials"


def test_unknown_encoding_falls_back_to_utf8() -> None:
    assert SafeHttpClient.decode(b"hello", "not-a-real-charset") == "hello"


def test_success_records_response_provenance_and_encoding() -> None:
    url = "https://example.test/"
    body = "café".encode("iso-8859-1")
    client = SafeHttpClient(
        opener=StaticOpener(FakeResponse(url, body)),
        enforce_public_addresses=False,
    )

    result = client.fetch(url, accepted_types=("text/html",))

    assert result.observation.status is ObservationStatus.OBSERVED
    assert result.observation.content_length == len(body)
    assert result.observation.encoding == "iso-8859-1"
    assert result.observation.redirect_chain == [url]
    assert result.body is not None
    assert client.decode(result.body, result.observation.encoding) == "café"


def test_declared_oversized_response_is_rejected_before_read() -> None:
    url = "https://example.test/large"
    client = SafeHttpClient(
        opener=StaticOpener(FakeResponse(url, b"small", declared_length=1_000)),
        enforce_public_addresses=False,
        max_bytes=100,
    )

    result = client.fetch(url)

    assert result.observation.status is ObservationStatus.FETCH_FAILED
    assert result.observation.reason == "response_too_large"
    assert result.observation.content_length == 1_000


def test_custom_opener_cannot_bypass_final_url_validation() -> None:
    client = SafeHttpClient(
        opener=StaticOpener(FakeResponse("http://127.0.0.1/admin", b"private")),
        resolver=lambda *args, **kwargs: [
            (2, 1, 6, "", ("93.184.216.34", 443)),
        ],
    )

    result = client.fetch("https://example.test/")

    assert result.observation.status is ObservationStatus.BLOCKED
    assert result.observation.reason == "non_public_address"


def test_control_characters_and_oversized_urls_are_rejected() -> None:
    for url in ("https://example.com/\nheader", "https://example.com/" + "x" * 8_200):
        try:
            validate_public_url(url)
        except ValueError as error:
            assert str(error) == "invalid_url"
        else:
            raise AssertionError("unsafe URL accepted")
