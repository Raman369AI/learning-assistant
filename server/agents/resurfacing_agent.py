"""Resurfacing Agent — spaced repetition nudges from session mood history."""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.genai import types as genai_types

RESURFACE_INSTRUCTION = """\
You are a Resurfacing Agent for a personal learning assistant.

You will receive a list of completed items with:
- title
- completed_at (ISO date)
- mood of the last session (easy | hard | confusing)
- decay_score (0-100, higher = more due for review)

Select up to 5 items most in need of review (highest decay score and/or hard/confusing mood).

For each, generate a short recall prompt — a challenge question that tests understanding
without giving away the answer.

Return a JSON array:
[
  {
    "item_id":       "<id>",
    "item_title":    "<title>",
    "recall_prompt": "<challenge question, 1-2 sentences>"
  }
]

Always return valid JSON.
"""


def build_resurfacing_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash",
        name="resurfacing_agent",
        description="Generates spaced-repetition recall prompts for items due for review.",
        instruction=RESURFACE_INSTRUCTION,
        generate_content_config=genai_types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )


resurfacing_agent = build_resurfacing_agent()
