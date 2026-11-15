import os, re, sys

# Genera materials/2eso/t3-algebra-polinomis.html. Ús: python3 _eines/apunts/2eso-t3/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el contingut és a alg.py (3.1-3.3)
# i pol.py (3.4-3.8), les ajudes a comu.py, el JavaScript a app.js (fet a partir del de ../3eso-t4, amb la potència de
# monomis, entrenadors nous i el qüestionari de 2n; window.FM23 per a provar-lo al navegador) i l'estil a extra.css.
# Les comprovacions chk() d'alg.py i pol.py (sympy) verifiquen els resultats escrits a mà.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t3-algebra-polinomis.html")
from comu import L, P, sec
from alg import s1, s2, s3
from pol import s4, s5, s6, s7, s8

# ============================================================ muntatge
SECS = [
  (L("L'àlgebra: el llenguatge algebraic", 'El álgebra: el lenguaje algebraico', 'Algebra: algebraic language'), s1),
  (L('Monomis: parts i valor numèric', 'Monomios: partes y valor numérico', 'Monomials: parts and value'), s2),
  (L('Operacions amb monomis', 'Operaciones con monomios', 'Operations with monomials'), s3),
  (L('Polinomis: parts', 'Polinomios: partes', 'Polynomials: parts'), s4),
  (L('Suma i resta de polinomis', 'Suma y resta de polinomios', 'Adding and subtracting polynomials'), s5),
  (L('Producte de polinomis', 'Producto de polinomios', 'Multiplying polynomials'), s6),
  (L('Identitats notables', 'Identidades notables', 'Special products'), s7),
  (L('Extracció de factor comú', 'Extracción de factor común', 'Taking out a common factor'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Àlgebra. Polinomis · FentMates</title>')
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "x²";')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 3 (Introducció a l\'àlgebra. Polinomis) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
assert 'Àlgebra. Polinomis · FentMates' in head and 'content: "x²"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
assert 'NSEC = %d' % NS in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">3.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 3", "Unidad 3", "Unit 3")}</span>
    <span class="spacer"></span>
    <div class="lang-switch" role="group" aria-label="Idioma / Language">
      <button type="button" data-setlang="va">VA</button><button type="button" data-setlang="es">ES</button><button type="button" data-setlang="en">EN</button>
    </div>
    <button class="icon-btn" type="button" id="theme-btn" aria-label="Mode clar / fosc"></button>
  </div>
  <div class="progress" id="progress"></div>
</header>

<section class="hero">
  <div class="in">
    <span class="kicker">{L("Apunts de teoria · 2n ESO · Matemàtiques", "Apuntes de teoría · 2º ESO · Matemáticas", "Theory notes · 2nd ESO · Mathematics")}</span>
    <h1><span class="u">{L("Unitat 3", "Unidad 3", "Unit 3")}</span> · {L("Introducció a l'àlgebra. Polinomis", "Introducción al álgebra. Polinomios", "Introduction to algebra. Polynomials")}</h1>
    <p>{L("Què és l'àlgebra i com es tradueix el llenguatge habitual al llenguatge algebraic, monomis (parts, grau, monomis semblants i valor numèric) i les seues operacions (suma, resta, producte, quocient, potències i operacions combinades), polinomis i les seues parts, suma, resta i producte de polinomis, identitats notables i extracció de factor comú: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Qué es el álgebra y cómo se traduce el lenguaje habitual al lenguaje algebraico, monomios (partes, grado, monomios semejantes y valor numérico) y sus operaciones (suma, resta, producto, cociente, potencias y operaciones combinadas), polinomios y sus partes, suma, resta y producto de polinomios, identidades notables y extracción de factor común: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "What algebra is and how to turn words into algebra, monomials (parts, degree, like terms and value) and their operations (adding, subtracting, multiplying, dividing, powers and mixed operations), polynomials and their parts, adding, subtracting and multiplying polynomials, special products and taking out a common factor: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
    <div class="chips"><span>{L(f"{NS} apartats", f"{NS} apartados", f"{NS} sections")}</span><span>{L(f"{ntools} eines interactives", f"{ntools} herramientas interactivas", f"{ntools} interactive tools")}</span><span>{L("Problemes per nivells ★☆☆ → ★★★", "Problemas por niveles ★☆☆ → ★★★", "Problems by level ★☆☆ → ★★★")}</span><span>{L("Autoavaluació final", "Autoevaluación final", "Final self-check")}</span></div>
  </div>
</section>

<div class="layout">
  <nav class="toc" aria-label="Índex">
    <details open id="toc-d">
      <summary>{L("Índex", "Índice", "Contents")}</summary>
      <ol id="toc-list">
{toc}        <li><a href="#quiz"><span class="n">?</span>{L("Autoavaluació", "Autoevaluación", "Self-check")}</a></li>
      </ol>
      <div class="meter"><i id="meter"></i></div>
      <div class="meter-l"><span id="meter-n">0</span>/{NS} {L("apartats estudiats", "apartados estudiados", "sections studied")}</div>
    </details>
  </nav>

<article>
{''.join(sec(i, t, b) for i, (t, b) in enumerate(SECS, 1))}
<!-- ======================= QUIZ ======================= -->
<section class="unit quiz-sec" id="quiz">
  <div class="sec-head"><span class="num">?</span><h2>{L("Autoavaluació", "Autoevaluación", "Self-check")}</h2></div>
  {P("Respon i comprova a l'instant si ho has entés. Les preguntes van de més fàcils a més difícils.", "Responde y comprueba al instante si lo has entendido. Las preguntas van de más fáciles a más difíciles.", "Answer and instantly check whether you've understood. The questions go from easier to harder.")}
  <div class="quiz" id="quiz-box"></div>
  <div class="score" id="quiz-score"></div>
  <button class="btn" type="button" id="quiz-reset">↺ {L("Torna a començar", "Volver a empezar", "Start again")}</button>
</section>

</article>
</div>

<footer class="foot">
  <p>{L("Apunts de teoria · Unitat 3: Introducció a l'àlgebra. Polinomis · 2n ESO", "Apuntes de teoría · Unidad 3: Introducción al álgebra. Polinomios · 2º ESO", "Theory notes · Unit 3: Introduction to algebra. Polynomials · 2nd ESO")}</p>
  <p><a href="../../index.html">FentMates</a> · {L("Fet amb ♥ per a l'alumnat", "Hecho con ♥ para el alumnado", "Made with ♥ for students")}</p>
</footer>
<button class="icon-btn to-top" type="button" id="to-top" aria-label="↑">↑</button>

<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
{js}</script>
</body>
</html>
'''
html = head + '\n' + css + '\n' + wide + '\n</style>\n</head>\n' + body
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)
print('ok', OUT, len(html.split('\n')), 'lines,', ntools, 'tools')

sys.path.insert(0, os.path.dirname(HERE))
import relabel
print('\n'.join(relabel.fix_file(OUT)))

# FentMates: enllaça el tema comú (logo i colors del bloc) només a aquesta pàgina; aplica.py sencer
# reescriuria la versió de totes les altres pàgines de materials/.
import importlib.util as _ilu
_d = os.path.dirname(HERE)
while os.path.basename(_d) != "_eines":
    _d = os.path.dirname(_d)
_sp = _ilu.spec_from_file_location("aplica", os.path.join(_d, "tema", "aplica.py"))
_tema = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_tema)
_tema.VERSION = "20261115d2"
_tema.aplica_fitxer(OUT)
