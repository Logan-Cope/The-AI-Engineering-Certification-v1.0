"""The codebase concierge: a read-only Claude Agent SDK agent behind one function."""

import asyncio
import logging
import os
from pathlib import Path

from claude_agent_sdk import (
    ClaudeAgentOptions,
    SystemMessage,
    create_sdk_mcp_server,
    query,
    tool,
)

log = logging.getLogger("concierge.tools")

TARGET_REPO = os.environ.get("TARGET_REPO", str(Path.cwd()))
MAX_TURNS = int(os.environ.get("MAX_TURNS", "25"))

SYSTEM_PROMPT = (
    "You are a concierge for the repository at the working directory you were given. "
    "Answer questions about this codebase using your tools rather than guessing. "
    "Be concise: a few sentences or a short list. Cite the file paths you relied on. "
    "If the repo does not contain the answer, say so plainly instead of inventing one."
)

# conversation_id (from the browser) -> session_id (from the SDK)
_sessions: dict[str, str] = {}


def _inside_target(file_path: str) -> Path:
    resolved = (Path(TARGET_REPO) / file_path).resolve()
    if not resolved.is_relative_to(Path(TARGET_REPO).resolve()):
        raise ValueError("path escapes the target repo")
    return resolved


@tool("count_lines", "Count the lines in a file, relative to the repo root", {"file_path": str})
async def count_lines(args):
    log.info("TOOL count_lines %s", args["file_path"])
    path = _inside_target(args["file_path"])
    n = sum(1 for _ in path.open(encoding="utf-8", errors="replace"))
    return {"content": [{"type": "text", "text": f"{args['file_path']}: {n} lines"}]}


@tool(
    "git_log",
    "Recent git commits in the repo. Optionally filter to commits touching a path.",
    {"limit": int, "path": str},
)
async def git_log(args):
    log.info("TOOL git_log limit=%s path=%s", args.get("limit"), args.get("path"))
    limit = min(int(args.get("limit") or 10), 50)
    cmd = ["git", "log", f"-{limit}", "--date=short", "--format=%h %ad %an: %s"]
    if args.get("path"):
        cmd += ["--", str(_inside_target(args["path"]).relative_to(Path(TARGET_REPO).resolve()))]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=TARGET_REPO,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    text = stdout.decode() if proc.returncode == 0 else f"git log failed: {stderr.decode()}"
    return {"content": [{"type": "text", "text": text or "no commits found"}]}


concierge_tools = create_sdk_mcp_server(
    name="concierge", version="1.0.0", tools=[count_lines, git_log]
)


def _options(conversation_id: str | None) -> ClaudeAgentOptions:
    return ClaudeAgentOptions(
        system_prompt=SYSTEM_PROMPT,
        cwd=TARGET_REPO,
        allowed_tools=[
            "Read",
            "Glob",
            "Grep",
            "mcp__concierge__count_lines",
            "mcp__concierge__git_log",
        ],
        mcp_servers={"concierge": concierge_tools},
        permission_mode="default",
        max_turns=MAX_TURNS,
        resume=_sessions.get(conversation_id) if conversation_id else None,
    )


async def answer(message: str, conversation_id: str | None = None) -> str:
    """The seam. This is the function the echo stub used to be."""
    reply = ""
    async for msg in query(prompt=message, options=_options(conversation_id)):
        if isinstance(msg, SystemMessage) and msg.subtype == "init":
            if conversation_id:
                _sessions[conversation_id] = msg.data["session_id"]
        if hasattr(msg, "result"):
            reply = msg.result
    return reply or "The agent finished without producing an answer. Try rephrasing."
