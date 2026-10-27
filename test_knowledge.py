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
