# Genera el .zip de entrega excluyendo carpetas autogeneradas (.gradle, build, .idea, local.properties).
param(
    [string]$Salida = "EcoTrip2026_Grupo4.zip"
)

$raiz = Resolve-Path (Join-Path $PSScriptRoot "..")
$temp = Join-Path ([System.IO.Path]::GetTempPath()) ("ecotrip_" + [guid]::NewGuid())
New-Item -ItemType Directory -Path $temp | Out-Null

robocopy $raiz $temp /E /XD .gradle build .idea .git .cxx captures .claude /XF local.properties *.iml .DS_Store | Out-Null

$destino = Join-Path $raiz $Salida
if (Test-Path $destino) { Remove-Item $destino -Force }
Compress-Archive -Path (Join-Path $temp "*") -DestinationPath $destino
Remove-Item $temp -Recurse -Force
Write-Host "Creado: $destino"
