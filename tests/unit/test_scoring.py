from svgai_marketing.models import (
    EvidenceDocument,
    FetchObservation,
    Finding,
    ObservationStatus,
    PageEvidence,
    Severity,
)
from svgai_marketing.scoring.engine import calculate_scores


def evidence(status: ObservationStatus) -> EvidenceDocument:
    return EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/",
        fetch=FetchObservation(url="https://example.test/", status=status),
        page=PageEvidence(url="https://example.test/"),
    )


def test_blocked_fetch_never_becomes_a_score() -> None:
    categories, overall, confidence, coverage, status = calculate_scores(
        evidence(ObservationStatus.BLOCKED), []
    )
    assert overall is None
    assert confidence == 0
    assert coverage == 0
    assert status == "insufficient_evidence"
    assert all(category.score is None for category in categories.values())


def test_untested_categories_are_not_imputed() -> None:
    finding = Finding(
        id="seo.example",
        category="seo",
        severity=Severity.HIGH,
        claim="Example",
        evidence=[],
        confidence=1.0,
    )
    categories, overall, _, coverage, status = calculate_scores(
        evidence(ObservationStatus.OBSERVED), [finding]
    )
    assert categories["seo"].score == 78
    assert categories["competitive"].score is None
    assert categories["growth"].status == "not_tested"
    assert overall is not None
    assert coverage == 0.75
    assert status == "partial"
