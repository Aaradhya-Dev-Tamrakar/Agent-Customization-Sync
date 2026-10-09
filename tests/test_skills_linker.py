"""
test_skills_linker.py
---------------------
Unit tests for skill linking, NTFS junction creation, and copy fallback.
"""

from pathlib import Path
from agent_customization_sync.transpilers.skills_linker import SkillsLinker


def test_list_source_skills(mock_config_dir: Path):
    linker = SkillsLinker(source_skills_dir=mock_config_dir / "skills")
    skills = linker.list_source_skills()
    assert "skill-alpha" in skills
    assert "skill-beta" in skills


def test_sync_to_destination_copy(mock_config_dir: Path, tmp_path: Path):
    dest = tmp_path / "target_claude_skills"
    linker = SkillsLinker(source_skills_dir=mock_config_dir / "skills")

    res = linker.sync_to_destination(dest, mode="copy")
    assert res["synced_count"] == 2
    assert (dest / "skill-alpha" / "SKILL.md").is_file()
    assert (dest / "skill-beta" / "SKILL.md").is_file()
    assert (dest / ".sync-manifest.json").is_file()


def test_sync_to_destination_junction_or_fallback(mock_config_dir: Path, tmp_path: Path):
    dest = tmp_path / "target_cursor_skills"
    linker = SkillsLinker(source_skills_dir=mock_config_dir / "skills")

    res = linker.sync_to_destination(dest, mode="junction")
    assert res["synced_count"] == 2
    assert (dest / "skill-alpha").exists()
    assert (dest / "skill-beta").exists()
