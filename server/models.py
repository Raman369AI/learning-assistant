from __future__ import annotations

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


def new_id() -> str:
    return str(uuid.uuid4())


def now() -> str:
    return datetime.utcnow().isoformat()


# ── Enumerations ──────────────────────────────────────────────────────────────

class ItemState(str, Enum):
    brain_dump = "brain_dump"
    backlog = "backlog"
    in_progress = "in_progress"
    done = "done"
    trash = "trash"


class ItemType(str, Enum):
    topic = "topic"
    resource = "resource"
    question = "question"
    paper = "paper"


class ConnectionStrength(str, Enum):
    weak = "weak"
    moderate = "moderate"
    strong = "strong"


class SessionMood(str, Enum):
    easy = "easy"
    hard = "hard"
    confusing = "confusing"


class JobStatus(str, Enum):
    pending = "pending"
    running = "running"
    complete = "complete"
    failed = "failed"


# ── Core domain models ────────────────────────────────────────────────────────

class Goal(BaseModel):
    title: str
    deadline: Optional[str] = None
    topics: list[str] = Field(default_factory=list)


class UserPreferences(BaseModel):
    digest_time: str = "06:00"
    monitored_topics: list[str] = Field(default_factory=list)
    study_cadence: str = "daily"


class UserProfile(BaseModel):
    user_id: str = Field(default_factory=new_id)
    name: str
    created_at: str = Field(default_factory=now)
    goals: list[Goal] = Field(default_factory=list)
    preferences: UserPreferences = Field(default_factory=UserPreferences)


class Item(BaseModel):
    item_id: str = Field(default_factory=new_id)
    user_id: str
    state: ItemState = ItemState.brain_dump
    type: ItemType = ItemType.topic
    title: str
    content: str = ""
    tags: list[str] = Field(default_factory=list)
    source_url: Optional[str] = None
    created_at: str = Field(default_factory=now)
    updated_at: str = Field(default_factory=now)
    effort_estimate: Optional[str] = None
    goal_id: Optional[str] = None


class Session(BaseModel):
    session_id: str = Field(default_factory=new_id)
    user_id: str
    item_id: str
    started_at: str = Field(default_factory=now)
    ended_at: Optional[str] = None
    mood: Optional[SessionMood] = None
    notes: str = ""
    open_questions: list[str] = Field(default_factory=list)
    progress_summary: str = ""


class DigestEntry(BaseModel):
    title: str
    url: str
    summary: str
    relevance_reason: str


class Digest(BaseModel):
    digest_id: str = Field(default_factory=new_id)
    user_id: str
    date: str = Field(default_factory=now)
    topic: str
    papers: list[DigestEntry] = Field(default_factory=list)
    generated_at: str = Field(default_factory=now)


class Connection(BaseModel):
    connection_id: str = Field(default_factory=new_id)
    user_id: str
    item_id_a: str
    item_id_b: str
    rationale: str
    strength: ConnectionStrength = ConnectionStrength.moderate
    discovered_at: str = Field(default_factory=now)


class ResearchJob(BaseModel):
    job_id: str = Field(default_factory=new_id)
    user_id: str
    item_id: str
    status: JobStatus = JobStatus.pending
    result: Optional[str] = None
    created_at: str = Field(default_factory=now)
    completed_at: Optional[str] = None


# ── API request/response shapes ───────────────────────────────────────────────

class CaptureRequest(BaseModel):
    user_id: str
    raw_text: Optional[str] = None
    url: Optional[str] = None

    model_config = {"json_schema_extra": {"example": {
        "user_id": "user-123",
        "url": "https://arxiv.org/abs/1706.03762",
    }}}


class ResearchRequest(BaseModel):
    user_id: str
    item_id: str


class ClarifyRequest(BaseModel):
    user_id: str
    text: str
    session_context: Optional[str] = None


class ClarifyResponse(BaseModel):
    explanation: str
    analogy: Optional[str] = None
    prerequisite_gaps: list[str] = Field(default_factory=list)
    suggested_backlog_item: Optional[str] = None
