import hashlib
from dataclasses import dataclass


@dataclass(frozen=True)
class Problem:
    category: str
    key: str
    title: str
    severity: str
    description: str
    verify_command: str
    source: str


def make_fingerprint(category: str, key: str) -> str:
    normalized = f"{category.strip().lower()}:{key.strip().lower()}"
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return digest[:8].upper()


def create_problem(
    category: str,
    key: str,
    title: str,
    severity: str,
    description: str,
    verify_command: str,
    source: str,
) -> Problem:
    if severity not in {"INFO", "WARNING", "CRITICAL"}:
        raise ValueError("Severity must be INFO, WARNING, or CRITICAL")

    return Problem(
        category=category,
        key=key,
        title=title,
        severity=severity,
        description=description,
        verify_command=verify_command,
        source=source,
    )


def format_problem(problem: Problem) -> str:
    fingerprint = make_fingerprint(problem.category, problem.key)

    return "\n".join([
        f"[{problem.severity}] {problem.title}",
        f"Fingerprint: {problem.category.upper()}-{fingerprint}",
        f"Category: {problem.category}",
        f"Details: {problem.description}",
        f"Verification: {problem.verify_command}",
        f"Documentation: {problem.source}",
    ])
