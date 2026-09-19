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
    assert project["project"]["name"] == "proofline-marketing-suite"
    scripts = project["project"]["scripts"]
    assert scripts["proofline"] == scripts["svgai-marketing"]
    assert manifest["repository"].endswith("/sbirfan/proofline-marketing-suite")
    if expected.startswith("1."):
        classifiers = project["project"]["classifiers"]
        assert "Development Status :: 5 - Production/Stable" in classifiers
        for relative in ("docs/support.md", "docs/migration.md", "docs/release-notes-1.0.md"):
            assert (ROOT / relative).is_file(), f"stable release document missing: {relative}"

    skills = list((ROOT / "skills").glob("*/SKILL.md"))
    agents = list((ROOT / "agents").glob("*.md"))
    for path in [*skills, *agents]:
        content = path.read_text(encoding="utf-8")
        assert content.startswith("---\n"), f"{path} has no YAML frontmatter"
    evidence_skills = [path for path in skills if path.parent.name != "health"]
    for path in [*evidence_skills, *agents]:
        content = path.read_text(encoding="utf-8")
        assert "untrusted" in content.casefold(), f"{path} has no untrusted-content boundary"

    for path in (ROOT / "schemas").glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        assert schema.get("$schema") == "https://json-schema.org/draft/2020-12/schema"
        assert schema.get("additionalProperties") is False

    evaluations = json.loads((ROOT / "evals/skill-routing.json").read_text(encoding="utf-8"))
    assert evaluations["schema_version"] == "1.0"
    case_ids = [case["id"] for case in evaluations["cases"]]
    assert len(case_ids) == len(set(case_ids)), "evaluation case IDs must be unique"
    skill_names = {path.parent.name for path in skills}
    for case in evaluations["cases"]:
        assert set(case) == {"id", "prompt", "expected_skill"}
        assert case["prompt"].strip()
        assert case["expected_skill"] is None or case["expected_skill"] in skill_names

    evidence_schema = json.loads(
        (ROOT / "schemas/evidence.schema.json").read_text(encoding="utf-8")
    )
    required = set(evidence_schema["required"])
    for path in (ROOT / "examples").glob("evidence-*.json"):
        example = json.loads(path.read_text(encoding="utf-8"))
        assert required <= set(example), f"{path} is missing required evidence fields"
        assert example["target_url"].endswith(".test/"), f"{path} must remain synthetic"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
