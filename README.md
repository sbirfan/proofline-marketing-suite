# Proofline Marketing Suite

Evidence-first marketing audits for Claude Code, with structured collection states, deterministic checks,
reproducible scoring, and source-backed recommendations.

> **Status:** stable (`2.3.0 — Reporting Integrity`). The suite includes evidence-backed audit, analysis,
> reporting, and review-ready campaign skills for copy, email, social, ads, launches, and proposals. Generation
> requires explicit context and produces drafts only; it never publishes, sends, launches, signs, or mutates an
> external account without separate approval.

## Why this project exists

Many automated audits collapse “not observed” into “does not exist” and present model impressions as facts.
This project uses a stricter pipeline:

```text
collection → evidence → deterministic findings → scores → interpretation → reports
```

Blocked requests, TLS failures, malformed responses, missing resources, and render-required pages remain
different states. Scores use a single 0–100 scale, with confidence and coverage reported separately.

## Delivery phases

| Phase | Version | Status | Completed |
|---|---|---|---|
| Foundation | 0.1.0 | Complete | 2026-09-18 |
| Evidence Engine | 0.2.0 | Complete | 2026-09-18 |
| Technical Audit | 0.3.0 | Complete | 2026-09-18 |
| Security and packaging | 0.4.0 | Complete | 2026-09-18 |
| Full Marketing Audit | 0.5.0 | Complete | 2026-09-18 |
| Client reporting | 0.6.0 | Complete | 2026-09-18 |
| Analysis capabilities | 0.7.0 | Complete | 2026-09-18 |
| Campaign capabilities | 0.8.0 | Complete | 2026-09-18 |
| Public beta | 0.9.0 | Complete | 2026-09-18 |
| Stable release | 1.0.0 | Complete | 2026-09-18 |
| Proofline compatibility rename | 1.1.0 | Complete | 2026-09-19 |
| Proofline namespace migration | 2.0.0 | Complete | 2026-09-19 |
| Context guide hotfix | 2.0.1 | Complete | 2026-09-19 |
| Context Integrity | 2.1.0 | Complete | 2026-09-19 |
| Evidence Integrity | 2.2.0 | Complete | 2026-09-19 |
| Reporting Integrity | 2.3.0 | Complete | 2026-09-19 |

The detailed, dated record of what each phase built and deferred is maintained in
[Build history](docs/BUILD_HISTORY.md).

## Start here — no coding experience required

Follow the [beginner setup and usage guide](docs/beginner-guide.md) for step-by-step Windows, macOS, and Linux
instructions, your first website audit, PDF reporting, focused analysis commands, campaign drafting examples,
and troubleshooting.

Never reuse business details from a documentation example. Supply the audited site's real audience, offer, and
conversion, or mark them unknown. Proofline stops for confirmation when supplied context materially conflicts
with observed business or conversion evidence.

## Install for development

```bash
git clone https://github.com/sbirfan/proofline-marketing-suite.git
cd proofline-marketing-suite
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
proofline doctor
```

Run an audit:

```bash
proofline audit https://example.com --format markdown
proofline audit https://example.com --format json --output .audit/example.json
proofline audit https://example.com --browser-fallback
proofline audit https://example.com --format html --output report.html
proofline audit https://example.com --format pdf --output report.pdf
proofline audit https://example.com --audience "Operations leaders" --offer "Demo"
proofline audit https://example.com --primary-conversion "checkout"
proofline audit https://example.com --primary-conversion "book a demo" --audit-mode planned_funnel
proofline audit https://example.com --competitor https://competitor.example --comparison-dimension positioning --confirm-competitors
```

Run checks:

```bash
ruff check .
mypy src
pytest --cov=proofline_marketing
python scripts/validate_release.py
python -m build
```

Public-beta compatibility, diagnostics, examples, and support-request guidance are documented in the
[public beta guide](docs/public-beta.md).

## Claude Code plugin

Load the repository during local development:

```bash
claude --plugin-dir .
```

Then use:

```text
/proofline:health
/proofline:audit example.com
/proofline:seo example.com
/proofline:landing example.com
/proofline:competitors example.com
/proofline:brand example.com
/proofline:funnel example.com
/proofline:report .audit/example.json
/proofline:copy
/proofline:emails
/proofline:social
/proofline:ads
/proofline:launch
/proofline:proposal
```

Version 2.0 completes the Proofline namespace migration. Claude commands use `/proofline:*`, Python imports use
`proofline_marketing`, and the command line uses `proofline`. See the
[Proofline migration guide](docs/renaming-to-proofline.md) when upgrading from 1.x.

Plugin instructions treat all retrieved material as untrusted evidence. Specialist agents receive structured
evidence rather than browsing independently.

## Current capabilities

- Verified-TLS HTTP fetches with timeout and response-size limits
- Public-address enforcement for initial URLs and redirect targets
- Redirect-chain, final-URL, response-size, content-type, encoding, and timing provenance
- Explicit observed, blocked, failed, and render-required states
- Static HTML extraction that excludes script, style, SVG, templates, and framework payloads from visible text
- Visibility-aware exclusion of hidden, aria-hidden, `display:none`, `visibility:hidden`, canvas, and noscript text
- Structured robots.txt groups, rules, crawl delays, sitemap declarations, digests, and access evaluation
- Bounded recursive sitemap-index and gzip traversal with scope, depth, count, and decompression limits
- Page language, visible word counts, internal/external link classification, link text, and form requirements
- Deterministic checks for titles, descriptions, headings, indexability, canonicals, image alternatives,
  structured data, Open Graph metadata, and conversion actions
- Deterministic business-model and conversion detection with a blocking context-conflict state
- Explicit current-state, planned-funnel, and confirmed-override audit modes
- Deterministic checks for thin visible content, form friction, generic actions, link availability, robots access,
  sitemap outcomes, and malformed structured data
- Versioned agent brief/result contracts that exclude raw webpage text from specialist hand-offs
- Versioned JSON schemas and explicit finding-ID rules for 0–100 category scores
- Confidence and evidence coverage distinct from score
- Machine-readable represented, discovered, unrepresented, and unavailable URL scope
- Page/resource claim scopes that prevent single-page evidence from becoming site-wide absence claims
- Prioritized JSON and Markdown output with evidence-availability and methodology sections
- Prompt-injection boundaries in the audit skill and every specialist agent
- Prompt-boundary neutralization, recursive secret redaction, credential-safe URLs, and bounded prompt inputs
- Reproducible source/wheel builds with metadata validation and clean-environment CLI installation in CI
- Optional browser-extra smoke checks, CodeQL scanning, Dependabot updates, and checksummed tag artifacts
- Six structured specialist briefs with explicit business context, limitations, and prohibited actions
- Confirmed competitor collection under the same bounded policy, with comparable states and retrieval provenance
- Concurrent caller-supplied specialist adapters with schema validation and isolated failure recording
- Deterministic score synthesis from bounded dimension ratings; agents never calculate canonical scores
- Self-contained, escaped, accessible, print-ready HTML reports with configurable branding
- Deterministic multi-page PDF reports with repeated headers, footers, page numbers, and wrapping content
- Client-report gates that reject unresolved context conflicts, unsupported site-wide claims, and unsourced findings
- Context, evidence-scope, and finding-scope disclosure in HTML and PDF reports
- Six focused analysis/report skills with shared evidence, source, limitation, and recommendation contracts
- Six review-only campaign skills with approved-claim tracking, assumptions, measurement, and approval gates

See [architecture](docs/architecture.md), [evidence model](docs/evidence-model.md),
[scoring](docs/scoring.md), [full marketing audit](docs/full-marketing-audit.md),
[client reporting](docs/client-reporting.md), [security](docs/security.md),
[skill catalog](docs/skills.md), [beginner guide](docs/beginner-guide.md),
[public beta guide](docs/public-beta.md), and
[support policy](docs/support.md), [migration guide](docs/migration.md),
[Proofline rename guide](docs/renaming-to-proofline.md),
[1.0 release notes](docs/release-notes-1.0.md), and [development](docs/development.md).

## Important limitations

The current release analyzes one target page while using robots.txt and sitemaps for discovery evidence; it
does not yet schedule every discovered page. It detects likely app shells and can render them when requested and
optional Playwright support is installed. Competitive and growth scores remain `not_tested` unless validated
specialist assessments are supplied. A partial overall covers tested categories only. The CLI creates briefs but
does not invoke an external language model. Competitor collection requires explicit target confirmation.

Audit output is decision support, not a guarantee of search rankings, accessibility compliance, privacy
compliance, or revenue impact. Manually verify client-facing claims.

## Acknowledgements

This project was inspired in part by
[AI Marketing Suite for Claude Code](https://github.com/zubair-trabzada/ai-marketing-claude)
by Zubair Trabzada.

Proofline Marketing Suite is an independent implementation with a new architecture, evidence model, scoring
system, crawling pipeline, testing strategy, and agent design. No source history was imported.

## License

[MIT](LICENSE) © 2026 Syed Irfan.
