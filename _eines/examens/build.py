#!/usr/bin/env python3
"""Genera un model d'examen trilingüe (va/es/en) a partir d'un fitxer font.

Ús:  python3 _eines/examens/build.py _eines/examens/2batx-u1/model1.src.html materials/2batx-ccss/examen-u1-matrius-model1.html

Al fitxer font:
  [[text va||text es||text en]]  -> tres <span>/<div> amb data-l="va|es|en"
  /*BASE_CSS*/                   -> s'hi insereix _eines/examens/base.css (estil dels apunts)
  Tot el que hi ha després de <!--SCRIPT--> es copia tal qual (no s'expandeix).
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
text, _, script = text.partition("<!--SCRIPT-->")

BLOCK = re.compile(r"<(p|ul|ol|div|table|h\d|details|li)\b")
MATH = re.compile(r"(?<!\\)\\\[(.*?)(?<!\\)\\\]|(?<!\\)\\\((.*?)(?<!\\)\\\)", re.S)
MARK = re.compile(r"\[\[(.*?)\]\]", re.S)


def localise_math(m):
    """Una fórmula amb text traduït es duplica sencera per a cada idioma."""
    seg = m.group(0)
    if "[[" not in seg:
        return seg
    versions = [MARK.sub(lambda k: k.group(1).split("||")[i], seg) for i in range(3)]
    return "[[ " + " || ".join(versions) + " ]]"


def expand(m):
    parts = m.group(1).split("||")
    if len(parts) != 3:
        raise SystemExit("Marcador incorrecte: " + m.group(0)[:120])
    tag = "div" if any(BLOCK.search(p) for p in parts) else "span"
    return "".join('<%s data-l="%s">%s</%s>' % (tag, l, p.strip() if tag == "div" else p, tag)
                   for l, p in zip(("va", "es", "en"), parts))


text = MATH.sub(localise_math, text)
text = MARK.sub(expand, text)
text = text.replace("/*BASE_CSS*/", open(os.path.join(HERE, "base.css"), encoding="utf-8").read())
open(out, "w", encoding="utf-8").write(text + script)
print("ok", out, len(text + script))
