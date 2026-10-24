"""
local_bin_provisioner.py
------------------------
Provisions, audits, and maintains global CLI wrapper shims in ~/.local/bin.
Guarantees friction-free access to ghw, gh.bat, gh-workflow, gh-task, and toggle-issue-task
from any directory on Windows without PATH collisions or manual environment setup.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

GH_BAT_TEMPLATE = """@echo off
setlocal
REM Global GitHub Workflow CLI Shim
set "GLOBAL_PS1=%USERPROFILE%\\.gemini\\config\\skills\\github-workflow\\scripts\\gh.ps1"
set "TARGET_PS1=%GLOBAL_PS1%"

if exist ".\\gh.ps1" (
    for %%F in (".\\gh.ps1") do set "LOCAL_RESOLVED=%%~fF"
    if /I not "%~f0"=="%LOCAL_RESOLVED%" (
        set "TARGET_PS1=.\\gh.ps1"
    )
)

where pwsh >nul 2>nul
if %ERRORLEVEL% equ 0 (
    pwsh -NoProfile -ExecutionPolicy Bypass -File "%TARGET_PS1%" %*
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%TARGET_PS1%" %*
)
exit /b %ERRORLEVEL%
"""

GH_PS1_TEMPLATE = """$globalPs1 = Join-Path $HOME ".gemini\\config\\skills\\github-workflow\\scripts\\gh.ps1"
$currentPs1 = Join-Path (Get-Location).Path "gh.ps1"

$targetPs1 = if ((Test-Path $currentPs1) -and ((Resolve-Path $currentPs1).Path -ine (Resolve-Path $MyInvocation.MyCommand.Path).Path)) {
    (Resolve-Path $currentPs1).Path
} else {
    $globalPs1
}

if (-not (Test-Path $targetPs1)) {
    throw "Target gh.ps1 not found at $targetPs1"
}

& $targetPs1 @args
exit $LASTEXITCODE
"""

GH_TASK_BAT_TEMPLATE = """@echo off
setlocal
set "GLOBAL_PY=%USERPROFILE%\\.gemini\\config\\skills\\github-workflow\\scripts\\toggle_issue_task.py"
if exist "%GLOBAL_PY%" (
    python "%GLOBAL_PY%" %*
) else (
    python "%USERPROFILE%\\.gemini\\config\\skills\\github-issue-pr-workflow\\scripts\\toggle_issue_task.py" %*
)
exit /b %ERRORLEVEL%
"""

GH_TASK_PS1_TEMPLATE = """$script = Join-Path $HOME ".gemini\\config\\skills\\github-workflow\\scripts\\toggle_issue_task.py"
if (-not (Test-Path $script)) {
    $script = Join-Path $HOME ".gemini\\config\\skills\\github-issue-pr-workflow\\scripts\\toggle_issue_task.py"
}
python $script @args
exit $LASTEXITCODE
"""


class LocalBinProvisioner:
    """Manages global executable shims in ~/.local/bin."""

    def __init__(self, bin_dir: Path | None = None):
        self.bin_dir = bin_dir or (Path.home() / ".local" / "bin")

    def get_shim_definitions(self) -> dict[str, str]:
        """Returns map of expected shim filenames to their canonical content."""
        return {
            "ghw.bat": GH_BAT_TEMPLATE,
            "ghw.ps1": GH_PS1_TEMPLATE,
            "gh.bat": GH_BAT_TEMPLATE,
            "gh.ps1": GH_PS1_TEMPLATE,
            "gh-workflow.bat": GH_BAT_TEMPLATE,
            "gh-workflow.ps1": GH_PS1_TEMPLATE,
            "gh-task.bat": GH_TASK_BAT_TEMPLATE,
            "gh-task.ps1": GH_TASK_PS1_TEMPLATE,
            "toggle-issue-task.bat": GH_TASK_BAT_TEMPLATE,
            "toggle-issue-task.ps1": GH_TASK_PS1_TEMPLATE,
        }

    def is_in_system_path(self) -> bool:
        """Checks if self.bin_dir is in the current environment PATH."""
        path_dirs = [Path(p).resolve() for p in os.environ.get("PATH", "").split(os.pathsep) if p.strip()]
        target = self.bin_dir.resolve()
        return target in path_dirs

    def audit(self) -> dict[str, Any]:
        """Audits current ~/.local/bin status against canonical definitions."""
        expected = self.get_shim_definitions()
        in_path = self.is_in_system_path()
        bin_exists = self.bin_dir.is_dir()

        present: list[str] = []
        missing: list[str] = []
        drifted: list[str] = []

        for name, content in expected.items():
            file_path = self.bin_dir / name
            if not file_path.is_file():
                missing.append(name)
            else:
                try:
                    current_content = file_path.read_bytes().decode("utf-8", errors="replace")
                    # Normalize line endings for comparison
                    if current_content.replace("\r\n", "\n").strip() == content.replace("\r\n", "\n").strip():
                        present.append(name)
                    else:
                        drifted.append(name)
                except Exception:
                    drifted.append(name)

        is_default = self.bin_dir.resolve() == (Path.home() / ".local" / "bin").resolve()
        is_healthy = (in_path or not is_default) and bin_exists and len(missing) == 0 and len(drifted) == 0

        return {
            "bin_dir": str(self.bin_dir),
            "bin_exists": bin_exists,
            "in_path": in_path,
            "healthy": is_healthy,
            "total_expected": len(expected),
            "present_count": len(present),
            "present": present,
            "missing": missing,
            "drifted": drifted,
        }

    def provision(self, overwrite: bool = True) -> dict[str, Any]:
        """Creates or updates all canonical shims in self.bin_dir."""
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        expected = self.get_shim_definitions()

        created: list[str] = []
        updated: list[str] = []
        skipped: list[str] = []

        for name, content in expected.items():
            file_path = self.bin_dir / name
            newline = "\r\n" if name.endswith(".bat") else "\n"
            normalized_content = content.replace("\r\n", "\n").replace("\n", newline)
            raw_bytes = normalized_content.encode("utf-8")

            if not file_path.exists():
                file_path.write_bytes(raw_bytes)
                created.append(name)
            elif overwrite:
                current_bytes = file_path.read_bytes()
                if current_bytes != raw_bytes:
                    file_path.write_bytes(raw_bytes)
                    updated.append(name)
                else:
                    skipped.append(name)
            else:
                skipped.append(name)

        return {
            "bin_dir": str(self.bin_dir),
            "created": created,
            "updated": updated,
            "skipped": skipped,
            "in_path": self.is_in_system_path(),
        }
