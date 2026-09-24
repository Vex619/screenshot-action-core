"""Deterministic text-to-action analysis.

This module deliberately has no network/model dependency. Model-backed adapters can
produce the same ActionResult schema later without coupling the core to a provider.
"""

from __future__ import annotations

import re

from .schema import Action, ActionResult

_PATTERNS: list[tuple[str, list[str], float]] = [
    ("assignment", ["assignment", "homework", "problem set", "submit by", "due"], 0.90),
    ("event", ["event", "appointment", "meeting", "seminar", "workshop", "starts at"], 0.86),
    ("travel", ["flight", "boarding", "departure", "arrival", "gate", "pnr"], 0.90),
    ("receipt", ["receipt", "total", "subtotal", "tax", "invoice", "amount paid"], 0.88),
    ("job", ["job", "application", "interview", "recruiter", "apply by", "position"], 0.84),
    ("recipe", ["recipe", "ingredients", "cook", "bake", "preheat", "servings"], 0.84),
    ("address", ["address", "street", "road", "avenue", "pin code", "pincode"], 0.80),
]

_TIME_RE = re.compile(r"\b(?:[01]?\d|2[0-3]):[0-5]\d\s?(?:am|pm)?\b|\b(?:[1-9]|1[0-2])(?::[0-5]\d)?\s?(?:am|pm)\b", re.I)
_DATE_RE = re.compile(r"\b(?:today|tomorrow|tonight|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", re.I)
_AMOUNT_RE = re.compile(r"(?:₹|rs\.?|inr|\$|€|£)\s?\d[\d,]*(?:\.\d{1,2})?", re.I)
_FLIGHT_RE = re.compile(r"\b(?:[A-Z]{2}\s?\d{2,4}|[A-Z]{2,3}-\d{2,4})\b")


def _classify(text: str) -> tuple[str, float]:
    normalized = text.lower()
    best = ("generic", 0.45)
    for kind, terms, confidence in _PATTERNS:
        hits = sum(term in normalized for term in terms)
        if hits and (hits > 1 or confidence > best[1]):
            score = min(0.99, confidence + max(0, hits - 1) * 0.03)
            if score > best[1]:
                best = (kind, score)
    return best


def _entities(text: str, kind: str) -> dict[str, str]:
    entities: dict[str, str] = {}
    date = _DATE_RE.search(text)
    time = _TIME_RE.search(text)
    amount = _AMOUNT_RE.search(text)
    flight = _FLIGHT_RE.search(text)

    if date:
        entities["date"] = date.group(0)
    if time:
        entities["time"] = time.group(0).strip()
    if amount:
        entities["amount"] = amount.group(0)
    if kind == "travel" and flight:
        entities["flight"] = flight.group(0)

    if kind in {"assignment", "job", "event"} and date:
        entities["deadline" if kind in {"assignment", "job"} else "date"] = date.group(0)

    return entities


def _title(text: str, kind: str) -> str | None:
    line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not line:
        return None
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"^(assignment|homework|event|receipt|flight)\s*[:\-–—]?\s*", "", line, flags=re.I)
    return line[:120] or kind.title()


def _actions(kind: str, title: str | None) -> list[Action]:
    label = title or kind.title()
    actions: list[Action] = []
    if kind in {"assignment", "job", "event"}:
        actions.append(Action("create_task", f"Review {label}"))
        actions.append(Action("set_reminder", "Set a reminder before the deadline"))
    elif kind == "travel":
        actions.append(Action("add_to_calendar", "Add travel details to your calendar"))
        actions.append(Action("set_reminder", "Set a travel reminder"))
    elif kind == "receipt":
        actions.append(Action("save_record", "Save purchase details"))
        actions.append(Action("review_expense", "Review this expense"))
    elif kind == "recipe":
        actions.append(Action("create_shopping_list", "Create a shopping list from ingredients"))
    elif kind == "address":
        actions.append(Action("open_map", "Open this location in a map"))
    else:
        actions.append(Action("review", "Review extracted information"))
    return actions


def analyze_text(text: str) -> ActionResult:
    """Analyze extracted screenshot text without executing any actions."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("text must not be empty")

    kind, confidence = _classify(cleaned)
    entities = _entities(cleaned, kind)
    title = _title(cleaned, kind)
    return ActionResult(kind, round(confidence, 2), title, entities, _actions(kind, title), cleaned)
