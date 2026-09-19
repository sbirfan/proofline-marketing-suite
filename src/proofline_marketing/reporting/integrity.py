"""Final report gates that protect evidence and context boundaries."""

from __future__ import annotations

from ..models import AuditResult


class ReportIntegrityError(ValueError):
    """Raised when a client-ready report would overstate canonical evidence."""


def validate_report_integrity(result: AuditResult) -> None:
    """Reject unresolved context and unsupported claim scopes before rendering."""
    if result.context_assessment.get("resolution_required"):
        raise ReportIntegrityError(
            "context conflict must be resolved before rendering a client-ready report"
        )
    sitewide_supported = result.evidence_scope.get("sitewide_claims_supported", False)
    for finding in result.findings:
        if not finding.evidence:
            raise ReportIntegrityError(f"finding {finding.id} has no evidence reference")
        if finding.claim_scope == "site" and not sitewide_supported:
            raise ReportIntegrityError(f"finding {finding.id} makes an unsupported site-wide claim")
