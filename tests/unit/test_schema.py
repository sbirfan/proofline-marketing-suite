import json
from pathlib import Path

import pytest

from proofline_marketing.models import (
    AuditResult,
    CategoryScore,
    EvidenceDocument,
    FetchObservation,
    ObservationStatus,
)

jsonschema = pytest.importorskip("jsonschema")
referencing = pytest.importorskip("referencing")

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


def test_full_audit_payload_matches_local_contracts() -> None:
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/",
        fetch=FetchObservation(url="https://example.test/", status=ObservationStatus.OBSERVED),
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
    result = AuditResult(
        schema_version="2.0",
        score_version="5.0",
        target_url=evidence.target_url,
        generated_at="2026-09-18T00:00:00+00:00",
        evidence=evidence,
        findings=[],
        categories={
            name: CategoryScore(None, 0, 0, "not_tested")
            for name in ("content", "conversion", "seo", "competitive", "brand", "growth")
        },
        overall=None,
        confidence=0,
        coverage=0,
        status="insufficient_evidence",
    )
    schema = json.loads((SCHEMAS / "audit.schema.json").read_text(encoding="utf-8"))
    documents = [
        json.loads(path.read_text(encoding="utf-8")) for path in SCHEMAS.glob("*.schema.json")
    ]
    registry = referencing.Registry().with_resources(
        (document["$id"], referencing.Resource.from_contents(document)) for document in documents
    )

    jsonschema.Draft202012Validator(schema, registry=registry).validate(result.to_dict())
