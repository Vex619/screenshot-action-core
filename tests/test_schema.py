import dataclasses
import json

import pytest

from screenshot_action import Action, analyze_text


def test_result_is_json_serializable_with_stable_keys():
    data = analyze_text("Assignment due tomorrow at 8 PM").to_dict()
    json.dumps(data)
    assert set(data) == {
        "type",
        "confidence",
        "title",
        "entities",
        "actions",
        "source_text",
        "metadata",
    }
    assert set(data["actions"][0]) == {"type", "label", "payload"}


def test_actions_are_immutable():
    action = Action("review", "Review")
    with pytest.raises(dataclasses.FrozenInstanceError):
        action.label = "changed"  # type: ignore[misc]
