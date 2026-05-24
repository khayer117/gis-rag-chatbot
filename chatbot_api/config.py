from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHROMA_DIR = str(ROOT / "chroma_db")
MODEL_DIR = str(ROOT / "models" / "all-MiniLM-L6-v2")
COLLECTION_NAME = "gis_knowledge"
OLLAMA_MODEL = "phi3"
TOP_K = 5
SIMILARITY_THRESHOLD = 0.3

DOCS_DIR = str(ROOT / "documents")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
SUPPORTED_EXTENSIONS = {".md", ".txt", ".markdown", ".text"}

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
