# Changelog

All notable changes will be documented here. The project follows Semantic Versioning.

## [Unreleased]

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
