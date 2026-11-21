import os, re, sys, glob

# Genera materials/1batx-ccss/t9-combinatoria-probabilitat.html. Ús: python3 _eines/apunts/1batx-ccss-t9/build.py
# Unitat 9 de 1r Batx CCSS: combinatòria i probabilitat (14 apartats). Els apartats 9.1-9.4 (tècniques de recompte i
# combinatòria) parteixen dels 9.1-9.3 de 4t ESO B (_eines/apunts/4eso-b-t9, copiats el 21/11/2026) i hi afigen el principi
# de la suma, les permutacions amb repetició i circulars, les propietats dels nombres combinatoris (Stifel, triangle de
# Tartaglia, suma d'una fila) i el binomi de Newton. Els apartats 9.5-9.14 són els 10.1-10.10 de 2n Batx MII
# (_eines/apunts/2batx-mii-t10, terminologia «succés»), sense les variables aleatòries ni la binomial, amb 9.8 (Laplace)
# fent servir la combinatòria de 9.1-9.4, i 9.12-9.13 com a «successos dependents i independents» i «experiències
# compostes» (amb el quadre d'experiències independents i dependents).
# app.js és el de MII sense wBin ni wNmin, amb els ginys de recompte de 4t ESO B (w-comb, w-mult, w-llista, w-tipus;
# w-tipus amb permutacions amb repetició). Com aquelles, agafa l'estil comú i el JavaScript genèric de
# materials/2batx-ccss/t3-programacio-lineal.html i l'extra.css de la unitat 4 de CCSS.
# Convencions: ⟪va‖es‖en⟫, ⟦va‖es‖en⟧ dins d'una fórmula, \SI, i «{,}» = coma decimal (en anglés es converteix en punt).
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/1batx-ccss/t9-combinatoria-probabilitat.html")
NSEC = 14
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
# fm-materials.js sap que la unitat 9 de 1r Batx CCSS és de probabilitat (bloc «pr») des del 21/11/2026: la versió força a recarregar-lo
VER = r"fm-materials.\1?v=20261121c9"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Combinatòria i probabilitat · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 9 (Combinatòria i probabilitat: tècniques de recompte, variacions, permutacions i combinacions, nombres combinatoris, experiments aleatoris i successos, regla de Laplace, propietats de la probabilitat, probabilitat condicionada, successos dependents i independents, experiències compostes, probabilitat total i teorema de Bayes) de 1r de Batxillerat de Matemàtiques Aplicades a les CCSS, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, head)
head += read("extra.css", T4) + "\n" + read("extra.css") + "\n" + \
    re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
raw = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html"))))
NW = len(re.findall(r'class="widget"|id="w-lab"', raw))
body = expand(raw.replace("@@NW@@", str(NW)))
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
