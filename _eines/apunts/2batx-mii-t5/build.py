import os, re, sys, glob

# Genera materials/2batx-mii/t5-limits-continuitat.html. Ús: python3 _eines/apunts/2batx-mii-t5/build.py
# Parteix de la unitat 4 de 2n Batx CCSS (contingut.html, app.js i extra.css copiats i ampliats aquí: més dificultat,
# límits amb paràmetres, límits trigonomètrics, funcions a trossos amb trossos de tota mena i teorema de Bolzano).
# No toqueu els fitxers de CCSS per a coses de MII.
# Agafa l'estil comú i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) de
# materials/2batx-ccss/t3-programacio-lineal.html. El contingut és a contingut.html, el JavaScript propi
# a app.js i l'estil propi a extra.css.
# Als fragments, ⟪va‖es‖en⟫ s'expandeix en els tres <span data-l>. Dins d'una fórmula, \SI s'escriu
# «si» / «si» / «if»: si la fórmula no és dins d'un ⟪…⟫, es triplica sencera. Dins d'una fórmula que no és
# dins d'un ⟪…⟫, ⟦va‖es‖en⟧ tria el text de cada idioma (i la fórmula també es triplica).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/2batx-mii/t5-limits-continuitat.html")
NSEC = 13

def read(name): return open(os.path.join(HERE, name), encoding="utf-8").read()
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
    assert "⟪" not in t and "‖" not in t and "⟫" not in t
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
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Límits i continuïtat · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 5 (Límits i continuïtat: indeterminacions, límits trigonomètrics, paràmetres, funcions a trossos, teorema de Bolzano i asímptotes) de 2n de Batxillerat MII, en valencià, castellà i anglés.">', head)
# fm-materials.js sap que les unitats 5-8 de MII són d'anàlisi des del 08/11/2026: la versió força a recarregar-lo
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=20261108m5", head)
head += read("extra.css") + "\n" + re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=20261108m5", cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand("".join(read(os.path.basename(f)) for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html")))))
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
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print(OUT, len(page), "bytes")
