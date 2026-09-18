"""Generate a synthetic client PDF for local visual review."""

from __future__ import annotations

from pathlib import Path

from svgai_marketing.models import (
    AuditResult,
    CategoryScore,
    EvidenceDocument,
    EvidenceReference,
    FetchObservation,
    Finding,
    ObservationStatus,
    Severity,
)
from svgai_marketing.reporting import ReportBrand, render_pdf


def sample_result() -> AuditResult:
    url = "https://example.test/products/evidence-first-marketing-platform"
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url=url,
        fetch=FetchObservation(url=url, status=ObservationStatus.OBSERVED),
    )
    findings = [
        Finding(
            id=f"sample.finding.{index:02d}",
            category="seo" if index % 2 else "conversion",
            severity=Severity.MEDIUM if index % 3 else Severity.HIGH,
            claim=f"Synthetic review item {index} needs a documented owner and validation step.",
            evidence=[
                EvidenceReference(
                    url=f"{url}?evidence=sample-{index}&source=client-report-regression",
                    source_type="synthetic",
                )
            ],
            confidence=0.9,
            recommendation=(
                "Review the observed condition, assign an owner, and validate the change against "
                "the same evidence source before publishing."
            ),
        )
        for index in range(1, 15)
    ]
    scores = {
        "content": 82,
        "conversion": 68,
        "seo": 74,
        "competitive": 70,
        "brand": 79,
        "growth": 65,
    }
    return AuditResult(
        schema_version="2.0",
        score_version="5.0",
        target_url=url,
        generated_at="2026-09-18T00:00:00+00:00",
        evidence=evidence,
        findings=findings,
        categories={name: CategoryScore(score, 0.84, 0.78) for name, score in scores.items()},
        overall=74.8,
        confidence=0.84,
        coverage=0.78,
        status="complete",
    )


if __name__ == "__main__":
    render_pdf(
        sample_result(),
        Path("output/pdf/client-report-sample.pdf"),
        ReportBrand(name="Example Advisory", accent_color="#b45309"),
    )
