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


def test_topic_scores_are_stored_separately_from_daily_challenge(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)
    practice_day = date(2026, 4, 6)

    tracker.save_topic_score(80, "fractions", target_date=practice_day)

    assert tracker.has_completed_today(practice_day) is False
    assert tracker.get_today_score(practice_day) is None
    assert tracker.get_recent_scores(topic="fractions") == [("2026-04-06", 80)]
    assert tracker.get_recent_scores(topic="decimals") == []


def test_topic_scores_do_not_overwrite_daily_challenge_scores(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)
    practice_day = date(2026, 4, 6)

    tracker.save_today(90, target_date=practice_day)
    tracker.save_topic_score(70, "decimals", target_date=practice_day)

    assert tracker.get_today_score(practice_day) == 90
    assert tracker.get_recent_scores() == [("2026-04-06", 90)]
    assert tracker.get_recent_scores(topic="decimals") == [("2026-04-06", 70)]


def test_last_topic_is_remembered_without_creating_a_score(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)

    assert tracker.get_last_topic() is None
    tracker.save_last_topic("fractions")

    assert tracker.get_last_topic() == "fractions"
    assert tracker.get_recent_scores() == []


def test_daily_score_does_not_overwrite_topic_score(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)
    practice_day = date(2026, 4, 6)

    tracker.save_topic_score(70, "fractions", target_date=practice_day)
    tracker.save_today(90, target_date=practice_day)

    assert tracker.get_today_score(practice_day) == 90
    assert tracker.get_recent_scores(topic="fractions") == [("2026-04-06", 70)]


def test_dark_mode_preference_is_remembered_without_changing_scores(tmp_path, monkeypatch) -> None:
    tracker_file = tmp_path / "daily_tracker.json"
    monkeypatch.setattr(tracker, "TRACKER_PATH", tracker_file)

    assert tracker.get_dark_mode() is False
    tracker.save_dark_mode(True)

    assert tracker.get_dark_mode() is True
    assert tracker.get_recent_scores() == []
    tracker.save_dark_mode(False)
    assert tracker.get_dark_mode() is False
