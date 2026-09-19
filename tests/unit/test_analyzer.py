from proofline_marketing.analyzers.technical import analyze_evidence, analyze_page
from proofline_marketing.models import (
    EvidenceDocument,
    FetchObservation,
    ObservationStatus,
    PageEvidence,
)


def test_missing_elements_create_source_backed_findings() -> None:
    findings = analyze_page(PageEvidence(url="https://example.test/"))
    ids = {finding.id for finding in findings}

    assert "seo.title.missing" in ids
    assert "seo.meta_description.missing" in ids
    assert "content.h1.missing" in ids
    assert all(finding.evidence[0].url == "https://example.test/" for finding in findings)


def test_noindex_is_reported_without_claiming_it_is_a_bug() -> None:
    page = PageEvidence(url="https://example.test/", robots_meta=["noindex", "follow"])
    finding = next(item for item in analyze_page(page) if item.id == "seo.indexing.noindex")
    assert "Confirm" in (finding.recommendation or "")


def test_conversion_and_structured_data_checks_are_deterministic() -> None:
    page = PageEvidence(
        url="https://example.test/",
        visible_word_count=300,
        buttons=["Submit"],
        forms=[{"fields": 12}],
        json_ld=[{"_invalid": True}],
        links=[{"kind": "external", "href": "https://outside.test/"}],
    )
    ids = {finding.id for finding in analyze_page(page)}

    assert "conversion.action.generic" in ids
    assert "conversion.form.fields_many" in ids
    assert "seo.structured_data.invalid_json" in ids
    assert "seo.internal_links.none" in ids


def test_blocked_sitemap_is_not_reported_as_missing() -> None:
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/",
        fetch=FetchObservation(url="https://example.test/", status=ObservationStatus.OBSERVED),
        page=PageEvidence(url="https://example.test/", visible_word_count=200),
        robots={"status": "observed", "search_engine_access": "allowed"},
        sitemap={"status": "blocked", "truncated": False},
    )
    ids = {finding.id for finding in analyze_evidence(evidence)}

    assert "seo.sitemap.audit_blocked" in ids
    assert "seo.sitemap.not_found" not in ids
