"""Sitemap inspection with explicit parse and access states."""

from __future__ import annotations

import gzip
from dataclasses import asdict
from urllib.parse import urlsplit, urlunsplit
from xml.etree import ElementTree

from .http import SafeHttpClient


def inspect_sitemap(
    url: str,
    client: SafeHttpClient,
    discovered: list[str] | None = None,
) -> dict[str, object]:
    parts = urlsplit(url)
    sitemap_url = (
        discovered or [urlunsplit((parts.scheme, parts.netloc, "/sitemap.xml", "", ""))]
    )[0]
    result = client.fetch(
        sitemap_url,
        accepted_types=("text/", "application/xml", "application/octet-stream", "application/gzip"),
    )
    payload: dict[str, object] = asdict(result.observation)
    payload["resource"] = "sitemap"
    payload["search_engine_access"] = "unknown"
    payload["urls"] = []
    payload["nested_sitemaps"] = []
    if result.body is None:
        return payload
    body = result.body
    if sitemap_url.endswith(".gz"):
        try:
            body = gzip.decompress(body)
        except (gzip.BadGzipFile, OSError):
            payload["status"] = "fetch_failed"
            payload["reason"] = "malformed_gzip"
            return payload
    try:
        root = ElementTree.fromstring(body)
    except ElementTree.ParseError:
        payload["status"] = "fetch_failed"
        payload["reason"] = "malformed_xml"
        return payload
    locations = [
        element.text.strip()
        for element in root.iter()
        if element.tag.endswith("loc") and element.text
    ]
    if root.tag.endswith("sitemapindex"):
        payload["nested_sitemaps"] = locations
    else:
        payload["urls"] = locations
    return payload
