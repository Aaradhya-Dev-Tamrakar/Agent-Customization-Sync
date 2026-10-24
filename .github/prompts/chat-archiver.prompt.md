---
description: ">-"
---

# Chat Archiver & Reader Skill (`save-chat` & `read-chat`)

CRITICAL RULE: Whenever the user asks to inspect, read, summarize, or archive:
1. An **Antigravity conversation session** (by UUID, prefix like `2417d518`, or latest in brain)
2. An **OpenAI Codex thread** (by thread UUID like `01a16ccd`, prefix like `threads/01a16ccd-...`, or `--codex` / `-x`)
3. An **external shared conversation link** (ChatGPT, Google Gemini)

**DO NOT** write scratch Python scripts, scrape raw files manually, or stream tokens parsing JSONL/HTML.
You **MUST** immediately run the globally installed CLI tools:
- **`read-chat`** to inspect, summarize (bird's-eye view), focus on Nth turns, filter turns, search, or export conversation sessions.
- **`save-chat`** to download and archive external share links, Codex threads, or Antigravity brain sessions.

---

## 1. Unified Session Reading & Inspection (`read-chat`)

`read-chat` automatically detects and parses transcripts from:
- **Antigravity Brain:** `~/.gemini/antigravity/brain/<id>/.system_generated/logs/transcript.jsonl`
- **OpenAI Codex:** `~/.codex/sessions/**/rollout-*.jsonl` (and `~/.codex/sqlite/codex-dev.db`)

### Bird's-Eye View / Session Summary
```bash
# Antigravity session
read-chat <CONVERSATION_ID> --summary    # or -s

# OpenAI Codex thread (accepts threads/<uuid>, raw UUID, or short 8-char prefix)
read-chat threads/01a16ccd-94e3-77a3-8904-5ff4d5e22894 -s
read-chat 01a16ccd -s
```

### Whole Session with Nth Turn Focus
```bash
# Focus on final turn (-1 / last) with full bird's-eye milestone overview:
read-chat <ID_OR_THREAD> -f -1
read-chat <ID_OR_THREAD> --focus-last    # or -F

# Focus on specific Nth turn (e.g. Turn 7, or penultimate -2):
read-chat <ID_OR_THREAD> -f 7
read-chat <ID_OR_THREAD> -f -2 --context 2
```

### User Prompts Audit
```bash
read-chat <ID_OR_THREAD> --user-only     # or -u
```

### Inspect Specific Turns & Tools
```bash
# View last N turns
read-chat <ID_OR_THREAD> --last 3

# View specific turn with full tool execution breakdown
read-chat <ID_OR_THREAD> --turn -1 --tools
```

### Listing Conversations
```bash
# List recent Antigravity brain conversations (default)
read-chat --list                         # or -l

# List recent OpenAI Codex threads (with titles, workspaces, and modified times)
read-chat -l --codex                     # or -l -x

# List both Antigravity and Codex sessions
read-chat -l --all                       # or -l -A
```

### Keyword Search Across Archives
```bash
# Searches across both Antigravity brain transcripts and Codex session rollouts:
read-chat --search "query"               # or -q "query"
```

### Export Session to Clean Markdown
```bash
# Export to default research/transcripts or docs/chat_history
read-chat <ID_OR_THREAD> --export        # or -e

# Export to custom path or directory
read-chat <ID_OR_THREAD> -o "path/to/session.md"
read-chat <ID_OR_THREAD> -e --dir "research/transcripts"
```

---

## 2. External Share Links & Direct Archiving (`save-chat`)

### Save External Share Link (ChatGPT / Gemini)
```bash
save-chat "<URL>"
save-chat "<URL>" --dir "f:/Aaradhya-Dev-Tamrakar/brainstorm/research/transcripts"
```

### Save Local Sessions (Codex or Antigravity) via `save-chat`
```bash
# Codex thread
save-chat threads/01a16ccd-94e3-77a3-8904-5ff4d5e22894
save-chat 01a16ccd

# Antigravity session
save-chat 2417d518
```

### Append Mode (Continuation of Last / Specified Transcript)
```bash
save-chat "<URL_OR_ID>" --append         # or -a
```
