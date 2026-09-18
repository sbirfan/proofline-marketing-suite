import json
from pathlib import Path

import pytest

from svgai_marketing.models import EvidenceDocument, FetchObservation, ObservationStatus

jsonschema = pytest.importorskip("jsonschema")

SCHEMAS = Path(__file__).parents[2] / "schemas"


def test_all_schema_documents_are_valid() -> None:
    for path in SCHEMAS.glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)


def test_minimal_unavailable_evidence_matches_contract() -> None:
    schema = json.loads((SCHEMAS / "evidence.schema.json").read_text(encoding="utf-8"))
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/",
        fetch=FetchObservation(
            url="https://example.test/",
            status=ObservationStatus.BLOCKED,
            reason="non_public_address",
        ),
        robots={
            "resource": "robots",
            "status": "not_tested",
            "search_engine_access": "unknown",
            "sitemaps": [],
            "groups": [],
            "body_sha256": None,
            "line_count": 0,
        },
        sitemap={
            "resource": "sitemap",
            "status": "not_tested",
            "reason": None,
            "search_engine_access": "unknown",
            "urls": [],
            "url_count": 0,
            "resources": [],
            "sitemap_count": 0,
            "truncated": False,
            "limits": {"max_depth": 3, "max_sitemaps": 20, "max_urls": 1000},
        },
    )

    jsonschema.Draft202012Validator(schema).validate(evidence.to_dict())
