#!/usr/bin/env python3
"""Global de Programació lineal (2n Batx CCSS): genera les dues pàgines.

    python3 _eines/examens/2batx-global-pl/build.py

  model1.src.html -> materials/2batx-ccss/global-pl-prova-model1.html
  pau.src.html    -> materials/2batx-ccss/global-pl-pau.html

Marcadors dels fitxers font (a més dels [[va||es||en]] de ../build.py):
  <!--FIG:clau|opcions-->  figura SVG de la regió (lp.svg; opcions = kwargs Python)
  <!--VTX:clau-->          sistemes que donen cada vèrtex
  <!--TAB:clau|opcions-->  taula vèrtex -> valor de la funció (lp.tab_html)
Abans de res s'executen totes les comprovacions de probs.py (vèrtexs i òptims).
Només tematitza les seues dues pàgines (no crida el aplica.py complet).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "_eines", "tema"))
import lp  # noqa: E402
from probs import P, run_checks  # noqa: E402
import aplica  # noqa: E402

VERSION = "20261120pl"
PAGES = [("model1.src.html", "global-pl-prova-model1.html"), ("pau.src.html", "global-pl-pau.html")]

BLOCK = re.compile(r"<(p|ul|ol|div|table|h\d|details|li|figure)\b")
MATH = re.compile(r"(?<!\\)\\\[(.*?)(?<!\\)\\\]|(?<!\\)\\\((.*?)(?<!\\)\\\)", re.S)
MARK = re.compile(r"\[\[(.*?)\]\]", re.S)


def localise_math(m):
    seg = m.group(0)
    if "[[" not in seg:
        return seg
    versions = [MARK.sub(lambda k: k.group(1).split("||")[i], seg) for i in range(3)]
    return "[[ " + " || ".join(versions) + " ]]"


def expand(m):
    parts = m.group(1).split("||")
    if len(parts) != 3:
        raise SystemExit("Marcador incorrecte: " + m.group(0)[:160])
    tag = "div" if any(BLOCK.search(p) for p in parts) else "span"
    return "".join('<%s data-l="%s">%s</%s>' % (tag, l, p.strip() if tag == "div" else p, tag)
                   for l, p in zip(("va", "es", "en"), parts))


def kw(s):
    return eval("dict(%s)" % s, {"F": lp.F}) if s else {}


def table(key, fname="f", fs=(1, 1), only=None, **k):
    Pk = P[key]
    if not isinstance(fs[0], (list, tuple)):
        fs, fname = [fs], [fname]
    marks = {}
    for j, f in enumerate(fs):
        vals = [(lp.ev(f, tuple(map(lp.fr, v))), n) for n, v in zip(Pk["names"], Pk["verts"])]
        hi, lo = max(v for v, _ in vals), min(v for v, _ in vals)
        for val, n in vals:
            if val == hi and only != "min":
                marks[(n, j)] = "vmx"
            if val == lo and only != "max":
                marks[(n, j)] = "vmn"
    return lp.tab_html(Pk, fname if len(fname) > 1 else fname[0], fs if len(fs) > 1 else fs[0], marks)


def markers(text):
    text = re.sub(r"<!--FIG:(\w+)\|?(.*?)-->", lambda m: lp.svg(P[m.group(1)], **kw(m.group(2))), text)
    text = re.sub(r"<!--VTX:(\w+)-->", lambda m: lp.vtx_html(P[m.group(1)]), text)
    text = re.sub(r"<!--TAB:(\w+)\|?(.*?)-->", lambda m: table(m.group(1), **kw(m.group(2))), text)
    return text


def build(src, out):
    text = open(os.path.join(HERE, src), encoding="utf-8").read()
    text, _, script = text.partition("<!--SCRIPT-->")
    text = markers(text)
    text = MATH.sub(localise_math, text)
    text = MARK.sub(expand, text)
    if "[[" in text or "]]" in text.replace("]]>", ""):
        raise SystemExit("Queden marcadors sense expandir a " + src)
    text = text.replace("/*BASE_CSS*/", open(os.path.join(HERE, "..", "base.css"), encoding="utf-8").read())
    text = text.replace("/*LP_CSS*/", open(os.path.join(HERE, "lp.css"), encoding="utf-8").read())
    path = os.path.join(ROOT, "materials", "2batx-ccss", out)
    open(path, "w", encoding="utf-8").write(text + script)
    aplica.VERSION = VERSION
    aplica.aplica_fitxer(path)
    print("ok", out, len(text + script))


if __name__ == "__main__":
    run_checks()
    print("comprovacions:", lp.CHECKS[0])
    for s, o in PAGES:
        if os.path.exists(os.path.join(HERE, s)):
            build(s, o)
