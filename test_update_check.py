from app import interpret_update_result


def test_updates_available():
    lines, failed = interpret_update_result(
        0,
        "alpha 1-1 -> 1-2\nbeta 2-1 -> 2-2\n",
        "",
    )
    assert not failed
    assert "Updates available: 2 package(s)." in lines
    assert "alpha 1-1 -> 1-2" in lines


def test_no_pending_updates():
    lines, failed = interpret_update_result(2, "", "")
    assert not failed
    assert any("No pending updates" in line for line in lines)


def test_command_failure():
    lines, failed = interpret_update_result(1, "", "network error")
    assert failed
    assert any("UNKNOWN" in line for line in lines)
    assert any("network error" in line for line in lines)


def test_unexpected_empty_success():
    lines, failed = interpret_update_result(0, "", "")
    assert failed
    assert any("UNKNOWN" in line for line in lines)


if __name__ == "__main__":
    tests = [
        test_updates_available,
        test_no_pending_updates,
        test_command_failure,
        test_unexpected_empty_success,
    ]
    for test in tests:
        test()
        print(f"PASS: {test.__name__}")
    print("All update-check tests passed.")
