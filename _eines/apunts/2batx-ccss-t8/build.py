import os, re, sys

# Genera materials/2batx-ccss/t8-integrals.html. Ús: python3 _eines/apunts/2batx-ccss-t8/build.py
# Com les unitats 4-7, agafa l'estil comú i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) de
# materials/2batx-ccss/t3-programacio-lineal.html. Reaprofita el nucli de _eines/apunts/2batx-ccss-t4/app.js
# (fraccions, polinomis amb coeficients fraccionaris, lector d'expressions i gràfiques), amb l'extra.css de la unitat 4.
# Al nucli de les gràfiques li afegim regions ombrejades (cfg.fill) i rectangles (cfg.rects) per a les àrees.
# El contingut és a contingut.html, el JavaScript propi a app.js i l'estil propi a extra.css.
# Les convencions ⟪va‖es‖en⟫, ⟦va‖es‖en⟧ i \SI són les mateixes que a la unitat 4.
HERE = os.path.dirname(os.path.abspath(__file__))
T4 = os.path.join(HERE, "..", "2batx-ccss-t4")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/2batx-ccss/t8-integrals.html")
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
# fm-materials.js sap que la unitat 8 és d'anàlisi des del 27/10/2026: la versió força a recarregar-lo
VER = r"fm-materials.\1?v=20261027u8"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Integrals · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 8 (Integrals) de 2n de Batxillerat CCSS, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, head)
head += read("extra.css", T4) + "\n" + read("extra.css") + "\n" + \
    re.sub(r"fm-materials\.(css|js)\?v=\w+", VER, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand(read("contingut.html"))
n_sec = len(re.findall(r'<section class="unit" id="s\d+">', body))
assert n_sec == NSEC, n_sec

# ---------- JavaScript ----------
js = read("app.js")
core = cut("  /* ---------- fraccions exactes ---------- */", "  /* ---------- figures estàtiques ---------- */", read("app.js", T4))
for a, b in [("var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: Math.log10, ln: Math.log, sin: Math.sin, cos: Math.cos };",
              "var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: function (v) { return v > 0 ? Math.log10(v) : NaN; }, ln: function (v) { return v > 0 ? Math.log(v) : NaN; }, sin: Math.sin, cos: Math.cos };"),
             # regions ombrejades entre f i g (o l'eix OX) i rectangles de les sumes de Riemann
             ("    (cfg.ha || []).forEach(function (y) {",
              "    var yc = function (y) { return Y(Math.max(y0 - (y1 - y0), Math.min(y1 + (y1 - y0), y))); };\n"
              "    (cfg.fill || []).forEach(function (q) {\n"
              "      var a = Math.max(q.a, x0), b = Math.min(q.b, x1); if (!(b > a)) return;\n"
              "      var N = 160, top = [], bot = [];\n"
              "      for (var i = 0; i <= N; i++) { var x = a + (b - a) * i / N, yf = q.f(x), yg = q.g ? q.g(x) : 0; if (!isFinite(yf) || !isFinite(yg)) continue; top.push(X(x) + \",\" + yc(yf)); bot.unshift(X(x) + \",\" + yc(yg)); }\n"
              "      if (top.length > 1) body += '<polygon class=\"fl\" points=\"' + top.concat(bot).join(\" \") + '\" style=\"fill:' + (q.col || \"var(--accent)\") + '\"/>';\n"
              "    });\n"
              "    (cfg.rects || []).forEach(function (q) {\n"
              "      if (!isFinite(q.y) || q.b < x0 || q.a > x1) return;\n"
              "      var ya = yc(q.y), yb = yc(0);\n"
              "      body += '<rect class=\"rc\" x=\"' + X(q.a) + '\" y=\"' + Math.min(ya, yb) + '\" width=\"' + (X(q.b) - X(q.a)).toFixed(2) + '\" height=\"' + Math.abs(yb - ya).toFixed(2) + '\" style=\"fill:' + (q.col || \"var(--accent-2)\") + ';stroke:' + (q.col || \"var(--accent-2)\") + '\"/>';\n"
              "    });\n"
              "    (cfg.ha || []).forEach(function (y) {")]:
    assert core.count(a) == 1, a
    core = core.replace(a, b)
js = js.replace("  /*@@CORE@@*/\n", core)
generic = cut("  var answers = {};", "  var TITLES")
generic = generic.replace("(n / 5 * 100)", f"(n / {NSEC} * 100)")
assert f"(n / {NSEC} * 100)" in generic
js = js.replace("  /*@@GENERIC@@*/\n", generic)
assert "@@" not in js

page = head + body + '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>\n' \
    '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>\n<script>\n' + js + "</script>\n</body>\n</html>\n"
open(OUT, "w", encoding="utf-8", newline="\n").write(page)
print(OUT, len(page), "bytes")
