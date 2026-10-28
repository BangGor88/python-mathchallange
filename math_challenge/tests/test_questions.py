"""Tests for question generation."""

from __future__ import annotations

from constants import TOPIC_HINT_TRANSLATIONS, TOPIC_QUESTION_TRANSLATIONS
from questions import generate_questions, generate_topic_questions


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


def test_topic_questions_are_deterministic_and_have_ten_questions() -> None:
    for topic in ("fractions", "decimals", "multiplication"):
        first_run = generate_topic_questions(topic, 20260406)
        second_run = generate_topic_questions(topic, 20260406)

        assert len(first_run) == 10
        assert first_run == second_run
        assert all(question["section"] == "practice" for question in first_run)


def test_fraction_questions_include_fraction_and_equivalence_practice() -> None:
    questions = generate_topic_questions("fractions", 20260406)

    assert any("equivalent fraction" in question["question_text"] for question in questions)
    assert any("Which fraction is greater?" in question["question_text"] for question in questions)
    assert any("/" in question["question_text"] and "+" in question["question_text"] for question in questions)


def test_multiplication_topic_uses_tens_and_hundreds() -> None:
    questions = generate_topic_questions("multiplication", 20260406)

    assert all(int(question["question_text"].split(" x ")[1].split(" =")[0]) % 10 == 0 for question in questions)
    for question in questions[3:6]:
        left = int(question["question_text"].split(" x ")[0])
        assert left % 100 == 0
    for question in questions[6:8]:
        left = int(question["question_text"].split(" x ")[0])
        assert 100 <= left <= 999


def test_unknown_topic_is_rejected() -> None:
    try:
        generate_topic_questions("geometry", 20260406)
    except ValueError as error:
        assert "Unknown practice topic" in str(error)
    else:
        raise AssertionError("Unknown practice topics should be rejected.")


def test_topic_questions_and_hints_are_translated_for_all_languages() -> None:
    for topic in ("fractions", "decimals", "multiplication"):
        for question in generate_topic_questions(topic, 20260406):
            for language in ("en", "sv", "de", "id"):
                TOPIC_QUESTION_TRANSLATIONS[language][question["template_id"]].format(
                    **question["template_values"]
                )
                TOPIC_HINT_TRANSLATIONS[language][question["hint_id"]].format(
                    **question["template_values"]
                )
