# Agent-Customization-Sync

Agent-Customization-Sync captures, snapshots, and losslessly projects Antigravity agent customization state across Cursor IDE, Claude Code CLI, GitHub Copilot, and OpenAI Codex environments while enforcing a strict 8,000-token static overhead ceiling.

---

## 1. System Architecture

The engine treats `~/.gemini/config/` as the canonical Single Source of Truth (SSOT). All rules, domain skills, and Model Context Protocol (MCP) declarations synchronize outward to target environments via deterministic transpilation and zero-duplication NTFS directory junctions.

```
                          +-----------------------------------+
                          |  Antigravity SSOT (~/.gemini/)    |
                          |  - AGENTS.md, GEMINI.md           |
                          |  - mcp_config.json, config.json   |
                          |  - skills/ (58 modular skills)    |
                          +-----------------+-----------------+
                                            |
                       +--------------------+--------------------+
                       |                                         |
                       v                                         v
        +-----------------------------+           +-----------------------------+
        |   Snapshot & Rollback       |           |   Cross-IDE Transpiler      |
        |   - SHA-256 Merkle Manifest |           |   - Rules: .mdc, CLAUDE.md  |
        |   - Rolling 5-slot Buffer   |           |   - MCP: Cursor/Claude/VSCode|
        |   - Pre-restore Safety Back |           |   - Skills: NTFS Junctions  |
        +--------------+--------------+           +--------------+--------------+
                       |                                         |
                       +--------------------+--------------------+
                                            |
                                            v
                         +-------------------------------------+
                         |      Drift & Token Auditor          |
                         |      - Cross-IDE divergence checks  |
                         |      - Ceiling: < 8,000 tokens      |
                         |      - Headroom: >= 60% budget      |
                         +-------------------------------------+
```

### Core Subsystems

1. **State Snapshot & Rollback Engine (`snapshot_engine.py`)**:
   - Generates a cryptographic SHA-256 manifest across all rules, skills, MCP servers, and settings.
   - Archives state bundles into `~/.gemini/snapshots/customizations/snapshot_<timestamp>.zip`.
   - Enforces a rolling 5-slot ring buffer eviction policy to bound disk consumption.
   - Guarantees safe restoration with pre-flight safety backups and byte-level hash verification.

2. **Cross-IDE Transpiler (`transpilers/`)**:
   - `RulesTranspiler`: Parses `AGENTS.md` and generates Claude Code `CLAUDE.md`, Cursor modular `.cursor/rules/*.mdc` (with YAML frontmatter `globs: ["*"]` and `alwaysApply: true`), legacy `.cursorrules`, and GitHub Copilot `.github/copilot-instructions.md`.
   - `MCPNormalizer`: Normalizes `mcp_config.json` into Cursor (`~/.cursor/mcp.json`), Claude Code (`~/.claude/settings.json`), and VS Code (`.vscode/mcp.json`) schemas with optional credential scrubbing.
   - `SkillsLinker`: Uses Windows NTFS Directory Junctions (`mklink /J`) to mirror `~/.gemini/config/skills/` into `~/.claude/skills/` and `~/.cursor/skills-cursor/` without disk duplication.

3. **Drift & Token Overhead Auditor (`auditor.py`)**:
   - Compares live configurations across target IDEs against the canonical manifest.
   - Measures token overhead per component and validates against the 8,000-token ceiling ($\ge 60\%$ context headroom).

4. **Zero-Friction CLI & Batch Wrapper (`custom_sync.bat`)**:
   - Exposes clean CLI subcommands (`snapshot`, `list`, `restore`, `push`, `audit`, `status`).

---

## 2. Scope Boundaries & Non-Goals

- **Non-Goal: Bidirectional Merging**: The engine does not perform three-way Git merges on rules modified independently across multiple IDEs. Antigravity is the authoritative source; changes in target IDEs are detected as drift and overwritten on push.
- **Non-Goal: Secret Vault Replacement**: MCP normalization masks credentials when exporting configuration bundles, but the tool does not replace dedicated credential vaults such as Bitwarden.
- **Supported Platforms**: Windows 10/11 (native NTFS junctions via `mklink /J`) and POSIX operating systems (standard symbolic links).

---

## 3. Command Line Interface

Execute the tool using the zero-friction batch wrapper `custom_sync.bat` or directly via Python:

```bat
REM Create a timestamped state snapshot checkpoint
.\custom_sync.bat snapshot --tag "pre-upgrade"

REM List available snapshots in the rolling ring buffer
.\custom_sync.bat list

REM Restore configuration from a designated snapshot
.\custom_sync.bat restore --latest
.\custom_sync.bat restore --id "snapshot_20261009_131500"

REM Project canonical state to all supported IDEs
.\custom_sync.bat push --all

REM Project state selectively to specific targets
.\custom_sync.bat push --cursor --mode junction
.\custom_sync.bat push --claude
.\custom_sync.bat push --vscode

REM Run drift detection and token budget audit
.\custom_sync.bat audit

REM View active configuration telemetry
.\custom_sync.bat status

REM One-click mirror of local Codex memory into Antigravity
.\mirror_codex_memory.bat
```

The memory mirror copies `~/.codex/memories/` into
`~/.gemini/config/codex-memories/`, verifies copied files with SHA-256, then
removes stale files from the destination. It leaves the Codex source untouched.
Run `custom_sync.bat mirror-memory --src <path> --dest <path>` to override either
directory.

---

## 4. Verification

Execute the test suite using pytest:

```powershell
pytest tests/ -v
```
