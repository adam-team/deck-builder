#!/usr/bin/env python3
"""Собирает презентацию из трёх решений: структура (слайды) + дизайн + переход и анимации.

  python3 scripts/build_deck.py projects/<id>                       # настоящая презентация → projects/<id>/deck/index.html
  python3 scripts/build_deck.py projects/<id> --pdf                 # + PDF рядом (нужен Google Chrome)
  python3 scripts/build_deck.py --demo <номер> [--preset lesson] [--transition cube] [--format 16:9] --out <папка>

projects/<id>/deck.json:
  {"design": 12, "format": "1:1", "transition": "cube", "appear": "up", "tag": "урок 2.1", "footer": "@kuraylife",
   "slides": [{"type": "cover", "title": "Сайт [[за вечер]]", "sub": "...", "theme": "dark"}, ...]}
Пустые поля слайда берутся из образца и попадают в список «ЗАПОЛНИТЬ». В заголовке [[слово]] = выделение плашкой.
Темы слайда: light (по умолчанию), dark, brand, soft. Поле "steps": true у слайда = элементы появляются по клику.
Работает для дизайнов kind=tokens. Готовые презентации (own, external) агент адаптирует по WORKFLOW.md.
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESIGNS = json.load(open(os.path.join(ROOT, "catalog", "designs.json"), encoding="utf-8"))
FONTS = {f["name"]: f for f in json.load(open(os.path.join(ROOT, "catalog", "fonts.json"), encoding="utf-8"))}
P = json.load(open(os.path.join(ROOT, "structure", "presets.json"), encoding="utf-8"))
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
E = html.escape


def rich(s):
    """[[слово]] → выделение; остальное экранируется."""
    return re.sub(r"\[\[(.+?)\]\]", r'<span class="hl">\1</span>', E(s or ""))


def design_by(n):
    for d in DESIGNS:
        if str(d["n"]) == str(n) or d["id"] == str(n):
            return d
    sys.exit(f"нет дизайна {n}. Список: python3 scripts/catalog.py")


def fstack(name, kind=None):
    t = kind or FONTS.get(name, {}).get("type", "sans")
    return f"'{name}'," + ("Georgia,serif" if t == "serif" else "monospace" if t == "mono" else "system-ui,sans-serif")


def font_url(t):
    fams = {}
    for name, w in ((t["fh"], t.get("fh_w", 700)), (t["fb"], 400), (t.get("fm", "JetBrains Mono"), 500)):
        ws = set(FONTS.get(name, {}).get("weights", [400, 700]))
        fams.setdefault(name, set()).update(({w, 400, 600, 700} & ws) or ws)
    q = "&".join("family=" + urllib.parse.quote(n).replace("%20", "+") + ":wght@" + ";".join(map(str, sorted(ws))) for n, ws in fams.items())
    return "https://fonts.googleapis.com/css2?" + q + "&display=swap"


def root_vars(t, st, fmt):
    w, h = P["formats"][fmt]["w"], P["formats"][fmt]["h"]
    u = min(w, h) / 100
    dark = t.get("dark")
    return (":root{" + f"--w:{w}px;--h:{h}px;--u:{u:.2f}px;--pad:{u * 6.4:.0f}px;"
            f"--bg:{t['bg']};--surface:{t['surface']};--text:{t['text']};--muted:{t['muted']};--brand:{t['brand']};"
            f"--brand-dark:{t['brand_dark']};--soft:{t['brand_soft']};--accent:{t['accent']};--on-brand:{t['on_brand']};"
            f"--dark-bg:{st.get('dark_bg', t['text'] if not dark else t['surface'])};--dark-text:{st.get('dark_text', t['bg'] if not dark else t['text'])};"
            f"--stage:{st.get('stage', '#0b0b0c')};--r:{t['radius']}px;--fh:{fstack(t['fh'])};--fb:{fstack(t['fb'])};"
            f"--fm:{fstack(t.get('fm', 'JetBrains Mono'), 'mono')};--fh-w:{t.get('fh_w', 700)}" + "}"
            f"@page{{size:{w}px {h}px;margin:0}}")


# ---------- образец содержания ----------
def demo_slide(kind, d, i):
    T = d["topic"]
    base = {
        "cover": {"title": T.replace("ИИ", "[[ИИ]]", 1) if "ИИ" in T else f"[[{T.split()[0]}]] " + " ".join(T.split()[1:]),
                  "sub": d["who"], "text": "Коротко: что получит зритель за эту презентацию.", "theme": "dark"},
        "agenda": {"title": "План на [[сегодня]]", "items": ["Зачем это нужно", "Как устроено", "Пошаговая инструкция", "Ошибки новичков", "Что сделать сейчас"]},
        "section": {"num": "0" + str(1 + i % 3), "title": ["Зачем", "Как это работает", "Практика"][i % 3], "text": "одна строка о том, что будет в разделе", "theme": "brand"},
        "text": {"title": "Одна мысль — [[один слайд]]", "text": "Короткий абзац на 2-3 строки: объясняем главное простыми словами, без воды и терминов."},
        "steps": {"title": "4 шага до [[результата]]", "items": [["Задача", "что хотим получить"], ["Промпт", "как сказать ИИ"], ["Проверка", "что посмотреть глазами"], ["Запуск", "ссылка, которую можно отправить"]], "steps": True},
        "stat": {"label": "результат клиента", "was": "491", "value": "50,9K", "text": "охват за месяц после запуска", "theme": "dark"},
        "quote": {"text": "Сделала сайт за вечер, хотя никогда не писала код. Клиенты пишут каждый день.", "who": "Айгерим, ученица потока"},
        "image": {"title": "Как это [[выглядит]]", "label": "скриншот или фото"},
        "split": {"title": "Покажите [[результат]] глазами", "text": "Слева мысль, справа скриншот, фото или схема. Так слайд запоминается лучше.", "label": "ваш скриншот"},
        "compare": {"title": "Было → [[стало]]", "left": ["Без ИИ", "2 недели и 300 000 ₸ на подрядчика"], "right": ["С ИИ", "1 вечер и подписка 20 $"]},
        "table": {"title": "Тарифы и [[что внутри]]", "rows": [["Старт", "записи уроков, чат", "90 000 ₸"], ["Про", "+ разборы, куратор", "190 000 ₸"], ["VIP", "+ личный созвон", "300 000 ₸"]], "head": ["тариф", "что внутри", "цена"]},
        "timeline": {"title": "Путь за [[30 дней]]", "items": [["Неделя 1", "тема и структура"], ["Неделя 2", "дизайн и тексты"], ["Неделя 3", "сборка"], ["Неделя 4", "запуск и продажи"]]},
        "cards": {"title": "Что [[внутри]]", "items": [["89", "дизайнов", "у каждого видео-превью"], ["16", "типов слайдов", "от обложки до призыва"], ["8", "переходов", "куб, переворот, полёт камеры"]], "steps": True},
        "chat": {"title": "Промпт → [[ответ]]", "msgs": [["me", "Сделай презентацию урока в моём стиле: 12 слайдов, квадрат, переход куб."], ["ai", "Готово: 12 слайдов, тема тёмная, 3D-куб. Открыть index.html или собрать PDF?"]]},
        "code": {"title": "Одной [[командой]]", "bar": "терминал", "code": "python3 scripts/build_deck.py projects/my-lesson --pdf\n<u>✓</u> 12 слайдов → deck/index.html\n<u>✓</u> PDF → deck/presentation.pdf", "theme": "dark"},
        "cta": {"title": "Напиши кодовое слово", "word": d["word"], "text": "и получи шаблон и инструкцию", "theme": "brand"},
    }
    return dict(base[kind], type=kind)


# ---------- рендер слайдов ----------
def r_cover(s):
    return (f'<div class="kicker">{E(s.get("sub", ""))}</div><h1>{rich(s["title"])}</h1>'
            f'<p class="lead">{E(s.get("text", ""))}</p>')


def r_agenda(s):
    li = "".join(f'<li class="f"><i>{k + 1:02d}</i><div><b>{E(x)}</b></div></li>' for k, x in enumerate(s["items"]))
    return f'<h2>{rich(s["title"])}</h2><ul class="steps">{li}</ul>'


def r_section(s):
    return f'<div class="num">{E(s.get("num", "01"))}</div><h1>{rich(s["title"])}</h1><p class="lead">{E(s.get("text", ""))}</p>'


def r_text(s):
    return f'<h2>{rich(s["title"])}</h2><p class="lead" style="max-width:46ch">{E(s.get("text", ""))}</p>'


def r_steps(s):
    li = "".join(f'<li class="f"><i>{k + 1:02d}</i><div><b>{E(a)}</b><p>{E(b)}</p></div></li>' for k, (a, b) in enumerate(s["items"]))
    return f'<h2>{rich(s["title"])}</h2><ul class="steps">{li}</ul>'


def r_stat(s):
    was = f'<span class="was">{E(s["was"])}</span> <span class="mono" style="font-size:calc(var(--u)*4)">→</span>' if s.get("was") else ""
    return f'<div class="kicker">{E(s.get("label", ""))}</div><div>{was}</div><div class="big f">{E(s["value"])}</div><p class="lead">{E(s.get("text", ""))}</p>'


def r_quote(s):
    return f'<blockquote>{E(s["text"])}</blockquote><div class="who">— {E(s.get("who", ""))}</div>'


def art(s):
    if s.get("img"):
        return f'<div class="art" style="background:url({E(s["img"])}) center/cover"></div>'
    return f'<div class="art" data-label="{E(s.get("label", "картинка"))}"></div>'


def r_image(s):
    pic = art(s).replace('class="art"', 'class="art" style="flex:1"', 1)
    return f'<h2>{rich(s.get("title", ""))}</h2><div style="flex:1;display:flex">{pic}</div>'


def r_split(s):
    return f'<div class="split"><div><h2>{rich(s["title"])}</h2><p class="lead" style="margin-top:calc(var(--u)*2)">{E(s.get("text", ""))}</p></div><div class="f">{art(s)}</div></div>'


def r_compare(s):
    L, R = s["left"], s["right"]
    return (f'<h2>{rich(s["title"])}</h2><div class="vs"><div class="card"><div class="k">{E(L[0])}</div><b>{E(L[1])}</b></div>'
            f'<div class="card f"><div class="k">{E(R[0])}</div><b>{E(R[1])}</b></div></div>')


def r_table(s):
    head = "".join(f"<th>{E(h)}</th>" for h in s.get("head", []))
    rows = "".join("<tr>" + "".join(f"<td>{E(c)}</td>" for c in r) + "</tr>" for r in s["rows"])
    return f'<h2>{rich(s["title"])}</h2><table><tr>{head}</tr>{rows}</table>'


def r_timeline(s):
    it = "".join(f'<div class="f"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in s["items"])
    return f'<h2>{rich(s["title"])}</h2><div class="tl">{it}</div>'


def r_cards(s):
    n = len(s["items"])
    cols = "g2" if n in (2, 4) else "g3"
    it = "".join(f'<div class="card f"><div class="big">{E(a)}</div><b>{E(b)}</b><span>{E(c)}</span></div>' for a, b, c in s["items"])
    return f'<h2>{rich(s["title"])}</h2><div class="grid {cols}">{it}</div>'


def r_chat(s):
    m = "".join((f'<div class="msg me f">{E(t)}</div>' if who == "me" else f'<div class="msg ai f"><small>{E(s.get("ai", "Claude Code"))}</small>{E(t)}</div>')
                for who, t in s["msgs"])
    return f'<h2>{rich(s["title"])}</h2><div class="chat">{m}</div>'


def r_code(s):
    code = E(s["code"]).replace("&lt;u&gt;", "<u>").replace("&lt;/u&gt;", "</u>")
    return f'<h2>{rich(s["title"])}</h2><div class="term"><div class="bar"><i></i><i></i><i></i><span>{E(s.get("bar", ""))}</span></div><pre>{code}</pre></div>'


def r_cta(s):
    w = f'<div><span class="word">{E(s["word"])}</span></div>' if s.get("word") else ""
    return f'<h1>{rich(s["title"])}</h1>{w}<p class="lead">{E(s.get("text", ""))}</p>'


R = {k[2:]: v for k, v in globals().items() if k.startswith("r_")}
ROUTE = '<svg class="route" viewBox="0 0 1000 60" preserveAspectRatio="none"><path d="M0,40 C150,5 250,55 400,30 S650,5 800,35 S950,50 1000,20"/></svg>'


def render(design, slides, fmt, transition, appear, tag="", footer="", title=""):
    t = design["tokens"]
    st = design.get("style", {})
    js = open(os.path.join(ROOT, "template", "deck.js"), encoding="utf-8").read()
    css = open(os.path.join(ROOT, "template", "deck.css"), encoding="utf-8").read()
    n = len(slides)
    out = []
    for i, s in enumerate(slides):
        kind = s["type"]
        th = s.get("theme", "light")
        cls = {"light": "", "dark": "dark", "brand": "brand", "soft": "soft"}[th]
        center = " center" if kind in ("section", "cta", "quote") else ""
        top = " top" if kind in ("table", "cards", "chat", "code", "steps", "agenda", "timeline", "image") and fmt != "16:9" else ""
        html_ = R[kind](s)
        if not s.get("steps") and kind not in ("agenda",):
            html_ = html_.replace(' class="f"', "").replace(" f\"", "\"").replace(' f"', '"')
        meta = (f'<div class="meta t"><b>{E(tag)}</b><span>{i + 1:02d} / {n:02d}</span></div>'
                f'<div class="meta b"><span>{E(footer)}</span><span>{E(title)}</span></div>')
        route = ROUTE if st.get("route") else ""
        out.append(f'<section class="slide {cls}{center}{top}" data-type="{kind}">{meta}{route}{html_}</section>')
    bcls = f't-{transition} a-{appear} bg-{st.get("bg", "dots")} h-{st.get("hl", "plate")} c-{st.get("cards", "solid")}'
    furl = font_url(t)
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title or 'Презентация')}</title>
<!-- дизайн №{design['n']} «{E(design['name'])}», переход {transition}, собрано scripts/build_deck.py -->
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{furl}" rel="stylesheet">
<style>{root_vars(t, st, fmt)}
{css}</style></head>
<body class="{bcls}"><div class="stage"><div class="deck">
{''.join(out)}
</div></div><div class="progress"><i></i></div><div class="counter"></div>
<script>{js}</script></body></html>"""


def pdf(index_html, out_pdf):
    tmp = tempfile.mkdtemp()
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files", f"--user-data-dir={tmp}/ud",
                    "--no-pdf-header-footer", "--virtual-time-budget=15000", f"--print-to-pdf={out_pdf}",
                    "file://" + os.path.abspath(index_html) + "?print"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=600)
    print("PDF:", out_pdf)


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__); return
    opt = lambda k, dflt=None: a[a.index(k) + 1] if k in a else dflt
    if a[0] == "--demo":
        d = design_by(a[1])
        if d["kind"] != "tokens":
            sys.exit(f"№{d['n']} это готовая презентация, а не палитра: {d.get('path') or d.get('url')}")
        preset = opt("--preset", d.get("preset", "lesson"))
        pr = P["presets"][preset]
        fmt = opt("--format", pr["format"])
        tr = opt("--transition", d.get("transition", "fade"))
        slides = [demo_slide(k, pr["demo"], i) for i, k in enumerate(pr["slides"])]
        page = render(d, slides, fmt, tr, d.get("appear", "up"), pr["demo"]["who"], "@kuraylife" if d.get("author") == "Куралай" else "", d["name"])
        out = opt("--out", os.path.join(ROOT, "gallery", "live", str(d["n"])))
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
        print(os.path.join(out, "index.html")); return
    proj = a[0].rstrip("/")
    cfg = json.load(open(os.path.join(proj, "deck.json"), encoding="utf-8"))
    d = design_by(cfg["design"])
    if d["kind"] != "tokens":
        sys.exit(f"№{d['n']} «{d['name']}» — готовая презентация. Агент копирует её в {proj}/deck/ и меняет по WORKFLOW.md, этап 5.")
    if "tokens" in cfg:
        d = dict(d, tokens=dict(d["tokens"], **cfg["tokens"]))
    if "style" in cfg:
        d = dict(d, style=dict(d.get("style", {}), **cfg["style"]))
    pr = P["presets"].get(cfg.get("preset", "lesson"), P["presets"]["lesson"])
    slides, missing = [], []
    for i, s in enumerate(cfg["slides"]):
        demo = demo_slide(s["type"], pr["demo"], i)
        miss = [k for k in demo if k not in s and k not in ("type", "theme")]
        if miss:
            missing.append(f"слайд {i + 1} ({s['type']}): {', '.join(miss)}")
        slides.append(dict(demo, **s))
    fmt = cfg.get("format", pr["format"])
    page = render(d, slides, fmt, cfg.get("transition", d.get("transition", "fade")), cfg.get("appear", "up"),
                  cfg.get("tag", ""), cfg.get("footer", ""), cfg.get("title", ""))
    outdir = os.path.join(proj, "deck")
    os.makedirs(outdir, exist_ok=True)
    idx = os.path.join(outdir, "index.html")
    open(idx, "w", encoding="utf-8").write(page)
    print("готово:", idx, f"({len(slides)} слайдов, {fmt}, переход {cfg.get('transition', d.get('transition', 'fade'))})")
    if missing:
        print("ЗАПОЛНИТЬ (сейчас стоит текст-образец):\n  " + "\n  ".join(missing))
    if "--pdf" in a:
        pdf(idx, os.path.join(outdir, "presentation.pdf"))


if __name__ == "__main__":
    main(sys.argv[1:])
