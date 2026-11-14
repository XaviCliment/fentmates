import os, re, sys, glob

# Genera materials/4eso-b/t5-trigonometria.html. Ús: python3 _eines/apunts/4eso-b-t5/build.py
# Parteix dels apartats 5.1-5.5 de la unitat 5 de 1r Batx MI (1batx-mi-t5), simplificats i reordenats en 8 apartats seguint les
# fitxes del departament de 4t ESO: graus i radians, raons d'un angle agut, raons de 30°, 45° i 60°, relacions fonamentals,
# triangles rectangles, problemes (doble observació, polígons, triangles qualssevol traçant una altura), angles qualssevol i
# reducció al primer quadrant. Sense teoremes del sinus i del cosinus ni raons recíproques. Com aquella, agafa l'estil comú i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) de
# materials/2batx-ccss/t3-programacio-lineal.html, i els extra.css de les unitats 4 i 9 de 2n Batx CCSS (controls dels ginys,
# taules, botons). Els ginys (radians, triangle rectangle, circumferència goniomètrica, raons a partir d'una, reducció al primer
# quadrant, resolució de triangles, laboratori del triangle, fórmules de la suma, identitats, equacions i funcions) són a app.js i
# l'estil propi a extra.css (còpia del de 1r Batx MI). Ginys nous: existeix un angle amb dues raons donades? (w-chk) i doble
# observació (w-dob). El contingut és a contingut-*.html (en ordre).
# Convencions: ⟪va‖es‖en⟫ per al text, ⟦va‖es‖en⟧ dins d'una fórmula i \SI com a la unitat 4. A més, dins de les fórmules
# «{,}» és la coma decimal: en anglés es converteix en un punt (0{,}86 → 0.86).
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
T9 = os.path.join(HERE, "..", "2batx-ccss-t9")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/4eso-b/t5-trigonometria.html")
NSEC = 8
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
# fm-materials.js sap que la unitat 5 de 4t ESO B és de geometria des del 14/11/2026: la versió força a recarregar-lo
VER = r"fm-materials.\1?v=20261114t5b"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Trigonometria · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 5 (Trigonometria: graus i radians, raons trigonomètriques d\'un angle agut, raons de 30°, 45° i 60°, relacions fonamentals, resolució de triangles rectangles, problemes, circumferència goniomètrica i reducció al primer quadrant) de 4t d\'ESO Matemàtiques B, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, head)
head += read("extra.css", T4) + "\n" + read("extra.css", T9) + "\n" + read("extra.css") + "\n" + \
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
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print(OUT, len(page), "bytes")
