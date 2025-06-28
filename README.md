<!-- @format -->

# Work/Personal Profile Switcher

This tool helps you manage separate work and personal profiles on your Mac by saving and restoring application states and browser sessions.

## Features

-   Saves and restores running applications
-   Saves and restores Chrome browser tabs
-   Maintains separate states for work and personal profiles
-   Provides a sandbox mode for temporary sessions
-   Automatically saves current state before switching profiles
-   Confirms with user before switching profiles

## Requirements

-   macOS
-   Python 3.x
-   Google Chrome (for browser tab management)

## Installation

1. Make the scripts executable:

```bash
chmod +x start_work.py stop_work.py sandbox.py
```

2. Add aliases to your shell configuration file (~/.zshrc):

```bash
# Work/Personal profile switching aliases
alias start_work="python3 /path/to/start_work.py"
alias stop_work="python3 /path/to/stop_work.py"
alias sandbox="python3 /path/to/sandbox.py"
```

3. Load the new aliases (or restart your terminal):

```bash
source ~/.zshrc
```

## Usage

### Switch to Work Profile

```bash
start_work
```

### Switch to Personal Profile

```bash
stop_work
```

### Start a Sandbox Session

```bash
sandbox
```

The sandbox mode provides a fresh session without saving its state. When you switch to sandbox mode:

-   Your current work/personal state is saved
-   All Chrome windows are closed
-   A fresh Chrome window is opened
-   No state is saved from the sandbox session

## How it Works

-   The scripts use AppleScript to interact with macOS applications and Chrome
-   States are saved in JSON files in your home directory:
    -   Work state: `~/.work_profile_state.json`
    -   Personal state: `~/.personal_profile_state.json`
    -   Sandbox: No state is saved
-   When switching profiles:
    1. Confirms the switch with user
    2. Current state is saved
    3. Running applications are noted
    4. Chrome tabs are saved
    5. Previous profile state is restored (except for sandbox mode)

## Notes

-   The first time you run either script, it will start fresh since no previous state exists
-   Some applications might require additional permissions to be controlled by the script
-   If an application fails to launch, you'll see a message in the console
-   Sandbox sessions are always fresh and do not persist any state
