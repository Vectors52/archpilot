from severity import summarize_severities


def test_all_severity_levels():
    result = summarize_severities(["INFO", "WARNING", "CRITICAL"])
    assert result == {"INFO": 1, "WARNING": 1, "CRITICAL": 1}


def test_repeated_levels():
    result = summarize_severities(["WARNING", "WARNING", "INFO"])
    assert result == {"INFO": 1, "WARNING": 2, "CRITICAL": 0}


def test_empty_results():
    result = summarize_severities([])
    assert result == {"INFO": 0, "WARNING": 0, "CRITICAL": 0}


def test_invalid_level():
    try:
        summarize_severities(["UNKNOWN"])
    except ValueError:
        return
    raise AssertionError("Invalid severity should raise ValueError")


if __name__ == "__main__":
    tests = [
        test_all_severity_levels,
        test_repeated_levels,
        test_empty_results,
        test_invalid_level,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print("All severity tests passed.")
