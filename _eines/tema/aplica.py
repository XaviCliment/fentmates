#!/usr/bin/env python3
"""Enllaça el tema comú (assets/css/fm-materials.css + assets/js/fm-materials.js)
a totes les pàgines de materials/. És idempotent: es pot executar sempre que es
regenere qualsevol material. Els generadors (apunts, calculadora, PAU, exàmens)
ja la criden en acabar.
Ús (des de l'arrel del web):  python3 _eines/tema/aplica.py
"""
import glob
import os
import re

VERSION = "20261024b"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TAG = ('<link rel="stylesheet" href="../../assets/css/fm-materials.css?v={v}">'
       '<script defer src="../../assets/js/fm-materials.js?v={v}"></script>')


def aplica_fitxer(path):
    s = open(path, encoding="utf-8").read()
    if "fm-materials.css" in s:
        s2 = re.sub(r"(fm-materials\.(?:css|js))\?v=[0-9a-z]+", r"\1?v=" + VERSION, s)
    else:
        s2 = s.replace("</head>", TAG.format(v=VERSION) + "\n</head>", 1)
    if s2 != s:
        open(path, "w", encoding="utf-8").write(s2)
        return True
    return False


def main():
    n = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "materials", "*", "*.html"))):
        n += aplica_fitxer(f)
    print("tema aplicat a", n, "pàgines")


if __name__ == "__main__":
    main()
