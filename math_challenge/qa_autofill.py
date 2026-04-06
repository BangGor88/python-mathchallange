"""QA helper: auto-populate answer fields and optionally submit."""

from __future__ import annotations

import argparse

from app import MathChallengeApp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Auto-fill Math Challenge answers for QA.")
    parser.add_argument(
        "--mode",
        choices=["correct", "wrong", "mixed"],
        default="mixed",
        help="Autofill strategy.",
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Submit automatically after auto-filling.",
    )
    parser.add_argument(
        "--delay-ms",
        type=int,
        default=600,
        help="Delay before autofill to allow UI to render.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = MathChallengeApp(skip_daily_check=True)
    app.after(args.delay_ms, lambda: app.autofill_for_qa(mode=args.mode, submit=args.submit))
    app.mainloop()


if __name__ == "__main__":
    main()
