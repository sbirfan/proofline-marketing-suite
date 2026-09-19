"""Versioned, rule-based 0-100 scoring with independent evidence coverage."""

from __future__ import annotations

from collections import defaultdict

from ..models import CategoryScore, EvidenceDocument, Finding, ObservationStatus

SCORE_VERSION = "5.0"
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


ASSESSMENT_VALUES = {"strong": 90.0, "adequate": 70.0, "weak": 40.0}
AGENT_CATEGORIES = {
    "content-strategist": "content",
    "conversion-analyst": "conversion",
    "competitive-analyst": "competitive",
    "brand-strategist": "brand",
    "growth-strategist": "growth",
}


def synthesize_specialist_scores(
    categories: dict[str, CategoryScore],
    agent_results: dict[str, dict[str, object]],
) -> tuple[dict[str, CategoryScore], float | None, float, float, str]:
    """Map bounded dimension ratings to canonical scores using fixed rules."""
    synthesized = dict(categories)
    for agent, category in AGENT_CATEGORIES.items():
        raw = agent_results.get(agent, {}).get("dimension_assessments", [])
        if not isinstance(raw, list):
            continue
        assessments = [item for item in raw if isinstance(item, dict)]
        scored = [item for item in assessments if item.get("rating") in ASSESSMENT_VALUES]
        if not scored:
            continue
        assessment_score = sum(ASSESSMENT_VALUES[str(item["rating"])] for item in scored) / len(
            scored
        )
        specialist_confidence = sum(float(item["confidence"]) for item in scored) / len(scored)
        assessment_coverage = len(scored) / len(assessments)
        existing = synthesized[category]
        score = assessment_score
        coverage = assessment_coverage
        confidence = specialist_confidence * coverage
        if existing.score is not None:
            score = existing.score * 0.6 + assessment_score * 0.4
            coverage = min(1.0, existing.coverage * 0.6 + assessment_coverage * 0.4)
            confidence = min(1.0, existing.confidence * 0.6 + specialist_confidence * 0.4)
        synthesized[category] = CategoryScore(
            round(score, 1), round(confidence, 2), round(coverage, 2)
        )

    tested = [name for name, value in synthesized.items() if value.score is not None]
    if not tested:
        return synthesized, None, 0.0, 0.0, "insufficient_evidence"
    tested_weight = sum(CATEGORY_WEIGHTS[name] for name in tested)
    overall = round(
        sum((synthesized[name].score or 0.0) * CATEGORY_WEIGHTS[name] for name in tested)
        / tested_weight,
        1,
    )
    coverage = round(
        sum(synthesized[name].coverage * CATEGORY_WEIGHTS[name] for name in synthesized), 2
    )
    confidence = round(
        sum(synthesized[name].confidence * CATEGORY_WEIGHTS[name] for name in synthesized), 2
    )
    status = "complete" if len(tested) == len(CATEGORY_WEIGHTS) else "partial"
    return synthesized, overall, confidence, coverage, status
