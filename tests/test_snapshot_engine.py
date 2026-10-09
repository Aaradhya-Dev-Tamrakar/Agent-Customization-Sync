"""
test_snapshot_engine.py
-----------------------
Unit tests for snapshot creation, ring buffer eviction, and safe rollback.
"""

import time
from pathlib import Path
from agent_customization_sync.snapshot_engine import SnapshotEngine
from agent_customization_sync.manifest import sha256_file


def test_create_and_list_snapshot(mock_config_dir: Path, mock_snapshot_dir: Path):
    engine = SnapshotEngine(source_dir=mock_config_dir, snapshot_dir=mock_snapshot_dir, max_snapshots=5)
    meta = engine.create_snapshot(tag="test-init")

    assert meta.snapshot_id.startswith("snapshot_")
    assert meta.tag == "test-init"
    assert meta.size_bytes > 0
    assert Path(meta.filepath).is_file()

    snapshots = engine.list_snapshots()
    assert len(snapshots) == 1
    assert snapshots[0].snapshot_id == meta.snapshot_id


def test_ring_buffer_eviction(mock_config_dir: Path, mock_snapshot_dir: Path):
    engine = SnapshotEngine(source_dir=mock_config_dir, snapshot_dir=mock_snapshot_dir, max_snapshots=3)

    # Create 5 snapshots with slight time delay to ensure distinct mtimes
    for i in range(5):
        engine.create_snapshot(tag=f"slot-{i}")
        time.sleep(0.02)

    snapshots = engine.list_snapshots()
    assert len(snapshots) == 3
    # Most recent should be slot-4, slot-3, slot-2
    tags = [s.tag for s in snapshots]
    assert "slot-4" in tags
    assert "slot-3" in tags
    assert "slot-2" in tags
    assert "slot-0" not in tags
    assert "slot-1" not in tags


def test_restore_snapshot_cycle(mock_config_dir: Path, mock_snapshot_dir: Path):
    engine = SnapshotEngine(source_dir=mock_config_dir, snapshot_dir=mock_snapshot_dir, max_snapshots=5)
    meta = engine.create_snapshot(tag="golden-baseline")

    original_agents_hash = sha256_file(mock_config_dir / "AGENTS.md")

    # Tamper with files in source_dir
    agents_file = mock_config_dir / "AGENTS.md"
    agents_file.write_text("# Corrupted Content\nDeleted everything.\n", encoding="utf-8")
    assert sha256_file(agents_file) != original_agents_hash

    # Delete config.json
    (mock_config_dir / "config.json").unlink()

    # Restore snapshot
    res = engine.restore_snapshot(snapshot_id=meta.snapshot_id, target_dir=mock_config_dir)

    assert res["status"] == "success"
    assert res["verification_passed"] is True
    assert (mock_config_dir / "config.json").is_file()
    assert sha256_file(agents_file) == original_agents_hash
    assert res["pre_backup_path"] is not None
    assert Path(res["pre_backup_path"]).is_file()
