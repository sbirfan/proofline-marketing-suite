# Development

Python 3.11 or newer is required. The runtime intentionally uses the standard library; lint, typing, schema
validation, test, and coverage tools are development dependencies.

Add controlled sites under `tests/fixtures/sites/` for parser behavior. Network-dependent tests do not belong
in the unit suite. Report behavior should be covered by stable assertions or snapshots derived from a canonical
`AuditResult`.

Optional browser work uses Playwright through the `browser` extra. Browser and static collection must emit the
same evidence shapes and must not suppress certificate, redirect, timeout, or access failures.

