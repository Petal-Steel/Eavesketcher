from __future__ import annotations

from pathlib import Path

from config import PlotterConfig
from motion import MotionCommand, PenState


def save_svg(commands: list[MotionCommand], config: PlotterConfig, path: Path) -> None:
    # SVG preview lets the team inspect the drawing before any machine moves.
    path.parent.mkdir(parents=True, exist_ok=True)

    polylines: list[list[tuple[float, float]]] = []
    current_line: list[tuple[float, float]] = []

    for command in commands:
        point = (command.x, command.y)
        if command.pen == PenState.DOWN:
            # Consecutive pen-down moves become one visible polyline.
            current_line.append(point)
        else:
            # A pen-up move breaks the visible line and starts a new path.
            if len(current_line) > 1:
                polylines.append(current_line)
            current_line = [point]

    if len(current_line) > 1:
        polylines.append(current_line)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{config.drawing_width_mm}mm" '
            f'height="{config.drawing_height_mm}mm" viewBox="0 0 {config.drawing_width_mm} {config.drawing_height_mm}">'
        ),
        '<rect x="0" y="0" width="100%" height="100%" fill="white"/>',
    ]

    for polyline in polylines:
        # Coordinates are already in millimeters, matching the machine footprint.
        points = " ".join(f"{x:.2f},{y:.2f}" for x, y in polyline)
        lines.append(f'<polyline points="{points}" fill="none" stroke="black" stroke-width="1.2"/>')

    lines.append("</svg>")
    path.write_text("\n".join(lines), encoding="utf-8")
