from pathlib import Path

import pytest

from proofline_marketing.models import (
    AuditResult,
    CategoryScore,
    EvidenceDocument,
    EvidenceReference,
    FetchObservation,
    Finding,
    ObservationStatus,
    Severity,
)
from proofline_marketing.reporting import (
    ReportBrand,
    ReportIntegrityError,
    render_html,
    render_pdf,
)

pypdf = pytest.importorskip("pypdf")


def audit() -> AuditResult:
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/a-very-long-report-path?campaign=client-reporting",
        fetch=FetchObservation(url="https://example.test/", status=ObservationStatus.OBSERVED),
    )
    finding = Finding(
        id="seo.title.missing",
        category="seo",
        severity=Severity.HIGH,
        claim="The <title> element is missing & should be reviewed.",
        evidence=[
            EvidenceReference(
                url="https://example.test/a-very-long-report-path?campaign=client-reporting",
                source_type="html",
            )
        ],
        confidence=1,
        recommendation="Add a concise, descriptive page title.",
    )
    return AuditResult(
        schema_version="2.0",
        score_version="5.0",
        target_url=evidence.target_url,
        generated_at="2026-09-18T00:00:00+00:00",
        evidence=evidence,
        findings=[finding],
        categories={
            name: CategoryScore(80 if name == "seo" else None, 0.8, 0.7)
            for name in ("content", "conversion", "seo", "competitive", "brand", "growth")
        },
        overall=80,
        confidence=0.8,
        coverage=0.7,
        status="partial",
    )


def test_html_is_accessible_printable_and_escapes_untrusted_values() -> None:
    body = render_html(audit(), ReportBrand(name="Client & Co"))

    assert "<!doctype html>" in body
    assert "<th scope='row'>Seo</th>" in body
    assert "@media print" in body
    assert "Client &amp; Co" in body
    assert "The &lt;title&gt; element is missing &amp; should be reviewed." in body
    assert "Context integrity" in body
    assert "Evidence scope" in body
    assert "scope: page" in body


def test_brand_colors_reject_css_injection() -> None:
    with pytest.raises(ValueError, match="hexadecimal"):
        ReportBrand(primary_color="#fff; background:url(evil)")


def test_pdf_is_deterministic_and_extractable(tmp_path: Path) -> None:
    first = render_pdf(audit(), tmp_path / "first.pdf")
    second = render_pdf(audit(), tmp_path / "second.pdf")

    assert first.read_bytes() == second.read_bytes()
    reader = pypdf.PdfReader(first)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert len(reader.pages) >= 1
    assert "Marketing Audit" in text
    assert "Category scores" in text
    assert "Context integrity" in text
    assert "Evidence scope" in text
    assert "Page 1" in text


def test_client_reports_block_unresolved_context_conflict(tmp_path: Path) -> None:
    result = audit()
    result.context_assessment["status"] = "conflict"
    result.context_assessment["resolution_required"] = True

    with pytest.raises(ReportIntegrityError, match="context conflict"):
        render_html(result)
    with pytest.raises(ReportIntegrityError, match="context conflict"):
        render_pdf(result, tmp_path / "blocked.pdf")


def test_client_reports_reject_unsupported_sitewide_claim() -> None:
    result = audit()
    result.findings[0].claim_scope = "site"

    with pytest.raises(ReportIntegrityError, match="site-wide"):
        render_html(result)


def test_client_reports_require_evidence_references() -> None:
    result = audit()
    result.findings[0].evidence = []

    with pytest.raises(ReportIntegrityError, match="no evidence"):
        render_html(result)
