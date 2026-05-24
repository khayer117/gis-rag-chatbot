import json
from typing import List, Dict, Generator

import chromadb
from sentence_transformers import SentenceTransformer
from ollama import chat

from chatbot_api.config import (
    MODEL_DIR, CHROMA_DIR, COLLECTION_NAME, OLLAMA_MODEL,
    TOP_K, SIMILARITY_THRESHOLD, SYSTEM_PROMPT,
)


def load_embedder() -> SentenceTransformer:
    return SentenceTransformer(MODEL_DIR)


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return client.get_collection(COLLECTION_NAME)


def retrieve(query: str, embedder, collection) -> List[Dict]:
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=TOP_K,
        include=["documents", "metadatas", "distances"],
    )
    chunks = []
    for doc, meta, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        similarity = 1 - (distance / 2)
        if similarity >= SIMILARITY_THRESHOLD:
            chunks.append({
                "text": doc,
                "source": meta["source"],
                "header": meta.get("header", ""),
                "similarity": similarity,
            })
    return chunks


def ask(question: str, embedder, collection, chat_history: list):
    """Non-streaming response for CLI use. Returns (answer, chunks, updated_history)."""
    chunks = retrieve(question, embedder, collection)

    if not chunks:
        return (
            "I couldn't find any relevant information in my knowledge base for that question.",
            [],
            chat_history,
        )

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source_info = f"[Source: {chunk['source']}"
        if chunk["header"]:
            source_info += f" > {chunk['header']}"
        source_info += f" | Relevance: {chunk['similarity']:.0%}]"
        context_parts.append(f"--- Chunk {i} {source_info} ---\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(context=context)}]
    for h in chat_history[-6:]:
        messages.append(h)
    messages.append({"role": "user", "content": question})

    response = chat(model=OLLAMA_MODEL, messages=messages)
    answer = response.message.content

    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": answer})

    return answer, chunks, chat_history


def ask_stream(question: str, embedder, collection, session_data: dict) -> Generator:
    """Streaming response for API use. Yields SSE strings and mutates session_data."""
    chunks = retrieve(question, embedder, collection)

    if not chunks:
        no_info = "I couldn't find any relevant information in my knowledge base for that question."
        yield f'data: {json.dumps({"type": "token", "content": no_info})}\n\n'
        session_data["history"].append({"role": "user", "content": question})
        session_data["history"].append({"role": "assistant", "content": no_info})
        session_data["last_chunks"] = []
        yield f'data: {json.dumps({"type": "sources", "chunks": []})}\n\n'
        yield f'data: {json.dumps({"type": "done"})}\n\n'
        return

    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source_info = f"[Source: {chunk['source']}"
        if chunk["header"]:
            source_info += f" > {chunk['header']}"
        source_info += f" | Relevance: {chunk['similarity']:.0%}]"
        context_parts.append(f"--- Chunk {i} {source_info} ---\n{chunk['text']}")
    context = "\n\n".join(context_parts)

    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(context=context)}]
    for h in session_data["history"][-6:]:
        messages.append(h)
    messages.append({"role": "user", "content": question})

    full_answer = []
    stream = chat(model=OLLAMA_MODEL, messages=messages, stream=True)
    for response_chunk in stream:
        token = response_chunk.message.content
        if token:
            full_answer.append(token)
            yield f'data: {json.dumps({"type": "token", "content": token})}\n\n'

    answer = "".join(full_answer)
    session_data["history"].append({"role": "user", "content": question})
    session_data["history"].append({"role": "assistant", "content": answer})
    session_data["last_chunks"] = chunks

    source_payload = [
        {
            "source": c["source"],
            "header": c["header"],
            "similarity": round(c["similarity"], 3),
            "preview": c["text"][:300] + ("..." if len(c["text"]) > 300 else ""),
        }
        for c in chunks
    ]
    yield f'data: {json.dumps({"type": "sources", "chunks": source_payload})}\n\n'
    yield f'data: {json.dumps({"type": "done"})}\n\n'
