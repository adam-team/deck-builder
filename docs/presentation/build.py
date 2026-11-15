#!/usr/bin/env python3
"""Презентация урока «Презентации с 3D-анимацией» в стиле брендбука Kuralay v2: квадратные слайды 1080×1080 → PDF.

  python3 docs/presentation/build.py      → docs/lesson-presentation.pdf (+ .html рядом)

Картинки: docs/presentation/img/ и обложки gallery/media/<номер>.jpg. Стиль: docs/presentation/style.css
(как у уроков «Брендбук», «Дизайн сайта»). Нужен Google Chrome.
"""
import os
import shutil
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
REPO = "github.com/adam-team/deck-builder"
TAG = "урок 7.3 · презентации"
OUT = os.path.join(ROOT, "docs", "lesson-presentation.pdf")

IMG = lambda name: "file://" + os.path.join(HERE, "img", name)
TH = lambda n: "file://" + os.path.join(ROOT, "gallery", "media", f"{n}.jpg")


def pic(src, h=None, st=""):
    hh = f"height:{h}px;" if h else ""
    return f'<div class="img" style="{hh}{st}"><img src="{src}" style="width:100%;object-fit:cover;object-position:top"></div>'


def thumbs(nums, cols=4, label=True):
    cells = "".join(
        f'<div><div class="img"><img src="{TH(n)}"></div>' + (f'<p class="mono sm" style="margin-top:6px">№{n}</p>' if label else "") + "</div>"
        for n in nums)
    return f'<div class="grid" style="grid-template-columns:repeat({cols},1fr);gap:14px">{cells}</div>'


SLIDES = [
    {"theme": "dark", "center": True, "html": f"""
      <div class="sub">модуль 7 · презентации, кп и материалы</div>
      <h1>Презентации с <span class="hl">3D-анимацией</span> вместе с агентом</h1>
      <p class="mut">Урок, вебинар, КП, карусель и сторис: структура → дизайн из видео-галереи → тексты → живая презентация, PDF и картинки.</p>
      <p class="mono" style="font-size:24px"><span class="ac">></span> {REPO}</p>"""},
    {"html": """
      <h2>Что получите <span class="hl">за урок</span></h2>
      <ul class="steps">
        <li><i>01</i><div><b>Структуру презентации</b><p>свою или собранную в конструкторе: какие слайды и в каком порядке</p></div></li>
        <li><i>02</i><div><b>Дизайн и 3D-переход</b><p>56 вариантов в видео: куб, переворот, полёт камеры</p></div></li>
        <li><i>03</i><div><b>Тексты по слайдам</b><p>одна мысль на слайд, цифры и отзывы только ваши</p></div></li>
        <li><i>04</i><div><b>Три результата</b><p>живая презентация по ссылке, PDF и картинки для Instagram</p></div></li>
      </ul>"""},
    {"theme": "cream", "html": """
      <h2>Что внутри <span class="hl">кода на GitHub</span></h2>
      <div class="grid g3">
        <div class="card"><div class="big" style="font-size:110px">56</div><b>дизайнов</b><span>у каждого видео, где видно переход</span></div>
        <div class="card"><div class="big" style="font-size:110px">16</div><b>типов слайдов</b><span>обложка, шаги, цифра, чат с ИИ, таблица…</span></div>
        <div class="card"><div class="big" style="font-size:110px">9</div><b>задач</b><span>урок, КП, вебинар, питч, карусель, сторис…</span></div>
        <div class="card"><div class="big" style="font-size:110px">4</div><b>формата</b><span>16:9, квадрат, карусель 4:5, сторис 9:16</span></div>
        <div class="card"><div class="big" style="font-size:110px">8</div><b>переходов</b><span>из них 5 в 3D</span></div>
        <div class="card"><div class="big" style="font-size:110px">4</div><b>появления</b><span>снизу, приближение, размытие, слева</span></div>
      </div>"""},
    {"theme": "dark", "html": """
      <h2>7 этапов <span class="hl">с агентом</span></h2>
      <table style="background:var(--graph);color:var(--cream)"><tr><th>этап</th><th>что происходит</th></tr>
      <tr><td>1 тема</td><td>для чего, кто смотрит, где покажете, что зритель сделает в конце</td></tr>
      <tr><td>2 структура</td><td>есть план — раскладываем по слайдам, нет — собираем в конструкторе</td></tr>
      <tr><td>3 дизайн</td><td>Дизайн-тека: 56 видео, выбираете дизайн и переход</td></tr>
      <tr><td>4 тексты</td><td>по слайдам сверху вниз, одна мысль на слайд</td></tr>
      <tr><td>5 сборка</td><td>одна команда: презентация + PDF</td></tr>
      <tr><td>6 проверка</td><td>скриншоты, поиск текстов-образцов и длинных слайдов</td></tr>
      <tr><td>7 выдача</td><td>ссылка, PDF, картинки для карусели и сторис</td></tr></table>"""},
    {"theme": "red", "center": True, "html": '<div class="num">01</div><h1>Структура</h1><p>одна мысль — один слайд</p>'},
    {"html": """
      <h2>Первый вопрос: <span class="hl">есть структура?</span></h2>
      <div class="grid g2">
        <div class="card"><div class="k">да, есть план</div><b>Текст урока, старая презентация, сценарий</b>
          <span>Агент режет материал на слайды и подбирает каждому тип из 16. Показывает список: «Так?»</span></div>
        <div class="card"><div class="k">нет плана</div><b>Собираем в конструкторе</b>
          <span>Задача, формат, слайды по порядку, кнопка «+ Добавить». Справа схема всех слайдов.</span></div>
      </div>
      <div class="win"><div class="bar"><i></i><i></i><i></i><span>чат с агентом</span></div>
        <p style="padding:22px 26px" class="sm">«У тебя уже есть структура: план слайдов, старая презентация, текст урока или сценарий? 1) да, пришлю 2) нет, соберём в конструкторе 3) предложи сама»</p></div>"""},
    {"theme": "cream", "html": f"""
      <h2>Конструктор <span class="hl">структуры</span></h2>
      {pic(IMG("structure.jpg"), 600)}
      <p class="sm mut">structure/index.html · 9 задач, 4 формата, порядок стрелками, «Скопировать для агента».</p>"""},
    {"html": """
      <h2>Формулы <span class="hl">порядка</span> слайдов</h2>
      <table><tr><th>задача</th><th>порядок</th></tr>
      <tr><td>урок</td><td>обложка → план → зачем → шаги → пример → практика → задание</td></tr>
      <tr><td>продажа</td><td>боль → было/стало → что внутри → цифра → отзыв → тарифы → призыв</td></tr>
      <tr><td>карусель</td><td>крючок → мысль → шаги → цифра → кодовое слово (5-8 слайдов)</td></tr>
      <tr><td>вебинар</td><td>обещание → кто я → план → 3 раздела → кейс → предложение</td></tr>
      <tr><td>питч</td><td>проблема → решение → цифры → план → команда → встреча</td></tr></table>
      <p class="sm mut">Каждая формула уже лежит в конструкторе: выбираете задачу — слайды подставляются.</p>"""},
    {"theme": "red", "center": True, "html": '<div class="num">02</div><h1>Дизайн и анимация</h1><p>56 презентаций в видео, как на YouTube</p>'},
    {"theme": "dark", "html": f"""
      <h2>Дизайн-тека: <span class="hl">видео листаются сами</span></h2>
      {pic(IMG("gallery.jpg"), 590)}
      <p class="sm mut">Наведите на обложку — презентация листается, видно переход. Вкладки: Мои · 3D-переходы · Тренды · Палитры · GitHub.</p>"""},
    {"html": """
      <h2>8 переходов, <span class="hl">5 из них 3D</span></h2>
      <table><tr><th>переход</th><th>как выглядит</th></tr>
      <tr><td>cube</td><td>слайды на гранях вращающегося куба</td></tr>
      <tr><td>orbit</td><td>полёт камеры, как в Prezi</td></tr>
      <tr><td>flip</td><td>слайд переворачивается как карточка</td></tr>
      <tr><td>convex</td><td>3D-поворот как страница книги</td></tr>
      <tr><td>cards</td><td>стопка: новый выезжает поверх, старый уходит назад</td></tr>
      <tr><td>zoom · slide · fade</td><td>приближение, сдвиг, проявление</td></tr></table>
      <p class="sm mut">Пункты на слайде появляются по клику: снизу, приближением, из размытия, слева.</p>"""},
    {"theme": "dark", "html": f"""
      <h2>Куб и <span class="hl">полёт камеры</span></h2>
      {pic(IMG("cube-frames.jpg"))}
      {pic(IMG("orbit-frames.jpg"))}
      <p class="sm mut">Кадры из видео Дизайн-теки: №8 «Куб 3D» и №9 «Полёт камеры». Переход живой, без видеоредактора.</p>"""},
    {"theme": "cream", "html": f"""
      <h2>Ваш стиль — <span class="hl">№8–15</span></h2>
      {pic(IMG("kuralay-slides.jpg"), 600)}
      <p class="sm mut">Брендбук Куралай v2: сетка точек, красные плашки, линия-маршрут. Тот же урок с каждым из 8 переходов.</p>"""},
    {"html": f"""
      <h2>Карусель <span class="hl">4:5</span> в один клик</h2>
      {pic(IMG("carousel.jpg"))}
      <p>Формат карусели → PDF → картинки слайдов для Instagram: <span class="mono ac">bash scripts/export-images.sh</span></p>
      <p class="sm mut">Так же для сторис 9:16 и квадратных уроков 1:1.</p>"""},
    {"theme": "cream", "html": f"""
      <h2>5 групп <span class="hl">дизайнов</span></h2>
      <div class="grid g3">
        <div class="card">{pic(TH(1))}<div class="k">1–7 · мои</div><span>уроки и BOSS VISION</span></div>
        <div class="card">{pic(TH(9))}<div class="k">8–15 · 3D-переходы</div><span>мой стиль × 8 переходов</span></div>
        <div class="card">{pic(TH(17))}<div class="k">16–25 · тренды</div><span>glass, брутализм, нуар</span></div>
        <div class="card">{pic(TH(30))}<div class="k">26–37 · палитры</div><span>карусель, сторис, питч</span></div>
        <div class="card">{pic(TH(42))}<div class="k">38–51 · reveal.js</div><span>14 тем с GitHub</span></div>
        <div class="card">{pic(TH(53))}<div class="k">52–56 · impress.js</div><span>3D-холст как Prezi</span></div>
      </div>"""},
    {"theme": "dark", "html": """
      <h2>Какой переход <span class="hl">под задачу</span></h2>
      <table style="background:var(--graph);color:var(--cream)"><tr><th>задача</th><th>переход</th></tr>
      <tr><td>урок, PDF</td><td>fade · slide · convex: спокойно, внимание на мысли</td></tr>
      <tr><td>вебинар</td><td>cube · cards: держат внимание на экране</td></tr>
      <tr><td>продажа, питч</td><td>orbit · zoom: wow-эффект на ключевых слайдах</td></tr>
      <tr><td>карусель, сторис</td><td>slide · flip: как листают в телефоне</td></tr></table>
      <p class="sm mut">Правило: один переход на всю презентацию. Если смотрят на анимацию, а не на мысль, переход слишком сильный.</p>"""},
    {"theme": "red", "center": True, "html": '<div class="num">03</div><h1>Тексты и выдача</h1><p>от плана к PDF и ссылке</p>'},
    {"html": """
      <h2>Тексты, которые <span class="hl">читают</span></h2>
      <ul class="steps">
        <li><i>01</i><div><b>Одна мысль — один слайд</b><p>до 30 слов; длинное режем на два слайда или «Шаги»</p></div></li>
        <li><i>02</i><div><b>Заголовок = результат или вопрос</b><p>«Как собрать сайт за вечер», а не «Сайты»</p></div></li>
        <li><i>03</i><div><b>Цифры «было → стало»</b><p>только настоящие, агент не выдумывает</p></div></li>
        <li><i>04</i><div><b>Конец всегда с действием</b><p>кодовое слово, ссылка, задание урока</p></div></li>
      </ul>"""},
    {"theme": "cream", "html": """
      <h2>Вся презентация — <span class="hl">один файл</span></h2>
      <div class="win term" style="background:var(--black);color:var(--cream)"><div class="bar"><i></i><i></i><i></i><span>projects/my-lesson/deck.json</span></div>
      <pre>{"design": <u>8</u>, "format": <u>"1:1"</u>, "transition": <u>"cube"</u>, "appear": "up",
 "slides": [
  {"type": "cover", "title": "Сайт [[за вечер]]", "theme": "dark"},
  {"type": "steps", "title": "4 шага", "steps": true, "items": [...]},
  {"type": "cta", "title": "Напиши слово", "word": "САЙТ"}]}</pre></div>
      <p class="sm mut">Агент заполняет его за вас. [[слово]] — красная плашка, "steps": true — пункты по клику.</p>"""},
    {"theme": "dark", "html": """
      <h2>Установка <span class="hl">одним сообщением</span></h2>
      <div class="win term" style="background:var(--black);color:var(--cream)"><div class="bar"><i></i><i></i><i></i><span>Claude Code · пустая папка</span></div>
      <pre>Склонируй репозиторий <u>https://github.com/adam-team/deck-builder</u>
в папку deck-builder, подготовь окружение по SETUP.md
и сразу начни опрос по docs/agent-contract/WORKFLOW.md.
Я хочу презентацию с красивым дизайном и анимациями.
Спрашивай по одному вопросу, с вариантами ответа.</pre></div>
      <p class="sm mut">Репозиторий приватный: сначала получите доступ у Куралай. Всё нужное агент поставит сам.</p>"""},
    {"theme": "cream", "html": """
      <h2>Команды, если <span class="hl">агент сбился</span></h2>
      <div class="win term" style="background:var(--black);color:var(--cream)"><div class="bar"><i></i><i></i><i></i><span>шпаргалка</span></div>
      <pre><u>/deck</u>                                   начать или продолжить
open structure/index.html               конструктор
open gallery/index.html                 Дизайн-тека
python3 scripts/catalog.py find куб     подобрать номера
python3 scripts/build_deck.py projects/имя --pdf   собрать
bash scripts/export-images.sh projects/имя      картинки</pre></div>
      <p class="sm mut">Показ вживую: открыть deck/index.html, F — на весь экран, стрелки и пробел листают.</p>"""},
    {"html": """
      <h2>Задание <span class="hl">урока</span></h2>
      <ul class="steps">
        <li><i>01</i><div><b>Установить deck-builder</b><p>сообщением со слайда 20</p></div></li>
        <li><i>02</i><div><b>Собрать структуру урока</b><p>своего курса: 10-15 слайдов</p></div></li>
        <li><i>03</i><div><b>Выбрать дизайн и переход</b><p>посмотреть 3 видео в Дизайн-теке</p></div></li>
        <li><i>04</i><div><b>Сделать PDF и карусель</b><p>прислать PDF и 1 картинку карусели в чат курса</p></div></li>
      </ul>"""},
    {"theme": "red", "center": True, "html": f"""
      <h2>Всё для урока — <span class="hl">в материалах</span></h2>
      <div class="grid g3">
        <div class="card" style="color:var(--black)"><div class="k">pdf</div><b>Эта презентация</b><span>кнопка «Презентация» вверху урока</span></div>
        <div class="card" style="color:var(--black)"><div class="k">github</div><b>Код deck-builder</b><span>{REPO}</span></div>
        <div class="card" style="color:var(--black)"><div class="k">видео</div><b>Дизайн-тека онлайн</b><span>56 презентаций с 3D-переходами</span></div>
      </div>
      <p>Пара к уроку про сайты: <b>site-builder</b> — та же логика для сайтов.</p>"""},
]


def slide(s, i, n):
    th = {"light": "", "cream": "cr", "dark": "dk", "red": "rd"}[s.get("theme", "light")]
    return (f'<section class="s {th}"><div class="top"><b>{TAG}</b><span>{i:02d} / {n:02d}</span></div>'
            f'<div class="in {"c" if s.get("center") else ""}">{s["html"]}</div>'
            f'<div class="bot"><span>@kuraylife</span><span>{REPO}</span></div></section>')


def main():
    css = open(os.path.join(HERE, "style.css"), encoding="utf-8").read()
    body = "".join(slide(s, i + 1, len(SLIDES)) for i, s in enumerate(SLIDES))
    page = f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Дизайн сайта</title><style>{css}</style></head><body>{body}</body></html>'
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "deck.html")
    open(src, "w", encoding="utf-8").write(page)
    pdf = os.path.join(tmp, "deck.pdf")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", f"--user-data-dir={tmp}/ud",
                    "--no-pdf-header-footer", "--virtual-time-budget=20000", f"--print-to-pdf={pdf}", "file://" + src],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
    shutil.copy(pdf, OUT)
    shutil.copy(src, os.path.join(HERE, "deck.html"))
    print(len(SLIDES), "слайдов →", OUT)


if __name__ == "__main__":
    main()
