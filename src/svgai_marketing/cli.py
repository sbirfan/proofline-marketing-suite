"""Command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .orchestrator import run_audit
from .reporting.markdown import render_markdown


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="svgai-marketing")
    sub = parser.add_subparsers(dest="command", required=True)
    audit = sub.add_parser("audit", help="Audit a public webpage")
    audit.add_argument("url")
    audit.add_argument("--format", choices=("json", "markdown"), default="markdown")
    audit.add_argument("--output", type=Path)
    audit.add_argument("--timeout", type=float, default=15.0)
    audit.add_argument(
        "--browser-fallback",
        action="store_true",
        help="Render likely app shells when optional Playwright support is installed",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command != "audit":
        return 2
    result = run_audit(
        args.url,
        timeout=args.timeout,
        browser_fallback=args.browser_fallback,
    )
    body = (
        json.dumps(result.to_dict(), indent=2, ensure_ascii=False)
        if args.format == "json"
        else render_markdown(result)
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body + "\n", encoding="utf-8")
    else:
        print(body)
    return 0 if result.status in {"complete", "partial"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
