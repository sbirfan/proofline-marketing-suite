"""Optional rendered-page adapter."""

from __future__ import annotations

from importlib.util import find_spec
from urllib.parse import urlsplit


def browser_available() -> bool:
    return find_spec("playwright.sync_api") is not None


def _is_allowed_browser_request(request_url: str, page_url: str) -> bool:
    request = urlsplit(request_url)
    if request.scheme in {"about", "blob", "data"}:
        return True
    page = urlsplit(page_url)
    return (
        request.scheme in {"http", "https"}
        and request.hostname is not None
        and request.hostname == page.hostname
    )


def render_html(url: str, *, timeout_ms: int = 20_000, privacy_mode: bool = False) -> str:
    try:
        from playwright.sync_api import Route, sync_playwright
    except ImportError as error:
        raise RuntimeError(
            "Install proofline-marketing-suite[browser] and Playwright Chromium"
        ) from error
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page(service_workers="block") if privacy_mode else browser.new_page()
            if privacy_mode:

                def handle_route(route: Route) -> None:
                    if _is_allowed_browser_request(route.request.url, url):
                        route.continue_()
                    else:
                        route.abort()

                page.route("**/*", handle_route)
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            return str(page.content())
        finally:
            browser.close()
