"""Collection entry point for one-page audits."""

from __future__ import annotations

from typing import cast
from urllib.parse import urlsplit

from ..models import EvidenceDocument, ObservationStatus
from .browser import browser_available, render_html
from .html import parse_html
from .http import SafeHttpClient
from .robots import inspect_robots
from .sitemap import inspect_sitemap


class EvidenceCollector:
    def __init__(self, *, timeout: float = 15.0, browser_fallback: bool = False) -> None:
        self.client = SafeHttpClient(timeout=timeout)
        self.browser_fallback = browser_fallback

    def collect(self, url: str) -> EvidenceDocument:
        normalized = normalize_url(url)
        result = self.client.fetch(
            normalized, accepted_types=("text/html", "application/xhtml+xml")
        )
        page = None
        if result.body is not None:
            final_url = result.observation.final_url or normalized
            page = parse_html(
                self.client.decode(result.body, result.observation.content_type), final_url
            )
            if page.render_required_reasons:
                result.observation.status = ObservationStatus.RENDER_REQUIRED
                result.observation.reason = ",".join(page.render_required_reasons)
                result.observation.confidence = 0.35
                if self.browser_fallback and browser_available():
                    try:
                        rendered = render_html(
                            final_url, timeout_ms=int(self.client.timeout * 1000)
                        )
                    except (RuntimeError, TimeoutError):
                        result.observation.reason = "browser_render_failed"
                    else:
                        page = parse_html(rendered, final_url)
                        result.observation.status = ObservationStatus.OBSERVED
                        result.observation.reason = None
                        result.observation.render_mode = "browser"
                        result.observation.confidence = 0.9
        robots = inspect_robots(normalized, self.client)
        discovered = cast(list[str], robots.get("sitemaps", []))
        sitemap = inspect_sitemap(normalized, self.client, discovered or None)
        return EvidenceDocument(
            schema_version="2.0",
            target_url=normalized,
            fetch=result.observation,
            page=page,
            robots=robots,
            sitemap=sitemap,
        )


def normalize_url(url: str) -> str:
    candidate = url.strip()
    if "://" not in candidate:
        candidate = "https://" + candidate
    parts = urlsplit(candidate)
    if parts.scheme not in {"http", "https"} or not parts.netloc:
        raise ValueError(f"Unsupported URL: {url}")
    return candidate
