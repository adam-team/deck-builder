# Контекст: что здесь и как работать

## Порядок

0. Окружение → 1. Тема ⏸ → 2. Структура ⏸ → 3. Дизайн и анимация ⏸ → 4. Тексты ⏸ → 5. Сборка → 6. Проверка ⏸ → 7. Как показать ⏸.
Полный контракт: `docs/agent-contract/WORKFLOW.md`.

## Команды

| Команда | Что делает |
|---|---|
| `/deck` | начать или продолжить опрос |
| `bash scripts/bootstrap.sh` | проверяет Python, Chrome, Node, ffmpeg; собирает данные конструктора и галереи |
| `bash scripts/new-project.sh <id>` | создаёт `projects/<id>/` с заготовками |
| `python3 scripts/structure.py list` | задачи, форматы, 16 типов слайдов, переходы |
| `python3 scripts/structure.py preset <задача>` | готовый порядок слайдов |
| `python3 scripts/structure.py write projects/<id> <structure.json или задача>` | `STRUCTURE.md` и `slides` в `deck.json` |
| `python3 scripts/catalog.py [номер \| find слово \| md]` | каталог дизайнов |
| `python3 scripts/build_deck.py projects/<id> [--pdf]` | собирает презентацию (и PDF) |
| `python3 scripts/build_deck.py --demo <номер> --preset <задача> --transition <переход> --format <формат> --out <папка>` | образец |
| `python3 scripts/build_reveal.py projects/<id> --theme <тема> --transition <переход>` | та же презентация на reveal.js |
| `bash scripts/export-images.sh projects/<id>` | PDF → картинки слайдов (карусель, сторис) |
| `bash scripts/check-deck.sh projects/<id>/deck` | «ЗАПОЛНИТЬ», тексты-образцы, длинные слайды |
| `bash scripts/check-secrets.sh` | ключи и запрещённые файлы в git |
| `cd tools && node record-previews.mjs [номера]` | видео-превью новых дизайнов |
| `python3 scripts/build_gallery.py` | пересобирает `gallery/data.js` |

## Где что лежит

| Что | Где |
|---|---|
| Ответы ученицы | `projects/<id>/BRIEF.md`, `STRUCTURE.md`, `DESIGN.md`, `CONTENT.md`, `DECISIONS.md`, `deck.json`, `assets/` |
| Готовая презентация | `projects/<id>/deck/index.html`, `presentation.pdf`, `slides/*.png` |
| Задачи, форматы, типы слайдов, переходы | `structure/presets.json` (после правки `python3 scripts/structure.py sync`) |
| Все дизайны | `catalog/designs.json` (после правки `python3 scripts/catalog.py md` и `python3 scripts/build_gallery.py`) |
| Видео и обложки | `gallery/media/<номер>.mp4`, `.jpg` |
| Живые образцы | `gallery/live/<номер>/index.html`, `gallery/live/reveal-<тема>/` |
| Шаблон и движок | `template/deck.css` (оформление, 8 переходов, 4 появления), `template/deck.js` (листание, автопоказ, печать) |
| Слайды по типам | функции `r_*` в `scripts/build_deck.py` |
| Презентации Куралай | `designs/own/*.pdf` |
| Движки с GitHub | `engines/reveal/` (MIT), `engines/impress/` (MIT) |

## Типы дизайнов

| Тип | Номера | Как применять |
|---|---|---|
| `own` | 1-7 | PDF-образец: стиль переносится в `tokens`/`style` палитры (8 = стиль Куралай) |
| `tokens` | 8-37 | `design: <номер>` в `deck.json` → `build_deck.py`; меняются `transition`, `appear`, `style`, `tokens` |
| `external` | 38-56 | reveal.js (`build_reveal.py`) или impress.js (вручную по `engines/impress/examples`) |

## Правила

- Без `BRIEF.md`, `STRUCTURE.md`, `DESIGN.md` не собираешь.
- `template/`, `engines/`, `designs/` под ученицу не правишь: только `projects/<id>/`.
- Одна мысль на слайд, до 30 слов. Не выдумываешь цифры и отзывы.

## Экономия подписки

Не читай целиком `gallery/data.js`, `structure/presets.js`, `engines/*`, `gallery/live/*`: ищи через `scripts/catalog.py` и `grep`.
