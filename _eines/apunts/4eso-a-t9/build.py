import os, re, sys

# Genera materials/4eso-a/t9-estadistica.html. Ús: python3 _eines/apunts/4eso-a-t9/build.py
# 4t ESO Matemàtiques A, Unitat 9: Estadística. Fet a partir dels apunts de 1r ESO (../1eso-t10): mateix comu.py (amb la
# variància, els percentils i el diagrama de caixes), extra.css i app.js (amb els ginys nous w-grp, w-var, w-quart i w-box i
# els entrenadors interval, marca, var, cv, quart, perc, boxread i boxpct; window.FM49 per a provar-lo al navegador).
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil base de les gràfiques és el de
# ../3eso-t8/extra.css i ../3eso-t9/extra.css (cal mantindre'n els marcadors) més extra.css. El contingut és a s123.py
# (9.1-9.3), s4.py, s5.py, s6.py i s78.py (9.7-9.8), amb comu.py: cada resultat es comprova amb ck() (exacte) o ckr()
# (arrodonit). El qüestionari és a quiz.js.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/4eso-a/t9-estadistica.html")
sys.path.insert(0, HERE)
from comu import L, P, sec, NCK
from s123 import s1, s2, s3
from s4 import s4
from s5 import s5
from s6 import s6
from s78 import s7, s8

SECS = [
  (L('Població, mostra i variables estadístiques', 'Población, muestra y variables estadísticas', 'Population, sample and statistical variables'), s1),
  (L('Taules de freqüències amb dades aïllades', 'Tablas de frecuencias con datos aislados', 'Frequency tables with ungrouped data'), s2),
  (L('Taules amb dades agrupades en intervals', 'Tablas con datos agrupados en intervalos', 'Tables with data grouped into intervals'), s3),
  (L('Gràfics estadístics', 'Gráficos estadísticos', 'Statistical charts'), s4),
  (L('Paràmetres de centralització', 'Parámetros de centralización', 'Measures of central tendency'), s5),
  (L('Paràmetres de dispersió', 'Parámetros de dispersión', 'Measures of spread'), s6),
  (L('Paràmetres de posició: quartils i percentils', 'Parámetros de posición: cuartiles y percentiles', 'Measures of position: quartiles and percentiles'), s7),
  (L('Diagrama de caixes', 'Diagrama de cajas', 'Box plots'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Estadística · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 9 (Estadística: població, mostra i variables, taules de freqüències amb dades aïllades i agrupades, gràfics estadístics, paràmetres de centralització, dispersió i posició i diagrama de caixes) de 4t d\'ESO Matemàtiques A, en valencià, castellà i anglés.">', head)
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
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">9.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Estadística", "Estadística", "Statistics")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../4eso-a.html">{L("4t ESO A", "4º ESO A", "4th ESO A (Year 10)")}</a> / {L("Unitat 9", "Unidad 9", "Unit 9")}</span>
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
    <span class="kicker">{L("Apunts de teoria · 4t ESO · Matemàtiques A", "Apuntes de teoría · 4º ESO · Matemáticas A", "Theory notes · 4th ESO · Mathematics A")}</span>
    <h1><span class="u">{L("Unitat 9", "Unidad 9", "Unit 9")}</span> · {TIT}</h1>
    <p>{L("Com es fa un estudi estadístic: població, mostra, mostreig i tipus de variables; les taules de freqüències (absolutes, relatives, acumulades i percentatges) amb dades aïllades i amb dades agrupades en intervals; els gràfics estadístics; els paràmetres de centralització (moda, mediana i mitjana), de dispersió (rang, desviació mitjana, variància, desviació típica i coeficient de variació) i de posició (quartils i percentils), i el diagrama de caixes: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Cómo se hace un estudio estadístico: población, muestra, muestreo y tipos de variables; las tablas de frecuencias (absolutas, relativas, acumuladas y porcentajes) con datos aislados y con datos agrupados en intervalos; los gráficos estadísticos; los parámetros de centralización (moda, mediana y media), de dispersión (rango, desviación media, varianza, desviación típica y coeficiente de variación) y de posición (cuartiles y percentiles), y el diagrama de cajas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "How a statistical study works: population, sample, sampling and types of variable; frequency tables (absolute, relative, cumulative and percentages) with ungrouped data and with data grouped into intervals; statistical charts; measures of central tendency (mode, median and mean), of spread (range, mean deviation, variance, standard deviation and coefficient of variation) and of position (quartiles and percentiles), and box plots: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 9: Estadística · 4t ESO Matemàtiques A", "Apuntes de teoría · Unidad 9: Estadística · 4º ESO Matemáticas A", "Theory notes · Unit 9: Statistics · 4th ESO Maths A")}</p>
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
_tema.VERSION = "20261118a4u9"
_tema.aplica_fitxer(OUT)
