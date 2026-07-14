#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptName = Split-Path -Leaf $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Source = Join-Path $RepoRoot "agents\global\AGENTS.md"

$MarkerStart = "<!-- agent-documentation:global-agents:start -->"
$MarkerEnd = "<!-- agent-documentation:global-agents:end -->"

$Targets = @(
  (Join-Path $HOME ".grok\AGENTS.md"),
  (Join-Path $HOME ".cursor\AGENTS.md"),
  (Join-Path $HOME ".codex\AGENTS.md"),
  (Join-Path $HOME ".kimi-code\AGENTS.md")
)

function Show-Usage {
  Write-Host @"
Usage: $ScriptName

Copy agents/global/AGENTS.md to global AGENTS.md paths for Grok, Cursor, Codex, and Kimi.
For OpenClaw, merge into ~/.openclaw/workspace/AGENTS.md without removing workspace bootstrap content.
"@
}

function Copy-Agents {
  param([string]$Dest)

  $destDir = Split-Path -Parent $Dest
  if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
  }
  Copy-Item -Path $Source -Destination $Dest -Force
  Write-Host "  -> $Dest"
}

function Merge-OpenClawAgents {
  $Dest = Join-Path $HOME ".openclaw\workspace\AGENTS.md"
  $destDir = Split-Path -Parent $Dest
  if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
  }

  if (-not (Test-Path $Dest)) {
    Copy-Item -Path $Source -Destination $Dest -Force
    Write-Host "  -> $Dest (created)"
    return
  }

  $tmp = [System.IO.Path]::GetTempFileName()
  $sourceContent = Get-Content -Path $Source -Raw
  $destContent = Get-Content -Path $Dest -Raw

  if ($destContent.Contains($MarkerStart)) {
    $pattern = [regex]::Escape($MarkerStart) + "[\s\S]*?" + [regex]::Escape($MarkerEnd)
    $replacement = $MarkerStart + "`n" + $sourceContent.TrimEnd() + "`n" + $MarkerEnd
    $merged = [regex]::Replace($destContent, $pattern, $replacement)
    Set-Content -Path $tmp -Value $merged -NoNewline -Encoding utf8
  }
  else {
    $merged = $destContent.TrimEnd() + "`n`n" + $MarkerStart + "`n" + $sourceContent.TrimEnd() + "`n" + $MarkerEnd + "`n"
    Set-Content -Path $tmp -Value $merged -NoNewline -Encoding utf8
  }

  Move-Item -Path $tmp -Destination $Dest -Force
  Write-Host "  -> $Dest (merged)"
}

if ($args -contains "-h" -or $args -contains "--help" -or $args -contains "/?") {
  Show-Usage
  exit 0
}

if (-not (Test-Path $Source)) {
  Write-Error "error: source not found: $Source"
  exit 1
}

Write-Host "Syncing global AGENTS.md"
Write-Host "  source: $Source"

foreach ($dest in $Targets) {
  Copy-Agents -Dest $dest
}

Merge-OpenClawAgents
Write-Host "Done."
