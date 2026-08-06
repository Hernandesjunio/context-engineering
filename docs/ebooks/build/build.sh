#!/usr/bin/env bash
set -euo pipefail

mode="${1:-latex}"
ebook_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
base="context-engineering-para-times-de-desenvolvimento-v5-beta2"

cd "$ebook_dir"

if [[ "$mode" == "markdown" ]]; then
  pandoc "$base.md" \
    --from markdown+fenced_divs \
    --lua-filter=callouts.lua \
    --include-in-header=ebook-style.tex \
    --standalone \
    --toc \
    --number-sections \
    -o "$base.tex"
elif [[ "$mode" != "latex" ]]; then
  echo "Uso: $0 [latex|markdown]" >&2
  exit 2
fi

xelatex -interaction=nonstopmode -halt-on-error "$base.tex"
xelatex -interaction=nonstopmode -halt-on-error "$base.tex"

echo "PDF gerado: $ebook_dir/$base.pdf"
