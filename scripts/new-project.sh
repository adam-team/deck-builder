#!/usr/bin/env bash
# Папка проекта ученицы: bash scripts/new-project.sh <id>   (латиница, цифры, дефис)
set -euo pipefail
cd "$(dirname "$0")/.."
id="${1:-}"
[[ "$id" =~ ^[a-z0-9][a-z0-9-]{1,40}$ ]] || { echo "id: латиница, цифры, дефис, например lesson-site"; exit 1; }
[[ -e "projects/$id" ]] && { echo "projects/$id уже есть: продолжаем по его файлам"; exit 0; }
mkdir -p "projects/$id/assets"
cp projects/_template/*.md "projects/$id/"
echo '{"design": 8, "format": "1:1", "transition": "fade", "appear": "up", "tag": "", "footer": "", "title": "", "slides": []}' > "projects/$id/deck.json"
echo "создано: projects/$id (BRIEF, STRUCTURE, DESIGN, CONTENT, DECISIONS, deck.json, assets/)"
