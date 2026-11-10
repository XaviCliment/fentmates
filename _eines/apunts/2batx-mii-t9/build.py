import os, re, sys, glob

# Genera materials/2batx-mii/t9-integrals.html. Ús: python3 _eines/apunts/2batx-mii-t9/build.py
# Unitat 9 de 2n Batx MII: integrals (primitives, immediates i quasi immediates —també trigonomètriques—, canvi de variable,
# integració per parts, funcions racionals, integral definida i regla de Barrow, teorema fonamental del càlcul i àrees).
# Segueix l'estructura de la unitat 8 de 2n Batx CCSS (integrals) i n'afegeix els mètodes de MII. El nucli (fraccions, lector
# d'expressions, límits, gràfiques) ve de _eines/apunts/2batx-mii-t5/app.js, amb les zones ombrejades entre corbes i els
# rectangles de Riemann de la unitat 8 de CCSS; la derivació simbòlica, de _eines/apunts/2batx-mii-t6/app.js, i els nombres
# exactes i les arrels numèriques, de _eines/apunts/2batx-mii-t7/app.js («nombres i rectes» fins a «figures estàtiques»).
# L'estil i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) són de materials/2batx-ccss/t3-programacio-lineal.html.
# No toqueu els fitxers d'altres unitats per a coses d'aquesta. El contingut és als contingut-*.html (en ordre alfabètic), el
# JavaScript propi a app.js i l'estil propi a extra.css (que s'afegeix després dels de la unitat 6 de MII i la 8 de CCSS).
# Als fragments, ⟪va‖es‖en⟫ s'expandeix en els tres <span data-l>. Dins d'una fórmula, \SI s'escriu
# «si» / «si» / «if»: si la fórmula no és dins d'un ⟪…⟫, es triplica sencera. Dins d'una fórmula que no és
# dins d'un ⟪…⟫, ⟦va‖es‖en⟧ tria el text de cada idioma (i la fórmula també es triplica).
HERE = os.path.dirname(os.path.abspath(__file__))
T5 = os.path.join(HERE, "..", "2batx-mii-t5")
T6 = os.path.join(HERE, "..", "2batx-mii-t6")
T7 = os.path.join(HERE, "..", "2batx-mii-t7")
C8 = os.path.join(HERE, "..", "2batx-ccss-t8")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/2batx-mii/t9-integrals.html")
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
    assert "⟪" not in t and "‖" not in t and "⟫" not in t, t[max(0, t.find("⟪") - 80):t.find("⟪") + 80]
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
V = "20261110m9"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Integrals · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 9 (Integrals: primitives, integrals immediates i quasi immediates, també trigonomètriques, canvi de variable, integració per parts, funcions racionals, integral definida, regla de Barrow, teorema fonamental del càlcul i àrees) de 2n de Batxillerat MII, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=" + V, head)
head += read("extra.css", T6) + "\n" + read("extra.css", C8) + "\n" + read("extra.css") + "\n" + re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=" + V, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand("".join(read(os.path.basename(f)) for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html")))))
n_sec = len(re.findall(r'<section class="unit" id="s\d+">', body))
assert n_sec == NSEC, n_sec

# ---------- JavaScript ----------
js = read("app.js")
core = cut("  /* ---------- fraccions exactes ---------- */", "  /* ---------- figures estàtiques ---------- */", read("app.js", T5))
for a, b in [('if (r && Math.abs(r.n) <= 40) return "e^{" + r.tex() + "}";', 'if (r && Math.abs(r.n) <= 40) return r.n === 1 && r.d === 1 ? "e" : "e^{" + r.tex() + "}";'),
             ('var NAMES = ["sqrt", "exp", "abs", "log", "sin", "cos", "tan", "ln", "pi", "x", "t", "a", "b", "e"];',
              'var NAMES = ["arcsin", "arccos", "arctan", "sqrt", "exp", "abs", "log", "sin", "cos", "tan", "ln", "pi", "x", "t", "a", "b", "e"];'),
             ("var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, tan: 1, ln: 1 };",
              "var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, tan: 1, arcsin: 1, arccos: 1, arctan: 1, ln: 1 };"),
             # (ln 0 no existeix: si no, x/ln(x) valdria 0 en x = 0 i el 0 entraria al domini)
             ("var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: Math.log10, ln: Math.log, sin: Math.sin, cos: Math.cos, tan: Math.tan };",
              "var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: function (v) { return v > 0 ? Math.log10(v) : NaN; }, ln: function (v) { return v > 0 ? Math.log(v) : NaN; }, sin: Math.sin, cos: Math.cos, tan: Math.tan, arcsin: Math.asin, arccos: Math.acos, arctan: Math.atan };"),
             # zones ombrejades (cfg.band: fora del domini...)
             ("    (cfg.ha || []).forEach(function (y) {",
              "    (cfg.band || []).forEach(function (q) { var a = Math.max(q.a, x0), b = Math.min(q.b, x1); if (b > a) body += '<rect class=\"' + (q.cls || \"nodom\") + '\" x=\"' + X(a) + '\" y=\"' + MT + '\" width=\"' + (X(b) - X(a)).toFixed(2) + '\" height=\"' + (H - MT - MB) + '\"/>'; });\n"
              "    (cfg.ha || []).forEach(function (y) {"),
             ("    (cfg.mark || []).forEach(function (q) {",
              "    (cfg.segs || []).forEach(function (S) { var d = \"\"; S.l.forEach(function (s) { d += \"M\" + X(s[0]) + \",\" + Y(s[1]) + \"L\" + X(s[2]) + \",\" + Y(s[3]); }); body += '<path class=\"cv\" d=\"' + d + '\" style=\"stroke:' + (S.col || COLS[0]) + (S.dash ? ';stroke-dasharray:6 5;stroke-width:1.8' : '') + '\"/>'; });\n"
              "    (cfg.mark || []).forEach(function (q) {"),
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
js = js.replace("  /*@@DERIV@@*/\n", cut("  /* ---------- derivació simbòlica ---------- */", "  /* ---------- figures estàtiques ---------- */", read("app.js", T6)))
a7 = read("app.js", T7)
study = cut("  /* ---------- nombres i rectes ---------- */", "  /* ---------- figures estàtiques ---------- */", a7)
# conjunt on g > 0 o g ≥ 0 (explicacions del domini): extrems ben inclosos o exclosos encara que g s'anul·le
a = "  function signSet(g, test) { return domTex(domainOf(function (x) { var v = g(x); return test(v) ? 1 : NaN; }, [])); }"
assert study.count(a) == 1
study = study.replace(a, "  function signSet(g, test) {\n"
    "    var D = domainOf(function (x) { var v = g(x); return isFinite(v) && test(v) ? 1 : NaN; }, []), ns = test(0);\n"
    "    D.iv.forEach(function (o) { if (!o.aInf && Math.abs(g(o.a)) < 1e-7) o.ai = ns; if (!o.bInf && Math.abs(g(o.b)) < 1e-7) o.bi = ns; });\n"
    "    return domTex(D);\n  }")
js = js.replace("  /*@@STUDY@@*/\n", study)
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
