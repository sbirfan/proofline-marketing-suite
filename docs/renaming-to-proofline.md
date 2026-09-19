# Renaming to Proofline

Version 1.1 renames SVG AI Marketing Suite to **Proofline Marketing Suite**. The new name describes the
project's evidence-first purpose and avoids confusion with SVG image tools.

## What changes in 1.1

| Area | New primary name | 1.x compatibility behavior |
|---|---|---|
| Product | Proofline Marketing Suite | Old prose name is retired |
| Repository | `sbirfan/proofline-marketing-suite` | GitHub redirects the previous repository URL |
| Distribution | `proofline-marketing-suite` | Install the new distribution name |
| Command line | `proofline` | `svgai-marketing` remains available |
| Python imports | Planned `proofline_marketing` for 2.0 | `svgai_marketing` remains canonical in 1.x |
| Claude plugin | Planned `/proofline:*` for 2.0 | `/svgai-marketing:*` remains available in 1.x |

The Python and Claude namespaces remain unchanged because changing them would break documented 1.0
integrations. The compatibility period provides time for scripts, examples, and saved workflows to move to the
new CLI and repository without losing functionality.

## Upgrade

Update an existing clone:

```bash
git remote set-url origin https://github.com/sbirfan/proofline-marketing-suite.git
git pull
python -m pip install -e ".[reports]"
proofline doctor
```

New clones should use:

```bash
git clone https://github.com/sbirfan/proofline-marketing-suite.git
cd proofline-marketing-suite
python -m venv .venv
python -m pip install -e ".[reports]"
proofline doctor
```

Commands can be migrated mechanically:

```text
svgai-marketing doctor  → proofline doctor
svgai-marketing audit   → proofline audit
```

Do not change `import svgai_marketing` or `/svgai-marketing:*` commands during the 1.x series. Their replacements
will be introduced with a major-version migration rather than silently breaking existing users.

No schema identifiers, observation states, or score algorithms change in 1.1. Schema IDs retain their existing
`svgai.example` identifiers to preserve reference resolution for stored 1.x documents.
