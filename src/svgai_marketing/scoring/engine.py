"""Versioned, rule-based 0-100 scoring with independent evidence coverage."""

from __future__ import annotations

from collections import defaultdict

from ..models import CategoryScore, EvidenceDocument, Finding, ObservationStatus

SCORE_VERSION = "3.0"
CATEGORY_WEIGHTS = {
    "content": 0.25,
    "conversion": 0.20,
    "seo": 0.20,
    "competitive": 0.15,
    "brand": 0.10,
    "growth": 0.10,
}

FINDING_PENALTIES = {
    "seo.title.missing": 20.0,
    "seo.title.length": 4.0,
    "seo.meta_description.missing": 10.0,
    "seo.meta_description.length": 3.0,
    "seo.indexing.noindex": 25.0,
    "seo.canonical.missing": 5.0,
    "seo.structured_data.missing": 2.0,
    "seo.structured_data.invalid_json": 10.0,
    "seo.internal_links.none": 5.0,
    "seo.robots.target_disallowed": 25.0,
    "seo.sitemap.not_found": 8.0,
    "seo.sitemap.audit_blocked": 0.0,
    "seo.sitemap.audit_truncated": 0.0,
    "content.h1.missing": 15.0,
    "content.h1.multiple": 4.0,
    "content.visible_text.thin": 8.0,
    "conversion.action.missing": 15.0,
    "conversion.form.fields_many": 10.0,
    "conversion.action.generic": 4.0,
    "accessibility.image_alt.missing": 10.0,
    "brand.open_graph.missing": 6.0,
    "brand.open_graph.incomplete": 3.0,
}


def _technical_coverage(evidence: EvidenceDocument) -> dict[str, float]:
    if evidence.page is None:
        return {"content": 0.0, "conversion": 0.0, "seo": 0.0, "brand": 0.0}
    robots_coverage = 0.2 if evidence.robots.get("status") in {"observed", "not_found"} else 0.0
    sitemap_coverage = 0.2 if evidence.sitemap.get("status") in {"observed", "not_found"} else 0.0
    return {
        "content": 0.85,
        "conversion": 0.75,
        "seo": min(1.0, 0.6 + robots_coverage + sitemap_coverage),
        "brand": 0.70,
    }


def calculate_scores(
    evidence: EvidenceDocument,
    findings: list[Finding],
) -> tuple[dict[str, CategoryScore], float | None, float, float, str]:
    if evidence.fetch.status not in {
        ObservationStatus.OBSERVED,
        ObservationStatus.RENDER_REQUIRED,
    }:
        unavailable = {
            name: CategoryScore(None, 0.0, 0.0, "insufficient_evidence")
            for name in CATEGORY_WEIGHTS
        }
        return unavailable, None, 0.0, 0.0, "insufficient_evidence"

    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.category].append(finding)

    collection_confidence = (
        0.45 if evidence.fetch.status is ObservationStatus.RENDER_REQUIRED else 0.95
    )
    coverage_by_category = _technical_coverage(evidence)
    categories: dict[str, CategoryScore] = {}
    for name in CATEGORY_WEIGHTS:
        coverage = coverage_by_category.get(name, 0.0)
        if coverage == 0.0:
            categories[name] = CategoryScore(None, 0.0, 0.0, "not_tested")
            continue
        deduction = sum(
            FINDING_PENALTIES.get(item.id, 0.0) * item.confidence for item in grouped.get(name, [])
        )
        categories[name] = CategoryScore(
            score=round(max(0.0, 100.0 - deduction), 1),
            confidence=round(collection_confidence * coverage, 2),
            coverage=coverage,
        )

    tested = [name for name, value in categories.items() if value.score is not None]
    if not tested:
        return categories, None, 0.0, 0.0, "insufficient_evidence"
    tested_weight = sum(CATEGORY_WEIGHTS[name] for name in tested)
    weighted_score = sum(
        (categories[name].score or 0.0) * CATEGORY_WEIGHTS[name] for name in tested
    )
    overall = round(weighted_score / tested_weight, 1)
    coverage = round(
        sum(categories[name].coverage * CATEGORY_WEIGHTS[name] for name in categories),
        2,
    )
    confidence = round(collection_confidence * coverage, 2)
    return categories, overall, confidence, coverage, "partial"
