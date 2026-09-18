# SVG AI Marketing Suite

Evidence-first marketing audits for Claude Code, with structured collection states, deterministic checks,
reproducible scoring, and source-backed recommendations.

> **Status:** alpha (`0.8.0 — Campaign Capabilities`). The suite now includes evidence-backed audit, analysis,
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
| Public beta | 0.9.0 | Planned | — |
| Stable release | 1.0.0 | Planned | — |

The detailed, dated record of what each phase built and deferred is maintained in
[Build history](docs/BUILD_HISTORY.md).

## Install for development

```bash
git clone https://github.com/sbirfan/svgai-marketing-suite.git
cd svgai-marketing-suite
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

Run an audit:

```bash
svgai-marketing audit https://example.com --format markdown
svgai-marketing audit https://example.com --format json --output .audit/example.json
svgai-marketing audit https://example.com --browser-fallback
svgai-marketing audit https://example.com --format html --output report.html
svgai-marketing audit https://example.com --format pdf --output report.pdf
svgai-marketing audit https://example.com --audience "Operations leaders" --offer "Demo"
svgai-marketing audit https://example.com --competitor https://competitor.example --comparison-dimension positioning --confirm-competitors
```

Run checks:

```bash
ruff check .
mypy src
pytest --cov=svgai_marketing
python scripts/validate_release.py
python -m build
```

## Claude Code plugin

Load the repository during local development:

```bash
claude --plugin-dir .
```

Then use:

```text
/svgai-marketing:health
/svgai-marketing:audit example.com
/svgai-marketing:seo example.com
/svgai-marketing:landing example.com
/svgai-marketing:competitors example.com
/svgai-marketing:brand example.com
/svgai-marketing:funnel example.com
/svgai-marketing:report .audit/example.json
/svgai-marketing:copy
/svgai-marketing:emails
/svgai-marketing:social
/svgai-marketing:ads
/svgai-marketing:launch
/svgai-marketing:proposal
```

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
- Deterministic checks for thin visible content, form friction, generic actions, link availability, robots access,
  sitemap outcomes, and malformed structured data
- Versioned agent brief/result contracts that exclude raw webpage text from specialist hand-offs
- Versioned JSON schemas and explicit finding-ID rules for 0–100 category scores
- Confidence and evidence coverage distinct from score
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
- Six focused analysis/report skills with shared evidence, source, limitation, and recommendation contracts
- Six review-only campaign skills with approved-claim tracking, assumptions, measurement, and approval gates

See [architecture](docs/architecture.md), [evidence model](docs/evidence-model.md),
[scoring](docs/scoring.md), [full marketing audit](docs/full-marketing-audit.md),
[client reporting](docs/client-reporting.md), [security](docs/security.md),
[skill catalog](docs/skills.md), and [development](docs/development.md).

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

SVG AI Marketing Suite is an independent implementation with a new architecture, evidence model, scoring
system, crawling pipeline, testing strategy, and agent design. No source history was imported.

## License

[MIT](LICENSE) © 2026 Syed Irfan.
