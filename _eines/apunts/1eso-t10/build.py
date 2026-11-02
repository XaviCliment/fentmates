import os, re, sys

# Genera materials/1eso/t10-estadistica.html. Ús: python3 _eines/apunts/1eso-t10/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil base de les gràfiques és el de
# ../3eso-t8/extra.css i ../3eso-t9/extra.css (cal mantindre'n els marcadors) més extra.css (gràfics estadístics).
# El JavaScript és a app.js (feta una vegada a partir de la de 1eso-t9: capçalera genèrica, qüestionari i navegació, amb els
# gràfics estadístics, els ginys i els entrenadors propis) i quiz.js. El contingut és a s123.py, s456.py i s789.py (amb comu.py):
# cada resultat es comprova amb ck() i asserts (fraccions exactes).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t10-estadistica.html")
sys.path.insert(0, HERE)
from comu import L, P, sec, NCK
from s123 import s1, s2, s3
from s456 import s4, s5, s6
from s789 import s7, s8, s9

SECS = [
  (L('Població, mostra i variables estadístiques', 'Población, muestra y variables estadísticas', 'Population, sample and statistical variables'), s1),
  (L('Freqüències absolutes i relatives', 'Frecuencias absolutas y relativas', 'Absolute and relative frequencies'), s2),
  (L('Taules de freqüències', 'Tablas de frecuencias', 'Frequency tables'), s3),
  (L('Diagrames de barres, polígons i histogrames', 'Diagramas de barras, polígonos e histogramas', 'Bar charts, polygons and histograms'), s4),
  (L('Diagrames de sectors i pictogrames', 'Diagramas de sectores y pictogramas', 'Pie charts and pictograms'), s5),
  (L('Moda, mitjana i mediana', 'Moda, media y mediana', 'Mode, mean and median'), s6),
  (L('Paràmetres a partir d’una taula de freqüències', 'Parámetros a partir de una tabla de frecuencias', 'Measures from a frequency table'), s7),
  (L('Rang i desviació mitjana', 'Rango y desviación media', 'Range and mean deviation'), s8),
  (L("Problemes d'estadística", 'Problemas de estadística', 'Statistics problems'), s9),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Estadística · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 10 (Estadística: població, mostra i variables, freqüències i taules, gràfics estadístics, moda, mitjana, mediana, rang i desviació mitjana) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "x̄";')
assert "Estadística · FentMates" in head and 'content: "x̄"' in head
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
TIT = L("Estadística", "Estadística", "Statistics")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 10", "Unidad 10", "Unit 10")}</span>
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
    <h1><span class="u">{L("Unitat 10", "Unidad 10", "Unit 10")}</span> · {TIT}</h1>
    <p>{L("Com es fa un estudi estadístic: població, mostra i tipus de variables; el recompte de dades i les taules de freqüències (absolutes, relatives, percentatges i acumulades, també amb dades agrupades en intervals); els gràfics estadístics (barres, polígons, histogrames, sectors i pictogrames) i els paràmetres que resumeixen les dades (moda, mitjana, mediana, rang i desviació mitjana): teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Cómo se hace un estudio estadístico: población, muestra y tipos de variables; el recuento de datos y las tablas de frecuencias (absolutas, relativas, porcentajes y acumuladas, también con datos agrupados en intervalos); los gráficos estadísticos (barras, polígonos, histogramas, sectores y pictogramas) y los parámetros que resumen los datos (moda, media, mediana, rango y desviación media): teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "How a statistical study works: population, sample and types of variable; tallying data and frequency tables (absolute, relative, percentages and cumulative, also with data grouped into intervals); statistical charts (bar charts, polygons, histograms, pie charts and pictograms) and the measures that sum up the data (mode, mean, median, range and mean deviation): theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 10: Estadística · 1r ESO", "Apuntes de teoría · Unidad 10: Estadística · 1º ESO", "Theory notes · Unit 10: Statistics · 1st ESO")}</p>
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
_tema.VERSION = "20261102p10"
_tema.aplica_fitxer(OUT)
