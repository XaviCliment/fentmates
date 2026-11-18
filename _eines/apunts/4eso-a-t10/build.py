import os, re, sys

# Genera materials/4eso-a/t10-estadistica-bidimensional.html. Ús: python3 _eines/apunts/4eso-a-t10/build.py
# 4t ESO Matemàtiques A, Unitat 10: Estadística bidimensional. Mateixa estructura que els apunts de la unitat 9 (../4eso-a-t9):
# comu.py (amb bi(), rl() i els núvols de punts en SVG, nuvol()), extra.css (a continuació del de la unitat 9) i app.js (ginys
# w-dbl, w-cloud, w-slide, w-cov, w-guess, w-eye, w-reg i w-est; entrenadors rel, cg, tipus, sentit, cov, rcalc, rint, recta,
# est i fiab; window.FM410 per a provar-lo al navegador). Els núvols dels ginys es dibuixen amb cloud() d'app.js, que copia
# nuvol() de comu.py. El contingut és a s12.py (10.1-10.2), s3.py, s4.py i s56.py (10.5-10.6): cada resultat es comprova amb
# ck() (exacte) o ckr() (arrodonit). El qüestionari és a quiz.js.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/4eso-a/t10-estadistica-bidimensional.html")
sys.path.insert(0, HERE)
from comu import L, P, sec, NCK
from s12 import s1, s2
from s3 import s3
from s4 import s4
from s56 import s5, s6

SECS = [
  (L('Distribucions bidimensionals', 'Distribuciones bidimensionales', 'Bivariate distributions'), s1),
  (L('Núvol de punts', 'Nube de puntos', 'Scatter plots'), s2),
  (L('Correlació', 'Correlación', 'Correlation'), s3),
  (L('Coeficient de correlació', 'Coeficiente de correlación', 'The correlation coefficient'), s4),
  (L('Recta de regressió', 'Recta de regresión', 'The regression line'), s5),
  (L('Estimacions', 'Estimaciones', 'Estimates'), s6),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Estadística bidimensional · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 10 (Estadística bidimensional: distribucions bidimensionals, núvol de punts, correlació, coeficient de correlació, recta de regressió i estimacions) de 4t d\'ESO Matemàtiques A, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "r";')
assert "Estadística bidimensional · FentMates" in head and 'content: "r"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css8 = open(os.path.join(HERE, '..', '3eso-t8', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 8: rectes i paràboles */' in css8
css9 = open(os.path.join(HERE, '..', '3eso-t9', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 9: figures geomètriques */' in css9
css = css8 + css9 + open(os.path.join(HERE, '..', '4eso-a-t9', 'extra.css'), encoding='utf-8').read() + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
js = js.replace('/*QUIZ*/\n', open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read())
assert 'NSEC = %d' % NS in js and '/*QUIZ*/' not in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">10.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Estadística bidimensional", "Estadística bidimensional", "Bivariate Statistics")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../4eso-a.html">{L("4t ESO A", "4º ESO A", "4th ESO A (Year 10)")}</a> / {L("Unitat 10", "Unidad 10", "Unit 10")}</span>
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
    <h1><span class="u">{L("Unitat 10", "Unidad 10", "Unit 10")}</span> · {TIT}</h1>
    <p>{L("Com s'estudien dues variables alhora: les distribucions bidimensionals i les seues taules, el núvol de punts i el centre de gravetat, la correlació (positiva o negativa, forta o feble) i el coeficient de correlació, la recta de regressió i com es fa servir per a fer estimacions fiables: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Cómo se estudian dos variables a la vez: las distribuciones bidimensionales y sus tablas, la nube de puntos y el centro de gravedad, la correlación (positiva o negativa, fuerte o débil) y el coeficiente de correlación, la recta de regresión y cómo se usa para hacer estimaciones fiables: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "How to study two variables at once: bivariate distributions and their tables, scatter plots and the centre of gravity, correlation (positive or negative, strong or weak) and the correlation coefficient, the regression line and how to use it to make reliable estimates: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 10: Estadística bidimensional · 4t ESO Matemàtiques A", "Apuntes de teoría · Unidad 10: Estadística bidimensional · 4º ESO Matemáticas A", "Theory notes · Unit 10: Bivariate Statistics · 4th ESO Maths A")}</p>
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
_tema.VERSION = "20261118a4u10"
_tema.aplica_fitxer(OUT)
