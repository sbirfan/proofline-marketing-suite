# Proofline Marketing Suite 1.0

Version 1.0 is the first stable release of the evidence-first audit and marketing workflow suite. It combines
bounded public-page collection, explicit observation states, deterministic findings and scoring, structured
specialist hand-offs, client reports, analysis skills, and approval-gated campaign drafting.

Stable contracts include the documented CLI, 14 namespaced plugin skills, JSON schemas with embedded versions,
the 0–100 score scale with separate confidence and coverage, and the distinction between observed, not found,
blocked, failed, render-required, not-tested, and unknown states. The current score version is 5.0.

The release supports CPython 3.11–3.13 on Linux, macOS, and Windows. CI builds source and wheel distributions,
installs the wheel in a clean environment, checks optional imports, runs CodeQL, and retains checksummed tag
artifacts. See the support and migration guides before integrating stored results.

Known limits remain explicit: audits target one primary page, rendered fallback is opt-in, specialist language
model execution is caller-provided, provider publishing is not included, and all client-facing claims require
human verification.
