# Build history

This ledger records what was built in each delivery phase, when it was completed, and what remains outside
that phase. Dates use UTC and refer to repository implementation work, not promises about future delivery.

## Phase summary

| Phase | Version | Status | Started | Completed | Repository record |
|---|---|---|---|---|---|
| Foundation | 0.1.0 | Complete | 2026-09-18 | 2026-09-18 | PR #1, commit `652f82b6` |
| Evidence Engine | 0.2.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/evidence-engine` |
| Technical Audit | 0.3.0 | Planned | — | — | EPICs 07–09 and 15–17 |
| Security and packaging | 0.4.0 | Planned | — | — | EPICs 18–19 |
| Full Marketing Audit | 0.5.0 | Planned | — | — | EPICs 10–14 |
| Client reporting | 0.6.0 | Planned | — | — | EPIC 16 |
| Public beta | 0.9.0 | Planned | — | — | To be scoped |
| Stable release | 1.0.0 | Planned | — | — | EPIC 20 |

## Phase 0.1.0 — Foundation

Completed on 2026-09-18.

Built:

- Claude Code plugin manifest and namespaced health/audit skills
- Python package, CLI, canonical dataclasses, and initial JSON schemas
- Verified-TLS bounded static fetching with distinct failure states
- Static HTML, robots.txt, and sitemap collection
- Deterministic technical findings and initial 0–100 partial scoring
- JSON and Markdown reports sourced from one canonical audit result
- Six tool-free specialist agent definitions with prompt-injection boundaries
- Architecture, evidence, scoring, security, development, and contribution documentation
- Linux, macOS, and Windows CI with lint, strict typing, tests, schema checks, and coverage
- Independent implementation acknowledgement and MIT licensing

Deliberately deferred:

- Multi-page crawling and recursive sitemap traversal
- Public/private address enforcement
- Full rendered-browser workflow
- Specialist-agent orchestration and complete category scores
- HTML/PDF reports and additional marketing skills

## Phase 0.2.0 — Evidence Engine

Completed on 2026-09-18.

Built:

- Public-address validation for initial URLs and every followed redirect, blocking loopback, private, link-local,
  reserved, credential-bearing, and unsupported destinations before collection
- Fetch provenance for redirect chains, final URL, response type, response length, encoding, duration, status,
  and machine-readable failure reason
- Structured robots.txt parsing for user-agent groups, allow/disallow rules, crawl delays, sitemap declarations,
  access evaluation, line count, and SHA-256 content identity without placing raw instructions in evidence
- Bounded recursive traversal of sitemap indexes with depth, sitemap-count, URL-count, decompression, same-origin,
  deduplication, malformed XML, partial-failure, and truncation handling
- Visibility-aware HTML text that excludes script, style, SVG, template, canvas, noscript, hidden, aria-hidden,
  `display:none`, and `visibility:hidden` content
- Page language, visible word count, internal/external link classification, anchor text, required form-field counts,
  and submit-action extraction
- A stricter evidence schema covering fetch, page, robots, and sitemap evidence and rejecting unknown score categories
- Controlled fixtures and regression tests for the new collection states and parsers

Quality record at phase completion:

- Ruff formatting and lint: passed
- Strict mypy: passed
- Pytest: 25 passed locally, including JSON Schema contract validation
- Total local coverage: 83%
- HTML extraction: 96%; robots parser: 98%; score engine: 100%

Still deferred to later phases:

- Crawl scheduling across every discovered page
- Automatic installation of Playwright browser binaries
- Complete measurement, accessibility, broken-link, and performance analyzers
- Agent execution and synthesis inside the orchestrator
- Full six-category score coverage

## Maintenance rule

Every phase pull request must update this file, the README capability/limitation sections, the changelog, and
the package/plugin version when applicable. A phase is marked complete only after local quality gates and the
configured GitHub CI pass.
