# Evidence model

An observation state is one of `observed`, `not_found`, `blocked`, `fetch_failed`, `render_required`,
`not_tested`, or `unknown`. These states are not interchangeable.

Every material finding contains a stable ID, category, severity, factual claim, one or more evidence
references, confidence, and an optional recommendation. The `kind` field separates observed facts from model
interpretations, recommendations, and estimates.

The result records `score`, `confidence`, and `coverage` independently. A score can be unavailable when
evidence is insufficient. Low coverage never becomes an average-looking score through imputation.

