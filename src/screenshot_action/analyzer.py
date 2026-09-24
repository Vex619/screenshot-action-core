"""Deterministic text-to-action analysis.

The analyzer is deliberately network-free. OCR, vision models, and external
integrations can be layered around this module without coupling the core to a
provider or allowing the core to execute side effects.
"""

from __future__ import annotations

import re
from datetime import date

from .schema import Action, ActionResult

_PATTERNS: list[tuple[str, tuple[str, ...], float]] = [
    ("assignment", ("assignment", "homework", "problem set", "submit by", "due"), 0.90),
    ("event", ("event", "appointment", "meeting", "seminar", "workshop", "starts at"), 0.86),
    ("travel", ("flight", "boarding", "departure", "arrival", "gate", "pnr"), 0.90),
    ("receipt", ("receipt", "total", "subtotal", "tax", "invoice", "amount paid"), 0.88),
    ("job", ("job", "application", "interview", "recruiter", "apply by", "position"), 0.84),
    ("recipe", ("recipe", "ingredients", "cook", "bake", "preheat", "servings"), 0.84),
    ("address", ("address", "street", "road", "avenue", "pin code", "pincode"), 0.80),
]

_TIME_RE = re.compile(
    r"\b(?:[01]?\d|2[0-3]):[0-5]\d\s?(?:am|pm)?\b"
    r"|\b(?:[1-9]|1[0-2])(?::[0-5]\d)?\s?(?:am|pm)\b",
    re.IGNORECASE,
)
_DATE_RE = re.compile(
    r"\b(?:today|tomorrow|tonight|yesterday|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    re.IGNORECASE,
)
_ABS_DATE_RE = re.compile(
    r"\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4})\b"
)
_AMOUNT_RE = re.compile(r"(?:₹|rs\.?|inr|\$|€|£)\s?\d[\d,]*(?:\.\d{1,2})?", re.IGNORECASE)
_FLIGHT_RE = re.compile(r"\b(?:[A-Z]{2}\s?\d{2,4}|[A-Z]{2,3}-\d{2,4})\b")
_URL_RE = re.compile(r"https?://[^\s)]+", re.IGNORECASE)
_EMAIL_RE = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d ()-]{7,}\d)(?!\d)")
_ADDRESS_RE = re.compile(
    r"\b(?:address\s*[:\-]?\s*)?\d{1,5}[^\n,]{0,80}(?:street|st|road|rd|avenue|ave|lane|ln|salai|highway|hwy)\b[^\n]{0,80}",
    re.IGNORECASE,
)


def _normalized_terms(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def _classify(text: str) -> tuple[str, float, dict[str, int]]:
    normalized = text.lower()
    scores: list[tuple[str, float, int]] = []
    for kind, terms, base in _PATTERNS:
        hits = sum(normalized.count(term) for term in terms)
        if hits:
            score = min(0.99, base + min(0.06, 0.03 * (hits - 1)))
            scores.append((kind, score, hits))
    if not scores:
        return "generic", 0.45, {}
    scores.sort(key=lambda item: (item[1], item[2]), reverse=True)
    kind, score, _ = scores[0]
    return kind, round(score, 2), {k: h for k, _, h in scores}


def _first_match(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    return match.group(0).strip() if match else None


def _entities(text: str, kind: str, reference_date: date | None) -> dict[str, str]:
    entities: dict[str, str] = {}
    date_match = _first_match(_DATE_RE, text)
    abs_date = _first_match(_ABS_DATE_RE, text)
    time = _first_match(_TIME_RE, text)
    amount = _first_match(_AMOUNT_RE, text)
    flight = _first_match(_FLIGHT_RE, text)
    url = _first_match(_URL_RE, text)
    email = _first_match(_EMAIL_RE, text)
    phone = _first_match(_PHONE_RE, text)
    address = _first_match(_ADDRESS_RE, text)

    if date_match:
        entities["date"] = date_match
        if reference_date:
            normalized = _normalize_relative_date(date_match, reference_date)
            if normalized:
                entities["date_iso"] = normalized
    elif abs_date:
        entities["date"] = abs_date
        normalized = _normalize_absolute_date(abs_date)
        if normalized:
            entities["date_iso"] = normalized
    if time:
        entities["time"] = time
    if amount:
        entities["amount"] = amount
    if kind == "travel" and flight:
        entities["flight"] = flight
    if url:
        entities["url"] = url
    if email:
        entities["email"] = email
    if phone:
        entities["phone"] = phone
    if address:
        entities["address"] = address

    if kind in {"assignment", "job"} and (date_match or abs_date):
        entities["deadline"] = date_match or abs_date or ""

    return entities


def _normalize_absolute_date(value: str) -> str | None:
    pieces = re.split(r"[-/]", value)
    try:
        if len(pieces[0]) == 4:
            y, m, d = map(int, pieces)
        else:
            d, m, y = map(int, pieces)
        return date(y, m, d).isoformat()
    except ValueError:
        return None


def _normalize_relative_date(value: str, reference_date: date) -> str | None:
    token = value.lower()
    if token == "today":
        return reference_date.isoformat()
    if token in {"tomorrow", "tonight"}:
        from datetime import timedelta
        return (reference_date + timedelta(days=1)).isoformat()
    if token == "yesterday":
        from datetime import timedelta
        return (reference_date - timedelta(days=1)).isoformat()

    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    if token in weekdays:
        from datetime import timedelta
        target = weekdays[token]
        delta = (target - reference_date.weekday()) % 7
        return (reference_date + timedelta(days=delta)).isoformat()
    return None


def _title(text: str, kind: str) -> str | None:
    line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not line:
        return None
    line = re.sub(r"\s+", " ", line)
    line = re.sub(
        r"^(assignment|homework|event|receipt|flight|appointment|meeting)\s*[:\-–—]?\s*",
        "",
        line,
        flags=re.IGNORECASE,
    )
    return line[:120] or kind.title()


def _actions(kind: str, title: str | None, entities: dict[str, str]) -> list[Action]:
    label = title or kind.title()
    actions: list[Action] = []
    if kind in {"assignment", "job", "event"}:
        actions.append(Action("create_task", f"Review {label}"))
        reminder_payload = {}
        if "date_iso" in entities:
            reminder_payload["date"] = entities["date_iso"]
        if "time" in entities:
            reminder_payload["time"] = entities["time"]
        actions.append(Action("set_reminder", "Set a reminder before the deadline", reminder_payload))
    elif kind == "travel":
        payload = {k: entities[k] for k in ("flight", "date_iso", "time") if k in entities}
        actions.append(Action("add_to_calendar", "Add travel details to your calendar", payload))
        actions.append(Action("set_reminder", "Set a travel reminder"))
    elif kind == "receipt":
        actions.append(Action("save_record", "Save purchase details", {"amount": entities.get("amount", "")}))
        actions.append(Action("review_expense", "Review this expense"))
    elif kind == "recipe":
        actions.append(Action("create_shopping_list", "Create a shopping list from ingredients"))
    elif kind == "address":
        actions.append(Action("open_map", "Open this location in a map"))
    else:
        actions.append(Action("review", "Review extracted information"))
    return actions


def analyze_text(text: str, *, reference_date: date | None = None) -> ActionResult:
    """Analyze extracted screenshot text without executing any actions.

    ``reference_date`` is optional and only affects normalization of relative dates.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cleaned = _normalized_terms(text)
    if not cleaned:
        raise ValueError("text must not be empty")

    kind, confidence, matched_terms = _classify(cleaned)
    entities = _entities(cleaned, kind, reference_date)
    title = _title(cleaned, kind)
    metadata = {
        "analyzer": "deterministic",
        "version": "0.2.0",
        "matched_terms": matched_terms,
        "reference_date": reference_date.isoformat() if reference_date else None,
    }
    return ActionResult(
        kind,
        confidence,
        title,
        entities,
        _actions(kind, title, entities),
        cleaned,
        metadata,
    )
