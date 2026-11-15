#!/usr/bin/env bash
# Проверка готовой презентации: bash scripts/check-deck.sh projects/<id>/deck
set -uo pipefail
dir="${1:?папка презентации}"; f="$dir/index.html"; fail=0
[[ -f "$f" ]] || { echo "✗ нет $f"; exit 1; }
hit(){ local r; r=$(grep -oE "$2" "$f" | sort | uniq -c | head -6); if [[ -n "$r" ]]; then echo "✗ $1:"; sed 's/^/    /' <<<"$r"; fail=1; else echo "✓ нет: $1"; fi; }
hit "пометки ЗАПОЛНИТЬ и ЧЕРНОВИК" 'ЗАПОЛНИТЬ|ЧЕРНОВИК'
hit "тексты-образцы шаблона" 'Айгерим, ученица потока|50,9K|Как собрать сайт с|Короткий абзац на 2-3 строки|Зачем это нужно|90 000 ₸'
python3 - "$f" <<'PY'
import re, sys, html
s = open(sys.argv[1], encoding="utf-8").read()
for i, sec in enumerate(re.findall(r'<section class="slide.*?</section>', s, re.S), 1):
    text = re.sub(r"<[^>]+>", " ", re.sub(r'<div class="meta.*?</div>', "", sec, flags=re.S))
    words = len(html.unescape(text).split())
    if words > 60: print(f"⚠ слайд {i}: {words} слов — подумайте, не разделить ли на два")
PY
[[ -f "$dir/presentation.pdf" ]] && echo "✓ есть PDF" || echo "· PDF нет: python3 scripts/build_deck.py <проект> --pdf"
[[ $fail -eq 0 ]] && echo "Презентация чистая." || echo "Исправь отмеченное или подтверди с ученицей."
exit $fail
