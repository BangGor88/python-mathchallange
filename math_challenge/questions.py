"""Question generation logic for Math Challenge."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any

from constants import BONUS_TEMPLATES, QUESTION_COUNTS, STORY_TEMPLATES

Question = dict[str, Any]

PRACTICE_TOPICS = ("fractions", "decimals", "multiplication")
PRACTICE_QUESTION_COUNT = 10


def _build_story_question(template: dict[str, Any], rng: random.Random) -> tuple[str, int, dict[str, Any]]:
    values = template["generator"](rng)
    if "post_process" in template:
        values = template["post_process"](values)
    answer = int(template["answer"](values))
    text = template["text"].format(**values)
    return text, answer, values


def _format_fraction(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def _make_topic_question(
    question_id: int,
    question_text: str,
    correct_answer: int | float | str,
    hint: str,
    template_id: str,
    template_values: dict[str, Any],
    hint_id: str,
) -> Question:
    return {
        "id": question_id,
        "section": "practice",
        "question_text": question_text,
        "correct_answer": correct_answer,
        "hint": hint,
        "template_id": template_id,
        "template_values": template_values,
        "hint_id": hint_id,
    }


def _generate_fraction_questions(rng: random.Random) -> list[Question]:
    questions: list[Question] = []

    for question_id in range(1, 4):
        numerator = rng.randint(1, 5)
        denominator = rng.randint(numerator + 1, 9)
        scale = rng.randint(2, 5)
        questions.append(
            _make_topic_question(
                question_id,
                f"Complete the equivalent fraction: {numerator}/{denominator} = ?/{denominator * scale}",
                numerator * scale,
                f"Multiply the numerator and denominator by {scale}.",
                "fraction_equivalent",
                {
                    "numerator": numerator,
                    "denominator": denominator,
                    "target_denominator": denominator * scale,
                    "scale": scale,
                },
                "fraction_equivalent",
            )
        )

    for question_id in range(4, 7):
        first = Fraction(rng.randint(1, 8), rng.randint(2, 9))
        second = Fraction(rng.randint(1, 8), rng.randint(2, 9))
        while first == second:
            second = Fraction(rng.randint(1, 8), rng.randint(2, 9))
        greater = max(first, second)
        questions.append(
            _make_topic_question(
                question_id,
                f"Which fraction is greater? {first} or {second} (enter the fraction)",
                _format_fraction(greater),
                "Use a common denominator, or compare the cross-products.",
                "fraction_compare",
                {"first": str(first), "second": str(second)},
                "fraction_compare",
            )
        )

    for question_id in range(7, 11):
        denominator = rng.randint(3, 12)
        first_numerator = rng.randint(1, denominator - 1)
        if question_id % 2:
            second_numerator = rng.randint(1, denominator - first_numerator)
            operation = "+"
            answer = Fraction(first_numerator + second_numerator, denominator)
        else:
            second_numerator = rng.randint(1, first_numerator)
            operation = "-"
            answer = Fraction(first_numerator - second_numerator, denominator)
        questions.append(
            _make_topic_question(
                question_id,
                f"{first_numerator}/{denominator} {operation} {second_numerator}/{denominator} = ?",
                _format_fraction(answer),
                "The denominators stay the same. Add or subtract the numerators, then simplify.",
                "fraction_operation",
                {
                    "first_numerator": first_numerator,
                    "second_numerator": second_numerator,
                    "denominator": denominator,
                    "operator": operation,
                },
                "fraction_operation",
            )
        )

    return questions


def _generate_decimal_questions(rng: random.Random) -> list[Question]:
    questions: list[Question] = []

    for question_id in range(1, PRACTICE_QUESTION_COUNT + 1):
        left = rng.randint(10, 999) / 100
        if question_id % 3 == 0:
            operator = "x"
            right = rng.randint(2, 9)
            right_display = str(right)
            answer = round(left * right, 4)
            hint = "Multiply as whole numbers first, then put the decimal places back."
        else:
            right = rng.randint(10, 999) / 100
            right_display = f"{right:.2f}"
            if question_id % 2 == 0:
                operator = "-"
                left, right = max(left, right), min(left, right)
                right_display = f"{right:.2f}"
                answer = round(left - right, 2)
                hint = "Line up the decimal points before subtracting."
            else:
                operator = "+"
                answer = round(left + right, 2)
                hint = "Line up the decimal points before adding."
        questions.append(
            _make_topic_question(
                question_id,
                f"{left:.2f} {operator} {right_display} = ?",
                answer,
                hint,
                "decimal_operation",
                {"left": f"{left:.2f}", "right": right_display, "operator": operator},
                f"decimal_{'multiply' if operator == 'x' else 'subtract' if operator == '-' else 'add'}",
            )
        )

    return questions


def _generate_multiplication_questions(rng: random.Random) -> list[Question]:
    questions: list[Question] = []

    for question_id in range(1, PRACTICE_QUESTION_COUNT + 1):
        if question_id <= 3:
            left = rng.randint(12, 99)
            right = rng.randint(1, 9) * 10
        elif question_id <= 6:
            left = rng.randint(1, 9) * 100
            right = rng.randint(1, 9) * 10
        elif question_id <= 8:
            left = rng.randint(100, 999)
            right = rng.randint(1, 9) * 10
        else:
            left = rng.randint(12, 99)
            right = rng.randint(1, 9) * 100
        questions.append(
            _make_topic_question(
                question_id,
                f"{left} x {right} = ?",
                left * right,
                "Multiply the non-zero digits first, then account for the tens or hundreds.",
                "multiplication",
                {"left": left, "right": right},
                "multiplication",
            )
        )

    return questions


def generate_topic_questions(topic: str, seed: int) -> list[Question]:
    """Generate a deterministic ten-question set for a Grade 5 practice topic."""
    rng = random.Random(seed)
    generators = {
        "fractions": _generate_fraction_questions,
        "decimals": _generate_decimal_questions,
        "multiplication": _generate_multiplication_questions,
    }
    try:
        return generators[topic](rng)
    except KeyError as error:
        raise ValueError(f"Unknown practice topic: {topic}") from error


def generate_questions(seed: int) -> list[Question]:
    """Generate a deterministic set of questions for the provided seed."""
    rng = random.Random(seed)
    questions: list[Question] = []
    question_id = 1

    for idx in range(QUESTION_COUNTS["operation_each"]):
        if idx < 3:
            left = rng.randint(20, 99)
            right = rng.randint(1, 9)
        else:
            left = rng.randint(1, 100)
            right = rng.randint(1, 100)
        questions.append(
            {
                "id": question_id,
                "section": "addition",
                "question_text": f"{left} + {right} = ?",
                "correct_answer": left + right,
            }
        )
        question_id += 1

    for idx in range(QUESTION_COUNTS["operation_each"]):
        if idx < 3:
            left = rng.randint(15, 99)
            right = rng.randint(1, 9)
        else:
            a = rng.randint(1, 100)
            b = rng.randint(1, 100)
            left, right = (a, b) if a >= b else (b, a)
        questions.append(
            {
                "id": question_id,
                "section": "subtraction",
                "question_text": f"{left} - {right} = ?",
                "correct_answer": left - right,
            }
        )
        question_id += 1

    for idx in range(QUESTION_COUNTS["operation_each"]):
        if idx < 3:
            left = rng.randint(2, 9)
            right = rng.randint(1, 5)
        else:
            left = rng.randint(2, 12)
            right = rng.randint(1, 20)
        questions.append(
            {
                "id": question_id,
                "section": "multiplication",
                "question_text": f"{left} x {right} = ?",
                "correct_answer": left * right,
            }
        )
        question_id += 1

    for idx in range(QUESTION_COUNTS["operation_each"]):
        if idx < 3:
            divisor = rng.randint(2, 9)
            quotient = rng.randint(2, 9)
        else:
            divisor = rng.randint(2, 10)
            quotient = rng.randint(2, 12)
        dividend = divisor * quotient
        questions.append(
            {
                "id": question_id,
                "section": "division",
                "question_text": f"{dividend} / {divisor} = ?",
                "correct_answer": quotient,
            }
        )
        question_id += 1

    selected_story_templates = rng.sample(STORY_TEMPLATES, QUESTION_COUNTS["story"])
    for template in selected_story_templates:
        text, answer, values = _build_story_question(template, rng)
        questions.append(
            {
                "id": question_id,
                "section": "story",
                "question_text": text,
                "correct_answer": answer,
                "template_id": template["id"],
                "template_values": values,
            }
        )
        question_id += 1

    bonus_template = rng.choice(BONUS_TEMPLATES)
    bonus_text, bonus_answer, bonus_values = _build_story_question(bonus_template, rng)
    questions.append(
        {
            "id": question_id,
            "section": "bonus",
            "question_text": bonus_text,
            "correct_answer": bonus_answer,
            "template_id": bonus_template["id"],
            "template_values": bonus_values,
        }
    )

    return questions
