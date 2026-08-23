from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PenState(str, Enum):
    # Pen state travels with each move so G-code generation can decide whether
    # to emit a rapid travel move or an actual drawing move.
    UP = "up"
    DOWN = "down"


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class MotionCommand:
    # One high-level motion command in machine coordinates.
    # This is intentionally not raw G-code so we can validate and preview before export.
    x: float
    y: float
    pen: PenState
    feed_rate_mm_min: float


class Drawing:
    def __init__(self) -> None:
        # Ordered list of moves. The first command is usually a pen-up travel.
        self.commands: list[MotionCommand] = []

    def move_to(self, x: float, y: float, feed_rate_mm_min: float) -> None:
        # Move without drawing. This should become G0 with the pen lifted.
        self.commands.append(MotionCommand(x=x, y=y, pen=PenState.UP, feed_rate_mm_min=feed_rate_mm_min))

    def line_to(self, x: float, y: float, feed_rate_mm_min: float) -> None:
        # Move while drawing. This should become G1 with the pen lowered.
        self.commands.append(MotionCommand(x=x, y=y, pen=PenState.DOWN, feed_rate_mm_min=feed_rate_mm_min))
