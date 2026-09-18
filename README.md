# SVG AI Marketing Suite

Evidence-first marketing audits for Claude Code, with structured collection states, deterministic checks,
reproducible scoring, and source-backed recommendations.

> **Status:** early alpha (`0.1.0`). The static technical audit is functional. Browser-rendered collection,
> multi-page crawling, competitor research, and full specialist synthesis remain roadmap work.

## Why this project exists

Many automated audits collapse “not observed” into “does not exist” and present model impressions as facts.
This project uses a stricter pipeline:

```text
collection → evidence → deterministic findings → scores → interpretation → reports
```

Blocked requests, TLS failures, malformed responses, missing resources, and render-required pages remain
different states. Scores use a single 0–100 scale, with confidence and coverage reported separately.

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
- Explicit observed, blocked, failed, and render-required states
- Static HTML extraction that excludes script, style, SVG, templates, and framework payloads from visible text
- robots.txt and sitemap discovery with preserved failure reasons
- Deterministic checks for titles, descriptions, headings, indexability, canonicals, image alternatives,
  structured data, Open Graph metadata, and conversion actions
- Versioned JSON schemas and 0–100 category scores
- Confidence and evidence coverage distinct from score
- JSON and Markdown output
- Prompt-injection boundaries in the audit skill and every specialist agent

See [architecture](docs/architecture.md), [evidence model](docs/evidence-model.md),
[scoring](docs/scoring.md), and [development](docs/development.md).

## Important limitations

The current release audits one public page using static HTML. It detects likely app shells and can render
them when `--browser-fallback` is requested and optional Playwright support is installed. Competitive and
growth scores remain `not_tested` until relevant
evidence exists. A partial overall score covers tested categories only and is labeled accordingly.

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
