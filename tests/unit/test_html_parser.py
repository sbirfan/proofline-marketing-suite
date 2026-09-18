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


def test_excludes_hidden_content_and_classifies_links() -> None:
    html = """
    <html lang="en"><body>
      <h1>Visible heading</h1>
      <div hidden>hidden words</div>
      <div aria-hidden="true"><h2>hidden heading</h2></div>
      <p style="display: none">also hidden</p>
      <a href="/about">About us</a>
      <a href="https://outside.test/">External source</a>
      <form><input required><input type="submit" value="Join now"></form>
    </body></html>
    """
    page = parse_html(html, "https://example.test/")

    assert page.language == "en"
    assert "hidden" not in page.visible_text
    assert "h2" not in page.headings
    assert page.links[0]["kind"] == "internal"
    assert page.links[0]["text"] == "About us"
    assert page.links[1]["kind"] == "external"
    assert page.forms[0]["required_fields"] == 1
    assert "Join now" in page.buttons
    assert page.visible_word_count == len(page.visible_text.split())
