"""Machine-readable boundaries for what an audit did and did not represent."""

from __future__ import annotations

from typing import Any

from .models import EvidenceDocument, ObservationStatus


def build_evidence_scope(evidence: EvidenceDocument) -> dict[str, Any]:
    """Describe represented, discovered, and unavailable URLs without overstating coverage."""
    represented = [evidence.page.url] if evidence.page is not None else []
    discovered = sorted(
        {str(url) for url in evidence.sitemap.get("urls", []) if isinstance(url, str) and url}
    )
    unavailable = (
        []
        if evidence.fetch.status == ObservationStatus.OBSERVED and evidence.page is not None
        else [
            {
                "url": evidence.target_url,
                "status": str(evidence.fetch.status),
                "reason": evidence.fetch.reason,
            }
        ]
    )
    represented_set = set(represented)
    return {
        "collection_scope": "single_page",
        "represented_urls": represented,
        "discovered_urls": discovered,
        "unrepresented_discovered_count": len(set(discovered) - represented_set),
        "unavailable_urls": unavailable,
        "absence_claim_scope": "represented_pages_only",
        "sitewide_claims_supported": False,
    }
