import os, re, sys, glob

# Genera materials/4eso-b/t9-recompte-probabilitat.html. Ús: python3 _eines/apunts/4eso-b-t9/build.py
# Unitat 9 de 4t ESO B: tècniques de recompte i probabilitat. Segueix els apunts del departament («Probabilitat. 4t ESO ·
# Matemàtiques B», 8 apartats) i hi afig al principi les tècniques de recompte (9.1 principi de multiplicació i diagrames
# d'arbre, 9.2 variacions i permutacions, 9.3 combinacions) i, al final, els problemes amb arbres de dues etapes (9.10:
# probabilitat total i probabilitat «a posteriori»), que són a la col·lecció d'exercicis del departament.
# Parteix d'una CÒPIA d'app.js i extra.css de la unitat 10 de 2n Batx MII (que no es toquen) sense la binomial ni el giny
# d'independència, amb la terminologia del departament (esdeveniment, passa) i amb tres ginys nous de recompte
# (w-mult, w-llista, w-tipus). Com aquella, agafa l'estil comú i el JavaScript genèric de
# materials/2batx-ccss/t3-programacio-lineal.html i l'extra.css de la unitat 4 de CCSS.
# Convencions de text com a la unitat 8 de 4t: ⟪va‖es‖en⟫, ⟦va‖es‖en⟧ dins d'una fórmula, \SI, i «{,}» = coma decimal
# (en anglés es converteix en punt).
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/4eso-b/t9-recompte-probabilitat.html")
NSEC = 10
LANGS = ("va", "es", "en")

def read(name, d=HERE): return open(os.path.join(d, name), encoding="utf-8").read()
def L(va, es, en): return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
SI = {"va": r"\text{si }", "es": r"\text{si }", "en": r"\text{if }"}
FORM = re.compile(r"\\\[.*?\\\]|\\\(.*?\\\)", re.S)

def variant(f, i):
    """versió de la fórmula f en l'idioma i: ⟦va‖es‖en⟧, \\SI i la coma decimal {,}"""
    k = LANGS[i]
    f = re.sub(r"⟦(.*?)⟧", lambda n: n.group(1).split("‖")[i], f, flags=re.S).replace(r"\SI", SI[k])
    return f.replace("{,}", ".") if k == "en" else f

def expand(t):
    # 1) els blocs de text ⟪va‖es‖en⟫ es guarden a part
    blocks = []
    def keep(m):
        p = m.group(1).split("‖")
        assert len(p) == 3, m.group(0)[:160]
        assert "⟦" not in m.group(1), m.group(0)[:160]
        blocks.append(p)
        return "\x00%d\x00" % (len(blocks) - 1)
    t = re.sub(r"⟪(.*?)⟫", keep, t, flags=re.S)
    assert "⟪" not in t and "⟫" not in t, t[t.find("⟪") - 80:t.find("⟪") + 80]
    # 2) fórmules fora dels blocs: si canvien amb l'idioma, se'n fan tres versions
    def form(m):
        f = m.group(0); vs = [variant(f, i) for i in range(3)]
        return f if vs[0] == vs[1] == vs[2] else L(*vs)
    t = FORM.sub(form, t)
    assert "⟦" not in t and "‖" not in t and r"\SI" not in t
    # 3) es tornen a posar els blocs, amb les fórmules de cada idioma adaptades
    def put(m):
        p = blocks[int(m.group(1))]
        return L(*[FORM.sub(lambda n: variant(n.group(0), i), x) for i, x in enumerate(p)])
    t = re.sub(r"\x00(\d+)\x00", put, t)
    assert "‖" not in t and "\x00" not in t
    return t

src = open(SRC, encoding="utf-8").read()
def cut(a, b, s=src):
    i = s.index(a); j = s.index(b, i)
    return s[i:j]

# ---------- capçalera i estil ----------
# fm-materials.js assigna la unitat 9 de 4t ESO B al bloc de probabilitat ("pr") des del 15/11/2026: la versió força a recarregar-lo
VER = r"fm-materials.\1?v=20261115p9"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Recompte i probabilitat · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 9 (Tècniques de recompte i probabilitat: principi de multiplicació, variacions, permutacions i combinacions, experiments aleatoris, esdeveniments, regla de Laplace, propietats de la probabilitat, experiments compostos, taules de contingència, probabilitat condicionada i probabilitat total) de 4t d\'ESO Matemàtiques B, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, head)
head += read("extra.css", T4) + "\n" + read("extra.css") + "\n" + \
    re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand("".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html")))))
assert "@@" not in body
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
