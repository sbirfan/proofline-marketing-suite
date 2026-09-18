# Security model

## Trust boundaries

The primary threat is hostile third-party content crossing into model instructions. Retrieved data stays in an
explicit evidence boundary and may not change the audit task, invoke tools, request secrets, or override system
and plugin instructions. Boundary-closing tags and control characters are neutralized before prompt use, and
prompt-bound evidence is capped at 20,000 characters.

## Collection controls

- Only HTTP(S) URLs without embedded credentials are accepted.
- The initial URL, every redirect, and the final response URL must resolve exclusively to public addresses.
- URL length, redirect count, time, response bytes, sitemap depth, decompression, and resource counts are bounded.
- TLS certificate verification is mandatory; there is no insecure mode.
- Authenticated crawling is not implemented.

## Data and output controls

- Common access-token shapes, authorization headers, secret-bearing mapping keys, URL userinfo, and sensitive
  query parameters can be redacted before diagnostic persistence.
- Raw webpage text is excluded from specialist-agent briefs; references use stable evidence identifiers and URLs.
- Local audit outputs, environment files, build artifacts, and caches are excluded from source control.
- Agent definitions are tool-free and repeat the untrusted-content boundary.

## Release controls

CI runs formatting, lint, strict typing, tests, and coverage across Linux, macOS, Windows, Python 3.11, and
Python 3.13. A separate packaging job validates synchronized versions and prompt boundaries, builds both source
and wheel distributions, installs the wheel in a clean virtual environment, and runs the installed CLI.

See the repository `SECURITY.md` for vulnerability reporting.
