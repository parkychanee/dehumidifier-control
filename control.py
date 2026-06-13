import base64
import json
import os
import sys
import uuid
from pathlib import Path

import requests

PAT = os.environ["THINQ_PAT"]
CLIENT_ID = os.environ["THINQ_CLIENT_ID"]
DEVICE_ID = os.environ["THINQ_DEVICE_ID"]

COUNTRY = "KR"
API_KEY = "v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3"
BASE_URL = "https://api-kic.lgthinq.com"

TURN_ON_ABOVE = 55
TURN_OFF_BELOW = 50

STATE_FILE = Path(__file__).parent / "state.json"


def load_last_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"is_on": None, "we_turned_off": False}


def save_last_state(data):
    STATE_FILE.write_text(json.dumps(data))


def make_message_id():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes)[:-2].decode("utf-8")


def headers():
    return {
        "Authorization": f"Bearer {PAT}",
        "x-country": COUNTRY,
        "x-message-id": make_message_id(),
        "x-client-id": CLIENT_ID,
        "x-api-key": API_KEY,
        "x-service-phase": "OP",
        "Content-Type": "application/json",
    }


def get_state():
    url = f"{BASE_URL}/devices/{DEVICE_ID}/state"
    res = requests.get(url, headers=headers(), timeout=15)
    res.raise_for_status()
    return res.json()["response"]


def set_power(turn_on: bool):
    url = f"{BASE_URL}/devices/{DEVICE_ID}/control"
    mode = "POWER_ON" if turn_on else "POWER_OFF"
    payload = {"operation": {"dehumidifierOperationMode": mode}}
    res = requests.post(url, headers=headers(), json=payload, timeout=15)
    res.raise_for_status()
    print(f"Set power -> {mode}: {res.json()}")


def main():
    try:
        state = get_state()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch device state: {e}")
        sys.exit(1)

    try:
        humidity = state["humidity"]["currentHumidity"]
        is_on = state["operation"]["dehumidifierOperationMode"] == "POWER_ON"
    except (KeyError, TypeError) as e:
        print(f"Unexpected state response format: {state} ({e})")
        sys.exit(1)

    print(f"Current humidity: {humidity}%, power on: {is_on}")

    last = load_last_state()
    we_turned_off = last.get("we_turned_off", False)

    try:
        if humidity >= TURN_ON_ABOVE and not is_on:
            if last.get("is_on") is True and not we_turned_off:
                print(
                    "Humidity is high but the dehumidifier turned itself off "
                    "since the last check (and we didn't turn it off). "
                    "This likely means the water tank is full - skipping auto restart."
                )
                save_last_state({"is_on": is_on, "we_turned_off": we_turned_off})
                sys.exit(1)
            set_power(True)
            we_turned_off = False
        elif humidity <= TURN_OFF_BELOW and is_on:
            set_power(False)
            we_turned_off = True
        else:
            print("No action needed.")
            if is_on:
                we_turned_off = False
    except requests.exceptions.RequestException as e:
        print(f"Failed to send control command: {e}")
        sys.exit(1)

    save_last_state({"is_on": is_on, "we_turned_off": we_turned_off})


if __name__ == "__main__":
    main()
