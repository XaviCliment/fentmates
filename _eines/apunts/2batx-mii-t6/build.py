import os, re, sys, glob

# Genera materials/2batx-mii/t6-derivades.html. Ús: python3 _eines/apunts/2batx-mii-t6/build.py
# Parteix de la unitat 5 de 2n Batx CCSS (app.js i extra.css copiats i ampliats aquí: més dificultat, recta normal,
# derivades successives, derivació logarítmica, derivació implícita i funcions a trossos amb trossos de tota mena).
# No toqueu els fitxers de CCSS per a coses de MII.
# Agafa l'estil comú i el JavaScript genèric (passos, índex, qüestionari, idioma i tema) de
# materials/2batx-ccss/t3-programacio-lineal.html i el nucli (fraccions, lector d'expressions, límits numèrics,
# gràfiques i funcions a trossos) de _eines/apunts/2batx-mii-t5/app.js. El contingut és als contingut-*.html (en ordre
# alfabètic), el JavaScript propi a app.js i l'estil propi a extra.css.
# Als fragments, ⟪va‖es‖en⟫ s'expandeix en els tres <span data-l>. Dins d'una fórmula, \SI s'escriu
# «si» / «si» / «if»: si la fórmula no és dins d'un ⟪…⟫, es triplica sencera. Dins d'una fórmula que no és
# dins d'un ⟪…⟫, ⟦va‖es‖en⟧ tria el text de cada idioma (i la fórmula també es triplica).
HERE = os.path.dirname(os.path.abspath(__file__))
T5 = os.path.join(HERE, "..", "2batx-mii-t5")
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/t3-programacio-lineal.html")
OUT = os.path.join(SITE, "materials/2batx-mii/t6-derivades.html")
NSEC = 11

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
V = "20261109m6"
head = cut("<!doctype html>", "/* unitat 3: programació lineal */")
head = head.replace("<title>Programació lineal · FentMates</title>", "<title>Càlcul de derivades · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              '<meta name="description" content="Apunts interactius de la Unitat 6 (Càlcul de derivades. Derivabilitat d\'una funció: definició, regles, regla de la cadena, derivació logarítmica, derivació implícita i derivabilitat de funcions a trossos) de 2n de Batxillerat MII, en valencià, castellà i anglés.">', head)
head = re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=" + V, head)
head += read("extra.css") + "\n" + re.sub(r"fm-materials\.(css|js)\?v=\w+", r"fm-materials.\1?v=" + V, cut("/* FentMates: 80% de l'ample", "</head>")) + "</head>\n"

# ---------- cos ----------
body = expand("".join(read(os.path.basename(f)) for f in sorted(glob.glob(os.path.join(HERE, "contingut-*.html")))))
n_sec = len(re.findall(r'<section class="unit" id="s\d+">', body))
assert n_sec == NSEC, n_sec

# ---------- JavaScript ----------
js = read("app.js")
core = cut("  /* ---------- fraccions exactes ---------- */", "  /* ---------- figures estàtiques ---------- */", read("app.js", T5))
# el lector d'expressions de la unitat 5 no coneix arcsin, arccos, arctan ni la variable y (derivació implícita)
for a, b in [('var NAMES = ["sqrt", "exp", "abs", "log", "sin", "cos", "tan", "ln", "pi", "x", "t", "a", "b", "e"];',
              'var NAMES = ["arcsin", "arccos", "arctan", "sqrt", "exp", "abs", "log", "sin", "cos", "tan", "ln", "pi", "x", "y", "t", "a", "b", "e"];'),
             ("var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, tan: 1, ln: 1 };",
              "var FUNCS = { sqrt: 1, exp: 1, abs: 1, log: 1, sin: 1, cos: 1, tan: 1, arcsin: 1, arccos: 1, arctan: 1, ln: 1 };"),
             ("var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: Math.log10, ln: Math.log, sin: Math.sin, cos: Math.cos, tan: Math.tan };",
              "var FN = { sqrt: Math.sqrt, exp: Math.exp, abs: Math.abs, log: Math.log10, ln: Math.log, sin: Math.sin, cos: Math.cos, tan: Math.tan, arcsin: Math.asin, arccos: Math.acos, arctan: Math.atan };"),
             # corbes implícites: conjunts de segments (cfg.segs = [{l: [[x1, y1, x2, y2], ...], col}])
             ("    (cfg.mark || []).forEach(function (q) {",
              "    (cfg.segs || []).forEach(function (S) { var d = \"\"; S.l.forEach(function (s) { d += \"M\" + X(s[0]) + \",\" + Y(s[1]) + \"L\" + X(s[2]) + \",\" + Y(s[3]); }); body += '<path class=\"cv\" d=\"' + d + '\" style=\"stroke:' + (S.col || COLS[0]) + '\"/>'; });\n    (cfg.mark || []).forEach(function (q) {")]:
    assert a in core, a
    core = core.replace(a, b)
js = js.replace("  /*@@CORE@@*/\n", core)
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
