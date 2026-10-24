from pathlib import Path

from agent_customization_sync.local_bin_provisioner import LocalBinProvisioner


def test_local_bin_provisioner_creates_all_shims(tmp_path: Path):
    provisioner = LocalBinProvisioner(bin_dir=tmp_path)
    res = provisioner.provision()

    assert len(res["created"]) == 10
    assert len(res["updated"]) == 0
    assert len(res["skipped"]) == 0

    expected_shims = [
        "ghw.bat", "ghw.ps1",
        "gh.bat", "gh.ps1",
        "gh-workflow.bat", "gh-workflow.ps1",
        "gh-task.bat", "gh-task.ps1",
        "toggle-issue-task.bat", "toggle-issue-task.ps1",
    ]
    for shim in expected_shims:
        assert (tmp_path / shim).is_file()


def test_local_bin_provisioner_audit(tmp_path: Path):
    provisioner = LocalBinProvisioner(bin_dir=tmp_path)

    # Initial state: missing all
    audit_pre = provisioner.audit()
    assert len(audit_pre["missing"]) == 10

    # Provision
    provisioner.provision()
    audit_post = provisioner.audit()
    assert len(audit_post["missing"]) == 0
    assert len(audit_post["present"]) == 10
    assert len(audit_post["drifted"]) == 0


def test_local_bin_provisioner_drift_detection(tmp_path: Path):
    provisioner = LocalBinProvisioner(bin_dir=tmp_path)
    provisioner.provision()

    # Modify one file to simulate drift
    target = tmp_path / "ghw.bat"
    target.write_text("corrupted content", encoding="utf-8")

    audit = provisioner.audit()
    assert "ghw.bat" in audit["drifted"]
    assert len(audit["present"]) == 9

    # Re-provision repairs drift
    repair_res = provisioner.provision(overwrite=True)
    assert "ghw.bat" in repair_res["updated"]

    audit_repaired = provisioner.audit()
    assert len(audit_repaired["drifted"]) == 0
    assert len(audit_repaired["present"]) == 10
