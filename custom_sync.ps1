<#
.SYNOPSIS
Zero-friction PowerShell automation wrapper for Agent-Customization-Sync.

.DESCRIPTION
Provides execution parity and convenient switches for snapshotting, auditing,
and cross-IDE synchronization of Antigravity customization state.

.EXAMPLE
.\custom_sync.ps1 -Snapshot -Tag "pre-exp"
.\custom_sync.ps1 -Audit
.\custom_sync.ps1 -Push -All
.\custom_sync.ps1 -Restore -Latest
#>

[CmdletBinding(DefaultParameterSetName = "Default")]
param(
    [Parameter(ParameterSetName = "Snapshot")]
    [switch]$Snapshot,

    [Parameter(ParameterSetName = "Snapshot")]
    [string]$Tag,

    [Parameter(ParameterSetName = "List")]
    [switch]$List,

    [Parameter(ParameterSetName = "Audit")]
    [switch]$Audit,

    [Parameter(ParameterSetName = "Status")]
    [switch]$Status,

    [Parameter(ParameterSetName = "Push")]
    [switch]$Push,

    [Parameter(ParameterSetName = "Push")]
    [switch]$All,

    [Parameter(ParameterSetName = "Push")]
    [switch]$Cursor,

    [Parameter(ParameterSetName = "Push")]
    [switch]$Claude,

    [Parameter(ParameterSetName = "Push")]
    [switch]$VSCode,

    [Parameter(ParameterSetName = "Push")]
    [switch]$Codex,

    [Parameter(ParameterSetName = "Push")]
    [ValidateSet("junction", "copy")]
    [string]$Mode = "junction",

    [Parameter(ParameterSetName = "Restore")]
    [switch]$Restore,

    [Parameter(ParameterSetName = "Restore")]
    [switch]$Latest,

    [Parameter(ParameterSetName = "Restore")]
    [string]$Id,

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

$RepoRoot = $PSScriptRoot
$env:PYTHONPATH = "$RepoRoot;$($env:PYTHONPATH)"

$cliArgs = @()

if ($Snapshot) {
    $cliArgs += "snapshot"
    if ($Tag) { $cliArgs += @("--tag", $Tag) }
}
elseif ($List) {
    $cliArgs += "list"
}
elseif ($Audit) {
    $cliArgs += "audit"
}
elseif ($Status) {
    $cliArgs += "status"
}
elseif ($Push) {
    $cliArgs += "push"
    if ($All) { $cliArgs += "--all" }
    if ($Cursor) { $cliArgs += "--cursor" }
    if ($Claude) { $cliArgs += "--claude" }
    if ($VSCode) { $cliArgs += "--vscode" }
    if ($Codex) { $cliArgs += "--codex" }
    if ($Mode) { $cliArgs += @("--mode", $Mode) }
}
elseif ($Restore) {
    $cliArgs += "restore"
    if ($Latest) { $cliArgs += "--latest" }
    if ($Id) { $cliArgs += @("--id", $Id) }
}
elseif ($RemainingArgs) {
    $cliArgs += $RemainingArgs
}
else {
    $cliArgs += "status"
}

python -m agent_customization_sync.cli @cliArgs
exit $LASTEXITCODE
