from fingerprint import create_problem, format_problem, make_fingerprint


def main():
    problem = create_problem(
        category="disk",
        key="root-usage-high",
        title="High root filesystem usage",
        severity="WARNING",
        description=(
            "Root filesystem usage is at least 90%. "
            "This does not necessarily mean the system is broken."
        ),
        verify_command="df -h /",
        source="https://wiki.archlinux.org/title/File_systems",
    )

    print("=== PROBLEM FINGERPRINT TEST ===")
    print(format_problem(problem))
    print()

    first = make_fingerprint("disk", "root-usage-high")
    second = make_fingerprint("disk", "root-usage-high")

    if first != second:
        raise SystemExit("FAIL: Fingerprint is not repeatable.")

    print("PASS: Identical problem keys produce the same fingerprint.")


if __name__ == "__main__":
    main()


def test_fingerprint_is_repeatable():
    first = make_fingerprint("disk", "root-usage-high")
    second = make_fingerprint("disk", "root-usage-high")
    assert first == second


def test_fingerprint_changes_for_different_problem_keys():
    first = make_fingerprint("disk", "root-usage-high")
    second = make_fingerprint("network", "dns-failure")
    assert first != second


def test_create_and_format_problem():
    problem = create_problem(
        category="disk",
        key="root-usage-high",
        title="High root filesystem usage",
        severity="WARNING",
        description="Root filesystem usage is high.",
        verify_command="df -h /",
        source="https://wiki.archlinux.org/title/File_systems",
    )
    formatted = format_problem(problem)
    assert isinstance(formatted, str)
    assert formatted
    assert "High root filesystem usage" in formatted
