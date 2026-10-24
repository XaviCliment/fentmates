#!/usr/bin/env python3
"""
Genera les guies «Amb la calculadora» a partir de guies.py.
Ús (des de la carpeta arrel del web):  python3 _eines/casio/build_casio.py
"""
import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from guies import GUIDES  # noqa: E402

# nom intern -> (text de la tecla, classe, descripció)
KEYS = {
    "HOME": ("⌂", "fn", "HOME"), "CONFIG": ("☰", "fn", "CONFIG (ajustos)"),
    "CATALOG": ("CATALOG", "fn", "CATALOG"), "TOOLS": ("⋯", "fn", "TOOLS (eines)"),
    "FORMAT": ("FORMAT", "fn", "FORMAT"), "VAR": ("x⇄", "fn", "VARIABLE"),
    "FUNC": ("f(x)", "fn", "FUNCTION"), "OK": ("OK", "ok", "OK"), "EXE": ("EXE", "exe", "EXE (executar)"),
    "AC": ("AC", "ac", "AC"), "BACK": ("↶", "fn", "Tornar enrere"), "DEL": ("DEL", "ac", "Esborrar"),
    "SHIFT": ("⇧", "shift", "SHIFT"), "FRAC": ("▭⁄▭", "num", "Fracció"),
    "SQRT": ("√▭", "num", "Arrel quadrada"), "SQ": ("▭²", "num", "Quadrat"), "POW": ("▭^▭", "num", "Potència"),
    "X": ("x", "num", "Tecla x"), "UP": ("▲", "cur", "Cursor amunt"), "DOWN": ("▼", "cur", "Cursor avall"),
    "LEFT": ("◀", "cur", "Cursor esquerra"), "RIGHT": ("▶", "cur", "Cursor dreta"),
}
LEGEND = ["HOME", "CONFIG", "CATALOG", "TOOLS", "FORMAT", "VAR", "FUNC", "SHIFT", "OK", "EXE", "AC",
          "FRAC", "SQRT", "POW", "X", "RIGHT"]


def key(name):
    if name in KEYS:
        t, c, d = KEYS[name]
        return '<kbd class="k %s" title="%s">%s</kbd>' % (c, d, html.escape(t))
    return '<kbd class="k num">%s</kbd>' % html.escape(name)


def fmt(s):
    # protegeix el LaTeX perquè no es toque
    maths = []
    def keep(m):
        maths.append(m.group(0)); return "\x00%d\x00" % (len(maths) - 1)
    s = re.sub(r"\$[^$]+\$", keep, s)
    s = re.sub(r"\[\[(.+?)\]\]", lambda m: key(m.group(1)), s)
    s = re.sub(r"<<(.+?)>>", lambda m: '<span class="menu">%s</span>' % html.escape(m.group(1)), s)
    s = s.replace(" › ", ' <span class="gt">›</span> ')
    return re.sub(r"\x00(\d+)\x00", lambda m: maths[int(m.group(1))], s)


def screen(s):
    # [[a,b],[c,d]] -> matriu dibuixada
    def mat(m):
        rows = re.findall(r"\[([^\[\]]+)\]", m.group(0))
        return '<span class="mat">' + "".join(
            "<span>" + "".join("<i>%s</i>" % html.escape(c.strip()) for c in r.split(",")) + "</span>" for r in rows) + "</span>"
    s = html.escape(s, quote=False)
    s = re.sub(r"\[\[[^\]]*\](?:,\[[^\]]*\])*\]", mat, s)
    return s.replace(" · ", '<span class="sep">·</span>')


def section(i, sec):
    out = ['<section class="card" id="s%d">' % (i + 1),
           '<h2><span class="n">%d</span>%s</h2>' % (i + 1, fmt(sec["t"]))]
    if sec.get("why"):
        out.append('<p class="why">%s</p>' % fmt(sec["why"]))
    out.append('<ol class="steps">' + "".join("<li>%s</li>" % fmt(st) for st in sec["steps"]) + "</ol>")
    out.append('<div class="example"><div class="ex-h">Exemple</div><p class="ex-q">%s</p>' % fmt(sec["ex"]))
    out.append('<div class="ex-keys">%s</div>' % fmt(sec["keys"]))
    out.append('<div class="lcd"><span class="lcd-l">Pantalla</span><span class="lcd-v">%s</span></div></div>' % screen(sec["screen"]))
    if sec.get("tip"):
        out.append('<p class="tip"><b>💡 Consell:</b> %s</p>' % fmt(sec["tip"]))
    out.append("</section>")
    return "\n".join(out)


def page(g):
    tpl = open(os.path.join(HERE, "plantilla.html"), encoding="utf-8").read()
    toc = "".join('<li><a href="#s%d">%s</a></li>' % (i + 1, fmt(s["t"])) for i, s in enumerate(g["sections"]))
    legend = "".join('<li>%s<span>%s</span></li>' % (key(k), KEYS[k][2]) for k in LEGEND)
    body = "\n".join(section(i, s) for i, s in enumerate(g["sections"]))
    rep = {"{{TITLE}}": g["title"], "{{UNIT}}": g["unit"], "{{INTRO}}": fmt(g["intro"]), "{{COLOR}}": g["color"],
           "{{BACK}}": g["back"], "{{BACK_LABEL}}": g["back_label"], "{{TOC}}": toc, "{{LEGEND}}": legend,
           "{{BODY}}": body, "{{N}}": str(len(g["sections"]))}
    for a, b in rep.items():
        tpl = tpl.replace(a, b)
    return tpl


for g in GUIDES:
    path = os.path.join(ROOT, g["file"])
    open(path, "w", encoding="utf-8").write(page(g))
    print(g["file"], len(g["sections"]), "apartats")

# FentMates: enllaça el tema comú (logo i colors del bloc) a les pàgines generades
import runpy as _runpy, os as _os
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "_eines":
    _d = _os.path.dirname(_d)
_runpy.run_path(_os.path.join(_d, "tema", "aplica.py"), run_name="__main__")
