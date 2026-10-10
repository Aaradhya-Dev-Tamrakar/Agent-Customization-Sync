"""
cli.py
------
Zero-friction Command Line Interface for Agent-Customization-Sync.
Pure standard-library implementation (argparse) with zero runtime dependencies.
"""

from __future__ import annotations

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List

from agent_customization_sync import __version__
from agent_customization_sync.manifest import (
    CustomizationManifest,
    sha256_file,
)
from agent_customization_sync.snapshot_engine import SnapshotEngine
from agent_customization_sync.auditor import CustomizationAuditor
from agent_customization_sync.transpilers.rules_transpiler import RulesTranspiler
from agent_customization_sync.transpilers.mcp_normalizer import MCPNormalizer
from agent_customization_sync.transpilers.skills_linker import SkillsLinker


# Ensure UTF-8 output streams on Windows terminals
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def cmd_snapshot(args: argparse.Namespace) -> int:
    src = Path(args.src) if args.src else None
    sdir = Path(args.snapshot_dir) if args.snapshot_dir else None
    engine = SnapshotEngine(source_dir=src, snapshot_dir=sdir)

    try:
        meta = engine.create_snapshot(tag=args.tag)
        print("[OK] Customization Snapshot Created Successfully")
        print(f"  Snapshot ID   : {meta.snapshot_id}")
        print(f"  Archive Path  : {meta.filepath}")
        print(f"  SHA-256 Root  : {meta.sha256_root}")
        print(f"  Token Overhead: {meta.token_overhead:,} tokens")
        print(f"  Archive Size  : {meta.size_bytes:,} bytes")
        return 0
    except Exception as e:
        print(f"[FAIL] Failed to create snapshot: {e}", file=sys.stderr)
        return 1


def cmd_list(args: argparse.Namespace) -> int:
    sdir = Path(args.snapshot_dir) if args.snapshot_dir else None
    engine = SnapshotEngine(snapshot_dir=sdir)
    snapshots = engine.list_snapshots()

    if not snapshots:
        print("No snapshots found in repository/archive directory.")
        return 0

    print("\nAvailable Customization Snapshots:")
    print("--------------------------------------------------------------------------------")
    print(f"{'Snapshot ID':<34} {'Created (UTC)':<20} {'Overhead':<10} {'Size':<10}")
    print("--------------------------------------------------------------------------------")
    for s in snapshots:
        size_kb = f"{s.size_bytes / 1024:.1f} KB"
        overhead_str = f"{s.token_overhead} tok" if s.token_overhead else "-"
        created_short = s.created_at[:19].replace("T", " ")
        print(f"{s.snapshot_id:<34} {created_short:<20} {overhead_str:<10} {size_kb:<10}")
    print("--------------------------------------------------------------------------------\n")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    src = Path(args.target) if args.target else None
    sdir = Path(args.snapshot_dir) if args.snapshot_dir else None
    engine = SnapshotEngine(source_dir=src, snapshot_dir=sdir)

    try:
        res = engine.restore_snapshot(
            snapshot_id=args.id,
            latest=args.latest,
            target_dir=src,
            create_backup=not args.no_backup,
        )
        print("[OK] Customization State Restored Successfully")
        print(f"  Snapshot ID       : {res['snapshot_id']}")
        print(f"  Target Directory  : {res['target_dir']}")
        print(f"  Restored Files    : {res['restored_count']}")
        if res.get("pre_backup_path"):
            print(f"  Pre-Restore Backup: {res['pre_backup_path']}")
        print(f"  Integrity Verified: {'PASS' if res['verification_passed'] else 'FAIL'}")
        if res.get("discrepancies"):
            for d in res["discrepancies"]:
                print(f"    - {d}", file=sys.stderr)
        return 0 if res["verification_passed"] else 1
    except Exception as e:
        print(f"[FAIL] Failed to restore snapshot: {e}", file=sys.stderr)
        return 1


def cmd_push(args: argparse.Namespace) -> int:
    src_dir = Path(args.src) if args.src else Path.home() / ".gemini" / "config"
    agents_path = src_dir / "AGENTS.md"
    mcp_path = src_dir / "mcp_config.json"
    skills_dir = src_dir / "skills"

    if not agents_path.is_file():
        print(f"[FAIL] Canonical AGENTS.md not found in {src_dir}", file=sys.stderr)
        return 1

    rt = RulesTranspiler.from_file(agents_path)
    mn = MCPNormalizer.from_file(mcp_path) if mcp_path.is_file() else MCPNormalizer()
    sl = SkillsLinker(source_skills_dir=skills_dir)

    target_all = args.all or not (args.cursor or args.claude or args.vscode or args.codex)
    mode = args.mode or "junction"
    scrub_env = args.scrub_env
    workspace = Path(args.workspace).resolve() if args.workspace else Path.cwd()

    print(f"Syncing Antigravity state ({src_dir}) to target environments...")

    # 1. Claude Code
    if target_all or args.claude:
        claude_dir = Path.home() / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)
        # Push CLAUDE.md to ~/.claude/ and optionally workspace
        (claude_dir / "CLAUDE.md").write_text(rt.transpile_claude(), encoding="utf-8")
        # Push MCP
        settings_file = claude_dir / "settings.json"
        existing_cfg = json.loads(settings_file.read_text(encoding="utf-8")) if settings_file.is_file() else {}
        updated_cfg = mn.to_claude_settings(existing_cfg, scrub_env=scrub_env)
        settings_file.write_text(json.dumps(updated_cfg, indent=2), encoding="utf-8")
        # Sync skills
        sl_res = sl.sync_to_destination(claude_dir / "skills", mode=mode)
        print(f"[OK] Claude Code updated: CLAUDE.md, settings.json, {sl_res['synced_count']} skills ({mode})")

    # 2. Cursor IDE
    if target_all or args.cursor:
        cursor_dir = Path.home() / ".cursor"
        cursor_dir.mkdir(parents=True, exist_ok=True)
        # Global MCP
        (cursor_dir / "mcp.json").write_text(
            json.dumps(mn.to_cursor(scrub_env=scrub_env), indent=2), encoding="utf-8"
        )
        # Global skills
        sl_res = sl.sync_to_destination(cursor_dir / "skills-cursor", mode=mode)
        # Workspace rules: .cursor/rules/*.mdc
        ws_rules_dir = workspace / ".cursor" / "rules"
        ws_rules_dir.mkdir(parents=True, exist_ok=True)
        cursor_rules = rt.transpile_cursor()
        for fname, content in cursor_rules.items():
            if fname.startswith("rules/"):
                leaf = Path(fname).name
                (ws_rules_dir / leaf).write_text(content, encoding="utf-8")
            elif fname == ".cursorrules":
                (workspace / ".cursorrules").write_text(content, encoding="utf-8")
        print(f"[OK] Cursor IDE updated: mcp.json, {sl_res['synced_count']} skills, modular .cursor/rules/ in workspace")

    # 3. VS Code / Copilot
    if target_all or args.vscode:
        vscode_dir = workspace / ".vscode"
        vscode_dir.mkdir(parents=True, exist_ok=True)
        (vscode_dir / "mcp.json").write_text(
            json.dumps(mn.to_vscode(scrub_env=scrub_env), indent=2), encoding="utf-8"
        )
        github_dir = workspace / ".github"
        github_dir.mkdir(parents=True, exist_ok=True)
        (github_dir / "copilot-instructions.md").write_text(
            rt.transpile_copilot(), encoding="utf-8"
        )
        # Global Copilot skills sync
        copilot_skills_dir = Path.home() / ".copilot" / "skills"
        copilot_skills_dir.mkdir(parents=True, exist_ok=True)
        sl_res = sl.sync_to_destination(copilot_skills_dir, mode=mode)
        print(f"[OK] VS Code & Copilot updated: .vscode/mcp.json, .github/copilot-instructions.md, {sl_res['synced_count']} skills ({mode})")

    # 4. OpenAI Codex CLI
    if target_all or args.codex:
        codex_dir = Path.home() / ".codex"
        codex_dir.mkdir(parents=True, exist_ok=True)
        (codex_dir / "AGENTS.md").write_text(rt.transpile_codex(), encoding="utf-8")
        print("[OK] Codex CLI updated: ~/.codex/AGENTS.md")

    print("\n[OK] Push synchronization completed across all designated environments.\n")
    return 0


def cmd_audit(args: argparse.Namespace) -> int:
    src_dir = Path(args.src) if args.src else None
    auditor = CustomizationAuditor(source_dir=src_dir)

    print("\n========================================================")
    print(" 1. CROSS-IDE CUSTOMIZATION DRIFT AUDIT")
    print("========================================================")
    drift = auditor.audit_drift()
    print(drift.to_table())
    print(f"Overall Drift Status: {drift.overall_status}\n")

    print("========================================================")
    print(" 2. TOKEN BUDGET OVERHEAD AUDIT")
    print("========================================================")
    tb = auditor.audit_token_budget()
    print(tb.to_table())
    print()

    return 0 if (drift.in_sync and tb.is_compliant) else (0 if tb.is_compliant else 1)


def cmd_status(args: argparse.Namespace) -> int:
    src_dir = Path(args.src) if args.src else Path.home() / ".gemini" / "config"
    sdir = Path(args.snapshot_dir) if args.snapshot_dir else None
    engine = SnapshotEngine(source_dir=src_dir, snapshot_dir=sdir)
    manifest = CustomizationManifest.from_dir(src_dir)

    print("\n========================================================")
    print(f" AGENT CUSTOMIZATION SYNC TELEMETRY (v{__version__})")
    print("========================================================")
    print(f"Source Directory    : {src_dir}")
    print(f"Rules Monitored     : {len(manifest.rules)} ({', '.join(manifest.rules.keys())})")
    print(f"Skills Monitored    : {len(manifest.skills)}")
    print(f"MCP Servers Active  : {len(manifest.mcp_servers)}")
    print(f"Static Token Cost   : {manifest.total_token_overhead:,} tokens ({manifest.headroom_percent:.1f}% headroom)")
    print(f"Root SHA-256 Digest : {manifest.sha256_root}")

    snapshots = engine.list_snapshots()
    print(f"Snapshots Available : {len(snapshots)} (Ring buffer capacity: {engine.max_snapshots})")
    if snapshots:
        print(f"Latest Snapshot     : {snapshots[0].snapshot_id} ({snapshots[0].created_at})")
    print("========================================================\n")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="custom-sync",
        description="Antigravity Customization State Saving, Snapshotting, and Cross-IDE Syncing Engine",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # snapshot
    p_snap = subparsers.add_parser("snapshot", help="Create a timestamped state snapshot checkpoint")
    p_snap.add_argument("--tag", "-t", type=str, help="Optional descriptive tag for the snapshot")
    p_snap.add_argument("--src", type=str, help="Custom source configuration directory")
    p_snap.add_argument("--snapshot-dir", type=str, help="Custom snapshot storage directory")

    # list
    p_list = subparsers.add_parser("list", help="List all available state snapshots in ring buffer")
    p_list.add_argument("--snapshot-dir", type=str, help="Custom snapshot storage directory")

    # restore
    p_rest = subparsers.add_parser("restore", help="Restore configuration from a designated snapshot")
    p_rest.add_argument("--id", type=str, help="Snapshot ID or substring to restore")
    p_rest.add_argument("--latest", "-l", action="store_true", help="Restore the latest snapshot")
    p_rest.add_argument("--target", type=str, help="Target restoration directory")
    p_rest.add_argument("--snapshot-dir", type=str, help="Custom snapshot storage directory")
    p_rest.add_argument("--no-backup", action="store_true", help="Skip safety pre-restore backup")

    # push
    p_push = subparsers.add_parser("push", help="Transpile and project configuration to target IDEs")
    p_push.add_argument("--all", action="store_true", help="Push to all supported environments")
    p_push.add_argument("--cursor", action="store_true", help="Push to Cursor IDE")
    p_push.add_argument("--claude", action="store_true", help="Push to Claude Code CLI")
    p_push.add_argument("--vscode", action="store_true", help="Push to VS Code / Copilot")
    p_push.add_argument("--codex", action="store_true", help="Push to OpenAI Codex CLI")
    p_push.add_argument("--workspace", "-w", type=str, help="Workspace directory for project-scoped rules")
    p_push.add_argument("--src", type=str, help="Custom source configuration directory")
    p_push.add_argument("--mode", choices=["junction", "copy"], default="junction", help="Skill synchronization mode")
    p_push.add_argument("--scrub-env", action="store_true", help="Mask sensitive environment variables in target configs")

    # audit
    p_audit = subparsers.add_parser("audit", help="Run cross-IDE drift and token budget audits")
    p_audit.add_argument("--src", type=str, help="Custom source configuration directory")

    # status
    p_stat = subparsers.add_parser("status", help="Show system status and customization metrics")
    p_stat.add_argument("--src", type=str, help="Custom source configuration directory")
    p_stat.add_argument("--snapshot-dir", type=str, help="Custom snapshot storage directory")

    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "snapshot": cmd_snapshot,
        "list": cmd_list,
        "restore": cmd_restore,
        "push": cmd_push,
        "audit": cmd_audit,
        "status": cmd_status,
    }
    handler = commands.get(args.command)
    if handler:
        return handler(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
