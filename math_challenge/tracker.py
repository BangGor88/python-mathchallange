"""Daily tracker persistence for Math Challenge."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from constants import TRACKER_FILENAME

# When running as a PyInstaller one-file EXE the module lives inside a
# temporary _MEIPASS directory that is destroyed on exit.  Use the real
# EXE directory so the tracker JSON survives between launches.
if getattr(sys, "frozen", False):
    _app_dir = Path(sys.executable).resolve().parent
else:
    _app_dir = Path(__file__).resolve().parent

TRACKER_PATH = _app_dir / TRACKER_FILENAME
SETTINGS_KEY = "_settings"


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
    day = data.get(day_key)
    if not isinstance(day, dict):
        day = {}
    day.update({"score": int(score), "completed": True})
    data[day_key] = day
    _save_tracker(data)


def save_topic_score(score: int, topic: str, target_date: date | None = None) -> None:
    """Store a practice-topic result without changing daily challenge completion."""
    data = load_tracker()
    day_key = _today_key(target_date)
    day = data.get(day_key)
    if not isinstance(day, dict):
        day = {}
    practice = day.get("practice")
    if not isinstance(practice, dict):
        practice = {}
    practice[topic] = {
        "score": int(score),
        "completed": True,
    }
    day["practice"] = practice
    data[day_key] = day
    _save_tracker(data)


def get_last_topic() -> str | None:
    """Return the last selected practice topic, if one has been saved."""
    data = load_tracker()
    settings = data.get(SETTINGS_KEY)
    if not isinstance(settings, dict):
        return None
    topic = settings.get("last_topic")
    return topic if isinstance(topic, str) else None


def save_last_topic(topic: str) -> None:
    """Remember the selected practice topic without changing score history."""
    data = load_tracker()
    settings = data.get(SETTINGS_KEY)
    if not isinstance(settings, dict):
        settings = {}
    settings["last_topic"] = topic
    data[SETTINGS_KEY] = settings
    _save_tracker(data)


def get_dark_mode() -> bool:
    """Return whether dark mode was selected."""
    data = load_tracker()
    settings = data.get(SETTINGS_KEY)
    if not isinstance(settings, dict):
        return False
    return bool(settings.get("dark_mode", False))


def save_dark_mode(enabled: bool) -> None:
    """Remember the selected color mode without changing score history."""
    data = load_tracker()
    settings = data.get(SETTINGS_KEY)
    if not isinstance(settings, dict):
        settings = {}
    settings["dark_mode"] = bool(enabled)
    data[SETTINGS_KEY] = settings
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


def get_recent_scores(limit: int = 10, topic: str | None = None) -> list[tuple[str, int]]:
    """Return recent completed daily or topic scores, oldest to newest."""
    data = load_tracker()
    rows: list[tuple[str, int]] = []

    for day_key, day_value in data.items():
        if not isinstance(day_value, dict):
            continue
        try:
            date.fromisoformat(day_key)
            if topic is None:
                if not day_value.get("completed", False):
                    continue
                raw_score = day_value.get("score")
            else:
                practice = day_value.get("practice", {})
                if not isinstance(practice, dict):
                    continue
                topic_result = practice.get(topic, {})
                if not isinstance(topic_result, dict) or not topic_result.get("completed", False):
                    continue
                raw_score = topic_result.get("score")
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
