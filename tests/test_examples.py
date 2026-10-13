import json
from pathlib import Path

from screenshot_action import analyze_text

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "assignment.json"


def test_assignment_example_matches_real_output():
    expected = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    actual = analyze_text("Assignment 3 — submit by Friday 11:59 PM").to_dict()
    # The version changes every release; everything else must stay in sync with the example.
    expected["metadata"].pop("version")
    actual["metadata"].pop("version")
    assert actual == expected
