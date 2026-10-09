"""
test_rules_transpiler.py
------------------------
Unit tests for cross-IDE rule transpilation (Claude, Cursor MDC, Copilot, Codex).
"""

from agent_customization_sync.transpilers.rules_transpiler import RulesTranspiler

SAMPLE_RULES = """<RULE[user_global]>
# System Invariants

Always adhere to deterministic verification.
Never skip verification gates.

## Git Operations

Always use sync.bat wrapper for version control.
Do not invoke raw git commands.

## Code Quality Standards

Maintain zero lint errors.
Preserve docstrings.
</RULE[user_global]>
"""


def test_clean_xml_tags():
    rt = RulesTranspiler(SAMPLE_RULES)
    cleaned = rt.clean_xml_tags(SAMPLE_RULES)
    assert "<RULE" not in cleaned
    assert "</RULE" not in cleaned
    assert "# System Invariants" in cleaned


def test_transpile_claude():
    rt = RulesTranspiler(SAMPLE_RULES)
    claude_md = rt.transpile_claude()
    assert "CLAUDE.md" in claude_md
    assert "<RULE" not in claude_md
    assert "System Invariants" in claude_md
    assert "sync.bat" in claude_md


def test_transpile_cursor():
    rt = RulesTranspiler(SAMPLE_RULES)
    cursor_dict = rt.transpile_cursor()

    assert ".cursorrules" in cursor_dict
    assert len(cursor_dict) > 1

    # Check for .mdc files
    mdc_keys = [k for k in cursor_dict.keys() if k.endswith(".mdc")]
    assert len(mdc_keys) >= 3

    # Check MDC frontmatter
    first_mdc = cursor_dict[mdc_keys[0]]
    assert first_mdc.startswith("---\n")
    assert 'globs: ["*"]' in first_mdc
    assert "alwaysApply: true" in first_mdc


def test_transpile_copilot():
    rt = RulesTranspiler(SAMPLE_RULES)
    copilot_md = rt.transpile_copilot()
    assert "GitHub Copilot Instructions" in copilot_md
    assert "<RULE" not in copilot_md
    assert "sync.bat" in copilot_md


def test_transpile_codex():
    rt = RulesTranspiler(SAMPLE_RULES)
    codex_md = rt.transpile_codex()
    assert "OpenAI Codex CLI" in codex_md
    assert "<RULE" not in codex_md
    assert "System Invariants" in codex_md
