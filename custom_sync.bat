@echo off
setlocal enabledelayedexpansion

REM ============================================================================
REM custom_sync.bat - Zero-Friction Automation Wrapper for Agent-Customization-Sync
REM Directly executes the Python CLI with PYTHONPATH set to the local repository root.
REM ============================================================================

set "PYTHONPATH=%~dp0;%PYTHONPATH%"

python -m agent_customization_sync.cli %*
exit /b %ERRORLEVEL%
