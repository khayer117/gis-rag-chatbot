import { useState, useRef, useEffect } from 'react'
import './chat.css'

function SourcePill({ chunk }) {
  const [expanded, setExpanded] = useState(false)
  const filename = chunk.source.split(/[\\/]/).pop()
  const pct = Math.round(chunk.similarity * 100)

  return (
    <div className="source-pill-wrapper">
      <button
        className="source-pill"
        onClick={() => setExpanded((v) => !v)}
        title="Click to expand source preview"
      >
        <span className="source-pill-icon">📄</span>
        <span className="source-pill-name">{filename}</span>
        {chunk.header && (
          <span className="source-pill-section">&rsaquo; {chunk.header}</span>
        )}
        <span className="source-pill-score">{pct}%</span>
      </button>
      {expanded && (
        <div className="source-preview">{chunk.preview}</div>
      )}
    </div>
  )
}

function Message({ msg }) {
  const isUser = msg.role === 'user'

  return (
    <div className={`msg-row ${isUser ? 'msg-row--user' : 'msg-row--assistant'}`}>
      {!isUser && (
        <div className="msg-avatar">AI</div>
      )}
      <div className={`msg-bubble ${isUser ? 'msg-bubble--user' : 'msg-bubble--assistant'}`}>
        {msg.content || <span className="msg-typing">▋</span>}
        {!isUser && msg.sources && msg.sources.length > 0 && (
          <div className="msg-sources">
            {msg.sources.map((chunk, i) => (
              <SourcePill key={i} chunk={chunk} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default function ChatWindow({ sessionId, onClose }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your GIS Assistant. Ask me anything about Geographic Information Systems, coordinate systems, spatial analysis, or your loaded documents.',
      sources: [],
    },
  ])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const bottomRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function handleSend() {
    const text = input.trim()
    if (!text || isStreaming) return

    setInput('')
    setIsStreaming(true)

    setMessages((prev) => [
      ...prev,
      { role: 'user', content: text },
      { role: 'assistant', content: '', sources: null },
    ])

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: text }),
      })

      if (!response.ok) {
        throw new Error(`API error ${response.status}`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const parts = buffer.split('\n\n')
        buffer = parts.pop()

        for (const part of parts) {
          if (!part.startsWith('data: ')) continue
          const event = JSON.parse(part.slice(6))

          if (event.type === 'token') {
            setMessages((prev) => {
              const updated = [...prev]
              const last = updated[updated.length - 1]
              updated[updated.length - 1] = { ...last, content: last.content + event.content }
              return updated
            })
          } else if (event.type === 'sources') {
            setMessages((prev) => {
              const updated = [...prev]
              updated[updated.length - 1] = {
                ...updated[updated.length - 1],
                sources: event.chunks,
              }
              return updated
            })
          } else if (event.type === 'done') {
            setIsStreaming(false)
          }
        }
      }
    } catch (err) {
      setMessages((prev) => {
        const updated = [...prev]
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: `Error: ${err.message}. Is the backend running?`,
          sources: [],
        }
        return updated
      })
      setIsStreaming(false)
    }

    inputRef.current?.focus()
  }

  async function handleClear() {
    await fetch('/api/chat/clear', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId }),
    })
    setMessages([
      {
        role: 'assistant',
        content: 'Conversation cleared. How can I help you?',
        sources: [],
      },
    ])
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="chat-window">
      <div className="chat-header">
        <div className="chat-header-left">
          <span className="chat-header-icon">🌍</span>
          <div>
            <div className="chat-header-title">GIS Assistant</div>
            <div className="chat-header-sub">Local RAG · Phi-3</div>
          </div>
        </div>
        <div className="chat-header-actions">
          <button className="chat-btn-icon" onClick={handleClear} title="Clear conversation">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="3 6 5 6 21 6" />
              <path d="M19 6l-1 14H6L5 6" />
              <path d="M10 11v6M14 11v6" />
            </svg>
          </button>
          <button className="chat-btn-icon" onClick={onClose} title="Close">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <Message key={i} msg={msg} />
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-bar">
        <textarea
          ref={inputRef}
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about GIS, coordinates, spatial data..."
          rows={1}
          disabled={isStreaming}
        />
        <button
          className="chat-send-btn"
          onClick={handleSend}
          disabled={isStreaming || !input.trim()}
          title="Send"
        >
          {isStreaming ? (
            <span className="chat-spinner" />
          ) : (
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
            </svg>
          )}
        </button>
      </div>
    </div>
  )
}
