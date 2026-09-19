import gzip

from proofline_marketing.crawler.http import FetchResult, SafeHttpClient
from proofline_marketing.crawler.sitemap import inspect_sitemap
from proofline_marketing.models import FetchObservation, ObservationStatus


class FakeClient(SafeHttpClient):
    def __init__(self, responses: dict[str, tuple[bytes | None, str]]) -> None:
        super().__init__(enforce_public_addresses=False)
        self.responses = responses

    def fetch(self, url: str, *, accepted_types: tuple[str, ...] = ()) -> FetchResult:
        del accepted_types
        body, content_type = self.responses[url]
        return FetchResult(
            FetchObservation(
                url=url,
                status=ObservationStatus.OBSERVED
                if body is not None
                else ObservationStatus.NOT_FOUND,
                http_status=200 if body is not None else 404,
                final_url=url,
                content_type=content_type,
                encoding="utf-8",
                redirect_chain=[url],
            ),
            body,
        )


def test_recurses_sitemap_index_and_deduplicates_urls() -> None:
    root = b"""<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <sitemap><loc>https://example.test/one.xml</loc></sitemap>
      <sitemap><loc>https://example.test/two.xml.gz</loc></sitemap>
    </sitemapindex>"""
    first = b"""<urlset><url><loc>https://example.test/a</loc></url></urlset>"""
    second = gzip.compress(
        b"<urlset><url><loc>https://example.test/a</loc></url>"
        b"<url><loc>https://example.test/b</loc></url></urlset>"
    )
    client = FakeClient(
        {
            "https://example.test/sitemap.xml": (root, "application/xml"),
            "https://example.test/one.xml": (first, "application/xml"),
            "https://example.test/two.xml.gz": (second, "application/gzip"),
        }
    )

    result = inspect_sitemap("https://example.test/", client)

    assert result["urls"] == ["https://example.test/a", "https://example.test/b"]
    assert result["sitemap_count"] == 3
    assert result["truncated"] is False


def test_malformed_xml_retains_failure_reason() -> None:
    client = FakeClient({"https://example.test/sitemap.xml": (b"<urlset><url>", "application/xml")})

    result = inspect_sitemap("https://example.test/", client)

    assert result["status"] == "fetch_failed"
    assert result["reason"] == "malformed_xml"


def test_cross_origin_nested_sitemap_is_not_fetched() -> None:
    root = b"<sitemapindex><sitemap><loc>https://other.test/map.xml</loc></sitemap></sitemapindex>"
    client = FakeClient({"https://example.test/sitemap.xml": (root, "application/xml")})

    result = inspect_sitemap("https://example.test/", client)

    assert result["sitemap_count"] == 2
    assert result["resources"][1]["reason"] == "cross_origin_sitemap"
