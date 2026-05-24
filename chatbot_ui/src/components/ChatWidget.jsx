import { useState, useRef } from 'react'
import ChatWindow from './ChatWindow'
import './chat.css'

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const sessionId = useRef(crypto.randomUUID())

  return (
    <div className="chat-widget">
      {isOpen && (
        <ChatWindow
          sessionId={sessionId.current}
          onClose={() => setIsOpen(false)}
        />
      )}
      <button
        className={`chat-fab ${isOpen ? 'chat-fab--open' : ''}`}
        onClick={() => setIsOpen((v) => !v)}
        aria-label={isOpen ? 'Close chat' : 'Open GIS Assistant'}
        title={isOpen ? 'Close chat' : 'GIS Assistant'}
      >
        {isOpen ? (
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M20 2H4a2 2 0 0 0-2 2v18l4-4h14a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z" />
          </svg>
        )}
        {!isOpen && <span className="chat-fab-label">GIS Assistant</span>}
      </button>
    </div>
  )
}
