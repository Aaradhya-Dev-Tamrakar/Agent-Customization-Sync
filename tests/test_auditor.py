"""
test_auditor.py
---------------
Unit tests for drift detection and token budget auditing.
"""

from pathlib import Path
from agent_customization_sync.auditor import CustomizationAuditor
from agent_customization_sync.manifest import CustomizationManifest


def test_drift_auditor_detects_missing(mock_config_dir: Path, tmp_path: Path):
    empty_claude = tmp_path / "empty_claude"
    empty_cursor = tmp_path / "empty_cursor"
    empty_workspace = tmp_path / "empty_workspace"

    auditor = CustomizationAuditor(source_dir=mock_config_dir)
    report = auditor.audit_drift(
        claude_dir=empty_claude,
        cursor_dir=empty_cursor,
        workspace_dir=empty_workspace,
    )

    assert report.overall_status == "DRIFT_DETECTED"
    assert report.in_sync is False
    assert any(it.status == "MISSING" for it in report.items)
    table = report.to_table()
    assert "Target IDE" in table


def test_token_budget_audit(mock_config_dir: Path):
    auditor = CustomizationAuditor(source_dir=mock_config_dir)
    manifest = CustomizationManifest.from_dir(mock_config_dir)

    tb = auditor.audit_token_budget(manifest=manifest)
    assert tb.is_compliant is True
    assert tb.total_tokens < 8000
    assert tb.headroom_percent >= 60.0
    assert len(tb.top_consumers) > 0
    table = tb.to_table()
    assert "COMPLIANT" in table
