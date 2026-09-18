"""Objective page checks. Models should interpret, not rediscover, these facts."""

from __future__ import annotations

from ..models import EvidenceReference, Finding, PageEvidence, Severity


def _reference(page: PageEvidence, selector: str, value: object) -> list[EvidenceReference]:
    return [
        EvidenceReference(
            url=page.url,
            source_type="html",
            selector=selector,
            observed_value=value,
        )
    ]


def analyze_page(page: PageEvidence) -> list[Finding]:
    findings: list[Finding] = []
    if not page.title:
        findings.append(
            Finding(
                id="seo.title.missing",
                category="seo",
                severity=Severity.HIGH,
                claim="The page does not contain a title element.",
                evidence=_reference(page, "title", None),
                confidence=1.0,
                recommendation="Add a concise, descriptive title aligned with search intent.",
            )
        )
    elif not 15 <= len(page.title) <= 65:
        findings.append(
            Finding(
                id="seo.title.length",
                category="seo",
                severity=Severity.LOW,
                claim=f"The page title is {len(page.title)} characters long.",
                evidence=_reference(page, "title", page.title),
                confidence=1.0,
                recommendation="Review the title for clarity and likely search-result truncation.",
            )
        )
    if not page.meta_description:
        findings.append(
            Finding(
                id="seo.meta_description.missing",
                category="seo",
                severity=Severity.MEDIUM,
                claim="The page does not contain a meta description.",
                evidence=_reference(page, 'meta[name="description"]', None),
                confidence=1.0,
                recommendation="Write a unique description that states the value proposition.",
            )
        )
    h1s = page.headings.get("h1", [])
    if not h1s:
        findings.append(
            Finding(
                id="content.h1.missing",
                category="content",
                severity=Severity.MEDIUM,
                claim="No H1 heading was detected.",
                evidence=_reference(page, "h1", []),
                confidence=1.0,
                recommendation="Add one clear page-level heading.",
            )
        )
    elif len(h1s) > 1:
        findings.append(
            Finding(
                id="content.h1.multiple",
                category="content",
                severity=Severity.LOW,
                claim=f"The page contains {len(h1s)} H1 headings.",
                evidence=_reference(page, "h1", h1s),
                confidence=1.0,
                recommendation="Confirm the heading hierarchy communicates one primary topic.",
            )
        )
    missing_alt = [image.get("src") for image in page.images if image.get("alt") is None]
    if missing_alt:
        findings.append(
            Finding(
                id="accessibility.image_alt.missing",
                category="brand",
                severity=Severity.MEDIUM,
                claim=f"{len(missing_alt)} image(s) omit the alt attribute.",
                evidence=_reference(page, "img:not([alt])", missing_alt),
                confidence=1.0,
                recommendation=(
                    "Add useful alt text for informative images and empty alt text "
                    "for decorative images."
                ),
            )
        )
    if "noindex" in page.robots_meta:
        findings.append(
            Finding(
                id="seo.indexing.noindex",
                category="seo",
                severity=Severity.HIGH,
                claim="The page instructs compliant crawlers not to index it.",
                evidence=_reference(page, 'meta[name="robots"]', page.robots_meta),
                confidence=1.0,
                recommendation="Confirm noindex is intentional before changing it.",
            )
        )
    if not page.canonical:
        findings.append(
            Finding(
                id="seo.canonical.missing",
                category="seo",
                severity=Severity.LOW,
                claim="No canonical link was detected.",
                evidence=_reference(page, 'link[rel="canonical"]', None),
                confidence=1.0,
                recommendation=(
                    "Declare the preferred URL when duplicates or URL variants are possible."
                ),
            )
        )
    if not page.open_graph:
        findings.append(
            Finding(
                id="brand.open_graph.missing",
                category="brand",
                severity=Severity.LOW,
                claim="No Open Graph metadata was detected.",
                evidence=_reference(page, 'meta[property^="og:"]', {}),
                confidence=1.0,
                recommendation="Add share title, description, image, and canonical URL metadata.",
            )
        )
    if not page.buttons and not page.forms:
        findings.append(
            Finding(
                id="conversion.action.missing",
                category="conversion",
                severity=Severity.MEDIUM,
                claim="No button or form was detected in the static page markup.",
                evidence=_reference(page, "button, form", []),
                confidence=0.9,
                recommendation=(
                    "Provide a clear next action or verify it appears in rendered content."
                ),
            )
        )
    if not page.json_ld:
        findings.append(
            Finding(
                id="seo.structured_data.missing",
                category="seo",
                severity=Severity.INFO,
                claim="No JSON-LD structured data was detected.",
                evidence=_reference(page, 'script[type="application/ld+json"]', []),
                confidence=1.0,
                recommendation=(
                    "Add only schema types that accurately describe visible page content."
                ),
            )
        )
    return findings
