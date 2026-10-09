"""
auditor.py
----------
Drift & Token Budget Auditor for Antigravity and multi-IDE customizations.
Detects configuration skew across Antigravity, Claude Code, Cursor, and Copilot,
and strictly enforces the <8,000 token static overhead ceiling (>=60% context headroom).
"""

from __future__ import annotations

import os
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple

from agent_customization_sync.manifest import (
    CustomizationManifest,
    estimate_tokens,
    sha256_file,
    sha256_dir,
)
from agent_customization_sync.transpilers.rules_transpiler import RulesTranspiler
from agent_customization_sync.transpilers.mcp_normalizer import MCPNormalizer


@dataclass
class DriftItem:
    component: str
    target_ide: str
    path: str
    status: str  # "MATCH", "DRIFTED", "MISSING", "EXTRA"
    details: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DriftReport:
    overall_status: str  # "IN_SYNC", "DRIFT_DETECTED", "UNCONFIGURED"
    source_path: str
    inspected_targets: List[str]
    items: List[DriftItem] = field(default_factory=list)

    @property
    def in_sync(self) -> bool:
        return all(item.status == "MATCH" for item in self.items)

    def to_table(self) -> str:
        """Renders an ASCII table representation of drift results."""
        if not self.items:
            return "No customization items checked."

        headers = ["Target IDE", "Component", "Status", "Path / Details"]
        col_w = [12, 16, 10, 48]

        line_fmt = "| {:" + str(col_w[0]) + "} | {:" + str(col_w[1]) + "} | {:" + str(col_w[2]) + "} | {:" + str(col_w[3]) + "} |"
        sep = "+-" + "-+-".join("-" * w for w in col_w) + "-+"

        rows = [sep, line_fmt.format(*headers), sep]
        for it in self.items:
            trunc_path = it.path if len(it.path) <= 45 else "..." + it.path[-42:]
            details_str = f"{trunc_path} ({it.details})" if it.details else trunc_path
            if len(details_str) > col_w[3]:
                details_str = details_str[: col_w[3] - 3] + "..."
            rows.append(line_fmt.format(it.target_ide, it.component, it.status, details_str))
        rows.append(sep)
        return "\n".join(rows)


@dataclass
class TokenConsumer:
    name: str
    category: str
    tokens: int
    percentage: float


@dataclass
class TokenBudgetReport:
    total_tokens: int
    budget_ceiling: int
    headroom_percent: float
    is_compliant: bool
    top_consumers: List[TokenConsumer] = field(default_factory=list)

    def to_table(self) -> str:
        status_str = "COMPLIANT" if self.is_compliant else "EXCEEDED"
        out = [
            f"Token Budget Audit: {status_str}",
            f"Total Overhead  : {self.total_tokens:,} tokens (Ceiling: {self.budget_ceiling:,} tokens)",
            f"Context Headroom: {self.headroom_percent:.1f}% (Minimum: 60.0%)",
            "",
            "Top Token Consumers:",
            "-------------------------------------------------------------",
            f"{'Asset':<32} {'Category':<14} {'Tokens':<8} {'Share':<6}",
            "-------------------------------------------------------------",
        ]
        for c in self.top_consumers[:10]:
            out.append(f"{c.name[:30]:<32} {c.category:<14} {c.tokens:<8} {c.percentage:.1f}%")
        out.append("-------------------------------------------------------------")
        return "\n".join(out)


class CustomizationAuditor:
    """
    Audits state drift across IDEs and enforces token budget boundaries.
    """

    TOKEN_CEILING = 8000
    PREFIX_BUDGET = 20000

    def __init__(self, source_dir: Optional[Path] = None):
        self.source_dir = (
            Path(source_dir).resolve()
            if source_dir
            else Path.home() / ".gemini" / "config"
        )

    def audit_drift(
        self,
        claude_dir: Optional[Path] = None,
        cursor_dir: Optional[Path] = None,
        workspace_dir: Optional[Path] = None,
    ) -> DriftReport:
        """
        Audits configuration drift across Claude, Cursor, and workspace environments.
        """
        claude_base = Path(claude_dir).resolve() if claude_dir else Path.home() / ".claude"
        cursor_base = Path(cursor_dir).resolve() if cursor_dir else Path.home() / ".cursor"
        workspace_base = Path(workspace_dir).resolve() if workspace_dir else Path.cwd()

        items: List[DriftItem] = []
        inspected = []

        manifest = CustomizationManifest.from_dir(self.source_dir)
        source_agents_path = self.source_dir / "AGENTS.md"
        source_mcp_path = self.source_dir / "mcp_config.json"

        # 1. Check Claude Code
        inspected.append("Claude Code")
        claude_rules_path = claude_base / "CLAUDE.md"
        if not claude_rules_path.exists():
            items.append(
                DriftItem("Rules", "Claude Code", str(claude_rules_path), "MISSING", "CLAUDE.md not found")
            )
        else:
            items.append(
                DriftItem("Rules", "Claude Code", str(claude_rules_path), "MATCH", "Present")
            )

        claude_skills_dir = claude_base / "skills"
        if not claude_skills_dir.is_dir():
            items.append(
                DriftItem("Skills", "Claude Code", str(claude_skills_dir), "MISSING", "Directory not found")
            )
        else:
            claude_skills = {p.name for p in claude_skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")}
            src_skills = set(manifest.skills.keys())
            missing = src_skills - claude_skills
            if missing:
                items.append(
                    DriftItem("Skills", "Claude Code", str(claude_skills_dir), "DRIFTED", f"Missing {len(missing)} skills")
                )
            else:
                items.append(
                    DriftItem("Skills", "Claude Code", str(claude_skills_dir), "MATCH", f"All {len(src_skills)} skills present")
                )

        # 2. Check Cursor IDE
        inspected.append("Cursor IDE")
        cursor_skills_dir = cursor_base / "skills-cursor"
        if not cursor_skills_dir.is_dir():
            items.append(
                DriftItem("Skills", "Cursor IDE", str(cursor_skills_dir), "MISSING", "skills-cursor dir missing")
            )
        else:
            cursor_skills = {p.name for p in cursor_skills_dir.iterdir() if p.is_dir() and not p.name.startswith(".")}
            src_skills = set(manifest.skills.keys())
            missing = src_skills - cursor_skills
            if missing:
                items.append(
                    DriftItem("Skills", "Cursor IDE", str(cursor_skills_dir), "DRIFTED", f"Missing {len(missing)} skills")
                )
            else:
                items.append(
                    DriftItem("Skills", "Cursor IDE", str(cursor_skills_dir), "MATCH", f"All {len(src_skills)} skills present")
                )

        cursor_mcp_path = cursor_base / "mcp.json"
        if not cursor_mcp_path.exists():
            items.append(
                DriftItem("MCP Servers", "Cursor IDE", str(cursor_mcp_path), "MISSING", "mcp.json not found")
            )
        else:
            items.append(
                DriftItem("MCP Servers", "Cursor IDE", str(cursor_mcp_path), "MATCH", "mcp.json present")
            )

        # 3. Check Workspace Copilot & Rules
        inspected.append("Workspace Copilot")
        copilot_inst = workspace_base / ".github" / "copilot-instructions.md"
        if not copilot_inst.exists():
            items.append(
                DriftItem("Copilot Rules", "Workspace", str(copilot_inst), "MISSING", "copilot-instructions.md missing")
            )
        else:
            items.append(
                DriftItem("Copilot Rules", "Workspace", str(copilot_inst), "MATCH", "Present")
            )

        overall = "IN_SYNC" if all(it.status == "MATCH" for it in items) else "DRIFT_DETECTED"
        return DriftReport(
            overall_status=overall,
            source_path=str(self.source_dir),
            inspected_targets=inspected,
            items=items,
        )

    def audit_token_budget(
        self,
        manifest: Optional[CustomizationManifest] = None,
    ) -> TokenBudgetReport:
        """
        Calculates total token overhead and validates against the 8,000 token ceiling.
        """
        if manifest is None:
            manifest = CustomizationManifest.from_dir(self.source_dir)

        total_tokens = manifest.total_token_overhead
        consumers: List[TokenConsumer] = []

        for name, r in manifest.rules.items():
            pct = (r.token_estimate / total_tokens * 100) if total_tokens else 0
            consumers.append(TokenConsumer(name, "Rule", r.token_estimate, pct))

        for name, s in manifest.skills.items():
            pct = (s.token_estimate / total_tokens * 100) if total_tokens else 0
            consumers.append(TokenConsumer(name, "Skill", s.token_estimate, pct))

        consumers.sort(key=lambda c: c.tokens, reverse=True)

        headroom_percent = max(0.0, round(((self.PREFIX_BUDGET - total_tokens) / self.PREFIX_BUDGET) * 100, 2))
        is_compliant = total_tokens <= self.TOKEN_CEILING and headroom_percent >= 60.0

        return TokenBudgetReport(
            total_tokens=total_tokens,
            budget_ceiling=self.TOKEN_CEILING,
            headroom_percent=headroom_percent,
            is_compliant=is_compliant,
            top_consumers=consumers,
        )
