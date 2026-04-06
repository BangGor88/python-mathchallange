"""Tests for scoring logic."""

from __future__ import annotations

from questions import generate_questions
from scorer import calculate_score, check_answers


def _build_answer_map(questions: list[dict], mode: str) -> dict[int, str]:
    answers: dict[int, str] = {}

    for question in questions:
        qid = question["id"]
        if mode == "perfect":
            answers[qid] = str(question["correct_answer"])
        elif mode == "zero":
            answers[qid] = ""
    return answers


def test_perfect_answers_score_100() -> None:
    questions = generate_questions(20260406)
    user_answers = _build_answer_map(questions, "perfect")
    results = check_answers(questions, user_answers)
    assert calculate_score(results) == 100


def test_blank_answers_score_0() -> None:
    questions = generate_questions(20260406)
    user_answers = _build_answer_map(questions, "zero")
    results = check_answers(questions, user_answers)
    assert calculate_score(results) == 0


def test_section_weighting_spot_check() -> None:
    questions = generate_questions(20260406)
    user_answers: dict[int, str] = {}

    for question in questions:
        qid = question["id"]
        if qid <= 36 or qid == 43:
            user_answers[qid] = str(question["correct_answer"])
        else:
            user_answers[qid] = "0"

    results = check_answers(questions, user_answers)
    assert calculate_score(results) == 80


def test_blank_whitespace_answer_is_wrong() -> None:
    questions = generate_questions(20260406)
    user_answers = _build_answer_map(questions, "perfect")
    user_answers[1] = "   "

    results = check_answers(questions, user_answers)

    assert results[1] is False
