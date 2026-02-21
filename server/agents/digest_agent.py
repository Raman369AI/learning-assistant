"""Digest Agent — daily paper monitoring per user topic."""

from __future__ import annotations

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from google.genai import types as genai_types

DIGEST_INSTRUCTION = """\
You are a Digest Agent for a personal learning assistant.

You will receive a user's monitored topic and their current study context.

Your task:
1. Search for the most recent (last 7 days) high-quality paper or article on the topic.
2. Score its relevance to this specific user's goals (0-100).
3. If relevance >= 60, include it in the digest.
4. Return a JSON object:

{
  "topic": "<topic name>",
  "entries": [
    {
      "title": "<paper title>",
      "url":   "<arxiv or source url>",
      "summary": "<2-3 sentence plain-english summary>",
      "relevance_reason": "<why this is relevant to THIS user specifically>"
    }
  ]
}

Return at most 1 entry per topic. If nothing relevant is found, return an empty entries list.
Always return valid JSON.
"""


def build_digest_agent() -> LlmAgent:
    return LlmAgent(
        model="gemini-2.0-flash",
        name="digest_agent",
        description="Monitors topics daily and surfaces the most relevant new paper.",
        instruction=DIGEST_INSTRUCTION,
        tools=[google_search],
        generate_content_config=genai_types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )


digest_agent = build_digest_agent()
