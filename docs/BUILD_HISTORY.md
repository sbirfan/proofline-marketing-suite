# Build history

This ledger records what was built in each delivery phase, when it was completed, and what remains outside
that phase. Dates use UTC and refer to repository implementation work, not promises about future delivery.

## Phase summary

| Phase | Version | Status | Started | Completed | Repository record |
|---|---|---|---|---|---|
| Foundation | 0.1.0 | Complete | 2026-09-18 | 2026-09-18 | PR #1, commit `652f82b6` |
| Evidence Engine | 0.2.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/evidence-engine` |
| Technical Audit | 0.3.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/technical-audit` |
| Security and packaging | 0.4.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/security-packaging` |
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

## Phase 0.3.0 — Technical Audit

Completed on 2026-09-18.

Built:

- Expanded deterministic SEO, content, conversion, brand, robots, and sitemap findings with stable IDs
- Explicit score version `3.0`, finding-ID penalties, category-specific evidence coverage, and deterministic
  behavior for unregistered future findings
- Structured technical-agent briefs that contain finding IDs, evidence URLs, limitations, prohibited actions,
  and the shared untrusted-content policy without raw webpage text
- JSON schemas for specialist-agent briefs and specialist-agent results
- Audit result provenance for both schema version and score version
- Severity-prioritized Markdown findings plus evidence-availability and scoring-methodology sections
- Regression tests for new checks, blocked-versus-missing sitemap semantics, score rules, and agent briefs

Quality record at phase completion:

- Ruff formatting and lint: passed
- Strict mypy: passed
- Pytest: 29 passed, including JSON Schema contract validation
- Total local coverage: 84%
- GitHub CI: required before merge on Linux, macOS, and Windows

Still deferred to later phases:

- External language-model invocation from the Python runtime
- Complete accessibility, measurement, broken-link, performance, and consent analysis
- Content, conversion, competitive, brand, and growth specialist synthesis
- HTML and PDF report rendering

## Phase 0.4.0 — Security and Packaging

Completed on 2026-09-18.

Built:

- Recursive redaction for common access-token formats, authorization values, sensitive mapping keys, URL
  credentials, and secret-bearing query parameters
- Untrusted-text sanitization that removes control characters, neutralizes evidence-boundary delimiters, and
  caps content before it can enter an agent prompt
- URL length and redirect limits plus validation of the response's final URL, including custom transport paths
- A standard-library release validator for synchronized package/plugin versions, closed schemas, skill
  frontmatter, and documented untrusted-content boundaries
- Reproducible source and wheel builds, followed by clean-environment wheel installation and CLI smoke testing
  as a dedicated GitHub CI job
- Security regression tests and an expanded threat-model document

Quality record at phase completion:

- Ruff formatting and lint: passed
- Strict mypy: passed
- Pytest and JSON Schema validation: required locally and in GitHub CI
- Build, metadata validation, wheel installation, and installed CLI smoke test: required in GitHub CI

Still deferred to later phases:

- Authenticated crawling and storage of private client data
- External specialist-model execution
- Signing or publishing packages to a public registry
- HTML and PDF report rendering

## Maintenance rule

Every phase pull request must update this file, the README capability/limitation sections, the changelog, and
the package/plugin version when applicable. A phase is marked complete only after local quality gates and the
configured GitHub CI pass. The feature PR is then merged to `develop`, post-merge CI is verified, and the
release PR is merged to `main` before work begins on the next phase.
