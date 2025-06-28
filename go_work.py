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


def get_confirmation(from_mode, to_mode):
    """Get user confirmation before switching modes"""
    print(f"\nPreparing to switch from {from_mode} mode to {to_mode} mode.")
    print("This will:")
    print("1. Save your current session state")
    print("2. Close all Chrome windows")
    print("3. Restore your previous work session")

    while True:
        response = input(
            "\nDo you want to proceed? (yes/no): ").lower().strip()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("Please answer 'yes' or 'no'")


def load_work_state():
    """Load and restore work state"""
    try:
        if not get_confirmation("personal", "work"):
            print("Switch cancelled. Maintaining current session.")
            return

        # First save current state as personal
        save_current_state(PERSONAL_STATE_FILE)
        print("Saved current state as personal profile")

        # Close all current Chrome windows
        subprocess.run("""
        osascript -e '
        tell application "Google Chrome"
            close every window
        end tell'
        """, shell=True)

        # Load work state
        if os.path.exists(WORK_STATE_FILE):
            with open(WORK_STATE_FILE, 'r') as f:
                state = json.load(f)

            # Restore Chrome tabs
            for url in state.get('chrome_tabs', []):
                webbrowser.get('chrome').open_new_tab(url)

            # Launch saved applications
            for app in state.get('running_apps', []):
                try:
                    subprocess.run(['open', '-a', app])
                except:
                    print(f"Could not open {app}")

            print("Work profile restored successfully!")
        else:
            print("No saved work state found. Starting fresh work session.")
    except Exception as e:
        print(f"Error restoring work state: {e}")


if __name__ == "__main__":
    load_work_state()
