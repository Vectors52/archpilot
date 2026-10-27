# Contributing to ArchPilot

Thank you for your interest in contributing to ArchPilot!

## Getting started

1. Fork the repository on GitHub.
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/archpilot.git
   cd archpilot
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
4. Install development dependencies:
   ```bash
   .venv/bin/python -m pip install -r requirements-dev.txt
   ```

## Running tests

Run the complete test suite before submitting changes:

```bash
.venv/bin/python -m pytest -v
```

Please add or update tests when changing behavior.

## Making changes

- Keep changes focused and easy to review.
- Preserve existing functionality unless a change is intentional.
- Use clear names and readable Python code.
- Update documentation when behavior or commands change.
- Never commit passwords, access tokens, private logs, or personal data.
- Do not add automatic repair actions without discussing the change first.

## Reporting bugs

Use the Bug report issue template. Include reproduction steps and relevant error output, after removing sensitive information.

## Suggesting features

Use the Feature request issue template to explain the problem and proposed solution.

## Pull requests

1. Create a branch for your change.
2. Make your changes and add tests where appropriate.
3. Run the test suite locally.
4. Submit a pull request using the repository template.
5. Explain what changed, why it is needed, and how it was tested.

GitHub Actions runs the test suite for pushes and pull requests.

## Code of conduct

Be respectful, constructive, and welcoming. Harassment and personal attacks are not acceptable.

## License

By contributing, you agree that your contributions are distributed under the project's MIT License.
