"""
Debounced Event-Driven Memory Watcher Daemon.
Monitors memory directories for changes, debounces write bursts, suppresses feedback loops,
and safely executes the unified memory synchronizer.
"""
from __future__ import annotations

import datetime
import sys
import threading
import time
from pathlib import Path

# Paths
HOME = Path.home()
CODEX_MEMORIES = HOME / ".codex" / "memories"
GEMINI_MEMORIES = HOME / ".gemini" / "config" / "codex-memories"
CLAUDE_TEAM_MEMORY = Path(r"F:\Aaradhya-Dev-Tamrakar\Claude-Desktop\team-memory.md")
SYNC_ENGINE = Path(r"F:\Aaradhya-Dev-Tamrakar\Agent-Customization-Sync\agent_customization_sync\sync_ecosystem_memory.py")

LOG_DIR = HOME / ".gemini" / "antigravity" / "log"
LOG_FILE = LOG_DIR / "ecosystem_memory_watcher.log"

DEBOUNCE_SECONDS = 5.0

def log(msg: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] [WATCHER] {msg}"
    print(formatted)
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception:
        pass

def get_directory_fingerprint(paths: list[Path]) -> dict[str, float]:
    """Capture mtimes of all non-git files across target memory paths."""
    mtimes: dict[str, float] = {}
    for root_dir in paths:
        if not root_dir.exists():
            continue
        if root_dir.is_file():
            try:
                mtimes[str(root_dir)] = root_dir.stat().st_mtime
            except OSError:
                pass
            continue
        for p in root_dir.rglob("*"):
            if p.is_file() and ".git" not in p.parts:
                try:
                    mtimes[str(p)] = p.stat().st_mtime
                except OSError:
                    pass
    return mtimes

class DebouncedSyncTrigger:
    def __init__(self, debounce_delay: float = DEBOUNCE_SECONDS):
        self.debounce_delay = debounce_delay
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()
        self._running_sync = False

    def trigger(self, reason: str = "") -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            log(f"Change detected ({reason}). Starting {self.debounce_delay}s quiet window...")
            self._timer = threading.Timer(self.debounce_delay, self._execute_sync)
            self._timer.daemon = True
            self._timer.start()

    def _execute_sync(self) -> None:
        with self._lock:
            if self._running_sync:
                return
            self._running_sync = True

        log("Quiet window elapsed. Executing debounced sync...")
        try:
            import subprocess
            res = subprocess.run(
                [sys.executable, str(SYNC_ENGINE)],
                capture_output=True,
                text=True,
                timeout=120,
                check=False
            )
            if res.returncode == 0:
                log("Debounced sync completed cleanly.")
            else:
                log(f"Debounced sync returned non-zero code {res.returncode}: {res.stderr[:200]}")
        except Exception as exc:
            log(f"Debounced sync execution failed: {exc}")
        finally:
            with self._lock:
                self._running_sync = False

def run_watcher_loop() -> None:
    log("=== Initializing Debounced Event-Driven Memory Watcher ===")
    watch_targets = [CODEX_MEMORIES, GEMINI_MEMORIES, CLAUDE_TEAM_MEMORY]
    log(f"Watching targets: {[str(p) for p in watch_targets]}")

    debouncer = DebouncedSyncTrigger(debounce_delay=DEBOUNCE_SECONDS)
    last_fingerprint = get_directory_fingerprint(watch_targets)

    try:
        while True:
            time.sleep(1.0)
            current_fingerprint = get_directory_fingerprint(watch_targets)
            if current_fingerprint != last_fingerprint:
                # Find which file changed
                changed = []
                for k, v in current_fingerprint.items():
                    if k not in last_fingerprint or last_fingerprint[k] != v:
                        changed.append(Path(k).name)
                for k in last_fingerprint:
                    if k not in current_fingerprint:
                        changed.append(f"{Path(k).name} (deleted)")

                sample = ", ".join(changed[:3])
                last_fingerprint = current_fingerprint
                debouncer.trigger(reason=f"{len(changed)} file(s) touched: {sample}")
    except KeyboardInterrupt:
        log("Watcher stopped by user.")
    except Exception as e:
        log(f"Watcher crashed with error: {e}")

if __name__ == "__main__":
    run_watcher_loop()
