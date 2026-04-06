"""Application constants for Math Challenge."""

from __future__ import annotations

from datetime import date

# UI configuration
APP_TITLE = "Math Challenge 🧮"
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 900

COLORS = {
    "background": "#EAF7EC",
    "panel": "#DDF1E1",
    "card": "#F4FBF6",
    "accent": "#2F8F4E",
    "accent_hover": "#287A42",
    "secondary": "#66B37A",
    "correct": "#27AE60",
    "wrong": "#E74C3C",
    "bonus": "#FFB300",
    "text": "#1E3A2B",
    "muted": "#557A66",
}

FONTS = {
    "title": ("Bahnschrift", 30, "bold"),
    "header": ("Bahnschrift", 20, "bold"),
    "question": ("Bahnschrift", 15, "bold"),
    "label": ("Bahnschrift", 13),
    "button": ("Bahnschrift", 16, "bold"),
    "score": ("Bahnschrift", 52, "bold"),
    "star": ("Bahnschrift", 30, "bold"),
}

SECTION_HEADINGS = {
    "addition": "➕ Addition",
    "subtraction": "➖ Subtraction",
    "multiplication": "✖️ Multiplication",
    "division": "➗ Division",
    "story": "📖 Story Questions",
    "bonus": "⭐ Bonus Question",
}

POINTS_PER_SECTION = {
    "addition": 60 / 36,
    "subtraction": 60 / 36,
    "multiplication": 60 / 36,
    "division": 60 / 36,
    "story": 20 / 6,
    "bonus": 20,
}

QUESTION_COUNTS = {
    "operation_each": 9,
    "story": 6,
    "bonus": 1,
}

TRACKER_FILENAME = "daily_tracker.json"
MINIMUM_PASS_SCORE = 40
SCORE_LOG_DAYS = 10


def default_daily_seed() -> int:
    """Return deterministic seed in YYYYMMDD format for current day."""
    return int(date.today().strftime("%Y%m%d"))


STORY_TEMPLATES = [
    {
        "id": "story_1",
        "text": "Emma has {a} apples. She gives {b} to her friend. How many does she have left?",
        "generator": lambda rng: {
            "a": rng.randint(15, 60),
            "b": rng.randint(1, 14),
        },
        "answer": lambda values: values["a"] - values["b"],
    },
    {
        "id": "story_2",
        "text": "A box holds {a} chocolates. There are {b} boxes. How many chocolates in total?",
        "generator": lambda rng: {
            "a": rng.randint(6, 18),
            "b": rng.randint(2, 12),
        },
        "answer": lambda values: values["a"] * values["b"],
    },
    {
        "id": "story_3",
        "text": "A class of {a} students is split into groups of {b}. How many groups?",
        "generator": lambda rng: {
            "b": rng.randint(2, 10),
            "q": rng.randint(2, 8),
        },
        "answer": lambda values: values["a"] // values["b"],
        "post_process": lambda values: {**values, "a": values["b"] * values["q"]},
    },
    {
        "id": "story_4",
        "text": "Tom saves £{a} each week. How much does he save in {b} weeks?",
        "generator": lambda rng: {
            "a": rng.randint(3, 25),
            "b": rng.randint(2, 12),
        },
        "answer": lambda values: values["a"] * values["b"],
    },
    {
        "id": "story_5",
        "text": "There are {a} pages in a book. Maya reads {b} pages per day. How many days to finish?",
        "generator": lambda rng: {
            "b": rng.randint(5, 20),
            "q": rng.randint(3, 15),
        },
        "answer": lambda values: values["a"] // values["b"],
        "post_process": lambda values: {**values, "a": values["b"] * values["q"]},
    },
    {
        "id": "story_6",
        "text": "Lena has {a} stickers and buys {b} more packs with {c} stickers each. How many stickers now?",
        "generator": lambda rng: {
            "a": rng.randint(10, 40),
            "b": rng.randint(2, 6),
            "c": rng.randint(3, 10),
        },
        "answer": lambda values: values["a"] + values["b"] * values["c"],
    },
    {
        "id": "story_7",
        "text": "A farmer picks {a} eggs each day for {b} days. He sells {c} eggs. How many eggs remain?",
        "generator": lambda rng: {
            "a": rng.randint(8, 20),
            "b": rng.randint(2, 7),
            "c": rng.randint(10, 60),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "story_8",
        "text": "A toy shop has {a} shelves with {b} toys on each shelf. {c} toys are sold. How many toys are left?",
        "generator": lambda rng: {
            "a": rng.randint(3, 8),
            "b": rng.randint(6, 15),
            "c": rng.randint(5, 40),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "story_9",
        "text": "A coach has {a} players and splits them into {b} equal teams. How many players per team?",
        "generator": lambda rng: {
            "b": rng.randint(2, 6),
            "q": rng.randint(3, 10),
        },
        "answer": lambda values: values["a"] // values["b"],
        "post_process": lambda values: {**values, "a": values["b"] * values["q"]},
    },
    {
        "id": "story_10",
        "text": "Nina reads {a} chapters each week for {b} weeks, then rereads {c} chapters. How many chapters read in total?",
        "generator": lambda rng: {
            "a": rng.randint(1, 5),
            "b": rng.randint(3, 10),
            "c": rng.randint(1, 8),
        },
        "answer": lambda values: values["a"] * values["b"] + values["c"],
    },
]

BONUS_TEMPLATES = [
    {
        "id": "bonus_1",
        "text": "A baker makes {a} loaves per day. Each loaf has {b} slices. If {c} slices are eaten, how many slices remain?",
        "generator": lambda rng: {
            "a": rng.randint(4, 12),
            "b": rng.randint(4, 10),
            "c": rng.randint(5, 25),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "bonus_2",
        "text": "A school buys {a} packs of pencils with {b} pencils in each pack, then gives away {c} pencils. How many pencils are left?",
        "generator": lambda rng: {
            "a": rng.randint(3, 9),
            "b": rng.randint(6, 15),
            "c": rng.randint(10, 40),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "bonus_3",
        "text": "A bus carries {a} children on each trip and makes {b} trips. If {c} children have already gone home, how many are still at school?",
        "generator": lambda rng: {
            "a": rng.randint(8, 20),
            "b": rng.randint(2, 5),
            "c": rng.randint(10, 50),
        },
        "answer": lambda values: values["a"] * values["b"] - values["c"],
    },
    {
        "id": "bonus_4",
        "text": "There are {a} teams with {b} players each. They share into groups of {c}. How many groups are made?",
        "generator": lambda rng: {
            "a": rng.randint(3, 8),
            "b": rng.randint(4, 9),
            "c": rng.randint(2, 6),
        },
        "answer": lambda values: (values["a"] * values["b"]) // values["c"],
        "post_process": lambda values: {
            **values,
            "b": values["b"] * values["c"],
        },
    },
]
