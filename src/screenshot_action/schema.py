"""Stable public data structures for Screenshot → Action."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Action:
    """A proposed next step. Actions are descriptive and never executed by core."""

    type: str
    label: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionResult:
    """Normalized analysis result."""

    type: str
    confidence: float
    title: str | None
    entities: dict[str, str]
    actions: list[Action]
    source_text: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
