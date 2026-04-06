"""Main CustomTkinter application for Math Challenge."""

from __future__ import annotations

from datetime import date
from tkinter import messagebox
from typing import Any

import customtkinter as ctk
import tkinter as tk

from animations import CelebrationAnimator
from constants import (
    APP_TITLE,
    COLORS,
    default_daily_seed,
    FONTS,
    MINIMUM_PASS_SCORE,
    SCORE_LOG_DAYS,
    SECTION_HEADINGS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from questions import generate_questions
from scorer import calculate_score, calculate_section_breakdown, check_answers, get_star_rating
from tracker import get_recent_scores, get_today_score, has_completed_today, save_today


class MathChallengeApp(ctk.CTk):
    """Main desktop app window."""

    def __init__(self, skip_daily_check: bool = False) -> None:
        super().__init__()

        self.current_seed = default_daily_seed()
        self.questions: list[dict[str, Any]] = []
        self.answer_entries: dict[int, ctk.CTkEntry] = {}
        self.correct_answer_labels: dict[int, ctk.CTkLabel] = {}
        self.last_user_answers: dict[int, str] = {}
        self.last_results: dict[int, bool] = {}
        self.last_unanswered_ids: set[int] = set()
        self.last_wrong_ids: set[int] = set()
        self.score_frame: ctk.CTkFrame | None = None
        self.score_value_label: ctk.CTkLabel | None = None
        self.score_canvas: tk.Canvas | None = None
        self.animator: CelebrationAnimator | None = None

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title(APP_TITLE)
        self.configure(fg_color=COLORS["background"])
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(900, 720)
        self.state("zoomed")

        self._center_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._build_layout()

        self.skip_daily_check = skip_daily_check
        self.after(50, self._check_daily_completion)

    def _center_window(self, width: int, height: int) -> None:
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_pos = (screen_width - width) // 2
        y_pos = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x_pos}+{y_pos}")

    def _build_layout(self) -> None:
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self, corner_radius=16, fg_color=COLORS["panel"])
        self.header.grid(row=0, column=0, padx=16, pady=(16, 10), sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            self.header,
            text=APP_TITLE,
            font=FONTS["title"],
            text_color=COLORS["accent"],
        )
        title_label.grid(row=0, column=0, padx=12, pady=(10, 2), sticky="w")

        date_label = ctk.CTkLabel(
            self.header,
            text=f"Today: {date.today().strftime('%A, %d %B %Y')}",
            font=FONTS["label"],
            text_color=COLORS["text"],
        )
        date_label.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="w")

        self.scrollable = ctk.CTkScrollableFrame(self, fg_color=COLORS["panel"])
        self.scrollable.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        self.scrollable.grid_columnconfigure(0, weight=1)
        self.scrollable.grid_columnconfigure(1, weight=1)
        self.scrollable.grid_columnconfigure(2, weight=1)

        self._load_questions(self.current_seed)

        self.submit_button = ctk.CTkButton(
            self,
            text="Submit Answers",
            width=300,
            height=52,
            font=FONTS["button"],
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._submit_placeholder,
            text_color="#F4FBF6",
        )
        self.submit_button.grid(row=2, column=0, padx=16, pady=(10, 16))

    def _load_questions(self, seed: int) -> None:
        self.current_seed = seed
        self.questions = generate_questions(seed)
        self._render_questions()

    def _clear_scrollable(self) -> None:
        for widget in self.scrollable.winfo_children():
            widget.destroy()

    def _render_questions(self) -> None:
        self._clear_scrollable()
        self.answer_entries.clear()
        self.correct_answer_labels.clear()

        grouped: dict[str, list[dict[str, Any]]] = {
            "addition": [],
            "subtraction": [],
            "multiplication": [],
            "division": [],
            "story": [],
            "bonus": [],
        }
        for question in self.questions:
            grouped[question["section"]].append(question)

        row = 0
        section_order = ["addition", "subtraction", "multiplication", "division", "story", "bonus"]
        for section in section_order:
            heading = ctk.CTkLabel(
                self.scrollable,
                text=SECTION_HEADINGS[section],
                font=FONTS["header"],
                text_color=COLORS["accent"],
            )
            heading.grid(row=row, column=0, columnspan=3, sticky="w", pady=(16, 8), padx=10)
            row += 1

            section_questions = grouped[section]
            for index, question in enumerate(section_questions):
                col = index % 3
                if col == 0 and index > 0:
                    row += 1

                card = ctk.CTkFrame(self.scrollable, fg_color=COLORS["card"], corner_radius=14)
                card.grid(row=row, column=col, sticky="nsew", padx=8, pady=6)
                card.grid_columnconfigure(0, weight=1)

                question_text = ctk.CTkLabel(
                    card,
                    text=f"Q{question['id']}. {question['question_text']}",
                    font=FONTS["question"],
                    text_color=COLORS["text"],
                    anchor="w",
                    justify="left",
                    wraplength=285,
                )
                question_text.grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 6))

                entry = ctk.CTkEntry(
                    card,
                    width=180,
                    height=36,
                    font=FONTS["label"],
                    fg_color="#EDF8F0",
                    text_color="#1E3A2B",
                    border_color=COLORS["accent"],
                )
                entry.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 8))
                self.answer_entries[question["id"]] = entry

                correct_label = ctk.CTkLabel(
                    card,
                    text="",
                    font=FONTS["label"],
                    text_color=COLORS["muted"],
                    anchor="w",
                    justify="left",
                    wraplength=285,
                )
                correct_label.grid(row=2, column=0, sticky="w", padx=12, pady=(0, 10))
                self.correct_answer_labels[question["id"]] = correct_label

            row += 1

    def _check_daily_completion(self) -> None:
        if self.skip_daily_check:
            return

        if not has_completed_today():
            return

        score = get_today_score()
        shown_score = score if score is not None else 0
        open_anyway = messagebox.askyesno(
            "Quiz Completed",
            "You already finished today's quiz! "
            f"Your score was {shown_score}/100.\n\n"
            "Would you like to open the app anyway for extra practice?",
            parent=self,
        )
        if not open_anyway:
            self.destroy()

    def _submit_placeholder(self) -> None:
        user_answers: dict[int, str] = {}
        blank_count = 0

        for question_id, entry in self.answer_entries.items():
            value = entry.get()
            user_answers[question_id] = value
            if not value.strip():
                blank_count += 1

        if blank_count > 0:
            should_continue = messagebox.askyesno(
                "Unanswered Questions",
                f"You have {blank_count} unanswered questions. Submit anyway?",
                parent=self,
            )
            if not should_continue:
                return

        results = check_answers(self.questions, user_answers)
        score = calculate_score(results)
        self.last_user_answers = dict(user_answers)
        self.last_results = dict(results)
        self.last_unanswered_ids = {
            question_id for question_id, answer in user_answers.items() if not answer.strip()
        }
        self.last_wrong_ids = {
            question_id
            for question_id, is_correct in results.items()
            if (not is_correct) and (question_id not in self.last_unanswered_ids)
        }

        for question in self.questions:
            question_id = question["id"]
            is_correct = results.get(question_id, False)
            entry = self.answer_entries[question_id]
            label = self.correct_answer_labels[question_id]

            if is_correct:
                entry.configure(fg_color=COLORS["correct"], text_color="white", border_color=COLORS["correct"])
                label.configure(text="")
            else:
                entry.configure(fg_color=COLORS["wrong"], text_color="white", border_color=COLORS["wrong"])
                label.configure(text="")

        if score >= MINIMUM_PASS_SCORE:
            save_today(score)
        else:
            redo_now = messagebox.askyesno(
                "Minimum Score",
                f"You need at least {MINIMUM_PASS_SCORE} points to finish today. "
                "Would you like to redo now?",
                parent=self,
            )
            if redo_now:
                self._prepare_retry_entries()
                return

        self.after(350, lambda: self._show_score_screen(score, results))

    def _prepare_retry_entries(self) -> None:
        for question in self.questions:
            question_id = question["id"]
            entry = self.answer_entries[question_id]
            label = self.correct_answer_labels[question_id]

            previous_value = self.last_user_answers.get(question_id, "")
            was_correct = self.last_results.get(question_id, False)

            entry.delete(0, "end")
            if was_correct and previous_value.strip():
                entry.insert(0, previous_value)
            entry.configure(fg_color="#EDF8F0", text_color="#1E3A2B", border_color=COLORS["accent"])
            label.configure(text="")

    def _show_score_screen(self, score: int, results: dict[int, bool]) -> None:
        self.scrollable.grid_forget()
        self.submit_button.grid_forget()

        breakdown = calculate_section_breakdown(results)
        stars = get_star_rating(score)

        self.score_frame = ctk.CTkFrame(self, fg_color=COLORS["background"])
        self.score_frame.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        self.score_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.score_frame,
            text="Your Score",
            font=FONTS["header"],
            text_color=COLORS["accent"],
        )
        title.grid(row=0, column=0, pady=(20, 8))

        self.score_value_label = ctk.CTkLabel(
            self.score_frame,
            text="0/100",
            font=FONTS["score"],
            text_color=COLORS["accent"],
        )
        self.score_value_label.grid(row=1, column=0, pady=(4, 8))

        self._animate_score_counter(score)

        star_text = "★" * stars + "☆" * (5 - stars)
        stars_label = ctk.CTkLabel(
            self.score_frame,
            text=star_text,
            font=FONTS["star"],
            text_color=COLORS["bonus"],
        )
        stars_label.grid(row=2, column=0, pady=(2, 12))

        breakdown_label = ctk.CTkLabel(
            self.score_frame,
            text=f"Section A: {breakdown['A']}/60   Section B: {breakdown['B']}/20   Bonus: {breakdown['bonus']}/20",
            font=FONTS["label"],
            text_color=COLORS["text"],
        )
        breakdown_label.grid(row=3, column=0, pady=(2, 20))

        button_row = ctk.CTkFrame(self.score_frame, fg_color=COLORS["background"])
        button_row.grid(row=4, column=0, pady=(2, 10))

        try_again = ctk.CTkButton(
            button_row,
            text="🔄 Try Again (same questions)",
            font=FONTS["label"],
            fg_color=COLORS["accent"],
            command=lambda: self._reset_quiz(self.current_seed, preserve_previous=True),
            width=280,
            height=44,
        )
        try_again.grid(row=0, column=0, padx=8)

        new_questions = ctk.CTkButton(
            button_row,
            text="🆕 New Questions",
            font=FONTS["label"],
            fg_color=COLORS["bonus"],
            hover_color="#D98A0E",
            command=lambda: self._reset_quiz(self.current_seed + 1, preserve_previous=False),
            width=200,
            height=44,
        )
        new_questions.grid(row=0, column=1, padx=8)

        unanswered_questions = [q for q in self.questions if q["id"] in self.last_unanswered_ids]
        wrong_questions = [q for q in self.questions if q["id"] in self.last_wrong_ids]

        retry_title = ctk.CTkLabel(
            self.score_frame,
            text="Retry Focus (no answers shown)",
            font=FONTS["header"],
            text_color=COLORS["accent"],
        )
        retry_title.grid(row=5, column=0, pady=(0, 8))

        retry_lists = ctk.CTkFrame(self.score_frame, fg_color=COLORS["background"])
        retry_lists.grid(row=6, column=0, pady=(0, 12), sticky="ew")
        retry_lists.grid_columnconfigure(0, weight=1)
        retry_lists.grid_columnconfigure(1, weight=1)

        unanswered_box = ctk.CTkScrollableFrame(retry_lists, fg_color=COLORS["panel"], width=350, height=170)
        unanswered_box.grid(row=0, column=0, padx=(0, 8), sticky="nsew")
        unanswered_box.grid_columnconfigure(0, weight=1)

        wrong_box = ctk.CTkScrollableFrame(retry_lists, fg_color=COLORS["panel"], width=350, height=170)
        wrong_box.grid(row=0, column=1, padx=(8, 0), sticky="nsew")
        wrong_box.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            unanswered_box,
            text="No Answer",
            font=FONTS["header"],
            text_color=COLORS["accent"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(6, 4))

        ctk.CTkLabel(
            wrong_box,
            text="Wrong Answer",
            font=FONTS["header"],
            text_color=COLORS["accent"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(6, 4))

        if not unanswered_questions:
            ctk.CTkLabel(
                unanswered_box,
                text="None",
                font=FONTS["label"],
                text_color=COLORS["muted"],
                anchor="w",
            ).grid(row=1, column=0, sticky="w", padx=8, pady=4)
        else:
            for index, question in enumerate(unanswered_questions, start=1):
                ctk.CTkLabel(
                    unanswered_box,
                    text=f"Q{question['id']}: {question['question_text']}",
                    font=FONTS["label"],
                    text_color=COLORS["text"],
                    anchor="w",
                    justify="left",
                    wraplength=320,
                ).grid(row=index, column=0, sticky="w", padx=8, pady=4)

        if not wrong_questions:
            ctk.CTkLabel(
                wrong_box,
                text="None",
                font=FONTS["label"],
                text_color=COLORS["muted"],
                anchor="w",
            ).grid(row=1, column=0, sticky="w", padx=8, pady=4)
        else:
            for index, question in enumerate(wrong_questions, start=1):
                ctk.CTkLabel(
                    wrong_box,
                    text=f"Q{question['id']}: {question['question_text']}",
                    font=FONTS["label"],
                    text_color=COLORS["text"],
                    anchor="w",
                    justify="left",
                    wraplength=320,
                ).grid(row=index, column=0, sticky="w", padx=8, pady=4)

        if not unanswered_questions and not wrong_questions:
            ctk.CTkLabel(
                self.score_frame,
                text="Amazing! You got every question right.",
                font=FONTS["label"],
                text_color=COLORS["text"],
            ).grid(row=7, column=0, pady=(0, 8))

        chart_title = ctk.CTkLabel(
            self.score_frame,
            text=f"Daily Score Log (Last {SCORE_LOG_DAYS} Days)",
            font=FONTS["header"],
            text_color=COLORS["accent"],
        )
        chart_title.grid(row=8, column=0, pady=(0, 8))

        history_canvas = tk.Canvas(
            self.score_frame,
            width=720,
            height=210,
            bg=COLORS["panel"],
            highlightthickness=0,
        )
        history_canvas.grid(row=9, column=0, pady=(0, 12))
        self._draw_score_log_chart(history_canvas, get_recent_scores(limit=SCORE_LOG_DAYS))

        self.score_canvas = tk.Canvas(
            self.score_frame,
            width=720,
            height=180,
            bg=COLORS["background"],
            highlightthickness=0,
        )
        self.score_canvas.grid(row=10, column=0, pady=(0, 12))
        self.animator = CelebrationAnimator(self.score_canvas)
        self.animator.run_for_score(score)

    def _draw_score_log_chart(self, canvas: tk.Canvas, data_points: list[tuple[str, int]]) -> None:
        canvas.delete("all")

        if not data_points:
            canvas.create_text(
                360,
                105,
                text="No completed scores yet.",
                fill=COLORS["muted"],
                font=FONTS["header"],
            )
            return

        left = 45
        top = 18
        right = 700
        bottom = 170
        width = right - left
        height = bottom - top

        canvas.create_line(left, top, left, bottom, fill=COLORS["muted"], width=2)
        canvas.create_line(left, bottom, right, bottom, fill=COLORS["muted"], width=2)

        for tick, label in [(0, "0"), (50, "50"), (100, "100")]:
            y = bottom - (height * tick / 100)
            canvas.create_line(left - 6, y, left, y, fill=COLORS["muted"], width=2)
            canvas.create_text(left - 12, y, text=label, fill=COLORS["muted"], font=FONTS["label"], anchor="e")

        slot_width = width / max(1, len(data_points))
        bar_width = max(14, min(40, int(slot_width * 0.55)))

        for index, (day_key, score) in enumerate(data_points):
            score = max(0, min(100, int(score)))
            center_x = left + (index + 0.5) * slot_width
            x0 = center_x - (bar_width / 2)
            x1 = center_x + (bar_width / 2)
            y0 = bottom - (height * score / 100)

            canvas.create_rectangle(x0, y0, x1, bottom, fill=COLORS["accent"], outline="")
            canvas.create_text(center_x, y0 - 8, text=str(score), fill=COLORS["text"], font=FONTS["label"])
            canvas.create_text(center_x, bottom + 16, text=day_key[5:], fill=COLORS["muted"], font=FONTS["label"])

    def _animate_score_counter(self, target_score: int) -> None:
        if self.score_value_label is None:
            return

        duration_ms = 1500
        interval_ms = 30
        steps = max(1, duration_ms // interval_ms)

        def tick(step: int) -> None:
            if self.score_value_label is None:
                return

            current = int(round((target_score * step) / steps))
            self.score_value_label.configure(text=f"{current}/100")
            if step < steps:
                self.after(interval_ms, lambda: tick(step + 1))
            else:
                self.score_value_label.configure(text=f"{target_score}/100")

        tick(0)

    def _reset_quiz(self, seed: int, preserve_previous: bool = False) -> None:
        if self.animator is not None:
            self.animator.clear()

        if self.score_frame is not None:
            self.score_frame.destroy()
            self.score_frame = None
            self.score_value_label = None
            self.score_canvas = None
            self.animator = None

        self.scrollable.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        self.submit_button.grid(row=2, column=0, padx=16, pady=(10, 16))
        self._load_questions(seed)
        if preserve_previous and seed == self.current_seed:
            self._prepare_retry_entries()

    def autofill_for_qa(self, mode: str = "correct", submit: bool = False) -> None:
        """Fill answers for QA scenarios and optionally submit automatically."""
        for question in self.questions:
            qid = question["id"]
            entry = self.answer_entries[qid]
            entry.delete(0, "end")

            if mode == "correct":
                entry.insert(0, str(question["correct_answer"]))
            elif mode == "wrong":
                entry.insert(0, str(int(question["correct_answer"]) + 1))
            elif mode == "mixed":
                if qid % 3 == 0:
                    entry.insert(0, "")
                elif qid % 2 == 0:
                    entry.insert(0, str(int(question["correct_answer"]) + 1))
                else:
                    entry.insert(0, str(question["correct_answer"]))

        if submit:
            self._submit_placeholder()
