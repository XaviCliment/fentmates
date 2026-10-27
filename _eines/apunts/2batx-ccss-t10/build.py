import os, re, sys, glob, math

# Genera materials/2batx-ccss/t10-binomial-normal.html. Ús: python3 _eines/apunts/2batx-ccss-t10/build.py
# Com les unitats 4-8, agafa l'estil comú i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) de
# materials/2batx-ccss/t3-programacio-lineal.html, i els extra.css de les unitats 4 i 9 (controls dels ginys, taules).
# Les taules de la binomial i de la normal N(0,1) són les que s'adjunten a l'examen de la PAU valenciana (des del curs
# 2025-26): es calculen ací (quatre decimals) i se substitueixen als marcadors <!--@@TAULA_BINOMIAL@@--> i <!--@@TAULA_NORMAL@@-->. El contingut és a contingut-*.html (en ordre), el JavaScript propi a app.js i l'estil propi a extra.css.
# Les convencions ⟪va‖es‖en⟫, ⟦va‖es‖en⟧ i \SI són les mateixes que a la unitat 4.
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/2batx-ccss/t10-binomial-normal.html")
T9 = os.path.join(HERE, "..", "2batx-ccss-t9")
NSEC = 8

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
# fm-materials.js sap que la unitat 10 és de probabilitat des del 27/10/2026: la versió força a recarregar-lo
VER = r"fm-materials.\1?v=20261027u10"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Distribució binomial i normal · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 10 (Distribució binomial i normal) de 2n de Batxillerat CCSS, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, head)
head += read("extra.css", T4) + "\n" + read("extra.css", T9) + "\n" + read("extra.css") + "\n" + \
    re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand("".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html")))))
body = body.replace("<!--@@TAULA_BINOMIAL@@-->", taula_binomial()).replace("<!--@@TAULA_NORMAL@@-->", taula_normal())
assert "@@TAULA" not in body
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
