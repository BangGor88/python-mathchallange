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
    BONUS_TEMPLATE_TRANSLATIONS,
    COLORS,
    default_daily_seed,
    FONTS,
    LANGUAGE_OPTIONS,
    MINIMUM_PASS_SCORE,
    SCORE_LOG_DAYS,
    STORY_TEMPLATE_TRANSLATIONS,
    TOPIC_HINT_TRANSLATIONS,
    TOPIC_QUESTION_TRANSLATIONS,
    UI_TEXT,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from questions import generate_questions, generate_topic_questions
from scorer import (
    calculate_practice_score,
    calculate_score,
    calculate_section_breakdown,
    check_answers,
    get_star_rating,
)
from tracker import (
    get_dark_mode,
    get_last_topic,
    get_recent_scores,
    get_today_score,
    has_completed_today,
    save_last_topic,
    save_dark_mode,
    save_today,
    save_topic_score,
)


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
        self.current_topic: str | None = None
        self.current_language = "en"
        self.language_display_to_code = dict(LANGUAGE_OPTIONS)
        self.language_code_to_display = {code: display for display, code in LANGUAGE_OPTIONS.items()}
        self.score_frame: ctk.CTkFrame | None = None
        self.score_value_label: ctk.CTkLabel | None = None
        self.score_canvas: tk.Canvas | None = None
        self.animator: CelebrationAnimator | None = None
        self.skip_daily_check = skip_daily_check
        self.dark_mode = get_dark_mode()
        self.history_canvas: tk.Canvas | None = None

        ctk.set_appearance_mode("dark" if self.dark_mode else "light")
        ctk.set_default_color_theme("blue")

        self.title(APP_TITLE)
        self.configure(fg_color=COLORS["background"])
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(900, 720)

        self._center_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self._build_layout()
        last_topic = get_last_topic()
        if last_topic in ("fractions", "decimals", "multiplication", "mixed"):
            self.after(50, lambda topic=last_topic: self._select_topic(topic))

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
        self.header.grid_columnconfigure(1, weight=0)
        self.header.grid_columnconfigure(2, weight=0)
        self.header.grid_columnconfigure(3, weight=0)

        self.title_label = ctk.CTkLabel(
            self.header,
            text=APP_TITLE,
            font=FONTS["title"],
            text_color=COLORS["accent"],
        )
        self.title_label.grid(row=0, column=0, padx=12, pady=(10, 2), sticky="w")

        self.date_label = ctk.CTkLabel(
            self.header,
            text=self._today_label_text(),
            font=FONTS["label"],
            text_color=COLORS["text"],
        )
        self.date_label.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="w")

        self.language_label = ctk.CTkLabel(
            self.header,
            text=self._t("language"),
            font=FONTS["label"],
            text_color=COLORS["text"],
        )
        self.language_label.grid(row=0, column=1, padx=(12, 12), pady=(10, 2), sticky="e")

        self.language_var = ctk.StringVar(value=self.language_code_to_display[self.current_language])
        self.language_menu = ctk.CTkOptionMenu(
            self.header,
            values=list(LANGUAGE_OPTIONS.keys()),
            variable=self.language_var,
            command=self._on_language_change,
            font=FONTS["label"],
            fg_color=COLORS["accent"],
            button_color=COLORS["accent_hover"],
            button_hover_color=COLORS["accent_hover"],
            text_color=COLORS["button_text"],
            width=180,
        )
        self.language_menu.grid(row=1, column=1, padx=(12, 12), pady=(0, 10), sticky="e")

        self.dark_mode_button = ctk.CTkButton(
            self.header,
            text=self._t("light_mode" if self.dark_mode else "dark_mode"),
            width=135,
            font=FONTS["label"],
            fg_color=COLORS["secondary"],
            hover_color=COLORS["accent_hover"],
            command=self._toggle_dark_mode,
        )
        self.dark_mode_button.grid(row=0, column=3, rowspan=2, padx=(8, 12), pady=10, sticky="e")

        self.change_topic_button = ctk.CTkButton(
            self.header,
            text=self._t("change_topic"),
            width=150,
            font=FONTS["label"],
            fg_color=COLORS["secondary"],
            hover_color=COLORS["accent_hover"],
            command=self._change_topic,
        )
        self.change_topic_button.grid(row=0, column=2, rowspan=2, padx=(8, 12), pady=10, sticky="e")
        self.change_topic_button.grid_remove()

        self.scrollable = ctk.CTkScrollableFrame(self, fg_color=COLORS["panel"])
        self.scrollable.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        self.scrollable.grid_columnconfigure(0, weight=1)
        self.scrollable.grid_columnconfigure(1, weight=1)
        self.scrollable.grid_columnconfigure(2, weight=1)

        self.submit_button = ctk.CTkButton(
            self,
            text=self._t("submit_answers"),
            width=300,
            height=52,
            font=FONTS["button"],
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            command=self._submit_placeholder,
            text_color=COLORS["button_text"],
        )
        self.submit_button.grid(row=2, column=0, padx=16, pady=(10, 16))
        self.submit_button.grid_remove()
        self._render_topic_picker()

    def _load_questions(self, seed: int) -> None:
        self.current_seed = seed
        if self.current_topic == "mixed":
            self.questions = generate_questions(seed)
        elif self.current_topic is not None:
            self.questions = generate_topic_questions(self.current_topic, seed)
        else:
            raise ValueError("Select a practice topic before loading questions.")
        self._render_questions()

    def _render_topic_picker(self) -> None:
        self._clear_scrollable()
        self.answer_entries.clear()
        self.correct_answer_labels.clear()

        title = ctk.CTkLabel(
            self.scrollable,
            text=self._t("welcome_title"),
            font=FONTS["title"],
            text_color=COLORS["accent"],
        )
        title.grid(row=0, column=0, columnspan=2, pady=(70, 10))

        prompt = ctk.CTkLabel(
            self.scrollable,
            text=self._t("choose_topic"),
            font=FONTS["header"],
            text_color=COLORS["text"],
        )
        prompt.grid(row=1, column=0, columnspan=2, pady=(0, 24))

        for index, topic in enumerate(("fractions", "decimals", "multiplication", "mixed")):
            button = ctk.CTkButton(
                self.scrollable,
                text=self._t(f"topic_{topic}"),
                width=420,
                height=64,
                font=FONTS["button"],
                fg_color=COLORS["accent"] if topic != "mixed" else COLORS["bonus"],
                hover_color=COLORS["accent_hover"] if topic != "mixed" else COLORS["bonus_hover"],
                text_color=COLORS["button_text"],
                command=lambda selected_topic=topic: self._select_topic(selected_topic),
            )
            button.grid(row=index + 2, column=0, columnspan=2, pady=8)

        self.submit_button.grid_remove()
        self.change_topic_button.grid_remove()

    def _select_topic(self, topic: str) -> None:
        if topic == "mixed" and not self._check_daily_completion():
            self.destroy()
            return

        save_last_topic(topic)
        self.current_topic = topic
        self.change_topic_button.configure(text=self._t("change_topic"))
        self.change_topic_button.grid(row=0, column=2, rowspan=2, padx=(8, 12), pady=10, sticky="e")
        self.submit_button.configure(text=self._t("submit_answers"))
        self.submit_button.grid(row=2, column=0, padx=16, pady=(10, 16))
        self._load_questions(default_daily_seed())

    def _toggle_dark_mode(self) -> None:
        self.dark_mode = not self.dark_mode
        ctk.set_appearance_mode("dark" if self.dark_mode else "light")
        save_dark_mode(self.dark_mode)
        self.dark_mode_button.configure(
            text=self._t("light_mode" if self.dark_mode else "dark_mode")
        )
        self.configure(fg_color=self._theme_color("background"))
        if self.history_canvas is not None and self.history_canvas.winfo_exists():
            self.history_canvas.configure(bg=self._theme_color("panel"))
            history_topic = None if self.current_topic == "mixed" else self.current_topic
            self._draw_score_log_chart(
                self.history_canvas,
                get_recent_scores(limit=SCORE_LOG_DAYS, topic=history_topic),
            )
        if self.score_canvas is not None and self.score_canvas.winfo_exists():
            self.score_canvas.configure(bg=self._theme_color("background"))

    def _theme_color(self, color_name: str) -> str:
        return COLORS[color_name][1 if self.dark_mode else 0]

    def _change_topic(self) -> None:
        if self.current_topic is None:
            return
        if self.score_frame is None:
            should_change = self._ask_confirmation(
                title=self._t("switch_topic_title"),
                message=self._t("switch_topic_message"),
                confirm_text=self._t("popup_submit_anyway"),
                cancel_text=self._t("popup_go_back"),
            )
            if not should_change:
                return

        if self.animator is not None:
            self.animator.clear()
        if self.score_frame is not None:
            self.score_frame.destroy()
            self.score_frame = None
            self.score_value_label = None
            self.score_canvas = None
            self.animator = None

        self.current_topic = None
        self.questions = []
        self.language_label.grid()
        self.language_menu.grid()
        self.scrollable.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        self._render_topic_picker()

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
            "practice": [],
        }
        for question in self.questions:
            section = question["section"]
            grouped.setdefault(section, []).append(question)

        row = 0
        section_order = [
            "addition",
            "subtraction",
            "multiplication",
            "division",
            "story",
            "bonus",
            "practice",
        ]
        section_order.extend(section for section in grouped if section not in section_order)
        for section in section_order:
            section_questions = grouped[section]
            if not section_questions:
                continue
            heading = ctk.CTkLabel(
                self.scrollable,
                text=self._section_heading(section),
                font=FONTS["header"],
                text_color=COLORS["accent"],
            )
            heading.grid(row=row, column=0, columnspan=3, sticky="w", pady=(16, 8), padx=10)
            row += 1

            for index, question in enumerate(section_questions):
                col = index % 3
                if col == 0 and index > 0:
                    row += 1

                card = ctk.CTkFrame(self.scrollable, fg_color=COLORS["card"], corner_radius=14)
                card.grid(row=row, column=col, sticky="nsew", padx=8, pady=6)
                card.grid_columnconfigure(0, weight=1)

                question_text = ctk.CTkLabel(
                    card,
                    text=f"Q{question['id']}. {self._display_question_text(question)}",
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
                    fg_color=COLORS["input"],
                    text_color=COLORS["input_text"],
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

    def _check_daily_completion(self) -> bool:
        if self.skip_daily_check:
            return True

        if not has_completed_today():
            return True

        score = get_today_score()
        shown_score = score if score is not None else 0
        return self._ask_confirmation(
            title=self._t("quiz_completed_title"),
            message=self._t("quiz_completed_message", score=shown_score),
            confirm_text=self._t("popup_open_anyway"),
            cancel_text=self._t("popup_exit"),
        )

    def _submit_placeholder(self) -> None:
        user_answers: dict[int, str] = {}
        blank_count = 0

        for question_id, entry in self.answer_entries.items():
            value = entry.get()
            user_answers[question_id] = value
            if not value.strip():
                blank_count += 1

        if blank_count > 0:
            should_continue = self._ask_confirmation(
                title=self._t("unanswered_title"),
                message=self._t("unanswered_message", count=blank_count),
                confirm_text=self._t("popup_submit_anyway"),
                cancel_text=self._t("popup_go_back"),
            )
            if not should_continue:
                return

        results = check_answers(self.questions, user_answers)
        if self.current_topic == "mixed":
            score = calculate_score(results)
        else:
            score = calculate_practice_score(results)
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

        if self.current_topic == "mixed" and score >= MINIMUM_PASS_SCORE:
            save_today(score)
        elif self.current_topic == "mixed":
            redo_now = self._ask_confirmation(
                title=self._t("minimum_score_title"),
                message=self._t("minimum_score_message", minimum=MINIMUM_PASS_SCORE),
                confirm_text=self._t("popup_redo_now"),
                cancel_text=self._t("popup_later"),
            )
            if redo_now:
                self._prepare_retry_entries()
                return
        elif self.current_topic is not None:
            save_topic_score(score, self.current_topic)

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
            entry.configure(
                fg_color=COLORS["input"],
                text_color=COLORS["input_text"],
                border_color=COLORS["accent"],
            )
            label.configure(text="")

    def _show_score_screen(self, score: int, results: dict[int, bool]) -> None:
        self.language_label.grid_remove()
        self.language_menu.grid_remove()
        self.scrollable.grid_forget()
        self.submit_button.grid_forget()

        if self.current_topic == "mixed":
            breakdown = calculate_section_breakdown(results)
            breakdown_text = self._t(
                "section_breakdown",
                a=breakdown["A"],
                b=breakdown["B"],
                bonus=breakdown["bonus"],
            )
        else:
            breakdown_text = self._t(
                "practice_breakdown",
                correct=sum(results.values()),
                total=len(results),
            )
        stars = get_star_rating(score)

        self.score_frame = ctk.CTkFrame(self, fg_color=COLORS["background"])
        self.score_frame.grid(row=1, column=0, padx=16, pady=8, sticky="nsew")
        self.score_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self.score_frame,
            text=self._t("your_score"),
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
            text=breakdown_text,
            font=FONTS["label"],
            text_color=COLORS["text"],
        )
        breakdown_label.grid(row=3, column=0, pady=(2, 20))

        button_row = ctk.CTkFrame(self.score_frame, fg_color=COLORS["background"])
        button_row.grid(row=4, column=0, pady=(2, 10))

        try_again = ctk.CTkButton(
            button_row,
            text=self._t("retry_button"),
            font=FONTS["label"],
            fg_color=COLORS["accent"],
            command=lambda: self._reset_quiz(self.current_seed, preserve_previous=True),
            width=280,
            height=44,
        )
        try_again.grid(row=0, column=0, padx=8)

        new_questions = ctk.CTkButton(
            button_row,
            text=self._t("new_questions_button"),
            font=FONTS["label"],
            fg_color=COLORS["bonus"],
            hover_color=COLORS["bonus_hover"],
            command=lambda: self._reset_quiz(self.current_seed + 1, preserve_previous=False),
            width=200,
            height=44,
        )
        new_questions.grid(row=0, column=1, padx=8)

        unanswered_questions = [q for q in self.questions if q["id"] in self.last_unanswered_ids]
        wrong_questions = [q for q in self.questions if q["id"] in self.last_wrong_ids]

        retry_title = ctk.CTkLabel(
            self.score_frame,
            text=self._t("retry_focus"),
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
            text=self._t("no_answer"),
            font=FONTS["header"],
            text_color=COLORS["accent"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(6, 4))

        ctk.CTkLabel(
            wrong_box,
            text=self._t("wrong_answer"),
            font=FONTS["header"],
            text_color=COLORS["accent"],
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=8, pady=(6, 4))

        if not unanswered_questions:
            ctk.CTkLabel(
                unanswered_box,
                text=self._t("none"),
                font=FONTS["label"],
                text_color=COLORS["muted"],
                anchor="w",
            ).grid(row=1, column=0, sticky="w", padx=8, pady=4)
        else:
            for index, question in enumerate(unanswered_questions, start=1):
                ctk.CTkLabel(
                    unanswered_box,
                    text=f"Q{question['id']}: {self._display_question_text(question)}",
                    font=FONTS["label"],
                    text_color=COLORS["text"],
                    anchor="w",
                    justify="left",
                    wraplength=320,
                ).grid(row=index, column=0, sticky="w", padx=8, pady=4)

        if not wrong_questions:
            ctk.CTkLabel(
                wrong_box,
                text=self._t("none"),
                font=FONTS["label"],
                text_color=COLORS["muted"],
                anchor="w",
            ).grid(row=1, column=0, sticky="w", padx=8, pady=4)
        else:
            for index, question in enumerate(wrong_questions, start=1):
                feedback = ""
                if question.get("hint"):
                    feedback = "\n" + self._t(
                        "practice_answer_hint",
                        answer=question["correct_answer"],
                        hint=self._display_question_hint(question),
                    )
                ctk.CTkLabel(
                    wrong_box,
                    text=f"Q{question['id']}: {self._display_question_text(question)}{feedback}",
                    font=FONTS["label"],
                    text_color=COLORS["text"],
                    anchor="w",
                    justify="left",
                    wraplength=320,
                ).grid(row=index, column=0, sticky="w", padx=8, pady=4)

        if not unanswered_questions and not wrong_questions:
            ctk.CTkLabel(
                self.score_frame,
                text=self._t("perfect_message"),
                font=FONTS["label"],
                text_color=COLORS["text"],
            ).grid(row=7, column=0, pady=(0, 8))

        chart_title = ctk.CTkLabel(
            self.score_frame,
            text=(
                self._t("score_log", days=SCORE_LOG_DAYS)
                if self.current_topic == "mixed"
                else self._t(
                    "practice_score_log",
                    topic=self._t(f"topic_{self.current_topic}"),
                    days=SCORE_LOG_DAYS,
                )
            ),
            font=FONTS["header"],
            text_color=COLORS["accent"],
        )
        chart_title.grid(row=8, column=0, pady=(0, 8))

        history_canvas = tk.Canvas(
            self.score_frame,
            width=720,
            height=210,
            bg=self._theme_color("panel"),
            highlightthickness=0,
        )
        history_canvas.grid(row=9, column=0, pady=(0, 12))
        self.history_canvas = history_canvas
        history_topic = None if self.current_topic == "mixed" else self.current_topic
        self._draw_score_log_chart(
            history_canvas,
            get_recent_scores(limit=SCORE_LOG_DAYS, topic=history_topic),
        )

        self.score_canvas = tk.Canvas(
            self.score_frame,
            width=720,
            height=180,
            bg=self._theme_color("background"),
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
                text=self._t("no_scores"),
                fill=self._theme_color("muted"),
                font=FONTS["header"],
            )
            return

        left = 45
        top = 18
        right = 700
        bottom = 170
        width = right - left
        height = bottom - top

        canvas.create_line(left, top, left, bottom, fill=self._theme_color("muted"), width=2)
        canvas.create_line(left, bottom, right, bottom, fill=self._theme_color("muted"), width=2)

        for tick, label in [(0, "0"), (50, "50"), (100, "100")]:
            y = bottom - (height * tick / 100)
            canvas.create_line(left - 6, y, left, y, fill=self._theme_color("muted"), width=2)
            canvas.create_text(
                left - 12,
                y,
                text=label,
                fill=self._theme_color("muted"),
                font=FONTS["label"],
                anchor="e",
            )

        slot_width = width / max(1, len(data_points))
        bar_width = max(14, min(40, int(slot_width * 0.55)))

        for index, (day_key, score) in enumerate(data_points):
            score = max(0, min(100, int(score)))
            center_x = left + (index + 0.5) * slot_width
            x0 = center_x - (bar_width / 2)
            x1 = center_x + (bar_width / 2)
            y0 = bottom - (height * score / 100)

            canvas.create_rectangle(x0, y0, x1, bottom, fill=self._theme_color("accent"), outline="")
            canvas.create_text(
                center_x,
                y0 - 8,
                text=str(score),
                fill=self._theme_color("text"),
                font=FONTS["label"],
            )
            canvas.create_text(
                center_x,
                bottom + 16,
                text=day_key[5:],
                fill=self._theme_color("muted"),
                font=FONTS["label"],
            )

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

        self.language_label.grid(row=0, column=1, padx=(12, 12), pady=(10, 2), sticky="e")
        self.language_menu.grid(row=1, column=1, padx=(12, 12), pady=(0, 10), sticky="e")
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
                entry.insert(0, "999")
            elif mode == "mixed":
                if qid % 3 == 0:
                    entry.insert(0, "")
                elif qid % 2 == 0:
                    entry.insert(0, "999")
                else:
                    entry.insert(0, str(question["correct_answer"]))

        if submit:
            self._submit_placeholder()

    def _section_heading(self, section_key: str) -> str:
        return self._t(f"section_{section_key}")

    def _display_question_text(self, question: dict[str, Any]) -> str:
        section = question.get("section")
        if section == "practice":
            template_id = question.get("template_id")
            template_values = question.get("template_values")
            if isinstance(template_id, str) and isinstance(template_values, dict):
                localized_template = TOPIC_QUESTION_TRANSLATIONS.get(
                    self.current_language, TOPIC_QUESTION_TRANSLATIONS["en"]
                ).get(template_id)
                if localized_template:
                    return localized_template.format(**template_values)
            return str(question.get("question_text", ""))

        if section not in ("story", "bonus"):
            return str(question.get("question_text", ""))

        if self.current_language == "en":
            return str(question.get("question_text", ""))

        template_id = question.get("template_id")
        template_values = question.get("template_values")
        if not isinstance(template_id, str) or not isinstance(template_values, dict):
            return str(question.get("question_text", ""))

        translation_map = (
            STORY_TEMPLATE_TRANSLATIONS if section == "story" else BONUS_TEMPLATE_TRANSLATIONS
        )
        localized_template = translation_map.get(self.current_language, {}).get(template_id)
        if not localized_template:
            return str(question.get("question_text", ""))

        try:
            return localized_template.format(**template_values)
        except KeyError:
            return str(question.get("question_text", ""))

    def _display_question_hint(self, question: dict[str, Any]) -> str:
        hint_id = question.get("hint_id")
        template_values = question.get("template_values")
        if isinstance(hint_id, str) and isinstance(template_values, dict):
            localized_hint = TOPIC_HINT_TRANSLATIONS.get(
                self.current_language, TOPIC_HINT_TRANSLATIONS["en"]
            ).get(hint_id)
            if localized_hint:
                return localized_hint.format(**template_values)
        return str(question.get("hint", ""))

    def _today_label_text(self) -> str:
        return f"{self._t('today_prefix')} {date.today().strftime('%A, %d %B %Y')}"

    def _t(self, key: str, **kwargs: Any) -> str:
        table = UI_TEXT.get(self.current_language, UI_TEXT["en"])
        fallback = UI_TEXT["en"]
        template = table.get(key, fallback.get(key, key))
        return template.format(**kwargs)

    def _on_language_change(self, selected_display: str) -> None:
        selected_code = self.language_display_to_code.get(selected_display, "en")
        if selected_code == self.current_language:
            return

        self.current_language = selected_code
        self.language_label.configure(text=self._t("language"))
        self.date_label.configure(text=self._today_label_text())
        self.submit_button.configure(text=self._t("submit_answers"))
        self.dark_mode_button.configure(
            text=self._t("light_mode" if self.dark_mode else "dark_mode")
        )

        if self.score_frame is None:
            self.change_topic_button.configure(text=self._t("change_topic"))
            if self.current_topic is None:
                self._render_topic_picker()
            else:
                existing_answers = {qid: entry.get() for qid, entry in self.answer_entries.items()}
                self._render_questions()
                for qid, value in existing_answers.items():
                    if qid in self.answer_entries:
                        self.answer_entries[qid].insert(0, value)

    def _ask_confirmation(self, title: str, message: str, confirm_text: str, cancel_text: str) -> bool:
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=COLORS["background"])
        dialog.resizable(False, False)

        dialog_width = 460
        dialog_height = 220
        self.update_idletasks()
        x_pos = self.winfo_rootx() + (self.winfo_width() // 2) - (dialog_width // 2)
        y_pos = self.winfo_rooty() + (self.winfo_height() // 2) - (dialog_height // 2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{x_pos}+{y_pos}")

        frame = ctk.CTkFrame(dialog, fg_color=COLORS["panel"], corner_radius=12)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        title_label = ctk.CTkLabel(frame, text=title, font=FONTS["header"], text_color=COLORS["accent"])
        title_label.pack(anchor="w", padx=12, pady=(10, 6))

        message_label = ctk.CTkLabel(
            frame,
            text=message,
            font=FONTS["label"],
            text_color=COLORS["text"],
            justify="left",
            anchor="w",
            wraplength=420,
        )
        message_label.pack(anchor="w", padx=12, pady=(0, 12))

        result = {"value": False}

        def on_confirm() -> None:
            result["value"] = True
            dialog.destroy()

        def on_cancel() -> None:
            result["value"] = False
            dialog.destroy()

        button_row = ctk.CTkFrame(frame, fg_color=COLORS["panel"])
        button_row.pack(anchor="e", padx=12, pady=(0, 12))

        cancel_button = ctk.CTkButton(
            button_row,
            text=cancel_text,
            font=FONTS["label"],
            fg_color=COLORS["muted"],
            hover_color=COLORS["secondary"],
            command=on_cancel,
            width=130,
        )
        cancel_button.grid(row=0, column=0, padx=(0, 8))

        confirm_button = ctk.CTkButton(
            button_row,
            text=confirm_text,
            font=FONTS["label"],
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            text_color=COLORS["button_text"],
            command=on_confirm,
            width=150,
        )
        confirm_button.grid(row=0, column=1)

        dialog.protocol("WM_DELETE_WINDOW", on_cancel)
        self.wait_window(dialog)
        return bool(result["value"])
