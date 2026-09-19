"""Objective page checks. Models should interpret, not rediscover, these facts."""

from __future__ import annotations

from ..models import EvidenceDocument, EvidenceReference, Finding, PageEvidence, Severity


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
    if page.meta_description and not 50 <= len(page.meta_description) <= 170:
        findings.append(
            Finding(
                id="seo.meta_description.length",
                category="seo",
                severity=Severity.LOW,
                claim=(f"The meta description is {len(page.meta_description)} characters long."),
                evidence=_reference(page, 'meta[name="description"]', page.meta_description),
                confidence=1.0,
                recommendation=(
                    "Review the description for useful search-result context and likely truncation."
                ),
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
    if page.visible_word_count < 150:
        findings.append(
            Finding(
                id="content.visible_text.thin",
                category="content",
                severity=Severity.LOW,
                claim=(
                    f"Only {page.visible_word_count} visible words were extracted from the page."
                ),
                evidence=_reference(page, "visible_text", {"word_count": page.visible_word_count}),
                confidence=0.85,
                recommendation=(
                    "Confirm the page answers its intended visitor questions; "
                    "do not add filler text."
                ),
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
    elif not {"og:title", "og:description", "og:image"}.issubset(page.open_graph):
        missing_open_graph = sorted(
            {"og:title", "og:description", "og:image"} - page.open_graph.keys()
        )
        findings.append(
            Finding(
                id="brand.open_graph.incomplete",
                category="brand",
                severity=Severity.LOW,
                claim="Important Open Graph fields are incomplete.",
                evidence=_reference(page, 'meta[property^="og:"]', {"missing": missing_open_graph}),
                confidence=1.0,
                recommendation="Add only the missing social sharing fields with accurate content.",
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
    if any(int(form.get("fields", 0)) > 8 for form in page.forms):
        findings.append(
            Finding(
                id="conversion.form.fields_many",
                category="conversion",
                severity=Severity.MEDIUM,
                claim="At least one form requests more than eight fields.",
                evidence=_reference(page, "form", page.forms),
                confidence=1.0,
                recommendation=(
                    "Confirm every requested field is necessary at this stage of the journey."
                ),
            )
        )
    generic_actions = {
        value
        for value in page.buttons
        if value.strip().lower() in {"click here", "go", "submit", "learn more"}
    }
    if generic_actions:
        findings.append(
            Finding(
                id="conversion.action.generic",
                category="conversion",
                severity=Severity.LOW,
                claim="One or more action labels do not describe the expected outcome.",
                evidence=_reference(page, "button, input[type=submit]", sorted(generic_actions)),
                confidence=0.95,
                recommendation="Use action copy that sets a clear expectation for the next step.",
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
    elif any(isinstance(item, dict) and item.get("_invalid") for item in page.json_ld):
        findings.append(
            Finding(
                id="seo.structured_data.invalid_json",
                category="seo",
                severity=Severity.MEDIUM,
                claim="At least one JSON-LD block is not valid JSON.",
                evidence=_reference(page, 'script[type="application/ld+json"]', {"valid": False}),
                confidence=1.0,
                recommendation="Correct the JSON syntax and validate the intended schema type.",
            )
        )
    internal_links = [item for item in page.links if item.get("kind") == "internal"]
    if not internal_links:
        findings.append(
            Finding(
                id="seo.internal_links.none",
                category="seo",
                severity=Severity.LOW,
                claim="No internal links were detected in the page markup.",
                evidence=_reference(page, "a[href]", page.links),
                confidence=0.95,
                recommendation=(
                    "Add useful paths to related content when the visitor journey supports it."
                ),
            )
        )
    return findings


def analyze_evidence(evidence: EvidenceDocument) -> list[Finding]:
    findings = analyze_page(evidence.page) if evidence.page else []
    robots_status = evidence.robots.get("status")
    if robots_status == "observed" and evidence.robots.get("search_engine_access") == "disallowed":
        findings.append(
            Finding(
                id="seo.robots.target_disallowed",
                category="seo",
                severity=Severity.HIGH,
                claim="robots.txt disallows the audited target for this crawler user agent.",
                evidence=[
                    EvidenceReference(
                        url=str(evidence.robots.get("url", evidence.target_url)),
                        source_type="robots",
                        observed_value={"search_engine_access": "disallowed"},
                    )
                ],
                confidence=1.0,
                recommendation=(
                    "Confirm the rule is intentional and test search-engine-specific "
                    "access separately."
                ),
                claim_scope="resource",
            )
        )
    sitemap_status = evidence.sitemap.get("status")
    if sitemap_status == "not_found":
        findings.append(
            Finding(
                id="seo.sitemap.not_found",
                category="seo",
                severity=Severity.MEDIUM,
                claim=(
                    "The conventional or declared sitemap resource returned a not-found response."
                ),
                evidence=[
                    EvidenceReference(
                        url=evidence.target_url,
                        source_type="sitemap",
                        observed_value={"status": "not_found"},
                    )
                ],
                confidence=0.95,
                recommendation=(
                    "Publish or declare a sitemap when the site benefits from URL discovery."
                ),
                claim_scope="resource",
            )
        )
    elif sitemap_status == "blocked":
        findings.append(
            Finding(
                id="seo.sitemap.audit_blocked",
                category="seo",
                severity=Severity.INFO,
                claim="The audit crawler was denied access to the sitemap resource.",
                evidence=[
                    EvidenceReference(
                        url=evidence.target_url,
                        source_type="sitemap",
                        observed_value={"status": "blocked"},
                    )
                ],
                confidence=1.0,
                recommendation=(
                    "Verify search-engine access with provider logs or a search-engine "
                    "inspection tool."
                ),
                claim_scope="resource",
            )
        )
    if evidence.sitemap.get("truncated") is True:
        findings.append(
            Finding(
                id="seo.sitemap.audit_truncated",
                category="seo",
                severity=Severity.INFO,
                claim="Sitemap discovery reached a configured safety limit.",
                evidence=[
                    EvidenceReference(
                        url=evidence.target_url,
                        source_type="sitemap",
                        observed_value=evidence.sitemap.get("limits"),
                    )
                ],
                confidence=1.0,
                recommendation=(
                    "Increase limits deliberately or sample sitemap segments separately."
                ),
                claim_scope="resource",
            )
        )
    return findings
