---
description: Сделать презентацию с ученицей: тема, структура (есть или вместе в конструкторе), дизайн и 3D-переходы из видео-галереи, тексты, сборка, PDF
---

Ты начинаешь или продолжаешь работу над презентацией. Порядок жёсткий.

1. Прочитай `CLAUDE.md`, `CONTEXT.md`, `docs/agent-contract/WORKFLOW.md`.
2. Есть `projects/<id>/` с файлами: скажи, на каком этапе остановились, и продолжай. Нет: `bash scripts/bootstrap.sh`, спроси имя, `bash scripts/new-project.sh <id>`.
3. **Тема ⏸** (блок A) → `BRIEF.md`.
4. **Структура ⏸:** сначала спроси, есть ли она. Есть: разложи по 16 типам слайдов. Нет: `structure/index.html` или `scripts/structure.py preset`. Затем `scripts/structure.py write`.
5. **Дизайн и анимация ⏸:** `gallery/index.html`, `scripts/catalog.py find|<номер>`, образцы на её структуре → `DESIGN.md`, `design/transition/appear` в `deck.json`.
6. **Тексты ⏸** по слайдам → `deck.json`, `CONTENT.md`.
7. **Сборка:** `python3 scripts/build_deck.py projects/<id> --pdf`.
8. **Проверка ⏸:** скриншоты, `scripts/check-deck.sh`.
9. **Как показать ⏸:** PDF, ссылка, картинки.

После каждого ответа: «Поняла так: … Верно?». Одна мысль на слайд. Не выдумывай цифры и отзывы.
