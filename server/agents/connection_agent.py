"""Connection Agent — finds semantic links across the knowledge base.

Strategy:
  1. The FastAPI router gathers all done/in-progress item titles + content.
  2. Passes them as context to this agent.
  3. Agent uses reasoning (Flash is fine post-embedding-filter) to validate
     and rate connections, returning JSON.
"""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.genai import types as genai_types

CONNECTION_INSTRUCTION = """\
You are a Connection Agent for a personal learning assistant.

You will receive a list of items the user has studied, each with an id, title,
and brief summary.

Your task: identify pairs of items that have non-obvious, meaningful conceptual
connections. Skip self-evident links (e.g. "both are about Python").

Return a JSON array of connection objects:
[
  {
    "item_id_a":  "<id>",
    "item_id_b":  "<id>",
    "rationale":  "<1-2 sentences explaining the connection>",
    "strength":   "weak" | "moderate" | "strong"
  }
]

Rules:
- Return at most 10 connections.
- Prefer strong/moderate connections.
- If no meaningful connections exist, return an empty array.
- Always return valid JSON.
"""


def build_connection_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash",
        name="connection_agent",
        description="Discovers semantic knowledge connections across a user's studied items.",
        instruction=CONNECTION_INSTRUCTION,
        generate_content_config=genai_types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )


connection_agent = build_connection_agent()
