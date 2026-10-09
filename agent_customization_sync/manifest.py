"""
manifest.py
-----------
Cryptographic manifest data models, deterministic hashing, and token budget estimation
for Antigravity and cross-IDE customizations.
"""

from __future__ import annotations

import os
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple


def estimate_tokens(text: str) -> int:
    """
    Calibrated token budget estimator for code, markdown, and configuration text.
    Uses a hybrid character-to-word metric aligned with standard BPE tokenizers
    (~3.8 - 4.0 chars/token on prose, ~3.2 chars/token on structured code/JSON).
    """
    if not text:
        return 0
    char_count = len(text)
    words = len(text.split())
    # Blend character estimate (1 token ~ 3.7 chars) with word count (1 word ~ 1.3 tokens)
    char_estimate = char_count / 3.7
    word_estimate = words * 1.3
    return int(max(char_estimate, word_estimate))


def sha256_bytes(data: bytes) -> str:
    """Computes standard hex SHA-256 digest of byte array."""
    h = hashlib.sha256()
    h.update(data)
    return h.hexdigest()


def sha256_file(path: Path) -> str:
    """Computes SHA-256 digest of a single file in 64KB chunks."""
    if not path.is_file():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def sha256_dir(path: Path, skip_dirs: Optional[set[str]] = None) -> Tuple[str, int, int]:
    """
    Computes a deterministic Merkle-style SHA-256 digest, total file count,
    and estimated token overhead of all files within a directory.
    """
    if skip_dirs is None:
        skip_dirs = {".git", ".pytest_cache", "__pycache__", "node_modules", ".venv"}

    if not path.is_dir():
        return "", 0, 0

    h = hashlib.sha256()
    file_count = 0
    total_tokens = 0

    for root, dirs, files in os.walk(path):
        dirs[:] = sorted([d for d in dirs if d not in skip_dirs])
        for filename in sorted(files):
            file_path = Path(root) / filename
            try:
                rel_path = file_path.relative_to(path).as_posix()
                content = file_path.read_bytes()
                file_hash = hashlib.sha256(content).hexdigest()
                h.update(f"{rel_path}:{file_hash}".encode("utf-8"))
                file_count += 1
                try:
                    text_str = content.decode("utf-8", errors="ignore")
                    total_tokens += estimate_tokens(text_str)
                except Exception:
                    pass
            except Exception:
                continue

    return h.hexdigest(), file_count, total_tokens


@dataclass
class RuleManifestEntry:
    name: str
    relative_path: str
    sha256: str
    line_count: int
    token_estimate: int


@dataclass
class SkillManifestEntry:
    name: str
    path: str
    sha256: str
    files_count: int
    token_estimate: int
    is_junction: bool = False
    target_paths: List[str] = field(default_factory=list)


@dataclass
class MCPServerEntry:
    name: str
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    env_keys: List[str] = field(default_factory=list)
    disabled: bool = False
    server_url: Optional[str] = None


@dataclass
class CustomizationManifest:
    schema_version: str = "1.0.0"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_path: str = ""
    rules: Dict[str, RuleManifestEntry] = field(default_factory=dict)
    skills: Dict[str, SkillManifestEntry] = field(default_factory=dict)
    mcp_servers: Dict[str, MCPServerEntry] = field(default_factory=dict)
    settings_hash: str = ""
    total_token_overhead: int = 0
    headroom_percent: float = 100.0
    sha256_root: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CustomizationManifest:
        rules = {
            k: RuleManifestEntry(**v) for k, v in data.get("rules", {}).items()
        }
        skills = {
            k: SkillManifestEntry(**v) for k, v in data.get("skills", {}).items()
        }
        mcp_servers = {
            k: MCPServerEntry(**v) for k, v in data.get("mcp_servers", {}).items()
        }
        return cls(
            schema_version=data.get("schema_version", "1.0.0"),
            created_at=data.get("created_at", ""),
            source_path=data.get("source_path", ""),
            rules=rules,
            skills=skills,
            mcp_servers=mcp_servers,
            settings_hash=data.get("settings_hash", ""),
            total_token_overhead=data.get("total_token_overhead", 0),
            headroom_percent=data.get("headroom_percent", 100.0),
            sha256_root=data.get("sha256_root", ""),
        )

    @classmethod
    def from_json(cls, json_str: str) -> CustomizationManifest:
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def from_dir(cls, config_dir: Path) -> CustomizationManifest:
        """
        Inspects an Antigravity config directory (e.g. ~/.gemini/config/) and builds
        a deterministic CustomizationManifest with component digests and token metrics.
        """
        config_path = Path(config_dir).resolve()
        rules: Dict[str, RuleManifestEntry] = {}
        skills: Dict[str, SkillManifestEntry] = {}
        mcp_servers: Dict[str, MCPServerEntry] = {}
        settings_hash = ""
        total_tokens = 0

        # 1. Rules: AGENTS.md, GEMINI.md
        for rule_file in ["AGENTS.md", "GEMINI.md"]:
            rf_path = config_path / rule_file
            if rf_path.is_file():
                try:
                    text = rf_path.read_text(encoding="utf-8", errors="ignore")
                    lines = len(text.splitlines())
                    tokens = estimate_tokens(text)
                    total_tokens += tokens
                    rules[rule_file] = RuleManifestEntry(
                        name=rule_file,
                        relative_path=rule_file,
                        sha256=sha256_file(rf_path),
                        line_count=lines,
                        token_estimate=tokens,
                    )
                except Exception:
                    pass

        # 2. Skills: skills/
        skills_dir = config_path / "skills"
        if skills_dir.is_dir():
            for item in sorted(skills_dir.iterdir()):
                if item.is_dir() and not item.name.startswith("."):
                    h, f_count, tokens = sha256_dir(item)
                    total_tokens += tokens
                    is_junc = False
                    try:
                        is_junc = item.is_symlink() or os.path.islink(str(item))
                    except Exception:
                        pass
                    skills[item.name] = SkillManifestEntry(
                        name=item.name,
                        path=str(item),
                        sha256=h,
                        files_count=f_count,
                        token_estimate=tokens,
                        is_junction=is_junc,
                    )

        # 3. MCP Servers: mcp_config.json
        mcp_file = config_path / "mcp_config.json"
        if mcp_file.is_file():
            try:
                mcp_data = json.loads(mcp_file.read_text(encoding="utf-8"))
                servers = mcp_data.get("mcpServers", {})
                for name, s_cfg in sorted(servers.items()):
                    env_keys = list(s_cfg.get("env", {}).keys()) if isinstance(s_cfg.get("env"), dict) else []
                    mcp_servers[name] = MCPServerEntry(
                        name=name,
                        command=s_cfg.get("command"),
                        args=s_cfg.get("args", []),
                        env_keys=env_keys,
                        disabled=s_cfg.get("disabled", False),
                        server_url=s_cfg.get("serverUrl"),
                    )
                mcp_tokens = estimate_tokens(mcp_file.read_text(encoding="utf-8"))
                total_tokens += mcp_tokens
            except Exception:
                pass

        # 4. Settings: config.json
        cfg_file = config_path / "config.json"
        if cfg_file.is_file():
            settings_hash = sha256_file(cfg_file)
            try:
                total_tokens += estimate_tokens(cfg_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        # Compute Merkle root hash across all components
        root_hasher = hashlib.sha256()
        for k in sorted(rules.keys()):
            root_hasher.update(f"rule:{k}:{rules[k].sha256}".encode())
        for k in sorted(skills.keys()):
            root_hasher.update(f"skill:{k}:{skills[k].sha256}".encode())
        for k in sorted(mcp_servers.keys()):
            root_hasher.update(f"mcp:{k}:{mcp_servers[k].disabled}".encode())
        if settings_hash:
            root_hasher.update(f"settings:{settings_hash}".encode())

        sha256_root = root_hasher.hexdigest()

        # Context ceiling calculation (Standard 20k token prefix budget target)
        prefix_budget = 20000
        headroom_percent = max(0.0, round(((prefix_budget - total_tokens) / prefix_budget) * 100, 2))

        return cls(
            schema_version="1.0.0",
            created_at=datetime.now(timezone.utc).isoformat(),
            source_path=str(config_path),
            rules=rules,
            skills=skills,
            mcp_servers=mcp_servers,
            settings_hash=settings_hash,
            total_token_overhead=total_tokens,
            headroom_percent=headroom_percent,
            sha256_root=sha256_root,
        )
