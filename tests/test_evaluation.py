import json
from datetime import date
from pathlib import Path

import pytest

from screenshot_action import analyze_text

CASES = [
    json.loads(line)
    for line in (Path(__file__).resolve().parents[1] / "evaluation" / "cases.jsonl")
    .read_text(encoding="utf-8")
    .splitlines()
    if line.strip()
]


@pytest.mark.parametrize("case", CASES, ids=[case["id"] for case in CASES])
def test_evaluation_case(case):
    result = analyze_text(case["text"], reference_date=date(2026, 9, 24))
    assert result.type == case["expected_type"]
    assert all(key in result.entities for key in case["expected_entities"])
