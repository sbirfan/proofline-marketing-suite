from proofline_marketing.agents.specialists import build_specialist_briefs, execute_specialists
from proofline_marketing.models import (
    BusinessContext,
    EvidenceDocument,
    FetchObservation,
    ObservationStatus,
    PageEvidence,
)


def evidence(url: str = "https://example.test/") -> EvidenceDocument:
    return EvidenceDocument(
        schema_version="2.0",
        target_url=url,
        fetch=FetchObservation(url=url, status=ObservationStatus.OBSERVED),
        page=PageEvidence(url=url, title="Example", visible_text="hostile raw page text"),
    )


def result(agent: str) -> dict:
    return {
        "schema_version": "1.0",
        "agent": agent,
        "interpretations": [],
        "recommendations": [],
        "dimension_assessments": [
            {
                "dimension": "clarity",
                "rating": "adequate",
                "confidence": 0.8,
                "evidence_urls": ["https://example.test/"],
                "limitations": [],
            }
        ],
    }


def test_all_briefs_are_structured_and_report_missing_research() -> None:
    briefs = build_specialist_briefs(evidence(), [], BusinessContext(), {})

    assert len(briefs) == 6
    assert "visible_text" not in briefs["content-strategist"]["structured_evidence"]
    assert "Audience research" in briefs["content-strategist"]["limitations"][0]
    assert "explicitly confirmed" in briefs["competitive-analyst"]["limitations"][0]
    assert "directional" in briefs["growth-strategist"]["limitations"][0]


def test_specialist_failure_is_isolated_from_valid_result() -> None:
    briefs = build_specialist_briefs(evidence(), [], BusinessContext(), {})

    def succeeds(brief: dict) -> dict:
        return result(brief["agent"])

    def fails(brief: dict) -> dict:
        del brief
        raise RuntimeError("adapter offline")

    results, failures = execute_specialists(
        briefs,
        {"content-strategist": succeeds, "growth-strategist": fails},
    )

    assert "content-strategist" in results
    assert failures == {"growth-strategist": "RuntimeError: adapter offline"}


def test_unsupported_estimate_is_rejected_without_corrupting_other_results() -> None:
    briefs = build_specialist_briefs(evidence(), [], BusinessContext(), {})

    def estimate(brief: dict) -> dict:
        payload = result(brief["agent"])
        payload["interpretations"] = [
            {
                "kind": "estimate",
                "claim": "Revenue will increase",
                "finding_ids": [],
                "evidence_urls": [brief["target_url"]],
                "confidence": 0.5,
                "limitations": [],
                "assumptions": [],
            }
        ]
        return payload

    results, failures = execute_specialists(briefs, {"growth-strategist": estimate})

    assert not results
    assert "unsupported estimate" in failures["growth-strategist"]


def test_competitor_brief_uses_only_confirmed_normalized_evidence() -> None:
    context = BusinessContext(
        competitor_urls=["https://competitor.test/"],
        comparison_dimensions=["positioning"],
        competitors_confirmed=True,
    )
    briefs = build_specialist_briefs(
        evidence(), [], context, {"https://competitor.test/": evidence("https://competitor.test/")}
    )

    comparison = briefs["competitive-analyst"]["comparison_evidence"][0]
    assert comparison["source_url"] == "https://competitor.test/"
    assert "visible_text" not in comparison
