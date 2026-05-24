# GIS RAG Chatbot

A fully **local** Retrieval-Augmented Generation (RAG) pipeline for GIS knowledge with two interfaces — a terminal CLI and a React web UI. No external API calls: embeddings, retrieval, and generation all run on your machine.

## How It Works

```
Your Question
     │
     ▼
Embed query (all-MiniLM-L6-v2, local)
     │
     ▼
ChromaDB vector search → top-5 relevant chunks
     │
     ▼
Build prompt with context + conversation history
     │
     ▼
Ollama (phi3) → streamed answer + source references
```

## Prerequisites

- Python 3.10+
- Node.js 18+ (for the web UI)
- [Ollama](https://ollama.com) installed and running

```powershell
ollama pull phi3
ollama serve   # skip if already running as a service
```

## Setup

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd chatbot_ui
npm install
cd ..
```

## First-Time Initialization

```powershell
# 1. Download the embedding model (~90 MB, one-time)
python get_model.py

# 2. Ingest documents into the vector store
python rag_ingest.py
```

After adding or changing files in `./documents/`, re-run step 2 to rebuild the index.

## Running — CLI Interface

```powershell
python rag_chat.py
```

| Command | Effect |
|---------|--------|
| `sources` | Show the chunks used to generate the last answer |
| `clear` | Wipe conversation history |
| `reload` | Reconnect to the vector store without restarting |
| `exit` | Quit |

## Running — Web UI

Start the backend and frontend in two separate terminals:

```powershell
# Terminal 1 — FastAPI backend (from project root, venv active)
.\venv\Scripts\python.exe -m uvicorn chatbot_api.main:app --reload --port 8000

# Terminal 2 — React frontend
cd chatbot_ui
npm run dev
```

Open **http://localhost:5173** — click the chat button in the bottom-right corner.

The web UI features:
- Collapsible chat widget (bottom-right corner)
- Token-by-token streaming responses
- Source document pills below each answer (click to expand preview)
- Per-session conversation history

## Adding Knowledge

Drop `.md`, `.txt`, `.markdown`, or `.text` files into `./documents/`, then re-ingest:

```powershell
python rag_ingest.py
```

Documents are split by markdown headers, then by character count for long sections (500-char chunks, 100-char overlap), stored with source path and section metadata.

## API Endpoints

The FastAPI backend exposes:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Status and chunk count |
| POST | `/api/chat` | Streaming SSE chat — `{session_id, message}` |
| POST | `/api/chat/clear` | Clear session history — `{session_id}` |
| POST | `/api/chat/reload` | Reload ChromaDB without restart |

## Architecture

| Component | Implementation |
|-----------|---------------|
| Embedding model | `all-MiniLM-L6-v2` (sentence-transformers), stored at `./models/` |
| Vector store | ChromaDB persistent client at `./chroma_db/`, cosine similarity |
| LLM | Ollama `phi3` (runs locally) |
| Backend API | FastAPI with SSE streaming (`chatbot_api/`) |
| Frontend | React 19 + Vite (`chatbot_ui/`) |
| Documents | `.md` / `.txt` files under `./documents/` |

## Project Structure

```
gis-rag-chatbot/
├── chatbot_api/            # FastAPI backend
│   ├── config.py           # Shared constants and paths
│   ├── rag_core.py         # Core RAG logic (retrieve, ask, streaming)
│   ├── session.py          # In-memory session store
│   └── main.py             # API endpoints
├── chatbot_ui/             # React + Vite frontend
│   └── src/
│       ├── pages/Home.jsx      # Landing page
│       └── components/
│           ├── ChatWidget.jsx  # Collapsible chat button
│           └── ChatWindow.jsx  # Chat interface with streaming
├── documents/              # Knowledge base source files
├── models/                 # Local embedding model
├── chroma_db/              # Vector store (auto-created)
├── get_model.py            # One-time model download
├── rag_ingest.py           # Document ingestion
├── rag_chat.py             # CLI chat interface
└── requirements.txt
```

## License

MIT
