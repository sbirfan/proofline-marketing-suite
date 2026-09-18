"""Structured hand-off contracts for constrained specialist agents."""

from .specialists import build_specialist_briefs, execute_specialists
from .technical import build_technical_brief

__all__ = ["build_specialist_briefs", "build_technical_brief", "execute_specialists"]
