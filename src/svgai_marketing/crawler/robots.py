"""robots.txt retrieval with non-binary conclusions."""

from __future__ import annotations

from dataclasses import asdict
from urllib.parse import urlsplit, urlunsplit

from .http import SafeHttpClient


def inspect_robots(url: str, client: SafeHttpClient) -> dict[str, object]:
    parts = urlsplit(url)
    robots_url = urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))
    result = client.fetch(robots_url, accepted_types=("text/", "application/octet-stream"))
    payload: dict[str, object] = asdict(result.observation)
    payload["resource"] = "robots"
    payload["search_engine_access"] = "unknown"
    payload["sitemaps"] = []
    if result.body is not None:
        text = client.decode(result.body)
        payload["body"] = text
        payload["sitemaps"] = [
            line.split(":", 1)[1].strip()
            for line in text.splitlines()
            if line.lower().startswith("sitemap:")
        ]
    return payload
