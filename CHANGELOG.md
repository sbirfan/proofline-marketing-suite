# Changelog

All notable changes will be documented here. The project follows Semantic Versioning.

## [Unreleased]

### Added

- Beginner-friendly Windows, macOS, and Linux setup and usage guide with first-audit, PDF reporting, focused
  analysis, campaign drafting, troubleshooting, update, and safety instructions

## [1.0.0] - 2026-09-18

### Added

- Stable 1.x support, compatibility, and deprecation policy
- Public-beta-to-stable migration guide and 1.0 release notes
- Direct CLI regression coverage for diagnostics and stable subcommands

### Changed

- Project maturity classifier advanced to Production/Stable
- Package and plugin versions advanced to 1.0.0
- Release validation now requires the stable policy, migration, and release-note documents

## [0.9.0] - 2026-09-18

### Added

- Secret-free `doctor` diagnostics in human-readable and JSON formats
- Synthetic observed and blocked evidence examples using reserved `.test` URLs
- Machine-checkable should-invoke and should-not-invoke skill-routing evaluation cases
- Public beta compatibility, optional-extra, and support-request guidance

### Changed

- Release validation now checks evaluation IDs, skill references, and synthetic-example boundaries
- Package CI smoke-tests installed-wheel diagnostics
- Package and plugin versions advanced to 0.9.0

## [0.8.0] - 2026-09-18

### Added

- `/copy`, `/emails`, `/social`, `/ads`, `/launch`, and `/proposal` campaign skills
- Shared campaign output schema covering artifacts, claim review, assumptions, approvals, and measurement
- Structural tests for campaign skill discovery, untrusted-evidence boundaries, and external-action approval gates

### Changed

- Skill catalog and README now document the complete analysis and campaign command surface
- Package and plugin versions advanced to 0.8.0

## [0.7.0] - 2026-09-18

### Added

- `/seo`, `/landing`, `/competitors`, `/brand`, `/funnel`, and `/report` Claude Code skills
- Shared analysis-skill output schema for facts, interpretations, recommendations, limitations, and sources
- Skill catalog and structural/safety regression tests

### Changed

- Release validation now requires every evidence-consuming skill to declare an untrusted-content boundary
- README documents the expanded plugin command surface and split 0.7/0.8 capability phases

## [0.6.0] - 2026-09-18

### Added

- Accessible, responsive, print-ready HTML reports with escaped untrusted values and configurable branding
- Deterministic PDF renderer with repeated headers, footers, page numbers, tables, wrapping URLs, and sparse states
- `reports` optional dependency, installed-wheel CI smoke check, and synthetic multi-page visual regression example
- Client-reporting guide and HTML/PDF renderer regression tests

### Changed

- CLI now supports `--format html` and `--format pdf`; PDF output requires an explicit file path
- Package and plugin versions advanced to 0.6.0

## [0.5.0] - 2026-09-18

### Added

- Explicit business context with confirmed audience, offer, conversion, comparison, and sourced metric inputs
- Six structured specialist briefs built from one canonical target evidence document
- Confirmed competitor collection using the same bounded collector and normalized comparison evidence
- Concurrent caller-supplied specialist adapters with runtime validation and isolated failures
- Fixed specialist dimension rating synthesis for complete or partial six-category scoring
- Caller-managed resume inputs for target and competitor evidence without implicit persistence

### Changed

- Score version advanced to 5.0 and audit results now retain specialist results, failures, business context, and competitive evidence
- Markdown reports distinguish specialist interpretations, recommendations, and unavailable adapters
- CLI accepts business audience, offer, primary conversion, competitor, and comparison-dimension inputs

## [0.4.1] - 2026-09-18

### Added

- Optional Playwright extra import smoke check in the package CI job
- CodeQL scanning on phase/release pull requests, protected branches, and a weekly schedule
- Weekly Dependabot checks for Python and GitHub Actions dependencies
- Tag-triggered source/wheel builds with SHA-256 checksums and retained workflow artifacts

## [0.4.0] - 2026-09-18

### Added

- Recursive diagnostic redaction for common tokens, sensitive keys, URL userinfo, and secret query parameters
- Prompt-boundary sanitization with delimiter neutralization, control-character removal, and size limits
- Release validator for version synchronization, schemas, skill frontmatter, and agent trust boundaries
- CI package job that builds source and wheel distributions and smoke-tests the installed wheel

### Changed

- URL validation now limits input length and redirect count and revalidates the final response URL
- Security documentation now records collection, prompt, data, and release controls
- Package and Claude plugin versions advanced to 0.4.0

## [0.3.0] - 2026-09-18

### Added

- Deterministic checks for description length, visible-content depth, form friction, generic actions, incomplete social metadata, malformed JSON-LD, internal-link absence, robots restrictions, sitemap absence, blocked sitemap audits, and truncated sitemap collection
- Versioned specialist-agent input and result schemas
- Injection-resistant technical-agent briefs containing references, limitations, and prohibited actions without raw page text
- Evidence-availability and scoring-methodology sections in Markdown reports

### Changed

- Scoring version advanced to `3.0` with explicit finding-ID penalties and category-specific evidence coverage
- Markdown findings are prioritized by severity and stable finding ID
- Audit results now record score version and structured agent briefs
- Technical Audit phase documentation and release gates were added

## [0.2.0] - 2026-09-18

### Added

- Public-address enforcement for initial targets and redirect destinations
- Redirect-chain, content-length, and encoding provenance on fetch observations
- Structured robots.txt groups, crawl delays, sitemap declarations, content digests, and access evaluation
- Bounded recursive sitemap-index traversal with deduplication, gzip limits, scope checks, and truncation signals
- Visibility-aware HTML extraction, link classification, link text, language, required fields, and visible word count
- Fixtures and regression tests for private addresses, hostile credentials, hidden content, robots groups, nested/gzipped sitemaps, malformed XML, app shells, noindex pages, and multiple H1s
- Dated phase ledger in `docs/BUILD_HISTORY.md`

### Changed

- Evidence schema now describes page, robots, sitemap, redirects, response encoding, and response size more precisely
- Category schema now rejects unknown score categories
- Audit crawler user agent advanced to version 0.2

## [0.1.0] - 2026-09-18

### Added

- Claude Code plugin manifest, health skill, and audit skill
- Canonical evidence, finding, score, and audit schemas
- Safe static HTTP collection, HTML extraction, robots.txt, and sitemap inspection
- Deterministic technical analyzers and reproducible partial scoring
- JSON and Markdown reporting
- Six evidence-bounded specialist agent definitions
- Unit, integration, schema, and report tests with cross-platform CI
