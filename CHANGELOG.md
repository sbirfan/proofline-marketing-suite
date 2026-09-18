# Changelog

All notable changes will be documented here. The project follows Semantic Versioning.

## [Unreleased]

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
