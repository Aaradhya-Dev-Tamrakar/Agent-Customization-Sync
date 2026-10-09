"""
rules_transpiler.py
-------------------
Transpiles canonical Antigravity AGENTS.md / GEMINI.md rules into:
1. Claude Code CLI format: CLAUDE.md
2. Cursor IDE format: .cursor/rules/*.mdc (with YAML frontmatter) & .cursorrules
3. VS Code / GitHub Copilot format: .github/copilot-instructions.md
4. OpenAI Codex CLI format: ~/.codex/AGENTS.md
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class RulesTranspiler:
    """
    Parses and projects canonical rules into target IDE schemas.
    Preserves structural invariants, eliminates tool-specific XML wrappers,
    and formats frontmatter according to each IDE's specification.
    """

    def __init__(self, source_content: Optional[str] = None):
        self.source_content = source_content or ""

    @classmethod
    def from_file(cls, path: Path) -> RulesTranspiler:
        content = Path(path).read_text(encoding="utf-8", errors="ignore")
        return cls(content)

    def clean_xml_tags(self, text: str) -> str:
        """Strips Antigravity-specific XML wrapping tags like <RULE[...]> and </RULE>."""
        cleaned = re.sub(r"<RULE\[[^\]]+\]>", "", text)
        cleaned = re.sub(r"</RULE\[[^\]]+\]>", "", cleaned)
        cleaned = re.sub(r"</?RULE>", "", cleaned)
        cleaned = re.sub(r"</?user_rules>", "", cleaned)
        cleaned = re.sub(r"</?identity>", "", cleaned)
        cleaned = re.sub(r"</?guidelines>", "", cleaned)
        return cleaned.strip()

    def split_into_sections(self, text: str) -> List[Tuple[str, str]]:
        """
        Splits markdown into header-based sections: (title, body).
        Recognizes # and ## heading boundaries.
        """
        cleaned = self.clean_xml_tags(text)
        lines = cleaned.splitlines()
        sections: List[Tuple[str, str]] = []
        current_title = "General Guidelines"
        current_body: List[str] = []

        for line in lines:
            header_match = re.match(r"^(#{1,3})\s+(.+)$", line)
            if header_match:
                if current_body:
                    body_text = "\n".join(current_body).strip()
                    if body_text:
                        sections.append((current_title, body_text))
                    current_body = []
                current_title = header_match.group(2).strip()
            else:
                current_body.append(line)

        if current_body:
            body_text = "\n".join(current_body).strip()
            if body_text:
                sections.append((current_title, body_text))

        return sections

    def transpile_claude(self) -> str:
        """
        Transpiles to CLAUDE.md for Claude Code CLI.
        Formats high-priority instructions, test commands, and operational boundaries.
        """
        cleaned = self.clean_xml_tags(self.source_content)
        header = (
            "# CLAUDE.md — Agent Directives & Repository Guidelines\n\n"
            "> Canonical source: ~/.gemini/config/AGENTS.md\n"
            "> Auto-transpiled by Agent-Customization-Sync. Do not edit directly.\n\n"
        )
        return header + cleaned + "\n"

    def transpile_cursor(self) -> Dict[str, str]:
        """
        Transpiles to modular Cursor MDC rules and legacy .cursorrules.
        Returns a dict mapping filename -> content:
        - "rules/01-global-invariants.mdc": "..."
        - "rules/02-...mdc": "..."
        - ".cursorrules": "..."
        """
        sections = self.split_into_sections(self.source_content)
        result: Dict[str, str] = {}
        all_rules_body = []

        idx = 1
        for title, body in sections:
            slug = re.sub(r"[^\w\-]", "-", title.lower()).strip("-")
            slug = re.sub(r"-+", "-", slug)[:40]
            if not slug:
                slug = f"section-{idx}"

            filename = f"rules/{idx:02d}-{slug}.mdc"
            mdc_content = (
                "---\n"
                f"description: \"{title}\"\n"
                "globs: [\"*\"]\n"
                "alwaysApply: true\n"
                "---\n\n"
                f"# {title}\n\n"
                f"{body}\n"
            )
            result[filename] = mdc_content
            all_rules_body.append(f"# {title}\n\n{body}")
            idx += 1

        # Legacy fallback
        legacy_header = (
            "# Cursor Rules (.cursorrules)\n"
            "# Auto-transpiled from ~/.gemini/config/AGENTS.md by Agent-Customization-Sync.\n\n"
        )
        result[".cursorrules"] = legacy_header + "\n\n---\n\n".join(all_rules_body) + "\n"
        return result

    def transpile_copilot(self) -> str:
        """
        Transpiles to .github/copilot-instructions.md for GitHub Copilot.
        Clean markdown instructions with no conversational boilerplate.
        """
        cleaned = self.clean_xml_tags(self.source_content)
        header = (
            "# GitHub Copilot Instructions\n\n"
            "This file defines authoritative behavioral rules, coding standards, and verification\n"
            "workflows for all GitHub Copilot workspace operations.\n\n"
        )
        return header + cleaned + "\n"

    def transpile_codex(self) -> str:
        """
        Transpiles to ~/.codex/AGENTS.md for OpenAI Codex CLI.
        """
        cleaned = self.clean_xml_tags(self.source_content)
        header = (
            "# OpenAI Codex CLI — Agent Directives\n\n"
            "> Canonical source: ~/.gemini/config/AGENTS.md\n"
            "> Auto-transpiled by Agent-Customization-Sync.\n\n"
        )
        return header + cleaned + "\n"
