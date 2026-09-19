"""Evidence-driven business context classification and conflict detection."""

from __future__ import annotations

from collections.abc import Iterable

from .models import (
    AuditMode,
    BusinessContext,
    ContextAssessment,
    ContextStatus,
    EvidenceDocument,
)

CONVERSION_SIGNALS: dict[str, tuple[str, ...]] = {
    "ecommerce_purchase": ("add to cart", "add to bag", "buy now", "checkout", "shop now"),
    "trial_signup": ("start free trial", "free trial", "sign up free", "get started free"),
    "demo_request": ("book a demo", "request a demo", "schedule a demo"),
    "consultation_booking": (
        "book a consultation",
        "free consultation",
        "schedule a consultation",
    ),
    "appointment_booking": ("book an appointment", "schedule an appointment"),
    "quote_request": ("request a quote", "get a quote"),
    "contact_lead": ("contact us", "get in touch"),
}

BUSINESS_MODEL_BY_CONVERSION = {
    "ecommerce_purchase": "ecommerce",
    "trial_signup": "saas",
    "demo_request": "saas",
    "consultation_booking": "service_business",
    "appointment_booking": "local_service",
    "quote_request": "service_business",
}


def _normalized_page_text(evidence: EvidenceDocument) -> str:
    page = evidence.page
    if page is None:
        return ""
    parts: list[str] = [page.visible_text, page.title or "", page.meta_description or ""]
    parts.extend(page.buttons)
    parts.extend(link.get("text", "") for link in page.links)
    return " ".join(parts).casefold()


def _matching_conversions(text: str) -> list[str]:
    return [
        conversion
        for conversion, phrases in CONVERSION_SIGNALS.items()
        if any(phrase in text for phrase in phrases)
    ]


def _context_conversion(values: Iterable[str | None]) -> str | None:
    text = " ".join(value for value in values if value).casefold()
    matches = _matching_conversions(text)
    return matches[0] if matches else None


def assess_context(
    evidence: EvidenceDocument,
    context: BusinessContext,
    audit_mode: AuditMode = AuditMode.CURRENT_STATE,
) -> ContextAssessment:
    """Compare explicit context to observed conversion evidence without inventing facts."""
    observed = _matching_conversions(_normalized_page_text(evidence))
    supplied = _context_conversion((context.offer, context.primary_conversion))
    model_candidates = [
        BUSINESS_MODEL_BY_CONVERSION[item]
        for item in observed
        if item in BUSINESS_MODEL_BY_CONVERSION
    ]
    observed_model = model_candidates[0] if model_candidates else "unknown"
    conflicts: list[str] = []
    if supplied and observed:
        supplied_model = BUSINESS_MODEL_BY_CONVERSION.get(supplied)
        observed_models = {BUSINESS_MODEL_BY_CONVERSION.get(item) for item in observed}
        if supplied not in observed and supplied_model not in observed_models:
            conflicts.append(
                f"Supplied conversion '{supplied}' conflicts with observed conversions: "
                + ", ".join(observed)
                + "."
            )

    if conflicts and audit_mode == AuditMode.CURRENT_STATE:
        status = ContextStatus.CONFLICT
        resolution_required = True
    elif conflicts:
        status = ContextStatus.OVERRIDDEN
        resolution_required = False
    elif supplied or observed:
        status = ContextStatus.ALIGNED
        resolution_required = False
    else:
        status = ContextStatus.UNKNOWN
        resolution_required = False

    return ContextAssessment(
        audit_mode=audit_mode,
        status=status,
        observed_business_model=observed_model,
        observed_conversions=observed,
        supplied_conversion=supplied,
        conflicts=conflicts,
        resolution_required=resolution_required,
    )
