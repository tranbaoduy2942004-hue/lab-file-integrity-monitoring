#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from urllib.request import urlopen

BASE = Path("/home/ubuntu/fim-lab")
STATE = BASE / "state.json"
ALERT = BASE / "alerts.log"
RESPONSE = BASE / "response.log"
URL = "http://172.29.115.10:8080/state"

def get_state():
    with urlopen(URL, timeout=8) as r:
        return json.load(r)

def collect():
    data = get_state()
    STATE.write_text(json.dumps(data, indent=2))
    print("SOC_COLLECT_OK")
    print("BASELINE:", data["baseline_hash"])
    print("CURRENT: ", data["current_hash"])

def detect():
    if not STATE.exists():
        sys.exit("RUN_COLLECT_FIRST")

    data = json.loads(STATE.read_text())
    checks = (
        bool(data["baseline_hash"]),
        data["baseline_hash"] != data["current_hash"],
        "audit=disabled" in data["current_config"],
        "UNAUTHORIZED_CHANGE" in data["actions"]
    )

    if not all(checks):
        sys.exit(f"DETECTION_PENDING: {checks}")

    with ALERT.open("a") as f:
        f.write("FIM_UNAUTHORIZED_CHANGE_DETECTED\n")

    print("FIM_UNAUTHORIZED_CHANGE_DETECTED")

def verify():
    data = get_state()

    checks = (
        bool(data["baseline_hash"]),
        data["baseline_hash"] == data["current_hash"],
        data["baseline_config"] == data["current_config"],
        "audit=enabled" in data["current_config"],
        "FILE_RESTORED" in data["actions"],
        ALERT.exists() and
        "FIM_UNAUTHORIZED_CHANGE_DETECTED" in ALERT.read_text()
    )

    if not all(checks):
        sys.exit(f"RECOVERY_NOT_VERIFIED: {checks}")

    with RESPONSE.open("a") as f:
        f.write("FIM_RECOVERY_VERIFIED\n")

    print("FIM_RECOVERY_VERIFIED")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: soc_fim.py collect|detect|verify")

    commands = {
        "collect": collect,
        "detect": detect,
        "verify": verify
    }

    command = commands.get(sys.argv[1])
    if command is None:
        sys.exit("UNKNOWN_MODE")
    command()
