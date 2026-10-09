"""
test_mcp_normalizer.py
----------------------
Unit tests for MCP configuration normalization and credential scrubbing.
"""

from agent_customization_sync.transpilers.mcp_normalizer import MCPNormalizer


RAW_MCP = {
    "mcpServers": {
        "active-tool": {
            "command": "node",
            "args": ["server.js"],
            "env": {
                "API_KEY": "secret-token-12345",
                "PORT": "8080",
            },
        },
        "inactive-tool": {
            "command": "python",
            "args": ["app.py"],
            "disabled": True,
        },
    }
}


def test_to_cursor():
    norm = MCPNormalizer(RAW_MCP)
    res = norm.to_cursor(scrub_env=False, include_disabled=False)

    assert "mcpServers" in res
    assert "active-tool" in res["mcpServers"]
    assert "inactive-tool" not in res["mcpServers"]
    assert res["mcpServers"]["active-tool"]["env"]["API_KEY"] == "secret-token-12345"


def test_to_cursor_with_scrub():
    norm = MCPNormalizer(RAW_MCP)
    res = norm.to_cursor(scrub_env=True)

    assert res["mcpServers"]["active-tool"]["env"]["API_KEY"] == "***MASKED***"
    assert res["mcpServers"]["active-tool"]["env"]["PORT"] == "8080"


def test_to_claude_settings():
    norm = MCPNormalizer(RAW_MCP)
    existing = {"telemetry": True, "theme": "system"}
    res = norm.to_claude_settings(existing_settings=existing)

    assert res["telemetry"] is True
    assert "mcpServers" in res
    assert "active-tool" in res["mcpServers"]


def test_to_vscode():
    norm = MCPNormalizer(RAW_MCP)
    res = norm.to_vscode()

    assert "servers" in res
    assert "mcpServers" in res
    assert "active-tool" in res["servers"]
