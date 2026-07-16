# Codebase Concierge

A chat web app that answers questions about another repository, using the Claude Agent SDK.

## Run and test

```bash
uv run uvicorn app:app --reload --port 8000     # http://localhost:8000
curl -s localhost:8000/api/health
curl -s localhost:8000/api/chat -H 'Content-Type: application/json' \
  -d '{"message":"what does this repo do?","conversation_id":"test"}'
```

Requires a `.env` (copy `.env.example`). `TARGET_REPO` is the repo the agent reads.
Auth falls back to the local Claude Code login when `ANTHROPIC_API_KEY` is unset.

## Architecture

`agent.py::answer()` is the seam. It is the only place that talks to the SDK, and it was
an echo stub before the agent existed. `app.py` knows nothing about Claude.

The agent is read-only by construction: `allowed_tools` is Read, Glob, Grep plus the two
in-process MCP tools, and there is no human at the permission gate on a server, so the
allowlist and `max_turns` are the gate.

Conversation memory is a `conversation_id -> session_id` dict in `agent.py`. It is in-memory
and dies with the process, which is fine for this project.

## Conventions

- Plain HTML/CSS/JS in `static/index.html`. No frontend framework, no build step.
- Custom tools go in `agent.py` with `@tool`, and must also be added to `allowed_tools`
  as `mcp__concierge__<name>`. Forgetting the allowlist is the usual bug.
- Never widen `allowed_tools` to a write or shell tool. That is the safety story.
