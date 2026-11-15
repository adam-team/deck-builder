#!/usr/bin/env python3
"""Образцы тем reveal.js (engines/reveal, лицензия MIT) на одном и том же содержании.

  python3 scripts/build_reveal.py              # все темы из catalog/designs.json → gallery/live/reveal-<тема>/index.html
  python3 scripts/build_reveal.py projects/<id> --theme moon --transition convex   # презентация ученицы на reveal.js

Для ученицы: deck.json тот же, что для build_deck.py (поле "engine": "reveal"); слайды переводятся в разметку reveal.js,
движок копируется в projects/<id>/deck/reveal/. Переходы reveal.js: none, fade, slide, convex, concave, zoom.
"""
import html
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape

DEMO = [
    ("cover", "Слайды с ИИ", "вебинар · вайбкодинг · 60 минут"),
    ("list", "План на сегодня", ["Зачем это нужно", "Как устроено", "Пошаговая инструкция", "Что сделать сейчас"]),
    ("big", "50,9K", "охват за месяц после запуска"),
    ("code", "Одной командой", "python3 scripts/build_deck.py projects/my-lesson --pdf"),
    ("quote", "Сделала сайт за вечер, хотя никогда не писала код.", "Айгерим, ученица потока"),
    ("cover", "Спасибо!", "напиши кодовое слово СТАРТ"),
]


def section(kind, a, b):
    if kind == "cover":
        return f"<section><h1>{E(a)}</h1><p>{E(b)}</p></section>"
    if kind == "list":
        return f"<section><h2>{E(a)}</h2><ul>" + "".join(f'<li class="fragment fade-up">{E(x)}</li>' for x in b) + "</ul></section>"
    if kind == "big":
        return f'<section><h1 style="font-size:3.4em">{E(a)}</h1><p class="fragment">{E(b)}</p></section>'
    if kind == "code":
        return f'<section><h2>{E(a)}</h2><pre><code class="language-bash">{E(b)}</code></pre></section>'
    if kind == "quote":
        return f"<section><blockquote>«{E(a)}»</blockquote><p><small>— {E(b)}</small></p></section>"
    return ""


def page(sections, theme, transition, base):
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>reveal.js · {E(theme)}</title>
<link rel="stylesheet" href="{base}/reset.css"><link rel="stylesheet" href="{base}/reveal.css">
<link rel="stylesheet" href="{base}/theme/{E(theme)}.css"><link rel="stylesheet" href="{base}/plugin/highlight/monokai.css">
</head><body><div class="reveal"><div class="slides">
{''.join(sections)}
</div></div>
<script src="{base}/reveal.js"></script><script src="{base}/plugin/highlight.js"></script>
<script>
var q = new URLSearchParams(location.search), auto = parseInt(q.get('autoplay')) || 0;
Reveal.initialize({{hash: true, transition: '{E(transition)}', backgroundTransition: 'fade', autoSlide: auto, loop: false,
  controls: !auto, progress: !auto, plugins: [RevealHighlight]}});
</script></body></html>"""


def demos():
    designs = json.load(open(os.path.join(ROOT, "catalog", "designs.json"), encoding="utf-8"))
    for d in designs:
        if d.get("engine") != "reveal":
            continue
        out = os.path.join(ROOT, "gallery", "live", "reveal-" + d["theme"])
        os.makedirs(out, exist_ok=True)
        html_ = page([section(*s) for s in DEMO], d["theme"], d["transition"], "../../../engines/reveal")
        open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html_)
        print("✓", d["name"])


def project(proj, theme, transition):
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import build_deck as bd
    cfg = json.load(open(os.path.join(proj, "deck.json"), encoding="utf-8"))
    pr = bd.P["presets"].get(cfg.get("preset", "lesson"), bd.P["presets"]["lesson"])
    secs = []
    for i, s in enumerate(cfg["slides"]):
        s = dict(bd.demo_slide(s["type"], pr["demo"], i), **s)
        body = bd.R[s["type"]](s).replace(' class="f"', ' class="fragment"').replace(' f"', ' fragment"')
        secs.append(f"<section>{body}</section>")
    outdir = os.path.join(proj, "deck")
    os.makedirs(outdir, exist_ok=True)
    shutil.copytree(os.path.join(ROOT, "engines", "reveal"), os.path.join(outdir, "reveal"), dirs_exist_ok=True)
    open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(page(secs, theme, transition, "reveal"))
    print("готово:", os.path.join(outdir, "index.html"), "· PDF: открыть index.html?print-pdf в Chrome → Печать → Сохранить как PDF")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        demos()
    elif a[0] in ("-h", "--help"):
        print(__doc__)
    else:
        opt = lambda k, dflt: a[a.index(k) + 1] if k in a else dflt
        project(a[0].rstrip("/"), opt("--theme", "white"), opt("--transition", "convex"))
