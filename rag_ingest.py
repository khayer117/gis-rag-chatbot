import os
import re
import chromadb
from sentence_transformers import SentenceTransformer

from chatbot_api.config import (
    DOCS_DIR, CHROMA_DIR, MODEL_DIR, COLLECTION_NAME,
    CHUNK_SIZE, CHUNK_OVERLAP, SUPPORTED_EXTENSIONS,
)


def chunk_by_headers(text, source_file):
    """
    Smart chunking: split by markdown headers first,
    then by size if sections are too long.
    """
    chunks = []

    sections = re.split(r'\n(?=#{1,4}\s)', text)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        header_match = re.match(r'^(#{1,4})\s+(.+)', section)
        header = header_match.group(2) if header_match else ""

        if len(section) <= CHUNK_SIZE:
            chunks.append({
                "text": section,
                "source": source_file,
                "header": header,
            })
        else:
            words = section.split()
            current_chunk = []
            current_length = 0

            for word in words:
                current_chunk.append(word)
                current_length += len(word) + 1

                if current_length >= CHUNK_SIZE:
                    chunk_text = " ".join(current_chunk)
                    chunks.append({
                        "text": chunk_text,
                        "source": source_file,
                        "header": header,
                    })
                    overlap_words = current_chunk[-CHUNK_OVERLAP // 5:]
                    current_chunk = overlap_words
                    current_length = sum(len(w) + 1 for w in current_chunk)

            if current_chunk:
                chunk_text = " ".join(current_chunk)
                if len(chunk_text.strip()) > 50:
                    chunks.append({
                        "text": chunk_text,
                        "source": source_file,
                        "header": header,
                    })

    return chunks


def load_documents(docs_dir):
    """Load all supported files from the documents directory."""
    all_chunks = []

    for root, dirs, files in os.walk(docs_dir):
        for filename in sorted(files):
            ext = os.path.splitext(filename)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS:
                continue

            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, docs_dir)

            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_by_headers(text, relative_path)
            all_chunks.extend(chunks)
            print(f"  Loaded: {relative_path} ({len(chunks)} chunks)")

    return all_chunks


def main():
    print("=" * 50)
    print("GIS RAG — Document Ingestion")
    print("=" * 50)

    print("\nLoading embedding model...")
    embedder = SentenceTransformer(MODEL_DIR)

    print(f"\nLoading documents from: {DOCS_DIR}")
    chunks = load_documents(DOCS_DIR)
    print(f"\nTotal chunks: {len(chunks)}")

    if not chunks:
        print("No documents found! Add .md or .txt files to ./documents/")
        return

    print("\nBuilding vector store...")
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts, show_progress_bar=True).tolist()

    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=texts,
        embeddings=embeddings,
        metadatas=[{"source": c["source"], "header": c["header"]} for c in chunks],
    )

    print(f"\nDone! {len(chunks)} chunks stored in {CHROMA_DIR}")
    print("You can now run: python rag_chat.py")


if __name__ == "__main__":
    main()
