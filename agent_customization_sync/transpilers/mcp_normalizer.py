"""
mcp_normalizer.py
-----------------
Normalizes Model Context Protocol (MCP) server definitions between Antigravity
(mcp_config.json), Cursor IDE (~/.cursor/mcp.json), Claude Code (~/.claude/settings.json
or .mcp.json), and VS Code (.vscode/mcp.json).
"""

from __future__ import annotations

import re
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional


class MCPNormalizer:
    """
    Normalizes and transforms MCP configuration schemas across AI environments.
    Supports credential masking, active/disabled filtering, and schema adaptation.
    """

    SENSITIVE_KEY_PATTERN = re.compile(
        r"(?i)(token|key|secret|password|passwd|auth|cred|signature|api_key|oauth)"
    )

    def __init__(self, raw_config: Optional[Dict[str, Any]] = None):
        self.raw_config = raw_config or {"mcpServers": {}}

    @classmethod
    def from_file(cls, path: Path) -> MCPNormalizer:
        p = Path(path)
        if not p.is_file():
            return cls({"mcpServers": {}})
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return cls(data)
        except Exception:
            return cls({"mcpServers": {}})

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MCPNormalizer:
        return cls(data)

    def get_servers(self) -> Dict[str, Any]:
        """Returns the canonical mcpServers dictionary."""
        return self.raw_config.get("mcpServers", {})

    def mask_env(self, env: Dict[str, str]) -> Dict[str, str]:
        """Masks sensitive environment variable values with '***MASKED***'."""
        masked = {}
        for k, v in env.items():
            if self.SENSITIVE_KEY_PATTERN.search(k):
                masked[k] = "***MASKED***"
            else:
                masked[k] = v
        return masked

    def to_cursor(
        self,
        scrub_env: bool = False,
        include_disabled: bool = False,
    ) -> Dict[str, Any]:
        """
        Translates to Cursor IDE schema (~/.cursor/mcp.json or .cursor/mcp.json).
        Cursor uses the standard 'mcpServers' root key.
        """
        servers = self.get_servers()
        cursor_servers: Dict[str, Any] = {}

        for name, s_cfg in servers.items():
            is_disabled = s_cfg.get("disabled", False)
            if is_disabled and not include_disabled:
                continue

            entry: Dict[str, Any] = {}
            if "command" in s_cfg:
                entry["command"] = s_cfg["command"]
            if "args" in s_cfg:
                entry["args"] = deepcopy(s_cfg["args"])
            if "serverUrl" in s_cfg:
                entry["url"] = s_cfg["serverUrl"]
            elif "url" in s_cfg:
                entry["url"] = s_cfg["url"]

            if "env" in s_cfg and isinstance(s_cfg["env"], dict):
                entry["env"] = self.mask_env(s_cfg["env"]) if scrub_env else deepcopy(s_cfg["env"])

            cursor_servers[name] = entry

        return {"mcpServers": cursor_servers}

    def to_claude_settings(
        self,
        existing_settings: Optional[Dict[str, Any]] = None,
        scrub_env: bool = False,
        include_disabled: bool = False,
    ) -> Dict[str, Any]:
        """
        Translates to Claude Code schema (merges into ~/.claude/settings.json or .mcp.json).
        Claude Code accepts 'mcpServers' mapping directly.
        """
        base = deepcopy(existing_settings) if existing_settings else {}
        cursor_data = self.to_cursor(scrub_env=scrub_env, include_disabled=include_disabled)
        base["mcpServers"] = cursor_data["mcpServers"]
        return base

    def to_vscode(
        self,
        scrub_env: bool = False,
        include_disabled: bool = False,
    ) -> Dict[str, Any]:
        """
        Translates to VS Code format (.vscode/mcp.json).
        Populates both 'servers' and 'mcpServers' for maximum client compatibility.
        """
        cursor_data = self.to_cursor(scrub_env=scrub_env, include_disabled=include_disabled)
        servers = cursor_data["mcpServers"]
        return {
            "servers": servers,
            "mcpServers": servers,
        }
