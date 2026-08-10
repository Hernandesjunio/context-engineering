param(
    [ValidateSet("latex", "markdown")]
    [string]$Mode = "latex"
)

$ErrorActionPreference = "Stop"
$EbookDir = Split-Path -Parent $PSScriptRoot
$Base = "context-engineering-para-times-de-desenvolvimento-v5-beta2"

Push-Location $EbookDir
try {
    if ($Mode -eq "markdown") {
        & pandoc "$Base.md" `
            --from "markdown+fenced_divs" `
            --lua-filter "callouts.lua" `
            --include-in-header "ebook-style.tex" `
            --standalone `
            --toc `
            --number-sections `
            -o "$Base.tex"
        if ($LASTEXITCODE -ne 0) { throw "Pandoc falhou com código $LASTEXITCODE." }
    }

    & xelatex -interaction=nonstopmode -halt-on-error "$Base.tex"
    if ($LASTEXITCODE -ne 0) { throw "Primeira compilação XeLaTeX falhou." }
    & xelatex -interaction=nonstopmode -halt-on-error "$Base.tex"
    if ($LASTEXITCODE -ne 0) { throw "Segunda compilação XeLaTeX falhou." }

    Write-Host "PDF gerado: $(Join-Path $EbookDir "$Base.pdf")"
}
finally {
    Pop-Location
}
