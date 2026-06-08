$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
	throw "python command not found in PATH"
}

Write-Host "Starting PikaQiu web app from $repoRoot ..."
& $pythonCmd.Source -m pikaqiu_agent
