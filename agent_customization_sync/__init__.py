"""
agent_customization_sync
------------------------
Antigravity Customization State Saving, Snapshotting, and Cross-IDE Syncing Engine.

Provides deterministic state snapshotting with rolling rollback, lossless rule/MCP/skill
transpilation, and drift auditing across Antigravity, Cursor, Claude Code, and Copilot.
"""

__version__ = "1.0.0"
__author__ = "Aaradhya Dev Tamrakar"

from agent_customization_sync.manifest import (
    CustomizationManifest,
    RuleManifestEntry,
    SkillManifestEntry,
    MCPServerEntry,
    estimate_tokens,
    sha256_file,
    sha256_dir,
)
from agent_customization_sync.snapshot_engine import (
    SnapshotEngine,
    SnapshotMetadata,
)
from agent_customization_sync.auditor import (
    CustomizationAuditor,
    DriftReport,
    TokenBudgetReport,
)

__all__ = [
    "__version__",
    "CustomizationManifest",
    "RuleManifestEntry",
    "SkillManifestEntry",
    "MCPServerEntry",
    "estimate_tokens",
    "sha256_file",
    "sha256_dir",
    "SnapshotEngine",
    "SnapshotMetadata",
    "CustomizationAuditor",
    "DriftReport",
    "TokenBudgetReport",
]
