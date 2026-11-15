#!/usr/bin/env bash
# PDF презентации → картинки слайдов для Instagram (карусель, сторис): bash scripts/export-images.sh projects/<id>
set -euo pipefail
proj="${1:?проект}"; pdf="$proj/deck/presentation.pdf"
[[ -f "$pdf" ]] || python3 "$(dirname "$0")/build_deck.py" "$proj" --pdf
mkdir -p "$proj/deck/slides"
pdftoppm -r 96 -png "$pdf" "$proj/deck/slides/slide"
ls "$proj/deck/slides" | wc -l | xargs echo "картинок:"; echo "папка: $proj/deck/slides/"
