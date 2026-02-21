"""Clarification Agent — concept explainer on demand."""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.genai import types as genai_types

CLARIFY_INSTRUCTION = """\
You are a Clarification Agent for a personal learning assistant.

The user has pasted a concept, paragraph, or term they don't fully understand.

Your task — return a JSON object:
{
  "explanation":             "<clear, jargon-free explanation, 3-5 sentences>",
  "analogy":                 "<a memorable real-world analogy>",
  "prerequisite_gaps":       ["<concept A>", "<concept B>"],
  "suggested_backlog_item":  "<title of a suggested backlog item to add, or null>"
}

Rules:
- Keep the explanation accessible but assume a technical background.
- List only genuine prerequisite gaps — things the user likely needs before this.
- Only suggest a backlog item if there is a clear, well-scoped topic worth adding.
- Always return valid JSON, nothing else.
"""


def build_clarify_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash",
        name="clarification_agent",
        description="Explains concepts clearly, finds analogies, identifies prerequisite gaps.",
        instruction=CLARIFY_INSTRUCTION,
        generate_content_config=genai_types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )


clarification_agent = build_clarify_agent()
