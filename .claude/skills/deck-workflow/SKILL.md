---
name: deck-workflow
description: Use at the start of every new presentation project in this repository ("сделай презентацию", "слайды", "урок", "вебинар", "КП", "карусель", "сторис", "питч", "3D-переходы"). Runs the staged questionnaire one question at a time (topic, structure — existing or co-created in structure/index.html, design and transitions in the video gallery gallery/index.html, texts), writes BRIEF/STRUCTURE/DESIGN/CONTENT and deck.json, then builds with scripts/build_deck.py (HTML + PDF).
---

# Этапы презентации

Порядок: `docs/agent-contract/WORKFLOW.md`. Вопросы: `docs/agent-contract/QUESTIONS.md`.

1. `bash scripts/bootstrap.sh`, `bash scripts/new-project.sh <id>`.
2. Тема ⏸ → `BRIEF.md`.
3. Структура ⏸: «Есть ли у тебя структура?» Есть — разложить по 16 типам. Нет — `structure/index.html` / `scripts/structure.py preset`. Затем `scripts/structure.py write`.
4. Дизайн и анимация ⏸: `gallery/index.html` (56 видео), `scripts/catalog.py <номер>` → `DESIGN.md`.
5. Тексты ⏸ → `deck.json`.
6. Сборка `scripts/build_deck.py projects/<id> --pdf`, проверка и выдача ⏸.

Один вопрос за раз, с вариантами. Без `BRIEF`, `STRUCTURE`, `DESIGN` не собираешь.
