import os, re, sys, glob, math

# Genera materials/1batx-ccss/t10-distribucions-probabilitat.html. Ús: python3 _eines/apunts/1batx-ccss-t10/build.py
# Unitat 10 de 1r Batx CCSS: distribucions de probabilitat (9 apartats). Parteix de la unitat 10 de 2n Batx CCSS
# (_eines/apunts/2batx-ccss-t10, copiada el 21/11/2026): 10.3-10.4 i 10.6-10.9 són els seus 10.2-10.3 i 10.5-10.8
# (binomial, taula de la binomial, normal, normal típica i taula, tipificació, aproximació de la binomial a la normal),
# sense la insistència en la PAU. Són nous 10.1 (variables aleatòries discretes i contínues, paral·lelisme amb
# l'estadística), 10.2 (funció de probabilitat, funció de distribució, mitjana i desviació típica, jocs justos; giny w-disc)
# i 10.5 (funció de densitat sense integrals: àrees de rectangles, triangles i trapezis, distribució uniforme; giny w-dens).
# Les taules de la binomial i de la normal N(0,1) són les de la PAU valenciana i es calculen ací, com a la unitat 10 de
# 2n Batx CCSS (marcadors <!--@@TAULA_BINOMIAL@@--> i <!--@@TAULA_NORMAL@@-->).
# Agafa l'estil comú i el JavaScript genèric de materials/2batx-ccss/t3-programacio-lineal.html i els extra.css de les
# unitats 4 i 9 de 2n Batx CCSS. Convencions: ⟪va‖es‖en⟫, ⟦va‖es‖en⟧ dins d'una fórmula, \SI, i «{,}» = coma decimal
# (en anglés es converteix en punt).
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/1batx-ccss/t10-distribucions-probabilitat.html")
T9 = os.path.join(HERE, "..", "2batx-ccss-t9")
NSEC = 9
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

# ---------- taules de la PAU ----------
PS = [("0,01", 0.01), ("0,05", 0.05), ("0,10", 0.10), ("0,15", 0.15), ("0,20", 0.20), ("0,25", 0.25), ("0,30", 0.30),
      ("1/3", 1 / 3), ("0,35", 0.35), ("0,40", 0.40), ("0,45", 0.45), ("0,49", 0.49), ("0,50", 0.50)]
def c4(v): return ("%.4f" % v).replace(".", ",")
def taula_binomial():
    # P[X = x] per a n = 2..9, com a la taula de la PAU
    h = ['<table class="data ptab" id="tbin"><thead><tr><th rowspan="2">n</th><th rowspan="2">x</th><th colspan="13">p</th></tr><tr>']
    h += ['<th data-j="%d">%s</th>' % (j, l) for j, (l, _) in enumerate(PS)] + ['</tr></thead>']
    for n in range(2, 10):
        h.append('<tbody>')
        for x in range(n + 1):
            h.append('<tr data-n="%d" data-x="%d">' % (n, x) + ('<th rowspan="%d" class="tn">%d</th>' % (n + 1, n) if x == 0 else '') + '<th class="tx">%d</th>' % x)
            h += ['<td data-j="%d">%s</td>' % (j, c4(math.comb(n, x) * p ** x * (1 - p) ** (n - x))) for j, (_, p) in enumerate(PS)]
            h.append('</tr>')
        h.append('</tbody>')
    return "".join(h) + "</table>"
def Phi(z): return 0.5 * (1 + math.erf(z / math.sqrt(2)))
def taula_normal():
    # F(z) = P(Z <= z) per a z = 0,00..3,99
    h = ['<table class="data ptab" id="tnorm"><thead><tr><th>z</th>'] + ['<th data-c="%d">0,0%d</th>' % (c, c) for c in range(10)] + ['</tr></thead><tbody>']
    for r in range(40):
        h.append('<tr data-r="%d"><th>%s</th>' % (r, ("%.1f" % (r / 10)).replace(".", ",")) + "".join('<td data-c="%d">%s</td>' % (c, c4(Phi(r / 10 + c / 100))) for c in range(10)) + "</tr>")
    return "".join(h) + "</tbody></table>"
# comprovacions amb valors de les taules oficials (PAU juliol 2026)
assert c4(math.comb(2, 1) * .49 * .51) == "0,4998" and c4(math.comb(9, 4) * (1 / 3) ** 4 * (2 / 3) ** 5) == "0,2048"
assert c4(Phi(0.05)) == "0,5199" and c4(Phi(1.96)) == "0,9750" and c4(Phi(2.33)) == "0,9901"

src = open(SRC, encoding="utf-8").read()
def cut(a, b, s=src):
    i = s.index(a); j = s.index(b, i)
    return s[i:j]

# ---------- capçalera i estil ----------
# fm-materials.js sap que la unitat 10 de 1r Batx CCSS és de probabilitat (bloc «pr») des del 21/11/2026: la versió força a recarregar-lo
VER = r"fm-materials.\1?v=20261121c10"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Distribucions de probabilitat · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 10 (Distribucions de probabilitat: variables aleatòries discretes i contínues, funció de probabilitat i de distribució, mitjana i desviació típica, distribució binomial i la seua taula, funció de densitat i distribució uniforme, distribució normal, normal típica i la seua taula, tipificació i aproximació de la binomial a la normal) de 1r de Batxillerat de Matemàtiques Aplicades a les CCSS, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, head)
head += read("extra.css", T4) + "\n" + read("extra.css", T9) + "\n" + read("extra.css") + "\n" + \
    re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
raw = "".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html"))))
NW = len(re.findall(r'id="w-[a-z]+"', raw))
body = expand(raw.replace("@@NW@@", str(NW)))
body = body.replace("<!--@@TAULA_BINOMIAL@@-->", taula_binomial()).replace("<!--@@TAULA_NORMAL@@-->", taula_normal())
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
