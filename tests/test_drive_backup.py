from pathlib import Path

from agent_customization_sync.drive_backup import CustomizationDriveBackup


def test_drive_backup_manifest_init(tmp_path: Path):
    manifest_file = tmp_path / "test_manifest.json"
    backup = CustomizationDriveBackup(
        folder_id="mock_folder_123",
        manifest_file=manifest_file,
    )
    man = backup.load_manifest()
    assert man["folder_id"] == "mock_folder_123"
    assert man["files"] == {}

    man["files"]["test_file"] = {"drive_file_id": "file_999", "sha256": "abc"}
    backup.save_manifest(man)

    reloaded = backup.load_manifest()
    assert reloaded["files"]["test_file"]["drive_file_id"] == "file_999"


def test_drive_backup_dry_run_collects_targets(mock_config_dir: Path, mock_snapshot_dir: Path):
    backup = CustomizationDriveBackup(
        folder_id="mock_folder_123",
        source_dir=mock_config_dir,
        snapshot_dir=mock_snapshot_dir,
        manifest_file=mock_snapshot_dir / "drive_manifest.json",
    )
    # Create snapshot first
    backup.engine.create_snapshot(tag="dry-run-test")

    res = backup.run_backup(dry_run=True)
    assert res["status"] == "dry_run"
    names = [t["name"] for t in res["targets"]]
    assert "customization_state_latest.zip" in names
    assert "local_bin_manifest.json" in names
