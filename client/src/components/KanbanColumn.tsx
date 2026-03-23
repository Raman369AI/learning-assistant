import { useState } from 'react';
import type { Item } from '../types';
import KanbanCard from './KanbanCard';

const COLUMN_META: Record<string, { label: string; icon: string }> = {
    brain_dump: { label: 'Brain Dump', icon: '🧠' },
    backlog: { label: 'Backlog', icon: '📋' },
    in_progress: { label: 'In Progress', icon: '⚡' },
    done: { label: 'Done', icon: '✅' },
};

function formatProjectLabel(tag: string): string {
    return tag.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function getProject(item: Item): string {
    return item.tags[0] ?? 'uncategorized';
}

interface Props {
    state: Item['state'];
    items: Item[];
    onCardClick: (item: Item) => void;
    onCardMoved: (item: Item, newState: Item['state']) => void;
    onDelete: (itemId: string) => void;
    viewMode: 'board' | 'list';
}

export default function KanbanColumn({ state, items, onCardClick, onCardMoved, onDelete, viewMode }: Props) {
    const meta = COLUMN_META[state] ?? { label: state, icon: '📌' };
    const [collapsed, setCollapsed] = useState<Set<string>>(new Set());

    const toggleGroup = (key: string) =>
        setCollapsed(prev => {
            const next = new Set(prev);
            next.has(key) ? next.delete(key) : next.add(key);
            return next;
        });

    // Group backlog items by project (first tag); other columns flat
    const useGroups = state === 'backlog' && items.length > 0;
    const groups: { key: string; label: string; items: Item[] }[] = [];

    if (useGroups) {
        const map = new Map<string, Item[]>();
        for (const item of items) {
            const key = getProject(item);
            if (!map.has(key)) map.set(key, []);
            map.get(key)!.push(item);
        }
        for (const [key, groupItems] of map) {
            groups.push({ key, label: formatProjectLabel(key), items: groupItems });
        }
        groups.sort((a, b) => a.label.localeCompare(b.label));
    }

    const cardProps = (item: Item) => ({
        item,
        onClick: onCardClick,
        onMoved: onCardMoved,
        onDelete,
        viewMode,
    });

    return (
        <section className={`column col-${state}${viewMode === 'list' ? ' column--list' : ''}`} aria-label={`${meta.label} column`}>
            <header className="column-header">
                <span>{meta.icon} {meta.label}</span>
                <span className="badge">{items.length}</span>
            </header>
            <div className="column-body">
                {items.length === 0 && (
                    <div className="empty">
                        <span className="empty-icon" aria-hidden="true">○</span>
                        Nothing here yet
                    </div>
                )}

                {useGroups ? (
                    groups.map(group => (
                        <div key={group.key} className="project-group">
                            <button
                                className="project-group-header"
                                onClick={() => toggleGroup(group.key)}
                            >
                                <span className="project-group-chevron">
                                    {collapsed.has(group.key) ? '▶' : '▼'}
                                </span>
                                <span className="project-group-label">{group.label}</span>
                                <span className="badge">{group.items.length}</span>
                            </button>
                            {!collapsed.has(group.key) && group.items.map(item => (
                                <KanbanCard key={item.item_id} {...cardProps(item)} />
                            ))}
                        </div>
                    ))
                ) : (
                    items.map(item => (
                        <KanbanCard key={item.item_id} {...cardProps(item)} />
                    ))
                )}
            </div>
        </section>
    );
}
