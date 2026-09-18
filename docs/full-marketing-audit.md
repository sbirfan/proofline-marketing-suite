# Full marketing audit orchestration

Version 0.5.0 collects the target once, produces six structured specialist briefs, optionally collects
explicitly confirmed competitors with the same bounded policy, and accepts caller-supplied specialist adapters.
Adapters run concurrently and cannot mutate deterministic evidence, findings, or base scores. Invalid or failed
adapters are recorded independently in `agent_failures`.

## Business context

Audience, offer, primary conversion, competitor targets, and comparison dimensions are user inputs; page copy
never substitutes for research or confirmation. Revenue estimates remain prohibited unless traffic, conversion
rate, average value, and close rate are all supplied as numeric values with sources. Missing inputs produce a
directional-only limitation in the growth brief.

## Specialist outputs and scoring

Specialists return facts, interpretations, hypotheses, recommendations, measurement plans, and dimension
assessments linked to evidence URLs. They do not calculate canonical scores. Score engine version 5.0 maps the
fixed `strong`, `adequate`, and `weak` ratings to 90, 70, and 40, then combines them with deterministic category
evidence. `unknown` remains unscored. A result is complete only when every category has scored evidence.

## Resume and cache behavior

The package does not silently persist client evidence. Callers that operate an approved cache can pass
`precollected_evidence` and `precollected_competitors` to resume without refetching. Cached documents must retain
their original retrieval timestamps and collection states. Agent failures may be retried by passing only the
failed adapters against the same briefs; deterministic outputs remain unchanged.
