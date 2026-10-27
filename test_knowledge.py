from knowledge_base import (
    find_by_fingerprint,
    find_solution,
    load_knowledge,
)


def main():
    problems = load_knowledge()
    print(f"PASS: Loaded {len(problems)} knowledge entries.")

    disk = find_solution("disk", "root-usage-high")
    assert disk is not None, "Disk solution was not found."
    print(f"PASS: Found disk solution: {disk['title']}")

    service = find_solution(
        "systemd",
        "failed-unit:example.service",
    )
    assert service is not None, "General systemd solution was not found."
    print(f"PASS: Found systemd template: {service['title']}")

    result = find_by_fingerprint("disk", "root-usage-high")
    assert result is not None
    assert result["fingerprint"].startswith("DISK-")
    print(f"PASS: Fingerprint lookup: {result['fingerprint']}")

    missing = find_solution("network", "wifi-disconnected")
    assert missing is None, "Unknown problem should not return a solution."
    print("PASS: Unknown problems are reported as not found.")

    print("\nAll knowledge-base tests passed.")


if __name__ == "__main__":
    main()


def test_knowledge_base_loads_entries():
    problems = load_knowledge()
    assert isinstance(problems, list)
    assert len(problems) > 0


def test_disk_solution_exists():
    result = find_solution("disk", "root-usage-high")
    assert result is not None
    assert result["title"]


def test_systemd_failed_unit_template_matches_service():
    result = find_solution("systemd", "failed-unit:example.service")
    assert result is not None


def test_unknown_problem_returns_none():
    result = find_solution("network", "wifi-disconnected")
    assert result is None


def test_fingerprint_lookup_returns_fingerprint():
    result = find_by_fingerprint("disk", "root-usage-high")
    assert result is not None
    assert result["fingerprint"].startswith("DISK-")
