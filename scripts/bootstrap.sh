#!/usr/bin/env bash
# Проверка и подготовка окружения. Запускает агент.
set -uo pipefail
cd "$(dirname "$0")/.."
ok(){ printf "  ✓ %s\n" "$1"; }; no(){ printf "  ✗ %s\n" "$1"; }
echo "Окружение Deck Builder:"
command -v python3 >/dev/null && ok "Python $(python3 -c 'import sys;print(sys.version.split()[0])')" || { no "Python 3 не найден"; exit 1; }
if [[ -d "/Applications/Google Chrome.app" ]] || command -v google-chrome >/dev/null; then ok "Google Chrome"; else no "Chrome не найден (нужен для PDF)"; fi
command -v pdftoppm >/dev/null && ok "pdftoppm" || echo "  · pdftoppm нет: нужен для картинок слайдов (brew install poppler)"
command -v node >/dev/null && ok "Node $(node -v)" || echo "  · Node нет: нужен только для видео-превью и Vercel"
command -v ffmpeg >/dev/null && ok "ffmpeg" || echo "  · ffmpeg нет: нужен только для видео-превью"
python3 scripts/structure.py sync >/dev/null && ok "конструктор: structure/presets.js"
python3 scripts/build_gallery.py | sed 's/^/  ✓ /'
for n in $(python3 -c "import json;print(' '.join(str(d['n']) for d in json.load(open('catalog/designs.json')) if d['kind']=='tokens'))"); do
  [[ -f gallery/live/$n/index.html ]] || python3 scripts/build_deck.py --demo "$n" >/dev/null
done
[[ -f gallery/live/reveal-white/index.html ]] || python3 scripts/build_reveal.py >/dev/null
ok "живые образцы: gallery/live/"
git rev-parse --git-dir >/dev/null 2>&1 && bash scripts/hooks/install.sh >/dev/null && ok "сторож секретов"
echo "Готово. Дальше: docs/agent-contract/WORKFLOW.md, этап 1."
