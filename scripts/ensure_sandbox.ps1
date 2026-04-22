$ErrorActionPreference = "Stop"

$containerName = "pikaqiu-sandbox-1"
$imageName = "pikaqiu-kali-sandbox:latest"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# Check if container exists
$existing = docker ps -a --filter "name=^/$containerName$" --format "{{.Names}}"
if ($existing -eq $containerName) {
  docker start $containerName *> $null
  docker ps --filter "name=^/$containerName$" --format "sandbox ready: {{.Names}} {{.Status}}"
  exit 0
}

Push-Location $repoRoot
try {
  docker image inspect $imageName *> $null
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Building Kali sandbox image..."
    docker build -f Dockerfile.sandbox -t $imageName .
  }

  Write-Host "Starting Kali sandbox container..."
  docker compose up -d sandbox-1
}
finally {
  Pop-Location
}

docker ps --filter "name=^/$containerName$" --format "sandbox ready: {{.Names}} {{.Status}}"
