from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SketchPlan:
    # Future structured output from the local LLM.
    # The app should validate this plan before converting anything to G-code.
    title: str
    description: str
    shape_hint: str


class LocalLLMClient:
    def create_sketch_plan(self, transcript: str) -> SketchPlan:
        # Candidate runtimes: Ollama or llama.cpp with a small quantized model.
        # Keep the interface narrow so the rest of the app does not care which one wins.
        raise NotImplementedError(
            "Local LLM support will be wired after choosing the runtime, likely Ollama or llama.cpp."
        )


class MockLLMClient:
    def create_sketch_plan(self, transcript: str) -> SketchPlan:
        # Development stand-in: echoes the transcript as the drawing hint.
        text = transcript.strip()
        return SketchPlan(title="Mock sketch", description=text, shape_hint=text)
