import os, re, sys

# Genera materials/2eso/t2-decimals-fraccions.html. Ús: python3 _eines/apunts/2eso-t2/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html i l'estil de 1eso-t4/extra.css i 1eso-t5/extra.css;
# el contingut és a dec.py (2.1-2.4), fra.py (2.5-2.8) i pot.py (2.9-2.11), les ajudes a comu.py, el JavaScript a app.js
# (fet a partir dels de 1eso-t4 i 1eso-t5 i editat a mà; window.FM22 per a provar-lo al navegador) i l'estil propi a extra.css.
# Les asserts ck() de dec.py, fra.py i pot.py comproven els resultats escrits a mà.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t2-decimals-fraccions.html")
from comu import L, P, sec
from dec import s1, s2, s3, s4
from fra import s5, s6, s7, s8
from pot import s9, s10, s11

# ============================================================ muntatge
SECS = [
  (L('Nombres decimals', 'Números decimales', 'Decimal numbers'), s1),
  (L('Tipus de nombres decimals', 'Tipos de números decimales', 'Kinds of decimal numbers'), s2),
  (L('Sumar, restar i multiplicar decimals', 'Sumar, restar y multiplicar decimales', 'Adding, subtracting and multiplying decimals'), s3),
  (L('Dividir amb decimals', 'Dividir con decimales', 'Dividing with decimals'), s4),
  (L('Fraccions', 'Fracciones', 'Fractions'), s5),
  (L('Fraccions i decimals', 'Fracciones y decimales', 'Fractions and decimals'), s6),
  (L('Suma i resta de fraccions', 'Suma y resta de fracciones', 'Adding and subtracting fractions'), s7),
  (L('Multiplicació i divisió de fraccions', 'Multiplicación y división de fracciones', 'Multiplying and dividing fractions'), s8),
  (L('Potències de fraccions', 'Potencias de fracciones', 'Powers of fractions'), s9),
  (L('Operacions combinades', 'Operaciones combinadas', 'Mixed operations'), s10),
  (L('Problemes amb fraccions', 'Problemas con fracciones', 'Fraction word problems'), s11),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Decimals i fraccions · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 2 (Decimals i fraccions) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
assert 'Decimals i fraccions · FentMates' in head and 'content: "%"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css4 = open(os.path.join(HERE, '..', '1eso-t4', 'extra.css'), encoding='utf-8').read()
assert '/* quadrícula del 100 (percentatges) */' in css4
css5 = open(os.path.join(HERE, '..', '1eso-t5', 'extra.css'), encoding='utf-8').read()
assert css5.startswith('/* unitat 5: decimals i proporcionalitat */')
css = css4 + '\n' + css5 + '\n' + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">2.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 2", "Unidad 2", "Unit 2")}</span>
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
    <h1><span class="u">{L("Unitat 2", "Unidad 2", "Unit 2")}</span> · {L("Decimals i fraccions", "Decimales y fracciones", "Decimals and fractions")}</h1>
    <p>{L("Nombres decimals (valor posicional, aproximació, tipus i operacions), fraccions (equivalència, comparació i pas de fracció a decimal i de decimal a fracció, amb la fracció generatriu), operacions amb fraccions (suma, resta, multiplicació, divisió, potències i operacions combinades) i problemes amb fraccions: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Números decimales (valor posicional, aproximación, tipos y operaciones), fracciones (equivalencia, comparación y paso de fracción a decimal y de decimal a fracción, con la fracción generatriz), operaciones con fracciones (suma, resta, multiplicación, división, potencias y operaciones combinadas) y problemas con fracciones: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Decimal numbers (place value, rounding, kinds and operations), fractions (equivalence, comparing, and converting between fractions and decimals, including recurring decimals), operations with fractions (adding, subtracting, multiplying, dividing, powers and mixed operations) and fraction word problems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 2: Decimals i fraccions · 2n ESO", "Apuntes de teoría · Unidad 2: Decimales y fracciones · 2º ESO", "Theory notes · Unit 2: Decimals and fractions · 2nd ESO")}</p>
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
