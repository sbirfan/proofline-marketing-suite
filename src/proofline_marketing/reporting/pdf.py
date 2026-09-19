"""Deterministic, client-ready PDF rendering from the canonical audit result."""

from __future__ import annotations

from html import escape
from pathlib import Path
from typing import Any

from ..models import AuditResult
from .html import ReportBrand
from .integrity import validate_report_integrity


def render_pdf(
    result: AuditResult,
    output: Path,
    brand: ReportBrand | None = None,
) -> Path:
    """Write a deterministic PDF; ReportLab remains an optional report dependency."""
    validate_report_integrity(result)
    try:
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_RIGHT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.pdfbase.pdfmetrics import stringWidth
        from reportlab.pdfgen import canvas
        from reportlab.platypus import (
            BaseDocTemplate,
            Frame,
            KeepTogether,
            PageTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
        )
    except ImportError as error:
        raise RuntimeError(
            "PDF output requires: pip install 'proofline-marketing-suite[reports]'"
        ) from error

    brand = brand or ReportBrand()
    output.parent.mkdir(parents=True, exist_ok=True)
    primary = colors.HexColor(brand.primary_color)
    accent = colors.HexColor(brand.accent_color)
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="TitleBrand", parent=styles["Title"], textColor=primary, fontSize=25, leading=30
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            textColor=primary,
            spaceBefore=14,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Finding",
            parent=styles["Heading3"],
            textColor=accent,
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SmallRight",
            parent=styles["BodyText"],
            alignment=TA_RIGHT,
            fontSize=8,
            textColor=colors.HexColor("#52606d"),
        )
    )

    def canvas_maker(*args: Any, **kwargs: Any) -> Any:
        kwargs["invariant"] = 1
        return canvas.Canvas(*args, **kwargs)

    def page_chrome(pdf_canvas: Any, doc: Any) -> None:
        pdf_canvas.saveState()
        width, height = A4
        pdf_canvas.setFillColor(primary)
        pdf_canvas.rect(0, height - 18 * mm, width, 18 * mm, stroke=0, fill=1)
        pdf_canvas.setFillColor(colors.white)
        pdf_canvas.setFont("Helvetica-Bold", 9)
        pdf_canvas.drawString(18 * mm, height - 11 * mm, brand.name)
        page = f"Page {doc.page}"
        pdf_canvas.drawString(
            width - 18 * mm - stringWidth(page, "Helvetica-Bold", 9), height - 11 * mm, page
        )
        pdf_canvas.setFillColor(colors.HexColor("#52606d"))
        pdf_canvas.setFont("Helvetica", 8)
        pdf_canvas.drawString(18 * mm, 10 * mm, brand.footer)
        pdf_canvas.restoreState()

    doc = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=25 * mm,
        bottomMargin=18 * mm,
        title="Marketing Audit",
        author=brand.name,
        creator="Proofline Marketing Suite",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="content")
    doc.addPageTemplates(PageTemplate(id="report", frames=[frame], onPage=page_chrome))

    story: list[Any] = [
        Paragraph("Marketing Audit", styles["TitleBrand"]),
        Paragraph(escape(result.target_url), styles["BodyText"]),
        Spacer(1, 6 * mm),
    ]
    score = "Unavailable" if result.overall is None else f"{result.overall:.1f}/100"
    summary = Table(
        [
            ["Status", "Overall", "Confidence", "Coverage"],
            [result.status, score, f"{result.confidence:.0%}", f"{result.coverage:.0%}"],
        ],
        colWidths=[doc.width / 4] * 4,
    )
    summary.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), primary),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#f3f6f8")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ccd5dc")),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    context = result.context_assessment
    scope = result.evidence_scope
    story.extend(
        [
            summary,
            Paragraph("Context integrity", styles["Section"]),
            Paragraph(
                escape(
                    f"Status: {context.get('status', 'unknown')}. Audit mode: "
                    f"{context.get('audit_mode', 'current_state')}. Observed business model: "
                    f"{context.get('observed_business_model', 'unknown')}."
                ),
                styles["BodyText"],
            ),
            Paragraph("Evidence scope", styles["Section"]),
            Paragraph(
                escape(
                    f"{len(scope.get('represented_urls', []))} represented page(s); "
                    f"{scope.get('unrepresented_discovered_count', 0)} discovered but "
                    "unrepresented page(s). Absence claims apply to represented pages only; "
                    "site-wide absence claims are not supported."
                ),
                styles["BodyText"],
            ),
            Paragraph("Category scores", styles["Section"]),
        ]
    )
    score_rows: list[list[Any]] = [["Category", "Score", "Confidence", "Coverage"]]
    for name, value in result.categories.items():
        score_rows.append(
            [
                name.title(),
                "Not tested" if value.score is None else f"{value.score:.1f}",
                f"{value.confidence:.0%}",
                f"{value.coverage:.0%}",
            ]
        )
    score_table = Table(
        score_rows,
        colWidths=[doc.width * 0.34, doc.width * 0.22, doc.width * 0.22, doc.width * 0.22],
        repeatRows=1,
    )
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), primary),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ccd5dc")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.extend([score_table, Paragraph("Prioritized findings", styles["Section"])])
    if not result.findings:
        story.append(
            Paragraph(
                "No deterministic findings were produced from the available evidence.",
                styles["BodyText"],
            )
        )
    for finding in result.findings:
        references = ", ".join(ref.url for ref in finding.evidence) or "No evidence URL recorded"
        story.append(
            KeepTogether(
                [
                    Paragraph(escape(finding.claim), styles["Finding"]),
                    Paragraph(
                        escape(f"{finding.severity} - {finding.id} - scope: {finding.claim_scope}"),
                        styles["BodyText"],
                    ),
                    Paragraph(
                        escape(finding.recommendation or "No recommendation recorded."),
                        styles["BodyText"],
                    ),
                    Paragraph(escape(f"Evidence: {references}"), styles["BodyText"]),
                    Spacer(1, 3 * mm),
                ]
            )
        )
    story.extend(
        [
            Paragraph("Methodology", styles["Section"]),
            Paragraph(
                f"Score version {result.score_version}. Scores use versioned rules. "
                "Confidence and coverage are separate, and unavailable evidence is never "
                "treated as absence.",
                styles["BodyText"],
            ),
            Spacer(1, 5 * mm),
            Paragraph(f"Generated {result.generated_at}", styles["SmallRight"]),
        ]
    )
    doc.build(story, canvasmaker=canvas_maker)
    return output
