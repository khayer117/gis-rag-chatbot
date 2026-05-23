
import chromadb
from sentence_transformers import SentenceTransformer
from ollama import chat
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# ============================================================
# CONFIG
# ============================================================
CHROMA_DIR = "./chroma_db"
MODEL_DIR = "./models/all-MiniLM-L6-v2"
COLLECTION_NAME = "gis_knowledge"
OLLAMA_MODEL = "phi3"
TOP_K = 5                  # Number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.3  # Minimum relevance (0-1, higher = stricter)

SYSTEM_PROMPT = """You are a GIS (Geographic Information Systems) expert assistant.
Answer questions using ONLY the provided context from the knowledge base.

Rules:
- Base your answers strictly on the provided context
- If the context doesn't contain enough information, say so honestly
- Be specific and technical when appropriate
- Include code examples if relevant context contains them
- If asked about something outside the context, say "I don't have information about that in my knowledge base"

Context from knowledge base:
{context}
"""

# ============================================================
# SETUP
# ============================================================
console = Console()


def initialize():
    """Load embedding model and vector store."""
    console.print("\n[dim]Loading embedding model...[/dim]")
    embedder = SentenceTransformer(MODEL_DIR)

    console.print("[dim]Connecting to vector store...[/dim]")
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(COLLECTION_NAME)

    doc_count = collection.count()
    console.print(f"[dim]Knowledge base: {doc_count} chunks loaded[/dim]\n")

    return embedder, collection


def retrieve(query, embedder, collection):
    """Find the most relevant chunks for a query."""
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
        # ChromaDB cosine distance: 0 = identical, 2 = opposite
        similarity = 1 - (distance / 2)
        if similarity >= SIMILARITY_THRESHOLD:
            chunks.append({
                "text": doc,
                "source": meta["source"],
                "header": meta.get("header", ""),
                "similarity": similarity,
            })

    return chunks


def ask(question, embedder, collection, chat_history):
    """Retrieve context, build prompt, get LLM response."""

    # Retrieve relevant chunks
    chunks = retrieve(question, embedder, collection)

    if not chunks:
        return (
            "I couldn't find any relevant information in my knowledge base "
            "for that question.",
            [],
            chat_history,
        )

    # Build context string
    context_parts = []
    for i, chunk in enumerate(chunks, 1):
        source_info = f"[Source: {chunk['source']}"
        if chunk["header"]:
            source_info += f" > {chunk['header']}"
        source_info += f" | Relevance: {chunk['similarity']:.0%}]"
        context_parts.append(f"--- Chunk {i} {source_info} ---\n{chunk['text']}")

    context = "\n\n".join(context_parts)

    # Build messages with conversation history
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT.format(context=context)},
    ]

    # Add recent history (last 6 exchanges to stay within context window)
    for h in chat_history[-6:]:
        messages.append(h)

    messages.append({"role": "user", "content": question})

    # Call Ollama
    response = chat(
        model=OLLAMA_MODEL,
        messages=messages,
    )

    answer = response.message.content

    # Update history
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": answer})

    return answer, chunks, chat_history


# ============================================================
# MAIN CHAT LOOP
# ============================================================
def main():
    console.print(Panel.fit(
        "[bold green]GIS Knowledge Assistant[/bold green]\n"
        "[dim]Fully local RAG — Phi-3 + ChromaDB[/dim]\n\n"
        "Commands:\n"
        "  [bold]exit[/bold]      — Quit\n"
        "  [bold]sources[/bold]   — Show sources from last answer\n"
        "  [bold]clear[/bold]     — Clear conversation history\n"
        "  [bold]reload[/bold]    — Reload the knowledge base",
        title="Welcome",
    ))

    embedder, collection = initialize()
    chat_history = []
    last_chunks = []

    while True:
        try:
            question = console.input("[bold cyan]You:[/bold cyan] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not question:
            continue

        if question.lower() == "exit":
            console.print("[dim]Goodbye![/dim]")
            break

        if question.lower() == "sources":
            if last_chunks:
                console.print("\n[bold]Sources used in last answer:[/bold]")
                for i, chunk in enumerate(last_chunks, 1):
                    console.print(f"\n[yellow]--- Chunk {i} ---[/yellow]")
                    console.print(f"[dim]File: {chunk['source']}[/dim]")
                    if chunk["header"]:
                        console.print(f"[dim]Section: {chunk['header']}[/dim]")
                    console.print(f"[dim]Relevance: {chunk['similarity']:.0%}[/dim]")
                    preview = chunk["text"][:300]
                    if len(chunk["text"]) > 300:
                        preview += "..."
                    console.print(preview)
                console.print()
            else:
                console.print("[dim]No sources yet — ask a question first.[/dim]\n")
            continue

        if question.lower() == "clear":
            chat_history = []
            console.print("[dim]Conversation history cleared.[/dim]\n")
            continue

        if question.lower() == "reload":
            embedder, collection = initialize()
            console.print("[dim]Knowledge base reloaded.[/dim]\n")
            continue

        # Get answer
        with console.status("[dim]Thinking...[/dim]"):
            answer, last_chunks, chat_history = ask(
                question, embedder, collection, chat_history
            )

        # Display answer
        console.print()
        console.print("[bold green]Assistant:[/bold green]")
        console.print(Markdown(answer))

        # Show source hint
        if last_chunks:
            sources = set(c["source"] for c in last_chunks)
            console.print(
                f"\n[dim]Sources: {', '.join(sources)} "
                f"— type 'sources' for details[/dim]"
            )
        console.print()


if __name__ == "__main__":
    main()