"""
skills_linker.py
----------------
Manages skill synchronization across AI IDEs using zero-duplication NTFS
Directory Junctions (mklink /J) with transparent fallback to directory mirrors.
Targets:
- Claude Code: ~/.claude/skills/
- Cursor IDE: ~/.cursor/skills-cursor/
"""

from __future__ import annotations

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class SkillsLinker:
    """
    Synchronizes Antigravity modular skills into Claude Code and Cursor.
    Uses NTFS Junctions on Windows to eliminate multi-gigabyte disk duplication
    and ensure live edits in one IDE reflect instantly across all tools.
    """

    def __init__(self, source_skills_dir: Optional[Path] = None):
        self.source_skills_dir = (
            Path(source_skills_dir).resolve()
            if source_skills_dir
            else Path.home() / ".gemini" / "config" / "skills"
        )

    def list_source_skills(self) -> List[str]:
        """Returns sorted list of skill folder names present in source directory."""
        if not self.source_skills_dir.is_dir():
            return []
        skills = []
        for p in self.source_skills_dir.iterdir():
            if p.is_dir() and not p.name.startswith("."):
                skills.append(p.name)
        return sorted(skills)

    def create_junction(self, target_link: Path, source_path: Path) -> bool:
        """
        Creates an NTFS directory junction on Windows (mklink /J).
        Does not require administrator privileges.
        """
        if sys.platform == "win32":
            try:
                # Remove existing file/link if broken or divergent
                if target_link.is_symlink() or os.path.islink(str(target_link)):
                    os.unlink(target_link)
                elif target_link.is_dir():
                    shutil.rmtree(target_link)

                cmd = f'cmd.exe /c mklink /J "{target_link}" "{source_path}"'
                res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return res.returncode == 0 and target_link.exists()
            except Exception:
                return False
        else:
            # POSIX symlink fallback
            try:
                if target_link.is_symlink() or target_link.exists():
                    target_link.unlink()
                target_link.symlink_to(source_path, target_is_directory=True)
                return True
            except Exception:
                return False

    def copy_mirror(self, target_dest: Path, source_path: Path) -> bool:
        """Copies skill directory cleanly."""
        try:
            if target_dest.is_symlink() or os.path.islink(str(target_dest)):
                os.unlink(target_dest)
            elif target_dest.is_dir():
                shutil.rmtree(target_dest)

            shutil.copytree(source_path, target_dest)
            return True
        except Exception:
            return False

    def sync_to_destination(
        self,
        dest_dir: Path,
        mode: str = "junction",
        skills_filter: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Synchronizes all or filtered source skills to the target directory.
        Generates .sync-manifest.json in destination.
        """
        dest_path = Path(dest_dir).resolve()
        dest_path.mkdir(parents=True, exist_ok=True)

        source_skills = self.list_source_skills()
        if skills_filter:
            source_skills = [s for s in source_skills if s in skills_filter]

        successful = []
        failed = []
        mode_used = {}

        for skill_name in source_skills:
            src_skill = self.source_skills_dir / skill_name
            target_link = dest_path / skill_name

            ok = False
            actual_mode = mode

            if mode == "junction":
                ok = self.create_junction(target_link, src_skill)
                if not ok:
                    # Fallback to copy mirror if junction failed
                    ok = self.copy_mirror(target_link, src_skill)
                    actual_mode = "copy_fallback"
                else:
                    actual_mode = "junction"
            else:
                ok = self.copy_mirror(target_link, src_skill)
                actual_mode = "copy"

            if ok:
                successful.append(skill_name)
                mode_used[skill_name] = actual_mode
            else:
                failed.append(skill_name)

        # Write .sync-manifest.json
        manifest_payload = {
            "source": str(self.source_skills_dir),
            "destination": str(dest_path),
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "requested_mode": mode,
            "total_synced": len(successful),
            "skills": mode_used,
        }
        try:
            (dest_path / ".sync-manifest.json").write_text(
                json.dumps(manifest_payload, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

        return {
            "destination": str(dest_path),
            "requested_mode": mode,
            "synced_count": len(successful),
            "failed_count": len(failed),
            "successful_skills": successful,
            "failed_skills": failed,
            "mode_used": mode_used,
        }
