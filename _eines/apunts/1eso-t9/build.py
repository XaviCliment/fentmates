import os, re, sys

# Genera materials/1eso/t9-grafics-funcions.html. Ús: python3 _eines/apunts/1eso-t9/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil de les gràfiques és el de
# ../3eso-t8/extra.css i ../3eso-t9/extra.css (cal mantindre'n els marcadors) més extra.css.
# El JavaScript és a app.js (feta a partir de la de 1eso-t8: capçalera genèrica, entrenadors, qüestionari i navegació,
# amb el pla cartesià pla() i els ginys propis) i quiz.js. El contingut és a s123.py i s4567.py (amb comu.py): cada
# resultat es comprova amb ck() i lin() (fraccions exactes).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t9-grafics-funcions.html")
sys.path.insert(0, HERE)
from comu import L, P, sec, NCK
from s123 import s1, s2, s3
from s4567 import s4, s5, s6, s7

SECS = [
  (L("El pla cartesià. Coordenades d'un punt", 'El plano cartesiano. Coordenadas de un punto', 'The Cartesian plane. Coordinates of a point'), s1),
  (L('Aplicacions de les coordenades', 'Aplicaciones de las coordenadas', 'Using coordinates'), s2),
  (L('Relacions entre magnituds: taules i gràfics', 'Relaciones entre magnitudes: tablas y gráficas', 'Related quantities: tables and graphs'), s3),
  (L('Interpretació de gràfics', 'Interpretación de gráficas', 'Interpreting graphs'), s4),
  (L('Funció de proporcionalitat directa: y = m·x', 'Función de proporcionalidad directa: y = m·x', 'Direct proportion: y = m·x'), s5),
  (L('Funció lineal: y = m·x + n', 'Función lineal: y = m·x + n', 'Linear functions: y = m·x + n'), s6),
  (L('Problemes amb funcions lineals', 'Problemas con funciones lineales', 'Problems with linear functions'), s7),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Gràfics de funcions · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 9 (Gràfics de funcions: coordenades cartesianes, taules i gràfics, interpretació de gràfics i funcions lineals) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "(x, y)";')
assert "Gràfics de funcions · FentMates" in head and 'content: "(x, y)"' in head
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
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">9.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Gràfics de funcions", "Gráficas de funciones", "Graphs of functions")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 9", "Unidad 9", "Unit 9")}</span>
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
    <span class="kicker">{L("Apunts de teoria · 1r ESO · Matemàtiques", "Apuntes de teoría · 1º ESO · Matemáticas", "Theory notes · 1st ESO · Mathematics")}</span>
    <h1><span class="u">{L("Unitat 9", "Unidad 9", "Unit 9")}</span> · {TIT}</h1>
    <p>{L("El pla cartesià i les coordenades d'un punt, les seues aplicacions (plànols, jocs, figures i moviments), les taules de valors i els gràfics de dues magnituds relacionades, la interpretació de gràfics (creixement, màxims i mínims, gràfics de distància i temps) i les funcions de proporcionalitat directa i lineals, amb la seua fórmula i la seua representació: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "El plano cartesiano y las coordenadas de un punto, sus aplicaciones (planos, juegos, figuras y movimientos), las tablas de valores y las gráficas de dos magnitudes relacionadas, la interpretación de gráficas (crecimiento, máximos y mínimos, gráficas de distancia y tiempo) y las funciones de proporcionalidad directa y lineales, con su fórmula y su representación: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "The Cartesian plane and the coordinates of a point, how they are used (maps, games, shapes and moves), tables of values and graphs of two related quantities, reading graphs (increasing and decreasing, maxima and minima, distance–time graphs) and direct proportion and linear functions, with their formula and their graph: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 9: Gràfics de funcions · 1r ESO", "Apuntes de teoría · Unidad 9: Gráficas de funciones · 1º ESO", "Theory notes · Unit 9: Graphs of functions · 1st ESO")}</p>
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
_tema.VERSION = "20261102f9"
_tema.aplica_fitxer(OUT)
