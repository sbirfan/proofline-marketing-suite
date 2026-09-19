"""Accessible, print-ready HTML rendering from the canonical audit result."""

from __future__ import annotations

import re
from dataclasses import dataclass
from html import escape

from ..models import AuditResult


@dataclass(slots=True, frozen=True)
class ReportBrand:
    name: str = "Proofline Marketing Suite"
    primary_color: str = "#17324d"
    accent_color: str = "#0f766e"
    footer: str = "Evidence-first marketing audit"

    def __post_init__(self) -> None:
        for color in (self.primary_color, self.accent_color):
            if not re.fullmatch(r"#[0-9a-fA-F]{6}", color):
                raise ValueError("brand colors must use six-digit hexadecimal notation")


def render_html(result: AuditResult, brand: ReportBrand | None = None) -> str:
    """Render a self-contained report without recalculating audit semantics."""
    brand = brand or ReportBrand()
    score = "Unavailable" if result.overall is None else f"{result.overall:.1f}/100"
    rows = "".join(
        "<tr>"
        f"<th scope='row'>{escape(name.title())}</th>"
        f"<td>{'Not tested' if value.score is None else f'{value.score:.1f}'}</td>"
        f"<td>{value.confidence:.0%}</td><td>{value.coverage:.0%}</td>"
        f"<td>{escape(value.status.replace('_', ' '))}</td></tr>"
        for name, value in result.categories.items()
    )
    findings = (
        "".join(
            "<article class='finding'>"
            f"<h3>{escape(item.claim)}</h3>"
            f"<p><span class='badge'>{escape(str(item.severity))}</span> "
            f"<code>{escape(item.id)}</code></p>"
            f"<p>{escape(item.recommendation or 'No recommendation recorded.')}</p>"
            "<ul>"
            + "".join(
                f"<li><a href='{escape(ref.url, quote=True)}'>{escape(ref.url)}</a></li>"
                for ref in item.evidence
            )
            + "</ul></article>"
            for item in result.findings
        )
        or "<p>No deterministic findings were produced from the available evidence.</p>"
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width">
<title>Marketing audit - {escape(result.target_url)}</title>
<style>
:root{{--primary:{escape(brand.primary_color)};--accent:{escape(brand.accent_color)}}}
*{{box-sizing:border-box}}
body{{font:16px/1.5 system-ui,sans-serif;color:#17202a;margin:0}}
main{{max-width:980px;margin:auto;padding:40px}}
header{{border-bottom:5px solid var(--accent);padding-bottom:20px}}
h1,h2,h3{{color:var(--primary);line-height:1.2}}
.summary{{display:flex;gap:24px;flex-wrap:wrap;margin:24px 0}}
.metric{{background:#f3f6f8;border-radius:8px;padding:16px;min-width:160px}}
.metric strong{{display:block;font-size:1.5rem}}
table{{border-collapse:collapse;width:100%;margin:20px 0}}
th,td{{padding:10px;border:1px solid #ccd5dc;text-align:left}}
thead th{{background:var(--primary);color:white}}
.finding{{break-inside:avoid;border-left:4px solid var(--accent)}}
.finding{{padding:2px 16px;margin:18px 0}}
.badge{{background:#e5f3f1;border-radius:99px;padding:3px 9px}}
a{{color:#075985;overflow-wrap:anywhere}}
footer{{border-top:1px solid #ccd5dc;margin-top:40px}}
footer{{padding-top:12px;color:#52606d}}
@media print{{
  main{{max-width:none;padding:12mm}}
  a{{color:inherit}}
  .finding{{page-break-inside:avoid}}
}}
</style></head><body><main>
<header><p>{escape(brand.name)}</p><h1>Marketing Audit</h1>
<p>{escape(result.target_url)}</p></header>
<section class="summary" aria-label="Audit summary">
<div class="metric"><span>Status</span><strong>{escape(result.status)}</strong></div>
<div class="metric"><span>Overall</span><strong>{score}</strong></div>
<div class="metric"><span>Confidence</span><strong>{result.confidence:.0%}</strong></div>
<div class="metric"><span>Coverage</span><strong>{result.coverage:.0%}</strong></div></section>
<section><h2>Category scores</h2><table><thead><tr>
<th>Category</th><th>Score</th><th>Confidence</th><th>Coverage</th><th>Status</th>
</tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Prioritized findings</h2>{findings}</section>
<section><h2>Methodology</h2>
<p>Score version {escape(result.score_version)}. Scores are produced by versioned rules.
Confidence and coverage are reported separately. Missing or blocked evidence is not treated
as absence.</p></section>
<footer>{escape(brand.footer)} - Generated {escape(result.generated_at)}</footer>
</main></body></html>"""
