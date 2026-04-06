"""Tests for question generation."""

from __future__ import annotations

from questions import generate_questions


def test_generate_questions_has_total_count() -> None:
    questions = generate_questions(20260406)
    assert len(questions) == 43


def test_division_questions_are_integer_answers() -> None:
    questions = generate_questions(20260406)
    division_questions = [q for q in questions if q["section"] == "division"]

    assert len(division_questions) == 9
    for question in division_questions:
        assert isinstance(question["correct_answer"], int)


def test_seed_determinism_and_variation() -> None:
    first_run = generate_questions(20260406)
    second_run = generate_questions(20260406)
    third_run = generate_questions(20260407)

    assert first_run == second_run
    assert first_run != third_run


def test_all_correct_answers_are_numeric() -> None:
    questions = generate_questions(20260406)
    for question in questions:
        assert isinstance(question["correct_answer"], (int, float))
