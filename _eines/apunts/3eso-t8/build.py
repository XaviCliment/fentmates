import os, re, sys, math
import sympy as sp

# Genera materials/3eso/t8-funcio-lineal-quadratica.html. Ús: python3 _eines/apunts/3eso-t8/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js
# (fet a partir del de la unitat 7: lector d'expressions, plot(), entrenadors, qüestionari i navegació) i l'estil
# propi, a extra.css. Cada resultat dels exemples resolts es comprova amb sympy (pendents, rectes, punts de tall,
# vèrtexs i arrels).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/3eso/t8-funcio-lineal-quadratica.html")

def L(va, es, en):
    return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
def P(va, es, en): return '<p>' + L(va, es, en) + '</p>'
def box(cls, title, body):
    head = f'<div class="bh">{title}</div>' if title else ''
    return f'<div class="box {cls}">{head}<div class="bb">{body}</div></div>\n'
def note(va, es, en, icon='💡'): return f'<div class="note"><p>{icon} {L(va, es, en)}</p></div>'
def ul(*items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
def ol(*items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
LV = {1: ('★☆☆', 'Nivell 1 · Bàsic', 'Nivel 1 · Básico', 'Level 1 · Basic'),
      2: ('★★☆', 'Nivell 2 · Intermedi', 'Nivel 2 · Intermedio', 'Level 2 · Intermediate'),
      3: ('★★★', 'Nivell 3 · Avançat', 'Nivel 3 · Avanzado', 'Level 3 · Advanced')}
def level(k, start, *probs):
    s, va, es, en = LV[k]
    st = f' start="{start}"' if start > 1 else ''
    return (f'<div class="lvl-h"><span class="stars">{s}</span><h3>{L(va, es, en)}</h3></div>\n'
            + box('ex', '', f'<ol class="ex-list"{st}>' + ''.join(probs) + '</ol>'))
def levels(*groups):
    out, n = '', 1
    for k, probs in enumerate(groups, 1):
        out += level(k, n, *probs); n += len(probs)
    return out
def prob(q, *steps):
    return '<li><p class="prob-q">' + q + '</p><div class="steps">' + ''.join(f'<div class="step">{s}</div>' for s in steps) + '</div></li>\n'
def practice(items, sol):
    lis = ''.join(f'<li><span class="stars">{st}</span> {t}</li>' for st, t in items)
    return box('pr', '✍ ' + L('Practica', 'Practica', 'Practice'),
               f'<ol class="ex-list">{lis}</ol><details class="sol"><summary>{L("Mostra la solució", "Mostrar la solución", "Show the solution")}</summary><div>{sol}</div></details>')
def sec(i, title, body):
    return (f'\n<!-- ======================= 8.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">8.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)
I_ = Lt('i', 'y', 'and')

# ---------- ginys ----------
def drill(kind, va, es, en, mode='num'):
    if mode == 'opts':
        row = f'<div class="wrow dopts"></div><div class="wrow"><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
    else:
        ph = '(2, −3)' if mode == 'pair' else '…'
        hint = (L("Escriu el punt com (2, −3) o bé 2; −3.", "Escribe el punto como (2, −3) o bien 2; −3.", "Type the point as (2, −3) or 2; −3.") if mode == 'pair'
                else L("Escriu un nombre. Els decimals, amb coma (2,5) o amb punt; les fraccions, com 2/3.", "Escribe un número. Los decimales, con coma (2,5) o con punto; las fracciones, como 2/3.", "Type a number. Decimals with a point or a comma (2.5); fractions like 2/3."))
        row = (f'<div class="wrow"><label>{L("Resposta", "Respuesta", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat" placeholder="{ph}"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
               + '<p class="hint-s">' + hint + '</p>')
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  {row}<div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='w'):
    return f'<label>{lab} <input class="tin {cls}" type="text" inputmode="text" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def rng(k, lo, hi, step, val, lab):
    return f'<label style="flex:1">{lab} <span class="{k}v"></span><input type="range" data-k="{k}" min="{lo}" max="{hi}" step="{step}" value="{val}" aria-label="{k}"></label>'
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls='', attrs=''):
    idattr = f' id="{wid}"' if wid else ''
    return (f'<div class="widget{extra_cls}"{idattr}{attrs}>\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
def seg(items, first=0):
    return '<div class="wrow"><div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{str(i == first).lower()}">{t}</button>' for i, (k, t) in enumerate(items)) + '</div></div>'

# ---------- càlculs i comprovacions amb sympy ----------
x, y = sp.symbols('x y')
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def E(s): return sp.nsimplify(parse_expr(s.replace(',', '.'), transformations=TR, local_dict={'x': x}), rational=True)
R = sp.Rational
def Q(v): return sp.nsimplify(v, rational=True)
def same(a, b): assert sp.simplify(E(a) - E(b)) == 0, (a, b)
def im(s, a, want):
    v = E(s).subs(x, Q(a)); assert sp.simplify(v - Q(want)) == 0, (s, a, v, want); return v
def slope(Pp, Qq, want):
    m = (Q(Qq[1]) - Q(Pp[1])) / (Q(Qq[0]) - Q(Pp[0])); assert m == Q(want), (Pp, Qq, m, want); return m
def line(Pp, Qq, want):
    """la recta 'want' (y = ...) passa pels dos punts"""
    for A in (Pp, Qq): im(want, A[0], A[1])
    assert sp.degree(E(want), x) <= 1
def cut(f, g, want):
    s = sp.solve(sp.Eq(E(f), E(g)), x); assert len(s) == 1 and s[0] == Q(want[0]) and E(f).subs(x, s[0]) == Q(want[1]), (f, g, s, want)
def vert(f, want):
    p = sp.Poly(E(f), x); a, b, c = p.all_coeffs(); xv = -b / (2 * a)
    assert (xv, E(f).subs(x, xv)) == (Q(want[0]), Q(want[1])), (f, xv, want)
def roots(f, want):
    r = sorted([t for t in sp.solve(E(f), x) if t.is_real], key=float)
    assert r == sorted([Q(w) for w in want], key=float), (f, r, want)
def nt(v):
    v = sp.nsimplify(v)
    if v.is_Integer: return str(v)
    if v.is_Rational:
        d = float(v); s = '%g' % d
        if sp.nsimplify(s) == v: return s.replace('.', r'{,}')
        return (r'-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.p), v.q)
    return sp.latex(v)
def tv(xs, ys, xl='x', yl='y', cls=''):
    return ('<div class="tbl-wrap"><table class="data tv %s"><tbody><tr><th>\\(%s\\)</th>' % (cls, xl) + ''.join(f'<td>\\({v}\\)</td>' for v in xs)
            + '</tr><tr><th>\\(%s\\)</th>' % yl + ''.join(f'<td>\\({v}\\)</td>' for v in ys) + '</tr></tbody></table></div>')
def tvf(s, xs, xl='x', yl='y', cls=''):
    """taula de valors d'una fórmula (calculada amb sympy)"""
    return tv([nt(a) for a in xs], [nt(E(s).subs(x, Q(a))) for a in xs], xl=xl, yl=yl, cls=cls)

# ---------- gràfiques estàtiques (SVG), com plot() d'app.js ----------
def svg(win, fns=(), dots=(), segs=(), guides=(), xl='x', yl='y', xs=None, ys=None, W=300, H=None, gx=None, gy=None):
    x0, x1, y0, y1 = win
    H = H or round(W * (y1 - y0) / (x1 - x0))
    sx = lambda v: round((float(v) - x0) / (x1 - x0) * W, 1)
    sy = lambda v: round(H - (float(v) - y0) / (y1 - y0) * H, 1)
    xs = xs or (5 if x1 - x0 > 24 else 2 if x1 - x0 > 14 else 1); ys = ys or (5 if y1 - y0 > 24 else 2 if y1 - y0 > 14 else 1)
    g = ''
    for k in range(math.ceil(x0), math.floor(x1) + 1):
        if not gx or k % gx == 0: g += f'<line class="grid" x1="{sx(k)}" y1="0" x2="{sx(k)}" y2="{H}"/>'
    for k in range(math.ceil(y0), math.floor(y1) + 1):
        if not gy or k % gy == 0: g += f'<line class="grid" x1="0" y1="{sy(k)}" x2="{W}" y2="{sy(k)}"/>'
    ax = min(max(0, y0), y1); ay = min(max(0, x0), x1)
    g += f'<line class="ax" x1="0" y1="{sy(ax)}" x2="{W}" y2="{sy(ax)}"/><line class="ax" x1="{sx(ay)}" y1="0" x2="{sx(ay)}" y2="{H}"/>'
    k = math.ceil(x0 / xs) * xs
    while k < x1:
        if k and k > x0: g += f'<text class="tk" x="{sx(k)}" y="{sy(ax) + 13}" text-anchor="middle">{str(k).replace("-", "−")}</text>'
        k += xs
    k = math.ceil(y0 / ys) * ys
    while k < y1:
        if k and k > y0: g += f'<text class="tk" x="{sx(ay) - 5}" y="{sy(k) + 4}" text-anchor="end">{str(k).replace("-", "−")}</text>'
        k += ys
    g += f'<text class="tk ax-l" x="{W - 6}" y="{sy(ax) - 6}" text-anchor="end">{xl}</text><text class="tk ax-l" x="{sx(ay) + 6}" y="12">{yl}</text>'
    for gx_ in guides: g += f'<line class="guide" x1="{sx(gx_)}" y1="0" x2="{sx(gx_)}" y2="{H}"/>'
    for (A, B, cls) in segs: g += f'<path class="cv {cls}" d="M{sx(A[0])} {sy(A[1])}L{sx(B[0])} {sy(B[1])}"/>'
    for f in fns:
        s, cls, a, b = (tuple(f) + ('c0', None, None)[len(f) - 1:])[:4]
        fl = sp.lambdify(x, E(s))
        a = x0 if a is None else max(a, x0); b = x1 if b is None else min(b, x1)
        d, pen = '', False
        for i in range(401):
            t = a + (b - a) * i / 400
            v = float(fl(t))
            if v > y1 + (y1 - y0) or v < y0 - (y1 - y0): pen = False; continue
            d += ('L' if pen else 'M') + f'{sx(t)} {sy(v)}'; pen = True
        g += f'<path class="cv {cls}" d="{d}"/>'
    for dd in dots:
        px, py, cls, lab = (tuple(dd) + (None,))[:4]
        g += f'<circle class="{cls}" cx="{sx(px)}" cy="{sy(py)}" r="{6 if cls in ("cut", "mx", "mn", "bad") else 4.5}"/>'
        if lab: g += f'<text class="plab" x="{sx(px) + 8}" y="{sy(py) - 8}">{lab}</text>'
    return f'<svg class="sgraf" viewBox="0 0 {W} {H}" role="img" aria-label="gràfica">{g}</svg>'
def fig(s, cap=None): return f'<figure>{s}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{s}</figure>'
def figs(*f, three=False): return '<div class="figs%s">' % (' three' if three else '') + ''.join(f) + '</div>'
def tri(x0, y0, m, run=1): return [((x0, y0), (x0 + run, y0), 'tri'), ((x0 + run, y0), (x0 + run, y0 + m * run), 'tri')]

# =====================================================================
# 8.1 Funció de proporcionalitat directa
# =====================================================================
s1 = box('def', L('Funció de proporcionalitat directa', 'Función de proporcionalidad directa', 'Direct proportion function'),
  P(r"Dues magnituds són <strong>directament proporcionals</strong> si en multiplicar (o dividir) una per un nombre, l'altra queda multiplicada (o dividida) pel mateix nombre. La funció que les relaciona és",
    r"Dos magnitudes son <strong>directamente proporcionales</strong> si al multiplicar (o dividir) una por un número, la otra queda multiplicada (o dividida) por el mismo número. La función que las relaciona es",
    r"Two quantities are <strong>directly proportional</strong> if multiplying (or dividing) one by a number multiplies (or divides) the other by the same number. The function linking them is")
  + D(r"y=m\,x")
  + ul(L(r"\(m\) és la <strong>constant de proporcionalitat</strong>: \(m=\dfrac{y}{x}\) és el mateix per a tots els parells de la taula.", r"\(m\) es la <strong>constante de proporcionalidad</strong>: \(m=\dfrac{y}{x}\) es igual para todos los pares de la tabla.", r"\(m\) is the <strong>constant of proportionality</strong>: \(m=\dfrac{y}{x}\) is the same for every pair in the table."),
       L(r"La gràfica és una <strong>recta que passa per l'origen</strong> \((0,\,0)\).", r"La gráfica es una <strong>recta que pasa por el origen</strong> \((0,\,0)\).", r"The graph is a <strong>straight line through the origin</strong> \((0,\,0)\)."),
       L(r"\(m\) també s'anomena <strong>pendent</strong>: és el que augmenta (o disminueix) la \(y\) quan la \(x\) augmenta 1.", r"\(m\) también se llama <strong>pendiente</strong>: es lo que aumenta (o disminuye) la \(y\) cuando la \(x\) aumenta 1.", r"\(m\) is also called the <strong>slope</strong>: how much \(y\) goes up (or down) when \(x\) goes up by 1.")))
s1 += box('prop', L('El pendent i la inclinació', 'La pendiente y la inclinación', 'Slope and steepness'),
  ul(L(r"Si \(m>0\), la funció és <strong>creixent</strong> (la recta puja d'esquerra a dreta).", r"Si \(m>0\), la función es <strong>creciente</strong> (la recta sube de izquierda a derecha).", r"If \(m>0\), the function is <strong>increasing</strong> (the line goes up from left to right)."),
     L(r"Si \(m<0\), la funció és <strong>decreixent</strong> (la recta baixa).", r"Si \(m<0\), la función es <strong>decreciente</strong> (la recta baja).", r"If \(m<0\), the function is <strong>decreasing</strong> (the line goes down)."),
     L(r"Com més gran és \(|m|\), més <strong>inclinada</strong> és la recta.", r"Cuanto mayor es \(|m|\), más <strong>inclinada</strong> es la recta.", r"The bigger \(|m|\), the <strong>steeper</strong> the line."))
  + figs(fig(svg((-4, 4, -4, 4), fns=[('2x', 'c0'), ('x/2', 'c1')], segs=tri(0, 0, 2), W=220), r'\(y=2x\) · \(y=\tfrac12x\)'),
         fig(svg((-4, 4, -4, 4), fns=[('-3x', 'c0'), ('-x/3', 'c1')], segs=tri(0, 0, -3), W=220), r'\(y=-3x\) · \(y=-\tfrac13x\)'), three=True)
  + widget('', '📈', L('Juga amb el pendent de y = mx', 'Juega con la pendiente de y = mx', 'Play with the slope of y = mx'),
           ['<div class="wrow">' + rng('m', -4, 4, 0.25, 2, '') + '</div>',
            quick([('2|0', 'y = 2x'), ('0.5|0', 'y = 0,5x'), ('-1|0', 'y = −x'), ('-3|0', 'y = −3x'), ('1|0', 'y = x')])],
           out='<div class="gout"></div>', extra_cls=' w-line', attrs=' data-mode="prop"')
  + drill('propk', 'Entrena: la constant de proporcionalitat', 'Entrena: la constante de proporcionalidad', 'Train: the constant of proportionality'))
s1 += box('prop', L('Com es representa', 'Cómo se representa', 'How to draw it'),
  P(r"N'hi ha prou amb <strong>dos punts</strong>, i un ja el sabem: l'origen. Per a \(y=\tfrac32x\) agafem una \(x\) que faça la \(y\) entera, per exemple \(x=2\Rightarrow y=3\): unim \((0,\,0)\) i \((2,\,3)\).",
    r"Basta con <strong>dos puntos</strong>, y uno ya lo sabemos: el origen. Para \(y=\tfrac32x\) tomamos una \(x\) que haga la \(y\) entera, por ejemplo \(x=2\Rightarrow y=3\): unimos \((0,\,0)\) y \((2,\,3)\).",
    r"<strong>Two points</strong> are enough, and we already know one: the origin. For \(y=\tfrac32x\) choose an \(x\) that makes \(y\) a whole number, e.g. \(x=2\Rightarrow y=3\): join \((0,\,0)\) and \((2,\,3)\).")
  + figs(fig(svg((-3, 5, -3, 5), fns=[('3x/2', 'c0')], segs=tri(0, 0, 1.5, 2), dots=[(0, 0, 'cut', 'O'), (2, 3, 'pt p0', '(2, 3)')], W=240), r'\(y=\tfrac32x\)')))
im('3x/2', 2, 3)
s1 += levels(
 [prob(L(r"Un quilo de cireres costa 4,50 €. Escriu la funció que dona el preu \(y\) de \(x\) kg, fes una taula i digues quant costen 2,4 kg.", r"Un kilo de cerezas cuesta 4,50 €. Escribe la función que da el precio \(y\) de \(x\) kg, haz una tabla y di cuánto cuestan 2,4 kg.", r"A kilo of cherries costs €4.50. Write the function giving the price \(y\) of \(x\) kg, make a table and find the price of 2.4 kg."),
       D(r"y=4{,}5\,x"), tvf('4.5x', [0, 1, 2, 3, 4], xl=r'x\ (\text{kg})', yl=r'y\ (€)'),
       D(r"y(2{,}4)=4{,}5\cdot2{,}4=\boxed{10{,}80\ €}")),
  prob(L(r"Digues si la taula correspon a una funció de proporcionalitat directa i, si és així, escriu-la.", r"Di si la tabla corresponde a una función de proporcionalidad directa y, si es así, escríbela.", r"Say whether the table is a direct proportion and, if so, write its formula.") + tvf('-5x/2', [2, 4, 6, 10]),
       P(r"Calculem \(\dfrac{y}{x}\) per a cada parell:", r"Calculamos \(\dfrac{y}{x}\) para cada par:", r"Work out \(\dfrac{y}{x}\) for each pair:"),
       D(r"\frac{-5}{2}=\frac{-10}{4}=\frac{-15}{6}=\frac{-25}{10}=-2{,}5"),
       P(r"Sempre dona el mateix: <strong>sí</strong> que ho és, \(\boxed{y=-2{,}5x}\) (decreixent).", r"Siempre da lo mismo: <strong>sí</strong> lo es, \(\boxed{y=-2{,}5x}\) (decreciente).", r"It's always the same: it <strong>is</strong>, \(\boxed{y=-2.5x}\) (decreasing)."))],
 [prob(L(r"Una funció de proporcionalitat directa passa pel punt \((-4,\,6)\). Escriu-ne l'expressió i comprova si el punt \((10,\,-15)\) és de la gràfica.", r"Una función de proporcionalidad directa pasa por el punto \((-4,\,6)\). Escribe su expresión y comprueba si el punto \((10,\,-15)\) es de la gráfica.", r"A direct proportion goes through \((-4,\,6)\). Write its formula and check whether \((10,\,-15)\) is on the graph."),
       D(r"m=\frac{6}{-4}=-\frac32\ \Rightarrow\ \boxed{y=-\tfrac32x}"),
       D(r"x=10:\ y=-\tfrac32\cdot10=-15\ \checkmark"),
       P(r"<strong>Sí</strong>, el punt \((10,\,-15)\) és de la recta.", r"<strong>Sí</strong>, el punto \((10,\,-15)\) es de la recta.", r"<strong>Yes</strong>, \((10,\,-15)\) is on the line."))],
 [prob(L(r"Un cotxe gasta 6 litres de gasolina cada 100 km. Escriu el consum en funció dels km recorreguts. Quants km pot fer amb un dipòsit de 45 L?", r"Un coche gasta 6 litros de gasolina cada 100 km. Escribe el consumo en función de los km recorridos. ¿Cuántos km puede hacer con un depósito de 45 L?", r"A car uses 6 litres of petrol every 100 km. Write the consumption as a function of the distance. How far can it go on a 45 L tank?"),
       D(r"m=\frac{6}{100}=0{,}06\ \text{L/km}\ \Rightarrow\ y=0{,}06\,x"),
       D(r"0{,}06\,x=45\Rightarrow x=\frac{45}{0{,}06}=\boxed{750\ \text{km}}"))])
im('4.5x', R(12, 5), R(108, 10)); [im('-5x/2', a, R(-5, 2) * a) for a in (2, 4, 6, 10)]
im('-3x/2', -4, 6); im('-3x/2', 10, -15); im('0.06x', 750, 45)
s1 += practice([
  ('★', L(r"a) Quina és la constant de proporcionalitat de \(y=-4x\)? És creixent o decreixent? b) Escriu la funció «perímetre d'un quadrat de costat \(x\)».", r"a) ¿Cuál es la constante de proporcionalidad de \(y=-4x\)? ¿Es creciente o decreciente? b) Escribe la función «perímetro de un cuadrado de lado \(x\)».", r"a) What is the constant of proportionality of \(y=-4x\)? Is it increasing or decreasing? b) Write the function “perimeter of a square with side \(x\)”.")),
  ('★★', L(r"c) Troba la funció de proporcionalitat que passa per \((3,\,2)\). d) Quina de les rectes \(y=5x\) i \(y=\tfrac15x\) és més inclinada?", r"c) Halla la función de proporcionalidad que pasa por \((3,\,2)\). d) ¿Cuál de las rectas \(y=5x\) e \(y=\tfrac15x\) es más inclinada?", r"c) Find the direct proportion through \((3,\,2)\). d) Which of the lines \(y=5x\) and \(y=\tfrac15x\) is steeper?")),
  ('★★★', L(r"e) Per a fer 3 pastissos calen 750 g de farina. Escriu la farina en funció del nombre de pastissos i calcula'n la quantitat per a 7 pastissos.", r"e) Para hacer 3 pasteles se necesitan 750 g de harina. Escribe la harina en función del número de pasteles y calcula la cantidad para 7 pasteles.", r"e) You need 750 g of flour for 3 cakes. Write the flour as a function of the number of cakes and work out how much you need for 7 cakes."))],
  P(r"a) \(m=-4\): decreixent. b) \(P=4x\). c) \(y=\tfrac23x\). d) \(y=5x\) (\(5>\tfrac15\)). e) \(m=\tfrac{750}{3}=250\): \(y=250x\); \(y(7)=1750\) g.",
    r"a) \(m=-4\): decreciente. b) \(P=4x\). c) \(y=\tfrac23x\). d) \(y=5x\) (\(5>\tfrac15\)). e) \(m=\tfrac{750}{3}=250\): \(y=250x\); \(y(7)=1750\) g.",
    r"a) \(m=-4\): decreasing. b) \(P=4x\). c) \(y=\tfrac23x\). d) \(y=5x\) (\(5>\tfrac15\)). e) \(m=\tfrac{750}{3}=250\): \(y=250x\); \(y(7)=1750\) g."))
im('2x/3', 3, 2); im('250x', 7, 1750)

# =====================================================================
# 8.2 Funció lineal (afí)
# =====================================================================
s2 = box('def', L('Funció lineal o afí', 'Función lineal o afín', 'Linear (affine) function'),
  D(r"y=m\,x+n")
  + ul(L(r"\(m\) és el <strong>pendent</strong>: el que varia la \(y\) quan la \(x\) augmenta 1.", r"\(m\) es la <strong>pendiente</strong>: lo que varía la \(y\) cuando la \(x\) aumenta 1.", r"\(m\) is the <strong>slope</strong>: how much \(y\) changes when \(x\) goes up by 1."),
       L(r"\(n\) és l'<strong>ordenada en l'origen</strong>: la recta talla l'eix \(Y\) en el punt \((0,\,n)\).", r"\(n\) es la <strong>ordenada en el origen</strong>: la recta corta el eje \(Y\) en el punto \((0,\,n)\).", r"\(n\) is the <strong>\(y\)-intercept</strong>: the line crosses the \(Y\) axis at \((0,\,n)\)."))
  + P(r"La gràfica és una <strong>recta</strong>, paral·lela a la de \(y=mx\) però desplaçada \(n\) unitats cap amunt (o cap avall si \(n<0\)). Si \(n=0\), és de proporcionalitat directa.",
      r"La gráfica es una <strong>recta</strong>, paralela a la de \(y=mx\) pero desplazada \(n\) unidades hacia arriba (o hacia abajo si \(n<0\)). Si \(n=0\), es de proporcionalidad directa.",
      r"The graph is a <strong>straight line</strong>, parallel to \(y=mx\) but shifted \(n\) units up (or down if \(n<0\)). If \(n=0\), it is a direct proportion.")
  + figs(fig(svg((-4, 4, -4, 5), fns=[('2x', 'c1 dash'), ('2x+3', 'c0')], dots=[(0, 3, 'cut', '(0, 3)')], W=230), r'\(y=2x\) · \(y=2x+3\)')))
s2 += box('prop', L('Funció constant i rectes verticals', 'Función constante y rectas verticales', 'Constant functions and vertical lines'),
  ul(L(r"Si \(m=0\), \(y=n\) és una <strong>funció constant</strong>: una recta <strong>horitzontal</strong>.", r"Si \(m=0\), \(y=n\) es una <strong>función constante</strong>: una recta <strong>horizontal</strong>.", r"If \(m=0\), \(y=n\) is a <strong>constant function</strong>: a <strong>horizontal</strong> line."),
     L(r"Les rectes <strong>verticals</strong> \(x=k\) <strong>no</strong> són funcions: al valor \(k\) li corresponen infinites \(y\).", r"Las rectas <strong>verticales</strong> \(x=k\) <strong>no</strong> son funciones: al valor \(k\) le corresponden infinitas \(y\).", r"<strong>Vertical</strong> lines \(x=k\) are <strong>not</strong> functions: \(k\) goes with infinitely many \(y\) values."))
  + figs(fig(svg((-4, 4, -4, 4), fns=[('2', 'c0')], W=200), r'\(y=2\)'), fig(svg((-4, 4, -4, 4), segs=[((-3, -4), (-3, 4), 'c1')], W=200), r'\(x=-3\)'), three=True))
s2 += box('prop', L('Representar una recta', 'Representar una recta', 'Drawing a line'),
  ol(L(r"Marquem l'ordenada en l'origen: \((0,\,n)\).", r"Marcamos la ordenada en el origen: \((0,\,n)\).", r"Mark the intercept \((0,\,n)\)."),
     L(r"Des d'aquest punt, avancem 1 cap a la dreta i pugem \(m\) (o baixem si \(m<0\)). Si \(m=\tfrac{p}{q}\) és una fracció, avancem \(q\) i pugem \(p\).", r"Desde ese punto, avanzamos 1 hacia la derecha y subimos \(m\) (o bajamos si \(m<0\)). Si \(m=\tfrac{p}{q}\) es una fracción, avanzamos \(q\) y subimos \(p\).", r"From there, move 1 to the right and \(m\) up (or down if \(m<0\)). If \(m=\tfrac{p}{q}\) is a fraction, move \(q\) right and \(p\) up."),
     L(r"Unim els dos punts. (També podem fer una taula de valors amb dos o tres punts.)", r"Unimos los dos puntos. (También podemos hacer una tabla de valores con dos o tres puntos.)", r"Join the two points. (A table with two or three points works too.)"))
  + figs(fig(svg((-4, 5, -4, 4), fns=[('-2x/3+2', 'c0')], segs=tri(0, 2, R(-2, 3), 3), dots=[(0, 2, 'cut', '(0, 2)'), (3, 0, 'pt p0', '(3, 0)')], W=250), r'\(y=-\tfrac23x+2\)'))
  + widget('', '📐', L('Juga amb m i n en y = mx + n', 'Juega con m y n en y = mx + n', 'Play with m and n in y = mx + n'),
           ['<div class="wrow">' + rng('m', -4, 4, 0.25, 1, '') + rng('n', -5, 5, 0.5, 2, '') + '</div>',
            quick([('2|-3', 'y = 2x − 3'), ('-1|4', 'y = −x + 4'), ('0.5|1', 'y = 0,5x + 1'), ('0|3', 'y = 3'), ('-2|0', 'y = −2x')])],
           out='<div class="gout"></div>', extra_cls=' w-line', attrs=' data-mode="afi"')
  + drill('mn', "Entrena: l'equació a partir de la gràfica", 'Entrena: la ecuación a partir de la gráfica', 'Train: the equation from the graph', 'opts'))
im('-2x/3+2', 3, 0)
s2 += box('prop', L("Talls amb els eixos", "Cortes con los ejes", "Where the line crosses the axes"),
  ul(L(r"Amb l'eix \(Y\): fem \(x=0\) → \((0,\,n)\).", r"Con el eje \(Y\): hacemos \(x=0\) → \((0,\,n)\).", r"\(Y\) axis: set \(x=0\) → \((0,\,n)\)."),
     L(r"Amb l'eix \(X\): fem \(y=0\) i resolem \(mx+n=0\).", r"Con el eje \(X\): hacemos \(y=0\) y resolvemos \(mx+n=0\).", r"\(X\) axis: set \(y=0\) and solve \(mx+n=0\)."))
  + D(r"y=3x-6:\quad x=0\Rightarrow(0,\,-6);\qquad 3x-6=0\Rightarrow x=2\Rightarrow(2,\,0)"))
roots('3x-6', [2]); im('3x-6', 0, -6)
s2 += levels(
 [prob(L(r"Indica el pendent i l'ordenada en l'origen de cada funció i digues si és creixent o decreixent: a) \(y=4x-1\); b) \(y=-x+\tfrac12\); c) \(y=5\); d) \(y=\dfrac{2-3x}{4}\).", r"Indica la pendiente y la ordenada en el origen de cada función y di si es creciente o decreciente: a) \(y=4x-1\); b) \(y=-x+\tfrac12\); c) \(y=5\); d) \(y=\dfrac{2-3x}{4}\).", r"Give the slope and intercept of each function and say whether it is increasing or decreasing: a) \(y=4x-1\); b) \(y=-x+\tfrac12\); c) \(y=5\); d) \(y=\dfrac{2-3x}{4}\)."),
       P(r"a) \(m=4,\ n=-1\): creixent. b) \(m=-1,\ n=\tfrac12\): decreixent. c) \(m=0,\ n=5\): constant.", r"a) \(m=4,\ n=-1\): creciente. b) \(m=-1,\ n=\tfrac12\): decreciente. c) \(m=0,\ n=5\): constante.", r"a) \(m=4,\ n=-1\): increasing. b) \(m=-1,\ n=\tfrac12\): decreasing. c) \(m=0,\ n=5\): constant."),
       P(r"d) Primer la separem en dos termes:", r"d) Primero la separamos en dos términos:", r"d) First split it into two terms:"), D(r"y=\frac24-\frac34x=-\frac34x+\frac12\ \Rightarrow\ m=-\tfrac34,\ n=\tfrac12\ \text{(%s)}" % Lt('decreixent', 'decreciente', 'decreasing')))],
 [prob(L(r"Representa \(y=\tfrac12x-3\) i troba els talls amb els eixos.", r"Representa \(y=\tfrac12x-3\) y halla los cortes con los ejes.", r"Draw \(y=\tfrac12x-3\) and find where it crosses the axes."),
       tvf('x/2-3', [-2, 0, 2, 4, 6]),
       D(r"x=0\Rightarrow(0,\,-3)\qquad \tfrac12x-3=0\Rightarrow x=6\Rightarrow(6,\,0)"),
       figs(fig(svg((-3, 8, -5, 2), fns=[('x/2-3', 'c0')], dots=[(0, -3, 'cut', '(0, −3)'), (6, 0, 'cut', '(6, 0)')], W=260))))],
 [prob(L(r"Troba el valor de \(k\) perquè la recta \(y=kx+5\) passe pel punt \((2,\,-1)\). Quin és el seu tall amb l'eix \(X\)?", r"Halla el valor de \(k\) para que la recta \(y=kx+5\) pase por el punto \((2,\,-1)\). ¿Cuál es su corte con el eje \(X\)?", r"Find \(k\) so that \(y=kx+5\) goes through \((2,\,-1)\). Where does it cross the \(X\) axis?"),
       D(r"-1=k\cdot2+5\Rightarrow 2k=-6\Rightarrow \boxed{k=-3}"),
       D(r"y=-3x+5:\quad -3x+5=0\Rightarrow x=\tfrac53\Rightarrow\left(\tfrac53,\,0\right)"))])
same('(2-3x)/4', '-3x/4+1/2'); roots('x/2-3', [6]); im('-3x+5', 2, -1); roots('-3x+5', [R(5, 3)])
s2 += practice([
  ('★', L(r"a) Escriu la recta de pendent \(-2\) i ordenada en l'origen 3. b) La recta \(y=x-4\), passa per \((1,\,-3)\)?", r"a) Escribe la recta de pendiente \(-2\) y ordenada en el origen 3. b) La recta \(y=x-4\), ¿pasa por \((1,\,-3)\)?", r"a) Write the line with slope \(-2\) and intercept 3. b) Does \(y=x-4\) go through \((1,\,-3)\)?")),
  ('★★', L(r"c) Troba els talls amb els eixos de \(y=-2x+8\). d) Escriu la recta horitzontal que passa per \((5,\,-1)\).", r"c) Halla los cortes con los ejes de \(y=-2x+8\). d) Escribe la recta horizontal que pasa por \((5,\,-1)\).", r"c) Find where \(y=-2x+8\) crosses the axes. d) Write the horizontal line through \((5,\,-1)\).")),
  ('★★★', L(r"e) Escriu en la forma \(y=mx+n\) la recta \(2x+3y=12\) i digues-ne el pendent.", r"e) Escribe en la forma \(y=mx+n\) la recta \(2x+3y=12\) y di su pendiente.", r"e) Write the line \(2x+3y=12\) as \(y=mx+n\) and give its slope."))],
  P(r"a) \(y=-2x+3\). b) Sí: \(1-4=-3\). c) \((0,\,8)\) i \((4,\,0)\). d) \(y=-1\). e) \(3y=-2x+12\Rightarrow y=-\tfrac23x+4\), \(m=-\tfrac23\).",
    r"a) \(y=-2x+3\). b) Sí: \(1-4=-3\). c) \((0,\,8)\) y \((4,\,0)\). d) \(y=-1\). e) \(3y=-2x+12\Rightarrow y=-\tfrac23x+4\), \(m=-\tfrac23\).",
    r"a) \(y=-2x+3\). b) Yes: \(1-4=-3\). c) \((0,\,8)\) and \((4,\,0)\). d) \(y=-1\). e) \(3y=-2x+12\Rightarrow y=-\tfrac23x+4\), \(m=-\tfrac23\)."))
im('x-4', 1, -3); roots('-2x+8', [4]); same('(12-2x)/3', '-2x/3+4')

# =====================================================================
# 8.3 Equació d'una recta
# =====================================================================
s3 = box('def', L('Pendent a partir de dos punts', 'Pendiente a partir de dos puntos', 'Slope from two points'),
  P(r"Si una recta passa per \(A(x_1,\,y_1)\) i \(B(x_2,\,y_2)\), el pendent és el quocient entre el que puja la \(y\) i el que avança la \(x\):",
    r"Si una recta pasa por \(A(x_1,\,y_1)\) y \(B(x_2,\,y_2)\), la pendiente es el cociente entre lo que sube la \(y\) y lo que avanza la \(x\):",
    r"If a line goes through \(A(x_1,\,y_1)\) and \(B(x_2,\,y_2)\), the slope is how much \(y\) rises divided by how much \(x\) advances:")
  + D(r"m=\frac{y_2-y_1}{x_2-x_1}")
  + figs(fig(svg((-2, 7, -2, 6), fns=[('2x/3+1', 'c0')], segs=[((0, 1), (3, 1), 'tri'), ((3, 1), (3, 3), 'tri')], dots=[(0, 1, 'pt p0', 'A'), (3, 3, 'pt p1', 'B')], W=250), r'\(m=\tfrac{3-1}{3-0}=\tfrac23\)')))
slope((0, 1), (3, 3), R(2, 3))
s3 += box('prop', L("Equació punt-pendent", "Ecuación punto-pendiente", "Point-slope form"),
  P(r"La recta de pendent \(m\) que passa pel punt \((x_0,\,y_0)\) té per equació", r"La recta de pendiente \(m\) que pasa por el punto \((x_0,\,y_0)\) tiene por ecuación", r"The line with slope \(m\) through \((x_0,\,y_0)\) has equation")
  + D(r"y-y_0=m\,(x-x_0)")
  + P(r"Per a trobar la recta que passa per <strong>dos punts</strong>: 1) calculem el pendent; 2) fem servir l'equació punt-pendent amb un dels dos punts; 3) aïllem la \(y\).",
      r"Para hallar la recta que pasa por <strong>dos puntos</strong>: 1) calculamos la pendiente; 2) usamos la ecuación punto-pendiente con uno de los dos puntos; 3) despejamos la \(y\).",
      r"To find the line through <strong>two points</strong>: 1) work out the slope; 2) use the point-slope form with one of the points; 3) solve for \(y\).")
  + P(r"Exemple: recta per \(A(1,\,-2)\) i \(B(4,\,7)\).", r"Ejemplo: recta por \(A(1,\,-2)\) y \(B(4,\,7)\).", r"Example: the line through \(A(1,\,-2)\) and \(B(4,\,7)\).")
  + D(r"m=\frac{7-(-2)}{4-1}=\frac93=3\qquad y-(-2)=3(x-1)\ \Rightarrow\ y+2=3x-3\ \Rightarrow\ \boxed{y=3x-5}")
  + note(r"Comprova sempre el resultat amb l'altre punt: \(3\cdot4-5=7\ \checkmark\).", r"Comprueba siempre el resultado con el otro punto: \(3\cdot4-5=7\ \checkmark\).", r"Always check with the other point: \(3\cdot4-5=7\ \checkmark\).", '✅')
  + widget('w-two', '📍', L('La recta que passa per dos punts', 'La recta que pasa por dos puntos', 'The line through two points'),
           ['<div class="wrow">' + tin('p', 'P =', '(1, -2)', 's2') + tin('q', 'Q =', '(4, 7)', 's2') + '</div>',
            quick([('(1, -2)|(4, 7)', '(1, −2), (4, 7)'), ('(-2, 3)|(2, 1)', '(−2, 3), (2, 1)'), ('(0, 4)|(3, 4)', '(0, 4), (3, 4)'), ('(2, 1)|(2, 5)', '(2, 1), (2, 5)'), ('(-3, -1)|(3, 3)', '(−3, −1), (3, 3)')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('slope', 'Entrena: calcula el pendent', 'Entrena: calcula la pendiente', 'Train: work out the slope')
  + drill('eq2', "Entrena: l'equació per dos punts", 'Entrena: la ecuación por dos puntos', 'Train: the equation through two points', 'opts'))
slope((1, -2), (4, 7), 3); line((1, -2), (4, 7), '3x-5'); line((-2, 3), (2, 1), '-x/2+2'); line((-3, -1), (3, 3), '2x/3+1')
s3 += box('prop', L("Forma general (implícita)", "Forma general (implícita)", "General form"),
  P(r"Tota recta es pot escriure com \(ax+by+c=0\). Per a passar a la forma \(y=mx+n\) (<em>explícita</em>) aïllem la \(y\):",
    r"Toda recta se puede escribir como \(ax+by+c=0\). Para pasar a la forma \(y=mx+n\) (<em>explícita</em>) despejamos la \(y\):",
    r"Every line can be written as \(ax+by+c=0\). To get the form \(y=mx+n\) (<em>explicit</em>) solve for \(y\):")
  + D(r"4x-2y+6=0\Rightarrow -2y=-4x-6\Rightarrow y=2x+3")
  + P(r"Si \(b=0\), queda \(x=k\): una recta vertical.", r"Si \(b=0\), queda \(x=k\): una recta vertical.", r"If \(b=0\), we get \(x=k\): a vertical line."))
same('(4x+6)/2', '2x+3')
s3 += box('prop', L("Rectes paral·leles", "Rectas paralelas", "Parallel lines"),
  P(r"Dues rectes són <strong>paral·leles</strong> si tenen el <strong>mateix pendent</strong>. La paral·lela a \(y=-2x+1\) que passa per \((3,\,4)\):",
    r"Dos rectas son <strong>paralelas</strong> si tienen la <strong>misma pendiente</strong>. La paralela a \(y=-2x+1\) que pasa por \((3,\,4)\):",
    r"Two lines are <strong>parallel</strong> if they have the <strong>same slope</strong>. The parallel to \(y=-2x+1\) through \((3,\,4)\):")
  + D(r"m=-2:\quad y-4=-2(x-3)\Rightarrow \boxed{y=-2x+10}"))
im('-2x+10', 3, 4)
s3 += levels(
 [prob(L(r"Calcula el pendent de la recta que passa per \(A(-1,\,5)\) i \(B(3,\,-3)\). És creixent o decreixent?", r"Calcula la pendiente de la recta que pasa por \(A(-1,\,5)\) y \(B(3,\,-3)\). ¿Es creciente o decreciente?", r"Work out the slope of the line through \(A(-1,\,5)\) and \(B(3,\,-3)\). Increasing or decreasing?"),
       D(r"m=\frac{-3-5}{3-(-1)}=\frac{-8}{4}=-2"), P(r"\(m<0\): <strong>decreixent</strong>.", r"\(m<0\): <strong>decreciente</strong>.", r"\(m<0\): <strong>decreasing</strong>.")),
  prob(L(r"Escriu l'equació de la recta de pendent \(\tfrac12\) que passa per \((4,\,-1)\).", r"Escribe la ecuación de la recta de pendiente \(\tfrac12\) que pasa por \((4,\,-1)\).", r"Write the line with slope \(\tfrac12\) through \((4,\,-1)\)."),
       D(r"y-(-1)=\tfrac12(x-4)\Rightarrow y+1=\tfrac12x-2\Rightarrow\boxed{y=\tfrac12x-3}"))],
 [prob(L(r"Troba l'equació de la recta que passa per \((-2,\,7)\) i \((4,\,-2)\) i el seu tall amb l'eix \(Y\).", r"Halla la ecuación de la recta que pasa por \((-2,\,7)\) y \((4,\,-2)\) y su corte con el eje \(Y\).", r"Find the line through \((-2,\,7)\) and \((4,\,-2)\) and its \(Y\)-intercept."),
       D(r"m=\frac{-2-7}{4-(-2)}=\frac{-9}{6}=-\frac32"),
       D(r"y-7=-\tfrac32(x+2)\Rightarrow y=-\tfrac32x-3+7\Rightarrow\boxed{y=-\tfrac32x+4}"),
       P(r"Talla l'eix \(Y\) en \((0,\,4)\). Comprovació: \(-\tfrac32\cdot4+4=-2\ \checkmark\)", r"Corta el eje \(Y\) en \((0,\,4)\). Comprobación: \(-\tfrac32\cdot4+4=-2\ \checkmark\)", r"It crosses the \(Y\) axis at \((0,\,4)\). Check: \(-\tfrac32\cdot4+4=-2\ \checkmark\)"))],
 [prob(L(r"Estan alineats els punts \(A(-1,\,-4)\), \(B(1,\,2)\) i \(C(3,\,7)\)?", r"¿Están alineados los puntos \(A(-1,\,-4)\), \(B(1,\,2)\) y \(C(3,\,7)\)?", r"Are the points \(A(-1,\,-4)\), \(B(1,\,2)\) and \(C(3,\,7)\) on one line?"),
       P(r"Si estan alineats, el pendent de \(AB\) i el de \(BC\) han de ser iguals:", r"Si están alineados, la pendiente de \(AB\) y la de \(BC\) deben ser iguales:", r"If they are on one line, the slopes of \(AB\) and \(BC\) must be equal:"),
       D(r"m_{AB}=\frac{2-(-4)}{1-(-1)}=\frac62=3\qquad m_{BC}=\frac{7-2}{3-1}=\frac52"),
       P(r"\(3\neq\tfrac52\): <strong>no</strong> estan alineats.", r"\(3\neq\tfrac52\): <strong>no</strong> están alineados.", r"\(3\neq\tfrac52\): they are <strong>not</strong> on one line."))])
slope((-1, 5), (3, -3), -2); im('x/2-3', 4, -1); line((-2, 7), (4, -2), '-3x/2+4'); slope((-1, -4), (1, 2), 3); slope((1, 2), (3, 7), R(5, 2))
s3 += practice([
  ('★', L(r"a) Pendent de la recta que passa per \((0,\,3)\) i \((2,\,9)\). b) Recta de pendent \(-3\) que passa per \((1,\,1)\).", r"a) Pendiente de la recta que pasa por \((0,\,3)\) y \((2,\,9)\). b) Recta de pendiente \(-3\) que pasa por \((1,\,1)\).", r"a) Slope of the line through \((0,\,3)\) and \((2,\,9)\). b) Line with slope \(-3\) through \((1,\,1)\).")),
  ('★★', L(r"c) Recta que passa per \((-3,\,2)\) i \((3,\,-2)\). d) Passa a la forma explícita: \(3x+y-5=0\).", r"c) Recta que pasa por \((-3,\,2)\) y \((3,\,-2)\). d) Pasa a la forma explícita: \(3x+y-5=0\).", r"c) Line through \((-3,\,2)\) and \((3,\,-2)\). d) Write in explicit form: \(3x+y-5=0\).")),
  ('★★★', L(r"e) Escriu la recta paral·lela a \(y=\tfrac34x\) que passa per \((4,\,-1)\).", r"e) Escribe la recta paralela a \(y=\tfrac34x\) que pasa por \((4,\,-1)\).", r"e) Write the line parallel to \(y=\tfrac34x\) through \((4,\,-1)\)."))],
  P(r"a) \(m=3\). b) \(y=-3x+4\). c) \(y=-\tfrac23x\). d) \(y=-3x+5\). e) \(y=\tfrac34x-4\).", r"a) \(m=3\). b) \(y=-3x+4\). c) \(y=-\tfrac23x\). d) \(y=-3x+5\). e) \(y=\tfrac34x-4\).", r"a) \(m=3\). b) \(y=-3x+4\). c) \(y=-\tfrac23x\). d) \(y=-3x+5\). e) \(y=\tfrac34x-4\)."))
slope((0, 3), (2, 9), 3); im('-3x+4', 1, 1); line((-3, 2), (3, -2), '-2x/3'); im('3x/4-4', 4, -1)

# =====================================================================
# 8.4 Aplicacions de la funció lineal
# =====================================================================
s4 = box('prop', L('On apareixen les funcions lineals', 'Dónde aparecen las funciones lineales', 'Where linear functions appear'),
  P(r"Moltes situacions tenen una part <strong>fixa</strong> i una part que creix (o decreix) al mateix <strong>ritme</strong>. Aleshores són funcions lineals \(y=mx+n\): \(n\) és el valor inicial (quan \(x=0\)) i \(m\), el ritme de canvi per unitat.",
    r"Muchas situaciones tienen una parte <strong>fija</strong> y una parte que crece (o decrece) al mismo <strong>ritmo</strong>. Entonces son funciones lineales \(y=mx+n\): \(n\) es el valor inicial (cuando \(x=0\)) y \(m\), el ritmo de cambio por unidad.",
    r"Many situations have a <strong>fixed</strong> part and a part that grows (or shrinks) at a steady <strong>rate</strong>. They are linear functions \(y=mx+n\): \(n\) is the starting value (when \(x=0\)) and \(m\) the rate of change per unit.")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Situació', 'Situación', 'Situation') + '</th><th>' + L('Funció', 'Función', 'Function') + '</th><th>\\(m\\)</th><th>\\(n\\)</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in [
    (L("Taxi: 3 € de baixada de bandera i 1,20 € per km", "Taxi: 3 € de bajada de bandera y 1,20 € por km", "Taxi: €3 to get in and €1.20 per km"), r'\(P=1{,}2x+3\)', L('preu per km', 'precio por km', 'price per km'), L('preu fix', 'precio fijo', 'fixed price')),
    (L("Moviment a velocitat constant (MRU)", "Movimiento a velocidad constante (MRU)", "Motion at constant speed"), r'\(d=d_0+v\,t\)', L('velocitat', 'velocidad', 'speed'), L('posició inicial', 'posición inicial', 'starting position')),
    (L("Graus Celsius → Fahrenheit", "Grados Celsius → Fahrenheit", "Celsius → Fahrenheit"), r'\(F=1{,}8\,C+32\)', '1,8', '32'),
    (L("Un dipòsit de 500 L que es buida a 25 L/min", "Un depósito de 500 L que se vacía a 25 L/min", "A 500 L tank draining at 25 L/min"), r'\(V=500-25t\)', r'\(-25\)', '500')])
  + '</tbody></table></div>'
  + note(r"En un problema, la fórmula només té sentit per a alguns valors de \(x\) (el temps no és negatiu, el dipòsit no pot tindre menys de 0 L…).", r"En un problema, la fórmula solo tiene sentido para algunos valores de \(x\) (el tiempo no es negativo, el depósito no puede tener menos de 0 L…).", r"In a word problem the formula only makes sense for some values of \(x\) (time isn't negative, the tank can't hold less than 0 L…).", '⚠')
  + widget('w-apl', '🚕', L('Situacions lineals', 'Situaciones lineales', 'Linear situations'),
           [seg([(str(i), n) for i, n in enumerate(['Taxi', 'Temperatura', 'Dipòsit', 'Ciclista'])]),
            '<div class="wrow"><label style="flex:1">' + L('Mou el valor de x', 'Mueve el valor de x', 'Move the value of x') + ' <input type="range" min="0" max="100" step="1" value="40" aria-label="x"></label></div>'],
           out='<div class="gout"></div>')
  + drill('apl', 'Entrena: problemes de funcions lineals', 'Entrena: problemas de funciones lineales', 'Train: linear-function word problems'))
im('1.8x+32', 100, 212); im('500-25x', 20, 0)
s4 += box('prop', L('Com es resol un problema', 'Cómo se resuelve un problema', 'How to solve a word problem'),
  ol(L(r"Identifica les variables: què és la \(x\) i què és la \(y\) (amb unitats).", r"Identifica las variables: qué es la \(x\) y qué es la \(y\) (con unidades).", r"Identify the variables: what are \(x\) and \(y\) (with units)."),
     L(r"Troba \(m\) (el ritme) i \(n\) (el valor inicial). Si et donen dos parells de valors, calcula la recta que passa per aquests dos punts.", r"Halla \(m\) (el ritmo) y \(n\) (el valor inicial). Si te dan dos pares de valores, calcula la recta que pasa por esos dos puntos.", r"Find \(m\) (the rate) and \(n\) (the starting value). If you're given two pairs of values, find the line through those two points."),
     L(r"Escriu la fórmula, respon i interpreta el resultat.", r"Escribe la fórmula, responde e interpreta el resultado.", r"Write the formula, answer and interpret the result.")))
s4 += levels(
 [prob(L(r"Una empresa de lloguer de bicicletes cobra 5 € per l'assegurança i 2,50 € per hora. Escriu el preu en funció de les hores. Quant costen 4 h? Quantes hores pots llogar-la amb 25 €?", r"Una empresa de alquiler de bicicletas cobra 5 € por el seguro y 2,50 € por hora. Escribe el precio en función de las horas. ¿Cuánto cuestan 4 h? ¿Cuántas horas puedes alquilarla con 25 €?", r"A bike-hire firm charges €5 insurance plus €2.50 per hour. Write the price as a function of the hours. How much do 4 h cost? How many hours can you get for €25?"),
       D(r"P(x)=2{,}5x+5"), D(r"P(4)=2{,}5\cdot4+5=\boxed{15\ €}\qquad 2{,}5x+5=25\Rightarrow 2{,}5x=20\Rightarrow\boxed{x=8\ \text{h}}"))],
 [prob(L(r"Un rellotge de sorra té 300 g de sorra a la part de dalt i en cauen 12 g per minut. Escriu la sorra de dalt en funció del temps, digues el domini amb sentit i representa-la.", r"Un reloj de arena tiene 300 g de arena en la parte de arriba y caen 12 g por minuto. Escribe la arena de arriba en función del tiempo, di el dominio con sentido y represéntala.", r"An hourglass has 300 g of sand at the top and 12 g fall each minute. Write the sand at the top as a function of time, give the meaningful domain and draw it."),
       D(r"S(t)=300-12t"), D(r"S(t)=0\Rightarrow 12t=300\Rightarrow t=25\ \text{min}\qquad \text{Dom}=[0,\,25]"),
       figs(fig(svg((-2, 28, -30, 330), fns=[('300-12x', 'c0', 0, 25)], dots=[(0, 300, 'cut', '(0, 300)'), (25, 0, 'cut', '(25, 0)')], xl='t', yl='S', xs=5, ys=50, gx=5, gy=50, W=280, H=220))))],
 [prob(L(r"L'aigua bull a 100 °C, que són 212 °F, i es congela a 0 °C, que són 32 °F. Sabent que la relació és lineal, troba la fórmula que passa de °C a °F. A quina temperatura coincideixen les dues escales?", r"El agua hierve a 100 °C, que son 212 °F, y se congela a 0 °C, que son 32 °F. Sabiendo que la relación es lineal, halla la fórmula que pasa de °C a °F. ¿A qué temperatura coinciden las dos escalas?", r"Water boils at 100 °C, which is 212 °F, and freezes at 0 °C, which is 32 °F. The relation is linear: find the formula from °C to °F. At what temperature do both scales agree?"),
       D(r"m=\frac{212-32}{100-0}=\frac{180}{100}=1{,}8\qquad n=32\ \Rightarrow\ F=1{,}8\,C+32"),
       D(r"F=C:\ C=1{,}8\,C+32\Rightarrow -0{,}8\,C=32\Rightarrow \boxed{C=-40}"),
       P(r"\(-40\ °C=-40\ °F\).", r"\(-40\ °C=-40\ °F\).", r"\(-40\ °C=-40\ °F\)."))])
im('2.5x+5', 4, 15); im('2.5x+5', 8, 25); roots('300-12x', [25]); line((0, 32), (100, 212), '1.8x+32'); cut('1.8x+32', 'x', (-40, -40))
s4 += practice([
  ('★', L(r"a) Un fontaner cobra 30 € pel desplaçament i 20 € per hora. Escriu la funció i calcula el preu de 3,5 h.", r"a) Un fontanero cobra 30 € por el desplazamiento y 20 € por hora. Escribe la función y calcula el precio de 3,5 h.", r"a) A plumber charges €30 call-out and €20 per hour. Write the function and the price of 3.5 h.")),
  ('★★', L(r"b) Un mòbil té el 80 % de bateria i en perd un 5 % cada hora. Quan s'apagarà?", r"b) Un móvil tiene el 80 % de batería y pierde un 5 % cada hora. ¿Cuándo se apagará?", r"b) A phone has 80 % battery and loses 5 % per hour. When will it switch off?")),
  ('★★★', L(r"c) Una planta mesura 12 cm el dia 3 i 21 cm el dia 6. Si creix de manera lineal, quant mesurava el dia 0? Quan arribarà als 45 cm?", r"c) Una planta mide 12 cm el día 3 y 21 cm el día 6. Si crece de manera lineal, ¿cuánto medía el día 0? ¿Cuándo llegará a 45 cm?", r"c) A plant is 12 cm tall on day 3 and 21 cm on day 6. If it grows linearly, how tall was it on day 0? When will it reach 45 cm?"))],
  P(r"a) \(P=20x+30\); \(P(3{,}5)=100\) €. b) \(B=80-5t=0\Rightarrow t=16\) h. c) \(m=\tfrac{21-12}{6-3}=3\), \(h=3t+3\): 3 cm el dia 0; \(3t+3=45\Rightarrow t=14\): el dia 14.",
    r"a) \(P=20x+30\); \(P(3{,}5)=100\) €. b) \(B=80-5t=0\Rightarrow t=16\) h. c) \(m=\tfrac{21-12}{6-3}=3\), \(h=3t+3\): 3 cm el día 0; \(3t+3=45\Rightarrow t=14\): el día 14.",
    r"a) \(P=20x+30\); \(P(3.5)=€100\). b) \(B=80-5t=0\Rightarrow t=16\) h. c) \(m=\tfrac{21-12}{6-3}=3\), \(h=3t+3\): 3 cm on day 0; \(3t+3=45\Rightarrow t=14\): day 14."))
im('20x+30', 3.5, 100); roots('80-5x', [16]); line((3, 12), (6, 21), '3x+3'); im('3x+3', 14, 45)

# =====================================================================
# 8.5 Estudi conjunt de dues funcions lineals
# =====================================================================
s5 = box('def', L('Posició relativa de dues rectes', 'Posición relativa de dos rectas', 'How two lines can be placed'),
  P(r"Donades \(r:\ y=m_1x+n_1\) i \(s:\ y=m_2x+n_2\), només comparant pendents i ordenades en l'origen sabem com són:",
    r"Dadas \(r:\ y=m_1x+n_1\) y \(s:\ y=m_2x+n_2\), solo comparando pendientes y ordenadas en el origen sabemos cómo son:",
    r"Given \(r:\ y=m_1x+n_1\) and \(s:\ y=m_2x+n_2\), comparing slopes and intercepts tells us how they lie:")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Condició', 'Condición', 'Condition') + '</th><th>' + L('Rectes', 'Rectas', 'Lines') + '</th><th>' + L('Punts comuns', 'Puntos comunes', 'Common points') + '</th><th>' + L('Sistema', 'Sistema', 'System') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in [
    (r'\(m_1\neq m_2\)', L('<strong>secants</strong>', '<strong>secantes</strong>', '<strong>intersecting</strong>'), L('un', 'uno', 'one'), 'SCD'),
    (r'\(m_1=m_2,\ n_1\neq n_2\)', L('<strong>paral·leles</strong>', '<strong>paralelas</strong>', '<strong>parallel</strong>'), L('cap', 'ninguno', 'none'), 'SI'),
    (r'\(m_1=m_2,\ n_1=n_2\)', L('<strong>coincidents</strong>', '<strong>coincidentes</strong>', '<strong>coincident</strong>'), L('infinits', 'infinitos', 'infinitely many'), 'SCI')])
  + '</tbody></table></div>'
  + figs(fig(svg((-4, 4, -4, 4), fns=[('x+1', 'c0'), ('-2x+4', 'c1')], dots=[(1, 2, 'cut')], W=200), L('Secants', 'Secantes', 'Intersecting')),
         fig(svg((-4, 4, -4, 4), fns=[('x/2+2', 'c0'), ('x/2-1', 'c1')], W=200), L('Paral·leles', 'Paralelas', 'Parallel')),
         fig(svg((-4, 4, -4, 4), fns=[('-x+1', 'c0'), ('-x+1', 'c1 dash')], W=200), L('Coincidents', 'Coincidentes', 'Coincident')), three=True)
  + note(r"És el mateix que vas veure en la unitat 6: el punt de tall de dues rectes és la solució del sistema format per les seues equacions.", r"Es lo mismo que viste en la unidad 6: el punto de corte de dos rectas es la solución del sistema formado por sus ecuaciones.", r"It's what you saw in unit 6: the meeting point of two lines is the solution of the system formed by their equations."))
cut('x+1', '-2x+4', (1, 2))
s5 += box('prop', L('El punt de tall', 'El punto de corte', 'The meeting point'),
  P(r"Com que en el punt de tall les dues \(y\) són iguals, <strong>igualem</strong> les dues expressions, resolem l'equació per a trobar la \(x\) i després calculem la \(y\):",
    r"Como en el punto de corte las dos \(y\) son iguales, <strong>igualamos</strong> las dos expresiones, resolvemos la ecuación para hallar la \(x\) y después calculamos la \(y\):",
    r"At the meeting point both \(y\) values are equal, so <strong>set the two expressions equal</strong>, solve for \(x\), then work out \(y\):")
  + D(r"y=3x-1,\ \ y=-x+7:\quad 3x-1=-x+7\Rightarrow 4x=8\Rightarrow x=2,\ \ y=3\cdot2-1=5\ \Rightarrow\ \boxed{(2,\,5)}")
  + figs(fig(svg((-2, 6, -2, 8), fns=[('3x-1', 'c0'), ('-x+7', 'c1')], dots=[(2, 5, 'cut', '(2, 5)')], W=230)))
  + widget('w-pair', '✖️', L('Dues rectes: posició i punt de tall', 'Dos rectas: posición y punto de corte', 'Two lines: position and meeting point'),
           ['<div class="wrow">' + tin('r', 'r: y =', '3x-1') + tin('s', 's: y =', '-x+7') + '</div>',
            quick([('3x-1|-x+7', '3x − 1 · −x + 7'), ('2x+1|2x-3', '2x + 1 · 2x − 3'), ('x/2+1|(x+2)/2', 'x/2 + 1 · (x + 2)/2'), ('30+2x|5x', '30 + 2x · 5x'), ('0.5x+2|-x+5', '0,5x + 2 · −x + 5')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('pos', 'Entrena: posició relativa', 'Entrena: posición relativa', 'Train: relative position', 'opts')
  + drill('cut', 'Entrena: el punt de tall', 'Entrena: el punto de corte', 'Train: the meeting point', 'pair'))
cut('3x-1', '-x+7', (2, 5)); same('x/2+1', '(x+2)/2'); cut('30+2x', '5x', (10, 50)); cut('0.5x+2', '-x+5', (2, 3))
s5 += box('prop', L('Comparar dues situacions', 'Comparar dos situaciones', 'Comparing two situations'),
  P(r"Moltes vegades hem de triar entre dues ofertes. Dibuixem les dues rectes en els mateixos eixos: el <strong>punt de tall</strong> diu on costen el mateix i, a cada costat, l'oferta més barata és la de la recta que va <strong>per baix</strong>.",
    r"Muchas veces tenemos que elegir entre dos ofertas. Dibujamos las dos rectas en los mismos ejes: el <strong>punto de corte</strong> dice dónde cuestan lo mismo y, a cada lado, la oferta más barata es la de la recta que va <strong>por debajo</strong>.",
    r"We often have to choose between two offers. Draw both lines on the same axes: the <strong>meeting point</strong> shows where they cost the same and, on each side, the cheaper offer is the line <strong>below</strong>."))
s5 += levels(
 [prob(L(r"Digues la posició relativa de cada parella de rectes: a) \(y=2x+3\) i \(y=2x-1\); b) \(y=-x+4\) i \(y=3x\); c) \(y=\tfrac12x+1\) i \(2y=x+2\).", r"Di la posición relativa de cada pareja de rectas: a) \(y=2x+3\) e \(y=2x-1\); b) \(y=-x+4\) e \(y=3x\); c) \(y=\tfrac12x+1\) y \(2y=x+2\).", r"Give the relative position of each pair: a) \(y=2x+3\) and \(y=2x-1\); b) \(y=-x+4\) and \(y=3x\); c) \(y=\tfrac12x+1\) and \(2y=x+2\)."),
       P(r"a) Mateix pendent (2), \(n\) diferent: <strong>paral·leles</strong>. b) Pendents diferents: <strong>secants</strong>.", r"a) Misma pendiente (2), \(n\) distinta: <strong>paralelas</strong>. b) Pendientes distintas: <strong>secantes</strong>.", r"a) Same slope (2), different \(n\): <strong>parallel</strong>. b) Different slopes: <strong>intersecting</strong>."),
       P(r"c) \(2y=x+2\Rightarrow y=\tfrac12x+1\): és la mateixa recta, <strong>coincidents</strong>.", r"c) \(2y=x+2\Rightarrow y=\tfrac12x+1\): es la misma recta, <strong>coincidentes</strong>.", r"c) \(2y=x+2\Rightarrow y=\tfrac12x+1\): it's the same line, <strong>coincident</strong>."))],
 [prob(L(r"Troba el punt de tall de \(y=-2x+5\) i \(y=\tfrac12x\) i comprova-ho gràficament.", r"Halla el punto de corte de \(y=-2x+5\) e \(y=\tfrac12x\) y compruébalo gráficamente.", r"Find where \(y=-2x+5\) and \(y=\tfrac12x\) meet and check it on a graph."),
       D(r"-2x+5=\tfrac12x\Rightarrow -4x+10=x\Rightarrow 10=5x\Rightarrow x=2,\quad y=\tfrac12\cdot2=1"),
       P(r"Es tallen en \(\boxed{(2,\,1)}\).", r"Se cortan en \(\boxed{(2,\,1)}\).", r"They meet at \(\boxed{(2,\,1)}\).")
       + figs(fig(svg((-2, 5, -2, 5), fns=[('-2x+5', 'c0'), ('x/2', 'c1')], dots=[(2, 1, 'cut', '(2, 1)')], W=220))))],
 [prob(L(r"La companyia A cobra 12 € al mes més 0,05 € per minut; la B, 4 € al mes més 0,15 € per minut. A partir de quants minuts al mes és millor A?", r"La compañía A cobra 12 € al mes más 0,05 € por minuto; la B, 4 € al mes más 0,15 € por minuto. ¿A partir de cuántos minutos al mes es mejor A?", r"Company A charges €12 a month plus €0.05 per minute; B charges €4 a month plus €0.15 per minute. From how many minutes a month is A better?"),
       D(r"A(x)=0{,}05x+12\qquad B(x)=0{,}15x+4"),
       D(r"0{,}05x+12=0{,}15x+4\Rightarrow 8=0{,}1x\Rightarrow x=80,\quad A(80)=B(80)=16\ €"),
       P(r"Amb 80 minuts costen igual (16 €). Com que B té més pendent, a partir de 80 minuts B és més cara: <strong>A és millor a partir de 80 minuts</strong>.", r"Con 80 minutos cuestan igual (16 €). Como B tiene más pendiente, a partir de 80 minutos B es más cara: <strong>A es mejor a partir de 80 minutos</strong>.", r"At 80 minutes they cost the same (€16). B has the bigger slope, so beyond 80 minutes B is dearer: <strong>A is better from 80 minutes on</strong>.")
       + figs(fig(svg((-10, 160, -3, 30), fns=[('0.05x+12', 'c0', 0, 160), ('0.15x+4', 'c1', 0, 160)], dots=[(80, 16, 'cut', '(80, 16)')], xl='min', yl='€', xs=20, ys=5, gx=10, gy=5, W=300, H=220))))])
same('(x+2)/2', 'x/2+1'); cut('-2x+5', 'x/2', (2, 1)); cut('0.05x+12', '0.15x+4', (80, 16))
s5 += practice([
  ('★', L(r"a) Són paral·leles \(y=3x-2\) i \(y=-3x+2\)? b) Escriu una recta secant i una paral·lela a \(y=x+1\).", r"a) ¿Son paralelas \(y=3x-2\) e \(y=-3x+2\)? b) Escribe una recta secante y una paralela a \(y=x+1\).", r"a) Are \(y=3x-2\) and \(y=-3x+2\) parallel? b) Write a line that crosses \(y=x+1\) and one parallel to it.")),
  ('★★', L(r"c) Punt de tall de \(y=x+4\) i \(y=-3x\). d) Punt de tall de \(y=2x-3\) amb l'eix \(X\) (\(y=0\)).", r"c) Punto de corte de \(y=x+4\) e \(y=-3x\). d) Punto de corte de \(y=2x-3\) con el eje \(X\) (\(y=0\)).", r"c) Meeting point of \(y=x+4\) and \(y=-3x\). d) Where \(y=2x-3\) meets the \(X\) axis (\(y=0\)).")),
  ('★★★', L(r"e) Un videoclub A cobra 20 € de quota i 1 € per pel·lícula; el B, 3 € per pel·lícula sense quota. Quan convé cadascun?", r"e) Un videoclub A cobra 20 € de cuota y 1 € por película; el B, 3 € por película sin cuota. ¿Cuándo conviene cada uno?", r"e) Video club A charges a €20 fee plus €1 per film; B charges €3 per film and no fee. When is each one better?"))],
  P(r"a) No: pendents 3 i \(-3\) (secants). b) Per exemple \(y=2x\) (secant) i \(y=x-5\) (paral·lela). c) \((-1,\,3)\). d) \((1{,}5,\,0)\). e) \(20+x=3x\Rightarrow x=10\): menys de 10 pel·lícules, B; més de 10, A; amb 10, igual (30 €).",
    r"a) No: pendientes 3 y \(-3\) (secantes). b) Por ejemplo \(y=2x\) (secante) e \(y=x-5\) (paralela). c) \((-1,\,3)\). d) \((1{,}5,\,0)\). e) \(20+x=3x\Rightarrow x=10\): menos de 10 películas, B; más de 10, A; con 10, igual (30 €).",
    r"a) No: slopes 3 and \(-3\) (intersecting). b) E.g. \(y=2x\) (intersecting) and \(y=x-5\) (parallel). c) \((-1,\,3)\). d) \((1.5,\,0)\). e) \(20+x=3x\Rightarrow x=10\): fewer than 10 films, B; more than 10, A; at 10 they're equal (€30)."))
cut('x+4', '-3x', (-1, 3)); roots('2x-3', [R(3, 2)]); cut('20+x', '3x', (10, 30))

# =====================================================================
# 8.6 La paràbola y = ax²
# =====================================================================
s6 = box('def', L('Funció quadràtica', 'Función cuadrática', 'Quadratic function'),
  P(r"Una <strong>funció quadràtica</strong> és la que té per expressió un polinomi de segon grau:", r"Una <strong>función cuadrática</strong> es la que tiene por expresión un polinomio de segundo grado:", r"A <strong>quadratic function</strong> is one given by a second-degree polynomial:")
  + D(r"y=ax^2+bx+c\qquad (a\neq0)")
  + P(r"La seua gràfica és una corba anomenada <strong>paràbola</strong>. La més senzilla és \(y=x^2\):", r"Su gráfica es una curva llamada <strong>parábola</strong>. La más sencilla es \(y=x^2\):", r"Its graph is a curve called a <strong>parabola</strong>. The simplest one is \(y=x^2\):")
  + '<div class="gout">' + tvf('x^2', [-3, -2, -1, 0, 1, 2, 3])
  + svg((-4, 4, -1, 9), fns=[('x^2', 'c0')], guides=[0], dots=[(t, t * t, 'pt p0') for t in range(-3, 4)] + [(0, 0, 'mn', 'V')], W=240) + '</div>'
  + ul(L(r"És <strong>simètrica</strong> respecte de l'eix \(Y\): \(x\) i \(-x\) tenen la mateixa imatge. Aquesta recta és l'<strong>eix de simetria</strong>.", r"Es <strong>simétrica</strong> respecto del eje \(Y\): \(x\) y \(-x\) tienen la misma imagen. Esta recta es el <strong>eje de simetría</strong>.", r"It is <strong>symmetric</strong> about the \(Y\) axis: \(x\) and \(-x\) have the same image. That line is the <strong>axis of symmetry</strong>."),
       L(r"El punt on talla l'eix de simetria és el <strong>vèrtex</strong>, \(V(0,\,0)\): és el mínim de la funció.", r"El punto donde corta el eje de simetría es el <strong>vértice</strong>, \(V(0,\,0)\): es el mínimo de la función.", r"The point on the axis of symmetry is the <strong>vertex</strong>, \(V(0,\,0)\): the minimum of the function."),
       L(r"Decreix en \((-\infty,\,0)\) i creix en \((0,\,+\infty)\).", r"Decrece en \((-\infty,\,0)\) y crece en \((0,\,+\infty)\).", r"It decreases on \((-\infty,\,0)\) and increases on \((0,\,+\infty)\).")))
s6 += box('prop', L('La paràbola y = ax²', 'La parábola y = ax²', 'The parabola y = ax²'),
  ul(L(r"Té el vèrtex en \((0,\,0)\) i l'eix de simetria és l'eix \(Y\).", r"Tiene el vértice en \((0,\,0)\) y el eje de simetría es el eje \(Y\).", r"Its vertex is \((0,\,0)\) and its axis of symmetry is the \(Y\) axis."),
     L(r"Si \(a>0\), les branques van cap <strong>dalt</strong> \(\cup\) i el vèrtex és un <strong>mínim</strong>; si \(a<0\), van cap <strong>baix</strong> \(\cap\) i és un <strong>màxim</strong>.", r"Si \(a>0\), las ramas van hacia <strong>arriba</strong> \(\cup\) y el vértice es un <strong>mínimo</strong>; si \(a<0\), van hacia <strong>abajo</strong> \(\cap\) y es un <strong>máximo</strong>.", r"If \(a>0\), the arms point <strong>up</strong> \(\cup\) and the vertex is a <strong>minimum</strong>; if \(a<0\), they point <strong>down</strong> \(\cap\) and it's a <strong>maximum</strong>."),
     L(r"Com més gran és \(|a|\), més <strong>tancada</strong> (estreta) és la paràbola; si \(|a|<1\), és més <strong>oberta</strong> que \(y=x^2\).", r"Cuanto mayor es \(|a|\), más <strong>cerrada</strong> (estrecha) es la parábola; si \(|a|<1\), es más <strong>abierta</strong> que \(y=x^2\).", r"The bigger \(|a|\), the <strong>narrower</strong> the parabola; if \(|a|<1\), it's <strong>wider</strong> than \(y=x^2\)."))
  + figs(fig(svg((-4, 4, -1, 9), fns=[('x^2', 'c1 dash'), ('3x^2', 'c0'), ('x^2/3', 'c0')], W=200), r'\(y=3x^2\) · \(y=\tfrac13x^2\)'),
         fig(svg((-4, 4, -9, 1), fns=[('-x^2', 'c0'), ('-x^2/4', 'c1')], W=200), r'\(y=-x^2\) · \(y=-\tfrac14x^2\)'), three=True)
  + widget('w-a', '🥣', L('Juga amb a en y = ax²', 'Juega con a en y = ax²', 'Play with a in y = ax²'),
           ['<div class="wrow">' + rng('a', -3, 3, 0.25, 2, '') + '</div>',
            quick([('1', 'y = x²'), ('2', 'y = 2x²'), ('0.5', 'y = 0,5x²'), ('-1', 'y = −x²'), ('-0.25', 'y = −0,25x²')])],
           out='<div class="gout"></div>'))
s6 += box('prop', L('Desplaçaments: y = ax² + c', 'Desplazamientos: y = ax² + c', 'Shifts: y = ax² + c'),
  P(r"La paràbola \(y=ax^2+c\) és la de \(y=ax^2\) <strong>desplaçada \(c\) unitats cap amunt</strong> (o cap avall si \(c<0\)): el vèrtex passa a ser \((0,\,c)\).",
    r"La parábola \(y=ax^2+c\) es la de \(y=ax^2\) <strong>desplazada \(c\) unidades hacia arriba</strong> (o hacia abajo si \(c<0\)): el vértice pasa a ser \((0,\,c)\).",
    r"The parabola \(y=ax^2+c\) is \(y=ax^2\) <strong>shifted \(c\) units up</strong> (or down if \(c<0\)): the vertex becomes \((0,\,c)\).")
  + figs(fig(svg((-4, 4, -5, 6), fns=[('x^2', 'c1 dash'), ('x^2-4', 'c0')], dots=[(0, -4, 'mn', 'V'), (-2, 0, 'cut'), (2, 0, 'cut')], W=220), r'\(y=x^2-4\)')))
roots('x^2-4', [-2, 2])
s6 += levels(
 [prob(L(r"Sense dibuixar-les, digues cap on van les branques i si la paràbola és més oberta o més tancada que \(y=x^2\): a) \(y=5x^2\); b) \(y=-\tfrac12x^2\); c) \(y=-2x^2+3\).", r"Sin dibujarlas, di hacia dónde van las ramas y si la parábola es más abierta o más cerrada que \(y=x^2\): a) \(y=5x^2\); b) \(y=-\tfrac12x^2\); c) \(y=-2x^2+3\).", r"Without drawing them, say which way the arms point and whether each is wider or narrower than \(y=x^2\): a) \(y=5x^2\); b) \(y=-\tfrac12x^2\); c) \(y=-2x^2+3\)."),
       P(r"a) \(a=5>0\): cap amunt, més tancada. b) \(a=-\tfrac12<0\): cap avall, més oberta. c) \(a=-2<0\): cap avall, més tancada, amb el vèrtex en \((0,\,3)\).", r"a) \(a=5>0\): hacia arriba, más cerrada. b) \(a=-\tfrac12<0\): hacia abajo, más abierta. c) \(a=-2<0\): hacia abajo, más cerrada, con el vértice en \((0,\,3)\).", r"a) \(a=5>0\): up, narrower. b) \(a=-\tfrac12<0\): down, wider. c) \(a=-2<0\): down, narrower, with vertex \((0,\,3)\)."))],
 [prob(L(r"Fes una taula de valors i representa \(y=-\tfrac12x^2+2\). On talla els eixos?", r"Haz una tabla de valores y representa \(y=-\tfrac12x^2+2\). ¿Dónde corta los ejes?", r"Make a table of values and draw \(y=-\tfrac12x^2+2\). Where does it cross the axes?"),
       tvf('-x^2/2+2', [-3, -2, -1, 0, 1, 2, 3]),
       D(r"-\tfrac12x^2+2=0\Rightarrow x^2=4\Rightarrow x=\pm2:\ (-2,\,0)\ %s\ (2,\,0);\quad \text{%s}\ Y:\ (0,\,2)" % (I_, Lt('eix', 'eje', 'axis'))),
       figs(fig(svg((-4, 4, -3, 3), fns=[('-x^2/2+2', 'c0')], guides=[0], dots=[(0, 2, 'mx', 'V'), (-2, 0, 'cut'), (2, 0, 'cut')], W=230))))],
 [prob(L(r"Troba el valor de \(a\) perquè la paràbola \(y=ax^2\) passe pel punt \((2,\,-6)\). Passa també per \((-2,\,-6)\)? Per què?", r"Halla el valor de \(a\) para que la parábola \(y=ax^2\) pase por el punto \((2,\,-6)\). ¿Pasa también por \((-2,\,-6)\)? ¿Por qué?", r"Find \(a\) so that \(y=ax^2\) goes through \((2,\,-6)\). Does it also go through \((-2,\,-6)\)? Why?"),
       D(r"-6=a\cdot2^2\Rightarrow 4a=-6\Rightarrow \boxed{a=-\tfrac32}"),
       P(r"<strong>Sí</strong>: per simetria respecte de l'eix \(Y\), \(x=-2\) té la mateixa imatge que \(x=2\).", r"<strong>Sí</strong>: por simetría respecto del eje \(Y\), \(x=-2\) tiene la misma imagen que \(x=2\).", r"<strong>Yes</strong>: by symmetry about the \(Y\) axis, \(x=-2\) has the same image as \(x=2\)."))])
roots('-x^2/2+2', [-2, 2]); im('-3x^2/2', 2, -6); im('-3x^2/2', -2, -6)
s6 += practice([
  ('★', L(r"a) Quin és el vèrtex de \(y=x^2+5\)? I de \(y=-3x^2\)? b) Quina de les dues té un màxim?", r"a) ¿Cuál es el vértice de \(y=x^2+5\)? ¿Y de \(y=-3x^2\)? b) ¿Cuál de las dos tiene un máximo?", r"a) What is the vertex of \(y=x^2+5\)? And of \(y=-3x^2\)? b) Which one has a maximum?")),
  ('★★', L(r"c) Troba els talls amb l'eix \(X\) de \(y=2x^2-18\).", r"c) Halla los cortes con el eje \(X\) de \(y=2x^2-18\).", r"c) Find where \(y=2x^2-18\) crosses the \(X\) axis.")),
  ('★★★', L(r"d) Escriu una paràbola amb el vèrtex en \((0,\,-1)\) que passe per \((1,\,2)\).", r"d) Escribe una parábola con el vértice en \((0,\,-1)\) que pase por \((1,\,2)\).", r"d) Write a parabola with vertex \((0,\,-1)\) through \((1,\,2)\)."))],
  P(r"a) \((0,\,5)\) i \((0,\,0)\). b) \(y=-3x^2\) (\(a<0\)). c) \(2x^2=18\Rightarrow x=\pm3\): \((-3,\,0)\) i \((3,\,0)\). d) \(y=ax^2-1\), \(2=a-1\Rightarrow a=3\): \(y=3x^2-1\).",
    r"a) \((0,\,5)\) y \((0,\,0)\). b) \(y=-3x^2\) (\(a<0\)). c) \(2x^2=18\Rightarrow x=\pm3\): \((-3,\,0)\) y \((3,\,0)\). d) \(y=ax^2-1\), \(2=a-1\Rightarrow a=3\): \(y=3x^2-1\).",
    r"a) \((0,\,5)\) and \((0,\,0)\). b) \(y=-3x^2\) (\(a<0\)). c) \(2x^2=18\Rightarrow x=\pm3\): \((-3,\,0)\) and \((3,\,0)\). d) \(y=ax^2-1\), \(2=a-1\Rightarrow a=3\): \(y=3x^2-1\)."))
roots('2x^2-18', [-3, 3]); im('3x^2-1', 1, 2); vert('3x^2-1', (0, -1))

# =====================================================================
# 8.7 Representació de y = ax² + bx + c
# =====================================================================
s7 = box('def', L('Elements de la paràbola y = ax² + bx + c', 'Elementos de la parábola y = ax² + bx + c', 'Features of the parabola y = ax² + bx + c'),
  ul(L(r"<strong>Forma</strong>: com en \(y=ax^2\), el signe de \(a\) diu si les branques van cap amunt o cap avall, i \(|a|\), si és més oberta o tancada.", r"<strong>Forma</strong>: como en \(y=ax^2\), el signo de \(a\) dice si las ramas van hacia arriba o hacia abajo, y \(|a|\), si es más abierta o cerrada.", r"<strong>Shape</strong>: as with \(y=ax^2\), the sign of \(a\) says whether the arms point up or down, and \(|a|\) whether it's wide or narrow."),
     L(r"<strong>Vèrtex</strong>: \(x_v=\dfrac{-b}{2a}\) i \(y_v\) és la seua imatge, \(y_v=f(x_v)\).", r"<strong>Vértice</strong>: \(x_v=\dfrac{-b}{2a}\) e \(y_v\) es su imagen, \(y_v=f(x_v)\).", r"<strong>Vertex</strong>: \(x_v=\dfrac{-b}{2a}\) and \(y_v\) is its image, \(y_v=f(x_v)\)."),
     L(r"<strong>Eix de simetria</strong>: la recta vertical \(x=x_v\).", r"<strong>Eje de simetría</strong>: la recta vertical \(x=x_v\).", r"<strong>Axis of symmetry</strong>: the vertical line \(x=x_v\)."),
     L(r"<strong>Tall amb l'eix \(Y\)</strong>: \((0,\,c)\).", r"<strong>Corte con el eje \(Y\)</strong>: \((0,\,c)\).", r"<strong>\(Y\)-intercept</strong>: \((0,\,c)\)."),
     L(r"<strong>Talls amb l'eix \(X\)</strong>: les solucions de \(ax^2+bx+c=0\). Pot tindre'n dos, un (el vèrtex) o cap, segons el discriminant \(\Delta=b^2-4ac\).", r"<strong>Cortes con el eje \(X\)</strong>: las soluciones de \(ax^2+bx+c=0\). Puede tener dos, uno (el vértice) o ninguno, según el discriminante \(\Delta=b^2-4ac\).", r"<strong>\(X\)-intercepts</strong>: the solutions of \(ax^2+bx+c=0\). There may be two, one (the vertex) or none, depending on the discriminant \(\Delta=b^2-4ac\)."))
  + figs(fig(svg((-1, 5, -2, 4), fns=[('x^2-4x+3', 'c0')], guides=[2], dots=[(2, -1, 'mn', 'V'), (1, 0, 'cut'), (3, 0, 'cut'), (0, 3, 'pt p1')], W=200), r'\(\Delta>0\): ' + L('dos talls', 'dos cortes', 'two')),
         fig(svg((-1, 5, -2, 4), fns=[('x^2-4x+4', 'c0')], guides=[2], dots=[(2, 0, 'mn', 'V')], W=200), r'\(\Delta=0\): ' + L('un tall', 'un corte', 'one')),
         fig(svg((-1, 5, -2, 4), fns=[('x^2-4x+5', 'c0')], guides=[2], dots=[(2, 1, 'mn', 'V')], W=200), r'\(\Delta<0\): ' + L('cap', 'ninguno', 'none')), three=True))
roots('x^2-4x+3', [1, 3]); roots('x^2-4x+4', [2]); roots('x^2-4x+5', []); vert('x^2-4x+5', (2, 1))
s7 += box('prop', L('Com es representa, pas a pas', 'Cómo se representa, paso a paso', 'How to draw it, step by step'),
  P(r"Exemple: \(y=x^2-2x-3\) (\(a=1,\ b=-2,\ c=-3\)).", r"Ejemplo: \(y=x^2-2x-3\) (\(a=1,\ b=-2,\ c=-3\)).", r"Example: \(y=x^2-2x-3\) (\(a=1,\ b=-2,\ c=-3\)).")
  + ol(L(r"\(a=1>0\): branques cap amunt, el vèrtex és un mínim.", r"\(a=1>0\): ramas hacia arriba, el vértice es un mínimo.", r"\(a=1>0\): arms up, the vertex is a minimum."),
       L(r"Vèrtex: \(x_v=\dfrac{-(-2)}{2\cdot1}=1\), \(y_v=1^2-2\cdot1-3=-4\) → \(V(1,\,-4)\). Eix: \(x=1\).", r"Vértice: \(x_v=\dfrac{-(-2)}{2\cdot1}=1\), \(y_v=1^2-2\cdot1-3=-4\) → \(V(1,\,-4)\). Eje: \(x=1\).", r"Vertex: \(x_v=\dfrac{-(-2)}{2\cdot1}=1\), \(y_v=1^2-2\cdot1-3=-4\) → \(V(1,\,-4)\). Axis: \(x=1\)."),
       L(r"Tall amb l'eix \(Y\): \((0,\,-3)\).", r"Corte con el eje \(Y\): \((0,\,-3)\).", r"\(Y\)-intercept: \((0,\,-3)\)."),
       L(r"Talls amb l'eix \(X\): \(x=\dfrac{2\pm\sqrt{4+12}}{2}=\dfrac{2\pm4}{2}\) → \((-1,\,0)\) i \((3,\,0)\).", r"Cortes con el eje \(X\): \(x=\dfrac{2\pm\sqrt{4+12}}{2}=\dfrac{2\pm4}{2}\) → \((-1,\,0)\) y \((3,\,0)\).", r"\(X\)-intercepts: \(x=\dfrac{2\pm\sqrt{4+12}}{2}=\dfrac{2\pm4}{2}\) → \((-1,\,0)\) and \((3,\,0)\)."),
       L(r"Taula de valors al voltant del vèrtex (simètrica) i dibuix.", r"Tabla de valores alrededor del vértice (simétrica) y dibujo.", r"Table of values around the vertex (symmetric) and sketch."))
  + '<div class="gout">' + tvf('x^2-2x-3', [-2, -1, 0, 1, 2, 3, 4])
  + svg((-3, 5, -5, 6), fns=[('x^2-2x-3', 'c0')], guides=[1], dots=[(1, -4, 'mn', 'V(1, −4)'), (-1, 0, 'cut'), (3, 0, 'cut'), (0, -3, 'pt p1')], W=240) + '</div>'
  + note(r"Si el vèrtex no té coordenades enteres o la paràbola no talla l'eix \(X\), la taula de valors al voltant del vèrtex és imprescindible.", r"Si el vértice no tiene coordenadas enteras o la parábola no corta el eje \(X\), la tabla de valores alrededor del vértice es imprescindible.", r"If the vertex isn't at whole numbers or the parabola doesn't cross the \(X\) axis, the table of values around the vertex is essential.")
  + widget('w-para', '🎚️', L('Juga amb a, b i c', 'Juega con a, b y c', 'Play with a, b and c'),
           ['<div class="wrow">' + rng('a', -3, 3, 0.5, 1, '') + rng('b', -6, 6, 1, -2, '') + rng('c', -6, 6, 1, -3, '') + '</div>'],
           out='<div class="gout"></div>')
  + widget('w-pstudy', '🔍', L("Estudi complet d'una paràbola", 'Estudio completo de una parábola', 'Full study of a parabola'),
           ['<div class="wrow">' + tin('f', 'y =', 'x^2-2x-3') + '</div>',
            '<p class="hint-s">' + L("Escriu la fórmula amb la x: potències amb ^ (x^2), el producte amb * o sense signe (3x). Els decimals, amb punt o coma.", "Escribe la fórmula con la x: potencias con ^ (x^2), el producto con * o sin signo (3x). Los decimales, con punto o coma.", "Type the formula in x: powers with ^ (x^2), products with * or no sign (3x). Decimals with a point or comma.") + '</p>',
            quick([('x^2-2x-3', 'x² − 2x − 3'), ('-x^2+4x', '−x² + 4x'), ('2x^2+4x+5', '2x² + 4x + 5'), ('x^2-6x+9', 'x² − 6x + 9'), ('-0.5x^2+x+4', '−0,5x² + x + 4'), ('x^2+x-1', 'x² + x − 1')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('vert', 'Entrena: calcula el vèrtex', 'Entrena: calcula el vértice', 'Train: find the vertex', 'pair')
  + drill('pgraph', 'Entrena: quina fórmula té la paràbola?', 'Entrena: ¿qué fórmula tiene la parábola?', 'Train: which formula is the parabola?', 'opts'))
vert('x^2-2x-3', (1, -4)); roots('x^2-2x-3', [-1, 3]); vert('-x^2+4x', (2, 4)); vert('2x^2+4x+5', (-1, 3)); roots('2x^2+4x+5', []); vert('-0.5x^2+x+4', (1, R(9, 2))); roots('-0.5x^2+x+4', [-2, 4])
s7 += levels(
 [prob(L(r"Calcula el vèrtex, l'eix de simetria i el tall amb l'eix \(Y\) de \(y=-x^2+6x-5\). Té un màxim o un mínim?", r"Calcula el vértice, el eje de simetría y el corte con el eje \(Y\) de \(y=-x^2+6x-5\). ¿Tiene un máximo o un mínimo?", r"Find the vertex, the axis of symmetry and the \(Y\)-intercept of \(y=-x^2+6x-5\). Maximum or minimum?"),
       D(r"x_v=\frac{-6}{2\cdot(-1)}=3,\qquad y_v=-3^2+6\cdot3-5=4\ \Rightarrow\ V(3,\,4)"),
       P(r"Eix: \(x=3\). Tall amb \(Y\): \((0,\,-5)\). Com que \(a=-1<0\), el vèrtex és un <strong>màxim</strong>.", r"Eje: \(x=3\). Corte con \(Y\): \((0,\,-5)\). Como \(a=-1<0\), el vértice es un <strong>máximo</strong>.", r"Axis: \(x=3\). \(Y\)-intercept: \((0,\,-5)\). Since \(a=-1<0\), the vertex is a <strong>maximum</strong>."))],
 [prob(L(r"Representa \(y=x^2+4x\) estudiant-ne tots els elements.", r"Representa \(y=x^2+4x\) estudiando todos sus elementos.", r"Draw \(y=x^2+4x\), studying all its features."),
       P(r"\(a=1>0\): cap amunt. Vèrtex: \(x_v=\tfrac{-4}{2}=-2\), \(y_v=4-8=-4\) → \(V(-2,\,-4)\).", r"\(a=1>0\): hacia arriba. Vértice: \(x_v=\tfrac{-4}{2}=-2\), \(y_v=4-8=-4\) → \(V(-2,\,-4)\).", r"\(a=1>0\): up. Vertex: \(x_v=\tfrac{-4}{2}=-2\), \(y_v=4-8=-4\) → \(V(-2,\,-4)\)."),
       P(r"Talls: \(x^2+4x=0\Rightarrow x(x+4)=0\) → \((0,\,0)\) i \((-4,\,0)\) (el tall amb l'eix \(Y\) és l'origen).", r"Cortes: \(x^2+4x=0\Rightarrow x(x+4)=0\) → \((0,\,0)\) y \((-4,\,0)\) (el corte con el eje \(Y\) es el origen).", r"Intercepts: \(x^2+4x=0\Rightarrow x(x+4)=0\) → \((0,\,0)\) and \((-4,\,0)\) (the \(Y\)-intercept is the origin)."),
       tvf('x^2+4x', [-5, -4, -3, -2, -1, 0, 1])
       + figs(fig(svg((-6, 2, -5, 6), fns=[('x^2+4x', 'c0')], guides=[-2], dots=[(-2, -4, 'mn', 'V'), (-4, 0, 'cut'), (0, 0, 'cut')], W=230))))],
 [prob(L(r"Estudia i representa \(y=2x^2-4x+5\). Per què no talla l'eix \(X\)?", r"Estudia y representa \(y=2x^2-4x+5\). ¿Por qué no corta el eje \(X\)?", r"Study and draw \(y=2x^2-4x+5\). Why doesn't it cross the \(X\) axis?"),
       D(r"x_v=\frac{4}{4}=1,\quad y_v=2-4+5=3\ \Rightarrow\ V(1,\,3);\qquad \Delta=16-40=-24<0"),
       P(r"El vèrtex és un mínim (\(a=2>0\)) que està per damunt de l'eix \(X\): la paràbola no hi pot arribar. Ho confirma \(\Delta<0\). Tall amb \(Y\): \((0,\,5)\).", r"El vértice es un mínimo (\(a=2>0\)) que está por encima del eje \(X\): la parábola no puede llegar a él. Lo confirma \(\Delta<0\). Corte con \(Y\): \((0,\,5)\).", r"The vertex is a minimum (\(a=2>0\)) above the \(X\) axis: the parabola can't reach it. \(\Delta<0\) confirms it. \(Y\)-intercept: \((0,\,5)\)."),
       tvf('2x^2-4x+5', [-1, 0, 1, 2, 3])
       + figs(fig(svg((-2, 4, -1, 12), fns=[('2x^2-4x+5', 'c0')], guides=[1], dots=[(1, 3, 'mn', 'V'), (0, 5, 'pt p1')], W=200))))])
vert('-x^2+6x-5', (3, 4)); vert('x^2+4x', (-2, -4)); roots('x^2+4x', [-4, 0]); vert('2x^2-4x+5', (1, 3)); roots('2x^2-4x+5', [])
s7 += practice([
  ('★', L(r"a) Vèrtex de \(y=x^2-8x+10\). b) Tall amb l'eix \(Y\) de \(y=3x^2-x-7\).", r"a) Vértice de \(y=x^2-8x+10\). b) Corte con el eje \(Y\) de \(y=3x^2-x-7\).", r"a) Vertex of \(y=x^2-8x+10\). b) \(Y\)-intercept of \(y=3x^2-x-7\).")),
  ('★★', L(r"c) Talls amb els eixos de \(y=-x^2+x+6\). d) Interval on creix \(y=x^2+6x\).", r"c) Cortes con los ejes de \(y=-x^2+x+6\). d) Intervalo donde crece \(y=x^2+6x\).", r"c) Intercepts of \(y=-x^2+x+6\). d) Interval where \(y=x^2+6x\) increases.")),
  ('★★★', L(r"e) Troba \(c\) perquè la paràbola \(y=x^2-6x+c\) tinga el vèrtex sobre l'eix \(X\).", r"e) Halla \(c\) para que la parábola \(y=x^2-6x+c\) tenga el vértice sobre el eje \(X\).", r"e) Find \(c\) so that the vertex of \(y=x^2-6x+c\) lies on the \(X\) axis."))],
  P(r"a) \(V(4,\,-6)\). b) \((0,\,-7)\). c) \((0,\,6)\); \(x=-2\) i \(x=3\). d) \(x_v=-3\), \(a>0\): creix en \((-3,\,+\infty)\). e) \(x_v=3\), \(y_v=9-18+c=0\Rightarrow c=9\).",
    r"a) \(V(4,\,-6)\). b) \((0,\,-7)\). c) \((0,\,6)\); \(x=-2\) y \(x=3\). d) \(x_v=-3\), \(a>0\): crece en \((-3,\,+\infty)\). e) \(x_v=3\), \(y_v=9-18+c=0\Rightarrow c=9\).",
    r"a) \(V(4,\,-6)\). b) \((0,\,-7)\). c) \((0,\,6)\); \(x=-2\) and \(x=3\). d) \(x_v=-3\), \(a>0\): increasing on \((-3,\,+\infty)\). e) \(x_v=3\), \(y_v=9-18+c=0\Rightarrow c=9\)."))
vert('x^2-8x+10', (4, -6)); roots('-x^2+x+6', [-2, 3]); vert('x^2+6x', (-3, -9)); vert('x^2-6x+9', (3, 0))

# =====================================================================
# 8.8 Problemes amb paràboles
# =====================================================================
s8 = box('prop', L('On apareixen les paràboles', 'Dónde aparecen las parábolas', 'Where parabolas appear'),
  ul(L(r"<strong>Llançaments</strong>: l'altura d'un objecte llançat cap amunt és \(h(t)=h_0+v_0t-5t^2\) (aproximadament, en metres i segons).", r"<strong>Lanzamientos</strong>: la altura de un objeto lanzado hacia arriba es \(h(t)=h_0+v_0t-5t^2\) (aproximadamente, en metros y segundos).", r"<strong>Throws</strong>: the height of an object thrown upwards is \(h(t)=h_0+v_0t-5t^2\) (roughly, in metres and seconds)."),
     L(r"<strong>Àrees</strong>: l'àrea d'un rectangle de perímetre fix és una funció quadràtica de la base.", r"<strong>Áreas</strong>: el área de un rectángulo de perímetro fijo es una función cuadrática de la base.", r"<strong>Areas</strong>: the area of a rectangle with a fixed perimeter is a quadratic function of its base."),
     L(r"<strong>Ingressos i beneficis</strong>: si en pujar el preu es venen menys unitats, els ingressos (preu × unitats) són quadràtics.", r"<strong>Ingresos y beneficios</strong>: si al subir el precio se venden menos unidades, los ingresos (precio × unidades) son cuadráticos.", r"<strong>Revenue and profit</strong>: if raising the price sells fewer units, revenue (price × units) is quadratic."))
  + note(r"La pregunta «quin és el valor màxim (o mínim)?» es respon sempre amb el <strong>vèrtex</strong>: \(x_v\) diu <em>quan</em> o <em>amb quin valor</em> s'aconsegueix i \(y_v\), <em>quant</em> val.", r"La pregunta «¿cuál es el valor máximo (o mínimo)?» se responde siempre con el <strong>vértice</strong>: \(x_v\) dice <em>cuándo</em> o <em>con qué valor</em> se consigue e \(y_v\), <em>cuánto</em> vale.", r"The question “what is the maximum (or minimum) value?” is always answered with the <strong>vertex</strong>: \(x_v\) says <em>when</em> or <em>for which value</em> it happens and \(y_v\) <em>how much</em> it is.", '🎯')
  + widget('w-proj', '🏀', L('Llançament vertical', 'Lanzamiento vertical', 'Vertical throw'),
           ['<div class="wrow">' + rng('v', 5, 40, 1, 20, L('Velocitat inicial', 'Velocidad inicial', 'Initial speed')) + rng('h', 0, 50, 1, 0, L('Altura inicial', 'Altura inicial', 'Initial height')) + '</div>'],
           out='<div class="gout"></div>'))
s8 += levels(
 [prob(L(r"Llancem una pedra cap amunt i la seua altura és \(h(t)=20t-5t^2\) (m, s). Quina altura màxima assoleix i quan? Quan torna a terra?", r"Lanzamos una piedra hacia arriba y su altura es \(h(t)=20t-5t^2\) (m, s). ¿Qué altura máxima alcanza y cuándo? ¿Cuándo vuelve al suelo?", r"A stone is thrown upwards and its height is \(h(t)=20t-5t^2\) (m, s). What maximum height does it reach, and when? When does it land?"),
       D(r"t_v=\frac{-20}{2\cdot(-5)}=2\ \text{s},\qquad h(2)=40-20=\boxed{20\ \text{m}}"),
       D(r"20t-5t^2=0\Rightarrow 5t(4-t)=0\Rightarrow t=0\ \text{%s}\ \boxed{t=4\ \text{s}}" % Lt('o', 'o', 'or')),
       figs(fig(svg((-0.5, 5, -2, 24), fns=[('20x-5x^2', 'c0', 0, 4)], guides=[2], dots=[(2, 20, 'mx', 'V(2, 20)'), (4, 0, 'cut')], xl='t', yl='h', ys=5, gy=5, W=260, H=220))))],
 [prob(L(r"Amb 40 m de tanca volem tancar un camp rectangular. Quines dimensions fan l'àrea màxima?", r"Con 40 m de valla queremos cercar un campo rectangular. ¿Qué dimensiones hacen el área máxima?", r"We want to fence a rectangular field with 40 m of fence. Which dimensions give the largest area?"),
       P(r"Si la base és \(x\), base + altura = 20, així que l'altura és \(20-x\):", r"Si la base es \(x\), base + altura = 20, así que la altura es \(20-x\):", r"If the base is \(x\), base + height = 20, so the height is \(20-x\):"),
       D(r"A(x)=x(20-x)=-x^2+20x\qquad x_v=\frac{-20}{-2}=10,\quad A(10)=100"),
       P(r"L'àrea màxima és \(100\ \text{m}^2\), amb un <strong>quadrat de 10 m de costat</strong>.", r"El área máxima es \(100\ \text{m}^2\), con un <strong>cuadrado de 10 m de lado</strong>.", r"The largest area is \(100\ \text{m}^2\), with a <strong>10 m square</strong>."))],
 [prob(L(r"Un teatre ven 300 entrades a 20 €. Per cada euro que baixa el preu, ven 30 entrades més. Quin preu dona els ingressos màxims?", r"Un teatro vende 300 entradas a 20 €. Por cada euro que baja el precio, vende 30 entradas más. ¿Qué precio da los ingresos máximos?", r"A theatre sells 300 tickets at €20. For each euro off the price, it sells 30 more tickets. Which price gives the most revenue?"),
       P(r"Si baixem \(x\) euros: preu \(20-x\), entrades \(300+30x\).", r"Si bajamos \(x\) euros: precio \(20-x\), entradas \(300+30x\).", r"If we take \(x\) euros off: price \(20-x\), tickets \(300+30x\)."),
       D(r"I(x)=(20-x)(300+30x)=-30x^2+300x+6000"),
       D(r"x_v=\frac{-300}{2\cdot(-30)}=5,\qquad I(5)=15\cdot450=6750\ €"),
       P(r"Cal vendre-les a <strong>15 €</strong>: s'omplin 450 butaques i s'ingressen 6 750 €.", r"Hay que venderlas a <strong>15 €</strong>: se llenan 450 butacas y se ingresan 6 750 €.", r"Sell them at <strong>€15</strong>: 450 seats are filled and the revenue is €6,750."))])
vert('20x-5x^2', (2, 20)); roots('20x-5x^2', [0, 4]); same('x(20-x)', '-x^2+20x'); vert('-x^2+20x', (10, 100))
same('(20-x)(300+30x)', '-30x^2+300x+6000'); vert('-30x^2+300x+6000', (5, 6750))
s8 += practice([
  ('★', L(r"a) Un sortidor llança aigua amb una altura \(h(t)=10t-5t^2\). Quina altura màxima assoleix?", r"a) Un surtidor lanza agua con una altura \(h(t)=10t-5t^2\). ¿Qué altura máxima alcanza?", r"a) A fountain shoots water to a height \(h(t)=10t-5t^2\). What is the maximum height?")),
  ('★★', L(r"b) Dos nombres sumen 14. Quins són si el seu producte és el més gran possible?", r"b) Dos números suman 14. ¿Cuáles son si su producto es el mayor posible?", r"b) Two numbers add up to 14. Which are they if their product is as large as possible?")),
  ('★★★', L(r"c) Des d'un balcó a 15 m d'altura llancem una pilota cap amunt: \(h(t)=15+10t-5t^2\). Quan arriba al punt més alt i quan toca a terra?", r"c) Desde un balcón a 15 m de altura lanzamos una pelota hacia arriba: \(h(t)=15+10t-5t^2\). ¿Cuándo llega al punto más alto y cuándo toca el suelo?", r"c) From a balcony 15 m up we throw a ball upwards: \(h(t)=15+10t-5t^2\). When is it highest, and when does it land?"))],
  P(r"a) \(t_v=1\), \(h(1)=5\) m. b) \(P(x)=x(14-x)\), \(x_v=7\): 7 i 7 (producte 49). c) \(t_v=1\) s (20 m); \(15+10t-5t^2=0\Rightarrow t^2-2t-3=0\Rightarrow t=3\) s.",
    r"a) \(t_v=1\), \(h(1)=5\) m. b) \(P(x)=x(14-x)\), \(x_v=7\): 7 y 7 (producto 49). c) \(t_v=1\) s (20 m); \(15+10t-5t^2=0\Rightarrow t^2-2t-3=0\Rightarrow t=3\) s.",
    r"a) \(t_v=1\), \(h(1)=5\) m. b) \(P(x)=x(14-x)\), \(x_v=7\): 7 and 7 (product 49). c) \(t_v=1\) s (20 m); \(15+10t-5t^2=0\Rightarrow t^2-2t-3=0\Rightarrow t=3\) s."))
vert('10x-5x^2', (1, 5)); vert('x(14-x)', (7, 49)); vert('15+10x-5x^2', (1, 20)); roots('15+10x-5x^2', [-1, 3])

# ============================================================ muntatge
SECS = [
  (L('Funció de proporcionalitat directa', 'Función de proporcionalidad directa', 'Direct proportion'), s1),
  (L('Funció lineal', 'Función lineal', 'Linear functions'), s2),
  (L("Equació d'una recta", 'Ecuación de una recta', 'The equation of a line'), s3),
  (L('Aplicacions de la funció lineal', 'Aplicaciones de la función lineal', 'Applications of linear functions'), s4),
  (L('Estudi conjunt de dues funcions lineals', 'Estudio conjunto de dos funciones lineales', 'Two linear functions together'), s5),
  (L('Funcions quadràtiques: la paràbola y = ax²', 'Funciones cuadráticas: la parábola y = ax²', 'Quadratic functions: the parabola y = ax²'), s6),
  (L('Representació de y = ax² + bx + c', 'Representación de y = ax² + bx + c', 'Drawing y = ax² + bx + c'), s7),
  (L('Problemes amb paràboles', 'Problemas con parábolas', 'Word problems with parabolas'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Funció lineal i quadràtica · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 8 (Funció lineal i quadràtica) de 3r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "y=mx+n";')
assert "Funció lineal i quadràtica · FentMates" in head and 'content: "y=mx+n"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
js = js.replace('/*QUIZ*/\n', open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read())
assert 'NSEC = %d' % NS in js and '/*QUIZ*/' not in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">8.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
TIT = L("Funció lineal i quadràtica", "Función lineal y cuadrática", "Linear and quadratic functions")
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../3eso.html">{L("3r ESO", "3º ESO", "3rd ESO (Year 9)")}</a> / {L("Unitat 8", "Unidad 8", "Unit 8")}</span>
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
    <h1><span class="u">{L("Unitat 8", "Unidad 8", "Unit 8")}</span> · {TIT}</h1>
    <p>{L("Funció de proporcionalitat directa, funció lineal (pendent i ordenada en l'origen), equació d'una recta, aplicacions de la funció lineal, estudi conjunt de dues rectes i funcions quadràtiques (paràboles: vèrtex, eix, talls amb els eixos i problemes de màxims): teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Función de proporcionalidad directa, función lineal (pendiente y ordenada en el origen), ecuación de una recta, aplicaciones de la función lineal, estudio conjunto de dos rectas y funciones cuadráticas (parábolas: vértice, eje, cortes con los ejes y problemas de máximos): teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Direct proportion, linear functions (slope and intercept), the equation of a line, applications of linear functions, two lines together and quadratic functions (parabolas: vertex, axis, intercepts and maximum problems): theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 8: Funció lineal i quadràtica · 3r ESO", "Apuntes de teoría · Unidad 8: Función lineal y cuadrática · 3º ESO", "Theory notes · Unit 8: Linear and quadratic functions · 3rd ESO")}</p>
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
_tema.VERSION = "20261030f8"
_tema.aplica_fitxer(OUT)
