from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlotterConfig:
    # Machine/controller assumptions used in generated notes and G-code headers.
    controller_name: str = "Arduino Uno + CNC Shield running GRBL"

    # All motion is expressed in millimeters because GRBL's G21 mode uses mm.
    # 609.6 x 914.4 mm equals a 24 x 36 inch drawing footprint.
    drawing_width_mm: float = 609.6
    drawing_height_mm: float = 914.4

    # The plotter homes to the bottom-left of the usable drawing area.
    # The paper scroll is separate from XY drawing and only advances fresh paper.
    origin_name: str = "bottom-left"
    paper_scroll_mode: str = "advance-only"

    # Feed rates are in mm/min, which is the unit GRBL expects for F values.
    feed_rate_mm_min: float = 2100.0
    travel_rate_mm_min: float = 3000.0

    # Servo angles are used by the mock driver for readable output.
    # The real machine may instead use GRBL M3/M5 commands to trigger pen lift.
    pen_up_angle: int = 35
    pen_down_angle: int = 85

    # Current recommendation: map pen state to GRBL spindle-style commands.
    # Later these may drive a servo adapter, solenoid, or small pen-lift MCU.
    pen_up_command: str = "M5"
    pen_down_command: str = "M3 S1000"

    # Machine home. With bottom-left origin, this is the lower-left corner.
    home_x_mm: float = 0.0
    home_y_mm: float = 0.0


# Shared default configuration imported by the app entry point.
CONFIG = PlotterConfig()
