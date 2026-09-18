"""Versioned, reproducible 0-100 scoring."""

from __future__ import annotations

from collections import defaultdict

from ..models import CategoryScore, EvidenceDocument, Finding, ObservationStatus, Severity

CATEGORY_WEIGHTS = {
    "content": 0.25,
    "conversion": 0.20,
    "seo": 0.20,
    "competitive": 0.15,
    "brand": 0.10,
    "growth": 0.10,
}

SEVERITY_DEDUCTIONS = {
    Severity.INFO: 2.0,
    Severity.LOW: 6.0,
    Severity.MEDIUM: 12.0,
    Severity.HIGH: 22.0,
    Severity.CRITICAL: 35.0,
}

TECHNICAL_CATEGORIES = {"content", "conversion", "seo", "brand"}


def calculate_scores(
    evidence: EvidenceDocument,
    findings: list[Finding],
) -> tuple[dict[str, CategoryScore], float | None, float, float, str]:
    if evidence.fetch.status not in {ObservationStatus.OBSERVED, ObservationStatus.RENDER_REQUIRED}:
        unavailable_categories = {
            name: CategoryScore(None, 0.0, 0.0, "insufficient_evidence")
            for name in CATEGORY_WEIGHTS
        }
        return unavailable_categories, None, 0.0, 0.0, "insufficient_evidence"

    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.category].append(finding)

    static_confidence = 0.45 if evidence.fetch.status is ObservationStatus.RENDER_REQUIRED else 0.95
    categories: dict[str, CategoryScore] = {}
    for name in CATEGORY_WEIGHTS:
        if name not in TECHNICAL_CATEGORIES:
            categories[name] = CategoryScore(None, 0.0, 0.0, "not_tested")
            continue
        deduction = sum(
            SEVERITY_DEDUCTIONS[item.severity] * item.confidence for item in grouped.get(name, [])
        )
        categories[name] = CategoryScore(
            score=round(max(0.0, 100.0 - deduction), 1),
            confidence=static_confidence,
            coverage=0.7,
        )

    tested_weight = sum(CATEGORY_WEIGHTS[name] for name in TECHNICAL_CATEGORIES)
    weighted = sum(
        (categories[name].score or 0.0) * CATEGORY_WEIGHTS[name] for name in TECHNICAL_CATEGORIES
    )
    overall = round(weighted / tested_weight, 1)
    coverage = round(tested_weight, 2)
    confidence = round(static_confidence * coverage, 2)
    return categories, overall, confidence, coverage, "partial"
