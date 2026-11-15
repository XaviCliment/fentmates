import os, re, sys
from fractions import Fraction

# Genera materials/2eso/t1-naturals-enters.html. Ús: python3 _eines/apunts/2eso-t1/build.py
# Reaprofita els ginys de 1r ESO (unitats 2 i 3) i hi afig potències i arrels amb enters.
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/2eso/t1-naturals-enters.html")

def L(va, es, en):
    return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
def P(va, es, en): return '<p>' + L(va, es, en) + '</p>'
def P1(t): return '<p>' + t + '</p>'
def box(cls, title, body):
    head = f'<div class="bh">{title}</div>' if title else ''
    return f'<div class="box {cls}">{head}<div class="bb">{body}</div></div>\n'
def note(va, es, en, icon='💡'): return f'<div class="note"><p>{icon} {L(va, es, en)}</p></div>'
def ul(*items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
LV = {1: ('★☆☆', 'Nivell 1 · Bàsic', 'Nivel 1 · Básico', 'Level 1 · Basic'),
      2: ('★★☆', 'Nivell 2 · Intermedi', 'Nivel 2 · Intermedio', 'Level 2 · Intermediate'),
      3: ('★★★', 'Nivell 3 · Avançat', 'Nivel 3 · Avanzado', 'Level 3 · Advanced')}
def level(k, start, *probs):
    s, va, es, en = LV[k]
    st = f' start="{start}"' if start > 1 else ''
    return (f'<div class="lvl-h"><span class="stars">{s}</span><h3>{L(va, es, en)}</h3></div>\n'
            + box('ex', '', f'<ol class="ex-list"{st}>' + ''.join(probs) + '</ol>'))
def prob(q, *steps):
    return '<li><p class="prob-q">' + q + '</p><div class="steps">' + ''.join(f'<div class="step">{s}</div>' for s in steps) + '</div></li>\n'
def practice(items, sol):
    lis = ''.join(f'<li><span class="stars">{st}</span> {t}</li>' for st, t in items)
    return box('pr', '✍ ' + L('Practica', 'Practica', 'Practice'),
               f'<ol class="ex-list">{lis}</ol><details class="sol"><summary>{L("Mostra la solució", "Mostrar la solución", "Show the solution")}</summary><div>{sol}</div></details>')
def sec(i, title, body):
    return (f'\n<!-- ======================= 1.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">1.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def drill(kind, va, es, en):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin m" type="text" autocomplete="off" aria-label="resultat"></label><button class="btn drill-neg" type="button" data-a="neg" aria-label="±">±</button><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs, attr='b'):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-{attr}="{v}">{t}</button>' for v, t in pairs) + '</div>'
def nin(k, va, es, en, val, cls='s'):
    return f'<label>{L(va, es, en)} <input class="tin {cls}" type="text" data-k="{k}" value="{val}" autocomplete="off" aria-label="{k}"></label>'
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def hier(presets):
    keys = ''.join(f'<button type="button" data-ins="{k}">{k}</button>' for k in ['−', '·', ':', '^', '√', '(', ')', '[', ']'])
    q = ''.join(f'<button type="button" data-e="{e}">{e.replace("-", "−")}</button>' for e in presets)
    return f'''<div class="widget w-hier">
  <div class="wt">🧮 {L("Calculadora pas a pas", "Calculadora paso a paso", "Step-by-step calculator")}</div>
  <div class="wrow"><label>{L("Expressió", "Expresión", "Expression")} <input class="tin w" type="text" value="{presets[0].replace("-", "−")}" autocomplete="off" spellcheck="false" aria-label="expressió"></label></div>
  <div class="quick kp"><span class="ql">⌨</span>{keys}</div>
  <div class="quick"><span class="ql">⚡</span>{q}</div>
  <div class="hsteps"></div>
  <div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><span class="step-count"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''

def sub(va, es, en): return f'<h3 class="sub">{L(va, es, en)}</h3>\n'
def col(rows):
    # mètode de la columna: [(nombre, factor primer), …, (1, '')]
    return r'\[\begin{array}{r|l}' + r'\\'.join(f'{a}&{b}' for a, b in rows) + r'\end{array}\]'
MCM = r'\tri{mcm}{mcm}{lcm}'
MCD = r'\tri{MCD}{MCD}{gcd}'
DV = r'\tri{Div}{Div}{Div}'
ML = r'\tri{M}{M}{M}'


# ---------- aritmètica per a les solucions (evita errors de càlcul) ----------
def ev(e):
    s = re.sub(r'(\d+)', r'F(\1)', e.replace('·', '*').replace(':', '/').replace('[', '(').replace(']', ')'))
    v = eval(s, {'F': Fraction})
    assert v.denominator == 1, e
    return int(v)
def tx(e): return e.replace('·', r'\cdot ')
def eq(e): return tx(e) + '=' + str(ev(e))
def OP(x): return r'\text{op}(' + x + ')'

# ---------- recta numèrica estàtica ----------
def nline(lo, hi, pts=(), arcs='', h=78):
    X0, X1 = 40, 580
    x = lambda v: X0 + (v - lo) * (X1 - X0) / (hi - lo)
    s = (f'<div class="nline"><svg viewBox="0 0 620 {h}" role="img" aria-label="recta"><line class="sv-ax" x1="16" y1="40" x2="604" y2="40"/>'
         '<path class="sv-ax" d="M596 34 L606 40 L596 46" fill="none"/><path class="sv-ax" d="M24 34 L14 40 L24 46" fill="none"/>')
    for v in range(lo, hi + 1):
        c = 'sv-tb' if v == 0 else 'sv-t'
        s += f'<line class="sv-ax" x1="{x(v):.1f}" y1="33" x2="{x(v):.1f}" y2="47"/><text class="{c}" x="{x(v):.1f}" y="68" text-anchor="middle">{str(v).replace("-", "−")}</text>'
    s += arcs if isinstance(arcs, str) else arcs(x)
    for v in pts:
        s += f'<circle class="{"sv-neg" if v < 0 else "sv-pos" if v > 0 else "sv-dot"}" cx="{x(v):.1f}" cy="40" r="6"/>'
    return s + '</svg></div>'


# ---------- ginys (de 1r ESO, unitats 2 i 3) ----------
SGT = ('<div class="tbl-wrap"><table class="data sgtab"><thead><tr><th class="sop">·</th><th>+</th><th>−</th></tr></thead><tbody>'
       '<tr><th>+</th><td class="pos" data-c="pp">+</td><td class="neg" data-c="pn">−</td></tr>'
       '<tr><th>−</th><td class="neg" data-c="np">−</td><td class="pos" data-c="nn">+</td></tr></tbody></table></div>')

W_rel = f'''<div class="widget" id="w-rel">
  <div class="wt">🔗 {L("És múltiple? És divisor?", "¿Es múltiplo? ¿Es divisor?", "Multiple? Divisor?")}</div>
  <div class="wrow">{nin("a", "Nombre", "Número", "Number", "24")}<span class="op">:</span>{nin("b", "Divisor", "Divisor", "Divisor", "6")}</div>
  {quick([("24:6", "24 : 6"), ("30:4", "30 : 4"), ("91:7", "91 : 7"), ("45:1", "45 : 1"), ("9:9", "9 : 9"), ("0:5", "0 : 5"), ("100:8", "100 : 8"), ("143:11", "143 : 11")])}
  <div class="dots"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_mult = f'''<div class="widget" id="w-mult">
  <div class="wt">🟧 {L("Taula del 100: múltiples", "Tabla del 100: múltiplos", "Hundred square: multiples")}</div>
  <div class="wrow">{nin("n", "Múltiples de", "Múltiplos de", "Multiples of", "6")}{nin("m", "i de (opcional)", "y de (opcional)", "and of (optional)", "")}</div>
  {quick([("3", "3"), ("7", "7"), ("9", "9"), ("12", "12"), ("4,6", "4 i 6"), ("6,10", "6 i 10"), ("2,5", "2 i 5")])}
  <div class="hgrid"></div>
  <div class="legend"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_divs = f'''<div class="widget" id="w-divs">
  <div class="wt">🧱 {L("Buscador de divisors", "Buscador de divisores", "Divisor finder")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "36", "w")}</div>
  {quick([("12", "12"), ("24", "24"), ("36", "36"), ("48", "48"), ("17", "17"), ("60", "60"), ("100", "100"), ("360", "360")])}
  <div class="tbl-wrap dvt"></div>
  <div class="rects"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_crit = f'''<div class="widget" id="w-crit">
  <div class="wt">🔍 {L("Detector de divisibilitat", "Detector de divisibilidad", "Divisibility detector")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "4950", "w")}</div>
  {quick([("4950", "4950"), ("2715", "2715"), ("8261", "8261"), ("5481", "5481"), ("1001", "1001"), ("123456", "123 456"), ("98766", "98 766")])}
  <div class="cdig"></div>
  <div class="ccards"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_sieve = f'''<div class="widget" id="w-sieve">
  <div class="wt">🧹 {L("Garbell d'Eratòstenes fins a 100", "Criba de Eratóstenes hasta 100", "Sieve of Eratosthenes up to 100")}</div>
  <div class="sieve"></div>
  <div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><button class="btn" type="button" data-a="reset">↺</button></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_prime = f'''<div class="widget" id="w-prime">
  <div class="wt">🔎 {L("És primer?", "¿Es primo?", "Is it prime?")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "113", "w")}</div>
  {quick([("91", "91"), ("97", "97"), ("113", "113"), ("127", "127"), ("221", "221"), ("323", "323"), ("1001", "1001"), ("2027", "2027")])}
  <div class="tbl-wrap pvt2"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_fact = f'''<div class="widget" id="w-fact">
  <div class="wt">🌳 {L("Factoritzador", "Factorizador", "Factoriser")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "360", "w")}{seg([("col", L("Columna", "Columna", "Column")), ("tree", L("Arbre", "Árbol", "Tree"))], "col")}</div>
  {quick([("60", "60"), ("84", "84"), ("360", "360"), ("1050", "1050"), ("1001", "1001"), ("1024", "1024"), ("97", "97"), ("7560", "7560")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_coin = f'''<div class="widget" id="w-coin">
  <div class="wt">⏱ {L("Quan tornen a coincidir?", "¿Cuándo vuelven a coincidir?", "When do they coincide again?")}</div>
  <div class="wrow">{nin("a", "Cada", "Cada", "Every", "12")}{nin("b", "cada", "cada", "every", "18")}{nin("c", "cada (opcional)", "cada (opcional)", "every (optional)", "")}</div>
  <div class="wrow">{seg([("min", L("minuts", "minutos", "minutes")), ("d", L("dies", "días", "days")), ("s", L("segons", "segundos", "seconds"))], "min")}<label class="tstart">{L("Comencen a les", "Empiezan a las", "They start at")} <input class="tin s" type="text" data-k="t" value="8:00" autocomplete="off" aria-label="hora"></label></div>
  {quick([("12,18", "12 i 18"), ("4,6", "4 i 6"), ("15,20", "15 i 20"), ("8,12,15", "8, 12 i 15"), ("20,30,45", "20, 30 i 45")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_tile = f'''<div class="widget" id="w-tile">
  <div class="wt">🟦 {L("Rajoles quadrades el més grans possible", "Baldosas cuadradas lo más grandes posible", "The biggest possible square tiles")}</div>
  <div class="wrow">{nin("a", "Llarg (cm)", "Largo (cm)", "Length (cm)", "120")}<span class="op">×</span>{nin("b", "Ample (cm)", "Ancho (cm)", "Width (cm)", "84")}</div>
  {quick([("120,84", "120 × 84"), ("60,36", "60 × 36"), ("90,60", "90 × 60"), ("420,300", "420 × 300"), ("100,75", "100 × 75"), ("35,24", "35 × 24")])}
  <div class="tchips"></div>
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_gcd_mcm = f'''<div class="widget w-gcd" data-mode="mcm">
  <div class="wt">🧮 {L("Calculadora del mcm", "Calculadora del mcm", "LCM calculator")}</div>
  <div class="wrow">{nin("a", "a", "a", "a", "12")}{nin("b", "b", "b", "b", "18")}{nin("c", "c (opcional)", "c (opcional)", "c (optional)", "")}</div>
  <div class="wrow">{seg([("fac", L("Descomposició", "Descomposición", "Factorisation")), ("list", L("Llistes", "Listas", "Lists"))], "fac")}</div>
  {quick([("4,6", "4, 6"), ("12,18", "12, 18"), ("8,15", "8, 15"), ("6,18", "6, 18"), ("45,60", "45, 60"), ("12,30,42", "12, 30, 42"), ("40,36,30", "40, 36, 30")])}
  <div class="gout"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_gcd_mcd = f'''<div class="widget w-gcd" data-mode="mcd">
  <div class="wt">🧮 {L("Calculadora del MCD", "Calculadora del MCD", "GCD calculator")}</div>
  <div class="wrow">{nin("a", "a", "a", "a", "12")}{nin("b", "b", "b", "b", "18")}{nin("c", "c (opcional)", "c (opcional)", "c (optional)", "")}</div>
  <div class="wrow">{seg([("fac", L("Descomposició", "Descomposición", "Factorisation")), ("list", L("Llistes", "Listas", "Lists"))], "fac")}</div>
  {quick([("12,18", "12, 18"), ("16,24", "16, 24"), ("8,15", "8, 15"), ("6,18", "6, 18"), ("90,126", "90, 126"), ("48,60,72", "48, 60, 72"), ("60,72,84", "60, 72, 84")])}
  <div class="gout"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_ctx = f'''<div class="widget" id="w-ctx">
  <div class="wt">🌡 {L("De la situació al nombre enter", "De la situación al número entero", "From the situation to the integer")}</div>
  <div class="wrow">{seg([("temp", L("Temperatura", "Temperatura", "Temperature")), ("floor", L("Plantes", "Plantas", "Floors")), ("alt", L("Altitud", "Altitud", "Altitude")), ("money", L("Diners", "Dinero", "Money")), ("year", L("Anys", "Años", "Years"))], "temp")}</div>
  <div class="wrow">{nin("v", "Nombre enter", "Número entero", "Integer", "-6", "m")}</div>
  {quick([("temp|-6", "−6 °C"), ("floor|-3", L("3r soterrani", "3.er sótano", "3rd basement")), ("alt|432", "432 m"), ("alt|-120", "−120 m"), ("money|-25", L("dec 25 €", "debo 25 €", "owe €25")), ("year|-470", "470 a. C."), ("year|0", L("any 0?", "¿año 0?", "year 0?"))])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_line = f'''<div class="widget" id="w-line">
  <div class="wt">📏 {L("Representa i ordena", "Representa y ordena", "Plot and order")}</div>
  <div class="wrow"><label>{L("Nombres", "Números", "Numbers")} <input class="tin w" type="text" data-k="v" value="−2, 0, 4, −1, 8, −3, −7, 1" autocomplete="off" spellcheck="false" aria-label="nombres"></label>{seg([("asc", L("menor → major", "menor → mayor", "smallest → largest")), ("desc", L("major → menor", "mayor → menor", "largest → smallest"))], "asc")}</div>
  {quick([("−7, 3, 1, −4, 6, −5, −2, 0", "−7, 3, 1, −4…"), ("−7, 0, 1, −1, 8, −4, −9, 3", "−7, 0, 1, −1…"), ("−8, −9", "−8 ? −9"), ("−6, 6", "−6 ? 6"), ("−15, −51", "−15 ? −51"), ("−120, 35, −300, 0, 210", "−120, 35, −300…")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_abs = f'''<div class="widget" id="w-abs">
  <div class="wt">↔ {L("Valor absolut i oposat", "Valor absoluto y opuesto", "Absolute value and opposite")}</div>
  <div class="wrow">{nin("a", "Nombre enter", "Número entero", "Integer", "-5", "m")}</div>
  {quick([("-5", "−5"), ("8", "8"), ("-23", "−23"), ("0", "0"), ("-100", "−100"), ("18", "18")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_add = f'''<div class="widget" id="w-add">
  <div class="wt">➕ {L("Sumes i restes en la recta", "Sumas y restas en la recta", "Adding and subtracting on the number line")}</div>
  <div class="wrow">{nin("a", "Partim de", "Partimos de", "Start at", "-2")}{seg([("+", "+"), ("-", "−")], "+")}{nin("b", "Nombre", "Número", "Number", "6")}</div>
  {quick([("-2|+|6", "−2 + 6"), ("5|-|7", "5 − 7"), ("-8|-|9", "−8 − 9"), ("-3|+|-4", "−3 + (−4)"), ("4|-|-6", "4 − (−6)"), ("-5|+|5", "−5 + 5")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_par = f'''<div class="widget" id="w-par">
  <div class="wt">🧹 {L("Lleva els parèntesis", "Quita los paréntesis", "Remove the brackets")}</div>
  <div class="wrow"><label>{L("Expressió", "Expresión", "Expression")} <input class="tin w" type="text" value="−(+4) + (−8) − (−6) + 4 − 1" autocomplete="off" spellcheck="false" aria-label="expressió"></label></div>
  <div class="quick"><span class="ql">⚡</span>{"".join(f'<button type="button" data-e="{e}">{e}</button>' for e in ["(−6) + (−3)", "(+7) + (−4)", "3 − (−1)", "−(−5) + 3", "(−2) − (+3) + (−6)", "−(−3) + (−1) − (+3) − (−8)", "12 − 25 + 3 − 8 − (−6)"])}</div>
  <div class="pchips"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_sign = f'''<div class="widget" id="w-sign">
  <div class="wt">✖ {L("La regla dels signes", "La regla de los signos", "The sign rule")}</div>
  <div class="wrow">{nin("a", "a", "a", "a", "-6")}{seg([("·", "·"), (":", ":")], "·")}{nin("b", "b", "b", "b", "4")}</div>
  {quick([("-6|·|4", "(−6)·(+4)"), ("-5|·|-7", "(−5)·(−7)"), ("3|·|-8", "(+3)·(−8)"), ("-36|:|9", "(−36):(+9)"), ("-48|:|-8", "(−48):(−8)"), ("42|:|-7", "(+42):(−7)"), ("-7|:|2", "(−7):(+2)")])}
  {SGT}
  <div class="info" aria-live="polite"></div>
</div>'''

W_powz = f'''<div class="widget" id="w-powz">
  <div class="wt">⚡ {L("Potències d'enters", "Potencias de enteros", "Powers of integers")}</div>
  <div class="wrow">{nin("b", "Base", "Base", "Base", "-2")}{nin("n", "Exponent", "Exponente", "Exponent", "5")}</div>
  {quick([("-2|5", "(−2)⁵"), ("-2|4", "(−2)⁴"), ("-3|3", "(−3)³"), ("-1|7", "(−1)⁷"), ("-1|10", "(−1)¹⁰"), ("-10|6", "(−10)⁶"), ("4|3", "4³"), ("-7|0", "(−7)⁰")])}
  <div class="pz"></div>
  <div class="info" aria-live="polite"></div>
</div>'''
W_rootz = f'''<div class="widget" id="w-rootz">
  <div class="wt">√ {L("Arrel quadrada d'un enter", "Raíz cuadrada de un entero", "Square root of an integer")}</div>
  <div class="wrow">{nin("a", "Radicand", "Radicando", "Radicand", "50")}</div>
  {quick([("49", "49"), ("50", "50"), ("144", "144"), ("200", "200"), ("-16", "−16"), ("0", "0"), ("1000", "1000")])}
  <div class="rz"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

# ============================================================ 1.1 Els nombres naturals
s1 = box('def', L('Definició: nombres naturals', 'Definición: números naturales', 'Definition: natural numbers'),
  P(r"Els <strong>nombres naturals</strong> són els que fem servir per a <strong>comptar</strong> i per a <strong>ordenar</strong>. El conjunt dels naturals es representa amb la lletra \(\mathbb{N}\):",
    r"Los <strong>números naturales</strong> son los que usamos para <strong>contar</strong> y para <strong>ordenar</strong>. El conjunto de los naturales se representa con la letra \(\mathbb{N}\):",
    r"<strong>Natural numbers</strong> are the numbers we use to <strong>count</strong> and to <strong>put things in order</strong>. The set of natural numbers is written with the letter \(\mathbb{N}\):")
  + r'\[\mathbb{N}=\{0,\ 1,\ 2,\ 3,\ 4,\ 5,\ \ldots\}\]'
  + ul(L(r"Tenen un <strong>primer</strong> element, el \(0\), però no un últim: després de cada natural sempre hi ha el <strong>següent</strong> (\(n+1\)). Hi ha infinits naturals.",
         r"Tienen un <strong>primer</strong> elemento, el \(0\), pero no un último: después de cada natural siempre está el <strong>siguiente</strong> (\(n+1\)). Hay infinitos naturales.",
         r"They have a <strong>first</strong> element, \(0\), but no last one: every natural number has a <strong>next</strong> one (\(n+1\)). There are infinitely many."),
       L(r"Es representen en una semirecta, ordenats de menor a major i separats sempre per la mateixa distància.",
         r"Se representan en una semirrecta, ordenados de menor a mayor y separados siempre por la misma distancia.",
         r"They are shown on a half-line, in increasing order and always the same distance apart."))
  + nline(0, 10, pts=range(0, 11)))
s1 += box('prop', L('Operacions amb nombres naturals', 'Operaciones con números naturales', 'Operations with natural numbers'),
  P(r"Si sumem o multipliquem dos naturals, el resultat <strong>sempre</strong> és un natural. En canvi, la resta i la divisió no sempre es poden fer dins de \(\mathbb{N}\):",
    r"Si sumamos o multiplicamos dos naturales, el resultado <strong>siempre</strong> es un natural. En cambio, la resta y la división no siempre se pueden hacer dentro de \(\mathbb{N}\):",
    r"If we add or multiply two natural numbers, the result is <strong>always</strong> a natural number. Subtraction and division, however, can't always be done inside \(\mathbb{N}\):")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Operació', 'Operación', 'Operation') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th><th>' + L('Sempre dona un natural?', '¿Siempre da un natural?', 'Always natural?') + '</th></tr></thead><tbody>'
  + r'<tr><td>' + L('Suma', 'Suma', 'Addition') + r'</td><td>\(7+5=12\)</td><td>✅</td></tr>'
  + r'<tr><td>' + L('Multiplicació', 'Multiplicación', 'Multiplication') + r'</td><td>\(7\cdot5=35\)</td><td>✅</td></tr>'
  + r'<tr><td>' + L('Resta', 'Resta', 'Subtraction') + r'</td><td>\(7-5=2\quad\) ' + L('però', 'pero', 'but') + r' \(\quad5-7=\ ?\)</td><td>❌ ' + L('(ho resoldrem amb els enters)', '(lo resolveremos con los enteros)', '(integers will solve it)') + r'</td></tr>'
  + r'<tr><td>' + L('Divisió', 'División', 'Division') + r'</td><td>\(35:5=7\quad\) ' + L('però', 'pero', 'but') + r' \(\quad 7:5=\ ?\)</td><td>❌ ' + L('(només si és exacta)', '(solo si es exacta)', '(only if exact)') + r'</td></tr>'
  + '</tbody></table></div>'
  + P(r"<strong>Propietats.</strong> La suma i la multiplicació són <strong>commutatives</strong> (\(a+b=b+a\), \(a\cdot b=b\cdot a\)) i <strong>associatives</strong> (\((a+b)+c=a+(b+c)\)); el \(0\) és l'element neutre de la suma i l'\(1\), el del producte. A més, la multiplicació és <strong>distributiva</strong> respecte de la suma i la resta: \(a\cdot(b\pm c)=a\cdot b\pm a\cdot c\).",
      r"<strong>Propiedades.</strong> La suma y la multiplicación son <strong>conmutativas</strong> (\(a+b=b+a\), \(a\cdot b=b\cdot a\)) y <strong>asociativas</strong> (\((a+b)+c=a+(b+c)\)); el \(0\) es el elemento neutro de la suma y el \(1\), el del producto. Además, la multiplicación es <strong>distributiva</strong> respecto de la suma y la resta: \(a\cdot(b\pm c)=a\cdot b\pm a\cdot c\).",
      r"<strong>Properties.</strong> Addition and multiplication are <strong>commutative</strong> (\(a+b=b+a\), \(a\cdot b=b\cdot a\)) and <strong>associative</strong> (\((a+b)+c=a+(b+c)\)); \(0\) is the identity for addition and \(1\) for multiplication. Multiplication is also <strong>distributive</strong> over addition and subtraction: \(a\cdot(b\pm c)=a\cdot b\pm a\cdot c\).")
  + note(r"La distributiva ajuda a calcular de cap: \(7\cdot99=7\cdot(100-1)=700-7=693\).",
         r"La distributiva ayuda a calcular de cabeza: \(7\cdot99=7\cdot(100-1)=700-7=693\).",
         r"The distributive property helps with mental maths: \(7\cdot99=7\cdot(100-1)=700-7=693\)."))
s1 += box('def', L('La divisió entera', 'La división entera', 'Division with remainder'),
  P(r"Quan dividim dos naturals obtenim un <strong>quocient</strong> \(q\) i un <strong>residu</strong> \(r\). Sempre es compleix la <strong>prova de la divisió</strong>:",
    r"Cuando dividimos dos naturales obtenemos un <strong>cociente</strong> \(q\) y un <strong>resto</strong> \(r\). Siempre se cumple la <strong>prueba de la división</strong>:",
    r"When we divide two natural numbers we get a <strong>quotient</strong> \(q\) and a <strong>remainder</strong> \(r\). The <strong>division check</strong> always holds:")
  + r'\[\underbrace{D}_{\tri{dividend}{dividendo}{dividend}}=\underbrace{d}_{\tri{divisor}{divisor}{divisor}}\cdot\underbrace{q}_{\tri{quocient}{cociente}{quotient}}+\underbrace{r}_{\tri{residu}{resto}{remainder}}\qquad\text{amb}\quad 0\le r\lt d\]'.replace(r'\text{amb}', r'\tri{amb}{con}{with}')
  + P(r"Si el residu és \(0\), la divisió és <strong>exacta</strong>. Per exemple, \(247:12\) dona \(q=20\) i \(r=7\), perquè \(12\cdot20+7=247\) i \(7<12\).",
      r"Si el resto es \(0\), la división es <strong>exacta</strong>. Por ejemplo, \(247:12\) da \(q=20\) y \(r=7\), porque \(12\cdot20+7=247\) y \(7<12\).",
      r"If the remainder is \(0\), the division is <strong>exact</strong>. For example, \(247:12\) gives \(q=20\) and \(r=7\), because \(12\cdot20+7=247\) and \(7<12\).")
  + W_rel)
s1 += level(1, 1,
  prob(L(r"En una divisió el divisor és 15, el quocient 23 i el residu 9. Quin és el dividend?", r"En una división el divisor es 15, el cociente 23 y el resto 9. ¿Cuál es el dividendo?", r"In a division the divisor is 15, the quotient 23 and the remainder 9. What is the dividend?"),
       r'\[D=d\cdot q+r=15\cdot23+9=345+9=\boxed{354}\]'),
  prob(L(r"Calcula de cap amb la propietat distributiva: \(\ 12\cdot15+12\cdot5\ \) i \(\ 35\cdot102\).", r"Calcula de cabeza con la propiedad distributiva: \(\ 12\cdot15+12\cdot5\ \) y \(\ 35\cdot102\).", r"Use the distributive property to work out mentally: \(\ 12\cdot15+12\cdot5\ \) and \(\ 35\cdot102\)."),
       r'\[12\cdot15+12\cdot5=12\cdot(15+5)=12\cdot20=\boxed{240}\qquad 35\cdot102=35\cdot100+35\cdot2=\boxed{3570}\]'))
s1 += level(2, 3,
  prob(L(r"Tenim 230 ous i els posem en oueres de 12. Quantes oueres omplim? Quants ous sobren? Quantes oueres calen per a guardar-los tots?", r"Tenemos 230 huevos y los ponemos en hueveras de 12. ¿Cuántas hueveras llenamos? ¿Cuántos huevos sobran? ¿Cuántas hueveras hacen falta para guardarlos todos?", r"We have 230 eggs and put them into boxes of 12. How many boxes do we fill? How many eggs are left over? How many boxes do we need for all of them?"),
       r'\[230=12\cdot19+2\]',
       P(r"Omplim \(\boxed{19}\) oueres i sobren \(\boxed{2}\) ous. Per a guardar-los tots en calen \(19+1=\boxed{20}\).", r"Llenamos \(\boxed{19}\) hueveras y sobran \(\boxed{2}\) huevos. Para guardarlos todos hacen falta \(19+1=\boxed{20}\).", r"We fill \(\boxed{19}\) boxes and \(\boxed{2}\) eggs are left over. To store them all we need \(19+1=\boxed{20}\) boxes.")))
s1 += practice([
  ('★', L(r"a) Calcula el quocient i el residu de \(1000:37\) i fes la prova. b) Indica si el resultat és un nombre natural: \(7-12\), \(\ 15\cdot4\), \(\ 20:6\), \(\ 6:3+1\).", r"a) Calcula el cociente y el resto de \(1000:37\) y haz la prueba. b) Indica si el resultado es un número natural: \(7-12\), \(\ 15\cdot4\), \(\ 20:6\), \(\ 6:3+1\).", r"a) Find the quotient and remainder of \(1000:37\) and check it. b) Is the result a natural number? \(7-12\), \(\ 15\cdot4\), \(\ 20:6\), \(\ 6:3+1\).")),
  ('★★', L(r"c) En una divisió el divisor és 8 i el quocient 14. Quins valors pot tindre el dividend?", r"c) En una división el divisor es 8 y el cociente 14. ¿Qué valores puede tener el dividendo?", r"c) In a division the divisor is 8 and the quotient 14. What values can the dividend take?"))],
  P(r"a) \(1000=37\cdot27+1\): quocient 27, residu 1. &nbsp; b) No (\(-5\)); sí (60); no (no és exacta); sí (3).", r"a) \(1000=37\cdot27+1\): cociente 27, resto 1. &nbsp; b) No (\(-5\)); sí (60); no (no es exacta); sí (3).", r"a) \(1000=37\cdot27+1\): quotient 27, remainder 1. &nbsp; b) No (\(-5\)); yes (60); no (not exact); yes (3).")
  + P(r"c) \(D=8\cdot14+r\) amb \(r=0,1,\ldots,7\): de \(112\) a \(119\).", r"c) \(D=8\cdot14+r\) con \(r=0,1,\ldots,7\): de \(112\) a \(119\).", r"c) \(D=8\cdot14+r\) with \(r=0,1,\ldots,7\): from \(112\) to \(119\)."))

# ============================================================ 1.2 Múltiples i divisors
s2 = box('def', L('Múltiples i divisors', 'Múltiplos y divisores', 'Multiples and divisors'),
  P(r"Si la divisió \(a:b\) és <strong>exacta</strong> (residu 0), és a dir, si \(a=b\cdot k\) per a algun natural \(k\), diem que:",
    r"Si la división \(a:b\) es <strong>exacta</strong> (resto 0), es decir, si \(a=b\cdot k\) para algún natural \(k\), decimos que:",
    r"If the division \(a:b\) is <strong>exact</strong> (remainder 0), that is, if \(a=b\cdot k\) for some natural number \(k\), we say that:")
  + ul(L(r"\(a\) <strong>és múltiple de</strong> \(b\) (o \(a\) és divisible per \(b\))", r"\(a\) <strong>es múltiplo de</strong> \(b\) (o \(a\) es divisible por \(b\))", r"\(a\) <strong>is a multiple of</strong> \(b\) (or \(a\) is divisible by \(b\))"),
       L(r"\(b\) <strong>és divisor de</strong> \(a\) (o \(b\) divideix \(a\))", r"\(b\) <strong>es divisor de</strong> \(a\) (o \(b\) divide a \(a\))", r"\(b\) <strong>is a divisor of</strong> \(a\) (or \(b\) divides \(a\))"))
  + r'\[42=6\cdot7\quad\Longrightarrow\quad \tri{42 és múltiple de 6 i de 7;\ \ 6 i 7 són divisors de 42}{42 es múltiplo de 6 y de 7;\ \ 6 y 7 son divisores de 42}{42 is a multiple of 6 and 7;\ \ 6 and 7 are divisors of 42}\]')
s2 += box('prop', L('Propietats', 'Propiedades', 'Properties'),
  ul(L(r"Els múltiples de \(n\) s'obtenen multiplicant-lo per \(0,1,2,3\ldots\): \(\ \dot{7}=\{0,\,7,\,14,\,21,\,28,\ldots\}\). Tot nombre té <strong>infinits</strong> múltiples i el \(0\) és múltiple de tots.",
         r"Los múltiplos de \(n\) se obtienen multiplicándolo por \(0,1,2,3\ldots\): \(\ \dot{7}=\{0,\,7,\,14,\,21,\,28,\ldots\}\). Todo número tiene <strong>infinitos</strong> múltiplos y el \(0\) es múltiplo de todos.",
         r"The multiples of \(n\) are found by multiplying it by \(0,1,2,3\ldots\): \(\ \dot{7}=\{0,\,7,\,14,\,21,\,28,\ldots\}\). Every number has <strong>infinitely many</strong> multiples, and \(0\) is a multiple of every number."),
       L(r"Els divisors d'un nombre són <strong>finits</strong>: \(\ \text{Div}(18)=\{1,\,2,\,3,\,6,\,9,\,18\}\). L'\(1\) és divisor de tots els nombres i tot nombre és divisor (i múltiple) d'ell mateix.",
         r"Los divisores de un número son <strong>finitos</strong>: \(\ \text{Div}(18)=\{1,\,2,\,3,\,6,\,9,\,18\}\). El \(1\) es divisor de todos los números y todo número es divisor (y múltiplo) de sí mismo.",
         r"A number has <strong>finitely many</strong> divisors: \(\ \text{Div}(18)=\{1,\,2,\,3,\,6,\,9,\,18\}\). \(1\) divides every number and every number is a divisor (and a multiple) of itself."),
       L(r"Per a trobar tots els divisors, dividim entre \(1,2,3\ldots\) i els anem traient <strong>per parelles</strong>: \(18=1\cdot18=2\cdot9=3\cdot6\). Parem quan el quocient és menor o igual que el divisor.",
         r"Para encontrar todos los divisores, dividimos entre \(1,2,3\ldots\) y los vamos sacando <strong>por parejas</strong>: \(18=1\cdot18=2\cdot9=3\cdot6\). Paramos cuando el cociente es menor o igual que el divisor.",
         r"To find all the divisors, divide by \(1,2,3\ldots\) and take them <strong>in pairs</strong>: \(18=1\cdot18=2\cdot9=3\cdot6\). Stop when the quotient is less than or equal to the divisor.")))
s2 += W_mult + drill('mult', 'Entrena: múltiples', 'Entrena: múltiplos', 'Train: multiples')
s2 += W_divs + drill('divs', 'Entrena: divisors', 'Entrena: divisores', 'Train: divisors')
s2 += level(1, 1,
  prob(L(r"Escriu els múltiples de \(15\) compresos entre \(100\) i \(200\).", r"Escribe los múltiplos de \(15\) comprendidos entre \(100\) y \(200\).", r"Write the multiples of \(15\) between \(100\) and \(200\)."),
       P(r"\(100=15\cdot6+10\): el primer és \(15\cdot7=105\). Després anem sumant 15:", r"\(100=15\cdot6+10\): el primero es \(15\cdot7=105\). Después vamos sumando 15:", r"\(100=15\cdot6+10\): the first is \(15\cdot7=105\). Then keep adding 15:"),
       r'\[\boxed{105,\ 120,\ 135,\ 150,\ 165,\ 180,\ 195}\]'))
s2 += level(2, 2,
  prob(L(r"Troba tots els divisors de \(60\).", r"Halla todos los divisores de \(60\).", r"Find all the divisors of \(60\)."),
       r'\[60=1\cdot60=2\cdot30=3\cdot20=4\cdot15=5\cdot12=6\cdot10\]',
       r'\[\text{Div}(60)=\boxed{\{1,2,3,4,5,6,10,12,15,20,30,60\}}\]'))
s2 += practice([
  ('★', L(r"a) Escriu els cinc primers múltiples no nuls de 7 i de 12. b) Escriu tots els divisors de 24, 45 i 17.", r"a) Escribe los cinco primeros múltiplos no nulos de 7 y de 12. b) Escribe todos los divisores de 24, 45 y 17.", r"a) Write the first five non-zero multiples of 7 and 12. b) Write all the divisors of 24, 45 and 17.")),
  ('★★', L(r"c) Vertader o fals: 48 és múltiple de 6; 5 és múltiple de 15; 1 és divisor de qualsevol nombre; 0 és múltiple de 9.", r"c) Verdadero o falso: 48 es múltiplo de 6; 5 es múltiplo de 15; 1 es divisor de cualquier número; 0 es múltiplo de 9.", r"c) True or false: 48 is a multiple of 6; 5 is a multiple of 15; 1 divides any number; 0 is a multiple of 9."))],
  P(r"a) 7, 14, 21, 28, 35; &nbsp; 12, 24, 36, 48, 60. &nbsp; b) \(\text{Div}(24)=\{1,2,3,4,6,8,12,24\}\), \(\text{Div}(45)=\{1,3,5,9,15,45\}\), \(\text{Div}(17)=\{1,17\}\).", r"a) 7, 14, 21, 28, 35; &nbsp; 12, 24, 36, 48, 60. &nbsp; b) \(\text{Div}(24)=\{1,2,3,4,6,8,12,24\}\), \(\text{Div}(45)=\{1,3,5,9,15,45\}\), \(\text{Div}(17)=\{1,17\}\).", r"a) 7, 14, 21, 28, 35; &nbsp; 12, 24, 36, 48, 60. &nbsp; b) \(\text{Div}(24)=\{1,2,3,4,6,8,12,24\}\), \(\text{Div}(45)=\{1,3,5,9,15,45\}\), \(\text{Div}(17)=\{1,17\}\).")
  + P(r"c) V (\(6\cdot8\)); F (5 és <em>divisor</em> de 15); V; V (\(9\cdot0=0\)).", r"c) V (\(6\cdot8\)); F (5 es <em>divisor</em> de 15); V; V (\(9\cdot0=0\)).", r"c) T (\(6\cdot8\)); F (5 is a <em>divisor</em> of 15); T; T (\(9\cdot0=0\))."))

# ============================================================ 1.3 Criteris de divisibilitat i nombres primers
CRIT = [('2', 'Acaba en 0, 2, 4, 6 o 8.', 'Acaba en 0, 2, 4, 6 u 8.', 'It ends in 0, 2, 4, 6 or 8.', r'3\,58\mathbf{4}'),
        ('3', 'La suma de les xifres és múltiple de 3.', 'La suma de sus cifras es múltiplo de 3.', 'The sum of its digits is a multiple of 3.', r'471:\ 4+7+1=12'),
        ('5', 'Acaba en 0 o en 5.', 'Acaba en 0 o en 5.', 'It ends in 0 or 5.', r'1\,23\mathbf{5}'),
        ('9', 'La suma de les xifres és múltiple de 9.', 'La suma de sus cifras es múltiplo de 9.', 'The sum of its digits is a multiple of 9.', r'5\,481:\ 5+4+8+1=18'),
        ('10', 'Acaba en 0.', 'Acaba en 0.', 'It ends in 0.', r'7\,49\mathbf{0}'),
        ('11', "La diferència entre la suma de les xifres de lloc senar i la de lloc parell és 0 o múltiple d'11.", 'La diferencia entre la suma de las cifras de lugar impar y la de lugar par es 0 o múltiplo de 11.', 'The difference between the sum of the digits in odd places and in even places is 0 or a multiple of 11.', r'8\,294:\ (8+9)-(2+4)=11')]
s3 = box('def', L('Criteris de divisibilitat', 'Criterios de divisibilidad', 'Divisibility rules'),
  P(r"Ens permeten saber si un nombre és divisible per un altre <strong>sense fer la divisió</strong>.", r"Nos permiten saber si un número es divisible por otro <strong>sin hacer la división</strong>.", r"They tell us whether a number is divisible by another <strong>without dividing</strong>.")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Per', 'Por', 'By') + '</th><th>' + L('Un nombre és divisible si…', 'Un número es divisible si…', 'A number is divisible if…') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td><strong>{k}</strong></td><td class="l">{L(va, es, en)}</td><td>\\({e}\\)</td></tr>' for k, va, es, en, e in CRIT)
  + '</tbody></table></div>')
s3 += W_crit + drill('crit', 'Entrena: criteris', 'Entrena: criterios', 'Train: divisibility rules')
s3 += box('def', L('Nombres primers i compostos', 'Números primos y compuestos', 'Prime and composite numbers'),
  ul(L(r"Un nombre és <strong>primer</strong> si només té dos divisors: l'\(1\) i ell mateix. Per exemple, \(2,\ 3,\ 5,\ 7,\ 11,\ 13\ldots\)", r"Un número es <strong>primo</strong> si solo tiene dos divisores: el \(1\) y él mismo. Por ejemplo, \(2,\ 3,\ 5,\ 7,\ 11,\ 13\ldots\)", r"A number is <strong>prime</strong> if it has exactly two divisors: \(1\) and itself. For example, \(2,\ 3,\ 5,\ 7,\ 11,\ 13\ldots\)"),
       L(r"Un nombre és <strong>compost</strong> si té més de dos divisors: \(12\) té els divisors \(1,2,3,4,6,12\).", r"Un número es <strong>compuesto</strong> si tiene más de dos divisores: \(12\) tiene los divisores \(1,2,3,4,6,12\).", r"A number is <strong>composite</strong> if it has more than two divisors: \(12\) has divisors \(1,2,3,4,6,12\)."),
       L(r"L'\(1\) no és ni primer ni compost (només té un divisor). El \(2\) és l'únic primer parell.", r"El \(1\) no es ni primo ni compuesto (solo tiene un divisor). El \(2\) es el único primo par.", r"\(1\) is neither prime nor composite (it has only one divisor). \(2\) is the only even prime."))
  + P(r"Per a saber si un nombre és primer, el dividim entre els primers \(2,3,5,7,11\ldots\) Si cap divisió és exacta i arribem a un quocient menor que el divisor, és primer.", r"Para saber si un número es primo, lo dividimos entre los primos \(2,3,5,7,11\ldots\) Si ninguna división es exacta y llegamos a un cociente menor que el divisor, es primo.", r"To check whether a number is prime, divide it by the primes \(2,3,5,7,11\ldots\) If no division is exact and the quotient becomes smaller than the divisor, it is prime."))
s3 += W_sieve + W_prime
s3 += level(1, 1,
  prob(L(r"Sense dividir, digues si \(4455\) és divisible per 2, 3, 5, 9, 10 i 11.", r"Sin dividir, di si \(4455\) es divisible por 2, 3, 5, 9, 10 y 11.", r"Without dividing, say whether \(4455\) is divisible by 2, 3, 5, 9, 10 and 11."),
       P(r"Acaba en 5: no és divisible per 2 ni per 10, però sí per 5. Les xifres sumen \(4+4+5+5=18\): és divisible per 3 i per 9. Criteri de l'11: \((4+5)-(4+5)=0\), sí.", r"Acaba en 5: no es divisible por 2 ni por 10, pero sí por 5. Las cifras suman \(4+4+5+5=18\): es divisible por 3 y por 9. Criterio del 11: \((4+5)-(4+5)=0\), sí.", r"It ends in 5: not divisible by 2 or 10, but divisible by 5. The digits add up to \(4+4+5+5=18\): divisible by 3 and 9. Rule for 11: \((4+5)-(4+5)=0\), yes."),
       r'\[4455\ \tri{és divisible per}{es divisible por}{is divisible by}\ \boxed{3,\ 5,\ 9,\ 11}\]'))
s3 += level(2, 2,
  prob(L(r"Quines xifres poden anar en el lloc de \(\square\) perquè \(4\square7\) siga múltiple de 3?", r"¿Qué cifras pueden ir en el lugar de \(\square\) para que \(4\square7\) sea múltiplo de 3?", r"Which digits can replace \(\square\) so that \(4\square7\) is a multiple of 3?"),
       P(r"La suma \(4+\square+7=11+\square\) ha de ser 12, 15 o 18:", r"La suma \(4+\square+7=11+\square\) tiene que ser 12, 15 o 18:", r"The sum \(4+\square+7=11+\square\) must be 12, 15 or 18:"),
       r'\[\square=\boxed{1,\ 4,\ 7}\quad\to\quad 417,\ 447,\ 477\]'),
  prob(L(r"És primer el \(91\)? I el \(97\)?", r"¿Es primo el \(91\)? ¿Y el \(97\)?", r"Is \(91\) prime? And \(97\)?"),
       P(r"\(91=7\cdot13\): és <strong>compost</strong>. El \(97\) no és divisible per 2, 3, 5 ni 7, i \(97:11\) dona un quocient (8) menor que 11: és <strong>primer</strong>.", r"\(91=7\cdot13\): es <strong>compuesto</strong>. El \(97\) no es divisible por 2, 3, 5 ni 7, y \(97:11\) da un cociente (8) menor que 11: es <strong>primo</strong>.", r"\(91=7\cdot13\): it is <strong>composite</strong>. \(97\) is not divisible by 2, 3, 5 or 7, and \(97:11\) gives a quotient (8) smaller than 11: it is <strong>prime</strong>.")))
s3 += practice([
  ('★', L(r"a) Classifica en primers i compostos: 31, 51, 57, 61, 87, 1.", r"a) Clasifica en primos y compuestos: 31, 51, 57, 61, 87, 1.", r"a) Sort into prime and composite: 31, 51, 57, 61, 87, 1.")),
  ('★★', L(r"b) Quina xifra cal posar en \(5\square2\) perquè siga múltiple de 9? c) I en \(23\square\) perquè siga múltiple de 2 i de 5 alhora?", r"b) ¿Qué cifra hay que poner en \(5\square2\) para que sea múltiplo de 9? c) ¿Y en \(23\square\) para que sea múltiplo de 2 y de 5 a la vez?", r"b) Which digit must go in \(5\square2\) to make it a multiple of 9? c) And in \(23\square\) to make it a multiple of both 2 and 5?"))],
  P(r"a) Primers: 31, 61. Compostos: \(51=3\cdot17\), \(57=3\cdot19\), \(87=3\cdot29\). L'1 no és ni primer ni compost. &nbsp; b) \(7+\square=9\Rightarrow\square=2\) (522). &nbsp; c) Ha d'acabar en 0: 230.", r"a) Primos: 31, 61. Compuestos: \(51=3\cdot17\), \(57=3\cdot19\), \(87=3\cdot29\). El 1 no es ni primo ni compuesto. &nbsp; b) \(7+\square=9\Rightarrow\square=2\) (522). &nbsp; c) Tiene que acabar en 0: 230.", r"a) Prime: 31, 61. Composite: \(51=3\cdot17\), \(57=3\cdot19\), \(87=3\cdot29\). 1 is neither. &nbsp; b) \(7+\square=9\Rightarrow\square=2\) (522). &nbsp; c) It must end in 0: 230."))

# ============================================================ 1.4 Descomposició en factors primers
s4 = box('def', L('Descomposició en factors primers', 'Descomposición en factores primos', 'Prime factorisation'),
  P(r"Tot nombre compost es pot escriure, d'una única manera, com a <strong>producte de factors primers</strong>. Per a trobar-la, el dividim successivament entre el primer més xicotet possible fins a arribar a \(1\) (mètode de la columna):",
    r"Todo número compuesto se puede escribir, de una única manera, como <strong>producto de factores primos</strong>. Para encontrarla, lo dividimos sucesivamente entre el primo más pequeño posible hasta llegar a \(1\) (método de la columna):",
    r"Every composite number can be written, in exactly one way, as a <strong>product of prime factors</strong>. To find it, keep dividing by the smallest possible prime until you reach \(1\) (the column method):")
  + '<div class="grid2">' + '<div>' + col([(360, 2), (180, 2), (90, 2), (45, 3), (15, 3), (5, 5), (1, '')]) + '</div><div>'
  + r'\[360=2\cdot2\cdot2\cdot3\cdot3\cdot5=\boxed{2^3\cdot3^2\cdot5}\]' + P(r"Els factors repetits s'escriuen com a <strong>potència</strong>.", r"Los factores repetidos se escriben como <strong>potencia</strong>.", r"Repeated factors are written as a <strong>power</strong>.") + '</div></div>')
s4 += W_fact + drill('fact', 'Entrena: descomposició', 'Entrena: descomposición', 'Train: factorisation')
s4 += level(2, 1,
  prob(L(r"Descompon \(1176\) en factors primers.", r"Descompón \(1176\) en factores primos.", r"Write \(1176\) as a product of primes."),
       col([(1176, 2), (588, 2), (294, 2), (147, 3), (49, 7), (7, 7), (1, '')]),
       r'\[1176=\boxed{2^3\cdot3\cdot7^2}\]'))
s4 += level(3, 2,
  prob(L(r"Per quin nombre, el més xicotet possible, cal multiplicar \(72\) perquè siga un quadrat perfecte?", r"¿Por qué número, el más pequeño posible, hay que multiplicar \(72\) para que sea un cuadrado perfecto?", r"What is the smallest number we must multiply \(72\) by to get a perfect square?"),
       P(r"\(72=2^3\cdot3^2\). En un quadrat perfecte tots els exponents són parells: falta un \(2\).", r"\(72=2^3\cdot3^2\). En un cuadrado perfecto todos los exponentes son pares: falta un \(2\).", r"\(72=2^3\cdot3^2\). In a perfect square every exponent is even: one more \(2\) is needed."),
       r'\[72\cdot\boxed{2}=144=2^4\cdot3^2=12^2\]'))
s4 += practice([
  ('★', L(r"a) Descompon en factors primers: 60, 84, 126, 1000.", r"a) Descompón en factores primos: 60, 84, 126, 1000.", r"a) Find the prime factorisation of 60, 84, 126, 1000.")),
  ('★★', L(r"b) Quin nombre té per descomposició \(2^3\cdot3\cdot5^2\)? I \(3\cdot5\cdot7\cdot11\)?", r"b) ¿Qué número tiene por descomposición \(2^3\cdot3\cdot5^2\)? ¿Y \(3\cdot5\cdot7\cdot11\)?", r"b) Which number has factorisation \(2^3\cdot3\cdot5^2\)? And \(3\cdot5\cdot7\cdot11\)?"))],
  P(r"a) \(60=2^2\cdot3\cdot5\), \(84=2^2\cdot3\cdot7\), \(126=2\cdot3^2\cdot7\), \(1000=2^3\cdot5^3\). &nbsp; b) \(600\) i \(1155\).", r"a) \(60=2^2\cdot3\cdot5\), \(84=2^2\cdot3\cdot7\), \(126=2\cdot3^2\cdot7\), \(1000=2^3\cdot5^3\). &nbsp; b) \(600\) y \(1155\).", r"a) \(60=2^2\cdot3\cdot5\), \(84=2^2\cdot3\cdot7\), \(126=2\cdot3^2\cdot7\), \(1000=2^3\cdot5^3\). &nbsp; b) \(600\) and \(1155\)."))

# ============================================================ 1.5 mcm i MCD
s5 = box('def', L('Mínim comú múltiple (mcm)', 'Mínimo común múltiplo (mcm)', 'Least common multiple (lcm)'),
  P(r"El <strong>mínim comú múltiple</strong> de diversos nombres és el <strong>més xicotet</strong> dels seus múltiples comuns, sense comptar el 0.", r"El <strong>mínimo común múltiplo</strong> de varios números es el <strong>menor</strong> de sus múltiplos comunes, sin contar el 0.", r"The <strong>least common multiple</strong> of several numbers is the <strong>smallest</strong> of their common multiples, not counting 0.")
  + r'\[\dot{4}=\{4,8,\mathbf{12},16,20,\mathbf{24},\ldots\}\quad \dot{6}=\{6,\mathbf{12},18,\mathbf{24},\ldots\}\quad\Rightarrow\quad\text{mcm}(4,6)=12\]'.replace(r'\text{mcm}', MCM)
  + P(r"<strong>Amb la descomposició:</strong> es multipliquen els factors primers <strong>comuns i no comuns</strong>, cadascun elevat al <strong>major</strong> exponent.", r"<strong>Con la descomposición:</strong> se multiplican los factores primos <strong>comunes y no comunes</strong>, cada uno elevado al <strong>mayor</strong> exponente.", r"<strong>Using factorisation:</strong> multiply the <strong>common and non-common</strong> prime factors, each raised to the <strong>highest</strong> exponent."))
s5 += box('def', L('Màxim comú divisor (MCD)', 'Máximo común divisor (MCD)', 'Greatest common divisor (gcd)'),
  P(r"El <strong>màxim comú divisor</strong> de diversos nombres és el <strong>més gran</strong> dels seus divisors comuns.", r"El <strong>máximo común divisor</strong> de varios números es el <strong>mayor</strong> de sus divisores comunes.", r"The <strong>greatest common divisor</strong> of several numbers is the <strong>largest</strong> of their common divisors.")
  + r'\[\text{Div}(12)=\{\mathbf{1},\mathbf{2},\mathbf{3},4,\mathbf{6},12\}\quad\text{Div}(18)=\{\mathbf{1},\mathbf{2},\mathbf{3},\mathbf{6},9,18\}\quad\Rightarrow\quad\text{MCD}(12,18)=6\]'.replace(r'\text{MCD}', MCD)
  + P(r"<strong>Amb la descomposició:</strong> es multipliquen només els factors primers <strong>comuns</strong>, cadascun elevat al <strong>menor</strong> exponent. Si el MCD és 1, els nombres són <strong>primers entre si</strong>.", r"<strong>Con la descomposición:</strong> se multiplican solo los factores primos <strong>comunes</strong>, cada uno elevado al <strong>menor</strong> exponente. Si el MCD es 1, los números son <strong>primos entre sí</strong>.", r"<strong>Using factorisation:</strong> multiply only the <strong>common</strong> prime factors, each raised to the <strong>lowest</strong> exponent. If the gcd is 1, the numbers are <strong>coprime</strong>."))
s5 += box('prop', L('Exemple: mcm i MCD de 72 i 60', 'Ejemplo: mcm y MCD de 72 y 60', 'Example: lcm and gcd of 72 and 60'),
  '<div class="grid2"><div>' + col([(72, 2), (36, 2), (18, 2), (9, 3), (3, 3), (1, '')]) + r'\[72=2^3\cdot3^2\]</div><div>' + col([(60, 2), (30, 2), (15, 3), (5, 5), (1, '')]) + r'\[60=2^2\cdot3\cdot5\]</div></div>'
  + r'\[' + MCM + r'(72,60)=2^3\cdot3^2\cdot5=\boxed{360}\qquad ' + MCD + r'(72,60)=2^2\cdot3=\boxed{12}\]'
  + note(r"Per a dos nombres es compleix \(\text{MCD}(a,b)\cdot\text{mcm}(a,b)=a\cdot b\): \(12\cdot360=4320=72\cdot60\).", r"Para dos números se cumple \(\text{MCD}(a,b)\cdot\text{mcm}(a,b)=a\cdot b\): \(12\cdot360=4320=72\cdot60\).", r"For two numbers, \(\gcd(a,b)\cdot\text{lcm}(a,b)=a\cdot b\): \(12\cdot360=4320=72\cdot60\)."))
s5 += W_gcd_mcm + drill('mcm', 'Entrena: mcm', 'Entrena: mcm', 'Train: lcm')
s5 += W_gcd_mcd + drill('mcd', 'Entrena: MCD', 'Entrena: MCD', 'Train: gcd')
s5 += level(2, 1,
  prob(L(r"Calcula el mcm i el MCD de \(45\), \(60\) i \(75\).", r"Calcula el mcm y el MCD de \(45\), \(60\) y \(75\).", r"Find the lcm and gcd of \(45\), \(60\) and \(75\)."),
       r'\[45=3^2\cdot5\qquad 60=2^2\cdot3\cdot5\qquad 75=3\cdot5^2\]',
       r'\[' + MCM + r'=2^2\cdot3^2\cdot5^2=\boxed{900}\qquad ' + MCD + r'=3\cdot5=\boxed{15}\]'))
s5 += level(3, 2,
  prob(L(r"El MCD de dos nombres és 6 i el mcm, 90. Si un dels nombres és 18, quin és l'altre?", r"El MCD de dos números es 6 y el mcm, 90. Si uno de los números es 18, ¿cuál es el otro?", r"The gcd of two numbers is 6 and their lcm is 90. If one of them is 18, what is the other?"),
       r'\[18\cdot b=6\cdot90=540\ \Rightarrow\ b=540:18=\boxed{30}\]',
       P(r"Comprovació: \(18=2\cdot3^2\), \(30=2\cdot3\cdot5\): MCD \(=6\), mcm \(=90\). ✓", r"Comprobación: \(18=2\cdot3^2\), \(30=2\cdot3\cdot5\): MCD \(=6\), mcm \(=90\). ✓", r"Check: \(18=2\cdot3^2\), \(30=2\cdot3\cdot5\): gcd \(=6\), lcm \(=90\). ✓")))
s5 += practice([
  ('★', L(r"a) Calcula llistant múltiples i divisors: \(\text{mcm}(8,20)\) i \(\text{MCD}(8,20)\).", r"a) Calcula listando múltiplos y divisores: \(\text{mcm}(8,20)\) y \(\text{MCD}(8,20)\).", r"a) By listing multiples and divisors, find \(\text{lcm}(8,20)\) and \(\gcd(8,20)\).")),
  ('★★', L(r"b) Calcula el mcm i el MCD de 84 i 126, i de 140 i 300. c) Són primers entre si 15 i 28? I 21 i 35?", r"b) Calcula el mcm y el MCD de 84 y 126, y de 140 y 300. c) ¿Son primos entre sí 15 y 28? ¿Y 21 y 35?", r"b) Find the lcm and gcd of 84 and 126, and of 140 and 300. c) Are 15 and 28 coprime? And 21 and 35?"))],
  P(r"a) 40 i 4. &nbsp; b) mcm(84,126) = 252, MCD = 42; mcm(140,300) = 2100, MCD = 20. &nbsp; c) Sí (MCD = 1); no (MCD = 7).", r"a) 40 y 4. &nbsp; b) mcm(84,126) = 252, MCD = 42; mcm(140,300) = 2100, MCD = 20. &nbsp; c) Sí (MCD = 1); no (MCD = 7).", r"a) 40 and 4. &nbsp; b) lcm(84,126) = 252, gcd = 42; lcm(140,300) = 2100, gcd = 20. &nbsp; c) Yes (gcd = 1); no (gcd = 7)."))

# ============================================================ 1.6 Problemes de mcm i MCD
s6 = box('def', L('mcm o MCD? Com ho sabem', '¿mcm o MCD? Cómo lo sabemos', 'lcm or gcd? How to tell'),
  '<div class="tbl-wrap"><table class="data"><thead><tr><th>mcm</th><th>MCD</th></tr></thead><tbody><tr><td class="l">'
  + ul(L("Busquem quan <strong>tornen a coincidir</strong> dues o més coses que es repeteixen (autobusos, fars, torns…).", "Buscamos cuándo <strong>vuelven a coincidir</strong> dos o más cosas que se repiten (autobuses, faros, turnos…).", "We look for when two or more repeating things <strong>coincide again</strong> (buses, lighthouses, shifts…)."),
       L("Busquem la quantitat <strong>més xicoteta</strong> que es pot repartir exactament de diverses maneres.", "Buscamos la cantidad <strong>más pequeña</strong> que se puede repartir exactamente de varias maneras.", "We look for the <strong>smallest</strong> amount that can be shared out exactly in several ways."),
       L("El resultat és <strong>més gran</strong> (o igual) que els nombres de l'enunciat.", "El resultado es <strong>mayor</strong> (o igual) que los números del enunciado.", "The answer is <strong>larger than</strong> (or equal to) the numbers given."))
  + '</td><td class="l">'
  + ul(L("Volem <strong>dividir o repartir</strong> en parts iguals, <strong>les més grans possible</strong>, sense que en sobre res.", "Queremos <strong>dividir o repartir</strong> en partes iguales, <strong>las mayores posibles</strong>, sin que sobre nada.", "We want to <strong>split or share</strong> into equal parts, <strong>as large as possible</strong>, with nothing left over."),
       L("Fer grups, rams, lots, rajoles o trossos iguals del major tamany.", "Hacer grupos, ramos, lotes, baldosas o trozos iguales del mayor tamaño.", "Making equal groups, bunches, lots, tiles or pieces of the largest size."),
       L("El resultat és <strong>més xicotet</strong> (o igual) que els nombres de l'enunciat.", "El resultado es <strong>menor</strong> (o igual) que los números del enunciado.", "The answer is <strong>smaller than</strong> (or equal to) the numbers given."))
  + '</td></tr></tbody></table></div>')
s6 += W_coin + W_tile
s6 += level(1, 1,
  prob(L(r"Dues línies d'autobús ixen de la mateixa parada a les 7:00. La línia A passa cada 15 minuts i la B, cada 20. A quina hora tornaran a coincidir?", r"Dos líneas de autobús salen de la misma parada a las 7:00. La línea A pasa cada 15 minutos y la B, cada 20. ¿A qué hora volverán a coincidir?", r"Two bus routes leave the same stop at 7:00. Route A runs every 15 minutes and route B every 20. When will they next coincide?"),
       P(r"«Tornar a coincidir» → mcm. \(15=3\cdot5\), \(20=2^2\cdot5\):", r"«Volver a coincidir» → mcm. \(15=3\cdot5\), \(20=2^2\cdot5\):", r"“Coincide again” → lcm. \(15=3\cdot5\), \(20=2^2\cdot5\):"),
       r'\[' + MCM + r'(15,20)=2^2\cdot3\cdot5=60\text{ min}\ \Rightarrow\ \boxed{8{:}00}\]'),
  prob(L(r"Tenim 60 roses i 84 clavells. Volem fer el major nombre possible de rams iguals, sense que sobre cap flor. Quants rams farem i quantes flors de cada tipus durà cada ram?", r"Tenemos 60 rosas y 84 claveles. Queremos hacer el mayor número posible de ramos iguales, sin que sobre ninguna flor. ¿Cuántos ramos haremos y cuántas flores de cada tipo llevará cada ramo?", r"We have 60 roses and 84 carnations. We want to make as many identical bunches as possible, with no flowers left over. How many bunches, and how many flowers of each kind in each?"),
       P(r"Repartir en parts iguals, el màxim possible → MCD. \(60=2^2\cdot3\cdot5\), \(84=2^2\cdot3\cdot7\):", r"Repartir en partes iguales, el máximo posible → MCD. \(60=2^2\cdot3\cdot5\), \(84=2^2\cdot3\cdot7\):", r"Share equally, as many as possible → gcd. \(60=2^2\cdot3\cdot5\), \(84=2^2\cdot3\cdot7\):"),
       r'\[' + MCD + r'(60,84)=2^2\cdot3=\boxed{12}\ \tri{rams}{ramos}{bunches}\qquad 60:12=5\ \tri{roses}{rosas}{roses},\quad 84:12=7\ \tri{clavells}{claveles}{carnations}\]'))
s6 += level(2, 3,
  prob(L(r"Volem enrajolar una habitació de 4,80 m × 3,60 m amb rajoles quadrades, les més grans possible i sense tallar-ne cap. Quant ha de mesurar el costat de cada rajola? Quantes en calen?", r"Queremos embaldosar una habitación de 4,80 m × 3,60 m con baldosas cuadradas, las mayores posibles y sin cortar ninguna. ¿Cuánto debe medir el lado de cada baldosa? ¿Cuántas hacen falta?", r"We want to tile a 4.80 m × 3.60 m room with square tiles, as large as possible and without cutting any. How long is the side of each tile? How many do we need?"),
       P(r"Passem a centímetres: 480 i 360. El costat ha de dividir els dos i ser el més gran possible → MCD.", r"Pasamos a centímetros: 480 y 360. El lado tiene que dividir a los dos y ser el mayor posible → MCD.", r"In centimetres: 480 and 360. The side must divide both and be as large as possible → gcd."),
       r'\[480=2^5\cdot3\cdot5\qquad 360=2^3\cdot3^2\cdot5\qquad ' + MCD + r'=2^3\cdot3\cdot5=\boxed{120\text{ cm}}\]',
       r'\[\tfrac{480}{120}=4,\quad \tfrac{360}{120}=3\ \Rightarrow\ 4\cdot3=\boxed{12}\ \tri{rajoles}{baldosas}{tiles}\]'),
  prob(L(r"Tres fars s'encenen cada 8, 12 i 18 segons. Si ara s'encenen alhora, quant de temps passarà fins que tornen a encendre's junts?", r"Tres faros se encienden cada 8, 12 y 18 segundos. Si ahora se encienden a la vez, ¿cuánto tiempo pasará hasta que vuelvan a encenderse juntos?", r"Three lighthouses flash every 8, 12 and 18 seconds. If they flash together now, how long until they flash together again?"),
       r'\[8=2^3\qquad 12=2^2\cdot3\qquad 18=2\cdot3^2\qquad ' + MCM + r'=2^3\cdot3^2=\boxed{72\text{ s}}\]'))
s6 += level(3, 5,
  prob(L(r"Si agrupem els caramels d'una bossa de 6 en 6, de 8 en 8 o de 10 en 10, sempre en sobren 3. Quants caramels hi ha com a mínim (més de 3)?", r"Si agrupamos los caramelos de una bolsa de 6 en 6, de 8 en 8 o de 10 en 10, siempre sobran 3. ¿Cuántos caramelos hay como mínimo (más de 3)?", r"If we group the sweets in a bag in sixes, eights or tens, there are always 3 left over. What is the smallest possible number of sweets (more than 3)?"),
       P(r"Si en llevem 3, el nombre que queda és múltiple de 6, de 8 i de 10:", r"Si quitamos 3, el número que queda es múltiplo de 6, de 8 y de 10:", r"Take away 3 and what's left is a multiple of 6, 8 and 10:"),
       r'\[' + MCM + r'(6,8,10)=2^3\cdot3\cdot5=120\ \Rightarrow\ 120+3=\boxed{123}\]'))

# ============================================================ 1.7 Els nombres enters
s7 = box('def', L('Definició: nombres enters', 'Definición: números enteros', 'Definition: integers'),
  P(r"Amb els naturals no podem expressar una temperatura <strong>baix zero</strong>, un <strong>soterrani</strong>, un <strong>deute</strong> o una <strong>profunditat</strong>, ni fer restes com \(3-5\). Per a això fem servir els <strong>nombres enters</strong>, que són els naturals amb signe positiu, els seus oposats amb signe negatiu i el zero:",
    r"Con los naturales no podemos expresar una temperatura <strong>bajo cero</strong>, un <strong>sótano</strong>, una <strong>deuda</strong> o una <strong>profundidad</strong>, ni hacer restas como \(3-5\). Para ello usamos los <strong>números enteros</strong>, que son los naturales con signo positivo, sus opuestos con signo negativo y el cero:",
    r"Natural numbers can't express a temperature <strong>below zero</strong>, a <strong>basement</strong>, a <strong>debt</strong> or a <strong>depth</strong>, nor subtractions like \(3-5\). For this we use <strong>integers</strong>: the natural numbers with a positive sign, their opposites with a negative sign, and zero:")
  + r'\[\mathbb{Z}=\{\,\ldots,\ -3,\ -2,\ -1,\ 0,\ +1,\ +2,\ +3,\ \ldots\}\qquad \mathbb{N}\subset\mathbb{Z}\]'
  + P(r"El signe \(+\) dels positius es pot ometre (\(+7=7\)); el signe \(-\) dels negatius s'ha d'escriure sempre. El \(0\) no és ni positiu ni negatiu.", r"El signo \(+\) de los positivos se puede omitir (\(+7=7\)); el signo \(-\) de los negativos se tiene que escribir siempre. El \(0\) no es ni positivo ni negativo.", r"The \(+\) sign of positives can be left out (\(+7=7\)); the \(-\) sign of negatives must always be written. \(0\) is neither positive nor negative."))
s7 += W_ctx
s7 += box('def', L('Recta numèrica i ordre', 'Recta numérica y orden', 'Number line and order'),
  P(r"Els enters es representen en una recta: el \(0\) al centre, els positius a la dreta i els negatius a l'esquerra. <strong>Com més a la dreta, més gran</strong>: qualsevol positiu és major que qualsevol negatiu i, entre dos negatius, és més gran el que té <strong>menor valor absolut</strong>.",
    r"Los enteros se representan en una recta: el \(0\) en el centro, los positivos a la derecha y los negativos a la izquierda. <strong>Cuanto más a la derecha, mayor</strong>: cualquier positivo es mayor que cualquier negativo y, entre dos negativos, es mayor el que tiene <strong>menor valor absoluto</strong>.",
    r"Integers are shown on a line: \(0\) in the middle, positives to the right and negatives to the left. <strong>The further right, the larger</strong>: every positive is larger than every negative and, of two negatives, the one with the <strong>smaller absolute value</strong> is larger.")
  + nline(-6, 6, pts=(-5, -2, 3)) + r'\[-5<-2<0<3\]')
s7 += W_line + drill('ord', 'Entrena: ordre', 'Entrena: orden', 'Train: order')
s7 += box('def', L('Valor absolut i oposat', 'Valor absoluto y opuesto', 'Absolute value and opposite'),
  ul(L(r"El <strong>valor absolut</strong> d'un enter, \(|a|\), és la distància que hi ha fins al \(0\); és el nombre sense signe: \(|-7|=7\), \(|+4|=4\), \(|0|=0\).", r"El <strong>valor absoluto</strong> de un entero, \(|a|\), es la distancia que hay hasta el \(0\); es el número sin signo: \(|-7|=7\), \(|+4|=4\), \(|0|=0\).", r"The <strong>absolute value</strong> of an integer, \(|a|\), is its distance from \(0\); it's the number without its sign: \(|-7|=7\), \(|+4|=4\), \(|0|=0\)."),
       L(r"L'<strong>oposat</strong> d'un enter té el mateix valor absolut i signe contrari: \(\text{op}(-7)=7\), \(\text{op}(4)=-4\). L'oposat de \(a\) s'escriu \(-a\).", r"El <strong>opuesto</strong> de un entero tiene el mismo valor absoluto y signo contrario: \(\text{op}(-7)=7\), \(\text{op}(4)=-4\). El opuesto de \(a\) se escribe \(-a\).", r"The <strong>opposite</strong> of an integer has the same absolute value and the other sign: \(\text{op}(-7)=7\), \(\text{op}(4)=-4\). The opposite of \(a\) is written \(-a\).")))
s7 += W_abs + drill('abs', 'Entrena: valor absolut i oposat', 'Entrena: valor absoluto y opuesto', 'Train: absolute value and opposite')
s7 += level(1, 1,
  prob(L(r"Ordena de menor a major: \(\ -3,\ 5,\ -8,\ 0,\ 2,\ -1,\ -12,\ 7\).", r"Ordena de menor a mayor: \(\ -3,\ 5,\ -8,\ 0,\ 2,\ -1,\ -12,\ 7\).", r"Put in increasing order: \(\ -3,\ 5,\ -8,\ 0,\ 2,\ -1,\ -12,\ 7\)."),
       r'\[-12<-8<-3<-1<0<2<5<7\]'))
s7 += level(2, 2,
  prob(L(r"Escriu tots els enters \(x\) que compleixen: a) \(-4\lt x\le2\); b) \(|x|<3\); c) \(|x|=5\).", r"Escribe todos los enteros \(x\) que cumplen: a) \(-4\lt x\le2\); b) \(|x|<3\); c) \(|x|=5\).", r"Write all the integers \(x\) such that: a) \(-4\lt x\le2\); b) \(|x|<3\); c) \(|x|=5\)."),
       P(r"a) \(-3,-2,-1,0,1,2\). &nbsp; b) \(-2,-1,0,1,2\). &nbsp; c) \(-5\) i \(5\).", r"a) \(-3,-2,-1,0,1,2\). &nbsp; b) \(-2,-1,0,1,2\). &nbsp; c) \(-5\) y \(5\).", r"a) \(-3,-2,-1,0,1,2\). &nbsp; b) \(-2,-1,0,1,2\). &nbsp; c) \(-5\) and \(5\).")))

# ============================================================ 1.8 Suma i resta d'enters
s8 = box('def', L("Suma d'enters", 'Suma de enteros', 'Adding integers'),
  ul(L(r"<strong>Mateix signe:</strong> se sumen els valors absoluts i es posa el signe comú: \(\ (-7)+(-5)=-12\), \(\ 4+9=13\).", r"<strong>Mismo signo:</strong> se suman los valores absolutos y se pone el signo común: \(\ (-7)+(-5)=-12\), \(\ 4+9=13\).", r"<strong>Same sign:</strong> add the absolute values and keep the common sign: \(\ (-7)+(-5)=-12\), \(\ 4+9=13\)."),
       L(r"<strong>Signe diferent:</strong> es resten els valors absoluts (el major menys el menor) i es posa el signe del que té <strong>major valor absolut</strong>: \(\ (-9)+4=-5\), \(\ 12+(-7)=5\).", r"<strong>Signo distinto:</strong> se restan los valores absolutos (el mayor menos el menor) y se pone el signo del que tiene <strong>mayor valor absoluto</strong>: \(\ (-9)+4=-5\), \(\ 12+(-7)=5\).", r"<strong>Different signs:</strong> subtract the absolute values (larger minus smaller) and use the sign of the one with the <strong>larger absolute value</strong>: \(\ (-9)+4=-5\), \(\ 12+(-7)=5\)."))
  + box('prop', L("Restar és sumar l'oposat", 'Restar es sumar el opuesto', 'Subtracting is adding the opposite'),
        r'\[a-b=a+(-b)\qquad 8-13=8+(-13)=-5\qquad (-6)-(-10)=-6+10=4\]'))
s8 += W_add + drill('add', 'Entrena: sumes i restes', 'Entrena: sumas y restas', 'Train: adding and subtracting')
s8 += box('def', L('Llevar parèntesis i claudàtors', 'Quitar paréntesis y corchetes', 'Removing brackets'),
  ul(L(r"Un parèntesi precedit de \(+\) es pot llevar sense canviar res: \(\ +(-3)=-3\), \(\ +(5-2)=5-2\).", r"Un paréntesis precedido de \(+\) se puede quitar sin cambiar nada: \(\ +(-3)=-3\), \(\ +(5-2)=5-2\).", r"Brackets preceded by \(+\) can be removed without changing anything: \(\ +(-3)=-3\), \(\ +(5-2)=5-2\)."),
       L(r"Un parèntesi precedit de \(-\) es lleva <strong>canviant el signe</strong> de tots els termes de dins: \(\ -(-3)=+3\), \(\ -(5-2)=-5+2\).", r"Un paréntesis precedido de \(-\) se quita <strong>cambiando el signo</strong> de todos los términos de dentro: \(\ -(-3)=+3\), \(\ -(5-2)=-5+2\).", r"Brackets preceded by \(-\) are removed by <strong>changing the sign</strong> of every term inside: \(\ -(-3)=+3\), \(\ -(5-2)=-5+2\)."),
       L(r"Amb moltes sumes i restes és còmode <strong>agrupar</strong> positius i negatius: \(\ 5-8+3-7+2=(5+3+2)-(8+7)=10-15=-5\).", r"Con muchas sumas y restas es cómodo <strong>agrupar</strong> positivos y negativos: \(\ 5-8+3-7+2=(5+3+2)-(8+7)=10-15=-5\).", r"With many additions and subtractions it helps to <strong>group</strong> positives and negatives: \(\ 5-8+3-7+2=(5+3+2)-(8+7)=10-15=-5\).")))
s8 += W_par + drill('par', 'Entrena: parèntesis', 'Entrena: paréntesis', 'Train: brackets')
s8 += level(1, 1,
  prob(L(r"Calcula: \(\ 7-(3-5+2)\).", r"Calcula: \(\ 7-(3-5+2)\).", r"Work out: \(\ 7-(3-5+2)\)."),
       r'\[7-(3-5+2)=7-3+5-2=(7+5)-(3+2)=12-5=\boxed{7}\]'))
s8 += level(2, 2,
  prob(L(r"Calcula: \(\ 10-[3-(5-8)]\).", r"Calcula: \(\ 10-[3-(5-8)]\).", r"Work out: \(\ 10-[3-(5-8)]\)."),
       P(r"Comencem pel parèntesi de dins:", r"Empezamos por el paréntesis de dentro:", r"Start with the innermost brackets:"),
       r'\[10-[3-(-3)]=10-[3+3]=10-6=\boxed{4}\]'),
  prob(L(r"Pitàgores va nàixer l'any 570 a. C. i va morir el 495 a. C. Quants anys va viure?", r"Pitágoras nació en el año 570 a. C. y murió en el 495 a. C. ¿Cuántos años vivió?", r"Pythagoras was born in 570 BC and died in 495 BC. How many years did he live?"),
       r'\[-495-(-570)=-495+570=\boxed{75\ \tri{anys}{años}{years}}\]'))

# ============================================================ 1.9 Multiplicació, divisió i operacions combinades
s9 = box('def', L('Multiplicació i divisió: la regla dels signes', 'Multiplicación y división: la regla de los signos', 'Multiplication and division: the sign rule'),
  P(r"Es multipliquen (o divideixen) els valors absoluts i el signe del resultat es decideix així:", r"Se multiplican (o dividen) los valores absolutos y el signo del resultado se decide así:", r"Multiply (or divide) the absolute values; the sign of the result is decided like this:")
  + SGT
  + r'\[(-6)\cdot(-4)=24\qquad 7\cdot(-8)=-56\qquad (-45):9=-5\qquad (-56):(-7)=8\]'
  + note(r"Si multipliquem diversos factors, el resultat és positiu si hi ha un nombre <strong>parell</strong> de factors negatius i negatiu si n'hi ha un nombre <strong>senar</strong>: \((-2)\cdot(-3)\cdot(-5)=-30\).", r"Si multiplicamos varios factores, el resultado es positivo si hay un número <strong>par</strong> de factores negativos y negativo si hay un número <strong>impar</strong>: \((-2)\cdot(-3)\cdot(-5)=-30\).", r"With several factors, the result is positive if there is an <strong>even</strong> number of negative factors and negative if there is an <strong>odd</strong> number: \((-2)\cdot(-3)\cdot(-5)=-30\)."))
s9 += W_sign + drill('mul', 'Entrena: multiplicació i divisió', 'Entrena: multiplicación y división', 'Train: multiplying and dividing')
s9 += box('def', L('Jerarquia de les operacions', 'Jerarquía de las operaciones', 'Order of operations'),
  '<ol>' + ''.join(f'<li>{x}</li>' for x in [
    L("<strong>Parèntesis i claudàtors</strong>, començant pels de dins.", "<strong>Paréntesis y corchetes</strong>, empezando por los de dentro.", "<strong>Brackets</strong>, starting with the innermost."),
    L("<strong>Potències i arrels</strong>.", "<strong>Potencias y raíces</strong>.", "<strong>Powers and roots</strong>."),
    L("<strong>Multiplicacions i divisions</strong>, d'esquerra a dreta.", "<strong>Multiplicaciones y divisiones</strong>, de izquierda a derecha.", "<strong>Multiplication and division</strong>, from left to right."),
    L("<strong>Sumes i restes</strong>, d'esquerra a dreta.", "<strong>Sumas y restas</strong>, de izquierda a derecha.", "<strong>Addition and subtraction</strong>, from left to right.")]) + '</ol>'
  + box('warn', L('Errors freqüents', 'Errores frecuentes', 'Common mistakes'),
        ul(L(r"\(8-3\cdot2=8-6=2\), i no \(5\cdot2=10\): primer la multiplicació.", r"\(8-3\cdot2=8-6=2\), y no \(5\cdot2=10\): primero la multiplicación.", r"\(8-3\cdot2=8-6=2\), not \(5\cdot2=10\): multiplication first."),
           L(r"\(12:2\cdot3=6\cdot3=18\), i no \(12:6=2\): d'esquerra a dreta.", r"\(12:2\cdot3=6\cdot3=18\), y no \(12:6=2\): de izquierda a derecha.", r"\(12:2\cdot3=6\cdot3=18\), not \(12:6=2\): left to right."))))
s9 += hier(["4-2·[3-(6-10)]", "18:(-3)+2·(-5)", "-20:4·(-2)", "25:(-5)-(-3)·(4-6):2", "(-3)·(2-7)+15:(-5)", "-6-[4-3·(2-5)]"])
s9 += drill('comb', 'Entrena: operacions combinades', 'Entrena: operaciones combinadas', 'Train: mixed operations')
s9 += level(2, 1,
  prob(L(r"Calcula: \(\ -6-[4-3\cdot(2-5)]\).", r"Calcula: \(\ -6-[4-3\cdot(2-5)]\).", r"Work out: \(\ -6-[4-3\cdot(2-5)]\)."),
       r'\[-6-[4-3\cdot(-3)]=-6-[4+9]=-6-13=\boxed{-19}\]'),
  prob(L(r"Un compte té un saldo de 230 €. Es paguen 3 rebuts de 85 € i després es cobren 120 €. Quin és el saldo final? Arriba a estar en negatiu?", r"Una cuenta tiene un saldo de 230 €. Se pagan 3 recibos de 85 € y después se cobran 120 €. ¿Cuál es el saldo final? ¿Llega a estar en negativo?", r"An account has a balance of €230. Three €85 bills are paid and then €120 comes in. What is the final balance? Does it go negative?"),
       r'\[230-3\cdot85+120=230-255+120=\boxed{95\text{ €}}\]',
       P(r"Sí: després de pagar els rebuts el saldo és \(230-255=-25\) €.", r"Sí: después de pagar los recibos el saldo es \(230-255=-25\) €.", r"Yes: after paying the bills the balance is \(230-255=-25\) €.")))
s9 += level(3, 3,
  prob(L(r"Un alumne ha fet \(\ 12-4:2\cdot(-3)=8:2\cdot(-3)=4\cdot(-3)=-12\). Troba l'error i fes-ho bé.", r"Un alumno ha hecho \(\ 12-4:2\cdot(-3)=8:2\cdot(-3)=4\cdot(-3)=-12\). Encuentra el error y hazlo bien.", r"A student wrote \(\ 12-4:2\cdot(-3)=8:2\cdot(-3)=4\cdot(-3)=-12\). Find the mistake and fix it."),
       P(r"Ha restat abans de dividir i multiplicar. Correcte:", r"Ha restado antes de dividir y multiplicar. Correcto:", r"They subtracted before dividing and multiplying. Correct:"),
       r'\[12-\underbrace{4:2}_{2}\cdot(-3)=12-\underbrace{2\cdot(-3)}_{-6}=12+6=\boxed{18}\]'))

# ============================================================ 1.10 Potències i arrels amb enters
s10 = box('def', L("Potències d'enters", 'Potencias de enteros', 'Powers of integers'),
  P(r"Una <strong>potència</strong> és una multiplicació de factors iguals: \(a^n=a\cdot a\cdots a\) (\(n\) vegades). El factor \(a\) és la <strong>base</strong> i \(n\), l'<strong>exponent</strong>.", r"Una <strong>potencia</strong> es una multiplicación de factores iguales: \(a^n=a\cdot a\cdots a\) (\(n\) veces). El factor \(a\) es la <strong>base</strong> y \(n\), el <strong>exponente</strong>.", r"A <strong>power</strong> is a product of equal factors: \(a^n=a\cdot a\cdots a\) (\(n\) times). The factor \(a\) is the <strong>base</strong> and \(n\) the <strong>exponent</strong>.")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Base', 'Base', 'Base') + '</th><th>' + L('Exponent', 'Exponente', 'Exponent') + '</th><th>' + L('Signe', 'Signo', 'Sign') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + r'<tr><td>' + L('positiva', 'positiva', 'positive') + r'</td><td>' + L('qualsevol', 'cualquiera', 'any') + r'</td><td class="pos">+</td><td>\(2^5=32\)</td></tr>'
  + r'<tr><td>' + L('negativa', 'negativa', 'negative') + r'</td><td>' + L('parell', 'par', 'even') + r'</td><td class="pos">+</td><td>\((-2)^4=16\)</td></tr>'
  + r'<tr><td>' + L('negativa', 'negativa', 'negative') + r'</td><td>' + L('senar', 'impar', 'odd') + r'</td><td class="neg">−</td><td>\((-2)^3=-8\)</td></tr>'
  + '</tbody></table></div>'
  + box('warn', L('Compte amb el parèntesi', 'Cuidado con el paréntesis', 'Watch the brackets'),
        r'\[(-3)^2=(-3)\cdot(-3)=9\qquad\qquad -3^2=-(3\cdot3)=-9\]'
        + P(r"Sense parèntesi, la base és \(3\) i el signe \(-\) queda fora de la potència. A més, \(a^1=a\) i \(a^0=1\) si \(a\neq0\): \((-7)^0=1\).", r"Sin paréntesis, la base es \(3\) y el signo \(-\) queda fuera de la potencia. Además, \(a^1=a\) y \(a^0=1\) si \(a\neq0\): \((-7)^0=1\).", r"Without brackets the base is \(3\) and the minus sign stays outside the power. Also, \(a^1=a\) and \(a^0=1\) if \(a\neq0\): \((-7)^0=1\).")))
s10 += W_powz
PROPS = [(r'a^m\cdot a^n=a^{m+n}', r'(-2)^3\cdot(-2)^5=(-2)^8'), (r'a^m:a^n=a^{m-n}', r'(-5)^9:(-5)^6=(-5)^3'), (r'(a^m)^n=a^{m\cdot n}', r'\left[(-3)^2\right]^4=(-3)^8'),
         (r'a^n\cdot b^n=(a\cdot b)^n', r'2^5\cdot(-3)^5=(-6)^5'), (r'a^n:b^n=(a:b)^n', r'(-12)^4:3^4=(-4)^4')]
s10 += box('prop', L('Propietats de les potències', 'Propiedades de las potencias', 'Properties of powers'),
  '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Propietat', 'Propiedad', 'Property') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>\\({a}\\)</td><td>\\({b}\\)</td></tr>' for a, b in PROPS) + '</tbody></table></div>'
  + P(r"Les dues primeres només es poden aplicar si les potències tenen la <strong>mateixa base</strong>; les dues últimes, si tenen el <strong>mateix exponent</strong>.", r"Las dos primeras solo se pueden aplicar si las potencias tienen la <strong>misma base</strong>; las dos últimas, si tienen el <strong>mismo exponente</strong>.", r"The first two only work when the powers have the <strong>same base</strong>; the last two, when they have the <strong>same exponent</strong>."))
s10 += drill('pow', 'Entrena: potències i arrels', 'Entrena: potencias y raíces', 'Train: powers and roots')
s10 += box('def', L('Arrel quadrada', 'Raíz cuadrada', 'Square root'),
  P(r"La <strong>arrel quadrada</strong> d'un nombre \(a\) és un nombre \(b\) que, elevat al quadrat, dona \(a\): \(\ \sqrt{a}=b\iff b^2=a\).", r"La <strong>raíz cuadrada</strong> de un número \(a\) es un número \(b\) que, elevado al cuadrado, da \(a\): \(\ \sqrt{a}=b\iff b^2=a\).", r"The <strong>square root</strong> of a number \(a\) is a number \(b\) whose square is \(a\): \(\ \sqrt{a}=b\iff b^2=a\).")
  + ul(L(r"Un enter <strong>positiu</strong> que és quadrat perfecte té <strong>dues</strong> arrels oposades: \(\sqrt{49}=\pm7\), perquè \(7^2=49\) i \((-7)^2=49\).", r"Un entero <strong>positivo</strong> que es cuadrado perfecto tiene <strong>dos</strong> raíces opuestas: \(\sqrt{49}=\pm7\), porque \(7^2=49\) y \((-7)^2=49\).", r"A <strong>positive</strong> perfect square has <strong>two</strong> opposite roots: \(\sqrt{49}=\pm7\), because \(7^2=49\) and \((-7)^2=49\)."),
       L(r"Un enter <strong>negatiu</strong> no té arrel quadrada entera: \(\sqrt{-49}\) no existeix (cap quadrat és negatiu).", r"Un entero <strong>negativo</strong> no tiene raíz cuadrada entera: \(\sqrt{-49}\) no existe (ningún cuadrado es negativo).", r"A <strong>negative</strong> integer has no integer square root: \(\sqrt{-49}\) doesn't exist (no square is negative)."),
       L(r"Si no és quadrat perfecte, calculem l'<strong>arrel entera</strong>: el major nombre el quadrat del qual no supera el radicand. \(\sqrt{50}\approx7\) amb residu \(1\), perquè \(50=7^2+1\).", r"Si no es cuadrado perfecto, calculamos la <strong>raíz entera</strong>: el mayor número cuyo cuadrado no supera el radicando. \(\sqrt{50}\approx7\) con resto \(1\), porque \(50=7^2+1\).", r"If it isn't a perfect square, we find the <strong>integer root</strong>: the largest number whose square doesn't exceed the radicand. \(\sqrt{50}\approx7\) with remainder \(1\), because \(50=7^2+1\)."))
  + note(r"En les operacions combinades, \(\sqrt{\ }\) indica l'arrel positiva: \(\sqrt{36}=6\).", r"En las operaciones combinadas, \(\sqrt{\ }\) indica la raíz positiva: \(\sqrt{36}=6\).", r"In mixed operations, \(\sqrt{\ }\) means the positive root: \(\sqrt{36}=6\)."))
s10 += W_rootz
s10 += hier(["(-2)^3+3^2", "-2^4+(-2)^4", "5-2·√36+(-1)^7", "[(-2)^2-3^2]^2:(-5)", "√(25-9)-(-3)^3:9", "(-3)^2·2-√49:(-7)"])
s10 += drill('comb2', 'Entrena: combinades amb potències i arrels', 'Entrena: combinadas con potencias y raíces', 'Train: mixed operations with powers and roots')
s10 += level(1, 1,
  prob(L(r"Calcula: \(\ (-3)^4,\ \ -3^4,\ \ (-2)^5,\ \ (-1)^{100},\ \ (-10)^3\).", r"Calcula: \(\ (-3)^4,\ \ -3^4,\ \ (-2)^5,\ \ (-1)^{100},\ \ (-10)^3\).", r"Work out: \(\ (-3)^4,\ \ -3^4,\ \ (-2)^5,\ \ (-1)^{100},\ \ (-10)^3\)."),
       r'\[81,\qquad -81,\qquad -32,\qquad 1,\qquad -1000\]'))
s10 += level(2, 2,
  prob(L(r"Expressa com una sola potència i calcula: \(\ (-2)^7:(-2)^4\ \) i \(\ \left[(-1)^3\right]^5\cdot(-1)^2\).", r"Expresa como una sola potencia y calcula: \(\ (-2)^7:(-2)^4\ \) y \(\ \left[(-1)^3\right]^5\cdot(-1)^2\).", r"Write as a single power and work out: \(\ (-2)^7:(-2)^4\ \) and \(\ \left[(-1)^3\right]^5\cdot(-1)^2\)."),
       r'\[(-2)^{7-4}=(-2)^3=\boxed{-8}\qquad (-1)^{15}\cdot(-1)^2=(-1)^{17}=\boxed{-1}\]'),
  prob(L(r"Calcula: \(\ \left[(-2)^2-3^2\right]^2:(-5)\).", r"Calcula: \(\ \left[(-2)^2-3^2\right]^2:(-5)\).", r"Work out: \(\ \left[(-2)^2-3^2\right]^2:(-5)\)."),
       r'\[[4-9]^2:(-5)=(-5)^2:(-5)=25:(-5)=\boxed{-5}\]'))
s10 += level(3, 4,
  prob(L(r"Una parcel·la quadrada té una superfície de 1225 m². Quant fa el costat? Quants metres de tanca calen per a envoltar-la?", r"Una parcela cuadrada tiene una superficie de 1225 m². ¿Cuánto mide el lado? ¿Cuántos metros de valla hacen falta para rodearla?", r"A square plot has an area of 1225 m². How long is each side? How many metres of fencing are needed to go round it?"),
       r'\[1225=5^2\cdot7^2=(5\cdot7)^2\ \Rightarrow\ \tri{costat}{lado}{side}=\sqrt{1225}=\boxed{35\text{ m}}\qquad 4\cdot35=\boxed{140\text{ m}}\]'))
s10 += practice([
  ('★', L(r"a) Calcula: \(\sqrt{144}\), \(\sqrt{400}\), \(\sqrt{-25}\), \((-7)^0\), \(0^7\).", r"a) Calcula: \(\sqrt{144}\), \(\sqrt{400}\), \(\sqrt{-25}\), \((-7)^0\), \(0^7\).", r"a) Work out: \(\sqrt{144}\), \(\sqrt{400}\), \(\sqrt{-25}\), \((-7)^0\), \(0^7\).")),
  ('★★', L(r"b) Arrel entera i residu de 90, 130 i 200. c) Signe, sense calcular: \((-7)^{12}\), \((-3)^{15}\), \(-5^4\), \(-(-2)^6\).", r"b) Raíz entera y resto de 90, 130 y 200. c) Signo, sin calcular: \((-7)^{12}\), \((-3)^{15}\), \(-5^4\), \(-(-2)^6\).", r"b) Integer root and remainder of 90, 130 and 200. c) Sign, without working out: \((-7)^{12}\), \((-3)^{15}\), \(-5^4\), \(-(-2)^6\)."))],
  P(r"a) \(\pm12\), \(\pm20\), no existeix, \(1\), \(0\). &nbsp; b) \(9\) (residu 9), \(11\) (residu 9), \(14\) (residu 4). &nbsp; c) \(+\), \(-\), \(-\), \(-\).", r"a) \(\pm12\), \(\pm20\), no existe, \(1\), \(0\). &nbsp; b) \(9\) (resto 9), \(11\) (resto 9), \(14\) (resto 4). &nbsp; c) \(+\), \(-\), \(-\), \(-\).", r"a) \(\pm12\), \(\pm20\), doesn't exist, \(1\), \(0\). &nbsp; b) \(9\) (remainder 9), \(11\) (remainder 9), \(14\) (remainder 4). &nbsp; c) \(+\), \(-\), \(-\), \(-\)."))

SECS = [
  (L('Els nombres naturals', 'Los números naturales', 'Natural numbers'), s1),
  (L('Múltiples i divisors', 'Múltiplos y divisores', 'Multiples and divisors'), s2),
  (L('Criteris de divisibilitat. Nombres primers', 'Criterios de divisibilidad. Números primos', 'Divisibility rules. Prime numbers'), s3),
  (L('Descomposició en factors primers', 'Descomposición en factores primos', 'Prime factorisation'), s4),
  (L('Mínim comú múltiple i màxim comú divisor', 'Mínimo común múltiplo y máximo común divisor', 'Least common multiple and greatest common divisor'), s5),
  (L('Problemes de mcm i MCD', 'Problemas de mcm y MCD', 'LCM and GCD problems'), s6),
  (L('Els nombres enters', 'Los números enteros', 'Integers'), s7),
  (L("Suma i resta d'enters", 'Suma y resta de enteros', 'Adding and subtracting integers'), s8),
  (L('Multiplicació, divisió i operacions combinades', 'Multiplicación, división y operaciones combinadas', 'Multiplication, division and mixed operations'), s9),
  (L('Potències i arrels amb enters', 'Potencias y raíces con enteros', 'Powers and roots with integers'), s10),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Nombres naturals i enters · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 1 (Nombres naturals i enters) de 2n d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "±";')
assert 'Nombres naturals i enters · FentMates' in head and 'content: "±"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">1.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../2eso.html">{L("2n ESO", "2º ESO", "2nd ESO (Year 8)")}</a> / {L("Unitat 1", "Unidad 1", "Unit 1")}</span>
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
    <h1><span class="u">{L("Unitat 1", "Unidad 1", "Unit 1")}</span> · {L("Nombres naturals i enters", "Números naturales y enteros", "Natural numbers and integers")}</h1>
    <p>{L("Els nombres naturals i la divisió entera, la divisibilitat (múltiples, divisors, criteris, nombres primers i descomposició), el mcm i el MCD amb els seus problemes, els nombres enters, les quatre operacions amb la regla dels signes, les operacions combinades i les potències i arrels amb enters: teoria explicada pas a pas, problemes resolts per nivells i eines interactives per a practicar.",
          "Los números naturales y la división entera, la divisibilidad (múltiplos, divisores, criterios, números primos y descomposición), el mcm y el MCD con sus problemas, los números enteros, las cuatro operaciones con la regla de los signos, las operaciones combinadas y las potencias y raíces con enteros: teoría explicada paso a paso, problemas resueltos por niveles y herramientas interactivas para practicar.",
          "Natural numbers and division with remainder, divisibility (multiples, divisors, rules, primes and factorisation), the lcm and gcd and their word problems, integers, the four operations with the sign rule, mixed operations, and powers and roots of integers: theory explained step by step, worked problems by level and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 1: Nombres naturals i enters · 2n ESO", "Apuntes de teoría · Unidad 1: Números naturales y enteros · 2º ESO", "Theory notes · Unit 1: Natural numbers and integers · 2nd ESO")}</p>
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

# FentMates: enllaça el tema comú (logo i colors del bloc) a les pàgines generades
import runpy as _runpy, os as _os
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "_eines":
    _d = _os.path.dirname(_d)
_runpy.run_path(_os.path.join(_d, "tema", "aplica.py"), run_name="__main__")
