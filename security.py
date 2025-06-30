import streamlit as st
import requests
import json
from pathlib import Path

# This grimoire holds the sacred laws of our fortress.
# It tracks mortal souls by their IP and curses those who are unworthy.

BLOCKLIST_PATH = Path("ip_blocklist.json")
MAX_ATTEMPTS = 3


def get_user_ip():
    """Fetches the user's public IP address from the ether."""
    try:
        # We consult the all-seeing eye of ipify
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json().get("ip", "unknown_soul")
    except requests.exceptions.RequestException:
        # If the eye is blind, we grant them a generic soul ID for this session
        return "unknown_soul"


def load_blocklist():
    """Loads the list of cursed souls from our persistent grimoire."""
    if BLOCKLIST_PATH.exists():
        try:
            with open(BLOCKLIST_PATH, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}  # If the grimoire is corrupted, we start anew
    return {}


def save_blocklist(blocklist):
    """Saves the updated list of cursed souls to the grimoire."""
    with open(BLOCKLIST_PATH, "w") as f:
        json.dump(blocklist, f, indent=4)


def check_ip_status(ip):
    """
    Checks if a soul is cursed.
    Returns: (is_blocked, attempts_made)
    """
    blocklist = load_blocklist()
    return blocklist.get(ip, {}).get("blocked", False), blocklist.get(ip, {}).get("attempts", 0)


def update_ip_status(ip, success):
    """Updates the status of a soul after an incantation attempt."""
    blocklist = load_blocklist()

    if ip not in blocklist:
        blocklist[ip] = {"attempts": 0, "blocked": False}

    if success:
        # The soul is worthy, their sins are forgiven.
        if ip in blocklist:
            del blocklist[ip]
    else:
        # The soul has failed. Their transgressions are recorded.
        blocklist[ip]["attempts"] += 1
        if blocklist[ip]["attempts"] >= MAX_ATTEMPTS:
            blocklist[ip]["blocked"] = True
            st.error("YOU ARE CURSED.")  # A final damning message

    save_blocklist(blocklist)

