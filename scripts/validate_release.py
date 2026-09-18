#!/usr/bin/env python3
"""Validate release metadata and security boundaries without third-party packages."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).parents[1]


def main() -> int:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    expected = project["project"]["version"]
    manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    package = (ROOT / "src/svgai_marketing/__init__.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__ = "([^"]+)"$', package, re.MULTILINE)
    assert match, "package version is missing"
    assert manifest["version"] == expected == match.group(1), "release versions differ"

    skills = list((ROOT / "skills").glob("*/SKILL.md"))
    agents = list((ROOT / "agents").glob("*.md"))
    for path in [*skills, *agents]:
        content = path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"{path} has no YAML frontmatter"
    for path in [ROOT / "skills/audit/SKILL.md", *agents]:
        content = path.read_text(encoding="utf-8")
        assert "untrusted" in content.casefold(), f"{path} has no untrusted-content boundary"

    for path in (ROOT / "schemas").glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        assert schema.get("additionalProperties") is False
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
