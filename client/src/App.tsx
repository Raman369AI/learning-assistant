import { useState, useEffect } from 'react';
import './index.css';
import type { Item } from './types';
import { api } from './services/api';
import CaptureBar from './components/CaptureBar';
import KanbanColumn from './components/KanbanColumn';
import ItemModal from './components/ItemModal';
import InsightSidebar from './components/InsightSidebar';

const COLUMNS: Item['state'][] = ['brain_dump', 'backlog', 'in_progress', 'done'];

export default function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [selected, setSelected] = useState<Item | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.listItems()
      .then(setItems)
      .catch(() => { })
      .finally(() => setLoading(false));
  }, []);

  const handleCapture = (item: Item) => {
    setItems(prev => [item, ...prev]);
  };

  const handleCardMoved = (movedItem: Item, newState: Item['state']) => {
    setItems(prev =>
      prev.map(it =>
        it.item_id === movedItem.item_id ? { ...it, state: newState } : it
      )
    );
  };

  const itemsForColumn = (state: Item['state']) =>
    items.filter(it => it.state === state);

  return (
    <div className="app-shell">
      {/* Top bar */}
      <header className="topbar" role="banner">
        <span className="topbar-logo">🧠 LearningOS</span>
        <CaptureBar onCapture={handleCapture} />
      </header>

      {/* Kanban board */}
      <main className="board" aria-label="Learning Kanban Board">
        {loading ? (
          <p style={{ color: 'var(--text-2)', alignSelf: 'center', margin: 'auto' }}>
            Loading your board…
          </p>
        ) : (
          COLUMNS.map(state => (
            <KanbanColumn
              key={state}
              state={state}
              items={itemsForColumn(state)}
              onCardClick={setSelected}
              onCardMoved={handleCardMoved}
            />
          ))
        )}
      </main>

      {/* Insight Sidebar */}
      <InsightSidebar />

      {/* Item detail modal */}
      {selected && (
        <ItemModal
          item={selected}
          onClose={() => setSelected(null)}
        />
      )}
    </div>
  );
}
