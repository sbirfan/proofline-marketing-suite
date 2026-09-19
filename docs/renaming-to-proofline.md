# Migrating to Proofline 2.0

Proofline 2.0 completes the rename from SVG AI Marketing Suite. Version 1.1 introduced the new product,
repository, distribution, and CLI while retaining compatibility aliases. Version 2.0 moves the remaining
technical namespaces to Proofline and removes those aliases.

## Namespace changes

| Area | Version 1.x | Version 2.0 |
|---|---|---|
| Repository | `sbirfan/proofline-marketing-suite` | unchanged |
| Distribution | `proofline-marketing-suite` | unchanged |
| Command line | `proofline` and legacy `svgai-marketing` | `proofline` only |
| Python imports | `svgai_marketing` | `proofline_marketing` |
| Claude plugin | `/svgai-marketing:*` | `/proofline:*` |
| Schema base ID | `https://svgai.example/schemas/` | `https://proofline.example/schemas/` |

Audit observation states and score algorithm 5.0 are unchanged. The schema ID change is breaking for registries
that key documents by `$id`; update those registrations before accepting 2.0 payloads.

## Upgrade an existing clone

```bash
git remote set-url origin https://github.com/sbirfan/proofline-marketing-suite.git
git pull
python -m pip install -e ".[reports]"
proofline doctor
```

Restart Claude Code from the repository folder:

```bash
claude --plugin-dir .
```

Then verify:

```text
/proofline:health
```

## Update scripts and integrations

Make these replacements:

```text
svgai-marketing       → proofline
svgai_marketing       → proofline_marketing
/svgai-marketing:     → /proofline:
https://svgai.example → https://proofline.example
```

For example:

```python
from proofline_marketing.models import AuditResult
from proofline_marketing.reporting import render_pdf
```

There is no automatic import alias in 2.0. This prevents new integrations from silently depending on the
retired identity and makes missing migrations fail clearly during testing.
