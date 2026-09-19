import json

from svgai_marketing import __version__, cli


def test_doctor_json_command(capsys) -> None:
    assert cli.main(["doctor", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["version"] == __version__
    assert payload["healthy"] is True


def test_parser_exposes_stable_commands() -> None:
    parser = cli.build_parser()
    assert parser.parse_args(["doctor"]).command == "doctor"
    audit = parser.parse_args(["audit", "https://example.test/"])
    assert audit.command == "audit"
    assert audit.format == "markdown"


def test_primary_program_name_is_proofline() -> None:
    assert cli.build_parser().prog == "proofline"
