"""Evidence-first audit orchestration."""

from __future__ import annotations

from collections.abc import Mapping

from .agents.specialists import (
    SpecialistExecutor,
    build_specialist_briefs,
    execute_specialists,
)
from .analyzers.technical import analyze_evidence
from .crawler.collector import EvidenceCollector
from .models import AuditResult, BusinessContext, EvidenceDocument, utc_now
from .scoring.engine import calculate_scores, synthesize_specialist_scores


def run_audit(
    url: str,
    *,
    timeout: float = 15.0,
    browser_fallback: bool = False,
    business_context: BusinessContext | None = None,
    specialist_executors: Mapping[str, SpecialistExecutor] | None = None,
    precollected_evidence: EvidenceDocument | None = None,
    precollected_competitors: Mapping[str, EvidenceDocument] | None = None,
) -> AuditResult:
    """Collect once, fan out immutable briefs, then synthesize validated results."""
    context = business_context or BusinessContext()
    collector = EvidenceCollector(timeout=timeout, browser_fallback=browser_fallback)
    evidence = precollected_evidence or collector.collect(url)
    competitor_evidence = dict(precollected_competitors or {})
    if context.competitors_confirmed:
        for competitor_url in context.competitor_urls:
            if competitor_url not in competitor_evidence:
                competitor_evidence[competitor_url] = collector.collect(competitor_url)
    findings = analyze_evidence(evidence)
    categories, overall, confidence, coverage, status = calculate_scores(evidence, findings)
    briefs = build_specialist_briefs(evidence, findings, context, competitor_evidence)
    results, failures = execute_specialists(briefs, specialist_executors)
    if results:
        categories, overall, confidence, coverage, status = synthesize_specialist_scores(
            categories, results
        )
    return AuditResult(
        schema_version="2.0",
        score_version="5.0",
        target_url=evidence.target_url,
        generated_at=utc_now(),
        evidence=evidence,
        findings=findings,
        categories=categories,
        overall=overall,
        confidence=confidence,
        coverage=coverage,
        status=status,
        agent_briefs=briefs,
        agent_results=results,
        agent_failures=failures,
        business_context=context.to_dict(),
        competitive_evidence={
            target: item.to_dict() for target, item in competitor_evidence.items()
        },
    )
