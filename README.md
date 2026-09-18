# SVG AI Marketing Suite

Evidence-first marketing audits for Claude Code, with structured collection states, deterministic checks,
reproducible scoring, and source-backed recommendations.

> **Status:** alpha (`0.2.0 — Evidence Engine`). Public-page evidence collection, recursive sitemap discovery,
> structured robots analysis, visibility-aware HTML extraction, deterministic findings, partial scoring, and
> JSON/Markdown reporting are functional. Multi-page audit scheduling, competitor research, and full specialist
> synthesis remain roadmap work.

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
| Technical Audit | 0.3.0 | Planned | — |
| Full Marketing Audit | 0.5.0 | Planned | — |
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
```

Run checks:

```bash
ruff check .
mypy src
pytest --cov=svgai_marketing
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
- Versioned JSON schemas and 0–100 category scores
- Confidence and evidence coverage distinct from score
- JSON and Markdown output
- Prompt-injection boundaries in the audit skill and every specialist agent

See [architecture](docs/architecture.md), [evidence model](docs/evidence-model.md),
[scoring](docs/scoring.md), and [development](docs/development.md).

## Important limitations

The current release analyzes one target page while using robots.txt and sitemaps for discovery evidence; it
does not yet schedule an audit of every discovered page. It detects likely app shells and can render them when
`--browser-fallback` is requested and optional Playwright support is installed. Competitive and growth scores
remain `not_tested` until relevant evidence exists. A partial overall score covers tested categories only and
is labeled accordingly.

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
