import type { Item } from '../types';
import KanbanCard from './KanbanCard';

const COLUMN_META: Record<string, { label: string; icon: string; count?: number }> = {
    brain_dump: { label: 'Brain Dump', icon: '🧠' },
    backlog: { label: 'Backlog', icon: '📋' },
    in_progress: { label: 'In Progress', icon: '⚡' },
    done: { label: 'Done', icon: '✅' },
};

interface Props {
    state: Item['state'];
    items: Item[];
    onCardClick: (item: Item) => void;
    onCardMoved: (item: Item, newState: Item['state']) => void;
}

export default function KanbanColumn({ state, items, onCardClick, onCardMoved }: Props) {
    const meta = COLUMN_META[state] ?? { label: state, icon: '📌' };

    return (
        <section className={`column col-${state}`} aria-label={`${meta.label} column`}>
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
                {items.map(item => (
                    <KanbanCard
                        key={item.item_id}
                        item={item}
                        onClick={onCardClick}
                        onMoved={onCardMoved}
                    />
                ))}
            </div>
        </section>
    );
}
