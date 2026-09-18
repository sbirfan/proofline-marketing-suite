"""robots.txt retrieval and deterministic rule parsing."""

from __future__ import annotations

import hashlib
from dataclasses import asdict
from urllib.parse import urlsplit, urlunsplit
from urllib.robotparser import RobotFileParser

from .http import SafeHttpClient


def parse_robots(text: str) -> tuple[list[dict[str, object]], list[str]]:
    groups: list[dict[str, object]] = []
    sitemaps: list[str] = []
    agents: list[str] = []
    allow: list[str] = []
    disallow: list[str] = []
    crawl_delay: float | None = None

    def finish_group() -> None:
        nonlocal agents, allow, disallow, crawl_delay
        if agents:
            groups.append(
                {
                    "user_agents": agents,
                    "allow": allow,
                    "disallow": disallow,
                    "crawl_delay": crawl_delay,
                }
            )
        agents, allow, disallow, crawl_delay = [], [], [], None

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, value = (part.strip() for part in line.split(":", 1))
        field = field.lower()
        if field == "sitemap":
            if value and value not in sitemaps:
                sitemaps.append(value)
            continue
        if field == "user-agent":
            if agents and (allow or disallow or crawl_delay is not None):
                finish_group()
            agents.append(value.lower())
        elif field == "allow" and agents:
            allow.append(value)
        elif field == "disallow" and agents:
            disallow.append(value)
        elif field == "crawl-delay" and agents:
            try:
                crawl_delay = float(value)
            except ValueError:
                crawl_delay = None
    finish_group()
    return groups, sitemaps


def inspect_robots(url: str, client: SafeHttpClient) -> dict[str, object]:
    parts = urlsplit(url)
    robots_url = urlunsplit((parts.scheme, parts.netloc, "/robots.txt", "", ""))
    result = client.fetch(robots_url, accepted_types=("text/", "application/octet-stream"))
    payload: dict[str, object] = asdict(result.observation)
    payload.update(
        {
            "resource": "robots",
            "search_engine_access": "unknown",
            "sitemaps": [],
            "groups": [],
            "body_sha256": None,
            "line_count": 0,
        }
    )
    if result.body is None:
        return payload
    text = client.decode(result.body, result.observation.encoding)
    groups, sitemaps = parse_robots(text)
    parser = RobotFileParser(robots_url)
    parser.parse(text.splitlines())
    payload.update(
        {
            "search_engine_access": (
                "allowed" if parser.can_fetch(client.user_agent, url) else "disallowed"
            ),
            "sitemaps": sitemaps,
            "groups": groups,
            "body_sha256": hashlib.sha256(result.body).hexdigest(),
            "line_count": len(text.splitlines()),
        }
    )
    return payload
