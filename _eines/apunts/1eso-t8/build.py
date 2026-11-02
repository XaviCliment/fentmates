import os, re, sys

# Genera materials/1eso/t8-arees-perimetres.html. Ús: python3 _eines/apunts/1eso-t8/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil de les figures és el de
# ../3eso-t8/extra.css, ../3eso-t9/extra.css i ../1eso-t7/extra.css (cal mantindre'n els marcadors) més extra.css.
# El JavaScript és a app.js (feta a partir de la de 1eso-t7: capçalera genèrica, dibuixant G(), entrenadors, qüestionari
# i navegació) i quiz.js. El contingut és a s123.py, s456.py, s789.py i s1011.py (amb comu.py): cada resultat es comprova amb ck()
# i els càlculs amb π es fan amb 3,14.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t8-arees-perimetres.html")
sys.path.insert(0, HERE)
from comu import L, P
from s123 import s1, s2, s3
from s456 import s4, s5, s6
from s789 import s7, s8, s9
from s1011 import s10, s11
from comu import sec

SECS = [
  (L('Perímetre i àrea. Unitats de mesura', 'Perímetro y área. Unidades de medida', 'Perimeter and area. Units of measurement'), s1),
  (L('Perímetre dels polígons', 'Perímetro de los polígonos', 'Perimeter of polygons'), s2),
  (L('Àrea del quadrat i del rectangle', 'Área del cuadrado y del rectángulo', 'Area of squares and rectangles'), s3),
  (L('Àrea del romboide i del triangle', 'Área del romboide y del triángulo', 'Area of parallelograms and triangles'), s4),
  (L('Àrea del rombe i del trapezi', 'Área del rombo y del trapecio', 'Area of rhombuses and trapeziums'), s5),
  (L('Àrea dels polígons regulars i dels polígons qualssevol', 'Área de los polígonos regulares y de los polígonos cualesquiera', 'Area of regular and irregular polygons'), s6),
  (L('La circumferència i la seua longitud', 'La circunferencia y su longitud', 'The circle and its length'), s7),
  (L("L'àrea del cercle i de les figures circulars", 'El área del círculo y de las figuras circulares', 'Area of discs and circular shapes'), s8),
  (L('Figures compostes', 'Figuras compuestas', 'Compound shapes'), s9),
  (L('El teorema de Pitàgores', 'El teorema de Pitágoras', "Pythagoras' theorem"), s10),
  (L('Pitàgores per a calcular àrees i perímetres', 'Pitágoras para calcular áreas y perímetros', "Using Pythagoras to find areas and perimeters"), s11),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Àrees i perímetres · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 8 (Àrees i perímetres: polígons, circumferència, cercle, figures compostes i teorema de Pitàgores) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "π";')
assert "Àrees i perímetres · FentMates" in head and 'content: "π"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css8 = open(os.path.join(HERE, '..', '3eso-t8', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 8: rectes i paràboles */' in css8
css9 = open(os.path.join(HERE, '..', '3eso-t9', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 9: figures geomètriques */' in css9
css7 = open(os.path.join(HERE, '..', '1eso-t7', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 7 (1r ESO): geometria bàsica del pla */' in css7
css = css8 + css9 + css7 + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
js = js.replace('/*QUIZ*/\n', open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read())
assert 'NSEC = %d' % NS in js and '/*QUIZ*/' not in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">8.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Àrees i perímetres", "Áreas y perímetros", "Area and perimeter")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 8", "Unidad 8", "Unit 8")}</span>
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
    <h1><span class="u">{L("Unitat 8", "Unidad 8", "Unit 8")}</span> · {TIT}</h1>
    <p>{L("Perímetre i àrea, unitats de longitud i de superfície, àrees del quadrat, el rectangle, el romboide, el triangle, el rombe, el trapezi i els polígons regulars, la longitud de la circumferència i el nombre π, l'àrea del cercle i de les figures circulars, les figures compostes i el teorema de Pitàgores per a calcular les mesures que ens falten: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Perímetro y área, unidades de longitud y de superficie, áreas del cuadrado, el rectángulo, el romboide, el triángulo, el rombo, el trapecio y los polígonos regulares, la longitud de la circunferencia y el número π, el área del círculo y de las figuras circulares, las figuras compuestas y el teorema de Pitágoras para calcular las medidas que nos faltan: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Perimeter and area, units of length and area, areas of squares, rectangles, parallelograms, triangles, rhombuses, trapeziums and regular polygons, the circumference and the number π, the area of discs and circular shapes, compound shapes, and Pythagoras' theorem to find missing lengths: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 8: Àrees i perímetres · 1r ESO", "Apuntes de teoría · Unidad 8: Áreas y perímetros · 1º ESO", "Theory notes · Unit 8: Area and perimeter · 1st ESO")}</p>
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
_tema.VERSION = "20261102g8"
_tema.aplica_fitxer(OUT)
