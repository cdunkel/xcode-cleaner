from __future__ import annotations

import json
import subprocess

from xcode_cleaner.constants import Category
from xcode_cleaner.models import ScanItem


def list_simulators() -> tuple[list[ScanItem], bool]:
    """List all simulators via xcrun simctl and return (items, success).

    The bool indicates whether the scan succeeded. False means xcrun was
    unavailable or timed out — callers can distinguish "no simulators"
    from "couldn't check."
    """
    try:
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except FileNotFoundError:
        return [], False
    except subprocess.TimeoutExpired:
        return [], False

    if result.returncode != 0:
        return [], False

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        return [], False

    items: list[ScanItem] = []
    for runtime, devices in data.get("devices", {}).items():
        # runtime looks like "com.apple.CoreSimulator.SimRuntime.iOS-17-5"
        runtime_name = runtime.rsplit(".", 1)[-1].replace("-", " ")
        for device in devices:
            udid = device.get("udid", "")
            if not udid:
                continue
            name = device.get("name", "Unknown")
            state = device.get("state", "Unknown")
            size_bytes = device.get("dataPathSize", 0) or 0

            items.append(
                ScanItem(
                    name=f"{name} ({runtime_name})",
                    size_bytes=size_bytes,
                    category=Category.SIMULATORS,
                    item_id=udid,
                    metadata={"state": state, "runtime": runtime_name},
                )
            )
    return items, True


def delete_simulator(udid: str) -> None:
    """Delete a simulator by UDID via xcrun simctl."""
    subprocess.run(
        ["xcrun", "simctl", "delete", udid],
        capture_output=True,
        text=True,
        timeout=60,
        check=True,
    )
