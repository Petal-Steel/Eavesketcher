from __future__ import annotations

import argparse
from pathlib import Path

from config import CONFIG
from gcode import gcode_text
from plotter import MockPlotterDriver, run_commands
from preview import save_svg
from sketch_generator import generate_sketch
from voice_input import get_prompt_from_microphone


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    # The real product path is microphone input. The simulated transcript is
    # only here so teammates can test sketch generation on a normal PC.
    parser = argparse.ArgumentParser(description="Sketch plotter controller")
    parser.add_argument("--simulate-transcript", help="Development-only stand-in for microphone transcription")
    parser.add_argument("--mock", action="store_true", help="Use the PC-safe mock plotter driver")
    parser.add_argument("--preview", default="output/preview.svg", help="SVG preview output path")
    parser.add_argument("--gcode", default="output/sketch.gcode", help="G-code output path")
    return parser.parse_args()


def project_path(path_text: str) -> Path:
    # Keep output paths stable even when VS Code launches the script from a
    # different current working directory.
    path = Path(path_text)
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


def main() -> None:
    args = parse_args()

    # On the Jetson, this will come from microphone speech-to-text.
    # On a PC, pass --simulate-transcript while the audio path is unfinished.
    prompt = args.simulate_transcript or get_prompt_from_microphone()

    # Prompt/transcript becomes a high-level drawing first, not raw G-code.
    drawing = generate_sketch(prompt, CONFIG)
    driver = MockPlotterDriver(CONFIG)

    print(f"Prompt: {prompt}")
    print(f"Commands: {len(drawing.commands)}")
    preview_path = project_path(args.preview)
    save_svg(drawing.commands, CONFIG, preview_path)

    # G-code is the file a GRBL sender can eventually stream to the Arduino Uno.
    gcode_path = project_path(args.gcode)
    gcode_path.parent.mkdir(parents=True, exist_ok=True)
    gcode_path.write_text(gcode_text(drawing.commands, CONFIG), encoding="utf-8")
    print(f"Preview: {preview_path}")
    print(f"G-code: {gcode_path}")
    run_commands(driver, drawing.commands)


if __name__ == "__main__":
    main()
