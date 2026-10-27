# Changelog

All notable changes to ArchPilot are documented in this file.

## [Unreleased]

- Improvements and fixes planned for future releases.

## [0.1.0] - Initial release

### Added
- Interactive terminal-based system diagnosis.
- Root filesystem usage checks.
- Failed systemd unit detection.
- Network connectivity and DNS checks.
- Package update detection without installing updates.
- Local knowledge base and problem fingerprints.
- Diagnostic report export.
- Command-line launcher and installer.
- Automated test suite with pytest.
- GitHub Actions workflow for automated testing.
- GitHub issue and pull request templates.
- Contributor documentation.

### Safety
- Diagnostics do not automatically repair the system.
- Package updates are detected but not installed automatically.
