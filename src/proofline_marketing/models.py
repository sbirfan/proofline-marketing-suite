"""Canonical, serializable domain models for the audit pipeline."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class ObservationStatus(StrEnum):
    OBSERVED = "observed"
    NOT_FOUND = "not_found"
    BLOCKED = "blocked"
    FETCH_FAILED = "fetch_failed"
    RENDER_REQUIRED = "render_required"
    NOT_TESTED = "not_tested"
    UNKNOWN = "unknown"


class Severity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditMode(StrEnum):
    """How supplied context should be interpreted against current website evidence."""

    CURRENT_STATE = "current_state"
    PLANNED_FUNNEL = "planned_funnel"
    CONFIRMED_OVERRIDE = "confirmed_override"


class ContextStatus(StrEnum):
    ALIGNED = "aligned"
    CONFLICT = "conflict"
    UNKNOWN = "unknown"
    OVERRIDDEN = "overridden"


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def default_context_assessment() -> dict[str, Any]:
    """Return a schema-valid assessment for directly constructed audit results."""
    return {
        "audit_mode": AuditMode.CURRENT_STATE,
        "status": ContextStatus.UNKNOWN,
        "observed_business_model": "unknown",
        "observed_conversions": [],
        "supplied_conversion": None,
        "conflicts": [],
        "resolution_required": False,
    }


@dataclass(slots=True)
class FetchObservation:
    url: str
    status: ObservationStatus
    retrieved_at: str = field(default_factory=utc_now)
    http_status: int | None = None
    final_url: str | None = None
    content_type: str | None = None
    content_length: int | None = None
    encoding: str | None = None
    reason: str | None = None
    render_mode: str = "static"
    confidence: float = 1.0
    elapsed_ms: int | None = None
    redirect_chain: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.redirect_chain:
            self.redirect_chain.append(self.url)


@dataclass(slots=True)
class PageEvidence:
    url: str
    language: str | None = None
    title: str | None = None
    meta_description: str | None = None
    canonical: str | None = None
    robots_meta: list[str] = field(default_factory=list)
    headings: dict[str, list[str]] = field(default_factory=dict)
    links: list[dict[str, str]] = field(default_factory=list)
    images: list[dict[str, str | None]] = field(default_factory=list)
    forms: list[dict[str, Any]] = field(default_factory=list)
    buttons: list[str] = field(default_factory=list)
    json_ld: list[Any] = field(default_factory=list)
    open_graph: dict[str, str] = field(default_factory=dict)
    visible_text: str = ""
    visible_word_count: int = 0
    tracking_indicators: list[str] = field(default_factory=list)
    render_required_reasons: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceReference:
    url: str
    source_type: str
    selector: str | None = None
    observed_value: Any = None


@dataclass(slots=True)
class Finding:
    id: str
    category: str
    severity: Severity
    claim: str
    evidence: list[EvidenceReference]
    confidence: float
    recommendation: str | None = None
    kind: str = "observed_fact"


@dataclass(slots=True)
class CategoryScore:
    score: float | None
    confidence: float
    coverage: float
    status: str = "scored"


@dataclass(slots=True, frozen=True)
class SourcedMetric:
    """A numeric business input whose provenance is explicit."""

    value: float
    source: str


@dataclass(slots=True)
class BusinessContext:
    """User-confirmed context; blank fields must never be inferred from website copy."""

    audience: str | None = None
    offer: str | None = None
    primary_conversion: str | None = None
    competitor_urls: list[str] = field(default_factory=list)
    comparison_dimensions: list[str] = field(default_factory=list)
    competitors_confirmed: bool = False
    monthly_traffic: SourcedMetric | None = None
    conversion_rate: SourcedMetric | None = None
    average_value: SourcedMetric | None = None
    close_rate: SourcedMetric | None = None
    currency: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def revenue_inputs_complete(self) -> bool:
        return all(
            value is not None
            for value in (
                self.monthly_traffic,
                self.conversion_rate,
                self.average_value,
                self.close_rate,
            )
        )


@dataclass(slots=True)
class ContextAssessment:
    """Deterministic comparison of supplied context with observed page evidence."""

    audit_mode: AuditMode
    status: ContextStatus
    observed_business_model: str
    observed_conversions: list[str] = field(default_factory=list)
    supplied_conversion: str | None = None
    conflicts: list[str] = field(default_factory=list)
    resolution_required: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class EvidenceDocument:
    schema_version: str
    target_url: str
    fetch: FetchObservation
    page: PageEvidence | None = None
    robots: dict[str, Any] = field(default_factory=dict)
    sitemap: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AuditResult:
    schema_version: str
    score_version: str
    target_url: str
    generated_at: str
    evidence: EvidenceDocument
    findings: list[Finding]
    categories: dict[str, CategoryScore]
    overall: float | None
    confidence: float
    coverage: float
    status: str
    agent_briefs: dict[str, dict[str, Any]] = field(default_factory=dict)
    agent_results: dict[str, dict[str, Any]] = field(default_factory=dict)
    agent_failures: dict[str, str] = field(default_factory=dict)
    business_context: dict[str, Any] = field(default_factory=dict)
    context_assessment: dict[str, Any] = field(default_factory=default_context_assessment)
    competitive_evidence: dict[str, dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
