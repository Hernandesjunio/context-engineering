param(
    [ValidateSet("book", "workbook", "all")]
    [string]$Mode = "all"
)

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $PSScriptRoot
$EbookDir = Join-Path $RootDir "ebook"
$WorkbookDir = Join-Path $RootDir "workbook"

function Build-Artifact([string]$Directory, [string]$Base, [string]$Style) {
    Push-Location $Directory
    try {
        & pandoc "$Base.md" `
            --from "markdown+fenced_divs" `
            --lua-filter "callouts.lua" `
            --include-in-header $Style `
            --standalone `
            --toc `
            --number-sections `
            -o "$Base.tex"
        if ($LASTEXITCODE -ne 0) { throw "Pandoc falhou com código $LASTEXITCODE." }

        & xelatex -interaction=nonstopmode -halt-on-error "$Base.tex"
        if ($LASTEXITCODE -ne 0) { throw "Primeira compilação XeLaTeX falhou." }
        & xelatex -interaction=nonstopmode -halt-on-error "$Base.tex"
        if ($LASTEXITCODE -ne 0) { throw "Segunda compilação XeLaTeX falhou." }

        Write-Host "PDF gerado: $(Join-Path $Directory "$Base.pdf")"
    }
    finally {
        Pop-Location
    }
}

if ($Mode -eq "book" -or $Mode -eq "all") {
    Build-Artifact $EbookDir "context-engineering-para-times-de-desenvolvimento-v5" "ebook-style.tex"
}
if ($Mode -eq "workbook" -or $Mode -eq "all") {
    Build-Artifact $WorkbookDir "workbook-context-engineering-v5" "workbook-style.tex"
}
