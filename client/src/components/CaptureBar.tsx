import { useState } from 'react';
import type { Item } from '../types';
import { api } from '../services/api';

interface Props {
    onCapture: (item: Item) => void;
}

export default function CaptureBar({ onCapture }: Props) {
    const [value, setValue] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const isUrl = (s: string) => /^https?:\/\//.test(s.trim());

    const submit = async () => {
        if (!value.trim()) return;
        setLoading(true);
        setError('');
        try {
            const item = await api.capture(
                isUrl(value) ? { url: value.trim() } : { raw_text: value.trim() }
            );
            onCapture(item);
            setValue('');
        } catch (e) {
            setError(e instanceof Error ? e.message : 'Capture failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <form
            className="capture-form"
            onSubmit={e => { e.preventDefault(); submit(); }}
        >
            <input
                id="capture-input"
                type="text"
                placeholder="Drop a URL, note, or question…"
                value={value}
                onChange={e => { setValue(e.target.value); setError(''); }}
                aria-label="Capture input"
                disabled={loading}
            />
            <button
                id="capture-btn"
                type="submit"
                className="btn btn-primary"
                disabled={loading || !value.trim()}
                aria-label="Capture"
            >
                {loading ? '⏳' : '⚡ Capture'}
            </button>
            {error && <span style={{ color: '#ff5555', fontSize: '.75rem', alignSelf: 'center' }}>{error}</span>}
        </form>
    );
}
