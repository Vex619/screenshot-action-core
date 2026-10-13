import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import screenshot_action
from screenshot_action.cli import main

SRC = Path(__file__).resolve().parents[1] / "src"


def test_cli_json_output():
    # Run as a real subprocess; PYTHONPATH makes this work even without `pip install -e .`.
    env = {**os.environ, "PYTHONPATH": os.pathsep.join([str(SRC), os.environ.get("PYTHONPATH", "")])}
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "screenshot_action.cli",
            "text",
            "Appointment tomorrow at 7 PM",
            "--reference-date",
            "2026-09-24",
        ],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    data = json.loads(proc.stdout)
    assert data["type"] == "event"
    assert data["entities"]["date_iso"] == "2026-09-25"
    assert data["entities"]["time"] == "7 PM"


def test_cli_pretty_output_in_process(capsys):
    code = main(["text", "Appointment tomorrow at 7 PM", "--reference-date", "2026-09-24", "--pretty"])
    out = capsys.readouterr().out
    assert code == 0
    assert "\n  " in out  # indented
    assert json.loads(out)["entities"]["date_iso"] == "2026-09-25"


def test_cli_file_command(tmp_path, capsys):
    path = tmp_path / "note.txt"
    path.write_text("Receipt\nTotal ₹1,499.00\nAmount paid", encoding="utf-8")
    assert main(["file", str(path)]) == 0
    assert json.loads(capsys.readouterr().out)["type"] == "receipt"


def test_cli_errors_exit_with_code_2(tmp_path, capsys):
    assert main(["text", "   "]) == 2
    assert main(["text", "hello", "--reference-date", "24-09-2026"]) == 2
    assert main(["file", str(tmp_path / "missing.txt")]) == 2
    assert capsys.readouterr().err.count("error:") == 3


def test_cli_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert screenshot_action.__version__ in capsys.readouterr().out


def test_cli_falls_back_to_escaped_json_on_ascii_stdout(monkeypatch):
    buffer = io.BytesIO()
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(buffer, encoding="ascii"))
    assert main(["text", "Total ₹1,499.00 receipt"]) == 0
    sys.stdout.flush()
    data = json.loads(buffer.getvalue().decode("ascii"))
    assert data["entities"]["amount"] == "₹1,499.00"
