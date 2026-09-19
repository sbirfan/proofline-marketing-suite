import json
from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_manifest_and_skill_frontmatter_exist() -> None:
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "proofline"
    for skill in (ROOT / "skills").glob("*/SKILL.md"):
        assert skill.read_text(encoding="utf-8").startswith("---\n")


def test_skill_names_match_folders_and_analysis_boundaries() -> None:
    analysis = {"seo", "landing", "competitors", "brand", "funnel", "report"}
    campaign = {"copy", "emails", "social", "ads", "launch", "proposal"}
    expected = analysis | campaign
    found: set[str] = set()
    for skill in (ROOT / "skills").glob("*/SKILL.md"):
        content = skill.read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1]
        name_line = next(line for line in frontmatter.splitlines() if line.startswith("name:"))
        name = name_line.split(":", 1)[1].strip()
        assert name == skill.parent.name
        if name in expected:
            found.add(name)
            assert "untrusted evidence" in content.casefold()
            assert "evidence" in content.casefold()
            if name in campaign:
                assert (
                    "explicit approval" in content.casefold()
                    or "without approval" in content.casefold()
                )
    assert found == expected


def test_agents_have_valid_frontmatter_boundaries() -> None:
    for agent in (ROOT / "agents").glob("*.md"):
        content = agent.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert content.count("---") >= 2
        assert "description:" in content.split("---", 2)[1]


def test_audit_skill_requires_context_conflict_resolution() -> None:
    content = (ROOT / "skills/audit/SKILL.md").read_text(encoding="utf-8").casefold()
    assert "do not copy" in content
    assert "materially conflict" in content
    assert "ask whether to audit the current site" in content
    assert "and stop" in content
