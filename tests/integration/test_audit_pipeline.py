from pathlib import Path

from proofline_marketing.crawler.http import FetchResult
from proofline_marketing.models import (
    BusinessContext,
    EvidenceDocument,
    FetchObservation,
    ObservationStatus,
    PageEvidence,
)
from proofline_marketing.orchestrator import run_audit
from proofline_marketing.reporting.markdown import render_markdown

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

    monkeypatch.setattr("proofline_marketing.crawler.http.SafeHttpClient.fetch", fake_fetch)
    result = run_audit("example.test")
    report = render_markdown(result)

    assert result.target_url == "https://example.test"
    assert result.status == "partial"
    assert result.evidence.sitemap["urls"] == ["https://example.test/"]
    assert "Marketing Audit" in report
    assert "Competitive" in report
    assert "not_tested" in report


def test_precollected_audit_with_specialists_can_be_complete() -> None:
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/",
        fetch=FetchObservation(url="https://example.test/", status=ObservationStatus.OBSERVED),
        page=PageEvidence(url="https://example.test/", visible_word_count=300),
        robots={"status": "observed"},
        sitemap={"status": "observed"},
    )

    def executor(brief: dict) -> dict:
        return {
            "schema_version": "1.0",
            "agent": brief["agent"],
            "interpretations": [],
            "recommendations": [],
            "dimension_assessments": [
                {
                    "dimension": brief["required_dimensions"][0],
                    "rating": "adequate",
                    "confidence": 0.8,
                    "evidence_urls": [brief["target_url"]],
                    "limitations": [],
                }
            ],
        }

    names = (
        "content-strategist",
        "conversion-analyst",
        "competitive-analyst",
        "brand-strategist",
        "growth-strategist",
    )
    result = run_audit(
        "https://example.test/",
        business_context=BusinessContext(
            competitor_urls=["https://competitor.test/"],
            comparison_dimensions=["positioning"],
            competitors_confirmed=True,
        ),
        specialist_executors={name: executor for name in names},
        precollected_evidence=evidence,
        precollected_competitors={"https://competitor.test/": evidence},
    )

    assert result.status == "complete"
    assert result.categories["growth"].score == 70
    assert not result.agent_failures
