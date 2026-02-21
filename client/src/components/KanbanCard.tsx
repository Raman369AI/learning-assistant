import { useState, useEffect } from 'react';
import type { Item, ResearchJob } from '../types';
import { api } from '../services/api';

interface Props {
    item: Item;
    onClick: (item: Item) => void;
    onMoved: (item: Item, newState: Item['state']) => void;
}

const STATE_ORDER: Item['state'][] = ['brain_dump', 'backlog', 'in_progress', 'done'];
const STATE_LABELS: Record<Item['state'], string> = {
    brain_dump: 'Brain Dump',
    backlog: 'Backlog',
    in_progress: 'In Progress',
    done: 'Done',
    trash: 'Trash',
};
const TYPE_ICONS: Record<Item['type'], string> = {
    topic: '📚', resource: '🔗', question: '❓', paper: '📄',
};

export default function KanbanCard({ item, onClick, onMoved }: Props) {
    const [researchJob, setResearchJob] = useState<ResearchJob | null>(null);
    const [polling, setPolling] = useState(false);

    const currentIdx = STATE_ORDER.indexOf(item.state);
    const nextState = currentIdx < STATE_ORDER.length - 1 ? STATE_ORDER[currentIdx + 1] : null;
    const prevState = currentIdx > 0 ? STATE_ORDER[currentIdx - 1] : null;

    useEffect(() => {
        if (!researchJob || researchJob.status === 'complete' || researchJob.status === 'failed') return;
        setPolling(true);
        const id = setInterval(async () => {
            const job = await api.pollResearch(researchJob.job_id);
            setResearchJob(job);
            if (job.status === 'complete' || job.status === 'failed') {
                clearInterval(id);
                setPolling(false);
            }
        }, 3000);
        return () => clearInterval(id);
    }, [researchJob]);

    const handleMoveRight = async (e: React.MouseEvent) => {
        e.stopPropagation();
        if (!nextState) return;
        if (nextState === 'in_progress') {
            const job = await api.startResearch(item.item_id);
            setResearchJob(job);
        }
        onMoved(item, nextState);
    };

    const handleMoveLeft = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (!prevState) return;
        onMoved(item, prevState);
    };

    return (
        <article
            id={`card-${item.item_id}`}
            className="card"
            onClick={() => onClick(item)}
            role="button"
            tabIndex={0}
            onKeyDown={e => e.key === 'Enter' && onClick(item)}
            aria-label={`Item: ${item.title}`}
        >
            <p className="card-title">
                <span aria-hidden="true">{TYPE_ICONS[item.type] ?? '📌'} </span>
                {item.title}
            </p>

            {polling && (
                <p className="card-researching">⬡ Researching…</p>
            )}

            <div className="card-meta">
                {item.tags.slice(0, 3).map(tag => (
                    <span key={tag} className="tag">{tag}</span>
                ))}
                {item.effort_estimate && (
                    <span className="card-effort">{item.effort_estimate}</span>
                )}
            </div>

            <div className="card-actions">
                {prevState && (
                    <button
                        className="btn btn-ghost"
                        onClick={handleMoveLeft}
                        aria-label={`Move to ${STATE_LABELS[prevState]}`}
                    >
                        ← {STATE_LABELS[prevState]}
                    </button>
                )}
                {nextState && (
                    <button
                        className="btn btn-primary"
                        onClick={handleMoveRight}
                        aria-label={`Move to ${STATE_LABELS[nextState]}`}
                    >
                        {STATE_LABELS[nextState]} →
                    </button>
                )}
            </div>
        </article>
    );
}
