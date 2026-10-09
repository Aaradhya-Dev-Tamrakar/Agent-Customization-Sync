"""
conftest.py
-----------
Pytest fixtures providing isolated temporary directories for Antigravity source
configuration, snapshot archives, and target IDE environments.
"""

import json
import pytest
from pathlib import Path


@pytest.fixture
def mock_config_dir(tmp_path: Path) -> Path:
    """Creates a temporary mock Antigravity configuration directory."""
    cfg = tmp_path / "mock_gemini_config"
    cfg.mkdir(parents=True, exist_ok=True)

    # 1. AGENTS.md
    agents_content = (
        "<RULE[user_global]>\n"
        "# Global Governance Directives\n\n"
        "Always enforce deterministic verification.\n"
        "Never perform raw git commands without safety wrappers.\n\n"
        "## Git Workflow Standards\n\n"
        "Use sync.bat for version control across all workspaces.\n\n"
        "## Code Quality Constraints\n\n"
        "Zero conversational filler. Target zero lint errors.\n"
        "</RULE[user_global]>\n"
    )
    (cfg / "AGENTS.md").write_text(agents_content, encoding="utf-8")

    # 2. GEMINI.md
    (cfg / "GEMINI.md").write_text("# Gemini Environment Directives\n", encoding="utf-8")

    # 3. mcp_config.json
    mcp_data = {
        "mcpServers": {
            "classroom": {
                "command": "node",
                "args": ["F:\\path\\to\\classroom\\index.mjs"],
                "env": {
                    "CLASSROOM_CREDENTIALS_PATH": "C:\\path\\cred.json",
                    "CLASSROOM_SECRET_KEY": "sk-1234567890abcdef",
                },
            },
            "deep-reasoning": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
            },
            "disabled-server": {
                "command": "python",
                "args": ["server.py"],
                "disabled": True,
            },
        }
    }
    (cfg / "mcp_config.json").write_text(json.dumps(mcp_data, indent=2), encoding="utf-8")

    # 4. config.json
    config_data = {
        "theme": "dark",
        "telemetry": False,
        "max_context": 32768,
    }
    (cfg / "config.json").write_text(json.dumps(config_data, indent=2), encoding="utf-8")

    # 5. skills/
    skills_dir = cfg / "skills"
    for name in ["skill-alpha", "skill-beta"]:
        s_dir = skills_dir / name
        s_dir.mkdir(parents=True, exist_ok=True)
        (s_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: Test skill {name}\n---\n# {name}\nOperational logic.\n",
            encoding="utf-8",
        )
        (s_dir / "helper.py").write_text(f"# {name} helper script\ndef run(): pass\n", encoding="utf-8")

    return cfg


@pytest.fixture
def mock_snapshot_dir(tmp_path: Path) -> Path:
    """Creates a temporary directory for snapshot archives."""
    sdir = tmp_path / "mock_snapshots"
    sdir.mkdir(parents=True, exist_ok=True)
    return sdir
