# Codebase Concierge

A chat web app powered by the Claude Agent SDK. Ask it questions about a repository and it
reads the actual files to answer, instead of guessing.

## Setup

```bash
cp .env.example .env      # point TARGET_REPO at the repo you want to ask about
uv sync
uv run uvicorn app:app --reload --port 8000
```

Open http://localhost:8000.

Auth: if `ANTHROPIC_API_KEY` is not set, the SDK uses your local Claude Code login.

## What it does

- `GET /` serves the chat page
- `POST /api/chat` takes `{"message": "...", "conversation_id": "..."}` and returns `{"reply": "..."}`
- Every message routes through `agent.py::answer()`, which calls the SDK's `query()`

The agent has five tools: the built-in Read, Glob and Grep, plus two custom ones defined
in `agent.py` as an in-process MCP server:

- `count_lines` — line count for a file
- `git_log` — recent commits, optionally filtered to a path

It has no write, edit or shell tool, so it cannot change anything in the target repo.
`max_turns` caps how long any one request can loop.

## Try it

- what does this repo do?
- what are its main dependencies?          (follow-up: sessions resume, so "its" resolves)
- what changed in the last week?           (forces git_log)
- how many lines is the biggest file in src?
