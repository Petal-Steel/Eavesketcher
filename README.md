# EaveSketcher

Starter project for a voice-prompted CNC sketch plotter built around a Jetson Orin Nano.

The intended machine:

- 2 stepper motors for the X axis
- 1 stepper motor for the Y axis
- NEMA 17 steppers
- Servo-controlled Z axis to lift and lower the pen
- Microphone input for spoken drawing prompts
- LLM/speech pipeline to turn prompts into plotter-friendly sketches
- GRBL-style motion controller or G-code sender for motor control
- 24 x 36 inch drawing footprint on a moving paper scroll
- Arduino Uno with CNC shield for motion control

## Development Plan

This project is designed so the basic code can be built on a Windows PC before the Jetson is ready.

Current PC-safe flow:

```text
simulated microphone transcript -> sketch generator -> SVG preview + G-code file
```

Later Jetson flow:

```text
microphone -> speech-to-text -> local LLM sketch planner -> G-code -> GRBL controller
```

## Run On This PC

From this folder:

```bash
python src/main.py --simulate-transcript "draw a house"
python src/main.py --simulate-transcript "draw a star"
python src/main.py --simulate-transcript "draw a spiral"
```

The simulated transcript option is only for development before the microphone path is available. The intended product input is microphone-only.

The program writes:

```text
output/preview.svg
output/sketch.gcode
```

## Drawing Workflow

The planned drawing process is:

```text
spoken prompt
-> speech-to-text transcript
-> local LLM sketch plan
-> validated motion commands
-> SVG preview
-> GRBL G-code
-> Arduino Uno + CNC shield
-> steppers and pen lift
```

See [docs/architecture.md](docs/architecture.md) for the full workflow.

## Project Layout

```text
src/
  main.py             Entry point
  config.py           Paper size, feed rate, step calibration, servo angles
  motion.py           Drawing and motion command types
  sketch_generator.py Prompt-to-sketch logic
  plotter.py          Mock driver now, Jetson driver later
  voice_input.py      Microphone input placeholder
  llm_client.py       Local LLM interface placeholder
  gcode.py            Motion commands to GRBL-style G-code
  grbl_sender.py      Future serial sender for a GRBL controller
docs/
  architecture.md     Hardware and software architecture notes
```

## Recommended VS Code Setup

Install these VS Code extensions on your PC:

- Remote - SSH
- Python
- Pylance

Once the Jetson is set up, connect with:

```text
jetson@192.168.1.50
```

Then open this project folder through the Remote-SSH window.

## Jetson Setup Later

Run this once on the Jetson:

```bash
chmod +x scripts/setup_jetson.sh
./scripts/setup_jetson.sh
```

Then start the app:

```bash
source .venv/bin/activate
python src/main.py
```

On the Jetson, `python src/main.py` will expect the microphone speech-to-text path to be implemented.

## Hardware Notes

Do not wire NEMA 17 motors directly to the Jetson GPIO pins. The Jetson should send step/direction signals to stepper drivers. Typical driver options are TMC2209, DRV8825, A4988, or an external CNC controller board.

The servo will also need a proper 5 V supply. Use common ground between the Jetson, motor drivers, and servo power supply.

The two X-axis motors can share the same step/direction command signals if the mechanics are cloned left/right rails. Each motor still needs its own driver or a driver setup rated for the motor current.

Home is bottom-left of the 24 x 36 inch drawing area. The paper scroll is not part of normal drawing motion; it only advances the paper to clean the slate.

## Local LLM Notes

Local LLM is possible, but it should be used as a sketch planner rather than a direct G-code writer. The app should ask the model for structured drawing intent, validate it, then generate the G-code itself.

Good first local options to evaluate on the Jetson are Ollama or llama.cpp with a small quantized model. Speech-to-text can also run locally, but it may need a smaller model for responsive microphone input.
