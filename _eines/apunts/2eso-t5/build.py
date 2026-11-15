import os, re, sys

# Genera materials/2eso/t5-sistemes-equacions.html. Ús: python3 _eines/apunts/2eso-t5/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el contingut és a sis1.py (5.1-5.3)
# i sis2.py (5.4-5.7), les ajudes a comu.py, el JavaScript a app.js (el de ../3eso-t6, sense la classificació amb noms ni
# els sistemes amb denominadors, amb els entrenadors nous «troba la y» i «quin és el sistema?» i el qüestionari de 2n;
# window.FM25 per a provar-lo al navegador) i l'estil a extra.css. Les comprovacions cs(), ok() i same() (sympy) verifiquen
# les solucions escrites a mà.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t5-sistemes-equacions.html")
from comu import L, P, sec
from sis1 import s1, s2, s3
from sis2 import s4, s5, s6, s7

# ============================================================ muntatge
SECS = [
  (L('Equacions de primer grau amb dues incògnites', 'Ecuaciones de primer grado con dos incógnitas', 'First-degree equations in two unknowns'), s1),
  (L("Sistemes de dues equacions amb dues incògnites", 'Sistemas de dos ecuaciones con dos incógnitas', 'Systems of two equations in two unknowns'), s2),
  (L('Mètode de substitució', 'Método de sustitución', 'Substitution method'), s3),
  (L("Mètode d'igualació", 'Método de igualación', 'Equalisation method'), s4),
  (L('Mètode de reducció', 'Método de reducción', 'Elimination method'), s5),
  (L('Mètode gràfic', 'Método gráfico', 'Graphical method'), s6),
  (L("Problemes amb sistemes d'equacions", 'Problemas con sistemas de ecuaciones', 'Word problems with systems'), s7),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Sistemes d'equacions · FentMates</title>")
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "{x,y}";')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 5 (Sistemes d\'equacions) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
assert "Sistemes d'equacions · FentMates" in head and 'content: "{x,y}"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
assert 'NSEC = %d' % NS in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">5.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 5", "Unidad 5", "Unit 5")}</span>
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
    <h1><span class="u">{L("Unitat 5", "Unidad 5", "Unit 5")}</span> · {L("Sistemes d'equacions", "Sistemas de ecuaciones", "Simultaneous equations")}</h1>
    <p>{L("Equacions de primer grau amb dues incògnites i les seues solucions, què és i què representa un sistema de dues equacions amb dues incògnites, els mètodes de substitució, igualació, reducció i gràfic, quantes solucions pot tindre un sistema i problemes que es resolen amb sistemes: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Ecuaciones de primer grado con dos incógnitas y sus soluciones, qué es y qué representa un sistema de dos ecuaciones con dos incógnitas, los métodos de sustitución, igualación, reducción y gráfico, cuántas soluciones puede tener un sistema y problemas que se resuelven con sistemas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "First-degree equations in two unknowns and their solutions, what a system of two equations in two unknowns is and what it represents, the substitution, equalisation, elimination and graphical methods, how many solutions a system can have and word problems solved with systems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 5: Sistemes d'equacions · 2n ESO", "Apuntes de teoría · Unidad 5: Sistemas de ecuaciones · 2º ESO", "Theory notes · Unit 5: Simultaneous equations · 2nd ESO")}</p>
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
