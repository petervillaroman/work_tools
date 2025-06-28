#!/usr/bin/env python3

import os
import json
import subprocess
import sys
from datetime import datetime
import webbrowser

WORK_STATE_FILE = os.path.expanduser('~/.work_profile_state.json')
PERSONAL_STATE_FILE = os.path.expanduser('~/.personal_profile_state.json')


def get_running_apps():
    """Get list of running applications using AppleScript"""
    cmd = """
    osascript -e '
    tell application "System Events"
        set appList to name of every application process where background only is false
    end tell'
    """
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return [app.strip() for app in result.stdout.split(',') if app.strip()]


def get_chrome_tabs():
    """Get Chrome tabs using AppleScript"""
    cmd = """
    osascript -e '
    tell application "Google Chrome"
        set tabList to {}
        set windowList to every window
        repeat with theWindow in windowList
            set tabList to tabList & {URL of every tab of theWindow}
        end repeat
    end tell'
    """
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return [url.strip() for url in result.stdout.split(',') if url.strip()]
    except:
        return []
    return []


def save_current_state(state_file):
    """Save current state of applications and browser tabs"""
    state = {
        'timestamp': datetime.now().isoformat(),
        'running_apps': get_running_apps(),
        'chrome_tabs': get_chrome_tabs()
    }

    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)


def detect_current_mode():
    """Detect if we're currently in work or personal mode based on most recent file timestamps"""
    work_time = os.path.getmtime(
        WORK_STATE_FILE) if os.path.exists(WORK_STATE_FILE) else 0
    personal_time = os.path.getmtime(
        PERSONAL_STATE_FILE) if os.path.exists(PERSONAL_STATE_FILE) else 0

    if work_time > personal_time:
        return "work"
    return "personal"


def get_confirmation():
    """Get user confirmation before switching to sandbox mode"""
    current_mode = detect_current_mode()
    print(f"\nPreparing to switch from {current_mode} mode to sandbox mode.")
    print("This will:")
    print(f"1. Save your current {current_mode} session state")
    print("2. Close all Chrome windows")
    print("3. Start a fresh session with no saved state")

    while True:
        response = input(
            "\nDo you want to proceed? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("Please answer 'yes' or 'no'")


def start_sandbox():
    """Start a fresh sandbox session while saving current state"""
    try:
        if not get_confirmation():
            print("Switch cancelled. Maintaining current session.")
            return

        # Detect and save current mode
        current_mode = detect_current_mode()
        if current_mode == "work":
            save_current_state(WORK_STATE_FILE)
        else:
            save_current_state(PERSONAL_STATE_FILE)
        print(f"Saved current state as {current_mode} profile")

        # Close all current Chrome windows
        subprocess.run("""
        osascript -e '
        tell application "Google Chrome"
            close every window
        end tell'
        """, shell=True)

        # Start fresh Chrome window
        subprocess.run("""
        osascript -e '
        tell application "Google Chrome"
            make new window
            activate
        end tell'
        """, shell=True)

        print("Started fresh sandbox session!")
        print("Note: This session's state will not be saved.")

    except Exception as e:
        print(f"Error starting sandbox session: {e}")


if __name__ == "__main__":
    start_sandbox()
