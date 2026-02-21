import { useState } from 'react';
import type { Item, ClarifyResponse } from '../types';
import { api } from '../services/api';

interface Props {
    item: Item;
    onClose: () => void;
}

type Tab = 'details' | 'clarify' | 'research';

export default function ItemModal({ item, onClose }: Props) {
    const [tab, setTab] = useState<Tab>('details');
    const [clarifyText, setClarifyText] = useState('');
    const [clarifyResult, setClarifyResult] = useState<ClarifyResponse | null>(null);
    const [clarifyLoading, setClarifyLoading] = useState(false);

    const handleClarify = async () => {
        if (!clarifyText.trim()) return;
        setClarifyLoading(true);
        setClarifyResult(null);
        try {
            const res = await api.clarify(clarifyText, item.title);
            setClarifyResult(res);
        } finally {
            setClarifyLoading(false);
        }
    };

    return (
        <div
            className="modal-backdrop"
            role="dialog"
            aria-modal="true"
            aria-label={item.title}
            onClick={e => e.target === e.currentTarget && onClose()}
        >
            <div className="modal">
                <header className="modal-header">
                    <h2 className="modal-title">{item.title}</h2>
                    <button id="modal-close-btn" className="btn modal-close" onClick={onClose} aria-label="Close">✕</button>
                </header>

                {/* Tabs */}
                <div className="sidebar-tabs" style={{ marginBottom: 16, borderRadius: 8 }}>
                    {(['details', 'clarify', 'research'] as Tab[]).map(t => (
                        <button
                            key={t}
                            id={`modal-tab-${t}`}
                            className={`sidebar-tab ${tab === t ? 'active' : ''}`}
                            onClick={() => setTab(t)}
                        >
                            {t === 'details' ? '📌 Detail' : t === 'clarify' ? '💡 Clarify' : '🔬 Research'}
                        </button>
                    ))}
                </div>

                {tab === 'details' && (
                    <>
                        <div className="modal-section">
                            <p><strong>Type:</strong> {item.type} &nbsp;|&nbsp; <strong>State:</strong> {item.state}</p>
                        </div>
                        {item.tags.length > 0 && (
                            <div className="modal-section">
                                <h4>Tags</h4>
                                <div className="gap-4">
                                    {item.tags.map(t => <span key={t} className="tag">{t}</span>)}
                                </div>
                            </div>
                        )}
                        {item.source_url && (
                            <div className="modal-section">
                                <h4>Source</h4>
                                <a href={item.source_url} target="_blank" rel="noreferrer" style={{ color: 'var(--accent-research)', fontSize: '.82rem', wordBreak: 'break-all' }}>
                                    {item.source_url}
                                </a>
                            </div>
                        )}
                        {item.content && (
                            <div className="modal-section">
                                <h4>Research Briefing</h4>
                                <p className="research-result">{item.content}</p>
                            </div>
                        )}
                    </>
                )}

                {tab === 'clarify' && (
                    <>
                        <div className="modal-section">
                            <h4>What do you want to understand?</h4>
                            <textarea
                                id="clarify-textarea"
                                className="clarify-input"
                                placeholder="Paste a concept, paragraph, or term you don't understand…"
                                value={clarifyText}
                                onChange={e => setClarifyText(e.target.value)}
                            />
                            <button
                                id="clarify-submit-btn"
                                className="btn btn-primary"
                                onClick={handleClarify}
                                disabled={clarifyLoading || !clarifyText.trim()}
                            >
                                {clarifyLoading ? '⏳ Thinking…' : '💡 Clarify'}
                            </button>
                        </div>
                        {clarifyResult && (
                            <>
                                <div className="modal-section">
                                    <h4>Explanation</h4>
                                    <p>{clarifyResult.explanation}</p>
                                </div>
                                {clarifyResult.analogy && (
                                    <div className="modal-section">
                                        <h4>Analogy</h4>
                                        <p>{clarifyResult.analogy}</p>
                                    </div>
                                )}
                                {clarifyResult.prerequisite_gaps.length > 0 && (
                                    <div className="modal-section">
                                        <h4>Prerequisite Gaps</h4>
                                        <div className="gap-4">
                                            {clarifyResult.prerequisite_gaps.map(g => (
                                                <span key={g} className="tag" style={{ background: 'rgba(224,64,251,.12)', color: 'var(--accent-clarify)', borderColor: 'rgba(224,64,251,.3)' }}>{g}</span>
                                            ))}
                                        </div>
                                    </div>
                                )}
                            </>
                        )}
                    </>
                )}

                {tab === 'research' && (
                    <div className="modal-section">
                        {item.content
                            ? <><h4>Briefing</h4><p className="research-result">{item.content}</p></>
                            : <p style={{ color: 'var(--text-2)', fontSize: '.85rem' }}>Move this card to <strong>In Progress</strong> to trigger the Deep Research Agent. The briefing will appear here when complete.</p>
                        }
                    </div>
                )}
            </div>
        </div>
    );
}
