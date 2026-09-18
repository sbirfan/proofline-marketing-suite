from svgai_marketing.analyzers.technical import analyze_page
from svgai_marketing.models import PageEvidence


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
