"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import BusinessContext
from .orchestrator import run_audit
from .reporting import render_html, render_markdown, render_pdf


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="svgai-marketing")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Audit a public webpage")
    audit.add_argument("url")
    audit.add_argument("--format", choices=("json", "markdown", "html", "pdf"), default="markdown")
    audit.add_argument("--output", type=Path)
    audit.add_argument("--timeout", type=float, default=15.0)
    audit.add_argument(
        "--browser-fallback",
        action="store_true",
        help="Render likely app shells when optional Playwright support is installed",
    )
    audit.add_argument("--audience", help="User-confirmed audience; never inferred from page copy")
    audit.add_argument("--offer", help="User-confirmed offer")
    audit.add_argument("--primary-conversion", help="User-confirmed primary conversion action")
    audit.add_argument("--competitor", action="append", default=[], help="Confirmed competitor URL")
    audit.add_argument(
        "--comparison-dimension", action="append", default=[], help="Confirmed comparison dimension"
    )
    audit.add_argument(
        "--confirm-competitors",
        action="store_true",
        help="Confirm competitor targets and permit bounded collection",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "audit":
        return 2
    context = BusinessContext(
        audience=args.audience,
        offer=args.offer,
        primary_conversion=args.primary_conversion,
        competitor_urls=args.competitor,
        comparison_dimensions=args.comparison_dimension,
        competitors_confirmed=args.confirm_competitors,
    )
    result = run_audit(
        args.url,
        timeout=args.timeout,
        browser_fallback=args.browser_fallback,
        business_context=context,
    )
    if args.format == "pdf":
        if not args.output:
            raise SystemExit("--output is required for PDF reports")
        render_pdf(result, args.output)
        return 0 if result.status in {"complete", "partial"} else 1
    if args.format == "json":
        body = json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
    elif args.format == "html":
        body = render_html(result)
    else:
        body = render_markdown(result)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body + "\n", encoding="utf-8")
    else:
        print(body)
    return 0 if result.status in {"complete", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
