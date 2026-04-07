"""Question generation logic for Math Challenge."""

from __future__ import annotations

import random
from typing import Any

from constants import BONUS_TEMPLATES, QUESTION_COUNTS, STORY_TEMPLATES

Question = dict[str, Any]


def _build_story_question(template: dict[str, Any], rng: random.Random) -> tuple[str, int, dict[str, Any]]:
    values = template["generator"](rng)
    if "post_process" in template:
        values = template["post_process"](values)
    answer = int(template["answer"](values))
    text = template["text"].format(**values)
    return text, answer, values


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
