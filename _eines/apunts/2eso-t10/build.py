import os, re, sys

# Genera materials/2eso/t10-funcions.html. Ús: python3 _eines/apunts/2eso-t10/build.py
# Fet a partir dels apunts de la unitat 9 de 1r ESO (../1eso-t9), ampliats i adaptats a 2n ESO.
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil de les gràfiques és el de
# ../3eso-t8/extra.css i ../3eso-t9/extra.css (cal mantindre'n els marcadors) més extra.css.
# El JavaScript és a app.js (el de 1eso-t9 amb el lector d'expressions de 3eso-t7 i ginys i entrenadors nous; window.FM210
# per a provar-lo al navegador) i quiz.js. El contingut és a s12.py (10.1-10.2), s345.py (10.3-10.5), s67.py (10.6-10.7)
# i s8.py (10.8, fet a partir dels apartats 9.4 i 9.7 de 1r), amb comu.py: cada resultat es comprova amb ck() i lin().
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t10-funcions.html")
sys.path.insert(0, HERE)
from comu import L, P, sec, NCK
from s12 import s1, s2
from s345 import s3, s4, s5
from s67 import s6, s7
from s8 import s8

SECS = [
  (L('Concepte de funció', 'Concepto de función', 'What a function is'), s1),
  (L('Funcions donades per taules de valors', 'Funciones dadas por tablas de valores', 'Functions given by tables of values'), s2),
  (L('Funcions donades per la seua equació', 'Funciones dadas por su ecuación', 'Functions given by their equation'), s3),
  (L('Funció de proporcionalitat: y = m·x', 'Función de proporcionalidad: y = m·x', 'Direct proportion: y = m·x'), s4),
  (L("Pendent d'una recta", 'Pendiente de una recta', 'The slope of a line'), s5),
  (L('Funcions lineals: y = m·x + n', 'Funciones lineales: y = m·x + n', 'Linear functions: y = m·x + n'), s6),
  (L('Funcions constants: y = k', 'Funciones constantes: y = k', 'Constant functions: y = k'), s7),
  (L('Interpretació de gràfics i problemes', 'Interpretación de gráficas y problemas', 'Reading graphs and solving problems'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Funcions · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 10 (Funcions: concepte de funció, taules de valors i equacions, funció de proporcionalitat, pendent, funcions lineals i constants, interpretació de gràfics i problemes) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "f(x)";')
assert "Funcions · FentMates" in head and 'content: "f(x)"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css8 = open(os.path.join(HERE, '..', '3eso-t8', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 8: rectes i paràboles */' in css8
css9 = open(os.path.join(HERE, '..', '3eso-t9', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 9: figures geomètriques */' in css9
css = css8 + css9 + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
js = js.replace('/*QUIZ*/\n', open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read())
assert 'NSEC = %d' % NS in js and '/*QUIZ*/' not in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">10.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Funcions", "Funciones", "Functions")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 10", "Unidad 10", "Unit 10")}</span>
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
    <h1><span class="u">{L("Unitat 10", "Unidad 10", "Unit 10")}</span> · {TIT}</h1>
    <p>{L("Què és una funció i com es reconeix, les funcions donades per un enunciat, per una taula de valors, per un gràfic o per la seua equació, la funció de proporcionalitat y = m·x, el pendent d'una recta, les funcions lineals y = m·x + n i les funcions constants, i la interpretació de gràfics i els problemes amb funcions: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Qué es una función y cómo se reconoce, las funciones dadas por un enunciado, por una tabla de valores, por una gráfica o por su ecuación, la función de proporcionalidad y = m·x, la pendiente de una recta, las funciones lineales y = m·x + n y las funciones constantes, y la interpretación de gráficas y los problemas con funciones: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "What a function is and how to recognise one, functions given in words, by a table of values, by a graph or by their equation, the direct proportion function y = m·x, the slope of a line, linear functions y = m·x + n and constant functions, and reading graphs and solving problems with functions: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 10: Funcions · 2n ESO", "Apuntes de teoría · Unidad 10: Funciones · 2º ESO", "Theory notes · Unit 10: Functions · 2nd ESO")}</p>
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
print('ok', OUT, len(html.split('\n')), 'lines,', ntools, 'tools,', NCK[0], 'checks')

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
_tema.VERSION = "20261116e2u10"
_tema.aplica_fitxer(OUT)
