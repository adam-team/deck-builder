#!/usr/bin/env python3
"""Этап «Структура» презентации.

  python3 scripts/structure.py sync                       # structure/presets.json → structure/presets.js (для конструктора)
  python3 scripts/structure.py list                       # задачи, форматы, типы слайдов, переходы
  python3 scripts/structure.py preset <задача>            # готовый порядок слайдов (текстом, для чата)
  python3 scripts/structure.py write projects/<id> <structure.json | задача>   # STRUCTURE.md + slides/format в deck.json
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(os.path.join(ROOT, "structure", "presets.json"), encoding="utf-8"))

def sync():
    open(os.path.join(ROOT, "structure", "presets.js"), "w", encoding="utf-8").write(
        "// собрано scripts/structure.py sync из structure/presets.json, руками не править\nwindow.PRESETS = " + json.dumps(P, ensure_ascii=False) + ";\n")
    print("structure/presets.js обновлён")

def write(proj, src):
    s = json.load(open(src, encoding="utf-8")) if os.path.exists(src) else {"preset": src, "format": P["presets"][src]["format"], "slides": P["presets"][src]["slides"]}
    bad = [t for t in s["slides"] if t not in P["slides"]]
    if bad: sys.exit("неизвестные типы слайдов: " + ", ".join(bad))
    os.makedirs(proj, exist_ok=True)
    md = ["# Структура презентации", "", f"Задача: **{P['presets'][s['preset']]['name']}** (`{s['preset']}`)", f"Формат: {s['format']} · {P['formats'][s['format']]['name']}"]
    if s.get("name"): md.append(f"Тема: {s['name']}")
    if s.get("goal"): md.append(f"Цель: {s['goal']}")
    md += ["", "| № | Слайд | Тип | Зачем |", "|---|---|---|---|"] + [f"| {i + 1} | {P['slides'][t]['name']} | `{t}` | {P['slides'][t]['why']} |" for i, t in enumerate(s["slides"])]
    if s.get("own_plan"): md += ["", "## План ученицы дословно", "", s["own_plan"]]
    open(os.path.join(proj, "STRUCTURE.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    dj = os.path.join(proj, "deck.json")
    cfg = json.load(open(dj, encoding="utf-8")) if os.path.exists(dj) else {}
    old = cfg.get("slides") or []
    cfg.update(preset=s["preset"], format=s["format"], title=s.get("name", cfg.get("title", "")),
               slides=[(old[i] if i < len(old) and old[i].get("type") == t else {"type": t}) for i, t in enumerate(s["slides"])])
    json.dump(cfg, open(dj, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"записано: {proj}/STRUCTURE.md и slides ({len(s['slides'])}) в {proj}/deck.json")

a = sys.argv[1:]
if not a or a[0] in ("-h", "--help"): print(__doc__)
elif a[0] == "sync": sync()
elif a[0] == "list":
    for k, p in P["presets"].items(): print(f"{k:10} {p['name']} · {p['format']} · {len(p['slides'])} слайдов")
    print(); [print(f"{k:5} {f['name']}: {f['note']}") for k, f in P["formats"].items()]
    print(); [print(f"{k:9} {t['name']}: {t['why']}") for k, t in P["slides"].items()]
    print(); [print(f"{k:7} {t['name']} ({t['kind']}): {t['note']}") for k, t in P["transitions"].items()]
elif a[0] == "preset":
    p = P["presets"][a[1]]; print(f"{p['name']} · формат {p['format']}")
    for i, t in enumerate(p["slides"]): print(f"  {i + 1}. {P['slides'][t]['name']} [{t}]: {P['slides'][t]['why']}")
elif a[0] == "write": write(a[1].rstrip("/"), a[2])
