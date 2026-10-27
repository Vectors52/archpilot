import json
from pathlib import Path

from fingerprint import make_fingerprint


PROJECT_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = PROJECT_DIR / "knowledge" / "problems.json"


def load_knowledge():
    """Load and validate the local problem knowledge base."""
    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
        problems = json.load(file)

    if not isinstance(problems, list):
        raise ValueError("Knowledge base must contain a JSON list.")

    for problem in problems:
        for field in ("category", "key", "title", "description", "solution"):
            if field not in problem:
                raise ValueError(f"Knowledge entry is missing: {field}")

    return problems


def find_solution(category: str, key: str):
    """Find an exact match, then try a general category-specific template."""
    problems = load_knowledge()
    category = category.strip().lower()
    key = key.strip().lower()

    for problem in problems:
        if (
            problem["category"].lower() == category
            and problem["key"].lower() == key
        ):
            return problem

    # Example: failed-unit:display-manager.service -> failed-unit
    if category == "systemd" and key.startswith("failed-unit:"):
        for problem in problems:
            if (
                problem["category"].lower() == "systemd"
                and problem["key"].lower() == "failed-unit"
            ):
                return problem

    return None


def find_by_fingerprint(category: str, key: str):
    """Return a knowledge entry together with the problem's fingerprint."""
    solution = find_solution(category, key)

    if solution is None:
        return None

    result = dict(solution)
    result["fingerprint"] = (
        f"{category.strip().upper()}-"
        f"{make_fingerprint(category, key)}"
    )
    return result
