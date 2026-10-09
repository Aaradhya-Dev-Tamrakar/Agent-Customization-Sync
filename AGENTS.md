# Agent Operating Guidelines — Agent-Customization-Sync

This repository (`F:\Aaradhya-Dev-Tamrakar\Agent-Customization-Sync`) maintains the core engine for capturing, snapshotting, and synchronizing Antigravity agent customizations across multi-IDE developer workflows.

---

## 1. Git Workflow & Automation

In compliance with ecosystem invariants, version control operations in this repository must use `.\sync.bat` (or `.\sync.ps1`).

```bat
REM Routine synchronization with secret scanning
.\sync.bat

REM Commit with explicit conventional message
.\sync.bat -m "feat(transpiler): add support for Zed editor MCP schema"

REM Pull latest upstream changes without committing
.\sync.bat -PullOnly
```

---

## 2. Invariant Rules & Boundaries

1. **Zero External Runtime Dependencies**: Core operations (`manifest`, `snapshot_engine`, `transpilers`, `auditor`, `cli`) must remain executable using standard Python library primitives (`hashlib`, `json`, `zipfile`, `argparse`, `dataclasses`).
2. **Deterministic Hash Invariance**: Any structural change to a rule, skill, or configuration file must alter the Merkle root hash reported by `CustomizationManifest`.
3. **Safe Rollback Invariant**: Restoring a snapshot must create an automated pre-restore safety backup of target directories before applying changes.
4. **Token Ceiling Invariant**: Total static overhead across active configurations must not exceed 8,000 tokens ($< 40\%$ of standard prefix budgets).

---

## 3. Verification Protocol

Before synchronizing changes, execute the full regression suite:

```powershell
pytest tests/ -v
```
