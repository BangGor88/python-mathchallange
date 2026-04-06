"""Celebration animations for Math Challenge score screen."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import tkinter as tk


@dataclass
class ConfettiPiece:
    item_id: int
    x: float
    y: float
    size: float
    vx: float
    vy: float
    angle: float
    angular_velocity: float
    color: tuple[int, int, int]


class CelebrationAnimator:
    """Runs score-dependent celebrations on a Tkinter canvas."""

    def __init__(self, canvas: tk.Canvas) -> None:
        self.canvas = canvas
        self.after_ids: list[str] = []

    def clear(self) -> None:
        for after_id in self.after_ids:
            try:
                self.canvas.after_cancel(after_id)
            except ValueError:
                pass
        self.after_ids.clear()
        self.canvas.delete("all")

    def run_for_score(self, score: int) -> None:
        self.clear()
        if score >= 90:
            self._start_confetti(piece_count=60, duration_ms=3000)
            self._show_pulsing_amazing(duration_ms=2000)
        elif score >= 60:
            self._start_confetti(piece_count=60, duration_ms=3000)
        elif score < 40:
            self._show_encouragement()

    def _show_encouragement(self) -> None:
        self.canvas.create_text(
            360,
            80,
            text="Keep practising! You'll get it 🤓",
            fill="#E67E22",
            font=("Comic Sans MS", 24, "bold"),
            anchor="center",
        )

    def _show_pulsing_amazing(self, duration_ms: int) -> None:
        text_id = self.canvas.create_text(
            360,
            40,
            text="🌟 AMAZING! 🌟",
            fill="#F39C12",
            font=("Comic Sans MS", 34, "bold"),
            anchor="center",
        )

        start_ms = 0
        interval = 40

        def tick(elapsed_ms: int) -> None:
            if elapsed_ms > duration_ms:
                return

            scale = 1.0 + 0.1 * math.sin(elapsed_ms / 120)
            font_size = max(18, int(34 * scale))
            self.canvas.itemconfigure(text_id, font=("Comic Sans MS", font_size, "bold"))
            aid = self.canvas.after(interval, lambda: tick(elapsed_ms + interval))
            self.after_ids.append(aid)

        tick(start_ms)

    def _start_confetti(self, piece_count: int, duration_ms: int) -> None:
        width = int(self.canvas.cget("width"))
        if width <= 1:
            width = max(700, self.canvas.winfo_width())

        pieces: list[ConfettiPiece] = []
        palette = [
            (231, 76, 60),
            (39, 174, 96),
            (52, 152, 219),
            (241, 196, 15),
            (155, 89, 182),
            (26, 188, 156),
        ]

        for _ in range(piece_count):
            x = random.uniform(10, width - 10)
            y = random.uniform(-180, -20)
            size = random.uniform(6, 14)
            color = random.choice(palette)
            item_id = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, 0, 0, fill=self._rgb_to_hex(color), outline="")
            pieces.append(
                ConfettiPiece(
                    item_id=item_id,
                    x=x,
                    y=y,
                    size=size,
                    vx=random.uniform(-1.2, 1.2),
                    vy=random.uniform(2.0, 4.5),
                    angle=random.uniform(0.0, math.pi * 2),
                    angular_velocity=random.uniform(-0.25, 0.25),
                    color=color,
                )
            )

        interval = 30

        def tick(elapsed_ms: int) -> None:
            progress = min(1.0, elapsed_ms / duration_ms)
            for piece in pieces:
                piece.x += piece.vx
                piece.y += piece.vy
                piece.angle += piece.angular_velocity

                faded = self._fade_to_white(piece.color, progress)
                self.canvas.itemconfigure(piece.item_id, fill=self._rgb_to_hex(faded))
                self.canvas.coords(piece.item_id, *self._rotated_square_points(piece.x, piece.y, piece.size, piece.angle))

            if elapsed_ms < duration_ms:
                aid = self.canvas.after(interval, lambda: tick(elapsed_ms + interval))
                self.after_ids.append(aid)

        tick(0)

    @staticmethod
    def _rotated_square_points(cx: float, cy: float, size: float, angle: float) -> list[float]:
        half = size / 2
        corners = [(-half, -half), (half, -half), (half, half), (-half, half)]
        points: list[float] = []

        for x, y in corners:
            rotated_x = x * math.cos(angle) - y * math.sin(angle)
            rotated_y = x * math.sin(angle) + y * math.cos(angle)
            points.append(cx + rotated_x)
            points.append(cy + rotated_y)

        return points

    @staticmethod
    def _fade_to_white(color: tuple[int, int, int], progress: float) -> tuple[int, int, int]:
        p = max(0.0, min(1.0, progress))
        return (
            int(color[0] + (255 - color[0]) * p),
            int(color[1] + (255 - color[1]) * p),
            int(color[2] + (255 - color[2]) * p),
        )

    @staticmethod
    def _rgb_to_hex(color: tuple[int, int, int]) -> str:
        return "#%02x%02x%02x" % color
