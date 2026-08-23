from __future__ import annotations


def get_prompt_from_microphone() -> str:
    # This is intentionally not a keyboard fallback. The desired product flow is
    # microphone-only, while --simulate-transcript exists for development tests.
    raise NotImplementedError(
        "Microphone capture is the intended input path. Choose a speech-to-text backend before enabling this."
    )
