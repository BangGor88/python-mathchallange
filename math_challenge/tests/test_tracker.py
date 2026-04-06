"""Tests for daily tracker persistence."""

from __future__ import annotations

import json
from datetime import date

import tracker


def test_new_file_created_if_absent(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)

    data = tracker.load_tracker()

    assert data == {}
    assert tracker_file.exists()


def test_has_completed_today_false_on_empty_file(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    tracker_file.write_text("{}", encoding="utf-8")
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)

    assert tracker.has_completed_today(date(2026, 4, 6)) is False


def test_save_today_sets_score_and_completion(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)

    tracker.save_today(85, target_date=date(2026, 4, 6))

    assert tracker.has_completed_today(date(2026, 4, 6)) is True

    content = json.loads(tracker_file.read_text(encoding="utf-8"))
    assert content["2026-04-06"]["score"] == 85


def test_multiple_days_stored_independently(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)

    tracker.save_today(70, target_date=date(2026, 4, 6))
    tracker.save_today(90, target_date=date(2026, 4, 7))

    content = json.loads(tracker_file.read_text(encoding="utf-8"))

    assert content["2026-04-06"]["score"] == 70
    assert content["2026-04-07"]["score"] == 90


def test_get_recent_scores_returns_last_10_sorted(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)

    for day in range(1, 13):
        tracker.save_today(day, target_date=date(2026, 4, day))

    recent = tracker.get_recent_scores(limit=10)

    assert len(recent) == 10
    assert recent[0][0] == "2026-04-03"
    assert recent[-1][0] == "2026-04-12"
    assert recent[-1][1] == 12
