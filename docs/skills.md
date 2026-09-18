# Skill catalog

The Claude Code plugin exposes small, task-specific entry points. Each analysis skill reuses canonical evidence,
preserves collection uncertainty, cites sources, treats retrieved material as untrusted, and cannot change scores.

| Skill | Use it for | Required context |
|---|---|---|
| `/seo` | Indexability, metadata, structure, links, schema | Canonical audit evidence |
| `/landing` | Message hierarchy, actions, forms, proof, friction | Audience, offer, primary conversion |
| `/competitors` | Comparable positioning and evidence gaps | Confirmed competitor URLs and dimensions |
| `/brand` | Clarity, consistency, proof, trust | Audited material and optional research |
| `/funnel` | Stage, journey, handoff, measurement gaps | User-defined stages and conversions |
| `/report` | JSON, Markdown, HTML, or PDF delivery | Existing canonical `AuditResult` |

Skills return facts, interpretations, recommendations, limitations, and sources as distinct values. The shared
analysis contract is `schemas/skill-output.schema.json`. Rendering is the one exception: `/report` returns the
selected report format without changing the canonical audit object.
