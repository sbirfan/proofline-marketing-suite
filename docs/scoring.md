# Scoring

Scoring version 5.0 uses six dimensions:

| Dimension | Weight |
|---|---:|
| Content and messaging | 25% |
| Conversion | 20% |
| SEO and discoverability | 20% |
| Competitive positioning | 15% |
| Brand and trust | 10% |
| Growth strategy | 10% |

The alpha release deterministically tests content, conversion, SEO, and brand primitives. Competitive and
growth remain `not_tested`. Its partial overall is normalized across tested weights and labeled partial; it is
not comparable to a future full-coverage score without considering coverage.

Every scored deterministic finding has an explicit finding-ID penalty in `scoring/engine.py`. Severity is a
communication priority and does not silently determine the numerical penalty. Findings without a registered
score rule have no numerical effect until the rule, documentation, and tests are added.

Category coverage is based on which evidence sources were successfully tested. Confidence combines collection
reliability with that coverage. Tracking-product count is not a quality metric. Future measurement scoring will
evaluate event coverage, consent, duplicates, data-layer quality, first-party measurement, and attribution readiness.

Validated specialist outputs contain dimension ratings, not scores. The engine maps `strong` to 90, `adequate`
to 70, and `weak` to 40; `unknown` remains unscored. For categories with deterministic evidence, the category
score is 60% deterministic and 40% specialist assessment. Competitive and growth remain null until a specialist
supplies at least one evidence-linked non-unknown rating. An overall status becomes complete only when all six
categories are scored.
