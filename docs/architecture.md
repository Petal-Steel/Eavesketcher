# EaveSketcher Architecture

## Roles

The Jetson Orin Nano handles:

- Microphone input
- Speech-to-text
- Local LLM sketch planning
- Sketch validation
- SVG preview
- G-code generation
- Optional G-code streaming

The Arduino Uno with CNC shield handles:

- GRBL motion control
- Step/direction timing
- X-axis cloned rail movement
- Y-axis movement
- Limit switches and homing, if installed

## Motion Setup

- Origin: bottom-left of the drawing footprint
- Drawing footprint: 24 x 36 inches, or 609.6 x 914.4 mm
- X axis: two cloned rail motors receiving the same step/direction commands
- Y axis: one motor
- Paper scroll: advance-only mechanism to clean the slate, not a drawing axis

## Pen Control Recommendation

The cleanest first version is to let GRBL-compatible commands control pen state:

```gcode
M3 S1000 ; pen down
M5       ; pen up
```

Those commands can drive one of these later:

- A servo adapter controlled by the CNC shield/spindle signal
- A small second microcontroller that listens for pen commands
- A relay/solenoid style pen lift

Servo is mechanically gentle and adjustable, so it is the best first choice for a marker or pen.

## Local LLM Plan

The local LLM should not output raw G-code directly. Safer flow:

```text
speech transcript -> local LLM -> structured sketch plan -> validator -> G-code
```

This keeps the machine inside known bounds and lets the app reject invalid or unsafe drawing instructions.

## Drawing Workflow

1. The user speaks a request into the microphone.

2. Speech-to-text converts the audio into a transcript.

Example:

```text
Draw a five point star with a circle around it.
```

3. The local LLM reads the transcript and creates a structured sketch plan.

The sketch plan should describe intent, not raw machine motion. For example:

```text
subject: star inside circle
style: simple line art
placement: centered
size: medium
```

4. The sketch generator converts the plan into internal motion commands.

Internal commands are simple pen-aware moves:

```text
move_to x,y with pen up
line_to x,y with pen down
```

5. The validator checks the drawing before export.

Future validation should confirm:

- All X coordinates stay between 0 and 609.6 mm
- All Y coordinates stay between 0 and 914.4 mm
- Feed rates are reasonable
- The pen starts and ends raised
- The drawing returns to a known safe state

6. The app writes an SVG preview.

The team can inspect this before running the machine:

```text
output/preview.svg
```

7. The app writes GRBL-style G-code.

The G-code file is the machine-facing output:

```text
output/sketch.gcode
```

8. A G-code sender streams the file to the Arduino Uno.

The Arduino Uno running GRBL handles timing-sensitive step pulses through the CNC shield.

9. GRBL drives the motion hardware.

- X motors receive cloned step/direction signals
- Y motor receives its own step/direction signals
- Pen lift responds to `M3 S1000` and `M5`, or an equivalent mapped mechanism

10. After the drawing finishes, the pen lifts and the machine returns home.

11. The paper scroll advances only when a fresh drawing area is needed.
