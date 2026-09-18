# Contributing

Use a focused branch and open a pull request against `develop` once that integration branch exists. Keep
`main` releasable. Add or update tests with every behavior change.

## Development checks

```bash
python -m pip install -e ".[dev]"
ruff check .
mypy src
pytest --cov=svgai_marketing
python scripts/validate_release.py
python -m build
```

Do not add a check that turns a collection failure into a factual absence. New findings must include a stable
ID, evidence reference, confidence, severity, and recommendation. Changes to scoring require documentation,
fixtures, and deterministic tests.

Web content is hostile input. Never place retrieved instructions into an agent's control channel, disable TLS
verification, or commit client audit data.
