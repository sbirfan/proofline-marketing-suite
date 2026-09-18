"""Optional rendered-page adapter."""

from __future__ import annotations

from importlib.util import find_spec


def browser_available() -> bool:
    return find_spec("playwright.sync_api") is not None


def render_html(url: str, *, timeout_ms: int = 20_000) -> str:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore[import-not-found]
    except ImportError as error:
        raise RuntimeError(
            "Install svgai-marketing-suite[browser] and Playwright Chromium"
        ) from error
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            return str(page.content())
        finally:
            browser.close()
