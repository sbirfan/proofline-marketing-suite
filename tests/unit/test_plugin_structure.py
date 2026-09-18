import json
from pathlib import Path

ROOT = Path(__file__).parents[2]


def test_manifest_and_skill_frontmatter_exist() -> None:
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert manifest["name"] == "svgai-marketing"
    for skill in (ROOT / "skills").glob("*/SKILL.md"):
        assert skill.read_text(encoding="utf-8").startswith("---\n")


def test_agents_have_valid_frontmatter_boundaries() -> None:
    for agent in (ROOT / "agents").glob("*.md"):
        content = agent.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert content.count("---") >= 2
        assert "description:" in content.split("---", 2)[1]
