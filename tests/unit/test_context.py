from proofline_marketing.context import assess_context
from proofline_marketing.models import (
    AuditMode,
    BusinessContext,
    ContextStatus,
    EvidenceDocument,
    FetchObservation,
    ObservationStatus,
    PageEvidence,
)


def evidence_with_actions(*actions: str) -> EvidenceDocument:
    return EvidenceDocument(
        schema_version="2.0",
        target_url="https://shop.example/",
        fetch=FetchObservation(url="https://shop.example/", status=ObservationStatus.OBSERVED),
        page=PageEvidence(
            url="https://shop.example/",
            buttons=list(actions),
            visible_text=" ".join(actions),
        ),
    )


def test_ecommerce_conflicts_with_consultation_context() -> None:
    assessment = assess_context(
        evidence_with_actions("Shop Now", "Add to Cart", "Checkout"),
        BusinessContext(offer="Free consultation", primary_conversion="Book a consultation"),
    )

    assert assessment.status == ContextStatus.CONFLICT
    assert assessment.observed_business_model == "ecommerce"
    assert assessment.observed_conversions == ["ecommerce_purchase"]
    assert assessment.resolution_required is True


def test_aligned_ecommerce_context_passes() -> None:
    assessment = assess_context(
        evidence_with_actions("Add to Cart"),
        BusinessContext(primary_conversion="Checkout"),
    )

    assert assessment.status == ContextStatus.ALIGNED
    assert assessment.resolution_required is False


def test_missing_signals_remain_unknown() -> None:
    assessment = assess_context(evidence_with_actions(), BusinessContext())

    assert assessment.status == ContextStatus.UNKNOWN
    assert assessment.observed_business_model == "unknown"


def test_planned_funnel_records_but_does_not_block_conflict() -> None:
    assessment = assess_context(
        evidence_with_actions("Buy Now"),
        BusinessContext(primary_conversion="Book a consultation"),
        AuditMode.PLANNED_FUNNEL,
    )

    assert assessment.status == ContextStatus.OVERRIDDEN
    assert assessment.conflicts
    assert assessment.resolution_required is False
