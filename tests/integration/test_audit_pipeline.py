from pathlib import Path

from svgai_marketing.crawler.http import FetchResult
from svgai_marketing.models import FetchObservation, ObservationStatus
from svgai_marketing.orchestrator import run_audit
from svgai_marketing.reporting.markdown import render_markdown

FIXTURES = Path(__file__).parents[1] / "fixtures" / "sites"


def test_audit_pipeline_uses_one_canonical_result(monkeypatch) -> None:
    html = (FIXTURES / "static-good" / "index.html").read_bytes()

    def fake_fetch(self, url, *, accepted_types=()):
        del self, accepted_types
        if url.endswith("robots.txt"):
            body = b"User-agent: *\nAllow: /\nSitemap: https://example.test/sitemap.xml\n"
            return FetchResult(FetchObservation(url=url, status=ObservationStatus.OBSERVED), body)
        if url.endswith("sitemap.xml"):
            body = b'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.test/</loc></url></urlset>'
            return FetchResult(FetchObservation(url=url, status=ObservationStatus.OBSERVED), body)
        return FetchResult(
            FetchObservation(
                url=url,
                status=ObservationStatus.OBSERVED,
                http_status=200,
                final_url=url,
                content_type="text/html",
            ),
            html,
        )

    monkeypatch.setattr("svgai_marketing.crawler.http.SafeHttpClient.fetch", fake_fetch)
    result = run_audit("example.test")
    report = render_markdown(result)

    assert result.target_url == "https://example.test"
    assert result.status == "partial"
    assert result.evidence.sitemap["urls"] == ["https://example.test/"]
    assert "Marketing Audit" in report
    assert "Competitive" in report
    assert "not_tested" in report
