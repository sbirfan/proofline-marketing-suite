from urllib.error import HTTPError

from svgai_marketing.crawler.http import SafeHttpClient
from svgai_marketing.models import ObservationStatus


class RaisingOpener:
    def __init__(self, status: int) -> None:
        self.status = status

    def open(self, request, timeout):
        del timeout
        raise HTTPError(request.full_url, self.status, "test", {}, None)


def test_access_denied_is_not_reported_as_absence() -> None:
    client = SafeHttpClient()
    client._opener = RaisingOpener(403)  # type: ignore[assignment]

    result = client.fetch("https://example.test/robots.txt")

    assert result.observation.status is ObservationStatus.BLOCKED
    assert result.observation.http_status == 403
    assert result.observation.reason == "crawler_access_denied"


def test_http_not_found_is_distinct() -> None:
    client = SafeHttpClient()
    client._opener = RaisingOpener(404)  # type: ignore[assignment]

    result = client.fetch("https://example.test/sitemap.xml")

    assert result.observation.status is ObservationStatus.NOT_FOUND
    assert result.observation.reason == "http_not_found"
