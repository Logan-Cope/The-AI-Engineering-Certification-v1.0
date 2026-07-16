"""FastAPI server: serves the chat UI and routes every message through the agent."""

import logging
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

from agent import TARGET_REPO, answer  # noqa: E402  (must load .env before reading it)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("concierge")

app = FastAPI(title="Codebase Concierge")
STATIC = Path(__file__).parent / "static"


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


@app.get("/")
async def index():
    return FileResponse(STATIC / "index.html")


@app.post("/api/chat")
async def chat(req: ChatRequest):
    log.info("chat: conversation=%s message=%r", req.conversation_id, req.message)
    try:
        reply = await answer(req.message, req.conversation_id)
    except Exception:
        log.exception("agent failed")
        reply = "Something went wrong on my end reading the repo. Try asking again."
    return {"reply": reply}


@app.get("/api/health")
async def health():
    return {"status": "ok", "target_repo": TARGET_REPO}
