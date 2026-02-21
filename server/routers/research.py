"""POST /research — async deep research via background task.
GET  /research/{job_id} — poll job status.
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from agents.deep_research_agent import deep_research_agent
from models import JobStatus, ResearchJob, ResearchRequest
from services.firestore_repo import (
    get_item,
    get_research_job,
    get_user_profile,
    save_item,
    save_research_job,
    update_research_job,
)

router = APIRouter(prefix="/research", tags=["research"])


async def _run_research(job_id: str, item_id: str, user_id: str) -> None:
    """Background coroutine: runs Deep Research Agent and writes result to Firestore."""
    await update_research_job(job_id, status=JobStatus.running)

    try:
        item = await get_item(item_id)
        profile = await get_user_profile(user_id)
        known_topics = [t for g in profile.goals for t in g.topics] if profile else []

        prompt = (
            f"Topic: {item.title if item else item_id}\n"
            f"Existing knowledge context: {known_topics}\n"
            "Please produce a full research briefing."
        )

        runner = InMemoryRunner(agent=deep_research_agent, app_name="research")
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name="research", user_id=user_id
        )

        result_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=genai_types.Content(
                role="user", parts=[genai_types.Part(text=prompt)]
            ),
        ):
            if event.is_final_response() and event.content:
                result_text = event.content.parts[0].text

        # Move item to in_progress and attach briefing
        if item:
            item.state = "in_progress"  # type: ignore[assignment]
            item.content = result_text
            item.updated_at = datetime.utcnow().isoformat()
            await save_item(item)

        await update_research_job(
            job_id,
            status=JobStatus.complete,
            result=result_text,
            completed_at=datetime.utcnow().isoformat(),
        )
    except Exception as exc:
        await update_research_job(
            job_id,
            status=JobStatus.failed,
            result=str(exc),
            completed_at=datetime.utcnow().isoformat(),
        )


@router.post("", response_model=ResearchJob, status_code=202)
async def start_research(
    req: ResearchRequest, background_tasks: BackgroundTasks
) -> ResearchJob:
    """Enqueue a deep-research job. Returns immediately with job_id."""
    job = ResearchJob(user_id=req.user_id, item_id=req.item_id)
    await save_research_job(job)
    background_tasks.add_task(_run_research, job.job_id, req.item_id, req.user_id)
    return job


@router.get("/{job_id}", response_model=ResearchJob)
async def poll_research(job_id: str) -> ResearchJob:
    """Poll the status of a research job."""
    job = await get_research_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found.")
    return job
