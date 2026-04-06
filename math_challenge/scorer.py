"""Scoring and answer checking logic for Math Challenge."""

from __future__ import annotations

from typing import Any

from constants import POINTS_PER_SECTION, QUESTION_COUNTS


def _parse_numeric(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()
    if not text:
        return None

    try:
        return float(text)
    except ValueError:
        return None


def _is_close_enough(left: float, right: float, tolerance: float = 1e-9) -> bool:
    return abs(left - right) <= tolerance


def check_answers(questions: list[dict[str, Any]], user_answers: dict[int, Any]) -> dict[int, bool]:
    """Return correctness map keyed by question id."""
    results: dict[int, bool] = {}

    for question in questions:
        question_id = int(question["id"])
        expected = _parse_numeric(question["correct_answer"])
        provided = _parse_numeric(user_answers.get(question_id, ""))

        if expected is None or provided is None:
            results[question_id] = False
            continue

        results[question_id] = _is_close_enough(provided, expected)

    return results


def calculate_section_breakdown(results: dict[int, bool]) -> dict[str, int]:
    """Return per-section points with integer totals for UI display."""
    operation_total = QUESTION_COUNTS["operation_each"] * 4
    story_total = QUESTION_COUNTS["story"]

    section_scores = {
        "A": 0.0,
        "B": 0.0,
        "bonus": 0.0,
    }

    for question_id, is_correct in results.items():
        if not is_correct:
            continue

        if 1 <= question_id <= operation_total:
            section_scores["A"] += POINTS_PER_SECTION["addition"]
        elif (operation_total + 1) <= question_id <= (operation_total + story_total):
            section_scores["B"] += POINTS_PER_SECTION["story"]
        elif question_id == (operation_total + story_total + 1):
            section_scores["bonus"] += POINTS_PER_SECTION["bonus"]

    return {
        "A": int(round(section_scores["A"])),
        "B": int(round(section_scores["B"])),
        "bonus": int(round(section_scores["bonus"])),
    }


def calculate_score(results: dict[int, bool]) -> int:
    """Calculate total score from correctness map."""
    breakdown = calculate_section_breakdown(results)
    total = breakdown["A"] + breakdown["B"] + breakdown["bonus"]
    return max(0, min(100, int(total)))


def get_star_rating(score: int) -> int:
    """Convert score to star count using required thresholds."""
    if score < 40:
        return 0
    if score <= 59:
        return 2
    if score <= 74:
        return 3
    if score <= 89:
        return 4
    return 5
