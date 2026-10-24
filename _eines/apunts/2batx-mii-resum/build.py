import os, re, sys

# Genera materials/2batx-mii/resum-teoric.html. Ús: python3 _eines/apunts/2batx-mii-resum/build.py
# Parteix del resum de CCSS (materials/2batx-ccss/resum-teoric.html): els blocs d'àlgebra, anàlisi i probabilitat
# són els mateixos. Lleva la programació lineal, hi posa el bloc de geometria (geometria.html), els afegits
# d'anàlisi que només té MII (analisi.html), el JavaScript nou (extra.js) i l'estil propi (extra.css).
# Als fragments, ⟪va‖es‖en⟫ s'expandeix en els tres <span data-l>. Dins d'una fórmula no hi pot haver ⟪…⟫:
# cal triplicar la fórmula sencera (⟪\[…\]‖\[…\]‖\[…\]⟫).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/2batx-ccss/resum-teoric.html")
OUT = os.path.join(SITE, "materials/2batx-mii/resum-teoric.html")

def read(name): return open(os.path.join(HERE, name), encoding="utf-8").read()
def L(va, es, en): return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'

def expand(t):
    def one(m):
        p = m.group(1).split("‖")
        assert len(p) == 3, m.group(0)[:80]
        return L(*p)
    t = re.sub(r"⟪(.*?)⟫", one, t, flags=re.S)
    assert "⟪" not in t and "‖" not in t and "⟫" not in t
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", t, flags=re.S):
        assert "data-l" not in m.group(0), "idioma dins d'una fórmula: " + m.group(0)[:100]
    return t

def frags(t):
    parts = re.split(r"<!-- @@(\w+)[^>]*-->\n", t)
    return {parts[i]: expand(parts[i + 1]) for i in range(1, len(parts), 2)}

s = open(SRC, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, f"{c}× (esperava {n}): {a[:90]}"
    s = s.replace(a, b)

# ---------- capçalera i textos generals ----------
rep('content="Formulari-resum teòric interactiu de Matemàtiques Aplicades a les CCSS II (2n Batxillerat): àlgebra, programació lineal, anàlisi i probabilitat. En valencià, castellà i anglés."',
    'content="Formulari-resum teòric interactiu de Matemàtiques II (2n Batxillerat): àlgebra, geometria, anàlisi i probabilitat. En valencià, castellà i anglés."')
rep('href="../../2batx-ccss.html">' + L("2n Batxillerat CCSS", "2º Bachillerato CCSS", "2nd Baccalaureate (Social Sciences)"),
    'href="../../2batx-mii.html">' + L("2n Batxillerat MII", "2º Bachillerato MII", "2nd Baccalaureate Maths II"))
rep(L("Formulari-resum teòric · Matemàtiques Aplicades a les CCSS II", "Formulario-resumen teórico · Matemáticas Aplicadas a las CCSS II", "Theory summary &amp; formula sheet · Applied Mathematics for Social Sciences II"),
    L("Formulari-resum teòric · Matemàtiques II", "Formulario-resumen teórico · Matemáticas II", "Theory summary &amp; formula sheet · Mathematics II"))
rep("· 2n BAT CCSS</h1>", "· 2n BAT MII</h1>")
rep('<a href="#bloc-pl"><i style="background:var(--pl)">II</i>' + L("Programació lineal", "Programación lineal", "Linear programming") + "</a>",
    '<a href="#bloc-ge"><i style="background:var(--ge)">II</i>' + L("Geometria", "Geometría", "Geometry") + "</a>")
for a, b in [("2n BAT CCSS", "2n BAT MII"), ("2º BAT CCSS", "2º BAT MII"), ("2n Batxillerat CCSS", "2n Batxillerat MII"), ("2º Bachillerato CCSS", "2º Bachillerato MII"),
             ("2nd Baccalaureate, Social Sciences", "2nd Baccalaureate, Mathematics II"), ("2nd Bacc. Social Sciences", "2nd Bacc. Maths II")]:
    s = s.replace(a, b)
assert "CCSS" not in s and "Social Sciences" not in s, "queda alguna menció a CCSS"

# ---------- estil: el color taronja de la programació lineal passa a la geometria ----------
s = s.replace("--pl", "--ge").replace('[data-b="pl"]', '[data-b="ge"]')
rep("</style>", read("extra.css") + "</style>")

# ---------- contingut ----------
m1 = re.search(r"<!-- =+ BLOC II: .*?-->", s); m2 = re.search(r"<!-- =+ BLOC III: .*?-->", s)
assert m1 and m2
s = s[:m1.start()] + "@@GEOMETRIA@@\n\n" + s[m2.start():]

# renumeració: anàlisi 8–13 → 13–19 (amb L'Hôpital nou al 16) i probabilitat 14–18 → 20–24
NUM = {8: 13, 9: 14, 10: 15, 11: 17, 12: 18, 13: 19, 14: 20, 15: 21, 16: 22, 17: 23, 18: 24}
s = re.sub(r'<section class="unit" id="s(\d+)">\n  <div class="sec-head"><span class="num">(\d+)</span>',
           lambda m: (lambda n: f'<section class="unit" id="s{n}">\n  <div class="sec-head"><span class="num">{n}</span>')(NUM.get(int(m.group(1)), int(m.group(1)))), s)
s = re.sub(r"<!-- =+ (\d+)\. ", lambda m: m.group(0).replace(m.group(1) + ".", str(NUM.get(int(m.group(1)), int(m.group(1)))) + "."), s)

s = s.replace("@@GEOMETRIA@@\n", expand(read("geometria.html")))
A = frags(read("analisi.html"))

def sec_end(sid):
    i = s.find(f'<section class="unit" id="{sid}">'); assert i > 0, sid
    return s.find("</section>", i)
j = sec_end("s14"); s = s[:j] + A["bolzano"] + s[j:]
rep('\n  <div class="card">\n    <h3 class="ch"><span data-l="va">Interpretació geomètrica de la derivada',
    "\n" + A["tecniques"] + '\n  <div class="card">\n    <h3 class="ch"><span data-l="va">Interpretació geomètrica de la derivada')
j = sec_end("s15"); s = s[:j] + A["rolle"] + s[j:]
j = sec_end("s15") + len("</section>\n"); s = s[:j] + "\n<!-- ======================= 16. REGLA DE L'HÔPITAL ======================= -->\n" + A["lhopital"] + s[j:]
rep('\n  <div class="card">\n    <h3 class="ch"><span data-l="va">Integral definida',
    "\n" + A["metodes"] + '\n  <div class="card">\n    <h3 class="ch"><span data-l="va">Integral definida')
rep('      <div class="widget" id="w-area">', A["volums"] + '      <div class="widget" id="w-area">')

# ---------- índex generat a partir de les seccions ----------
toc = []
for b in re.finditer(r'<div class="bloc" data-b="(\w+)" id="bloc-\w+">\n<header class="bloc-head"><span class="bi">(\w+)</span><div><h2>(.*?)</h2>', s):
    key, roman, h2 = b.group(1), b.group(2), b.group(3)
    toc.append(f'        <li class="tb" data-b="{key}">' + re.sub(r'(<span data-l="\w+">)', r"\1" + roman + " · ", h2) + "</li>")
    end = s.find('<div class="bloc"', b.end()); end = len(s) if end < 0 else end
    for m in re.finditer(r'<section class="unit" id="s(\d+)">\n  <div class="sec-head"><span class="num">\d+</span><h2>(.*?)</h2>', s[b.end():end]):
        toc.append(f'        <li data-b="{key}"><a href="#s{m.group(1)}"><span class="n">{m.group(1)}</span>{m.group(2)}<span class="ck">✓</span></a></li>')
nsec = sum(1 for t in toc if 'class="n"' in t)
assert nsec == 24, nsec
i = s.find('<ol id="toc-list">') + len('<ol id="toc-list">\n'); j = s.find('        <li class="tb" style="--b:var(--muted)">', i)
s = s[:i] + "\n".join(toc) + "\n" + s[j:]
rep("<span id=\"meter-n\">0</span>/18 ", f"<span id=\"meter-n\">0</span>/{nsec} ")

# ---------- JavaScript ----------
rep('var DONE_KEY = "fm-2batx-resum-done";', 'var DONE_KEY = "fm-2batx-mii-resum-done";')
rep("var NSEC = 18;", f"var NSEC = {nsec};")
rep('COL = { alg: "#4e81bd", pl: "#f79645",', 'COL = { alg: "#4e81bd", ge: "#f79645",')
# fora la programació lineal: dades, gràfiques i ginys
i = s.find("  var PL = { region:"); j = s.find("  var PLOTS = {"); assert 0 < i < j; s = s[:i] + s[j:]
i = s.find('\n    "in-p4":'); j = s.find("\n    /* discontinuïtats */"); assert 0 < i < j; s = s[:i] + s[j:]
i = s.find("  function wIneq() {"); j = s.find("  function wLim() {"); assert 0 < i < j; s = s[:i] + s[j:]
assert "plLines" not in s and "PL." not in s and "COL.pl" not in s
rep("wIneq, wPL, ", "")
rep("wTables, wQuiz]", "wTables, drawS3, wVec, wRR, w3P, wPP, wBolz, wLhop, wQuiz]")
rep("  /* ---------- qüestionari ---------- */", read("extra.js") + "  /* ---------- qüestionari ---------- */")

# qüestionari: fora les preguntes de programació lineal, noves de geometria i d'anàlisi
s = re.sub(r'\n    \{ b: "pl", q: .*?\} \},', "", s, flags=re.S)
assert 'b: "pl"' not in s
Q = read("quiz.js").rstrip()
QG, QA = Q.split("// @@an\n")
rep('\n    { b: "an", q: { va: "$\\\\lim\\\\limits_{x\\\\to+\\\\infty}\\\\dfrac{5x^3-x}{2x^3+7}=$"',
    "\n" + QG.replace("// @@ge\n", "").rstrip() + '\n    { b: "an", q: { va: "$\\\\lim\\\\limits_{x\\\\to+\\\\infty}\\\\dfrac{5x^3-x}{2x^3+7}=$"')
rep('\n    { b: "pr", q: { va: "$P(A)=0.5$', "\n" + QA.rstrip() + '\n    { b: "pr", q: { va: "$P(A)=0.5$')

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(s)
print("OK", OUT, len(s), "bytes,", nsec, "apartats")

# FentMates: enllaça el tema comú (logo i colors del bloc) a les pàgines generades
import runpy as _runpy, os as _os
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "_eines":
    _d = _os.path.dirname(_d)
_runpy.run_path(_os.path.join(_d, "tema", "aplica.py"), run_name="__main__")
