# GIS RAG Chatbot

A fully **local** Retrieval-Augmented Generation (RAG) pipeline for GIS knowledge. No external API calls — embeddings run via a local sentence-transformers model, retrieval via ChromaDB, and generation via Ollama (Phi-3).

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
Build prompt with context
     │
     ▼
Ollama (phi3) → answer
```

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running

Pull the LLM before first run:

```powershell
ollama pull phi3
ollama serve   # skip if already running as a service
```

## Setup

```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install sentence-transformers chromadb ollama rich
```

## Usage

Run these three steps in order on first setup:

```powershell
# 1. Download the embedding model (~90 MB, one-time)
python get_model.py

# 2. Ingest documents into the vector store
python rag_ingest.py

# 3. Start the chat interface
python rag_chat.py
```

After adding or changing documents in `./documents/`, re-run step 2 to rebuild the index.

## Adding Knowledge

Drop `.md`, `.txt`, `.markdown`, or `.text` files into the `./documents/` folder, then run:

```powershell
python rag_ingest.py
```

The ingestion pipeline splits documents by markdown headers, then by character count for long sections (500-char chunks, 100-char overlap), and stores them with source and section metadata.

## Chat Commands

| Command | Effect |
|---------|--------|
| `sources` | Show the chunks used to generate the last answer |
| `clear` | Wipe conversation history |
| `reload` | Reconnect to the vector store without restarting |
| `exit` | Quit |

## Architecture

| Component | Implementation |
|-----------|---------------|
| Embedding model | `all-MiniLM-L6-v2` (sentence-transformers), stored at `./models/` |
| Vector store | ChromaDB persistent client at `./chroma_db/`, cosine similarity |
| LLM | Ollama `phi3` (runs locally) |
| Documents | `.md` / `.txt` files under `./documents/` |

**Retrieval details:** top-5 chunks per query, minimum similarity threshold of 0.3, last 6 chat turns kept in context for multi-turn conversation.

## Project Structure

```
gis-rag-chatbot/
├── documents/          # Your knowledge base files (add .md/.txt here)
├── models/             # Downloaded embedding model (created by get_model.py)
├── chroma_db/          # Vector store (created by rag_ingest.py)
├── get_model.py        # One-time model download script
├── rag_ingest.py       # Document ingestion and indexing
└── rag_chat.py         # Interactive chat interface
```

## License

MIT
