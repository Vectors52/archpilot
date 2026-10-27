# ArchPilot

An interactive terminal-based diagnostic tool for Arch Linux.

## Features
- System diagnostics
- Disk usage checks
- Failed systemd unit detection
- Network and DNS checks
- Package update detection without installing updates
- Local knowledge base and problem fingerprints
- Diagnostic report export

## Requirements
- Arch Linux
- Python 3.10 or newer

## Installation

    git clone https://github.com/YOUR_USERNAME/archpilot.git
    cd archpilot
    python -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt

## Run

    python app.py

## Tests

    python test_severity.py
    python test_update_check.py
    python test_fingerprint.py
    python test_knowledge.py

## Safety
ArchPilot performs diagnostics only. It does not automatically repair the system or install updates.

## License
MIT License. See LICENSE.

## Install the `archpilot` command

After cloning the repository and installing the Python dependencies, run:

    chmod +x run.sh install.sh
    ./install.sh

Ensure `~/.local/bin` is in your `PATH`. Then launch ArchPilot from any terminal:

    archpilot

The launcher uses the project's `.venv` Python interpreter when available.
