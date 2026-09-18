"""Bounded sitemap and sitemap-index traversal."""

from __future__ import annotations

import gzip
from collections import deque
from dataclasses import asdict
from io import BytesIO
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree

from .http import SafeHttpClient

ACCEPTED_TYPES = (
    "text/",
    "application/xml",
    "application/octet-stream",
    "application/gzip",
)


def _same_origin(left: str, right: str) -> bool:
    first = urlsplit(left)
    second = urlsplit(right)
    return (first.scheme, first.hostname, first.port) == (
        second.scheme,
        second.hostname,
        second.port,
    )


def _decompress(body: bytes, limit: int) -> bytes:
    with gzip.GzipFile(fileobj=BytesIO(body)) as archive:
        expanded = archive.read(limit + 1)
    if len(expanded) > limit:
        raise ValueError("decompressed_sitemap_too_large")
    return expanded


def _parse_xml(body: bytes) -> tuple[str, list[str]]:
    root = ElementTree.fromstring(body)
    locations = [
        element.text.strip()
        for element in root.iter()
        if element.tag.endswith("loc") and element.text and element.text.strip()
    ]
    if root.tag.endswith("sitemapindex"):
        return "index", locations
    if root.tag.endswith("urlset"):
        return "urlset", locations
    return "unknown", locations


def inspect_sitemap(
    url: str,
    client: SafeHttpClient,
    discovered: list[str] | None = None,
    *,
    max_depth: int = 3,
    max_sitemaps: int = 20,
    max_urls: int = 1_000,
) -> dict[str, object]:
    parts = urlsplit(url)
    defaults = [urlunsplit((parts.scheme, parts.netloc, "/sitemap.xml", "", ""))]
    queue: deque[tuple[str, int]] = deque((item, 0) for item in (discovered or defaults))
    visited: set[str] = set()
    urls: list[str] = []
    seen_urls: set[str] = set()
    resources: list[dict[str, object]] = []
    truncated = False

    while queue and len(visited) < max_sitemaps:
        sitemap_url, depth = queue.popleft()
        if sitemap_url in visited:
            continue
        visited.add(sitemap_url)
        if not _same_origin(url, sitemap_url):
            resources.append(
                {
                    "url": sitemap_url,
                    "status": "not_tested",
                    "reason": "cross_origin_sitemap",
                    "depth": depth,
                    "kind": "unknown",
                    "location_count": 0,
                }
            )
            continue
        result = client.fetch(sitemap_url, accepted_types=ACCEPTED_TYPES)
        resource: dict[str, object] = asdict(result.observation)
        resource.update({"depth": depth, "kind": "unknown", "location_count": 0})
        resources.append(resource)
        if result.body is None:
            continue
        body = result.body
        if sitemap_url.lower().endswith(".gz") or result.observation.content_type in {
            "application/gzip",
            "application/x-gzip",
        }:
            try:
                body = _decompress(body, client.max_bytes)
            except (gzip.BadGzipFile, OSError, ValueError) as error:
                resource["status"] = "fetch_failed"
                resource["reason"] = str(error) or "malformed_gzip"
                continue
        try:
            kind, locations = _parse_xml(body)
        except ElementTree.ParseError:
            resource["status"] = "fetch_failed"
            resource["reason"] = "malformed_xml"
            continue
        resource["kind"] = kind
        resource["location_count"] = len(locations)
        if kind == "index":
            if depth >= max_depth:
                resource["reason"] = "max_depth_reached"
                truncated = truncated or bool(locations)
                continue
            for location in locations:
                if location not in visited:
                    queue.append((location, depth + 1))
        elif kind == "urlset":
            for location in locations:
                if location in seen_urls:
                    continue
                if len(urls) >= max_urls:
                    truncated = True
                    break
                seen_urls.add(location)
                urls.append(location)
        else:
            resource["status"] = "fetch_failed"
            resource["reason"] = "unexpected_root_element"

    if queue:
        truncated = True
    observed = [item for item in resources if item.get("status") == "observed"]
    first = resources[0] if resources else {}
    return {
        "resource": "sitemap",
        "status": "observed" if observed else first.get("status", "not_found"),
        "reason": "partial_failures"
        if observed and len(observed) != len(resources)
        else first.get("reason"),
        "search_engine_access": "unknown",
        "urls": urls,
        "url_count": len(urls),
        "resources": resources,
        "sitemap_count": len(visited),
        "truncated": truncated,
        "limits": {
            "max_depth": max_depth,
            "max_sitemaps": max_sitemaps,
            "max_urls": max_urls,
        },
    }
