from __future__ import annotations

from config import PlotterConfig
from motion import MotionCommand, PenState


def generate_gcode(commands: list[MotionCommand], config: PlotterConfig) -> list[str]:
    # G-code is the handoff format for GRBL. Keep all safety-relevant decisions
    # here so the LLM never sends raw motion directly to the controller.
    lines = [
        "; EaveSketcher",
        f"; Controller: {config.controller_name}",
        f"; Origin: {config.origin_name}",
        f"; Drawing area: {config.drawing_width_mm:.1f} x {config.drawing_height_mm:.1f} mm",
        f"; Paper scroll: {config.paper_scroll_mode}",
        "; Units: millimeters",
        "G21",  # Use millimeters.
        "G90",  # Use absolute coordinates from the bottom-left origin.
        config.pen_up_command,  # Start safe with the pen raised.
        f"G0 X{config.home_x_mm:.3f} Y{config.home_y_mm:.3f}",
    ]

    current_pen = PenState.UP

    for command in commands:
        # Only emit pen commands when the state changes. This keeps G-code
        # readable and avoids hammering a servo or solenoid unnecessarily.
        if command.pen != current_pen:
            lines.append(config.pen_down_command if command.pen == PenState.DOWN else config.pen_up_command)
            current_pen = command.pen

        # Pen-up moves are rapid positioning moves; pen-down moves are drawing moves.
        move_code = "G1" if command.pen == PenState.DOWN else "G0"
        feed = command.feed_rate_mm_min
        lines.append(f"{move_code} X{command.x:.3f} Y{command.y:.3f} F{feed:.1f}")

    lines.extend(
        [
            config.pen_up_command,  # End with the pen up before returning home.
            f"G0 X{config.home_x_mm:.3f} Y{config.home_y_mm:.3f} F{config.travel_rate_mm_min:.1f}",
            "M2",  # Program end.
        ]
    )
    return lines


def gcode_text(commands: list[MotionCommand], config: PlotterConfig) -> str:
    # Most senders expect a final newline at the end of a G-code file.
    return "\n".join(generate_gcode(commands, config)) + "\n"
