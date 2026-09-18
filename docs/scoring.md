# Scoring

Scoring version 2.0 uses six dimensions:

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

Severity deductions are versioned in `scoring/engine.py`. Tracking-product count is not a quality metric.
Future measurement scoring will evaluate event coverage, consent, duplicates, data-layer quality, first-party
measurement, and attribution readiness.

