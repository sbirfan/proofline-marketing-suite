# Architecture

The canonical flow is:

1. Normalize a public HTTP(S) target.
2. Collect bounded static evidence with normal TLS verification.
3. Preserve collection status and failure reason.
4. Parse page, robots, and sitemap evidence into typed structures.
5. Produce objective findings with deterministic analyzers.
6. Calculate versioned scores independently of model prose.
7. Let constrained specialist agents interpret supplied evidence.
8. Render one canonical `AuditResult` to JSON, Markdown, HTML, or PDF.

The Evidence Engine validates that initial and redirected destinations resolve to public addresses. It records
redirects and response metadata, parses robots rules without exposing raw instructions to agents, and follows
sitemap indexes only within bounded same-origin, depth, count, URL, and decompression limits.

Agents do not independently browse. Report renderers do not recompute audit facts. Browser rendering is an
optional collection adapter and must preserve the same evidence contract.
