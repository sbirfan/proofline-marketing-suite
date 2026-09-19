from proofline_marketing.models import (
    EvidenceDocument,
    FetchObservation,
    Finding,
    ObservationStatus,
    PageEvidence,
    Severity,
)
from proofline_marketing.scoring.engine import calculate_scores, synthesize_specialist_scores


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
        id="seo.title.missing",
        category="seo",
        severity=Severity.HIGH,
        claim="Example",
        evidence=[],
        confidence=1.0,
    )
    categories, overall, _, coverage, status = calculate_scores(
        evidence(ObservationStatus.OBSERVED), [finding]
    )
    assert categories["seo"].score == 80
    assert categories["competitive"].score is None
    assert categories["growth"].status == "not_tested"
    assert overall is not None
    assert coverage == 0.55
    assert status == "partial"


def test_unregistered_finding_cannot_silently_change_score() -> None:
    finding = Finding(
        id="seo.future_rule",
        category="seo",
        severity=Severity.CRITICAL,
        claim="A future rule",
        evidence=[],
        confidence=1.0,
    )

    categories, _, _, _, _ = calculate_scores(evidence(ObservationStatus.OBSERVED), [finding])

    assert categories["seo"].score == 100


def test_specialist_assessments_complete_unscored_categories_deterministically() -> None:
    categories, _, _, _, _ = calculate_scores(evidence(ObservationStatus.OBSERVED), [])
    results = {
        agent: {
            "dimension_assessments": [
                {
                    "dimension": "example",
                    "rating": "adequate",
                    "confidence": 0.8,
                    "evidence_urls": ["https://example.test/"],
                    "limitations": [],
                }
            ]
        }
        for agent in (
            "content-strategist",
            "conversion-analyst",
            "competitive-analyst",
            "brand-strategist",
            "growth-strategist",
        )
    }

    updated, overall, confidence, coverage, status = synthesize_specialist_scores(
        categories, results
    )

    assert updated["competitive"].score == 70
    assert updated["growth"].score == 70
    assert overall is not None
    assert confidence > 0
    assert coverage > 0
    assert status == "complete"
