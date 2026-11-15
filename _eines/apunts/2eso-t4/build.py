import os, re, sys

# Genera materials/2eso/t4-equacions.html. Ús: python3 _eines/apunts/2eso-t4/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el contingut és a eq1.py (4.1-4.5,
# primer grau) i eq2.py (4.6-4.9, segon grau), les ajudes a comu.py, el JavaScript a app.js (el de ../3eso-t5 sense Ruffini,
# amb entrenadors nous de parèntesis, denominadors i problemes de segon grau i el qüestionari de 2n; window.FM24 per a
# provar-lo al navegador) i l'estil a extra.css. Les comprovacions ce() i chk() (sympy) verifiquen les solucions escrites a mà.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t4-equacions.html")
from comu import L, P, sec
from eq1 import s1, s2, s3, s4, s5
from eq2 import s6, s7, s8, s9

# ============================================================ muntatge
SECS = [
  (L('Equacions: elements i solucions', 'Ecuaciones: elementos y soluciones', 'Equations: parts and solutions'), s1),
  (L('Equacions de primer grau', 'Ecuaciones de primer grado', 'Linear equations'), s2),
  (L('Equacions amb parèntesis', 'Ecuaciones con paréntesis', 'Equations with brackets'), s3),
  (L('Equacions amb denominadors', 'Ecuaciones con denominadores', 'Equations with fractions'), s4),
  (L('Problemes amb equacions de primer grau', 'Problemas con ecuaciones de primer grado', 'Word problems with linear equations'), s5),
  (L('Equacions de segon grau incompletes', 'Ecuaciones de segundo grado incompletas', 'Incomplete quadratic equations'), s6),
  (L('Equacions de segon grau completes', 'Ecuaciones de segundo grado completas', 'Complete quadratic equations'), s7),
  (L('El discriminant', 'El discriminante', 'The discriminant'), s8),
  (L('Problemes amb equacions de segon grau', 'Problemas con ecuaciones de segundo grado', 'Word problems with quadratics'), s9),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Equacions de 1r i 2n grau · FentMates</title>')
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "x=?";')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 4 (Equacions de 1r i 2n grau) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
assert 'Equacions de 1r i 2n grau · FentMates' in head and 'content: "x=?"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
assert 'NSEC = %d' % NS in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">4.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 4", "Unidad 4", "Unit 4")}</span>
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
    <h1><span class="u">{L("Unitat 4", "Unidad 4", "Unit 4")}</span> · {L("Equacions de 1r i 2n grau", "Ecuaciones de 1.er y 2.º grado", "Linear and quadratic equations")}</h1>
    <p>{L("Equacions i identitats, equacions de primer grau (senzilles, amb parèntesis i amb denominadors), problemes que es resolen amb equacions de primer grau, equacions de segon grau incompletes i completes, el discriminant i problemes amb equacions de segon grau: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Ecuaciones e identidades, ecuaciones de primer grado (sencillas, con paréntesis y con denominadores), problemas que se resuelven con ecuaciones de primer grado, ecuaciones de segundo grado incompletas y completas, el discriminante y problemas con ecuaciones de segundo grado: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Equations and identities, linear equations (simple, with brackets and with fractions), word problems solved with linear equations, incomplete and complete quadratic equations, the discriminant and word problems with quadratics: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 4: Equacions de 1r i 2n grau · 2n ESO", "Apuntes de teoría · Unidad 4: Ecuaciones de 1.er y 2.º grado · 2º ESO", "Theory notes · Unit 4: Linear and quadratic equations · 2nd ESO")}</p>
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
_tema.VERSION = "20261115d2"
_tema.aplica_fitxer(OUT)
