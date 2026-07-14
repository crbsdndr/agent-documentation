#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptName = Split-Path -Leaf $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Source = Join-Path $RepoRoot "agents\global\AGENTS.md"

$MarkerStart = "<!-- agent-documentation:global-agents:start -->"
$MarkerEnd = "<!-- agent-documentation:global-agents:end -->"

# Only sync when the tool home directory already exists.
$CopyTargets = @(
  @{ Name = "Grok";   Home = (Join-Path $HOME ".grok");      Dest = (Join-Path $HOME ".grok\AGENTS.md") },
  @{ Name = "Cursor"; Home = (Join-Path $HOME ".cursor");    Dest = (Join-Path $HOME ".cursor\AGENTS.md") },
  @{ Name = "Codex";  Home = (Join-Path $HOME ".codex");     Dest = (Join-Path $HOME ".codex\AGENTS.md") },
  @{ Name = "Kimi";   Home = (Join-Path $HOME ".kimi-code"); Dest = (Join-Path $HOME ".kimi-code\AGENTS.md") }
)

function Show-Usage {
  Write-Host @"
Usage: $ScriptName

Copy agents/global/AGENTS.md to installed CLI tool homes only.
Skips tools whose home directory does not exist (does not create them).

Targets (if present):
  ~/.grok/AGENTS.md
  ~/.cursor/AGENTS.md
  ~/.codex/AGENTS.md
  ~/.kimi-code/AGENTS.md
  ~/.openclaw/workspace/AGENTS.md  (merged)
"@
}

function Copy-Agents {
  param(
    [string]$Name,
    [string]$HomeDir,
    [string]$Dest
  )

  if (-not (Test-Path $HomeDir -PathType Container)) {
    Write-Host "  skip $Name ($HomeDir not found)"
    return $false
  }

  Copy-Item -Path $Source -Destination $Dest -Force
  Write-Host "  -> $Dest"
  return $true
}

function Merge-OpenClawAgents {
  $HomeDir = Join-Path $HOME ".openclaw"
  $Dest = Join-Path $HomeDir "workspace\AGENTS.md"

  if (-not (Test-Path $HomeDir -PathType Container)) {
    Write-Host "  skip OpenClaw ($HomeDir not found)"
    return $false
  }

  $destDir = Split-Path -Parent $Dest
  if (-not (Test-Path $destDir)) {
    New-Item -ItemType Directory -Path $destDir -Force | Out-Null
  }

  if (-not (Test-Path $Dest)) {
    Copy-Item -Path $Source -Destination $Dest -Force
    Write-Host "  -> $Dest (created)"
    return $true
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
  return $true
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

$synced = 0
foreach ($t in $CopyTargets) {
  if (Copy-Agents -Name $t.Name -HomeDir $t.Home -Dest $t.Dest) {
    $synced++
  }
}

if (Merge-OpenClawAgents) {
  $synced++
}

if ($synced -eq 0) {
  Write-Error "error: no installed CLI tool homes found to sync"
  exit 1
}

Write-Host "Done. ($synced target(s))"
