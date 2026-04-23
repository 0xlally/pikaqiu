$ErrorActionPreference = "Stop"

$containerName = "pikaqiu-sandbox-1"
$imageName = "pikaqiu-kali-sandbox:latest"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Get-ContainerName([string]$Name) {
  docker ps -a --filter "name=^/$Name$" --format "{{.Names}}"
}

function Ensure-Image([string]$Name) {
  docker image inspect $Name *> $null
  if ($LASTEXITCODE -eq 0) {
    return
  }
  Write-Host "Building Kali sandbox image..."
  docker build -f Dockerfile.sandbox -t $Name .
}

if ((Get-ContainerName $containerName) -eq $containerName) {
  docker start $containerName *> $null
  docker ps --filter "name=^/$containerName$" --format "sandbox ready: {{.Names}} {{.Status}}"
  exit 0
}

Push-Location $repoRoot
try {
  Ensure-Image $imageName

  Write-Host "Starting Kali sandbox container..."
  docker compose up -d sandbox-1
}
finally {
  Pop-Location
}

docker ps --filter "name=^/$containerName$" --format "sandbox ready: {{.Names}} {{.Status}}"
