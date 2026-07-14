#Requires -Version 5.1
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ScriptName = Split-Path -Leaf $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$SkillsRoot = Join-Path $RepoRoot "skills\global"

$Targets = @(
  (Join-Path $HOME ".grok\skills"),
  (Join-Path $HOME ".cursor\skills"),
  (Join-Path $HOME ".codex\skills"),
  (Join-Path $HOME ".openclaw\skills"),
  (Join-Path $HOME ".kimi-code\skills")
)

function Show-Usage {
  Write-Host @"
Usage: $ScriptName [skill-name|all]

Copy global skills from skills/global/ to all CLI skill directories.

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

  foreach ($base in $Targets) {
    $dest = Join-Path $base $Name
    if (-not (Test-Path $dest)) {
      New-Item -ItemType Directory -Path $dest -Force | Out-Null
    }
    Copy-Item -Path (Join-Path $source "*") -Destination $dest -Recurse -Force
    Write-Host "  -> $dest"
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
