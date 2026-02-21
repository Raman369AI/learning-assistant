import { useState, useEffect } from 'react';
import type { Digest, Connection } from '../types';
import { api } from '../services/api';

type Tab = 'digests' | 'connections' | 'resurface';

export default function InsightSidebar() {
    const [tab, setTab] = useState<Tab>('digests');
    const [digests, setDigests] = useState<Digest[]>([]);
    const [connections, setConnections] = useState<Connection[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (tab === 'digests' && digests.length === 0) {
            setLoading(true);
            api.listDigests().then(setDigests).catch(() => { }).finally(() => setLoading(false));
        }
        if (tab === 'connections' && connections.length === 0) {
            setLoading(true);
            api.listConnections().then(setConnections).catch(() => { }).finally(() => setLoading(false));
        }
    }, [tab]);

    const strengthColor: Record<string, string> = {
        strong: 'var(--accent-research)',
        moderate: 'var(--accent-connect)',
        weak: 'var(--text-2)',
    };

    return (
        <aside className="sidebar" aria-label="Insight Center">
            <nav className="sidebar-tabs" aria-label="Insight tabs">
                {([
                    ['digests', '📰 Digest'],
                    ['connections', '🕸 Links'],
                    ['resurface', '🔁 Review'],
                ] as [Tab, string][]).map(([t, label]) => (
                    <button
                        key={t}
                        id={`sidebar-tab-${t}`}
                        className={`sidebar-tab ${tab === t ? 'active' : ''}`}
                        onClick={() => setTab(t)}
                    >
                        {label}
                    </button>
                ))}
            </nav>

            <div className="sidebar-body">
                {loading && <p style={{ color: 'var(--text-2)', fontSize: '.8rem' }}>Loading…</p>}

                {tab === 'digests' && !loading && (
                    digests.length === 0
                        ? <div className="empty"><span className="empty-icon">📰</span>No digests yet — trigger the Digest Agent first.</div>
                        : digests.map(d => (
                            <div key={d.digest_id} className="insight-card">
                                <p className="insight-card-title">
                                    <span className="insight-dot dot-digest" />
                                    {d.topic}
                                </p>
                                {d.papers.map(p => (
                                    <div key={p.url} style={{ borderTop: '1px solid var(--border)', paddingTop: 8, marginTop: 4 }}>
                                        <a href={p.url} target="_blank" rel="noreferrer" className="insight-card-title" style={{ color: 'var(--accent-digest)' }}>{p.title}</a>
                                        <p className="insight-card-body">{p.summary}</p>
                                        <p className="insight-card-sub">📎 {p.relevance_reason}</p>
                                    </div>
                                ))}
                            </div>
                        ))
                )}

                {tab === 'connections' && !loading && (
                    connections.length === 0
                        ? <div className="empty"><span className="empty-icon">🕸</span>No connections yet — complete more items first.</div>
                        : connections.map(c => (
                            <div key={c.connection_id} className="insight-card">
                                <p className="insight-card-title" style={{ color: strengthColor[c.strength] ?? 'inherit' }}>
                                    <span className="insight-dot dot-connect" />
                                    {c.strength} link
                                </p>
                                <p className="insight-card-body">{c.rationale}</p>
                            </div>
                        ))
                )}

                {tab === 'resurface' && !loading && (
                    <div className="empty">
                        <span className="empty-icon">🔁</span>
                        <p>Spaced-repetition cards appear here after the Resurfacing Agent runs daily.</p>
                        <button
                            id="trigger-resurface-btn"
                            className="btn btn-ghost"
                            style={{ marginTop: 12 }}
                            onClick={() => api.triggerResurface().catch(() => { })}
                        >
                            Run now (dev)
                        </button>
                    </div>
                )}

                {/* Dev triggers */}
                <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: 8, borderTop: '1px solid var(--border)', paddingTop: 12 }}>
                    <p style={{ fontSize: '.68rem', color: 'var(--text-2)', fontWeight: 700, letterSpacing: '.06em' }}>DEV TRIGGERS</p>
                    <button id="trigger-digest-btn" className="btn btn-ghost" style={{ fontSize: '.72rem' }} onClick={() => api.triggerDigest().catch(() => { })}>▶ Run Digest Agent</button>
                    <button id="trigger-connect-btn" className="btn btn-ghost" style={{ fontSize: '.72rem' }} onClick={() => api.triggerConnect().catch(() => { })}>▶ Run Connection Agent</button>
                </div>
            </div>
        </aside>
    );
}
