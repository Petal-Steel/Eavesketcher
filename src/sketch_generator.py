from __future__ import annotations

from math import cos, pi, sin

from config import PlotterConfig
from motion import Drawing


def generate_sketch(prompt: str, config: PlotterConfig) -> Drawing:
    # Temporary rule-based sketch selector.
    # Later this will likely consume a structured plan from the local LLM.
    prompt_lower = prompt.lower()

    if "house" in prompt_lower:
        return house(config)
    if "star" in prompt_lower:
        return star(config)
    if "spiral" in prompt_lower:
        return spiral(config)

    return simple_box(config)


def simple_box(config: PlotterConfig) -> Drawing:
    drawing = Drawing()

    # 76.2 mm is 3 inches. Keeping a margin gives the machine room for clamps,
    # paper curl, pen holder width, and early calibration error.
    margin = 76.2
    left = margin
    right = config.drawing_width_mm - margin
    top = margin
    bottom = config.drawing_height_mm - margin

    drawing.move_to(left, top, config.travel_rate_mm_min)
    drawing.line_to(right, top, config.feed_rate_mm_min)
    drawing.line_to(right, bottom, config.feed_rate_mm_min)
    drawing.line_to(left, bottom, config.feed_rate_mm_min)
    drawing.line_to(left, top, config.feed_rate_mm_min)
    return drawing


def house(config: PlotterConfig) -> Drawing:
    drawing = Drawing()

    # Scale the house to the current drawing footprint so it stays centered
    # even if the plotter size changes later.
    cx = config.drawing_width_mm / 2.0
    base_y = config.drawing_height_mm * 0.68
    roof_y = config.drawing_height_mm * 0.30
    half_w = 152.4
    wall_h = 177.8

    drawing.move_to(cx - half_w, base_y, config.travel_rate_mm_min)
    drawing.line_to(cx + half_w, base_y, config.feed_rate_mm_min)
    drawing.line_to(cx + half_w, base_y - wall_h, config.feed_rate_mm_min)
    drawing.line_to(cx, roof_y, config.feed_rate_mm_min)
    drawing.line_to(cx - half_w, base_y - wall_h, config.feed_rate_mm_min)
    drawing.line_to(cx - half_w, base_y, config.feed_rate_mm_min)

    door_w = 63.5
    door_h = 101.6
    drawing.move_to(cx - door_w / 2.0, base_y, config.travel_rate_mm_min)
    drawing.line_to(cx - door_w / 2.0, base_y - door_h, config.feed_rate_mm_min)
    drawing.line_to(cx + door_w / 2.0, base_y - door_h, config.feed_rate_mm_min)
    drawing.line_to(cx + door_w / 2.0, base_y, config.feed_rate_mm_min)
    return drawing


def star(config: PlotterConfig) -> Drawing:
    drawing = Drawing()
    cx = config.drawing_width_mm / 2.0
    cy = config.drawing_height_mm / 2.0
    outer = 177.8
    inner = 71.12
    points = []

    # Build a 10-point alternating-radius star: outer, inner, outer, inner...
    for index in range(10):
        radius = outer if index % 2 == 0 else inner
        angle = -pi / 2.0 + index * pi / 5.0
        points.append((cx + cos(angle) * radius, cy + sin(angle) * radius))

    drawing.move_to(points[0][0], points[0][1], config.travel_rate_mm_min)
    for x, y in points[1:]:
        drawing.line_to(x, y, config.feed_rate_mm_min)
    drawing.line_to(points[0][0], points[0][1], config.feed_rate_mm_min)
    return drawing


def spiral(config: PlotterConfig) -> Drawing:
    drawing = Drawing()
    cx = config.drawing_width_mm / 2.0
    cy = config.drawing_height_mm / 2.0
    turns = 4.0
    samples = 160
    max_radius = 228.6

    # Approximate a spiral with many short line segments. GRBL receives simple
    # straight moves, which is easier to stream and preview than curves.
    for index in range(samples):
        t = index / (samples - 1)
        angle = turns * 2.0 * pi * t
        radius = max_radius * t
        x = cx + cos(angle) * radius
        y = cy + sin(angle) * radius
        if index == 0:
            drawing.move_to(x, y, config.travel_rate_mm_min)
        else:
            drawing.line_to(x, y, config.feed_rate_mm_min)

    return drawing
