import type { Item, ResearchJob, ClarifyResponse, Digest, Connection } from '../types';

const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
const USER_ID = 'demo-user';

async function req<T>(path: string, options?: RequestInit): Promise<T> {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 5000);
    try {
        const res = await fetch(`${BASE}${path}`, {
            headers: { 'Content-Type': 'application/json' },
            signal: controller.signal,
            ...options,
        });
        if (!res.ok) {
            const detail = await res.text();
            throw new Error(`${res.status}: ${detail}`);
        }
        return res.json() as Promise<T>;
    } finally {
        clearTimeout(timeout);
    }
}

export const api = {
    // Items
    listItems: (state?: string) =>
        req<Item[]>(`/items/${USER_ID}${state ? `?state=${state}` : ''}`),

    deleteItem: (item_id: string) =>
        req<void>(`/items/${USER_ID}/${item_id}`, { method: 'DELETE' }),

    // Capture (Triage Agent)
    capture: (input: { raw_text?: string; url?: string }) =>
        req<Item>('/capture', {
            method: 'POST',
            body: JSON.stringify({ user_id: USER_ID, ...input }),
        }),

    // Research (Deep Research Agent)
    startResearch: (item_id: string) =>
        req<ResearchJob>('/research', {
            method: 'POST',
            body: JSON.stringify({ user_id: USER_ID, item_id }),
        }),

    pollResearch: (job_id: string) => req<ResearchJob>(`/research/${job_id}`),

    // Clarify (Clarification Agent)
    clarify: (text: string, session_context?: string) =>
        req<ClarifyResponse>('/clarify', {
            method: 'POST',
            body: JSON.stringify({ user_id: USER_ID, text, session_context }),
        }),

    // Digests
    listDigests: () => req<Digest[]>(`/digest/${USER_ID}`),

    // Connections
    listConnections: () => req<Connection[]>(`/connect/${USER_ID}`),

    // Trigger batch agents (scheduled — useful for manual trigger in dev)
    triggerDigest: () => req('/digest/trigger', { method: 'POST' }),
    triggerConnect: () => req('/connect', { method: 'POST' }),
    triggerResurface: () => req('/resurface', { method: 'POST' }),
};
