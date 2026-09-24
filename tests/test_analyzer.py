from datetime import date

import pytest

from screenshot_action import analyze_text


def test_assignment_detection():
    result = analyze_text("Assignment 3 — submit by Friday 11:59 PM")
    assert result.type == "assignment"
    assert result.entities["date"] == "Friday"
    assert result.entities["time"] == "11:59 PM"
    assert result.entities["deadline"] == "Friday"
    assert any(action.type == "create_task" for action in result.actions)


def test_relative_date_normalization():
    result = analyze_text("Appointment tomorrow at 7 PM", reference_date=date(2026, 9, 24))
    assert result.entities["date_iso"] == "2026-09-25"


def test_absolute_date_and_url_extraction():
    result = analyze_text("Interview on 2026-10-02. Apply at https://example.com/jobs")
    assert result.entities["date_iso"] == "2026-10-02"
    assert result.entities["url"] == "https://example.com/jobs"


def test_receipt_detection_and_amount():
    result = analyze_text("Receipt\nTotal: ₹1,499.00\nAmount paid")
    assert result.type == "receipt"
    assert result.entities["amount"] == "₹1,499.00"


def test_travel_detection():
    result = analyze_text("Flight AI 102 departs at 18:30 tomorrow from Gate 4")
    assert result.type == "travel"
    assert result.entities["flight"] == "AI 102"
    assert result.entities["time"] == "18:30"


def test_address_detection():
    result = analyze_text("Address: 12 Anna Salai, Chennai 600002")
    assert result.type == "address"
    assert "Anna Salai" in result.entities["address"]


def test_generic_input():
    result = analyze_text("Remember to call the lab")
    assert result.type == "generic"
    assert result.actions[0].type == "review"


def test_empty_and_wrong_type_rejected():
    with pytest.raises(ValueError):
        analyze_text("   ")
    with pytest.raises(TypeError):
        analyze_text(None)  # type: ignore[arg-type]
