
import React, { useState, useRef, useEffect } from 'react';
import './App.css';

const QUICK_QUERIES = [
  "Explain the Phonetic Alphabet",
  "Explain the Q-code: What is QTE",
  "Procedures for Radio Failure (7600)",
  "What does Roger actually mean",
  "Standard phraseology for Line Up and Wait",
  "What is a METAR? report",
  "What is QDM and QDR?",
  "Difference between Roger and Wilco"

];

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'model',
      content: "WELCOME TO ATC CHATBOT.\nI am your specialized resource for Air Traffic Control operations and safety protocols. Whether you are a flight professional or an aviation enthusiast, I am here to assist with ICAO standard phraseology, aircraft separation rules, emergency procedures, and airspace regulations.\nHow can I assist you? — OVER.",
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (text) => {
    const userText = (text || input).trim();
    if (!userText || loading) return;

    setMessages(prev => [...prev, { role: 'user', content: userText }]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          message: userText, 
          history: messages.map(m => ({ role: m.role, content: m.content })) 
        }),
      });

      if (!res.ok) throw new Error(`HTTP Error: ${res.status}`);

      const data = await res.json();
      
      // Safety check for empty responses (prevents the issue in image_00a9a2.png)
      if (!data.reply || data.reply.trim() === "") {
        throw new Error("The advisory system returned an empty response. Check API logs.");
      }

      setMessages(prev => [...prev, { role: 'model', content: data.reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { 
        role: 'model', 
        content: `[SYSTEM FAULT] COMMUNICATION FAILURE.\nDetails: ${err.message}\nEnsure your local backend is running at http://127.0.0.1:8000` 
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="header-brand">
          <div className="logo-icon">📡</div>
          <div className="header-title">ATC CHATBOT</div>
        </div>
        <div className="status-badge">
          <span className="live-dot"></span> LIVE
        </div>
      </header>

      <main className="chat-area">
        {messages.map((msg, i) => (
          <div key={i} className={`message-row ${msg.role === 'user' ? 'user' : 'atc'}`}>
            <div className={`bubble ${msg.role === 'user' ? 'user-bubble' : 'atc-bubble'} ${msg.content.includes('[SYSTEM FAULT]') ? 'fault' : ''}`}>
              <div className="message-content">{msg.content}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="message-row atc">
            <div className="bubble atc-bubble">
              <div style={{ fontStyle: 'italic', fontSize: '0.85rem' }}>TRANSMITTING...</div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </main>

      <footer className="footer-container">
        <div className="suggestions-box">
          {QUICK_QUERIES.map((q) => (
            <button key={q} className="chip" onClick={() => sendMessage(q)}>
              {q}
            </button>
          ))}
        </div>
        <div className="input-group">
          <input
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="State your query..."
          />
          <button className="send-btn" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
            SEND
          </button>
        </div>
      </footer>
    </div>
  );
}

export default App;