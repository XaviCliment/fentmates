import os, re, sys, glob

# Genera materials/2batx-ccss/t9-probabilitat.html. Ús: python3 _eines/apunts/2batx-ccss-t9/build.py
# Com les unitats 4-8, agafa l'estil comú i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) de
# materials/2batx-ccss/t3-programacio-lineal.html, i l'extra.css de la unitat 4 (controls dels ginys, taules).
# No necessita el nucli de gràfiques de la unitat 4: els diagrames (Venn, arbres, quadrat unitat, daus) es
# dibuixen amb app.js. El contingut és a contingut-*.html (en ordre), el JavaScript propi a app.js i l'estil propi a extra.css.
# Les convencions ⟪va‖es‖en⟫, ⟦va‖es‖en⟧ i \SI són les mateixes que a la unitat 4.
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/2batx-ccss/t9-probabilitat.html")
NSEC = 10

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
        assert len(p) == 3, m.group(0)[:160]
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
# fm-materials.js sap que la unitat 9 és de probabilitat des del 27/10/2026: la versió força a recarregar-lo
VER = r"fm-materials.\1?v=20261027u9"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Probabilitat · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 9 (Probabilitat) de 2n de Batxillerat CCSS, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, head)
head += read("extra.css", T4) + "\n" + read("extra.css") + "\n" + \
    re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand("".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html")))))
n_sec = len(re.findall(r'<section class="unit" id="s\d+">', body))
assert n_sec == NSEC, n_sec

# ---------- JavaScript ----------
js = read("app.js")
generic = cut("  var answers = {};", "  var TITLES")
generic = generic.replace("(n / 5 * 100)", f"(n / {NSEC} * 100)")
assert f"(n / {NSEC} * 100)" in generic
js = js.replace("  /*@@GENERIC@@*/\n", generic)
assert "@@" not in js

page = head + body + '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>\n' \
    '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>\n<script>\n' + js + "</script>\n</body>\n</html>\n"
open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print(OUT, len(page), "bytes")
