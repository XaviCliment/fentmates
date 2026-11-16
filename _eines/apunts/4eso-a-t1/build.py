import os, re, sys

# Genera materials/4eso-a/t1-naturals-enters-fraccions.html. Ús: python3 _eines/apunts/4eso-a-t1/build.py
# 4t ESO Matemàtiques A, Unitat 1: Nombres naturals, enters i fraccionaris (11 apartats).
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html i els estils propis de 2eso-t1, 1eso-t4,
# 1eso-t5 i 2eso-t2. El contingut és a nat.py (1.1-1.4), fra4.py (1.5-1.8, que importa apartats de ../2eso-t2/fra.py i pot.py)
# pot4.py (1.9-1.10) i neg4.py (1.11); les ajudes, a eines4a.py.
# app.js té dues parts: la 1 és l'app.js de 2eso-t2 (fraccions, potències de fraccions, índex, idioma i qüestionari;
# window.FM4A1) i la 2, el de 2eso-t1 (naturals i enters: els ginys amb classe «wz»; window.FM4A1z). El qüestionari és a quiz.js.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/4eso-a/t1-naturals-enters-fraccions.html")
from eines4a import L, P, sec
from nat import s1, s2, s3, s4
from fra4 import s5, s6, s7, s8
from pot4 import s9, s10
from neg4 import s11

# ============================================================ muntatge
SECS = [
  (L('Els nombres naturals', 'Los números naturales', 'Natural numbers'), s1),
  (L('Potències, arrels i operacions combinades amb naturals', 'Potencias, raíces y operaciones combinadas con naturales', 'Powers, roots and mixed operations with natural numbers'), s2),
  (L('Els nombres enters. Valor absolut', 'Los números enteros. Valor absoluto', 'Integers. Absolute value'), s3),
  (L('Operacions combinades amb enters', 'Operaciones combinadas con enteros', 'Mixed operations with integers'), s4),
  (L('Fraccions. Fraccions equivalents', 'Fracciones. Fracciones equivalentes', 'Fractions. Equivalent fractions'), s5),
  (L('Operacions amb fraccions', 'Operaciones con fracciones', 'Operations with fractions'), s6),
  (L('Operacions combinades amb fraccions', 'Operaciones combinadas con fracciones', 'Mixed operations with fractions'), s7),
  (L('Problemes amb fraccions', 'Problemas con fracciones', 'Fraction word problems'), s8),
  (L('Potències amb base entera i racional', 'Potencias con base entera y racional', 'Powers with integer and rational bases'), s9),
  (L('Propietats de les potències', 'Propiedades de las potencias', 'Laws of powers'), s10),
  (L("Potències d'exponent zero i negatiu", 'Potencias de exponente cero y negativo', 'Zero and negative exponents'), s11),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Nombres naturals, enters i fraccionaris · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 1 (Nombres naturals, enters i fraccionaris) de 4t d\'ESO Matemàtiques A, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "±";')
assert 'Nombres naturals, enters i fraccionaris · FentMates' in head and 'content: "±"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
def rd(*p): return open(os.path.join(HERE, '..', *p), encoding='utf-8').read()
css = '\n'.join([rd('2eso-t1', 'extra.css'), rd('1eso-t4', 'extra.css'), rd('1eso-t5', 'extra.css'), rd('2eso-t2', 'extra.css'), rd('4eso-a-t1', 'extra.css')])
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
quiz = open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read().rstrip('\n')
assert js.count('/*QUIZ*/') == 1
js = js.replace('/*QUIZ*/', quiz)

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">1.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../4eso-a.html">{L("4t ESO A", "4º ESO A", "4th ESO A (Year 10)")}</a> / {L("Unitat 1", "Unidad 1", "Unit 1")}</span>
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
    <h1><span class="u">{L("Unitat 1", "Unidad 1", "Unit 1")}</span> · {L("Nombres naturals, enters i fraccionaris", "Números naturales, enteros y fraccionarios", "Natural numbers, integers and fractions")}</h1>
    <p>{L("Els nombres naturals i les operacions combinades amb potències i arrels, els nombres enters i el valor absolut, les operacions combinades amb enters, les fraccions (equivalència, simplificació i amplificació), les operacions i les operacions combinades amb fraccions, els problemes amb fraccions les potències amb base entera o racional i les seues propietats, i les potències d'exponent zero i negatiu: teoria explicada pas a pas, problemes resolts per nivells i eines interactives per a practicar.",
          "Los números naturales y las operaciones combinadas con potencias y raíces, los números enteros y el valor absoluto, las operaciones combinadas con enteros, las fracciones (equivalencia, simplificación y amplificación), las operaciones y las operaciones combinadas con fracciones, los problemas con fracciones las potencias con base entera o racional y sus propiedades, y las potencias de exponente cero y negativo: teoría explicada paso a paso, problemas resueltos por niveles y herramientas interactivas para practicar.",
          "Natural numbers and mixed operations with powers and roots, integers and absolute value, mixed operations with integers, fractions (equivalence, simplifying and scaling up), operations and mixed operations with fractions, fraction word problems, and powers with integer or rational bases and their laws, and zero and negative exponents: theory explained step by step, worked problems by level and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 1: Nombres naturals, enters i fraccionaris · 4t ESO Matemàtiques A", "Apuntes de teoría · Unidad 1: Números naturales, enteros y fraccionarios · 4º ESO Matemáticas A", "Theory notes · Unit 1: Natural numbers, integers and fractions · 4th ESO Maths A")}</p>
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
_tema.VERSION = "20261116a1"
_tema.aplica_fitxer(OUT)
