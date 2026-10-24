# GitHub Copilot Instructions

This file defines authoritative behavioral rules, coding standards, and verification
workflows for all GitHub Copilot workspace operations.

# Global Agent Configuration & Rules

## 1. Autonomous Swarms & Teamwork Integration (`/teamwork-preview`)
- Whenever the user invokes the `/teamwork-preview` slash command, mentions teamwork delegation, or requests an autonomous agent team, the agent **MUST automatically activate and apply the `agent-teams-orchestration` skill** (`C:\Users\Aaradhya\.gemini\config\skills\agent-teams-orchestration\SKILL.md`).
- All teamwork prompt drafts (`prompt_draft.md`) must strictly embed:
  1. The **Scout-Reviewer-Writer-Lead** cognitive division of labor.
  2. Concurrency isolation via separate working files or isolated worktree branches (`Workspace: 'branch'`).
  3. Bounded stopping criteria (e.g. hard token/time/paper budgets) to prevent runaway loops.
  4. Grounding and compilation into the local Obsidian knowledge graph (`[[wikilinks]]`) with epistemic provenance.

## 2. NotebookLM MCP Grounding & Notebook IDs
When interacting with `super-nlm` or `notebooklm` MCP tools, reference these primary notebook IDs:
- **Personal Notebook**: `95a79d26-2f87-42cd-8cb9-8361a1e56059` (⚙️ Aaradhya — Engineer's Personal Notebook)
- **SPARK**: `2c00f5a4-98dc-4783-96d1-3682fa3cb516` (https://notebook.google.com/notebook/2c00f5a4-98dc-4783-96d1-3682fa3cb516)
- **BiasAperture**: `99bee3c6-07ed-4ff0-8ac8-0027b18ad06a` (https://notebook.google.com/notebook/99bee3c6-07ed-4ff0-8ac8-0027b18ad06a)

## 3. Cross-Tool Session Continuity
- When any `Claude_export*.md` or exported transcript files exist in the active directory or project, read them first to inherit context before proceeding with subsequent tasks.

## 4. Execution & Safety Constraints
- **Background Task & Subprocess Governance (`background-task-governance`)**:
  - Automatically enforce the [`background-task-governance`](file:///C:/Users/Aaradhya/.gemini/config/skills/background-task-governance/SKILL.md) skill to prevent hung processes, freezes, or blocked subprocesses on Windows.
  - **Zero Interactive CLIs Headlessly**: Never invoke CLI utilities that prompt for unattached stdin or confirmation without non-interactive flags (e.g., `diskpart`, interactive WSL flags, interactive formatters).
  - **Zero Elevated UAC Headlessly**: Commands requiring administrator elevation must never be dispatched headlessly; instruct the user to run them in an external elevated terminal.
  - **PowerShell Script-File First**: Never pass multi-pipe expressions or complex PowerShell blocks via inline `-Command "..."` strings that risk quote/pipeline mangling. Write to a `.ps1` in the scratch directory and invoke with `-ExecutionPolicy Bypass -File`.
  - **Proactive Watchdog**: If any background task produces no output or progress for >60s, inspect process CPU/IO immediately and kill deadlocked tasks.
- **Jupyter Notebooks**: Never run or execute `.ipynb` files headlessly via CLI commands; leave execution for Google Colab or manual runs.
- **In-Place File Delivery**: Apply edits directly to target files in the repository using diff-precise tools; do not stage files into zip archives or external output directories unless explicitly asked.
- **Ambiguity & Disambiguation Gate**: Execute what is explicitly instructed. If scope, repository target, or file formatting is ambiguous, ask first rather than assuming.
- **Slash Command Discipline**: Suggest at most one single relevant slash command only when immediately helpful to the next user action. Never enumerate, repeat, or list multiple alternative slash commands in a single response.
- **Filesystem Pruning & Mirror Invariant**: Any script or tool that synchronizes, mirrors, or cleans up destination directories (e.g. `mirror_memory`, mirror sync scripts) must unconditionally exclude `.git`, `.github`, and `.gitignore` from pruning walks to avoid Windows access-denial collisions on read-only VCS objects.

## 5. Workflow Patterns & Ecosystem Automation (`sync.ps1` / `sync.bat`)
- **Inspection Before Action**: Discover actual repository conventions, schema, and layout via direct inspection; never assume conventions.
- **Integrity Diff Checks**: Diff new/modified content against live repository state (title/search-index diffs, `id` ↔ `href` link integrity, syntax validity, HTML/JSX tag balance) before completing work.
- **Default GitHub Development Workflow (`github-workflow`)**:
  - Whenever implementing features, fixing bugs, refactoring, or managing version control across GitHub repositories, the agent **MUST automatically activate and apply the `github-workflow` skill** (`C:\Users\Aaradhya\.gemini\config\skills\github-workflow\SKILL.md`).
  - Standard development sequence:
    1. **Issue Anchoring**: Formulate requirements with acceptance tasks (`- [ ]`) and create a tracked issue with full metadata (`gh issue create --assignee "@me" --label "<labels>"`).
    2. **Branch Isolation**: Branch off `main` via `<type>/<slug>-#<id>`, never committing multi-step changes directly to `main`.
    3. **Progressive Task Tracking**: Check off tasks as completed using `gh-task --issue <id> --task "..."` (or `toggle-issue-task`).
    4. **Verification Gate**: Enforce local test suite (`pytest`) and linting (`ruff`) clean passes before commits.
    5. **Ecosystem Synchronization**: Run all version control through `.\sync.bat -m "type(scope): summary (#id)"` (or `.\sync.ps1`).
    6. **Pull Request & Review Dispatch**: Open PR with complete sidebar metadata (`gh pr create --assignee "@me" --label "<labels>" --reviewer <teammate>`), link the issue (`Closes #<id>`), and document test proof.
    7. **PR Merge Governance**: For collaborative/cohort repositories, require peer review sign-off. For solo project repositories, PRs can be merged directly once local verification gates and remote CI pass (`gh pr merge <id> --squash --delete-branch`).
- **`sync.ps1` / `sync.bat` Self-Reporting & Enforcement Gate**:
  - Always check if `sync.ps1` or `sync.bat` is present in the repository root.
  - If `sync.ps1` is present: raw `git commit`, `git push`, or `git add` are strictly forbidden. All version control must run through `.\sync.bat` (or `.\sync.ps1`):
    - **Zero-Friction Wrapper**: Prefer `.\sync.bat` across Windows environments to automatically bypass PowerShell ExecutionPolicy (`Restricted`/`RemoteSigned`) on fresh clones without manual system configuration.
    - **Routine / Minor Changes**: `.\sync.bat` (or `.\sync.ps1`)
    - **Major Features / Architectural Changes**: Update tracker (e.g., `dev-logs/PortfolioWebsite_TRACKER.md` or repo tracker) first, then run `.\sync.bat -m "feat(scope): detailed summary"`.
  - **Root Entrypoint & Companion Guarantee**:
    - If a repository contains `sync.ps1` but lacks `sync.bat`, create or maintain `sync.bat` as the companion entrypoint to guarantee friction-free execution across new machines.
    - If a repository organizes sync scripts under `scripts/` (e.g., `scripts/sync.ps1` and `scripts/sync.bat` in repos with root `Makefile`/`make.bat` like `BiasAperture`), a root `sync.bat` forwarder (`call "%~dp0scripts\sync.bat" %*`) **MUST** be maintained at the repository root so `.\sync.bat` works unconditionally.
  - **Task Runner vs. VCS Engine Boundary (`Makefile` vs `sync.ps1`)**:
    - `Makefile` / `make.bat` serves as an omnibus developer task runner for build/test routines (`make test`, `make lint`, `make verify`, `make audit`, `make clean`). Highly recommended in collaborative/fellowship repositories.
    - `sync.ps1` / `sync.bat` remains the sole authoritative engine for version control, secret screening, diff AST analysis, automated conventional commits, and PR routing. In repositories with a `Makefile`, `make sync` delegates directly to `sync.bat`.
- **Output Discipline**:
  - Zero conversational framing, fluff, or narrative padding. Dive straight into execution.
  - No unnecessary post-explanations of code edits unless specifically requested.
  - If verification fails or conflicts occur, halt and report the exact discrepancy concisely.

## 6. Authoritative Portfolio Repository
- The user's authoritative portfolio repository is **`AaradhyaDT.github.io`** (`F:\AaradhyaDT\AaradhyaDT.github.io`), hosted under the personal account (`https://github.com/AaradhyaDT/AaradhyaDT.github.io`). The organization repository (`Aaradhya-Dev-Tamrakar/AaradhyaDT.github.io`) is strictly a secondary mirror. Whenever referencing, updating, or tracking the portfolio, use `F:\AaradhyaDT\AaradhyaDT.github.io` as the canonical default.


## Codex Memory Mirror
- A full local mirror of Codex memory is stored at `~/.gemini/config/codex-memories/`.
- For prior decisions or user preferences, consult `codex-memories/MEMORY.md` and `codex-memories/memory_summary.md` when relevant.
- `codex-memories/rollout_summaries/` and `codex-memories/extensions/` retain detailed historical context; consult selectively when needed.
- **Bidirectional Mirror Invariant**: Personal operating telemetry and health guardrails reside in `codex-memories/extensions/ad_hoc/notes/`. When updating memory, mirror changes between `~/.codex/memories/` and `~/.gemini/config/codex-memories/` using `Agent-Customization-Sync/custom_sync.bat mirror-memory`.
