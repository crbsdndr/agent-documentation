#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptName = Split-Path -Leaf $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$SkillsRoot = Join-Path $RepoRoot "skills\global"

# Only sync when the tool home directory already exists.
$Targets = @(
  @{ Name = "Grok";     Home = (Join-Path $HOME ".grok");      Skills = (Join-Path $HOME ".grok\skills") },
  @{ Name = "Cursor";   Home = (Join-Path $HOME ".cursor");    Skills = (Join-Path $HOME ".cursor\skills") },
  @{ Name = "Codex";    Home = (Join-Path $HOME ".codex");     Skills = (Join-Path $HOME ".codex\skills") },
  @{ Name = "OpenClaw"; Home = (Join-Path $HOME ".openclaw");  Skills = (Join-Path $HOME ".openclaw\skills") },
  @{ Name = "Kimi";     Home = (Join-Path $HOME ".kimi-code"); Skills = (Join-Path $HOME ".kimi-code\skills") }
)

function Show-Usage {
  Write-Host @"
Usage: $ScriptName [skill-name|all]

Copy global skills from skills/global/ to installed CLI skill directories only.
Skips tools whose home directory does not exist (does not create them).

Examples:
  $ScriptName git-commit
  $ScriptName all
"@
}

function Copy-Skill {
  param([string]$Name)

  $source = Join-Path $SkillsRoot $Name

  if (-not (Test-Path $source -PathType Container)) {
    Write-Error "error: skill not found: $source"
    exit 1
  }

  Write-Host "Syncing: $Name"
  Write-Host "  source: $source"

  $synced = 0
  foreach ($t in $Targets) {
    if (-not (Test-Path $t.Home -PathType Container)) {
      Write-Host "  skip $($t.Name) ($($t.Home) not found)"
      continue
    }

    $dest = Join-Path $t.Skills $Name
    if (-not (Test-Path $dest)) {
      New-Item -ItemType Directory -Path $dest -Force | Out-Null
    }
    Copy-Item -Path (Join-Path $source "*") -Destination $dest -Recurse -Force
    Write-Host "  -> $dest"
    $synced++
  }

  if ($synced -eq 0) {
    Write-Error "error: no installed CLI tool homes found to sync"
    exit 1
  }

  Write-Host ""
}

$arg = if ($args.Count -ge 1) { $args[0] } else { "git-commit" }

if ($arg -eq "-h" -or $arg -eq "--help" -or $arg -eq "/?") {
  Show-Usage
  exit 0
}

if (-not (Test-Path $SkillsRoot -PathType Container)) {
  Write-Error "error: skills directory not found: $SkillsRoot"
  exit 1
}

if ($arg -eq "all") {
  $dirs = Get-ChildItem -Path $SkillsRoot -Directory
  if ($dirs.Count -eq 0) {
    Write-Error "error: no skills found in $SkillsRoot"
    exit 1
  }
  foreach ($dir in $dirs) {
    Copy-Skill -Name $dir.Name
  }
}
else {
  Copy-Skill -Name $arg
}

Write-Host "Done."
