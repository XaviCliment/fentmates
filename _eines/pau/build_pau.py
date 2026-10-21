#!/usr/bin/env python3
"""Genera les pàgines d'exercicis tipus PAU a partir dels fitxers de text transcrits."""
import json, re, sys, html, os

SP = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]  # carpeta materials/2batx-ccss

MONTHS = {"Juny": 6, "Juliol": 7, "Setembre": 9}


def parse(path):
    out = []
    for block in open(path, encoding="utf-8").read().split("\n## ")[0:]:
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            block = block[3:]
        head, *lines = block.split("\n")
        kind, conv = [s.strip() for s in head.split("|")]
        body, parts, conds = [], [], []
        img = None

        def flush_conds():
            if conds:
                body.append('<ul class="conds">' + "".join("<li>%s</li>" % c for c in conds) + "</ul>")
                conds.clear()

        for ln in lines:
            ln = ln.rstrip()
            if not ln:
                continue
            if ln.startswith("- "):
                flush_conds()
                parts.append(txt(ln[2:]))
            elif ln.startswith("* "):
                conds.append(txt(ln[2:]))
            elif ln.startswith("IMG "):
                flush_conds()
                img = ln[4:].strip()
            elif ln.startswith("<"):
                flush_conds()
                body.append('<div class="tbl">%s</div>' % ln)
            elif ln.startswith("$$") and ln.endswith("$$"):
                flush_conds()
                body.append('<div class="disp">%s</div>' % txt(ln))
            else:
                flush_conds()
                body.append("<p>%s</p>" % txt(ln))
        flush_conds()
        h = "".join(body)
        if parts:
            h += '<ol class="parts">' + "".join("<li>%s</li>" % p for p in parts) + "</ol>"
        if img:
            h += '<figure><img src="../../assets/img/%s" alt="Esquema de l\'enunciat" loading="lazy"></figure>' % img
        m = re.match(r"(\w+) (\d{4})( extra)?", conv)
        year = int(m.group(2)) if m else 0
        month = MONTHS.get(m.group(1), 0) if m else 0
        out.append({"k": kind, "conv": conv, "y": year, "m": month + (0.5 if m and m.group(3) else 0), "h": h})
    return out


def txt(s):
    s = html.escape(s, quote=False)
    return s.replace("&lt;br&gt;", "<br>")


def parse_sol(path):
    """Solucions: blocs "## TIPUS | Convocatòria | n" seguits d'HTML."""
    sol = {}
    if not os.path.exists(path):
        return sol
    for block in open(path, encoding="utf-8").read().split("\n## ")[1:]:
        head, _, body = block.partition("\n")
        kind, conv, n = [s.strip() for s in head.split("|")]
        sol[(kind, conv, int(n))] = body.strip()
    return sol


def attach_sol(items, sol):
    seen = {}
    for e in items:
        key = (e["k"], e["conv"])
        seen[key] = seen.get(key, 0) + 1
        s = sol.pop((e["k"], e["conv"], seen[key]), None)
        if s:
            e["s"] = s


alg = parse(os.path.join(SP, "alg.txt"))
pl = parse(os.path.join(SP, "pl.txt"))
sol = parse_sol(os.path.join(SP, "sol.txt"))
attach_sol(alg, sol)
attach_sol(pl, sol)
if sol:
    print("AVÍS: solucions sense exercici:", sorted(sol))
units = [
    ("pau-u1-matrius.html", "1", "Matrius i determinants", [e for e in alg if e["k"] == "M"]),
    ("pau-u2-sistemes.html", "2", "Sistemes d'equacions lineals", [e for e in alg if e["k"] == "S"]),
    ("pau-u3-programacio-lineal.html", "3", "Programació lineal", pl),
]
tpl = open(os.path.join(SP, "pau_template.html"), encoding="utf-8").read()
for fn, num, name, items in units:
    data = [{"conv": e["conv"], "y": e["y"], "m": e["m"], "h": e["h"], **({"s": e["s"]} if "s" in e else {})} for e in items]
    page = (tpl.replace("{{NUM}}", num).replace("{{NAME}}", name)
               .replace("{{COUNT}}", str(len(items))).replace("{{KEY}}", fn.replace(".html", ""))
               .replace("{{DATA}}", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")))
    open(os.path.join(OUT, fn), "w", encoding="utf-8").write(page)
    print(fn, len(items))
