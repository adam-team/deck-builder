#!/usr/bin/env python3
"""Одноразовая сборка catalog/designs.json для презентаций. Дальше правим сам JSON."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SB = json.load(open(os.path.expanduser("~/Projects/site-builder/catalog/designs.json"), encoding="utf-8"))
out = []
def add(**k):
    k["n"] = len(out) + 1; out.append(k)

# 1. Мои презентации (PDF)
for f, name, fmt, mood in [
  ("brandbook.pdf", "Урок: Брендбук с Claude Code", "1:1", "26 слайдов в стиле брендбука: сетка точек, красные плашки, окна приложений"),
  ("design-style.pdf", "Урок: Дизайн — как выбрать стиль", "1:1", "25 слайдов: листы стилей, таблицы, шаги"),
  ("site-design.pdf", "Урок: Дизайн сайта", "1:1", "24 слайда: скриншоты галереи, терминал, задание"),
  ("montazh-rils.pdf", "Урок: Монтаж рилсов и уроков", "16:9", "38 широких слайдов про монтаж с агентом"),
  ("platform-builder.pdf", "Урок: Platform Builder", "16:9", "60 слайдов: платформа с нуля по готовому коду"),
  ("boss-vision-10.pdf", "BOSS VISION: 10 вариантов дизайна", "16:9", "презентация дизайн-концепций приложения"),
  ("boss-vision-v2.pdf", "BOSS VISION: дизайн v2", "16:9", "вторая версия: синий и золото"),
]:
    add(id=f[:-4], name=name, kind="own", group="own", path="designs/own/" + f, format=fmt, mood=mood, niche="уроки, продукт, кейсы",
        dark=False, author="Куралай", license="свой")

K = dict(bg="#F4F2EF", surface="#FFFFFF", text="#0E0D0D", muted="#A69D92", brand="#C8102E", brand_dark="#8E0B20", brand_soft="#F3EDE4",
         accent="#FF4D63", on_brand="#FFFFFF", fh="Unbounded", fb="Manrope", fm="JetBrains Mono", radius=24, dark=False, fh_w=700)
KS = dict(bg="dots", hl="plate", cards="solid", route=True, dark_bg="#0E0D0D", dark_text="#F3EDE4", stage="#0E0D0D")

# 2. Мой стиль + все переходы (одна презентация, разная анимация)
TR = [("cube", "Куб 3D"), ("orbit", "Полёт камеры (Prezi)"), ("flip", "Переворот 3D"), ("convex", "Страница 3D"),
      ("cards", "Стопка карточек"), ("zoom", "Приближение"), ("slide", "Сдвиг"), ("fade", "Проявление")]
for tr, nm in TR:
    add(id="tr-" + tr, name=f"Мой стиль · {nm}", kind="tokens", group="anim", tokens=K, style=KS, transition=tr, appear="up",
        preset="lesson", format="1:1", mood=f"брендбук Куралай v2, переход «{nm}»", niche="уроки, вебинары, карусели", dark=False,
        author="Куралай", license="свой")

# 3. Тренды для контента (палитры сайтов + стиль презентации)
deck_style = {
 "bento": (dict(bg="none", hl="color", cards="solid"), "convex", "zoom", "sales"),
 "glass": (dict(bg="glow", hl="grad", cards="glass", stage="#05070f"), "orbit", "blur", "webinar"),
 "brutal": (dict(bg="grid", hl="plate", cards="brutal"), "cards", "up", "carousel"),
 "luxe": (dict(bg="none", hl="color", cards="outline"), "fade", "blur", "about"),
 "aurora": (dict(bg="blobs", hl="grad", cards="solid"), "flip", "up", "stories"),
 "swiss": (dict(bg="grid", hl="plate", cards="outline"), "slide", "left", "case"),
 "clay": (dict(bg="blobs", hl="under", cards="solid"), "cards", "zoom", "lesson"),
 "noir": (dict(bg="glow", hl="color", cards="outline", stage="#000"), "cube", "blur", "pitch"),
 "steppe": (dict(bg="dots", hl="plate", cards="solid", route=True), "convex", "up", "workshop"),
 "mint": (dict(bg="dots", hl="under", cards="outline"), "zoom", "up", "sales"),
}
for d in SB:
    if d["group"] == "trend":
        st, tr, ap, pr = deck_style[d["id"]]
        t = dict(d["tokens"], fm="JetBrains Mono")
        add(id="trend-" + d["id"], name=d["name"], kind="tokens", group="trend", tokens=t, style=st, transition=tr, appear=ap, preset=pr,
            mood=d["mood"], niche=d["niche"], dark=d["dark"], author="Куралай", license="свой")

# 4. Палитры платформ (12 самых разных) — в форматах контента
pick = {"pb-01": "carousel", "pb-03": "pitch", "pb-07": "webinar", "pb-08": "lesson", "pb-12": "about", "pb-14": "sales",
        "pb-16": "stories", "pb-17": "case", "pb-19": "workshop", "pb-27": "lesson", "pb-30": "webinar", "pb-32": "about"}
trs = ["slide", "convex", "zoom", "fade", "cube", "cards", "flip", "orbit"]
for i, d in enumerate([x for x in SB if x["id"] in pick]):
    t = dict(d["tokens"], fm="JetBrains Mono")
    st = dict(bg="glow" if d["dark"] else ["dots", "none", "grid"][i % 3], hl=["plate", "color", "under"][i % 3], cards="glass" if d["dark"] else "solid")
    add(id="pal-" + d["id"], name=d["name"], kind="tokens", group="platform", tokens=t, style=st, transition=trs[i % 8], appear=["up", "zoom", "left"][i % 3],
        preset=pick[d["id"]], mood=d["mood"], niche=d["niche"], dark=d["dark"], author="Куралай", license="свой")

# 5. GitHub: reveal.js (14 тем) и impress.js (3D)
rv = [("black", True), ("white", False), ("league", True), ("beige", False), ("night", True), ("serif", False), ("simple", False),
      ("solarized", False), ("moon", True), ("dracula", True), ("sky", False), ("blood", True), ("black-contrast", True), ("white-contrast", False)]
rtr = ["slide", "convex", "concave", "zoom", "fade"]
for i, (th, dk) in enumerate(rv):
    add(id="reveal-" + th, name=f"reveal.js · {th}", kind="external", group="github", engine="reveal", theme=th, transition=rtr[i % 5],
        path=f"gallery/live/reveal-{th}/index.html", mood=f"тема «{th}» движка reveal.js, переход {rtr[i % 5]}", niche="выступления, IT, вебинары", dark=dk,
        author="hakimel", repo="https://github.com/hakimel/reveal.js", license="MIT")
for ex, name, mood in [("index.html", "impress.js · классическое демо", "полёт по 3D-холсту как в Prezi"),
                       ("examples/cube/index.html", "impress.js · куб", "слайды на гранях огромного куба"),
                       ("examples/3D-rotations/index.html", "impress.js · 3D-повороты", "слайды вращаются в пространстве"),
                       ("examples/classic-slides/index.html", "impress.js · классические слайды", "привычные слайды с 3D-переходами"),
                       ("examples/3D-positions/index.html", "impress.js · 3D-позиции", "слайды висят на разной глубине")]:
    add(id="impress-" + ex.split("/")[-2] if "/" in ex else "impress-demo", name=name, kind="external", group="github", engine="impress",
        path="engines/impress/" + ex, mood=mood, niche="выступления, wow-эффект", dark=False,
        author="impress", repo="https://github.com/impress/impress.js", license="MIT")

json.dump(out, open(os.path.join(ROOT, "catalog", "designs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
import collections; print(len(out), collections.Counter(x["group"] for x in out))
