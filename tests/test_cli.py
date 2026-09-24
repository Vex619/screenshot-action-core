import json
import subprocess
import sys


def test_cli_json_output():
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
    )
    data = json.loads(proc.stdout)
    assert data["type"] == "event"
    assert data["entities"]["date_iso"] == "2026-09-25"
    assert data["entities"]["time"] == "7 PM"
