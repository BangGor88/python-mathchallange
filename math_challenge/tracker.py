"""Daily tracker persistence for Math Challenge."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from constants import TRACKER_FILENAME

TRACKER_PATH = Path(__file__).resolve().parent / TRACKER_FILENAME


def _today_key(target_date: date | None = None) -> str:
    current = target_date or date.today()
    return current.isoformat()


def load_tracker() -> dict[str, Any]:
    """Load tracker data and create file when missing or invalid."""
    if not TRACKER_PATH.exists():
        TRACKER_PATH.write_text("{}", encoding="utf-8")
        return {}

    try:
        raw = TRACKER_PATH.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        TRACKER_PATH.write_text("{}", encoding="utf-8")
        return {}

    if not raw:
        TRACKER_PATH.write_text("{}", encoding="utf-8")
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        TRACKER_PATH.write_text("{}", encoding="utf-8")
        return {}

    if not isinstance(data, dict):
        TRACKER_PATH.write_text("{}", encoding="utf-8")
        return {}

    return data


def _save_tracker(data: dict[str, Any]) -> None:
    TRACKER_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_today(score: int, target_date: date | None = None) -> None:
    """Store completion result for the selected day (default: today)."""
    data = load_tracker()
    day_key = _today_key(target_date)
    data[day_key] = {
        "score": int(score),
        "completed": True,
    }
    _save_tracker(data)


def has_completed_today(target_date: date | None = None) -> bool:
    """Return True if quiz is completed for selected day (default: today)."""
    data = load_tracker()
    day = data.get(_today_key(target_date), {})
    return bool(day.get("completed", False))


def get_today_score(target_date: date | None = None) -> int | None:
    """Return saved score for selected day (default: today), if available."""
    data = load_tracker()
    day = data.get(_today_key(target_date), {})
    if not day.get("completed"):
        return None
    try:
        return int(day.get("score"))
    except (TypeError, ValueError):
        return None


def get_recent_scores(limit: int = 10) -> list[tuple[str, int]]:
    """Return last completed daily scores as (YYYY-MM-DD, score), oldest to newest."""
    data = load_tracker()
    rows: list[tuple[str, int]] = []

    for day_key, day_value in data.items():
        if not isinstance(day_value, dict):
            continue
        if not day_value.get("completed", False):
            continue

        try:
            date.fromisoformat(day_key)
            raw_score = day_value.get("score")
            if raw_score is None:
                continue
            score = int(raw_score)
        except (TypeError, ValueError):
            continue

        rows.append((day_key, score))

    rows.sort(key=lambda item: item[0])
    if limit <= 0:
        return []
    return rows[-limit:]
