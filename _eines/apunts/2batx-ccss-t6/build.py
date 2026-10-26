import os, re, sys

# Genera materials/2batx-ccss/t6-aplicacions-derivada.html. Ús: python3 _eines/apunts/2batx-ccss-t6/build.py
# Com les unitats 4 i 5, agafa l'estil comú i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) de
# materials/2batx-ccss/t3-programacio-lineal.html. Reaprofita el nucli de _eines/apunts/2batx-ccss-t4/app.js
# (fraccions, lector d'expressions, límits numèrics i gràfiques) i la derivació simbòlica de
# _eines/apunts/2batx-ccss-t5/app.js (de «derivació simbòlica» fins a «figures estàtiques»), amb els extra.css
# de totes dues. El contingut és a contingut.html, el JavaScript propi a app.js i l'estil propi a extra.css.
# Les convencions ⟪va‖es‖en⟫, ⟦va‖es‖en⟧ i \SI són les mateixes que a la unitat 4.
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
T5 = os.path.join(HERE, "..", "2batx-ccss-t5")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/2batx-ccss/t6-aplicacions-derivada.html")
NSEC = 7

def read(name, d=HERE): return open(os.path.join(d, name), encoding="utf-8").read()
def L(va, es, en): return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
SI = {"va": r"\text{si }", "es": r"\text{si }", "en": r"\text{if }"}

def expand(t):
    def form(m):
        f = m.group(0)
        if "⟦" not in f: return f
        out = []
        for i, k in enumerate(("va", "es", "en")):
            out.append(re.sub(r"⟦(.*?)⟧", lambda n: n.group(1).split("‖")[i], f).replace(r"\SI", SI[k]))
        return L(*out)
    t = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", form, t, flags=re.S)
    assert "⟦" not in t
    def one(m):
        p = m.group(1).split("‖")
        assert len(p) == 3, m.group(0)[:120]
        return L(*[x.replace(r"\SI", SI[k]) for x, k in zip(p, ("va", "es", "en"))])
    t = re.sub(r"⟪(.*?)⟫", one, t, flags=re.S)
    assert "⟪" not in t and "‖" not in t and "⟫" not in t, t[t.find("⟪") - 80:t.find("⟪") + 80]
    def tri(m):
        f = m.group(0)
        return L(*[f.replace(r"\SI", SI[k]) for k in ("va", "es", "en")]) if r"\SI" in f else f
    t = re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)", tri, t, flags=re.S)
    assert r"\SI" not in t
    return t

src = open(SRC, encoding="utf-8").read()
def cut(a, b, s=src):
    i = s.index(a); j = s.index(b, i)
    return s[i:j]

# ---------- capçalera i estil ----------
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Aplicacions de la derivada · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 6 (Aplicacions de la derivada) de 2n de Batxillerat CCSS, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=20261024u4", head)
head += read("extra.css", T4) + "\n" + read("extra.css", T5) + "\n" + read("extra.css") + "\n" + \
    re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=20261024u4", cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand(read("contingut.html"))
n_sec = len(re.findall(r'<section class="unit" id="s\d+">', body))
assert n_sec == NSEC, n_sec

# ---------- JavaScript ----------
js = read("app.js")
core = cut("  /* ---------- fraccions exactes ---------- */", "  /* ---------- figures estàtiques ---------- */", read("app.js", T4))
# el lector d'expressions de la unitat 4 no coneix tan, arcsin, arccos ni arctan (igual que a la unitat 5)
for a, b in [('var NAMES = ["sqrt", "exp", "abs", "log", "sin", "cos", "ln", "pi", "x", "t", "a", "b", "e"];',
              'var NAMES = ["arcsin", "arccos", "arctan", "sqrt", "exp", "abs", "log", "sin", "cos", "tan", "ln", "pi", "x", "t", "a", "b", "e"];'),
             ("var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, ln: 1 };",
              "var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, tan: 1, arcsin: 1, arccos: 1, arctan: 1, ln: 1 };"),
             ("var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: Math.log10, ln: Math.log, sin: Math.sin, cos: Math.cos };",
              "var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: Math.log10, ln: Math.log, sin: Math.sin, cos: Math.cos, tan: Math.tan, arcsin: Math.asin, arccos: Math.acos, arctan: Math.atan };")]:
    assert a in core, a
    core = core.replace(a, b)
js = js.replace("  /*@@CORE@@*/\n", core)
deriv = cut("  /* ---------- derivació simbòlica ---------- */", "  /* ---------- figures estàtiques ---------- */", read("app.js", T5))
js = js.replace("  /*@@DERIV@@*/\n", deriv)
generic = cut("  var answers = {};", "  var TITLES")
generic = generic.replace("(n / 5 * 100)", f"(n / {NSEC} * 100)")
assert f"(n / {NSEC} * 100)" in generic
js = js.replace("  /*@@GENERIC@@*/\n", generic)
assert "@@" not in js

page = head + body + '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>\n' \
    '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>\n<script>\n' + js + "</script>\n</body>\n</html>\n"
open(OUT, "w", encoding="utf-8").write(page)
print(OUT, len(page), "bytes")
