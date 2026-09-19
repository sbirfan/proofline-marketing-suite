from proofline_marketing.evidence_scope import build_evidence_scope
from proofline_marketing.models import (
    EvidenceDocument,
    FetchObservation,
    ObservationStatus,
    PageEvidence,
)


def test_scope_separates_represented_from_discovered_urls() -> None:
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/",
        fetch=FetchObservation(url="https://example.test/", status=ObservationStatus.OBSERVED),
        page=PageEvidence(url="https://example.test/"),
        sitemap={
            "urls": [
                "https://example.test/",
                "https://example.test/products",
                "https://example.test/contact",
            ]
        },
    )

    scope = build_evidence_scope(evidence)

    assert scope["represented_urls"] == ["https://example.test/"]
    assert scope["unrepresented_discovered_count"] == 2
    assert scope["sitewide_claims_supported"] is False
    assert scope["absence_claim_scope"] == "represented_pages_only"


def test_unavailable_target_is_recorded_with_reason() -> None:
    evidence = EvidenceDocument(
        schema_version="2.0",
        target_url="https://example.test/",
        fetch=FetchObservation(
            url="https://example.test/",
            status=ObservationStatus.BLOCKED,
            reason="address_not_public",
        ),
    )

    scope = build_evidence_scope(evidence)

    assert scope["represented_urls"] == []
    assert scope["unavailable_urls"] == [
        {
            "url": "https://example.test/",
            "status": "blocked",
            "reason": "address_not_public",
        }
    ]
