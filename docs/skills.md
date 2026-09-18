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

## Campaign skills

| Skill | Use it for | Required context |
|---|---|---|
| `/copy` | Marketing copy variants | Channel, audience, offer, objective, claims |
| `/emails` | Lifecycle or campaign sequences | Permission basis, sender, cadence, offer |
| `/social` | Platform-specific organic posts | Platform, voice, objective, approved claims |
| `/ads` | Paid concepts and test matrices | Channel, budget context, exclusions, measurement |
| `/launch` | Phased launch plans | Timing, owners, channels, dependencies, risks |
| `/proposal` | Services proposals | Client context, scope, pricing inputs, approvals |

Campaign skills emit `schemas/campaign-output.schema.json`. Outputs remain drafts and expose claims, assumptions,
required approvals, and measurement separately. No skill is authorized to publish, send, launch, sign, purchase,
invoice, or mutate an external account merely because it drafted an artifact.
