export type ItemState = 'brain_dump' | 'backlog' | 'in_progress' | 'done' | 'trash';
export type ItemType = 'topic' | 'resource' | 'question' | 'paper';
export type ConnectionStrength = 'weak' | 'moderate' | 'strong';
export type JobStatus = 'pending' | 'running' | 'complete' | 'failed';

export interface Item {
    item_id: string;
    user_id: string;
    state: ItemState;
    type: ItemType;
    title: string;
    content: string;
    tags: string[];
    source_url?: string;
    created_at: string;
    updated_at: string;
    effort_estimate?: string;
    goal_id?: string;
}

export interface ResearchJob {
    job_id: string;
    user_id: string;
    item_id: string;
    status: JobStatus;
    result?: string;
    created_at: string;
    completed_at?: string;
}

export interface ClarifyResponse {
    explanation: string;
    analogy?: string;
    prerequisite_gaps: string[];
    suggested_backlog_item?: string;
}

export interface DigestEntry {
    title: string;
    url: string;
    summary: string;
    relevance_reason: string;
}

export interface Digest {
    digest_id: string;
    user_id: string;
    date: string;
    topic: string;
    papers: DigestEntry[];
    generated_at: string;
}

export interface Connection {
    connection_id: string;
    user_id: string;
    item_id_a: string;
    item_id_b: string;
    rationale: string;
    strength: ConnectionStrength;
    discovered_at: string;
}
