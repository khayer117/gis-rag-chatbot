# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Is

A fully local RAG (Retrieval-Augmented Generation) pipeline for GIS knowledge. No external API calls — embeddings run via a local sentence-transformers model, retrieval via ChromaDB, and generation via Ollama (phi3).

## Workflow

Run these steps in order on first setup:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# 1. Download embedding model (one-time)
python get_model.py

# 2. Ingest documents into vector store
python rag_rag_ingest.py

# 3. Start the chat interface
python rag_chat.py
```

After adding or changing documents in `./documents/`, re-run `python rag_rag_ingest.py` to rebuild the index (it deletes and recreates the ChromaDB collection).

## Architecture

| Component | Implementation | Config |
|-----------|---------------|--------|
| Embedding model | `all-MiniLM-L6-v2` (sentence-transformers), stored locally at `./models/all-MiniLM-L6-v2` | `MODEL_DIR` in both scripts |
| Vector store | ChromaDB persistent client at `./chroma_db/`, collection `gis_knowledge`, cosine similarity | `CHROMA_DIR`, `COLLECTION_NAME` |
| LLM | Ollama `phi3` — must be running separately (`ollama serve`) | `OLLAMA_MODEL` in `rag_chat.py` |
| Documents | `.md`, `.txt`, `.markdown`, `.text` files under `./documents/` | `SUPPORTED_EXTENSIONS` in `rag_ingest.py` |

## Chunking Strategy (`rag_ingest.py`)

Documents are split first by markdown headers (`#`–`####`), then by character count if a section exceeds `CHUNK_SIZE` (500 chars) with `CHUNK_OVERLAP` (100 chars, approximated as `CHUNK_OVERLAP // 5` words carried forward). Each chunk stores `source` (relative path) and `header` (section title) metadata.

## Retrieval (`rag_chat.py`)

- Retrieves `TOP_K = 5` chunks per query using cosine similarity
- Filters out chunks below `SIMILARITY_THRESHOLD = 0.3` (similarity = `1 - distance/2` since ChromaDB cosine distance ∈ [0, 2])
- Keeps last 6 chat exchanges in context window for multi-turn conversation
- System prompt is rebuilt on every turn with freshly retrieved context

## Chat Commands

| Command | Effect |
|---------|--------|
| `sources` | Show chunks used in the last answer |
| `clear` | Wipe conversation history |
| `reload` | Reconnect to vector store without restarting |
| `exit` | Quit |

## External Dependency: Ollama

Ollama must be installed and the `phi3` model pulled before running `rag_chat.py`:

```powershell
ollama pull phi3
ollama serve   # if not already running as a service
```
