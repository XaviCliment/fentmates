import os, re, sys

# Genera materials/2eso/t11-atzar-probabilitat.html. Ús: python3 _eines/apunts/2eso-t11/build.py
# Fet a partir dels apunts de probabilitat de 3r ESO (../3eso-t12), adaptats a 2n ESO.
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil propi és el de
# ../3eso-t8/extra.css més extra.css; el JavaScript és a app.js (el de ../3eso-t12 amb els entrenadors nous «aleatori o
# determinista?» i de taules de contingència i el giny de la taula de contingència; window.FM211 per a provar-lo al
# navegador) i quiz.js. El contingut és a s12.py (11.1-11.2), s3.py, s4.py i s5.py (amb comu.py): cada probabilitat es
# comprova amb fraccions exactes.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t11-atzar-probabilitat.html")
sys.path.insert(0, HERE)
from comu import L, P, sec
from s12 import s1, s2
from s3 import s3
from s4 import s4
from s5 import s5

SECS = [
  (L('Experiments aleatoris i deterministes', 'Experimentos aleatorios y deterministas', 'Random and deterministic experiments'), s1),
  (L('Espai mostral i esdeveniments', 'Espacio muestral y sucesos', 'Sample space and events'), s2),
  (L("Probabilitat d'un esdeveniment", 'Probabilidad de un suceso', 'Probability of an event'), s3),
  (L('Probabilitat en experiments regulars: llei de Laplace', 'Probabilidad en experimentos regulares: ley de Laplace', "Probability in regular experiments: Laplace's rule"), s4),
  (L("Estratègies: diagrama d'arbre i taula de contingència", 'Estrategias: diagrama de árbol y tabla de contingencia', 'Strategies: tree diagrams and contingency tables'), s5),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Atzar i probabilitat · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 11 (Atzar i probabilitat) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "P(A)";')
assert "<title>Atzar i probabilitat · FentMates" in head and 'content: "P(A)"' in head and "Unitat 11 (Atzar i probabilitat)" in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css8 = open(os.path.join(HERE, '..', '3eso-t8', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 8: rectes i paràboles */' in css8
css = css8 + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
js = js.replace('/*QUIZ*/\n', open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read())
js = re.sub(r'NSEC = \d+', 'NSEC = %d' % NS, js)
assert 'NSEC = %d' % NS in js and '/*QUIZ*/' not in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">11.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Atzar i probabilitat", "Azar y probabilidad", "Chance and probability")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 11", "Unidad 11", "Unit 11")}</span>
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
    <h1><span class="u">{L("Unitat 11", "Unidad 11", "Unit 11")}</span> · {TIT}</h1>
    <p>{L("Experiments aleatoris i deterministes, el llenguatge de l'atzar, l'espai mostral i els esdeveniments, freqüències i probabilitat, la llei dels grans nombres, la llei de Laplace i les estratègies per a calcular probabilitats: diagrames d'arbre, taules de doble entrada i taules de contingència. Teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a experimentar i practicar.",
          "Experimentos aleatorios y deterministas, el lenguaje del azar, el espacio muestral y los sucesos, frecuencias y probabilidad, la ley de los grandes números, la ley de Laplace y las estrategias para calcular probabilidades: diagramas de árbol, tablas de doble entrada y tablas de contingencia. Teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para experimentar y practicar.",
          "Random and deterministic experiments, the language of chance, sample spaces and events, frequencies and probability, the law of large numbers, Laplace's rule and strategies for working out probabilities: tree diagrams, two-way tables and contingency tables. Theory explained step by step, worked problems from easier to harder and interactive tools to experiment and practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 11: Atzar i probabilitat · 2n ESO", "Apuntes de teoría · Unidad 11: Azar y probabilidad · 2º ESO", "Theory notes · Unit 11: Chance and probability · 2nd ESO")}</p>
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
_tema.VERSION = "20261116e2u11"
_tema.aplica_fitxer(OUT)
