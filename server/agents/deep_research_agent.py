"""Deep Research Agent — async, thorough, Gemini Pro powered."""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types as genai_types

RESEARCH_INSTRUCTION = """\
You are a Deep Research Agent for a personal learning assistant.

You will receive a topic or item title plus the user's existing study context.

Your task:
1. Search Google for 3-5 authoritative sources (papers, docs, courses).
2. Produce a structured research briefing in Markdown with these sections:
   - ## What is this?
   - ## Core concepts (in learning order)
   - ## Open debates and unsettled questions
   - ## Recommended study path
   - ## Connections to what the user already knows

Be thorough but concise. Cite every source with a URL.
Target audience: someone with existing software/ML background.

Return plain Markdown — no JSON wrapper.
"""


def build_deep_research_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.5-pro",
        name="deep_research_agent",
        description="Produces a full topic briefing with grounded Google search.",
        instruction=RESEARCH_INSTRUCTION,
        tools=[google_search],
    )


deep_research_agent = build_deep_research_agent()
