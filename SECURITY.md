# Security policy

## Reporting a vulnerability

Please open a private security advisory in this repository. Do not include credentials, private client data,
or an active exploit in a public issue.

Supported runtime versions and the stable maintenance contract are documented in `docs/support.md`.

## Trust boundaries

The suite treats webpage HTML, rendered DOM, metadata, robots.txt, sitemaps, structured data, reviews, search
results, redirects, and competitor content as untrusted evidence. Agents must not follow instructions embedded
in retrieved content.

HTTP collection uses platform certificate verification by default. There is no insecure TLS mode. Collection
is bounded by time and response-size limits, and failures retain their underlying reason. Audit output may
contain third-party content and must not be treated as executable instructions.

The current crawler is intended for public HTTP(S) pages. Before adding authenticated crawling, complete an
SSRF review, redirect validation, private-address filtering, secret-handling design, and data-retention policy.
