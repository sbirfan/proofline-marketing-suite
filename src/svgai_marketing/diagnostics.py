"""Local installation diagnostics for beta support requests."""

from __future__ import annotations

import importlib.util
import json
import platform
import sys
from dataclasses import asdict, dataclass

from . import __version__


@dataclass(frozen=True, slots=True)
class DiagnosticReport:
    version: str
    python: str
    platform: str
    supported_python: bool
    browser_extra: bool
    reports_extra: bool

    @property
    def healthy(self) -> bool:
        return self.supported_python

    def to_dict(self) -> dict[str, str | bool]:
        return asdict(self)


def collect_diagnostics() -> DiagnosticReport:
    """Return deterministic, secret-free runtime capability information."""
    version = sys.version_info
    return DiagnosticReport(
        version=__version__,
        python=platform.python_version(),
        platform=platform.system().lower() or "unknown",
        supported_python=(3, 11) <= version[:2] <= (3, 13),
        browser_extra=importlib.util.find_spec("playwright") is not None,
        reports_extra=importlib.util.find_spec("reportlab") is not None,
    )


def render_diagnostics(report: DiagnosticReport, *, as_json: bool = False) -> str:
    if as_json:
        return json.dumps({**report.to_dict(), "healthy": report.healthy}, indent=2)
    extras = (
        f"browser={'available' if report.browser_extra else 'not installed'}, "
        f"reports={'available' if report.reports_extra else 'not installed'}"
    )
    return "\n".join(
        (
            f"Proofline Marketing Suite {report.version}",
            f"Python {report.python} ({'supported' if report.supported_python else 'unsupported'})",
            f"Platform: {report.platform}",
            f"Optional extras: {extras}",
        )
    )
