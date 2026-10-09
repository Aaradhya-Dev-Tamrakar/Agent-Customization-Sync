"""
test_cli.py
-----------
End-to-end unit tests for the command line interface.
"""

from pathlib import Path
from agent_customization_sync.cli import main


def test_cli_help(capsys):
    import pytest
    with pytest.raises(SystemExit) as excinfo:
        main(["--help"])
    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert "usage:" in captured.out or "custom-sync" in captured.out


def test_cli_status(mock_config_dir: Path, mock_snapshot_dir: Path, capsys):
    ret = main([
        "status",
        "--src", str(mock_config_dir),
        "--snapshot-dir", str(mock_snapshot_dir),
    ])
    assert ret == 0
    captured = capsys.readouterr()
    assert "AGENT CUSTOMIZATION SYNC TELEMETRY" in captured.out
    assert "Rules Monitored" in captured.out


def test_cli_snapshot_and_list(mock_config_dir: Path, mock_snapshot_dir: Path, capsys):
    ret = main([
        "snapshot",
        "--tag", "ci-test",
        "--src", str(mock_config_dir),
        "--snapshot-dir", str(mock_snapshot_dir),
    ])
    assert ret == 0
    captured = capsys.readouterr()
    assert "Customization Snapshot Created Successfully" in captured.out

    ret_list = main([
        "list",
        "--snapshot-dir", str(mock_snapshot_dir),
    ])
    assert ret_list == 0
    list_out = capsys.readouterr()
    assert "ci-test" in list_out.out
