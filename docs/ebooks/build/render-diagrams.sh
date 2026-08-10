#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
diagram_dir="$root_dir/ebook/assets/diagrams"

for svg in "$diagram_dir"/*.svg; do
  png="${svg%.svg}.png"
  inkscape "$svg" --export-type=png --export-filename="$png" --export-width=1800
  echo "Gerado: $png"
done
