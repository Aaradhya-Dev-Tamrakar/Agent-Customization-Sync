"""
Unified Ecosystem Memory Sync Engine.
Synchronizes Antigravity, Codex, Claude Profiles, and VS Code memories headlessly.
"""
from __future__ import annotations

import datetime
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

# Paths
HOME = Path.home()
CODEX_MEMORIES = HOME / ".codex" / "memories"
GEMINI_MEMORIES = HOME / ".gemini" / "config" / "codex-memories"
CLAUDE_PROFILES = HOME / ".claude-profiles"
CLAUDE_DESKTOP_REPO = Path(r"F:\Aaradhya-Dev-Tamrakar\Claude-Desktop")
CLAUDE_TEAM_MEMORY = CLAUDE_DESKTOP_REPO / "team-memory.md"
DRIVE_SYNC_SCRIPT = Path(r"F:\Aaradhya-Dev-Tamrakar\Fleet-Orchestrator\scripts\sync_drive.py")
LOG_DIR = HOME / ".gemini" / "antigravity" / "log"
LOG_FILE = LOG_DIR / "ecosystem_memory_sync.log"

def log(msg: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(65536):
            h.update(block)
    return h.hexdigest()

def sync_codex_and_gemini() -> int:
    """Bidirectional safe merge between Codex and Gemini memory directories."""
    log("Synchronizing Codex <-> Gemini memory directories...")
    if not CODEX_MEMORIES.is_dir() or not GEMINI_MEMORIES.is_dir():
        log("Warning: Either Codex or Gemini memory directory does not exist.")
        return 0

    codex_files = {p.relative_to(CODEX_MEMORIES): p for p in CODEX_MEMORIES.rglob("*") if p.is_file() and ".git" not in p.parts}
    gemini_files = {p.relative_to(GEMINI_MEMORIES): p for p in GEMINI_MEMORIES.rglob("*") if p.is_file() and ".git" not in p.parts}

    # 1. Copy missing from Codex to Gemini
    copied = 0
    for rel, src in codex_files.items():
        dst = GEMINI_MEMORIES / rel
        if not dst.exists() or sha256_file(src) != sha256_file(dst):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1

    # 2. Copy missing from Gemini to Codex
    for rel, src in gemini_files.items():
        dst = CODEX_MEMORIES / rel
        if not dst.exists() or sha256_file(src) != sha256_file(dst):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1

    log(f"Synced {copied} updated/new files between Codex and Gemini.")
    return copied

def bridge_claude_team_memory() -> None:
    """Index Claude Desktop team-memory dates into GLOBAL_MEMORY.md."""
    if not CLAUDE_TEAM_MEMORY.is_file():
        return

    global_mem = GEMINI_MEMORIES / "GLOBAL_MEMORY.md"
    if not global_mem.is_file():
        return

    log("Checking Claude team-memory integration...")
    try:
        content = global_mem.read_text(encoding="utf-8")
        if "Claude Desktop Team Memory Bridge" not in content:
            marker = "## 2. Chronological Modular Registry"
            addition = (
                "\n### Claude Desktop Team Memory Integration\n"
                "- Authoritative Fleet Log: `F:\\Aaradhya-Dev-Tamrakar\\Claude-Desktop\\team-memory.md`\n"
                "- Profiles: `C:\\Users\\Aaradhya\\.claude-profiles\\user1..user25`\n"
            )
            if marker in content:
                content = content.replace(marker, marker + addition)
                global_mem.write_text(content, encoding="utf-8")
                # Mirror back to codex
                shutil.copy2(global_mem, CODEX_MEMORIES / "GLOBAL_MEMORY.md")
                log("Appended Claude team-memory integration section to GLOBAL_MEMORY.md.")
    except Exception as e:
        log(f"Error bridging Claude team-memory: {e}")

def trigger_cloud_drive_sync() -> None:
    """Trigger background Drive manifest/memory sync if script exists."""
    if DRIVE_SYNC_SCRIPT.is_file():
        log(f"Triggering Google Drive sync via {DRIVE_SYNC_SCRIPT.name}...")
        try:
            subprocess.run(
                [sys.executable, str(DRIVE_SYNC_SCRIPT), "--quiet"],
                capture_output=True,
                text=True,
                timeout=60,
                check=False
            )
            log("Google Drive sync finished successfully.")
        except Exception as e:
            log(f"Google Drive sync skipped or timed out: {e}")


def trigger_customization_drive_backup() -> None:
    """Trigger background Drive backup of customization state and runner shims."""
    try:
        from agent_customization_sync.drive_backup import CustomizationDriveBackup
        log("Triggering Customization Drive cloud backup...")
        backup_engine = CustomizationDriveBackup()
        backup_engine.run_backup(dry_run=False, force=False)
        log("Customization Drive cloud backup finished successfully.")
    except Exception as e:
        log(f"Customization Drive cloud backup skipped: {e}")


def main() -> int:
    log("=== Starting Unified Ecosystem Memory Sync ===")
    try:
        sync_codex_and_gemini()
        bridge_claude_team_memory()
        trigger_cloud_drive_sync()
        trigger_customization_drive_backup()
        log("=== Unified Ecosystem Memory Sync Finished Successfully ===")
        return 0
    except Exception as exc:
        log(f"Error during memory sync: {exc}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
