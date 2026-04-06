"""Generate an answer key file for QA from the current question set."""

from __future__ import annotations

import argparse
from pathlib import Path

from constants import default_daily_seed
from questions import generate_questions


def build_answer_key_text(seed: int) -> str:
    questions = generate_questions(seed)
    lines: list[str] = [
        f"Math Challenge QA Answer Key",
        f"Seed: {seed}",
        f"Total Questions: {len(questions)}",
        "",
    ]

    for question in questions:
        qid = question["id"]
        section = question["section"]
        text = question["question_text"]
        answer = question["correct_answer"]
        lines.append(f"Q{qid:02d} [{section}] {text}")
        lines.append(f"Answer: {answer}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate QA answer key for Math Challenge.")
    parser.add_argument(
        "--seed",
        type=int,
        default=default_daily_seed(),
        help="Question seed to generate (default: today's seed).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Output file path (default: answer_key_<seed>.txt in app folder).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    seed = int(args.seed)

    output_path = (
        Path(args.output)
        if args.output
        else Path(__file__).resolve().parent / f"answer_key_{seed}.txt"
    )

    content = build_answer_key_text(seed)
    output_path.write_text(content, encoding="utf-8")

    print(f"Answer key generated: {output_path}")


if __name__ == "__main__":
    main()
