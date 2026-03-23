import { useState, useEffect } from 'react';
import './index.css';
import type { Item } from './types';
import { api } from './services/api';
import CaptureBar from './components/CaptureBar';
import KanbanColumn from './components/KanbanColumn';
import ItemModal from './components/ItemModal';
import InsightSidebar from './components/InsightSidebar';
import StaleNotification, { getStaleItems } from './components/StaleNotification';

const COLUMNS: Item['state'][] = ['brain_dump', 'backlog', 'in_progress', 'done'];

// Persist dismissed stale item IDs in sessionStorage so they don't reappear
// in the same browser session.
const DISMISSED_KEY = 'la_dismissed_stale';
const getDismissed = (): Set<string> =>
  new Set(JSON.parse(sessionStorage.getItem(DISMISSED_KEY) ?? '[]'));
const saveDismissed = (ids: Set<string>) =>
  sessionStorage.setItem(DISMISSED_KEY, JSON.stringify([...ids]));

export default function App() {
  const [items, setItems] = useState<Item[]>([]);
  const [selected, setSelected] = useState<Item | null>(null);
  const [loading, setLoading] = useState(true);
  const [dismissed, setDismissed] = useState<Set<string>>(getDismissed);

  useEffect(() => {
    api.listItems()
      .then(setItems)
      .catch(() => { })
      .finally(() => setLoading(false));
  }, []);

  // Re-check every 30 minutes in case the user leaves the tab open
  useEffect(() => {
    const id = setInterval(() => setItems(prev => [...prev]), 30 * 60 * 1000);
    return () => clearInterval(id);
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
    // If user moves a stale item out of brain_dump, auto-remove its notification
    if (newState !== 'brain_dump') {
      handleDismiss(movedItem.item_id);
    }
  };

  const handleDismiss = (itemId: string) => {
    setDismissed(prev => {
      const next = new Set(prev).add(itemId);
      saveDismissed(next);
      return next;
    });
  };

  const handleDismissAll = () => {
    const allStaleIds = staleItems.map(it => it.item_id);
    setDismissed(prev => {
      const next = new Set(prev);
      allStaleIds.forEach(id => next.add(id));
      saveDismissed(next);
      return next;
    });
  };

  const itemsForColumn = (state: Item['state']) =>
    items.filter(it => it.state === state);

  const staleItems = getStaleItems(items).filter(it => !dismissed.has(it.item_id));

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

      {/* Stale Brain Dump notification */}
      <StaleNotification
        staleItems={staleItems}
        onDismiss={handleDismiss}
        onDismissAll={handleDismissAll}
      />
    </div>
  );
}
