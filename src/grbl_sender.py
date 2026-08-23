from __future__ import annotations

from pathlib import Path


def send_gcode_file(port: str, baud: int, path: Path) -> None:
    raise NotImplementedError(
        "GRBL serial streaming will be added once the motion controller board and serial port are known."
    )
