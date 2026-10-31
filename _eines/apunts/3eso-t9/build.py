import os, re, sys

# Genera materials/3eso/t9-perimetres-arees-pitagores.html. Ús: python3 _eines/apunts/3eso-t9/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil propi és el de la
# unitat 8 (../3eso-t8/extra.css) més extra.css; el JavaScript és a app.js (feta a partir del de la unitat 8: ajudes,
# entrenadors, qüestionari i navegació, més el dibuixant de figures G() i els ginys de la unitat) i quiz.js.
# El contingut és a s12.py, s34.py, s56.py i s78.py (amb comu.py): cada resultat numèric es comprova amb ck().
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/3eso/t9-perimetres-arees-pitagores.html")
sys.path.insert(0, HERE)
from comu import L, P
from s12 import s1, s2
from s34 import s3, s4
from s56 import s5, s6
from s78 import s7, s8
from comu import sec

SECS = [
  (L('El teorema de Pitàgores', 'El teorema de Pitágoras', "Pythagoras' theorem"), s1),
  (L('Classificació de triangles pels costats', 'Clasificación de triángulos por sus lados', 'Classifying triangles by their sides'), s2),
  (L('Aplicacions del teorema de Pitàgores', 'Aplicaciones del teorema de Pitágoras', "Applications of Pythagoras' theorem"), s3),
  (L('Perímetres i àrees de triangles i quadrilàters', 'Perímetros y áreas de triángulos y cuadriláteros', 'Perimeters and areas of triangles and quadrilaterals'), s4),
  (L('Polígons regulars', 'Polígonos regulares', 'Regular polygons'), s5),
  (L('La circumferència: longitud i arcs', 'La circunferencia: longitud y arcos', 'The circle: circumference and arcs'), s6),
  (L('Àrea del cercle i figures circulars', 'Área del círculo y figuras circulares', 'Area of a disc and circular shapes'), s7),
  (L('Figures compostes i problemes', 'Figuras compuestas y problemas', 'Composite shapes and problems'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Perímetres i àrees. Teorema de Pitàgores · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 9 (Perímetres i àrees. Teorema de Pitàgores) de 3r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "a²+b²=c²";')
assert "Teorema de Pitàgores · FentMates" in head and 'content: "a²+b²=c²"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css8 = open(os.path.join(HERE, '..', '3eso-t8', 'extra.css'), encoding='utf-8').read()
assert '/* unitat 8: rectes i paràboles */' in css8
css = css8 + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
js = js.replace('/*QUIZ*/\n', open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read())
assert 'NSEC = %d' % NS in js and '/*QUIZ*/' not in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">9.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Perímetres i àrees. Teorema de Pitàgores", "Perímetros y áreas. Teorema de Pitágoras", "Perimeters and areas. Pythagoras' theorem")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../3eso.html">{L("3r ESO", "3º ESO", "3rd ESO (Year 9)")}</a> / {L("Unitat 9", "Unidad 9", "Unit 9")}</span>
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
    <span class="kicker">{L("Apunts de teoria · 3r ESO · Matemàtiques", "Apuntes de teoría · 3º ESO · Matemáticas", "Theory notes · 3rd ESO · Mathematics")}</span>
    <h1><span class="u">{L("Unitat 9", "Unidad 9", "Unit 9")}</span> · {TIT}</h1>
    <p>{L("El teorema de Pitàgores i el seu recíproc, classificació de triangles, aplicacions en figures planes i en el pla de coordenades, perímetres i àrees de polígons, polígons regulars, la circumferència i el cercle (arcs, sectors, corones) i figures compostes: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "El teorema de Pitágoras y su recíproco, clasificación de triángulos, aplicaciones en figuras planas y en el plano de coordenadas, perímetros y áreas de polígonos, polígonos regulares, la circunferencia y el círculo (arcos, sectores, coronas) y figuras compuestas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Pythagoras' theorem and its converse, classifying triangles, applications in plane shapes and on the coordinate plane, perimeters and areas of polygons, regular polygons, circles and discs (arcs, sectors, annuli) and composite shapes: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 9: Perímetres i àrees. Teorema de Pitàgores · 3r ESO", "Apuntes de teoría · Unidad 9: Perímetros y áreas. Teorema de Pitágoras · 3º ESO", "Theory notes · Unit 9: Perimeters and areas. Pythagoras' theorem · 3rd ESO")}</p>
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
_tema.VERSION = "20261031g9"
_tema.aplica_fitxer(OUT)
