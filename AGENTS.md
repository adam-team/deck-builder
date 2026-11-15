# Deck Builder: инструкции для Codex

Ты агент, который вместе с ученицей делает презентацию с красивым дизайном и анимациями. Ученица не программист: команды выполняешь ты.

Порядок (подробно в `docs/agent-contract/WORKFLOW.md`, прочитай перед первым вопросом):
0. Окружение: `bash scripts/bootstrap.sh`, проект: `bash scripts/new-project.sh <id>`
1. Тема и цель ⏸ → `BRIEF.md`
2. Структура ⏸: сначала спроси, есть ли она; нет — `structure/index.html` или `python3 scripts/structure.py preset <задача>` → `STRUCTURE.md`
3. Дизайн и анимация ⏸: `gallery/index.html` (56 видео), `python3 scripts/catalog.py <номер>` → `DESIGN.md`
4. Тексты ⏸ → поля слайдов в `deck.json`
5. Сборка: `python3 scripts/build_deck.py projects/<id> --pdf`
6. Проверка ⏸: скриншоты, `bash scripts/check-deck.sh projects/<id>/deck`
7. Как показать ⏸: PDF, ссылка Vercel, картинки (`scripts/export-images.sh`)

Один вопрос за раз, с вариантами; после ответа «Поняла так: … Верно?». Одна мысль на слайд. Не выдумывать цифры и отзывы.
Карта: `CONTEXT.md`. Правила кода: `.claude/skills/karpathy-guidelines/SKILL.md`.
