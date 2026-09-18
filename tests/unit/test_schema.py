import json
from pathlib import Path

import pytest

jsonschema = pytest.importorskip("jsonschema")

SCHEMAS = Path(__file__).parents[2] / "schemas"


def test_all_schema_documents_are_valid() -> None:
    for path in SCHEMAS.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
