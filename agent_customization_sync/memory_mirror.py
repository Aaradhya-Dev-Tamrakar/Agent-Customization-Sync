"""Mirror local Codex memories into Antigravity's configuration tree."""

from __future__ import annotations

import hashlib
import shutil
from pathlib import Path


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def mirror_memory(source_dir: Path | None = None, destination_dir: Path | None = None) -> int:
    """Copy Codex memories to Antigravity and remove stale destination entries.

    The source is never modified. Stale destination files are removed only after
    every current source file has been copied and its SHA-256 hash verified.
    """
    home = Path.home()
    source = (source_dir or home / ".codex" / "memories").expanduser().resolve()
    destination = (
        destination_dir or home / ".gemini" / "config" / "codex-memories"
    ).expanduser().resolve()

    if not source.is_dir():
        raise FileNotFoundError(f"Codex memory source directory not found: {source}")
    if source == destination or source in destination.parents or destination in source.parents:
        raise ValueError("Source and destination must be separate, non-nested directories")

    source_files = {
        path.relative_to(source): path
        for path in source.rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    if not source_files:
        raise ValueError(f"Codex memory source contains no regular files: {source}")

    destination.mkdir(parents=True, exist_ok=True)
    for relative_path, source_path in source_files.items():
        target_path = destination / relative_path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)

    mismatches = [
        relative_path
        for relative_path, source_path in source_files.items()
        if not (destination / relative_path).is_file()
        or _sha256(source_path) != _sha256(destination / relative_path)
    ]
    if mismatches:
        detail = ", ".join(str(path) for path in mismatches[:5])
        raise OSError(f"Memory mirror hash verification failed for: {detail}")

    expected_files = set(source_files)
    for target_path in sorted(destination.rglob("*"), reverse=True):
        if target_path.is_file() or target_path.is_symlink():
            if target_path.relative_to(destination) not in expected_files:
                target_path.unlink()
        elif target_path.is_dir() and not any(target_path.iterdir()):
            target_path.rmdir()

    return len(source_files)
