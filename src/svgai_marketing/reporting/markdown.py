"""Markdown is the first canonical human-readable renderer."""

from __future__ import annotations

from ..models import AuditResult


def render_markdown(result: AuditResult) -> str:
    score = "Unavailable" if result.overall is None else f"{result.overall:.1f}/100"
    lines = [
        "# Marketing Audit",
        "",
        f"- Target: {result.target_url}",
        f"- Status: {result.status}",
        f"- Overall (tested categories only): {score}",
        f"- Confidence: {result.confidence:.0%}",
        f"- Coverage: {result.coverage:.0%}",
        "",
        "## Category scores",
        "",
        "| Category | Score | Confidence | Coverage | Status |",
        "|---|---:|---:|---:|---|",
    ]
    for name, category in result.categories.items():
        category_score = "—" if category.score is None else f"{category.score:.1f}"
        lines.append(
            f"| {name.title()} | {category_score} | {category.confidence:.0%} | "
            f"{category.coverage:.0%} | {category.status} |"
        )
    lines.extend(["", "## Findings", ""])
    if not result.findings:
        lines.append("No deterministic findings were produced from the available evidence.")
    for finding in result.findings:
        lines.extend(
            [
                f"### {finding.claim}",
                "",
                f"- ID: `{finding.id}`",
                f"- Category: {finding.category}",
                f"- Severity: {finding.severity}",
                f"- Confidence: {finding.confidence:.0%}",
                f"- Evidence: {finding.evidence[0].url} — `{finding.evidence[0].selector}`",
                f"- Recommendation: {finding.recommendation or 'None'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Interpretation notes",
            "",
            "Observed facts, interpretations, recommendations, and estimates are separate ",
            "concepts. Untested competitive and growth categories do not silently receive scores. ",
            "Revenue dollar ",
            "estimates require traffic, conversion, value, and close-rate inputs with sources.",
        ]
    )
    return "\n".join(lines)
