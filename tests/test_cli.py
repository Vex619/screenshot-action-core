import json
import subprocess
import sys


def test_cli_json_output():
    proc = subprocess.run(
        [sys.executable, "-m", "screenshot_action.cli", "text", "Appointment tomorrow at 7 PM"],
        check=True,
        capture_output=True,
        text=True,
    )
    data = json.loads(proc.stdout)
    assert data["type"] == "event"
    assert data["entities"]["time"] == "7 PM"
