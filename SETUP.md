# Установка окружения

Делает агент: `bash scripts/bootstrap.sh`. Скрипт проверяет:

1. **Python 3**: сборка презентаций, структура, каталог (без пакетов).
2. **Google Chrome**: просмотр и PDF.
3. **pdftoppm** (poppler): картинки слайдов для Instagram. Mac: `brew install poppler`.
4. **Node.js** и **ffmpeg**: только для записи новых видео-превью и выкладки на Vercel.
5. Собирает `structure/presets.js`, `gallery/data.js`, живые образцы и ставит сторож секретов.

Дальше сразу этап 1 из `docs/agent-contract/WORKFLOW.md`.
