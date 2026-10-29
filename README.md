# ArchPilot

An interactive terminal-based diagnostic tool for Arch Linux.

ArchPilot helps users identify common system issues and review possible
solutions without automatically modifying their system.

## Features

- System diagnostics
- Root filesystem usage checks
- Failed systemd unit detection
- Network connectivity and DNS checks
- Package update detection without installing updates
- Local knowledge base and deterministic problem fingerprints
- Diagnostic report export
- Interactive terminal interface

## Requirements

- Arch Linux
- Python 3.10 or newer
- Internet access for network checks and package update information

## Installation

Clone the repository:

```bash
git clone https://github.com/am2q/archpilot.git
cd archpilot
```

Create a virtual environment and install the application dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## Run ArchPilot

Run directly:

```bash
.venv/bin/python app.py
```

Alternatively, use the launcher:

```bash
chmod +x run.sh install.sh
./install.sh
archpilot
```

Ensure `~/.local/bin` is in your `PATH` to run `archpilot` from any terminal.

## Development setup

Install the development dependencies:

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
```

## Tests

Run the complete automated test suite:

```bash
.venv/bin/python -m pytest -v
```

GitHub Actions runs these tests on pushes and pull requests.

## Contributing

Bug reports, feature suggestions, and pull requests are welcome.

- Read [CONTRIBUTING.md](CONTRIBUTING.md).
- Use the GitHub issue templates to report bugs or suggest features.
- Use the pull request template when submitting changes.

## Safety

ArchPilot is a diagnostic tool. It does not automatically repair the system
or install package updates. Review any suggested commands before running them.

## License

ArchPilot is distributed under the MIT License. See [LICENSE](LICENSE).
