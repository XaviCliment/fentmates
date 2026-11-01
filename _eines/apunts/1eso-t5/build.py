import os, re, sys

# Genera materials/1eso/t5-proporcionalitat-decimals.html. Ús: python3 _eines/apunts/1eso-t5/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html i l'estil de 1eso-t4/extra.css;
# el contingut és a dec.py (5.1-5.5) i prop.py (5.6-5.10), les ajudes a comu.py, el JavaScript a app.js i l'estil propi a extra.css.
# Les asserts ck() de dec.py i prop.py comproven els resultats escrits a mà.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t5-proporcionalitat-decimals.html")
from comu import L, P, sec
from dec import s1, s2, s3, s4, s5
from prop import s6, s7, s8, s9, s10

# ============================================================ muntatge
SECS = [
  (L('Nombres decimals', 'Números decimales', 'Decimal numbers'), s1),
  (L('Comparar, representar i aproximar decimals', 'Comparar, representar y aproximar decimales', 'Comparing, plotting and rounding decimals'), s2),
  (L('Sumar, restar i multiplicar decimals', 'Sumar, restar y multiplicar decimales', 'Adding, subtracting and multiplying decimals'), s3),
  (L('Dividir amb decimals', 'Dividir con decimales', 'Dividing with decimals'), s4),
  (L('Decimals i fraccions', 'Decimales y fracciones', 'Decimals and fractions'), s5),
  (L('Raons i proporcions', 'Razones y proporciones', 'Ratios and proportions'), s6),
  (L('Proporcionalitat directa', 'Proporcionalidad directa', 'Direct proportion'), s7),
  (L('Proporcionalitat inversa', 'Proporcionalidad inversa', 'Inverse proportion'), s8),
  (L('Percentatges', 'Porcentajes', 'Percentages'), s9),
  (L('Augments i disminucions percentuals', 'Aumentos y disminuciones porcentuales', 'Percentage increases and decreases'), s10),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Proporcionalitat i percentatges. Nombres decimals · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 5 (Proporcionalitat i percentatges. Nombres decimals) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
assert 'Nombres decimals · FentMates' in head and 'content: "%"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css4 = open(os.path.join(HERE, '..', '1eso-t4', 'extra.css'), encoding='utf-8').read()
assert '/* quadrícula del 100 (percentatges) */' in css4
css = css4 + '\n' + open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">5.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 5", "Unidad 5", "Unit 5")}</span>
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
    <h1><span class="u">{L("Unitat 5", "Unidad 5", "Unit 5")}</span> · {L("Proporcionalitat i percentatges. Nombres decimals", "Proporcionalidad y porcentajes. Números decimales", "Proportionality and percentages. Decimal numbers")}</h1>
    <p>{L("Nombres decimals (valor posicional, comparació, aproximació i operacions), relació entre decimals i fraccions, raons i proporcions, proporcionalitat directa i inversa amb la regla de tres, percentatges i augments i disminucions percentuals: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Números decimales (valor posicional, comparación, aproximación y operaciones), relación entre decimales y fracciones, razones y proporciones, proporcionalidad directa e inversa con la regla de tres, porcentajes y aumentos y disminuciones porcentuales: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Decimal numbers (place value, comparing, rounding and operations), decimals and fractions, ratios and proportions, direct and inverse proportion with the rule of three, percentages and percentage increases and decreases: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 5: Proporcionalitat i percentatges. Nombres decimals · 1r ESO", "Apuntes de teoría · Unidad 5: Proporcionalidad y porcentajes. Números decimales · 1º ESO", "Theory notes · Unit 5: Proportionality and percentages. Decimal numbers · 1st ESO")}</p>
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
_tema.VERSION = "20261101d5"
_tema.aplica_fitxer(OUT)
