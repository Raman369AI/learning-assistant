"""Triage Agent — classifies and routes brain-dump captures.

Fast path: uses Gemini Flash so the user never waits.
"""

from __future__ import annotations

import json
import os

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.genai import types as genai_types

TRIAGE_INSTRUCTION = """\
You are a personal learning assistant's Triage Agent.

Your job is to analyse a raw piece of content the user just captured (a URL,
pasted text, or note) and return a JSON object with these fields:

{
  "type":             "topic" | "resource" | "question" | "paper",
  "title":            "<concise title, max 80 chars>",
  "tags":             ["<tag1>", "<tag2>"],
  "suggested_state":  "brain_dump" | "backlog" | "trash",
  "goal_id":          "<goal_id or null>",
  "effort_estimate":  "15min" | "1h" | "2-4h" | "1d+" | null,
  "reasoning":        "<one sentence explaining your decision>"
}

Rules:
- If the content is clearly irrelevant or junk → suggest "trash"
- If the topic is clear and maps to a known goal → suggest "backlog"
- Otherwise → keep in "brain_dump" for the user to review
- Tags must come from the user's existing topic list when possible
- Always return valid JSON, nothing else
"""


def build_triage_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash",
        name="triage_agent",
        description="Classifies and routes raw brain-dump captures into structured items.",
        instruction=TRIAGE_INSTRUCTION,
        generate_content_config=genai_types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )


triage_agent = build_triage_agent()
