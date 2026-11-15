import os, re, sys

# Genera materials/2eso/t9-cossos-geometrics.html. Ús: python3 _eines/apunts/2eso-t9/build.py
# Adaptació a 2n ESO de ../3eso-t11 (sense troncs ni la Terra; problemes resolts, «Practica» i part del qüestionari nous).
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; l'estil propi és el de la
# unitat 8 de 3r (../3eso-t8/extra.css) i el de la unitat 9 de 3r (../3eso-t9/extra.css, figures) més extra.css; el JavaScript és a
# app.js (fet a partir del de la unitat 9: ajudes, G(), entrenadors, qüestionari i navegació, més els ginys de la unitat)
# i quiz.js. El contingut és a s12.py, s34.py, s56.py i s78.py (amb comu.py, solids.py i fig11.py): cada resultat es comprova amb ck().
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t9-cossos-geometrics.html")
sys.path.insert(0, HERE)
from comu import L, P
from s12 import s1, s2
from s34 import s3, s4
from s56 import s5, s6
from s78 import s7, s8
from comu import sec

SECS = [
  (L("Poliedres. Fórmula d'Euler. Poliedres regulars", 'Poliedros. Fórmula de Euler. Poliedros regulares', "Polyhedra. Euler's formula. Regular polyhedra"), s1),
  (L('Prismes: elements i àrea', 'Prismas: elementos y área', 'Prisms: parts and surface area'), s2),
  (L('Piràmides: elements i àrea', 'Pirámides: elementos y área', 'Pyramids: parts and surface area'), s3),
  (L('Cossos de revolució: cilindre i con', 'Cuerpos de revolución: cilindro y cono', 'Solids of revolution: cylinder and cone'), s4),
  (L("L'esfera i la seua àrea", 'La esfera y su área', 'The sphere and its surface area'), s5),
  (L('Volum. Prismes i cilindres', 'Volumen. Prismas y cilindros', 'Volume. Prisms and cylinders'), s6),
  (L('Volum de piràmides, cons i esferes', 'Volumen de pirámides, conos y esferas', 'Volume of pyramids, cones and spheres'), s7),
  (L('Cossos compostos i problemes', 'Cuerpos compuestos y problemas', 'Composite solids and problems'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Cossos geomètrics · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 9 (Cossos geomètrics. Àrees i volums) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "C+V=A+2";')
assert "Cossos geomètrics · FentMates" in head and 'content: "C+V=A+2"' in head
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
TIT = L("Cossos geomètrics. Àrees i volums", "Cuerpos geométricos. Áreas y volúmenes", "Solids. Surface area and volume")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 9", "Unidad 9", "Unit 9")}</span>
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
    <h1><span class="u">{L("Unitat 9", "Unidad 9", "Unit 9")}</span> · {TIT}</h1>
    <p>{L("Poliedres i fórmula d'Euler, els cinc poliedres regulars, prismes i piràmides, els cossos de revolució (cilindre, con i esfera) amb els seus desenvolupaments i àrees, unitats de volum i capacitat, el principi de Cavalieri, el volum de tots aquests cossos i problemes amb cossos compostos: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives (cossos que pots girar) per a practicar.",
          "Poliedros y fórmula de Euler, los cinco poliedros regulares, prismas y pirámides, los cuerpos de revolución (cilindro, cono y esfera) con sus desarrollos y áreas, unidades de volumen y capacidad, el principio de Cavalieri, el volumen de todos estos cuerpos y problemas con cuerpos compuestos: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas (cuerpos que puedes girar) para practicar.",
          "Polyhedra and Euler's formula, the five regular polyhedra, prisms and pyramids, solids of revolution (cylinder, cone and sphere) with their nets and surface areas, units of volume and capacity, Cavalieri's principle, the volume of all these solids and problems with composite solids: theory explained step by step, worked problems from easier to harder and interactive tools (solids you can rotate) to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 9: Cossos geomètrics. Àrees i volums · 2n ESO", "Apuntes de teoría · Unidad 9: Cuerpos geométricos. Áreas y volúmenes · 2º ESO", "Theory notes · Unit 9: Solids. Surface area and volume · 2nd ESO")}</p>
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
_tema.VERSION = "20261115e2u9"
_tema.aplica_fitxer(OUT)
