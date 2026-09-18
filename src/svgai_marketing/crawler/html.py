"""Static HTML evidence extraction that excludes non-visible payloads."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

from ..models import PageEvidence

TRACKING_SIGNATURES = {
    "google_analytics": ("googletagmanager.com/gtag", "google-analytics.com"),
    "google_tag_manager": ("googletagmanager.com/gtm.js",),
    "meta_pixel": ("connect.facebook.net", "fbq("),
    "hotjar": ("static.hotjar.com",),
    "segment": ("cdn.segment.com", "analytics.load"),
    "hubspot": ("js.hs-scripts.com",),
}

HIDDEN_TAGS = {"script", "style", "svg", "template", "canvas", "head", "noscript"}
VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}


class PageParser(HTMLParser):
    def __init__(self, url: str) -> None:
        super().__init__(convert_charrefs=True)
        self.url = url
        self.page = PageEvidence(url=url)
        self._hidden_depth = 0
        self._hidden_stack: list[bool] = []
        self._heading: str | None = None
        self._heading_parts: list[str] = []
        self._button_depth = 0
        self._button_parts: list[str] = []
        self._text: list[str] = []
        self._json_ld_depth = 0
        self._json_ld_parts: list[str] = []
        self._title_depth = 0
        self._title_parts: list[str] = []
        self._active_link: dict[str, str] | None = None
        self._link_parts: list[str] = []

    @staticmethod
    def _is_hidden(tag: str, data: dict[str, str | None]) -> bool:
        style = (data.get("style") or "").lower().replace(" ", "")
        return (
            tag in HIDDEN_TAGS
            or "hidden" in data
            or (data.get("aria-hidden") or "").lower() == "true"
            or "display:none" in style
            or "visibility:hidden" in style
        )

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        data = {key.lower(): value for key, value in attrs}
        hidden_here = self._is_hidden(tag, data)
        if tag not in VOID_TAGS:
            self._hidden_stack.append(hidden_here)
        if hidden_here and tag not in VOID_TAGS:
            self._hidden_depth += 1
        if tag == "html":
            self.page.language = data.get("lang")
        if tag == "title":
            self._title_depth += 1
        if tag == "script" and (data.get("type") or "").lower() == "application/ld+json":
            self._json_ld_depth += 1
        if re.fullmatch(r"h[1-6]", tag):
            self._heading = tag
            self._heading_parts = []
        if tag == "meta":
            name = (data.get("name") or "").lower()
            prop = (data.get("property") or "").lower()
            content = data.get("content") or ""
            if name == "description":
                self.page.meta_description = content.strip() or None
            elif name == "robots":
                self.page.robots_meta = [
                    part.strip().lower() for part in content.split(",") if part.strip()
                ]
            elif prop.startswith("og:"):
                self.page.open_graph[prop] = content
        elif tag == "link":
            rel = {part.lower() for part in (data.get("rel") or "").split()}
            href = data.get("href")
            if href and "canonical" in rel:
                self.page.canonical = urljoin(self.url, href)
        elif tag == "a":
            href = data.get("href")
            if href:
                absolute = urljoin(self.url, href)
                kind = (
                    "internal"
                    if urlsplit(absolute).netloc == urlsplit(self.url).netloc
                    else "external"
                )
                self._active_link = {
                    "href": absolute,
                    "rel": data.get("rel") or "",
                    "kind": kind,
                    "text": "",
                }
                self._link_parts = []
                self.page.links.append(self._active_link)
        elif tag == "img":
            src = data.get("src")
            self.page.images.append(
                {"src": urljoin(self.url, src) if src else None, "alt": data.get("alt")}
            )
        elif tag == "form":
            self.page.forms.append(
                {
                    "action": urljoin(self.url, data.get("action") or ""),
                    "method": (data.get("method") or "get").lower(),
                    "fields": 0,
                    "required_fields": 0,
                }
            )
        elif tag in {"input", "select", "textarea"} and self.page.forms:
            self.page.forms[-1]["fields"] += 1
            if "required" in data:
                self.page.forms[-1]["required_fields"] = (
                    int(self.page.forms[-1].get("required_fields", 0)) + 1
                )
            if tag == "input" and (data.get("type") or "").lower() in {"submit", "button"}:
                value = (data.get("value") or "").strip()
                if value:
                    self.page.buttons.append(value)
        elif tag == "button":
            self._button_depth += 1
            self._button_parts = []

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == self._heading:
            value = " ".join(self._heading_parts).strip()
            if value:
                self.page.headings.setdefault(tag, []).append(value)
            self._heading = None
            self._heading_parts = []
        if tag == "button" and self._button_depth:
            value = " ".join(self._button_parts).strip()
            if value:
                self.page.buttons.append(value)
            self._button_depth -= 1
            self._button_parts = []
        if tag == "a" and self._active_link is not None:
            self._active_link["text"] = " ".join(self._link_parts).strip()
            self._active_link = None
            self._link_parts = []
        if tag == "script" and self._json_ld_depth:
            raw = "".join(self._json_ld_parts).strip()
            if raw:
                try:
                    self.page.json_ld.append(json.loads(raw))
                except json.JSONDecodeError:
                    self.page.json_ld.append({"_invalid": True})
            self._json_ld_depth -= 1
            self._json_ld_parts = []
        if tag == "title" and self._title_depth:
            self.page.title = " ".join(self._title_parts).strip() or None
            self._title_depth -= 1
            self._title_parts = []
        if tag not in VOID_TAGS and self._hidden_stack:
            hidden_here = self._hidden_stack.pop()
            if hidden_here and self._hidden_depth:
                self._hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._json_ld_depth:
            self._json_ld_parts.append(data)
        if self._title_depth:
            self._title_parts.append(data)
        if self._heading is not None and not self._hidden_depth:
            self._heading_parts.append(data)
        if self._button_depth and not self._hidden_depth:
            self._button_parts.append(data)
        if self._active_link is not None and not self._hidden_depth:
            self._link_parts.append(data)
        if not self._hidden_depth:
            cleaned = " ".join(data.split())
            if cleaned:
                self._text.append(cleaned)

    def finish(self, raw_html: str) -> PageEvidence:
        self.page.visible_text = " ".join(self._text)
        self.page.visible_word_count = len(self.page.visible_text.split())
        lowered = raw_html.lower()
        self.page.tracking_indicators = [
            name
            for name, signatures in TRACKING_SIGNATURES.items()
            if any(value in lowered for value in signatures)
        ]
        text_len = self.page.visible_word_count
        if text_len < 50 and any(
            marker in lowered
            for marker in ("__next_data__", "data-reactroot", 'id="root"', 'id="app"')
        ):
            self.page.render_required_reasons.append("low_static_text_with_app_shell")
        return self.page


def parse_html(html: str, url: str) -> PageEvidence:
    parser = PageParser(url)
    parser.feed(html)
    parser.close()
    return parser.finish(html)
