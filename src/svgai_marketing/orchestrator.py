"""Evidence-first audit orchestration."""

from __future__ import annotations

from .analyzers.technical import analyze_page
from .crawler.collector import EvidenceCollector
from .models import AuditResult, utc_now
from .scoring.engine import calculate_scores


def run_audit(url: str, *, timeout: float = 15.0, browser_fallback: bool = False) -> AuditResult:
    evidence = EvidenceCollector(timeout=timeout, browser_fallback=browser_fallback).collect(url)
    findings = analyze_page(evidence.page) if evidence.page else []
    categories, overall, confidence, coverage, status = calculate_scores(evidence, findings)
    return AuditResult(
        schema_version="2.0",
        target_url=evidence.target_url,
        generated_at=utc_now(),
        evidence=evidence,
        findings=findings,
        categories=categories,
        overall=overall,
        confidence=confidence,
        coverage=coverage,
        status=status,
    )
