from collections import Counter


VALID_SEVERITIES = {"INFO", "WARNING", "CRITICAL"}


def summarize_severities(severities):
    counts = Counter()

    for severity in severities:
        normalized = severity.strip().upper()

        if normalized not in VALID_SEVERITIES:
            raise ValueError(f"Unknown severity: {severity}")

        counts[normalized] += 1

    return {
        "INFO": counts["INFO"],
        "WARNING": counts["WARNING"],
        "CRITICAL": counts["CRITICAL"],
    }
