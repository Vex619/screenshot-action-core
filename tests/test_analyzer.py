from datetime import date

import pytest

import screenshot_action
from screenshot_action import analyze_text

REFERENCE = date(2026, 9, 24)  # a Thursday


def test_assignment_detection():
    result = analyze_text("Assignment 3 — submit by Friday 11:59 PM")
    assert result.type == "assignment"
    assert result.entities["date"] == "Friday"
    assert result.entities["time"] == "11:59 PM"
    assert result.entities["deadline"] == "Friday"
    assert any(action.type == "create_task" for action in result.actions)


def test_relative_date_normalization():
    result = analyze_text("Appointment tomorrow at 7 PM", reference_date=REFERENCE)
    assert result.entities["date_iso"] == "2026-09-25"


def test_tonight_means_today_not_tomorrow():
    result = analyze_text("Dinner tonight at 8 PM", reference_date=REFERENCE)
    assert result.entities["date_iso"] == "2026-09-24"


def test_yesterday_and_weekday_normalization():
    assert analyze_text("Paid yesterday", reference_date=REFERENCE).entities["date_iso"] == (
        "2026-09-23"
    )
    assert analyze_text("Submit by Friday", reference_date=REFERENCE).entities["date_iso"] == (
        "2026-09-25"
    )


def test_absolute_date_and_url_extraction():
    result = analyze_text("Interview on 2026-10-02. Apply at https://example.com/jobs")
    assert result.entities["date_iso"] == "2026-10-02"
    assert result.entities["url"] == "https://example.com/jobs"


def test_url_drops_trailing_sentence_punctuation():
    result = analyze_text("Apply at https://example.com/jobs.")
    assert result.entities["url"] == "https://example.com/jobs"


def test_date_is_not_mistaken_for_phone_number():
    result = analyze_text("Interview on 2026-10-02. Apply at https://example.com/jobs")
    assert "phone" not in result.entities


def test_real_phone_number_is_still_extracted():
    result = analyze_text("Call the recruiter on +91 98765 43210 before Friday")
    assert result.entities["phone"] == "+91 98765 43210"


def test_receipt_detection_and_amount():
    result = analyze_text("Receipt\nTotal: ₹1,499.00\nAmount paid")
    assert result.type == "receipt"
    assert result.entities["amount"] == "₹1,499.00"


def test_amount_is_not_matched_inside_words_or_with_trailing_comma():
    result = analyze_text("Receipt\nOpen hours 9 to 5\nUsers 100\nTotal $5, paid")
    assert result.entities["amount"] == "$5"


def test_amount_with_indian_digit_grouping():
    result = analyze_text("Total ₹1,23,456.50")
    assert result.entities["amount"] == "₹1,23,456.50"


def test_travel_detection():
    result = analyze_text("Flight AI 102 departs at 18:30 tomorrow from Gate 4")
    assert result.type == "travel"
    assert result.entities["flight"] == "AI 102"
    assert result.entities["time"] == "18:30"


def test_flight_ignores_am_pm_markers():
    result = analyze_text("Flight departs 6:30 PM 12 Oct")
    assert result.type == "travel"
    assert "flight" not in result.entities


def test_address_detection():
    result = analyze_text("Address: 12 Anna Salai, Chennai 600002")
    assert result.type == "address"
    assert "Anna Salai" in result.entities["address"]


@pytest.mark.parametrize(
    "text",
    [
        "Meeting at 5 PM you must attend",
        "Meeting at 5 PM, you must attend\nBring your laptop",
        "Room 12 has the first test",
    ],
)
def test_ordinary_text_is_not_an_address(text):
    assert "address" not in analyze_text(text).entities


def test_address_does_not_swallow_the_next_line():
    result = analyze_text("12 Anna Salai, Chennai 600002\nBring your laptop and ID card")
    assert result.entities["address"] == "12 Anna Salai, Chennai 600002"


def test_keywords_match_whole_words_only():
    assert analyze_text("Pickup at 221 Baker Street, London").type == "address"  # not "bake"
    assert analyze_text("Please investigate the taxi").type == "generic"  # not "gate" / "tax"


def test_plural_keywords_still_match():
    assert analyze_text("Two meetings and three events").type == "event"
    assert analyze_text("Overdue").type == "assignment"


def test_generic_input():
    result = analyze_text("Remember to call the lab")
    assert result.type == "generic"
    assert result.actions[0].type == "review"


def test_title_is_the_first_line_and_keeps_its_wording():
    result = analyze_text("Assignment 3 — submit by Friday 11:59 PM\nProblems 1-5 from chapter 17")
    assert result.title == "Assignment 3 — submit by Friday 11:59 PM"
    assert result.actions[0].label == "Review Assignment 3 — submit by Friday 11:59 PM"


def test_title_drops_a_label_only_when_followed_by_a_separator():
    assert analyze_text("Assignment: Problem Set 3\nDue Friday").title == "Problem Set 3"
    assert analyze_text("Appointment tomorrow at 7 PM").title == "Appointment tomorrow at 7 PM"


def test_title_is_truncated_to_120_characters():
    assert len(analyze_text("x" * 300).title) == 120


def test_source_text_keeps_line_breaks_and_collapses_spaces():
    result = analyze_text("Receipt\n\n  Total:   ₹10  ")
    assert result.source_text == "Receipt\nTotal: ₹10"


def test_classification_sees_phrases_split_across_lines():
    assert analyze_text("Amount\npaid").type == "receipt"


def test_event_reminder_label_mentions_the_event():
    result = analyze_text("Seminar tomorrow at 18:30", reference_date=REFERENCE)
    reminder = next(action for action in result.actions if action.type == "set_reminder")
    assert reminder.label == "Set a reminder before the event"
    assert reminder.payload == {"date": "2026-09-25", "time": "18:30"}


def test_metadata_reports_the_package_version():
    assert analyze_text("hello").metadata["version"] == screenshot_action.__version__


def test_empty_and_wrong_type_rejected():
    with pytest.raises(ValueError):
        analyze_text("   ")
    with pytest.raises(TypeError):
        analyze_text(None)  # type: ignore[arg-type]
