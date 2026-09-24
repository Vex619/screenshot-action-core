"""Tiny dependency-free regression evaluator for the public analyzer."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from screenshot_action import analyze_text


def main() -> int:
    path = Path("evaluation/cases.jsonl")
    total = passed = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        case = json.loads(line)
        total += 1
        result = analyze_text(case["text"], reference_date=date(2026, 9, 24))
        type_ok = result.type == case["expected_type"]
        entities_ok = all(key in result.entities for key in case["expected_entities"])
        ok = type_ok and entities_ok
        passed += int(ok)
        status = "PASS" if ok else "FAIL"
        print(f"{status:4} {case['id']}: got={result.type} expected={case['expected_type']}")
    print(f"\n{passed}/{total} cases passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
