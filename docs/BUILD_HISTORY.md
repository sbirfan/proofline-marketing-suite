# Build history

This ledger records what was built in each delivery phase, when it was completed, and what remains outside
that phase. Dates use UTC and refer to repository implementation work, not promises about future delivery.

## Phase summary

| Phase | Version | Status | Started | Completed | Repository record |
|---|---|---|---|---|---|
| Foundation | 0.1.0 | Complete | 2026-09-18 | 2026-09-18 | PR #1, commit `652f82b6` |
| Evidence Engine | 0.2.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/evidence-engine` |
| Technical Audit | 0.3.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/technical-audit` |
| Security and packaging | 0.4.1 | Complete | 2026-09-18 | 2026-09-18 | `feature/security-packaging` |
| Full Marketing Audit | 0.5.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/full-marketing-audit` |
| Client reporting | 0.6.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/client-reporting` |
| Analysis capabilities | 0.7.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/analysis-capabilities` |
| Campaign capabilities | 0.8.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/campaign-capabilities` |
| Public beta | 0.9.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/public-beta` |
| Stable release | 1.0.0 | Complete | 2026-09-18 | 2026-09-18 | `feature/stable-release` |
| Proofline compatibility rename | 1.1.0 | Complete | 2026-09-19 | 2026-09-19 | `feature/proofline-rename` |
| Proofline namespace migration | 2.0.0 | Complete | 2026-09-19 | 2026-09-19 | `feature/proofline-v2` |
| Context guide hotfix | 2.0.1 | Complete | 2026-09-19 | 2026-09-19 | `fix/context-guide-2.0.1` |

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

## Phase 0.4.0–0.4.1 — Security and Packaging

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
- Optional Playwright-extra import smoke testing, CodeQL analysis, weekly dependency updates, and tag-triggered
  release builds that retain source/wheel distributions with SHA-256 checksums
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

## Phase 0.5.0 — Full Marketing Audit

Completed on 2026-09-18.

Built:

- Explicit, user-confirmed business context for audience, offer, primary conversion, competitors, comparison
  dimensions, and sourced growth metrics
- Six structured specialist briefs from one canonical target collection, with no raw webpage text in prompts
- Comparable competitor evidence collected only from confirmed targets under the same bounded collector policy
- Concurrent caller-supplied specialist execution with runtime result validation and per-agent failure isolation
- Evidence-linked dimension assessments, interpretations, recommendations, test designs, and measurement needs
- Score engine 5.0, which deterministically maps bounded specialist ratings and never lets agents calculate scores
- Caller-managed resume inputs for approved caches without implicit client-data persistence
- End-to-end partial and complete audit coverage plus hostile, sparse, missing-context, and adapter-failure cases

Quality record at phase completion:

- Ruff formatting and lint: required locally and in CI
- Strict mypy: required locally and in CI
- Pytest, coverage, JSON Schema, release validation, package build, wheel install, and browser-extra smoke: required
- GitHub CI and CodeQL: required before both `develop` and `main` merges

Still deferred to later phases:

- Bundled external model credentials or provider-specific invocation
- Crawl scheduling across every sitemap URL
- Client-ready HTML and PDF report rendering

## Phase 0.6.0 — Client Reporting

Completed on 2026-09-18.

Built:

- A self-contained semantic HTML renderer with escaped values, responsive layout, print styles, scoped table
  headers, and configurable client branding
- A deterministic ReportLab PDF renderer with page numbers, repeated page chrome, wrapping category tables,
  long evidence URLs, sparse states, and stable metadata
- HTML and PDF CLI formats, with explicit output paths required for binary PDF output
- A `reports` optional dependency and clean installed-wheel import smoke check in CI
- Regression tests for hostile values, accessibility primitives, long URLs, deterministic bytes, PDF page count,
  text extraction, and page numbering
- A multi-page synthetic report rendered through Poppler and visually inspected before release

Quality record at phase completion:

- Ruff, strict mypy, pytest, coverage, schema validation, and package validation: required locally and in CI
- Source/wheel build, installed CLI, browser extra, and reports extra smoke checks: required in CI
- GitHub CI and CodeQL: required on feature and release PRs
- Latest PDF page images: required to show no clipping, overlap, broken tables, or unreadable content

Still deferred to later phases:

- Rich charts and benchmark visualizations
- Hosted report delivery and authenticated client portals

## Phase 0.7.0 — Analysis Capabilities

Completed on 2026-09-18.

Built:

- Focused `/seo`, `/landing`, `/competitors`, `/brand`, `/funnel`, and `/report` Claude Code skills
- Explicit invocation boundaries and required context for search, conversion, comparison, trust, journey, and
  reporting requests
- Shared structured output contract that separates facts, interpretations, recommendations, limitations, and
  timestamped sources
- Central untrusted-evidence requirements, missing-context behavior, canonical-score protection, and
  unsupported-lift/revenue restrictions across every new skill
- Skill catalog, folder/frontmatter validation, evidence-boundary checks, and JSON Schema validation

Quality record at phase completion:

- All standard local gates, package builds, installed extras, GitHub CI, and CodeQL are required
- Every new skill is validated with the skill-creator quick validator

Still deferred to later phases:

- Campaign asset generation for copy, email, social, ads, launches, and proposals
- Hosted delivery, provider-specific publishing, and external account mutations

## Phase 0.8.0 — Campaign Capabilities

Completed on 2026-09-18.

Built:

- Review-ready `/copy`, `/emails`, `/social`, `/ads`, `/launch`, and `/proposal` Claude Code skills
- Required audience, offer, objective, channel, budget, timing, ownership, commercial, and permission context
  appropriate to each campaign mode
- Shared structured campaign contract for artifacts, approved or placeholder claims, assumptions, approvals, and
  measurement guardrails
- Explicit prohibitions on invented proof, consent, scarcity, pricing, performance, legal approval, and authority
- External-action boundaries that require separate approval before publishing, sending, launching, scheduling,
  signing, purchasing, invoicing, or modifying connected accounts
- Skill catalog, folder/frontmatter checks, security-boundary tests, and official skill validation

Quality record at phase completion:

- All standard local gates, package builds, installed extras, GitHub CI, and CodeQL are required
- Every campaign skill is validated with the skill-creator quick validator

Still deferred to later phases:

- Provider-specific publishing adapters
- Live account mutation, budget changes, list uploads, and CRM updates

## Phase 0.9.0 — Public Beta

Completed on 2026-09-18.

Built:

- Secret-free `doctor` diagnostics with human-readable and JSON output for version, Python support, platform,
  and installed optional capabilities
- Installed-wheel CI coverage for the diagnostic command
- Synthetic observed and blocked evidence examples using reserved `.test` URLs
- Machine-checkable skill-routing evaluation cases covering expected invocation and refusal of unapproved
  sending, launching, and live-account mutation
- Release checks for unique evaluation IDs, valid skill references, example structure, and synthetic-data scope
- Public-beta compatibility, optional-extra, reproduction, and support-request guidance

Quality record at phase completion:

- All standard local gates, distribution builds, clean-wheel smoke checks, GitHub CI, and CodeQL are required
- Diagnostic output is deliberately bounded to non-secret runtime capability data

Still deferred to the stable release:

- Long-term compatibility and deprecation policy
- Stable support policy, migration guide, and 1.0 release notes

## Phase 1.0.0 — Stable Release

Completed on 2026-09-18.

Built:

- Stable compatibility promise for the documented CLI, plugin skill names, and versioned output contracts
- CPython 3.11–3.13 support policy across Linux, macOS, and Windows
- Patch/minor/major change policy with a documented deprecation window and security exception
- Schema and score-version consumer rules, including rejection of unknown major schemas
- Public-beta-to-stable migration guide and comprehensive 1.0 release notes
- Direct CLI regression tests and stable-release document checks in the release validator
- Production/Stable package metadata and synchronized 1.0.0 package/plugin versions

Quality record at phase completion:

- All local formatting, lint, typing, test, coverage, schema, evaluation, build, and clean-wheel gates are required
- Phase and release PRs both require successful cross-platform CI and CodeQL before merge

Known limits retained deliberately:

- Single-primary-page audit scheduling, opt-in rendering, and caller-provided specialist execution
- No provider-specific publishing, authenticated crawling, or automatic external-account mutation
- No guarantee of rankings, regulatory compliance, accessibility compliance, or revenue impact

## Phase 1.1.0 — Proofline Compatibility Rename

Completed on 2026-09-19.

Built:

- Proofline Marketing Suite product, repository, diagnostic, report, and HTTP user-agent branding
- `proofline` as the primary CLI with `svgai-marketing` retained as a compatible 1.x alias
- `proofline-marketing-suite` distribution metadata and updated installation guidance
- A migration matrix for repository, distribution, CLI, Python, Claude plugin, and schema identifiers
- Explicit preservation of the `svgai_marketing` Python namespace, `/svgai-marketing:*` plugin namespace, and
  existing schema IDs until a major release can change them safely
- Updated README, beginner guide, changelog, support material, tests, CI smoke checks, and release validation

Quality record at phase completion:

- Both primary and compatibility CLI commands must pass installed-wheel smoke tests
- All standard local gates, GitHub CI, and CodeQL are required before both merges

Deferred to 2.0:

- `proofline_marketing` Python namespace
- `/proofline:*` Claude plugin namespace
- Removal of deprecated SVG AI technical aliases

## Phase 2.0.0 — Proofline Namespace Migration

Completed on 2026-09-19.

Built:

- `/proofline:*` Claude plugin namespace across all 14 health, audit, analysis, reporting, and campaign skills
- `proofline_marketing` Python namespace across runtime modules, examples, tests, typing, coverage, and skill calls
- `proofline` as the sole installed CLI and `proofline` as the plugin manifest name
- `proofline.example` schema identifiers with updated cross-schema references
- Proofline-named release artifacts, clean-wheel checks, and complete 1.x-to-2.0 migration guidance
- README, beginner guide, changelog, and dated build history synchronized with the final namespace

Quality record at phase completion:

- All formatting, lint, strict typing, tests, coverage, schema, build, and clean-wheel gates are required
- Phase and release PRs both require successful cross-platform CI and CodeQL before merge

Breaking changes:

- Removed the `svgai-marketing` command, `svgai_marketing` imports, `/svgai-marketing:*` commands, and legacy
  schema base identifiers after the 1.1 compatibility release

## Phase 2.0.1 — Context Guide Hotfix

Completed on 2026-09-19.

Built:

- Placeholder-based beginner prompt that cannot be mistaken for universal business context
- Separate ecommerce, SaaS, and local-service examples
- Audit-skill parsing that keeps the target URL distinct from optional user context
- Explicit context-versus-evidence comparison and a stop-and-confirm rule for material conflicts
- Page-scoped absence language and prohibition on scoring a brief conflict as a website defect
- Synthetic ecommerce conflict, aligned checkout, and missing-context evaluation cases

Quality record at phase completion:

- All local gates, clean-wheel checks, GitHub CI, and CodeQL are required
- The ShearStore regression must ask for resolution rather than recommend a consultation funnel

## Maintenance rule

Every phase pull request must update this file, the README capability/limitation sections, the changelog, and
the package/plugin version when applicable. A phase is marked complete only after local quality gates and the
configured GitHub CI pass. The feature PR is then merged to `develop`, post-merge CI is verified, and the
release PR is merged to `main` before work begins on the next phase.

## Post-1.0 documentation updates

### 2026-09-19 — Beginner guide

- Added a no-code-oriented setup path for Windows, macOS, and Linux
- Added ready-to-copy first-audit, PDF, focused-analysis, email, and proposal examples
- Documented installation checks, optional browser rendering, common errors, safe updating, evidence-state
  interpretation, permissions, and external-action approval boundaries
- Linked the guide prominently from the README
