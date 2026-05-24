from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from chatbot_api.rag_core import load_embedder, get_collection, ask

console = Console()


def initialize():
    """Load embedding model and connect to vector store."""
    console.print("\n[dim]Loading embedding model...[/dim]")
    embedder = load_embedder()

    console.print("[dim]Connecting to vector store...[/dim]")
    collection = get_collection()

    doc_count = collection.count()
    console.print(f"[dim]Knowledge base: {doc_count} chunks loaded[/dim]\n")

    return embedder, collection


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

        with console.status("[dim]Thinking...[/dim]"):
            answer, last_chunks, chat_history = ask(
                question, embedder, collection, chat_history
            )

        console.print()
        console.print("[bold green]Assistant:[/bold green]")
        console.print(Markdown(answer))

        if last_chunks:
            sources = set(c["source"] for c in last_chunks)
            console.print(
                f"\n[dim]Sources: {', '.join(sources)} "
                f"— type 'sources' for details[/dim]"
            )
        console.print()


if __name__ == "__main__":
    main()
