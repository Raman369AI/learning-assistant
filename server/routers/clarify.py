"""POST /clarify — on-demand concept explanation."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agents.clarification_agent import clarification_agent
from models import ClarifyRequest, ClarifyResponse

router = APIRouter(prefix="/clarify", tags=["clarify"])


@router.post("", response_model=ClarifyResponse)
async def clarify(req: ClarifyRequest) -> ClarifyResponse:
    """Explain a concept, surface analogies and prerequisite gaps."""
    prompt = req.text
    if req.session_context:
        prompt = f"Session context: {req.session_context}\n\nConcept to clarify: {req.text}"

    runner = InMemoryRunner(agent=clarification_agent, app_name="clarify")
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="clarify", user_id=req.user_id
    )

    result_text = ""
    async for event in runner.run_async(
        user_id=req.user_id,
        session_id=session.id,
        new_message=genai_types.Content(
            role="user", parts=[genai_types.Part(text=prompt)]
        ),
    ):
        if event.is_final_response() and event.content:
            result_text = event.content.parts[0].text

    try:
        data = json.loads(result_text)
    except json.JSONDecodeError:
        raise HTTPException(status_code=502, detail="Clarification agent returned invalid JSON.")

    return ClarifyResponse(
        explanation=data.get("explanation", ""),
        analogy=data.get("analogy"),
        prerequisite_gaps=data.get("prerequisite_gaps", []),
        suggested_backlog_item=data.get("suggested_backlog_item"),
    )
