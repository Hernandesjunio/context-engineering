$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $PSScriptRoot
$DiagramDir = Join-Path $RootDir "assets\diagrams"

Get-ChildItem -Path $DiagramDir -Filter "*.svg" | ForEach-Object {
    $Png = [System.IO.Path]::ChangeExtension($_.FullName, ".png")
    & inkscape $_.FullName --export-type=png --export-filename=$Png --export-width=1800
    if ($LASTEXITCODE -ne 0) { throw "Falha ao renderizar $($_.Name)." }
    Write-Host "Gerado: $Png"
}
