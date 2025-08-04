import React, { useState } from 'react';

const AIFeatures: React.FC = () => {
  const [context, setContext] = useState('');
  const [question, setQuestion] = useState('');
  const [qaAnswer, setQaAnswer] = useState('');

  const [summaryInput, setSummaryInput] = useState('');
  const [summaryResult, setSummaryResult] = useState('');

  const [translateInput, setTranslateInput] = useState('');
  const [targetLang, setTargetLang] = useState('es');
  const [translationResult, setTranslationResult] = useState('');

  const [ttsInput, setTtsInput] = useState('');
  const [ttsAudioUrl, setTtsAudioUrl] = useState('');

  const [imageUrl, setImageUrl] = useState('');
  const [detectResult, setDetectResult] = useState<any>(null);

  const handleQaSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context, question })
      });
      const data = await res.json();
      setQaAnswer(data.answer || JSON.stringify(data));
    } catch (err) {
      setQaAnswer('Error performing QA');
    }
  };

  const handleSummarizeSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/summarize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: summaryInput })
      });
      const data = await res.json();
      setSummaryResult(data.summary || JSON.stringify(data));
    } catch (err) {
      setSummaryResult('Error performing summarization');
    }
  };

  const handleTranslateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: translateInput, target_lang: targetLang })
      });
      const data = await res.json();
      setTranslationResult(data.translation || JSON.stringify(data));
    } catch (err) {
      setTranslationResult('Error performing translation');
    }
  };

  const handleTtsSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/tts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: ttsInput })
      });
      const data = await res.json();
      setTtsAudioUrl(data.audio_url);
    } catch (err) {
      setTtsAudioUrl('');
    }
  };

  const handleDetectSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/detect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_url: imageUrl })
      });
      const data = await res.json();
      setDetectResult(data);
    } catch (err) {
      setDetectResult('Error performing detection');
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h1>AI Features</h1>

      <section style={{ marginBottom: '1rem' }}>
        <h2>Question Answering</h2>
        <form onSubmit={handleQaSubmit}>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Context text"
            rows={3}
            style={{ width: '100%' }}
          />
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Question"
            style={{ width: '100%', marginTop: '0.5rem' }}
          />
          <button type="submit" style={{ marginTop: '0.5rem' }}>Ask</button>
        </form>
        {qaAnswer && <p><strong>Answer:</strong> {qaAnswer}</p>}
      </section>

      <section style={{ marginBottom: '1rem' }}>
        <h2>Summarization</h2>
        <form onSubmit={handleSummarizeSubmit}>
          <textarea
            value={summaryInput}
            onChange={(e) => setSummaryInput(e.target.value)}
            placeholder="Enter text to summarize"
            rows={3}
            style={{ width: '100%' }}
          />
          <button type="submit" style={{ marginTop: '0.5rem' }}>Summarize</button>
        </form>
        {summaryResult && <p><strong>Summary:</strong> {summaryResult}</p>}
      </section>

      <section style={{ marginBottom: '1rem' }}>
        <h2>Translation</h2>
        <form onSubmit={handleTranslateSubmit}>
          <textarea
            value={translateInput}
            onChange={(e) => setTranslateInput(e.target.value)}
            placeholder="Enter text to translate"
            rows={3}
            style={{ width: '100%' }}
          />
          <input
            type="text"
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
            placeholder="Target language code (e.g. es, fr)"
            style={{ width: '100%', marginTop: '0.5rem' }}
          />
          <button type="submit" style={{ marginTop: '0.5rem' }}>Translate</button>
        </form>
        {translationResult && <p><strong>Translation:</strong> {translationResult}</p>}
      </section>

      <section style={{ marginBottom: '1rem' }}>
        <h2>Text to Speech</h2>
        <form onSubmit={handleTtsSubmit}>
          <textarea
            value={ttsInput}
            onChange={(e) => setTtsInput(e.target.value)}
            placeholder="Enter text for TTS"
            rows={2}
            style={{ width: '100%' }}
          />
          <button type="submit" style={{ marginTop: '0.5rem' }}>Generate Audio</button>
        </form>
        {ttsAudioUrl && (
          <audio controls style={{ marginTop: '0.5rem' }}>
            <source src={ttsAudioUrl} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        )}
      </section>

      <section style={{ marginBottom: '1rem' }}>
        <h2>Image Detection</h2>
        <form onSubmit={handleDetectSubmit}>
          <input
            type="text"
            value={imageUrl}
            onChange={(e) => setImageUrl(e.target.value)}
            placeholder="Image URL"
            style={{ width: '100%' }}
          />
          <button type="submit" style={{ marginTop: '0.5rem' }}>Detect</button>
        </form>
        {detectResult && (
          <pre style={{ backgroundColor: '#f5f5f5', padding: '0.5rem' }}>
            {JSON.stringify(detectResult, null, 2)}
          </pre>
        )}
      </section>
    </div>
  );
};

export default AIFeatures;
