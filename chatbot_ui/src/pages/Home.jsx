import './Home.css'

const features = [
  {
    icon: '🗄️',
    title: 'Fully Local',
    desc: 'No external API calls. Embeddings, retrieval, and generation all run on your machine.',
  },
  {
    icon: '📄',
    title: 'Knowledge-Grounded',
    desc: 'Answers are generated strictly from your GIS document library — no hallucinations.',
  },
  {
    icon: '🔍',
    title: 'Source Transparency',
    desc: 'Every answer shows the exact document sections used, with relevance scores.',
  },
  {
    icon: '💬',
    title: 'Multi-turn Chat',
    desc: 'Maintains conversation context across multiple questions in the same session.',
  },
]

const stack = [
  { label: 'React 19', color: '#61dafb' },
  { label: 'FastAPI', color: '#009688' },
  { label: 'ChromaDB', color: '#f97316' },
  { label: 'Ollama / Phi-3', color: '#7c3aed' },
  { label: 'all-MiniLM-L6-v2', color: '#1a5276' },
]

export default function Home() {
  return (
    <div className="home">
      <header className="home-header">
        <div className="home-header-inner">
          <div className="home-logo">
            <span className="home-logo-icon">🌍</span>
            <span className="home-logo-text">GIS RAG Assistant</span>
          </div>
        </div>
      </header>

      <main>
        <section className="hero">
          <div className="hero-inner">
            <h1 className="hero-title">
              GIS Knowledge<br />
              <span className="hero-accent">AI Assistant</span>
            </h1>
            <p className="hero-desc">
              A fully local Retrieval-Augmented Generation system for Geographic
              Information Systems knowledge. Ask questions about GIS concepts,
              coordinate systems, spatial analysis, and more — powered entirely
              by your own documents.
            </p>
            <div className="hero-cta">
              <span className="hero-cta-hint">
                Click the chat button in the bottom-right corner to get started
              </span>
              <span className="hero-arrow">↘</span>
            </div>
          </div>
          <div className="hero-graphic">
            <div className="geo-grid">
              {Array.from({ length: 25 }).map((_, i) => (
                <div key={i} className="geo-cell" />
              ))}
            </div>
            <div className="geo-pin">📍</div>
          </div>
        </section>

        <section className="features">
          <div className="features-inner">
            <h2 className="section-title">How It Works</h2>
            <div className="feature-grid">
              {features.map((f) => (
                <div key={f.title} className="feature-card">
                  <span className="feature-icon">{f.icon}</span>
                  <h3 className="feature-title">{f.title}</h3>
                  <p className="feature-desc">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="pipeline">
          <div className="pipeline-inner">
            <h2 className="section-title">RAG Pipeline</h2>
            <div className="pipeline-steps">
              <div className="pipeline-step">
                <div className="step-num">1</div>
                <div className="step-label">Documents ingested &amp; chunked</div>
              </div>
              <div className="pipeline-arrow">→</div>
              <div className="pipeline-step">
                <div className="step-num">2</div>
                <div className="step-label">Embeddings stored in ChromaDB</div>
              </div>
              <div className="pipeline-arrow">→</div>
              <div className="pipeline-step">
                <div className="step-num">3</div>
                <div className="step-label">Query encoded &amp; top-K retrieved</div>
              </div>
              <div className="pipeline-arrow">→</div>
              <div className="pipeline-step">
                <div className="step-num">4</div>
                <div className="step-label">Phi-3 generates grounded answer</div>
              </div>
            </div>
          </div>
        </section>

        <section className="tech-stack">
          <div className="tech-inner">
            <h2 className="section-title">Tech Stack</h2>
            <div className="tech-badges">
              {stack.map((t) => (
                <span
                  key={t.label}
                  className="tech-badge"
                  style={{ borderColor: t.color, color: t.color }}
                >
                  {t.label}
                </span>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="home-footer">
        <p>GIS RAG Chatbot &mdash; Fully local AI &mdash; No data leaves your machine</p>
      </footer>
    </div>
  )
}
