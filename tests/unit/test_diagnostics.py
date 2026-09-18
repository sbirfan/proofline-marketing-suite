import json

from svgai_marketing import __version__, diagnostics


def test_diagnostics_are_secret_free_and_machine_readable() -> None:
    report = diagnostics.collect_diagnostics()
    payload = json.loads(diagnostics.render_diagnostics(report, as_json=True))

    assert payload["version"] == __version__
    assert payload["healthy"] is True
    assert set(payload) == {
        "version",
        "python",
        "platform",
        "supported_python",
        "browser_extra",
        "reports_extra",
        "healthy",
    }


def test_human_diagnostics_explain_optional_extras() -> None:
    body = diagnostics.render_diagnostics(diagnostics.collect_diagnostics())
    assert "Optional extras:" in body
    assert "browser=" in body
    assert "reports=" in body
