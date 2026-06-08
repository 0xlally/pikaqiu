param(
  [string]$KaliBaseImage = "kalilinux/kali-rolling:latest",
  [string]$KaliAptMirror = "http://http.kali.org/kali",
  [string]$KaliAptSuite = "kali-rolling",
  [string]$ProxyUrl = ""
)

$ErrorActionPreference = "Stop"

$containerName = "pikaqiu-sandbox-1"
$imageName = "pikaqiu-kali-sandbox:latest"
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Get-ContainerName([string]$Name) {
  docker ps -a --filter "name=^/$Name$" --format "{{.Names}}"
}

function Ensure-Image([string]$Name) {
  $exists = $false
  try {
    docker image inspect $Name *> $null
    $exists = ($LASTEXITCODE -eq 0)
  }
  catch {
    $exists = $false
  }

  if ($exists) {
    return
  }
  Write-Host "Building Kali sandbox image..."
  Write-Host "  base image: $KaliBaseImage"
  Write-Host "  apt mirror: $KaliAptMirror"
  Write-Host "  apt suite:  $KaliAptSuite"
  if ($ProxyUrl) {
    Write-Host "  proxy:     $ProxyUrl"
  }
  docker build `
    --build-arg KALI_BASE_IMAGE=$KaliBaseImage `
    --build-arg KALI_APT_MIRROR=$KaliAptMirror `
    --build-arg KALI_APT_SUITE=$KaliAptSuite `
    --build-arg PROXY_URL=$ProxyUrl `
    -f Dockerfile.sandbox `
    -t $Name `
    .
  if ($LASTEXITCODE -ne 0) {
    throw "Failed to build Docker image $Name. Check Docker Hub network/proxy access and rerun this script."
  }
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
  if ($LASTEXITCODE -ne 0) {
    throw "Failed to start sandbox container."
  }
}
finally {
  Pop-Location
}

docker ps --filter "name=^/$containerName$" --format "sandbox ready: {{.Names}} {{.Status}}"
