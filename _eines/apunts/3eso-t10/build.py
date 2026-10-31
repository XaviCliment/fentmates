import os, re, sys

# Genera materials/3eso/t10-tales-semblanca.html. Ús: python3 _eines/apunts/3eso-t10/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil propi és el de la
# unitat 8 (../3eso-t8/extra.css) i el de la unitat 9 (../3eso-t9/extra.css, figures) més extra.css; el JavaScript és a
# app.js (fet a partir del de la unitat 9: ajudes, G(), entrenadors, qüestionari i navegació, més els ginys de la unitat)
# i quiz.js. El contingut és a s12.py, s34.py, s56.py i s78.py (amb comu.py i fig10.py): cada resultat es comprova amb ck().
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/3eso/t10-tales-semblanca.html")
sys.path.insert(0, HERE)
from comu import L, P
from s12 import s1, s2
from s34 import s3, s4
from s56 import s5, s6
from s78 import s7, s8
from comu import sec

SECS = [
  (L('Raons i proporcions entre segments', 'Razones y proporciones entre segmentos', 'Ratios and proportions between segments'), s1),
  (L('El teorema de Tales', 'El teorema de Tales', "Thales' theorem"), s2),
  (L('Dividir un segment en parts iguals o proporcionals', 'Dividir un segmento en partes iguales o proporcionales', 'Dividing a segment into equal or proportional parts'), s3),
  (L('Triangles en posició de Tales', 'Triángulos en posición de Tales', 'Triangles in Thales position'), s4),
  (L('Figures semblants. Raó de semblança', 'Figuras semejantes. Razón de semejanza', 'Similar figures. Scale factor'), s5),
  (L('Criteris de semblança de triangles', 'Criterios de semejanza de triángulos', 'Similarity criteria for triangles'), s6),
  (L('Aplicacions: altures i distàncies', 'Aplicaciones: alturas y distancias', 'Applications: heights and distances'), s7),
  (L('Escales. Àrees i volums de figures semblants', 'Escalas. Áreas y volúmenes de figuras semejantes', 'Scales. Areas and volumes of similar figures'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Proporcionalitat. Teorema de Tales · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 10 (Proporcionalitat. Teorema de Tales) de 3r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "a/b = c/d";')
assert "Teorema de Tales · FentMates" in head and 'content: "a/b = c/d"' in head
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
TIT = L("Proporcionalitat. Teorema de Tales", "Proporcionalidad. Teorema de Tales", "Proportionality. Thales' theorem")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../3eso.html">{L("3r ESO", "3º ESO", "3rd ESO (Year 9)")}</a> / {L("Unitat 10", "Unidad 10", "Unit 10")}</span>
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
    <h1><span class="u">{L("Unitat 10", "Unidad 10", "Unit 10")}</span> · {TIT}</h1>
    <p>{L("Raons i proporcions entre segments, el teorema de Tales i el seu recíproc, la divisió d'un segment en parts iguals o proporcionals, triangles en posició de Tales, figures semblants i raó de semblança, criteris de semblança de triangles, càlcul d'altures i distàncies amb ombres i miralls, escales de plànols i mapes i la raó de les àrees i dels volums: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Razones y proporciones entre segmentos, el teorema de Tales y su recíproco, la división de un segmento en partes iguales o proporcionales, triángulos en posición de Tales, figuras semejantes y razón de semejanza, criterios de semejanza de triángulos, cálculo de alturas y distancias con sombras y espejos, escalas de planos y mapas y la razón de las áreas y de los volúmenes: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Ratios and proportions between segments, Thales' theorem and its converse, dividing a segment into equal or proportional parts, triangles in Thales position, similar figures and scale factors, similarity criteria for triangles, finding heights and distances with shadows and mirrors, scales on plans and maps and the ratio of areas and volumes: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>>
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
  <p>{L("Apunts de teoria · Unitat 10: Proporcionalitat. Teorema de Tales · 3r ESO", "Apuntes de teoría · Unidad 10: Proporcionalidad. Teorema de Tales · 3º ESO", "Theory notes · Unit 10: Proportionality. Thales' theorem · 3rd ESO")}</p>
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
_tema.VERSION = "20261031g10"
_tema.aplica_fitxer(OUT)
