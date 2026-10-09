<#
.SYNOPSIS
Safely sync a Git repo, check staged changes for secrets, and commit when appropriate.

.DESCRIPTION
Pulls the latest changes from the configured origin remote, prevents accidental credential
commits, and exits cleanly when there is nothing to commit.
#>

[CmdletBinding()]
param (
    [Alias("m")]
    [string]$Message,

    [switch]$PullOnly,

    [Alias("NoCI", "SkipActions")]
    [switch]$SkipCI
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-Status {
    param(
        [string]$Message,
        [System.ConsoleColor]$Color = [System.ConsoleColor]::Cyan
    )
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $Message" -ForegroundColor $Color
}

function Write-Notice {
    param([string]$Message)
    Write-Status -Message $Message -Color ([System.ConsoleColor]::Yellow)
}

function Write-Success {
    param([string]$Message)
    Write-Status -Message $Message -Color ([System.ConsoleColor]::Green)
}

function Find-StagedSecrets {
    $stagedDiff = git diff --cached -U0 2>$null
    if (-not $stagedDiff) { return @() }

    $addedLines = $stagedDiff | Where-Object { $_ -match '^\+[^+]' } | ForEach-Object { $_.Substring(1) }
    if (-not $addedLines) { return @() }

    $secretPatterns = @(
        'AKIA[0-9A-Z]{16}'
        'sk-[a-zA-Z0-9]{20,}'
        'sk-ant-[a-zA-Z0-9\-]{20,}'
        'ghp_[a-zA-Z0-9]{36}'
        'github_pat_[a-zA-Z0-9_]{20,}'
        'AIza[0-9A-Za-z\-_]{35}'
        'xox[baprs]-[0-9a-zA-Z\-]{10,}'
        '-----BEGIN (RSA|EC|OPENSSH|PGP|DSA)? ?PRIVATE KEY-----'
        '(?i)(api[_-]?key|secret|password|token|passwd)\s*[:=]\s*[''"][^''"\s]{8,}[''"]'
    )

    $hits = @()
    foreach ($line in $addedLines) {
        foreach ($pattern in $secretPatterns) {
            if ($line -match $pattern) {
                $snippet = $line.Trim()
                $hits += [PSCustomObject]@{
                    Pattern = $pattern
                    Snippet = $snippet.Substring(0, [Math]::Min(60, $snippet.Length))
                }
                break
            }
        }
    }

    return @($hits)
}

function Get-AutoCommitMessage {
    $statusLines = git status --porcelain
    if (-not $statusLines) {
        return "chore: synchronization checkpoint"
    }

    $files = $statusLines | ForEach-Object {
        $parts = $_.Trim() -split '\s+', 2
        if ($parts.Length -gt 1) { $parts[1] } else { $parts[0] }
    }

    $hasCode = $false
    $hasTest = $false
    $hasDocs = $false

    foreach ($file in $files) {
        if ($file -match '^(tests/|test_)') { $hasTest = $true }
        elseif ($file -match '\.(md|txt|rst)$') { $hasDocs = $true }
        elseif ($file -match '\.(py|ps1|bat|json|toml)$') { $hasCode = $true }
    }

    if ($hasTest -and -not $hasCode) {
        return "test: update test suite and verification fixtures"
    }
    if ($hasDocs -and -not $hasCode) {
        return "docs: update documentation and specifications"
    }
    if ($hasCode) {
        return "feat(sync): update customization state and cross-ide engine"
    }
    return "chore: routine repository synchronization"
}

$repoPath = $PSScriptRoot
Push-Location $repoPath

try {
    # Check git repo status
    if (-not (Test-Path ".git")) {
        Write-Error "Not a git repository: $repoPath"
        exit 1
    }

    $currentBranch = (git branch --show-current 2>$null)
    if (-not $currentBranch) { $currentBranch = "main" }

    # Check remote origin
    $remotes = git remote 2>$null
    $hasOrigin = $remotes -contains "origin"

    if ($hasOrigin) {
        Write-Status "Checking remote origin updates..."
        try {
            git pull --rebase --autostash origin $currentBranch 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "Pulled latest updates from origin/$currentBranch."
            }
        }
        catch {
            Write-Notice "Remote branch not ready or diverged; skipping pull."
        }
    }

    if ($PullOnly) {
        Write-Success "PullOnly requested. Finished."
        exit 0
    }

    # Stage all changes
    git add -A

    # Secret scanner guard
    $secretHits = @(Find-StagedSecrets)
    if ($secretHits.Length -gt 0) {
        Write-Host "FATAL: Potential credentials detected in staged diff:" -ForegroundColor Red
        foreach ($h in $secretHits) {
            Write-Host "  Pattern: $($h.Pattern)" -ForegroundColor Red
            Write-Host "  Snippet: $($h.Snippet)" -ForegroundColor DarkRed
        }
        git reset HEAD 2>$null
        exit 1
    }

    # Check if there are staged changes
    $staged = git diff --cached --quiet 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Clean working tree, nothing to commit."
        exit 0
    }

    # Determine commit message
    $commitMsg = if ($Message) { $Message } else { Get-AutoCommitMessage }
    if ($SkipCI -and $commitMsg -notmatch '(?i)\[skip ci\]') {
        $commitMsg = "$commitMsg [skip ci]"
    }

    Write-Status "Committing changes: $commitMsg"
    git commit -m $commitMsg

    if ($hasOrigin) {
        Write-Status "Pushing to origin/$currentBranch..."
        git push origin $currentBranch 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Pushed to origin/$currentBranch successfully."
        }
        else {
            Write-Notice "Push failed or remote upstream not set. Commit preserved locally."
        }
    }
    else {
        Write-Success "Committed locally. Remote 'origin' not configured yet."
    }
}
finally {
    Pop-Location
}
