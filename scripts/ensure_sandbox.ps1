$ErrorActionPreference = "Stop"

$containerName = "tpt-kali-sandbox"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# Check if container exists
$existing = docker ps -a --filter "name=^/$containerName$" --format "{{.Names}}"
if ($existing -eq $containerName) {
  docker start $containerName *> $null
  docker ps --filter "name=^/$containerName$" --format "sandbox ready: {{.Names}} {{.Status}}"
  exit 0
}

# Build and start via docker-compose
Write-Host "Building Kali sandbox container..."
Push-Location $repoRoot
docker compose up -d --build sandbox
Pop-Location

docker ps --filter "name=^/$containerName$" --format "sandbox ready: {{.Names}} {{.Status}}"
