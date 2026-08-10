#!/usr/bin/env bash
set -euo pipefail

mode="${1:-all}"
root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ebook_dir="$root_dir/ebook"
workbook_dir="$root_dir/workbook"
book_base="context-engineering-para-times-de-desenvolvimento-v5"
workbook_base="workbook-context-engineering-v5"

build_one() {
  local dir="$1"
  local base="$2"
  local style="$3"
  cd "$dir"
  pandoc "$base.md" \
      --from markdown+fenced_divs \
      --lua-filter=callouts.lua \
      --include-in-header="$style" \
      --standalone --toc --number-sections \
      -o "$base.tex"
  xelatex -interaction=nonstopmode -halt-on-error "$base.tex"
  xelatex -interaction=nonstopmode -halt-on-error "$base.tex"
  echo "PDF gerado: $dir/$base.pdf"
}

case "$mode" in
  book) build_one "$ebook_dir" "$book_base" "ebook-style.tex" ;;
  workbook) build_one "$workbook_dir" "$workbook_base" "workbook-style.tex" ;;
  all)
    build_one "$ebook_dir" "$book_base" "ebook-style.tex"
    build_one "$workbook_dir" "$workbook_base" "workbook-style.tex"
    ;;
  *) echo "Uso: $0 [book|workbook|all]" >&2; exit 2 ;;
esac
