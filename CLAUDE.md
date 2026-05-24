# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A fully local RAG (Retrieval-Augmented Generation) pipeline for GIS knowledge with two interfaces:
- **CLI** (`rag_chat.py`) — terminal chat interface
- **Web UI** (`chatbot_ui/`) — React 19 + Vite frontend with a collapsible chat widget, backed by a FastAPI REST API (`chatbot_api/`)

No external API calls — embeddings run via a local sentence-transformers model, retrieval via ChromaDB, and generation via Ollama (phi3).

## First-Time Setup

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# 1. Download embedding model (one-time)
python get_model.py

# 2. Ingest documents into vector store
python rag_ingest.py

# 3a. Start CLI chat
python rag_chat.py

# 3b. OR start the web UI (two terminals)
.\venv\Scripts\python.exe -m uvicorn chatbot_api.main:app --reload --port 8000
cd chatbot_ui && npm run dev   # open http://localhost:5173
```

After adding or changing documents in `./documents/`, re-run `python rag_ingest.py` to rebuild the index.

## Architecture

| Component | Implementation | Config |
|-----------|---------------|--------|
| Embedding model | `all-MiniLM-L6-v2` (sentence-transformers), stored locally at `./models/all-MiniLM-L6-v2` | `MODEL_DIR` in `chatbot_api/config.py` |
| Vector store | ChromaDB persistent client at `./chroma_db/`, collection `gis_knowledge`, cosine similarity | `CHROMA_DIR`, `COLLECTION_NAME` in `chatbot_api/config.py` |
| LLM | Ollama `phi3` — must be running separately (`ollama serve`) | `OLLAMA_MODEL` in `chatbot_api/config.py` |
| Documents | `.md`, `.txt`, `.markdown`, `.text` files under `./documents/` | `SUPPORTED_EXTENSIONS` in `chatbot_api/config.py` |
| REST API | FastAPI at `http://localhost:8000` with SSE streaming | `chatbot_api/main.py` |
| Frontend | React 19 + Vite at `http://localhost:5173`, proxies `/api` to port 8000 | `chatbot_ui/` |

## Project Structure

```
gis-rag-chatbot/
├── chatbot_api/            # FastAPI backend
│   ├── config.py           # All shared constants (absolute paths)
│   ├── rag_core.py         # retrieve(), ask(), ask_stream()
│   ├── session.py          # In-memory session store
│   └── main.py             # FastAPI app + endpoints
├── chatbot_ui/             # React + Vite frontend
│   ├── vite.config.js      # Proxies /api → localhost:8000
│   └── src/
│       ├── pages/Home.jsx      # Landing page
│       └── components/
│           ├── ChatWidget.jsx  # Collapsible FAB (bottom-right)
│           └── ChatWindow.jsx  # Chat messages + SSE streaming
├── documents/              # Knowledge base source files
├── models/                 # Local embedding model
├── chroma_db/              # ChromaDB vector store
├── get_model.py            # One-time model download
├── rag_ingest.py           # Document ingestion (imports chatbot_api.config)
├── rag_chat.py             # CLI chat wrapper (imports chatbot_api.rag_core)
└── requirements.txt
```

## Shared Config (`chatbot_api/config.py`)

All constants live here — both `rag_chat.py` and `rag_ingest.py` import from it. Paths are computed as absolute using `Path(__file__).resolve().parent.parent` so they work regardless of working directory.

## Chunking Strategy (`rag_ingest.py`)

Documents are split first by markdown headers (`#`–`####`), then by character count if a section exceeds `CHUNK_SIZE` (500 chars) with `CHUNK_OVERLAP` (100 chars, approximated as `CHUNK_OVERLAP // 5` words carried forward). Each chunk stores `source` (relative path) and `header` (section title) metadata.

## Retrieval (`chatbot_api/rag_core.py`)

- Retrieves `TOP_K = 5` chunks per query using cosine similarity
- Filters out chunks below `SIMILARITY_THRESHOLD = 0.3` (similarity = `1 - distance/2` since ChromaDB cosine distance ∈ [0, 2])
- Keeps last 6 chat exchanges in context window for multi-turn conversation
- System prompt is rebuilt on every turn with freshly retrieved context

## API Endpoints (`chatbot_api/main.py`)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Returns status and chunk count |
| POST | `/api/chat` | SSE streaming chat — body: `{session_id, message}` |
| POST | `/api/chat/clear` | Clear session history — body: `{session_id}` |
| POST | `/api/chat/reload` | Reload ChromaDB collection |

SSE event types: `token` (streamed text), `sources` (chunk metadata), `done`.

## SSE Streaming Note

Run uvicorn with `python -m uvicorn` (not the `.exe` launcher) to avoid stale venv path issues:

```powershell
.\venv\Scripts\python.exe -m uvicorn chatbot_api.main:app --reload --port 8000
```

## CLI Chat Commands

| Command | Effect |
|---------|--------|
| `sources` | Show chunks used in the last answer |
| `clear` | Wipe conversation history |
| `reload` | Reconnect to vector store without restarting |
| `exit` | Quit |

## External Dependency: Ollama

Ollama must be installed and the `phi3` model pulled before running either interface:

```powershell
ollama pull phi3
ollama serve   # if not already running as a service
```
