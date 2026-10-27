import platform
import shutil
import socket
import subprocess
from datetime import datetime
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Footer, Header, Static

from fingerprint import create_problem, format_problem
from knowledge_base import find_by_fingerprint
from severity import summarize_severities


PROJECT_DIR = Path(__file__).resolve().parent
REPORT_DIR = PROJECT_DIR / "reports"


def problem_report(
    category,
    key,
    title,
    severity,
    description,
    verify_command,
    source,
):
    problem = create_problem(
        category=category,
        key=key,
        title=title,
        severity=severity,
        description=description,
        verify_command=verify_command,
        source=source,
    )
    lines = format_problem(problem).splitlines()

    try:
        knowledge = find_by_fingerprint(category, key)
    except (OSError, ValueError) as error:
        lines.extend([
            "",
            "LOCAL KNOWLEDGE BASE: Unavailable",
            f"Reason: {error}",
        ])
        return lines

    if knowledge is None:
        lines.extend([
            "",
            "LOCAL KNOWLEDGE BASE: No matching solution found.",
        ])
        return lines

    lines.extend([
        "",
        "MATCHING KNOWLEDGE BASE ENTRY",
        f"Title: {knowledge['title']}",
        f"Fingerprint: {knowledge['fingerprint']}",
        f"Description: {knowledge['description']}",
        f"Verification: {knowledge.get('verify_command', 'Not specified')}",
        "",
        "Suggested steps:",
    ])

    for index, step in enumerate(knowledge.get("solution", []), start=1):
        lines.append(f"  {index}. {step}")

    lines.extend([
        "",
        f"Risk warning: {knowledge.get('risk', 'Review the steps before acting.')}",
        f"Documentation: {knowledge.get('source', 'Not specified')}",
        "These are suggestions, not automatically executed repairs.",
    ])

    return lines


def interpret_update_result(returncode, stdout, stderr):
    """Interpret checkupdates output without changing the system."""
    output = stdout.strip()
    errors = stderr.strip()
    lines = []

    if returncode == 0 and output:
        updates = [line for line in output.splitlines() if line.strip()]
        lines.append(f"Updates available: {len(updates)} package(s).")
        lines.extend(updates[:20])

        if len(updates) > 20:
            lines.append(
                f"... and {len(updates) - 20} more package(s)."
            )
        return lines, False

    if returncode == 2:
        return ["No pending updates found by checkupdates."], False

    lines.append(
        "UNKNOWN: package update check did not complete "
        f"successfully (exit code {returncode})."
    )
    if errors:
        lines.append(f"Details: {errors[:500]}")
    return lines, True


class ArchPilot(App):
    TITLE = "ArchPilot"
    SUB_TITLE = "System Diagnosis"

    BINDINGS = [("q", "quit", "Exit")]

    CSS = """
    Screen {
        align: center middle;
    }

    #panel {
        width: 90%;
        max-width: 90;
        height: 90%;
        max-height: 90%;
        border: round $accent;
        padding: 1 2;
    }

    #results {
        height: 1fr;
        min-height: 10;
        overflow-y: auto;
        margin-bottom: 1;
    }

    Button {
        width: 100%;
        margin-top: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.report_lines = [
            "ArchPilot has not run a system check yet."
        ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="panel"):
            yield Static(
                "ARCHPILOT\n"
                "Diagnose problems. Understand your system.\n\n"
                "Choose a task below to begin.",
                id="results",
            )

            yield Button(
                "1. Run System Diagnosis",
                id="check",
                variant="primary",
            )

            yield Button(
                "2. Test Knowledge Base",
                id="knowledge",
                variant="warning",
            )

            yield Button(
                "3. Export Diagnosis Report",
                id="export",
                variant="success",
            )

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "check":
            self.run_diagnosis()
        elif event.button.id == "knowledge":
            self.test_knowledge_base()
        elif event.button.id == "export":
            self.export_report()

    def run_diagnosis(self) -> None:
        lines = [
            "ARCHPILOT SYSTEM DIAGNOSIS",
            "=" * 32,
            f"Date: {datetime.now().astimezone().isoformat(timespec='seconds')}",
            f"Kernel: {platform.release()}",
            f"Python: {platform.python_version()}",
            "",
            "DIAGNOSTIC FINDINGS",
            "-" * 32,
        ]

        findings = 0

        # Check root filesystem
        try:
            usage = shutil.disk_usage("/")
            free_gb = usage.free / (1024 ** 3)
            total_gb = usage.total / (1024 ** 3)
            used_percent = usage.used / usage.total * 100

            lines.append(
                f"Root filesystem: {used_percent:.1f}% used "
                f"({free_gb:.1f} GB free of {total_gb:.1f} GB)"
            )

            if used_percent >= 90:
                lines.append(
                    "WARNING: Root filesystem usage is at least 90%. "
                    "Check which files or directories use space before deleting anything."
                )
                lines.append("")
                lines.extend(problem_report(
                    category="disk",
                    key="root-usage-high",
                    title="High root filesystem usage",
                    severity="WARNING",
                    description=(
                        f"Root filesystem usage is {used_percent:.1f}%. "
                        "Inspect disk usage before removing files."
                    ),
                    verify_command="df -h /",
                    source="https://wiki.archlinux.org/title/File_systems",
                ))
                findings += 1
            else:
                lines.append("OK: Root filesystem usage is below 90%.")

        except OSError as error:
            lines.append(f"UNKNOWN: Disk check failed: {error}")
            findings += 1

        lines.append("")

        # Check failed systemd units
        try:
            process = subprocess.run(
                [
                    "systemctl",
                    "--failed",
                    "--no-legend",
                    "--plain",
                    "--no-pager",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )

            if process.returncode != 0:
                lines.append(
                    "UNKNOWN: Could not inspect systemd units."
                )
                if process.stderr.strip():
                    lines.append(process.stderr.strip()[:500])
                findings += 1
            else:
                failed_units = [
                    item.strip()
                    for item in process.stdout.splitlines()
                    if item.strip()
                ]

                if not failed_units:
                    lines.append("OK: No failed systemd units reported.")
                else:
                    lines.append(
                        f"WARNING: {len(failed_units)} failed systemd unit(s) found."
                    )
                    findings += len(failed_units)

                    for unit in failed_units[:10]:
                        unit_name = unit.split()[0]
                        lines.append(f"  - {unit}")

                        lines.append("")
                        lines.extend(problem_report(
                            category="systemd",
                            key=f"failed-unit:{unit_name}",
                            title=f"Failed systemd unit: {unit_name}",
                            severity="WARNING",
                            description=(
                                f"systemctl reported this unit as failed: "
                                f"{unit_name}. The cause is not determined yet."
                            ),
                            verify_command=f"systemctl status {unit_name}",
                            source="https://wiki.archlinux.org/title/Systemd",
                        ))

                    if len(failed_units) > 10:
                        lines.append(
                            f"Only the first 10 units are shown; "
                            f"{len(failed_units) - 10} more were detected."
                        )

                    lines.extend([
                        "",
                        "Suggested next step:",
                        "Inspect a unit with: systemctl status UNIT",
                        "Official guide: https://wiki.archlinux.org/title/Systemd",
                    ])

        except (OSError, subprocess.TimeoutExpired) as error:
            lines.append(
                f"UNKNOWN: systemd check could not complete: {error}"
            )
            findings += 1

        # Read-only network checks
        lines.extend(["", "NETWORK CHECKS", "-" * 32])

        try:
            with socket.create_connection(
                ("1.1.1.1", 443), timeout=3
            ):
                ip_connect_ok = True
        except OSError:
            ip_connect_ok = False

        try:
            socket.getaddrinfo(
                "archlinux.org", 443, type=socket.SOCK_STREAM
            )
            dns_ok = True
        except OSError:
            dns_ok = False

        if ip_connect_ok:
            lines.append("OK: Public IP connectivity test succeeded.")
        else:
            lines.append(
                "WARNING: Public IP connectivity test failed or timed out."
            )
            lines.append("")
            lines.extend(problem_report(
                category="network",
                key="internet-connectivity-failure",
                title="Public IP connectivity test failed",
                severity="WARNING",
                description=(
                    "The connection test to 1.1.1.1:443 failed. "
                    "This does not prove all internet access is unavailable."
                ),
                verify_command="ip route",
                source=(
                    "https://wiki.archlinux.org/title/Network_configuration"
                ),
            ))
            findings += 1

        if dns_ok:
            lines.append("OK: DNS resolution for archlinux.org succeeded.")
        elif ip_connect_ok:
            lines.append(
                "WARNING: DNS resolution failed while IP connectivity succeeded."
            )
            lines.append("")
            lines.extend(problem_report(
                category="network",
                key="dns-failure",
                title="DNS name resolution failed",
                severity="WARNING",
                description=(
                    "archlinux.org could not be resolved although "
                    "the public IP connectivity test succeeded."
                ),
                verify_command="getent hosts archlinux.org",
                source=(
                    "https://wiki.archlinux.org/title/Domain_name_resolution"
                ),
            ))
            findings += 1
        else:
            lines.append(
                "UNKNOWN: DNS also failed, but the connectivity test failed; "
                "a DNS-specific fault cannot be confirmed."
            )

        # Read-only Arch Linux package update check
        lines.extend(["", "PACKAGE UPDATES", "-" * 32])

        checkupdates_path = shutil.which("checkupdates")

        if not checkupdates_path:
            lines.append(
                "UNKNOWN: checkupdates is not installed; "
                "no package update check was performed."
            )
        else:
            try:
                update_result = subprocess.run(
                    [checkupdates_path],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    check=False,
                )

                update_lines, update_failed = interpret_update_result(
                    update_result.returncode,
                    update_result.stdout,
                    update_result.stderr,
                )
                lines.extend(update_lines)

                if update_failed:
                    findings += 1

                lines.append(
                    "This check does not install or apply package updates."
                )

            except (OSError, subprocess.TimeoutExpired) as error:
                lines.append(
                    f"UNKNOWN: package update check failed: {error}"
                )
                findings += 1

        # Summarize the visible diagnostic status lines.
        severity_events = []
        for line in lines:
            item = line.strip()
            if item.startswith("CRITICAL:"):
                severity_events.append("CRITICAL")
            elif item.startswith(("WARNING:", "UNKNOWN:", "Updates available:")):
                severity_events.append("WARNING")
            elif item.startswith("OK:"):
                severity_events.append("INFO")

        severity_summary = summarize_severities(severity_events)

        lines.extend([
            "",
            "SEVERITY SUMMARY",
            "-" * 32,
            f"INFO: {severity_summary['INFO']}",
            f"WARNING: {severity_summary['WARNING']}",
            f"CRITICAL: {severity_summary['CRITICAL']}",
            "",
            "-" * 32,
            f"Findings requiring attention: {findings}",
            "No repair commands were executed.",
            "This report contains diagnostic indicators, not a full system audit.",
        ])

        self.report_lines = lines

        self.query_one("#results", Static).update(
            "\n".join(lines)
        )

    def test_knowledge_base(self) -> None:
        lines = [
            "ARCHPILOT KNOWLEDGE BASE TEST",
            "=" * 32,
            "DEMO ONLY: This is not a real system finding.",
            "Testing a sample high-disk-usage problem.",
            "",
        ]

        lines.extend(problem_report(
            category="disk",
            key="root-usage-high",
            title="High root filesystem usage (TEST)",
            severity="WARNING",
            description=(
                "This is a simulated problem used to test "
                "knowledge-base lookup and display."
            ),
            verify_command="df -h /",
            source="https://wiki.archlinux.org/title/File_systems",
        ))

        lines.extend([
            "",
            "Knowledge base test completed.",
            "No repair commands were executed.",
            "This demo does not replace the diagnosis report for export.",
        ])

        self.query_one("#results", Static).update("\\n".join(lines))

    def export_report(self) -> None:
        if self.report_lines == [
            "ArchPilot has not run a system check yet."
        ]:
            self.query_one("#results", Static).update(
                "Run System Diagnosis first, then export your report."
            )
            return

        try:
            REPORT_DIR.mkdir(parents=True, exist_ok=True)

            filename = (
                "archpilot-"
                + datetime.now().strftime("%Y%m%d-%H%M%S")
                + ".txt"
            )

            report_path = REPORT_DIR / filename
            report_path.write_text(
                "\n".join(self.report_lines) + "\n",
                encoding="utf-8",
            )

            self.query_one("#results", Static).update(
                "REPORT EXPORTED SUCCESSFULLY\n\n"
                f"Saved to:\n{report_path}\n\n"
                "Review the report before sharing it publicly."
            )

        except OSError as error:
            self.query_one("#results", Static).update(
                f"Could not save the report:\n{error}"
            )


if __name__ == "__main__":
    ArchPilot().run()
