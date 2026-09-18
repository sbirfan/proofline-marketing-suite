# Scoring

Scoring version 3.0 uses six dimensions:

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
