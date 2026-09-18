from pathlib import Path

from svgai_marketing.crawler.html import parse_html

FIXTURES = Path(__file__).parents[1] / "fixtures" / "sites"


def test_extracts_marketing_evidence_and_excludes_script_and_style_text() -> None:
    html = (FIXTURES / "static-good" / "index.html").read_text(encoding="utf-8")
    page = parse_html(html, "https://example.test/")

    assert page.title == "Evidence-first marketing audits for growing teams"
    assert page.headings["h1"] == ["Know what the evidence supports"]
    assert page.forms[0]["fields"] == 1
    assert page.buttons == ["Request an audit"]
    assert page.json_ld[0]["@type"] == "Organization"
    assert "secretFrameworkPayload" not in page.visible_text
    assert "display: none" not in page.visible_text


def test_marks_static_app_shell_as_render_required() -> None:
    html = '<html><body><div id="root"></div><script id="__NEXT_DATA__">{}</script></body></html>'
    page = parse_html(html, "https://example.test/app")
    assert page.render_required_reasons == ["low_static_text_with_app_shell"]
