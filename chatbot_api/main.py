from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from chatbot_api.rag_core import load_embedder, get_collection, ask_stream
from chatbot_api.session import get_session, clear_session

app = FastAPI(title="GIS RAG Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    app.state.embedder = load_embedder()
    app.state.collection = get_collection()


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ClearRequest(BaseModel):
    session_id: str


@app.get("/api/health")
async def health(request: Request):
    count = request.app.state.collection.count()
    return {"status": "ok", "chunks_count": count}


@app.post("/api/chat")
async def chat_endpoint(body: ChatRequest, request: Request):
    session = get_session(body.session_id)
    embedder = request.app.state.embedder
    collection = request.app.state.collection

    def generate():
        yield from ask_stream(body.message, embedder, collection, session)

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.post("/api/chat/clear")
async def clear_endpoint(body: ClearRequest):
    clear_session(body.session_id)
    return {"ok": True}


@app.post("/api/chat/reload")
async def reload_endpoint(request: Request):
    request.app.state.collection = get_collection()
    count = request.app.state.collection.count()
    return {"ok": True, "chunks": count}
