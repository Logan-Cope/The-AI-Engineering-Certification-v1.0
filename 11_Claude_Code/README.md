<p align = "center" draggable="false" ><img src="https://github.com/AI-Maker-Space/LLM-Dev-101/assets/37101144/d1343317-fa2f-41e1-8af1-1dbb18399719"
     width="200px"
     height="auto"/>
</p>

<h1 align="center" id="heading">Session 11: Claude Code & the Claude Agent SDK</h1>

| 📰 Session Sheet | ⏺️ Recording | 🖼️ Slides | 👨‍💻 Repo | 📝 Homework | 📁 Feedback |
|:-----------------|:-------------|:----------|:----------|:------------|:------------|
| [Session 11: Claude Code & Claude Agent SDK ](https://github.com/AI-Maker-Space/The-AI-Engineering-Certification-v1.0/tree/main/00_Docs/Modules/11_Claude_Code) |[Recording!](https://us02web.zoom.us/rec/share/2I5HA6DwVFgmtyjPaq1SJDgkaVEuYZoWYyMCK8DOAZ99Zm6f7dTi0IGONXj6mRel.YHFzKF03mI5v6JAM) <br> passcode: `&Qhi!cf0`| [Session 11 Slides](https://canva.link/uw1cl42x84tm6zh) |You are here! <br><br> [Certification Challenge](https://github.com/AI-Maker-Space/The-AI-Engineering-Certification-v1.0/tree/main/00_Docs/Certification%20Challenge) | [Optional Session 11 Assignment](https://forms.gle/sAyr5BgBLTfgJV8EA) <br><br>  [Cert Challenge Submission Form](https://forms.gle/xtM9F38nfRKcdjH97)| [Feedback 7/7](https://forms.gle/oDrguLDNvva65mtM8) |

## Useful Resources

**Claude Code**
- [Claude Code Documentation](https://code.claude.com/docs) — official docs: setup, workflows, settings
- [Claude Code Quickstart](https://code.claude.com/docs/en/quickstart) — from install to first session
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) — Anthropic engineering guide

**Claude Agent SDK**
- [Agent SDK Overview](https://docs.anthropic.com/en/api/agent-sdk/overview) — what the SDK is and when to use it
- [Building Agents with the Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk) — Anthropic engineering deep dive

## Main Assignment

**Build a chat web app powered by the Claude Agent SDK** — and build it *with* Claude Code.

This session is markdown-only on purpose. There is no starter code and no notebook: every line of code in your final app will be written in collaboration with Claude Code. The session has one build arc across a single breakout room:

```text
you → Claude Code → chat app skeleton → wire in Agent SDK query()
      (FastAPI + chat UI, echo stub)      ├─ tools: Read / Glob / Grep
                                           └─ your custom tool
```

The finished product: a **codebase concierge** — a chat interface in the browser where an agent (with real tools) answers questions about any repository you point it at. In Session 10 you served models behind endpoints; today you serve an *agent* behind one.

Work through the three guides in order:

```text
01_Installing_Claude_Code.md   # install, authenticate, verify
02_Using_Claude_Code.md        # drive Claude Code; scaffold the chat app skeleton
03_Claude_Agent_SDK.md         # add the agent and connect it to your website
```

## Outline

### Breakout Room #1: Claude Code, the Agent SDK, and the Connection

- Task 1: Install Claude Code and authenticate ([guide](./01_Installing_Claude_Code.md))
- Task 2: Learn the loop — explore a repo you didn't write ([guide](./02_Using_Claude_Code.md))
- Task 3: Scaffold the chat app skeleton with Claude Code (plan → implement → verify)
- Task 4: Write the project's `CLAUDE.md`
- Question #1 and Question #2
- Task 5: Install the Agent SDK and run your first `query()` ([guide](./03_Claude_Agent_SDK.md))
- Task 6: Wire the agent into `/api/chat` — replace the echo stub
- Task 7: Conversation memory — resume sessions across messages
- Task 8: Give the agent a custom tool
- Question #3 and Question #4
- Activity #1: Level Up the Chat App

## Questions

### ❓ Question #1

While scaffolding in Task 3 you used **plan mode** before letting Claude Code write anything. Why does an agent that can execute shell commands need a permission system at all, and why is plan mode particularly valuable when starting a project from an empty directory?

#### ✅ Answer

An agent with shell access can do real and irreversible things. It can delete files, force push, spend money, or leak a secret into a log. It decides to do those things based on a probabilistic guess about what I meant, and it is confidently wrong often enough that I do not want the gap between it deciding and it happening to be zero. The permission system is that gap. It also lets me set trust per action instead of all or nothing, so reading files can be silent while anything destructive has to come ask me first.

Plan mode matters most on an empty directory because there is nothing there to check the work against. Normally I can read a diff, run the tests, or roll back to the last commit. In an empty folder there is no diff, no test suite, and no git history to undo to, so the first thing the agent writes becomes the thing everything else gets built on top of. The plan is the only artifact that exists before any of that is true. Reviewing it is how I catch a wrong architecture while changing it still costs nothing, instead of finding out after there are twenty files depending on it.

### ❓ Question #2

`CLAUDE.md` is loaded into context at the start of every session. What belongs in it — and what *doesn't*? How does this relate to what you learned about context management and memory in Session 3?

#### ✅ Answer

CLAUDE.md gets loaded into every single session, so I am paying for every line of it on every turn forever. That makes it expensive real estate and it should only hold durable facts the agent cannot cheaply work out for itself. In my chat app that means how to run the server and curl the endpoint, the one architecture decision that is not obvious from reading a file (the agent lives behind a single swappable function and /api/chat is the seam), the conventions I care about like plain JS and no build step, and the rule that the tool allowlist never gets widened. Things that would cost the agent five tool calls to rediscover are exactly what earns a line.

What does not belong is anything the code already says, since the code is the source of truth and a second copy of it just rots. Also out: transient state about what I am working on this week, long explanations, and anything that goes stale. A stale CLAUDE.md is worse than an empty one because now the agent believes something false and I have no idea it is happening.

This is the same problem from Session 3, just wearing different clothes. A context window is finite working memory and you cannot put everything in it, so you curate what is worth the tokens and push the rest to retrieval. CLAUDE.md is the always loaded part, like the system prompt or a running summary. The repo itself is the retrieval part, because the agent has Read and Grep and can go get a detail on demand instead of me paying to hold it in context on the chance it matters. So the question I ask about a candidate line is the same one I asked when I was trimming message history: does this earn its place in every turn, or can it be fetched when it is actually needed.

### ❓ Question #3

The Agent SDK gives you the same agent loop that powers Claude Code. Compare this to the agent loops you hand-built with LangGraph in Sessions 2–4: what does the SDK give you for free, and what control do you give up?

#### ✅ Answer

What I got for free was almost everything I spent Sessions 2 through 4 building by hand. The ReAct loop itself, retries and error handling, a set of tools that already work (read, grep, glob, bash, web search), the permission gate, conversation persistence I can resume by session id, subagents, and automatic context compaction. My whole agent is one function that calls query() and reads the result off the last message. In LangGraph the equivalent was a state schema, nodes, edges, a conditional router, a tool node, and a checkpointer, and I had to debug all of it.

What I gave up is ownership of the graph. In LangGraph I decided the exact topology, so when I wanted a helpfulness check I added a node and an edge back to the top, and when I wanted a human in the loop I put an interrupt at a specific point in the state machine. The SDK's loop belongs to Anthropic. I steer it from the outside with the system prompt, the tool allowlist, permissions and max_turns, but I cannot reach in and change what happens between iteration three and four. I am also locked to Claude models, where LangGraph would let me swap providers per node.

The trade is control for speed and robustness, and which side you want depends on whether the loop is the product. For this app the loop is not interesting, the answers are, so paying for a battle tested loop with a dependency was clearly right. If I needed a custom topology, or an evaluator inside the cycle, or a specific model per step, I would go back to LangGraph and accept that I now own the bugs too.

### ❓ Question #4

Your chat app could have called a chat completions API directly, the way you did early in the course. What do you gain by routing every message through the Agent SDK's `query()` instead — and what new risks does an agent with tools introduce that a plain chat completion doesn't have? How did your tool allowlist and permission mode address them?

#### ✅ Answer

The gain is that the answers are grounded in the actual repository instead of recalled from training data. I pointed mine at my reforge project, which was written months after any model's cutoff, so a chat completion could only make something up. Through query() the agent globs the tree, greps for the entry point, reads the files it decides it needs, and calls my git_log tool, then answers from what it found and cites the paths. It also chains: asked about the last five commits it called my tool and then went and read the files those commits touched, which is several steps I never specified. Session resumption gives me follow ups for free, so "what are its main dependencies" resolves "its" without me resending the history.

The new risk is a category change. A chat completion can only say a wrong thing. An agent with tools can do a wrong thing. It can run a destructive command, read a .env and put the key in its answer, or read a file that contains instructions aimed at it and follow them, which is prompt injection where the attack arrives through content rather than through the chat box. And my app is headless on a server, so there is no me sitting there clicking approve. Whatever a random user types goes straight to the loop.

So the allowlist is the gate, and it is structural rather than a matter of trust. My agent gets Read, Glob, Grep and my two custom tools, and that is the complete list. There is no Bash, no Write, no Edit. Someone can type "delete this repo" into my chat box and it does not matter how convincing they are, because there is no tool in the process that can delete anything. I tested exactly that and it declined, but the refusal is not the point, the missing tool is. Custom tools have to be allowlisted explicitly by their mcp__concierge__ name for the same reason, so adding a tool is a deliberate decision and not something that leaks in. max_turns at 25 caps a runaway loop so no single request can burn my account, and my git_log tool builds its argument list itself and resolves paths against the repo root rather than passing a user string to a shell, so there is nothing to inject into. The blast radius is set by what I handed it, which I can read in one place in agent.py.

## Activity 1: Level Up the Chat App

Extend your working chat app with **at least one** of the following (built with Claude Code, of course):

1. **Live progress streaming** — stream the agent's activity to the browser (e.g. via Server-Sent Events) so users see tool calls ("reading `app.py`…") while the agent works, instead of a spinner
2. **Multi-conversation support** — a sidebar of separate conversations, each mapped to its own SDK session
3. **A second custom tool** — something genuinely useful for your target repo (e.g. `git_log` for recent changes, or a test-runner summary tool)

Whichever you pick, demo it in your Loom video and explain the design decision in one paragraph.

### ✅ What I built: a second custom tool, `git_log`

I added `git_log` to the concierge alongside `count_lines`. It returns recent commits and can filter to a path. I picked it because of what the target repo is: reforge is a project I am actively working on, and the questions I actually want answered are about change over time, not just structure. Read and Grep can tell me what the code says right now, but they cannot tell me what moved last week or why a file looks the way it does, because that information lives in git and not in the working tree. The tool closes that gap, and the interesting part is what the agent does with it unprompted. Asked "what changed in the last five commits" it calls `git_log` and then reads the files those commits touched, so it explains the change rather than just reciting subject lines. It is composition I never had to specify. The design decision worth naming is that the tool shells out to git but never hands it a user string: it builds its own argument list, caps the limit, and resolves any path against the repo root, so it stays consistent with the read-only guarantee the allowlist is making. A tool that runs a subprocess is the obvious place to accidentally hand back the shell access I deliberately withheld.

## Advanced Activity: The Cat Shop Concierge

Connect your Session 8 cat shop MCP server to your chat app's agent via the SDK's `mcp_servers` option. Your chat app becomes a shopping concierge: users can browse the catalog, fill a cart, and check out — in natural language, through the UI you built, hitting the OAuth-protected server you wrote in Session 8.

Include your findings and a demo in your Loom video.

## Ship 🚢

The working chat app!

### Deliverables

- A short Loom showing:
  - Claude Code scaffolding or extending the app (plan → implement → verify — show the plan!); and
  - the chat app answering real questions about a repository, including at least one visible custom-tool use

## Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped a chat app powered by the Claude Agent SDK — scaffolded entirely with Claude Code! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI agents. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#ClaudeCode #AgentSDK #AIAgents #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

## Submitting Your Homework (Optional For Extra Mark)

Follow these steps to prepare and submit your homework:

1. Pull the latest updates from upstream into the main branch of your repo:

```bash
git checkout main
git pull upstream main
git push origin main
```

2. Work through `01_Installing_Claude_Code.md`, `02_Using_Claude_Code.md`, and `03_Claude_Agent_SDK.md` in order.
3. Build your chat app in a new `chat-app/` folder inside this session directory (include its `CLAUDE.md` — we want to see it!).
4. Fill in your answers to Questions #1–#4 in this README.
5. Complete Activity #1 and record your Loom video.
6. Add, commit, and push your work to your origin repository. Remove `.env` files and API keys before committing.

When submitting your homework, provide the GitHub URL to your repo.
