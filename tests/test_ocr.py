import sys

import pytest

from screenshot_action.ocr import extract_text_from_image


def test_missing_ocr_extra_gives_actionable_error(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "pytesseract", None)  # simulates "not installed"
    with pytest.raises(RuntimeError, match="'ocr' extra"):
        extract_text_from_image(tmp_path / "shot.png")
