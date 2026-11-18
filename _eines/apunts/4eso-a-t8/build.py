import os, re, sys

# Genera materials/4eso-a/t8-semblanca-aplicacions.html. Ús: python3 _eines/apunts/4eso-a-t8/build.py
# 4t ESO Matemàtiques A, Unitat 8: Semblança. Aplicacions. Fet a partir dels apunts de 2n ESO (../2eso-t8), que ja venien
# dels de 3r (../3eso-t10), amb els volums de cossos semblants i de maquetes, la distància a un punt inaccessible (8.5),
# la semblança de triangles rectangles amb els teoremes de l'altura i del catet (8.6) i un apartat de problemes (8.7).
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil propi és el de
# ../3eso-t8/extra.css i ../3eso-t9/extra.css (figures) més extra.css; el JavaScript és a app.js (el de ../3eso-t10, amb els
# mateixos ginys i entrenadors més w-inacc, w-alt i els entrenadors inacc, rect i mix; window.FM48 per a provar-lo al
# navegador) i quiz.js. El contingut és a s123.py (8.1-8.3), s4.py, s5.py i s67.py (8.6-8.7), amb comu.py i fig8.py: cada
# resultat es comprova amb ck().
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/4eso-a/t8-semblanca-aplicacions.html")
sys.path.insert(0, HERE)
from comu import L, P, sec
from s123 import s1, s2, s3
from s4 import s4
from s5 import s5
from s67 import s6, s7

SECS = [
  (L('Figures semblants', 'Figuras semejantes', 'Similar figures'), s1),
  (L('Plànols, mapes i maquetes', 'Planos, mapas y maquetas', 'Plans, maps and scale models'), s2),
  (L('El teorema de Tales', 'El teorema de Tales', "Thales' theorem"), s3),
  (L('Semblança de triangles. Criteris', 'Semejanza de triángulos. Criterios', 'Similar triangles. Criteria'), s4),
  (L('Aplicació: distància a un punt inaccessible', 'Aplicación: distancia a un punto inaccesible', 'Application: distance to an inaccessible point'), s5),
  (L('Semblança de triangles rectangles', 'Semejanza de triángulos rectángulos', 'Similar right triangles'), s6),
  (L('Problemes de semblança', 'Problemas de semejanza', 'Similarity problems'), s7),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Semblança. Aplicacions · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 8 (Semblança. Aplicacions: figures semblants, plànols, mapes i maquetes, teorema de Tales, semblança de triangles, distància a un punt inaccessible i triangles rectangles) de 4t d\'ESO Matemàtiques A, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "k";')
assert "Semblança. Aplicacions · FentMates" in head and 'content: "k"' in head
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
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">8.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Semblança. Aplicacions", "Semejanza. Aplicaciones", "Similarity. Applications")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../4eso-a.html">{L("4t ESO A", "4º ESO A", "4th ESO A (Year 10)")}</a> / {L("Unitat 8", "Unidad 8", "Unit 8")}</span>
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
    <h1><span class="u">{L("Unitat 8", "Unidad 8", "Unit 8")}</span> · {TIT}</h1>
    <p>{L("Figures semblants i raó de semblança, perímetres, àrees i volums de figures semblants, escales de plànols, mapes i maquetes, el teorema de Tales, triangles en posició de Tales i criteris de semblança, el càlcul de la distància a un punt inaccessible, la semblança de triangles rectangles (amb els teoremes de l'altura i del catet) i problemes d'altures i distàncies amb ombres, miralls i fanals: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Figuras semejantes y razón de semejanza, perímetros, áreas y volúmenes de figuras semejantes, escalas de planos, mapas y maquetas, el teorema de Tales, triángulos en posición de Tales y criterios de semejanza, el cálculo de la distancia a un punto inaccesible, la semejanza de triángulos rectángulos (con los teoremas de la altura y del cateto) y problemas de alturas y distancias con sombras, espejos y farolas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Similar figures and the scale factor, perimeters, areas and volumes of similar figures, scales of plans, maps and scale models, Thales' theorem, triangles in Thales position and similarity criteria, finding the distance to an inaccessible point, similar right triangles (with the altitude and leg theorems) and problems on heights and distances using shadows, mirrors and street lamps: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 8: Semblança. Aplicacions · 4t ESO Matemàtiques A", "Apuntes de teoría · Unidad 8: Semejanza. Aplicaciones · 4º ESO Matemáticas A", "Theory notes · Unit 8: Similarity. Applications · 4th ESO Maths A")}</p>
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
_tema.VERSION = "20261118a4u8"
_tema.aplica_fitxer(OUT)
