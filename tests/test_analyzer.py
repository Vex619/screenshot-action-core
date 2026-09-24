from screenshot_action import analyze_text


def test_assignment_detection():
    result = analyze_text("Assignment 3 — submit by Friday 11:59 PM")
    assert result.type == "assignment"
    assert result.entities["date"] == "Friday"
    assert result.entities["time"] == "11:59 PM"
    assert any(action.type == "create_task" for action in result.actions)


def test_receipt_detection_and_amount():
    result = analyze_text("Receipt\nTotal: ₹1,499.00\nAmount paid")
    assert result.type == "receipt"
    assert result.entities["amount"] == "₹1,499.00"


def test_travel_detection():
    result = analyze_text("Flight AI 102 departs at 18:30 tomorrow from Gate 4")
    assert result.type == "travel"
    assert result.entities["flight"] == "AI 102"
    assert result.entities["time"] == "18:30"


def test_empty_input_rejected():
    try:
        analyze_text("   ")
    except ValueError:
        pass
    else:
        raise AssertionError("empty input should fail")
