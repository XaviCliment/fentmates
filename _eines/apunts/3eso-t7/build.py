import os, re, sys
from fractions import Fraction as Fr
import math
import sympy as sp

# Genera materials/3eso/t7-funcions.html. Ús: python3 _eines/apunts/3eso-t7/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
# L'estudi de les gràfiques (domini, recorregut, creixement, extrems, continuïtat) el fa pl.py, que també
# comprova cada resultat per mostreig; les imatges i les taules de valors es calculen amb sympy.
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pl
from pl import F, INF
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/3eso/t7-funcions.html")

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
    return (f'\n<!-- ======================= 7.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">7.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)

# ---------- ginys ----------
def drill(kind, va, es, en, mode='num'):
    if mode == 'opts':
        row = f'<div class="wrow dopts"></div><div class="wrow"><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
    else:
        ph = '(2, −3)' if mode == 'pair' else '…'
        hint = (L("Escriu el punt com (2, −3) o bé 2; −3.", "Escribe el punto como (2, −3) o bien 2; −3.", "Type the point as (2, −3) or 2; −3.") if mode == 'pair'
                else L("Escriu un nombre. Els decimals, amb coma (2,5) o amb punt.", "Escribe un número. Los decimales, con coma (2,5) o con punto.", "Type a number. Decimals with a point or a comma (2.5)."))
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
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls='', attrs=''):
    idattr = f' id="{wid}"' if wid else ''
    return (f'<div class="widget{extra_cls}"{idattr}{attrs}>\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
def seg(items, first=0):
    return '<div class="wrow"><div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{str(i == first).lower()}">{t}</button>' for i, (k, t) in enumerate(items)) + '</div></div>'
HELP = '<p class="hint-s">' + L("Escriu la fórmula amb la x: potències amb ^ (x^2), el producte amb * o sense signe (3x), fraccions amb / i arrels amb sqrt( ). Els decimals, amb punt o coma.", "Escribe la fórmula con la x: potencias con ^ (x^2), el producto con * o sin signo (3x), fracciones con / y raíces con sqrt( ). Los decimales, con punto o coma.", "Type the formula in x: powers with ^ (x^2), products with * or no sign (3x), fractions with / and roots with sqrt( ). Decimals with a point or comma.") + '</p>'
def anal(mode, title, n):
    btns = [(str(i), L(f'Funció {c}', f'Función {c}', f'Function {c}')) for i, c in enumerate('ABCDE'[:n])] + [('rnd', '🎲 ' + L('Una a l’atzar', 'Una al azar', 'A random one'))]
    return widget('', '📊', title, [seg(btns)], out='<div class="gout"></div>', extra_cls=' w-anal', attrs=f' data-mode="{mode}"')

# ---------- càlculs amb sympy ----------
x = sp.Symbol('x')
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def E(s): return parse_expr(s, transformations=TR, local_dict={'x': x})
def im(s, a, want):
    v = E(s).subs(x, sp.nsimplify(a)); assert sp.simplify(v - sp.nsimplify(want)) == 0, (s, a, v, want); return v
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
def tvf(s, xs, yl='y', cls=''):
    """taula de valors d'una fórmula (calculada amb sympy)"""
    return tv([nt(a) for a in xs], [nt(E(s).subs(x, sp.nsimplify(a))) for a in xs], yl=yl, cls=cls)

# ---------- gràfiques estàtiques (SVG), com plot() d'app.js ----------
def svg(win, pls=(), fns=(), curves=(), dots=(), bars=None, xl='x', yl='y', xs=None, ys=None, W=300, H=None, mono=False, guides=(), gx=None, gy=None):
    x0, x1, y0, y1 = win
    H = H or round(W * (y1 - y0) / (x1 - x0))
    sx = lambda v: round((float(v) - x0) / (x1 - x0) * W, 1)
    sy = lambda v: round(H - (float(v) - y0) / (y1 - y0) * H, 1)
    xs = xs or (5 if x1 - x0 > 24 else 2 if x1 - x0 > 14 else 1); ys = ys or (5 if y1 - y0 > 24 else 2 if y1 - y0 > 14 else 1)
    g = ''
    import math
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
    def bar(iv, cls, horiz):
        out = ''
        for a, b, ca, cb in iv:
            A, B = max(a, x0 if horiz else y0), min(b, x1 if horiz else y1)
            out += (f'<line class="bar {cls}" x1="{sx(A)}" y1="{sy(ax)}" x2="{sx(B)}" y2="{sy(ax)}"/>' if horiz else f'<line class="bar {cls}" x1="{sx(ay)}" y1="{sy(A)}" x2="{sx(ay)}" y2="{sy(B)}"/>')
            for e, c in ((a, ca), (b, cb)):
                if e in (INF, -INF): continue
                cx, cy = (sx(e), sy(ax)) if horiz else (sx(ay), sy(e))
                out += f'<circle class="bd {cls}{"" if c else " op"}" cx="{cx}" cy="{cy}" r="4.5"/>'
        return out
    if bars and 'dom' in bars: g += bar(bars['dom'], 'bdom', True)
    if bars and 'rec' in bars: g += bar(bars['rec'], 'brec', False)
    for gx_ in guides: g += f'<line class="guide" x1="{sx(gx_)}" y1="0" x2="{sx(gx_)}" y2="{H}"/>'
    for c in curves:
        pts, cls = (c if isinstance(c, tuple) else (c, 'c0'))
        d = ''.join(('L' if i else 'M') + f'{sx(p[0])} {sy(p[1])}' for i, p in enumerate(pts))
        g += f'<path class="cv {cls}" d="{d}"/>'
    for f in fns:
        s, cls, a, b = (f + (None, None))[:4] if len(f) < 4 else f
        fl = sp.lambdify(x, E(s))
        a = x0 if a is None else max(a, x0); b = x1 if b is None else min(b, x1)
        d, pen = '', False
        for i in range(401):
            t = a + (b - a) * i / 400
            try: v = float(fl(t))
            except (ZeroDivisionError, ValueError): v = float('nan')
            if v != v or abs(v) > 1e6 or v > y1 + (y1 - y0) or v < y0 - (y1 - y0): pen = False; continue
            d += ('L' if pen else 'M') + f'{sx(t)} {sy(v)}'; pen = True
        g += f'<path class="cv {cls}" d="{d}"/>'
    for f, cls in pls:
        def segl(Pp, Q, s):
            c = ('up' if s > 0 else 'down' if s < 0 else 'flat') if mono else cls
            return f'<line class="cv {c}" x1="{sx(Pp[0])}" y1="{sy(Pp[1])}" x2="{sx(Q[0])}" y2="{sy(Q[1])}"/>'
        def ray(Pp, Q, back):
            m = float(pl.slope(Pp, Q)); dx = -1 if back else 1
            t = ((x0 if back else x1) - float(Pp[0])) * dx
            if abs(m) > 1e-12: t = min(t, ((y1 if m * dx > 0 else y0) - float(Pp[1])) / (m * dx))
            t = max(t - 0.15, 0.1)
            Ex = (float(Pp[0]) + dx * t, float(Pp[1]) + m * dx * t)
            s = pl.sgn(m); c = ('up' if s > 0 else 'down' if s < 0 else 'flat') if mono else cls
            ang = math.atan2(-(sy(Ex[1]) - sy(Pp[1])), sx(Ex[0]) - sx(Pp[0])); ex, ey = sx(Ex[0]), sy(Ex[1]); Lh = 9
            return segl(Pp, Ex, s) + (f'<path class="ah {c}" d="M{ex + math.cos(ang) * 3:.1f} {ey - math.sin(ang) * 3:.1f}L{ex - math.cos(ang - .45) * Lh:.1f} {ey + math.sin(ang - .45) * Lh:.1f}'
                                       f'L{ex - math.cos(ang + .45) * Lh:.1f} {ey + math.sin(ang + .45) * Lh:.1f}Z"/>')
        for p in f['p']:
            v = p['v']
            for i in range(len(v) - 1): g += segl(v[i], v[i + 1], pl.sgn(pl.slope(v[i], v[i + 1])))
            if p['l'] == 'a': g += ray(v[0], v[1], True)
            if p['r'] == 'a': g += ray(v[-1], v[-2], False)
        for p in f['p']:
            v = p['v']
            if p['l'] != 'a': g += f'<circle class="ep {cls}{" op" if p["l"] == "o" else ""}" cx="{sx(v[0][0])}" cy="{sy(v[0][1])}" r="4.5"/>'
            if p['r'] != 'a' and len(v) > 1: g += f'<circle class="ep {cls}{" op" if p["r"] == "o" else ""}" cx="{sx(v[-1][0])}" cy="{sy(v[-1][1])}" r="4.5"/>'
        for Pp in f['pts']: g += f'<circle class="ep {cls}" cx="{sx(Pp[0])}" cy="{sy(Pp[1])}" r="4.5"/>'
    for d in dots:
        px, py, cls, lab = (tuple(d) + (None,))[:4]
        g += f'<circle class="{cls}" cx="{sx(px)}" cy="{sy(py)}" r="{6 if cls in ("cut", "mx", "mn", "bad") else 4}"/>'
        if lab: g += f'<text class="plab" x="{sx(px) + 8}" y="{sy(py) - 8}">{lab}</text>'
    return f'<svg class="sgraf" viewBox="0 0 {W} {H}" role="img" aria-label="gràfica">{g}</svg>'
def fig(s, cap=None): return f'<figure>{s}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{s}</figure>'
def figs(*f, three=False): return '<div class="figs%s">' % (' three' if three else '') + ''.join(f) + '</div>'
def win(f, pad=1):
    xs_ = [P[0] for p in f['p'] for P in p['v']] + [P[0] for P in f['pts']]
    ys_ = [P[1] for p in f['p'] for P in p['v']] + [P[1] for P in f['pts']]
    a, b = min(min(xs_), 0) - pad, max(max(xs_), 0) + pad
    c, d = min(min(ys_), 0) - pad, max(max(ys_), 0) + pad
    if any(p['l'] == 'a' for p in f['p']): a -= 1
    if any(p['r'] == 'a' for p in f['p']): b += 1
    return (float(a), float(b), float(c), float(d))
def gr(f, cap=None, **kw): return fig(svg(win(f), pls=[(f, 'c0')], **kw), cap)
ST = {}
def st(f):
    """estudi comprovat per mostreig"""
    k = id(f)
    if k not in ST: ST[k] = pl.check(f)
    return ST[k]
def S(iv): return pl.settex(iv)
def PT(Pp): return pl.pttex(Pp)

# =====================================================================
# 7.1 Concepte de funció
# =====================================================================
s1 = box('def', L('Funció', 'Función', 'Function'),
  P(r"Una <strong>funció</strong> és una relació entre dues magnituds o variables que a <strong>cada valor</strong> de la primera li fa correspondre <strong>un únic valor</strong> de la segona.",
    r"Una <strong>función</strong> es una relación entre dos magnitudes o variables que a <strong>cada valor</strong> de la primera le hace corresponder <strong>un único valor</strong> de la segunda.",
    r"A <strong>function</strong> is a relationship between two quantities (variables) that assigns to <strong>each value</strong> of the first <strong>exactly one value</strong> of the second.")
  + ul(L(r"La \(x\) és la <strong>variable independent</strong>: li donem nosaltres els valors.", r"La \(x\) es la <strong>variable independiente</strong>: le damos nosotros los valores.", r"\(x\) is the <strong>independent variable</strong>: we choose its values."),
       L(r"La \(y\) és la <strong>variable dependent</strong>: el seu valor <em>depén</em> del de la \(x\).", r"La \(y\) es la <strong>variable dependiente</strong>: su valor <em>depende</em> del de la \(x\).", r"\(y\) is the <strong>dependent variable</strong>: its value <em>depends</em> on \(x\)."))
  + P(r"S'escriu \(y=f(x)\) i es llig «\(y\) és igual a \(f\) de \(x\)». El valor \(f(a)\) que correspon a \(x=a\) s'anomena <strong>imatge</strong> de \(a\).",
      r"Se escribe \(y=f(x)\) y se lee «\(y\) es igual a \(f\) de \(x\)». El valor \(f(a)\) que corresponde a \(x=a\) se llama <strong>imagen</strong> de \(a\).",
      r"We write \(y=f(x)\), read “\(y\) equals \(f\) of \(x\)”. The value \(f(a)\) that goes with \(x=a\) is called the <strong>image</strong> of \(a\)."))
s1 += box('prop', L('Exemples', 'Ejemplos', 'Examples'),
  '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Relació', 'Relación', 'Relationship') + '</th><th>' + L('És funció?', '¿Es función?', 'Function?') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in [
    (L("Quilos de pomes → preu que paguem (1,80 €/kg)", "Kilos de manzanas → precio que pagamos (1,80 €/kg)", "Kilos of apples → price paid (€1.80/kg)"), L("✓ Sí: cada pes té un sol preu.", "✓ Sí: cada peso tiene un solo precio.", "✓ Yes: each weight has one price.")),
    (L("Hora del dia → temperatura en un lloc", "Hora del día → temperatura en un lugar", "Time of day → temperature at a place"), L("✓ Sí: en cada moment hi ha una sola temperatura.", "✓ Sí: en cada momento hay una sola temperatura.", "✓ Yes: at each moment there is one temperature.")),
    (L("Costat d'un quadrat → àrea", "Lado de un cuadrado → área", "Side of a square → area"), L(r"✓ Sí: \(A=x^2\).", r"✓ Sí: \(A=x^2\).", r"✓ Yes: \(A=x^2\).")),
    (L("Nombre positiu → nombres que elevats al quadrat el donen", "Número positivo → números que elevados al cuadrado lo dan", "Positive number → numbers whose square is that number"), L(r"✗ No: al 9 li corresponen el 3 i el \(-3\).", r"✗ No: al 9 le corresponden el 3 y el \(-3\).", r"✗ No: 9 goes with both 3 and \(-3\).")),
    (L("Edat → alçada dels alumnes d'un institut", "Edad → altura de los alumnos de un instituto", "Age → height of the students in a school"), L("✗ No: alumnes de la mateixa edat tenen alçades diferents.", "✗ No: alumnos de la misma edad tienen alturas distintas.", "✗ No: students of the same age have different heights."))])
  + '</tbody></table></div>')
s1 += box('prop', L('Com sabem si una gràfica és d\'una funció?', '¿Cómo sabemos si una gráfica es de una función?', 'How can we tell if a graph is a function?'),
  P(r"Una gràfica correspon a una funció si <strong>cap recta vertical no la talla en més d'un punt</strong>. Si alguna recta vertical la talla en dos punts, aquell valor de \(x\) tindria dues imatges.",
    r"Una gráfica corresponde a una función si <strong>ninguna recta vertical la corta en más de un punto</strong>. Si alguna recta vertical la corta en dos puntos, ese valor de \(x\) tendría dos imágenes.",
    r"A graph is a function if <strong>no vertical line meets it more than once</strong>. If some vertical line meets it twice, that value of \(x\) would have two images.")
  + figs(fig(svg((-5, 5, -5, 5), fns=[('x^2/2-3', 'c0')], W=220), L('✓ És funció', '✓ Es función', '✓ Function')),
         fig(svg((-5, 5, -5, 5), curves=[([(4 * math.cos(t * math.pi / 60), 4 * math.sin(t * math.pi / 60)) for t in range(121)], 'c1')], dots=[(2, 3.464, 'bad'), (2, -3.464, 'bad')], guides=[2], W=220), L('✗ No és funció', '✗ No es función', '✗ Not a function')), three=True)
  + widget('w-vline', '📏', L('La prova de la recta vertical', 'La prueba de la recta vertical', 'The vertical line test'),
           [seg([(str(i), n) for i, n in enumerate(['Paràbola', 'Circumferència', 'Paràbola tombada', 'Corba en S', 'Ziga-zaga', 'Poligonal'])]),
            '<div class="wrow"><label style="flex:1">' + L('Mou la recta vertical', 'Mueve la recta vertical', 'Move the vertical line') + ' <input type="range" min="-5.5" max="5.5" step="0.25" value="1" aria-label="x"></label></div>'],
           out='<div class="gout"></div>')
  + drill('isf', 'Entrena: és una funció?', 'Entrena: ¿es una función?', 'Train: is it a function?', 'opts'))
F_ok = F(('c', [(-5, 2), (-2, -3), (1, 1), (4, -1)], 'c'))
s1 += levels(
 [prob(L(r"En cada relació, digues quina és la variable independent i quina la dependent: a) el temps que està encés un forn i l'electricitat que gasta; b) la velocitat d'un cotxe i el temps que tarda a fer 100 km.",
         r"En cada relación, di cuál es la variable independiente y cuál la dependiente: a) el tiempo que está encendido un horno y la electricidad que gasta; b) la velocidad de un coche y el tiempo que tarda en hacer 100 km.",
         r"In each relationship, say which is the independent variable and which the dependent one: a) how long an oven is on and the electricity it uses; b) a car's speed and the time it takes to cover 100 km."),
       P(r"a) Independent: el <strong>temps</strong> encés; dependent: l'<strong>electricitat</strong> gastada (depén de quant de temps està encés).", r"a) Independiente: el <strong>tiempo</strong> encendido; dependiente: la <strong>electricidad</strong> gastada (depende de cuánto tiempo está encendido).", r"a) Independent: the <strong>time</strong> it's on; dependent: the <strong>electricity</strong> used (it depends on how long it's on)."),
       P(r"b) Independent: la <strong>velocitat</strong>; dependent: el <strong>temps</strong> (com més velocitat, menys temps).", r"b) Independiente: la <strong>velocidad</strong>; dependiente: el <strong>tiempo</strong> (cuanta más velocidad, menos tiempo).", r"b) Independent: the <strong>speed</strong>; dependent: the <strong>time</strong> (the faster, the less time).")),
  prob(L(r"És una funció la relació que a cada alumne de la classe li assigna el seu dia de naixement? I la que a cada dia de l'any li assigna els alumnes nascuts aquell dia?",
         r"¿Es una función la relación que a cada alumno de la clase le asigna su día de nacimiento? ¿Y la que a cada día del año le asigna los alumnos nacidos ese día?",
         r"Is the relationship that gives each student in the class their birthday a function? What about the one that gives each day of the year the students born that day?"),
       P(r"La primera <strong>sí</strong>: cada alumne té un únic dia de naixement.", r"La primera <strong>sí</strong>: cada alumno tiene un único día de nacimiento.", r"The first one <strong>is</strong>: each student has exactly one birthday."),
       P(r"La segona <strong>no</strong>: un dia pot tindre dos alumnes (o cap!).", r"La segunda <strong>no</strong>: un día puede tener dos alumnos (¡o ninguno!).", r"The second one <strong>isn't</strong>: one day may have two students (or none!)."))],
 [prob(L(r"Quines d'aquestes gràfiques són d'una funció?", r"¿Cuáles de estas gráficas son de una función?", r"Which of these graphs are functions?")
       + figs(fig(svg((-5, 5, -5, 5), pls=[(F_ok, 'c0')], W=200), 'A'), fig(svg((-5, 5, -5, 5), curves=[([(t / 10 * t / 10 / 2 - 3, t / 10) for t in range(-45, 46)], 'c0')], W=200), 'B'),
              fig(svg((-5, 5, -5, 5), fns=[('x^3/20-x', 'c0')], W=200), 'C'), three=True),
       P(r"Tracem rectes verticals: <strong>A</strong> i <strong>C</strong> són funcions; <strong>B</strong> no, perquè per exemple la recta \(x=1\) la talla en dos punts.", r"Trazamos rectas verticales: <strong>A</strong> y <strong>C</strong> son funciones; <strong>B</strong> no, porque por ejemplo la recta \(x=1\) la corta en dos puntos.", r"Draw vertical lines: <strong>A</strong> and <strong>C</strong> are functions; <strong>B</strong> isn't, because for example the line \(x=1\) meets it twice."))],
 [prob(L(r"En una funció, poden dos valors diferents de \(x\) tindre la mateixa imatge? Posa'n un exemple.", r"En una función, ¿pueden dos valores distintos de \(x\) tener la misma imagen? Pon un ejemplo.", r"Can two different values of \(x\) have the same image? Give an example."),
       P(r"<strong>Sí</strong>, això està permés. El que no pot passar és que una \(x\) tinga dues imatges. Per exemple, en \(f(x)=x^2\):", r"<strong>Sí</strong>, eso está permitido. Lo que no puede pasar es que una \(x\) tenga dos imágenes. Por ejemplo, en \(f(x)=x^2\):", r"<strong>Yes</strong>, that's allowed. What can't happen is one \(x\) having two images. For example, in \(f(x)=x^2\):"),
       D(r"f(3)=9\quad\text{i}\quad f(-3)=9".replace(r'\text{i}', Lt('i', 'y', 'and'))),
       P(r"En la gràfica, una recta <em>horitzontal</em> sí que pot tallar-la en diversos punts.", r"En la gráfica, una recta <em>horizontal</em> sí puede cortarla en varios puntos.", r"On the graph, a <em>horizontal</em> line may well meet it several times."))])
im('x^2', 3, 9); im('x^2', -3, 9)
s1 += practice([
  ('★', L(r"a) És funció la relació que a cada persona li assigna el seu DNI? b) I la que a cada nombre li assigna el seu doble?", r"a) ¿Es función la relación que a cada persona le asigna su DNI? b) ¿Y la que a cada número le asigna su doble?", r"a) Is the relationship that gives each person their ID number a function? b) And the one that gives each number its double?")),
  ('★★', L(r"c) En la relació «nombre de fotocòpies → preu», quina és la variable independent? d) Un pare diu: «a cada fill meu li correspon la seua edat». I a l'inrevés, «a cada edat, el fill que la té», sempre és funció?", r"c) En la relación «número de fotocopias → precio», ¿cuál es la variable independiente? d) Un padre dice: «a cada hijo mío le corresponde su edad». Y al revés, «a cada edad, el hijo que la tiene», ¿siempre es función?", r"c) In “number of photocopies → price”, which is the independent variable? d) A father says: “each of my children has an age”. The other way round, “each age → the child with that age”: is it always a function?")),
  ('★★★', L(r"e) Una gràfica és una recta vertical, \(x=2\). És una funció?", r"e) Una gráfica es una recta vertical, \(x=2\). ¿Es una función?", r"e) A graph is a vertical line, \(x=2\). Is it a function?"))],
  P(r"a) Sí (cada persona té un únic DNI). b) Sí: \(f(x)=2x\). c) El nombre de fotocòpies. d) No sempre: si té bessons, una edat correspondria a dos fills. e) No: la mateixa recta vertical la talla en infinits punts; al 2 li corresponen totes les \(y\).",
    r"a) Sí (cada persona tiene un único DNI). b) Sí: \(f(x)=2x\). c) El número de fotocopias. d) No siempre: si tiene gemelos, una edad correspondería a dos hijos. e) No: la propia recta vertical la corta en infinitos puntos; al 2 le corresponden todas las \(y\).",
    r"a) Yes (each person has one ID number). b) Yes: \(f(x)=2x\). c) The number of photocopies. d) Not always: with twins, one age would go with two children. e) No: the vertical line itself meets it at infinitely many points; 2 goes with every \(y\)."))

# =====================================================================
# 7.2 Expressió d'una funció
# =====================================================================
taxi = '3+1.2*x'
s2 = box('prop', L('Quatre maneres de donar una funció', 'Cuatro maneras de dar una función', 'Four ways to describe a function'),
  P(r"Una mateixa funció es pot expressar de quatre maneres. Per exemple: <em>un taxi cobra 3 € per pujar-hi (baixada de bandera) i 1,20 € per cada quilòmetre</em>.",
    r"Una misma función se puede expresar de cuatro maneras. Por ejemplo: <em>un taxi cobra 3 € por subir (bajada de bandera) y 1,20 € por cada kilómetro</em>.",
    r"The same function can be given in four ways. For example: <em>a taxi charges €3 to get in and €1.20 for each kilometre</em>.")
  + ol(L(r"<strong>Enunciat</strong> (descripció verbal): és el text d'adés.", r"<strong>Enunciado</strong> (descripción verbal): es el texto de antes.", r"<strong>In words</strong>: the sentence above."),
       L(r"<strong>Taula de valors</strong>: alguns parells (km, preu).", r"<strong>Tabla de valores</strong>: algunos pares (km, precio).", r"<strong>Table of values</strong>: some (km, price) pairs."),
       L(r"<strong>Gràfica</strong>: els punts \((x,\,y)\) dibuixats en uns eixos.", r"<strong>Gráfica</strong>: los puntos \((x,\,y)\) dibujados en unos ejes.", r"<strong>Graph</strong>: the points \((x,\,y)\) plotted on axes."),
       L(r"<strong>Expressió algebraica</strong> (fórmula): \(f(x)=3+1{,}2x\), on \(x\) són els km i \(f(x)\) el preu en €.", r"<strong>Expresión algebraica</strong> (fórmula): \(f(x)=3+1{,}2x\), donde \(x\) son los km y \(f(x)\) el precio en €.", r"<strong>Formula</strong>: \(f(x)=3+1.2x\), where \(x\) is the distance in km and \(f(x)\) the price in €."))
  + '<div class="gout">' + tv(['0', '1', '2', '5', '10'], [nt(E(taxi).subs(x, a)) for a in [0, 1, 2, 5, 10]], xl=r'x\ (\text{km})', yl=r'f(x)\ (€)')
  + svg((-1, 11, -2, 17), fns=[(taxi, 'c0', 0, 11)], dots=[(a, float(E(taxi).subs(x, a)), 'pt p0') for a in [0, 1, 2, 5, 10]], xl='km', yl='€', W=280, H=230, ys=3) + '</div>'
  + note(r"La fórmula és la manera més completa: amb ella podem calcular el preu de <em>qualsevol</em> trajecte, per exemple \(f(7)=3+1{,}2\cdot7=11{,}40\) €.",
         r"La fórmula es la manera más completa: con ella podemos calcular el precio de <em>cualquier</em> trayecto, por ejemplo \(f(7)=3+1{,}2\cdot7=11{,}40\) €.",
         r"The formula is the most complete: with it we can work out the price of <em>any</em> trip, for example \(f(7)=3+1.2\cdot7=€11.40\)."))
im(taxi, 7, Fr('11.4'))
s2 += box('def', L('Imatge i antiimatge', 'Imagen y antiimagen', 'Image and preimage'),
  ul(L(r"La <strong>imatge</strong> d'un valor \(a\) és \(f(a)\): el resultat de substituir \(x\) per \(a\) en la fórmula.", r"La <strong>imagen</strong> de un valor \(a\) es \(f(a)\): el resultado de sustituir \(x\) por \(a\) en la fórmula.", r"The <strong>image</strong> of a value \(a\) is \(f(a)\): what you get by replacing \(x\) with \(a\) in the formula."),
     L(r"Una <strong>antiimatge</strong> d'un valor \(k\) és un valor de \(x\) que té imatge \(k\): l'obtenim resolent l'equació \(f(x)=k\).", r"Una <strong>antiimagen</strong> de un valor \(k\) es un valor de \(x\) que tiene imagen \(k\): la obtenemos resolviendo la ecuación \(f(x)=k\).", r"A <strong>preimage</strong> of a value \(k\) is a value of \(x\) whose image is \(k\): we find it by solving the equation \(f(x)=k\)."))
  + P(r"Si \(f(x)=x^2-3x+1\):", r"Si \(f(x)=x^2-3x+1\):", r"If \(f(x)=x^2-3x+1\):")
  + D(r"f(-2)=(-2)^2-3\cdot(-2)+1=4+6+1=\boxed{11}\qquad f(0)=\boxed{1}")
  + P(r"Si \(g(x)=2x+5\), l'antiimatge de \(11\) és la solució de \(2x+5=11\Rightarrow 2x=6\Rightarrow \boxed{x=3}\).", r"Si \(g(x)=2x+5\), la antiimagen de \(11\) es la solución de \(2x+5=11\Rightarrow 2x=6\Rightarrow \boxed{x=3}\).", r"If \(g(x)=2x+5\), the preimage of \(11\) is the solution of \(2x+5=11\Rightarrow 2x=6\Rightarrow \boxed{x=3}\).")
  + note(r"En substituir un nombre negatiu, posa'l <strong>entre parèntesis</strong>: \((-2)^2=4\), però \(-2^2=-4\).", r"Al sustituir un número negativo, ponlo <strong>entre paréntesis</strong>: \((-2)^2=4\), pero \(-2^2=-4\).", r"When you substitute a negative number, put it <strong>in brackets</strong>: \((-2)^2=4\), but \(-2^2=-4\).", '⚠')
  + widget('w-machine', '⚙️', L('Màquina de funcions: calcula imatges', 'Máquina de funciones: calcula imágenes', 'Function machine: work out images'),
           ['<div class="wrow">' + tin('f', r'f(x) =', 'x^2-3x+1') + tin('x', 'x =', '-2', 's') + '</div>', HELP,
            quick([('x^2-3x+1|-2', 'x²−3x+1, x = −2'), ('2x+5|3', '2x+5, x = 3'), ('(x+1)/2|5', '(x+1)/2, x = 5'), ('12/x|-4', '12/x, x = −4'), ('12/x|0', '12/x, x = 0'), ('sqrt(x+4)|5', '√(x+4), x = 5'), ('3+1.2x|7', '3+1,2x, x = 7')])])
  + drill('img', 'Entrena: calcula la imatge', 'Entrena: calcula la imagen', 'Train: work out the image')
  + drill('anti', "Entrena: troba l'antiimatge", 'Entrena: halla la antiimagen', 'Train: find the preimage'))
im('x^2-3x+1', -2, 11); im('x^2-3x+1', 0, 1); im('2x+5', 3, 11)
s2 += box('prop', L("De l'enunciat a la fórmula", 'Del enunciado a la fórmula', 'From words to formula'),
  P(r"Per a trobar la fórmula, pensem què fem amb la \(x\) per a obtindre la \(y\) en uns quants casos i ho generalitzem:", r"Para hallar la fórmula, pensamos qué hacemos con la \(x\) para obtener la \(y\) en unos cuantos casos y lo generalizamos:", r"To find the formula, think about what we do to \(x\) to get \(y\) in a few cases, then generalise:")
  + ul(L(r"Perímetre d'un quadrat de costat \(x\): \(P(x)=4x\).", r"Perímetro de un cuadrado de lado \(x\): \(P(x)=4x\).", r"Perimeter of a square with side \(x\): \(P(x)=4x\)."),
       L(r"Àrea d'un quadrat de costat \(x\): \(A(x)=x^2\).", r"Área de un cuadrado de lado \(x\): \(A(x)=x^2\).", r"Area of a square with side \(x\): \(A(x)=x^2\)."),
       L(r"Preu de \(x\) entrades a 6 € més 2 € de gestió: \(f(x)=6x+2\).", r"Precio de \(x\) entradas a 6 € más 2 € de gestión: \(f(x)=6x+2\).", r"Price of \(x\) tickets at €6 plus a €2 fee: \(f(x)=6x+2\)."),
       L(r"Temps per a fer 120 km a \(x\) km/h: \(t(x)=\dfrac{120}{x}\).", r"Tiempo para hacer 120 km a \(x\) km/h: \(t(x)=\dfrac{120}{x}\).", r"Time to cover 120 km at \(x\) km/h: \(t(x)=\dfrac{120}{x}\).")))
s2 += levels(
 [prob(L(r"Donada \(f(x)=5-2x\), calcula \(f(3)\), \(f(-1)\) i \(f(0)\).", r"Dada \(f(x)=5-2x\), calcula \(f(3)\), \(f(-1)\) y \(f(0)\).", r"Given \(f(x)=5-2x\), work out \(f(3)\), \(f(-1)\) and \(f(0)\)."),
       D(r"f(3)=5-2\cdot3=-1\qquad f(-1)=5-2\cdot(-1)=7\qquad f(0)=5")),
  prob(L(r"Completa la taula de valors de \(y=x^2-1\).", r"Completa la tabla de valores de \(y=x^2-1\).", r"Complete the table of values of \(y=x^2-1\)."),
       tvf('x^2-1', [-3, -2, -1, 0, 1, 2, 3]),
       P(r"Fixa't que \(x\) i \(-x\) tenen la mateixa imatge: \((-3)^2-1=3^2-1=8\).", r"Fíjate en que \(x\) y \(-x\) tienen la misma imagen: \((-3)^2-1=3^2-1=8\).", r"Notice that \(x\) and \(-x\) have the same image: \((-3)^2-1=3^2-1=8\)."))],
 [prob(L(r"Si \(f(x)=3x-4\), quin valor de \(x\) té imatge 11? I quin té imatge 0?", r"Si \(f(x)=3x-4\), ¿qué valor de \(x\) tiene imagen 11? ¿Y cuál tiene imagen 0?", r"If \(f(x)=3x-4\), which \(x\) has image 11? And which has image 0?"),
       D(r"3x-4=11\Rightarrow 3x=15\Rightarrow \boxed{x=5}\qquad 3x-4=0\Rightarrow \boxed{x=\tfrac43}")),
  prob(L(r"Observa la taula i troba la fórmula de la funció.", r"Observa la tabla y halla la fórmula de la función.", r"Look at the table and find the formula of the function.") + tvf('2x+1', [0, 1, 2, 3, 4]),
       P(r"Cada vegada que la \(x\) augmenta 1, la \(y\) augmenta 2; i quan \(x=0\), \(y=1\). Per tant:", r"Cada vez que la \(x\) aumenta 1, la \(y\) aumenta 2; y cuando \(x=0\), \(y=1\). Por tanto:", r"Each time \(x\) goes up by 1, \(y\) goes up by 2; and when \(x=0\), \(y=1\). So:"),
       D(r"\boxed{y=2x+1}\qquad \text{%s: } 2\cdot4+1=9\ \checkmark" % Lt('comprovació', 'comprobación', 'check')))],
 [prob(L(r"Una piscina té 12 000 litres d'aigua i es buida a raó de 400 litres per minut. Escriu la fórmula del volum en funció del temps i calcula quan estarà buida.", r"Una piscina tiene 12 000 litros de agua y se vacía a razón de 400 litros por minuto. Escribe la fórmula del volumen en función del tiempo y calcula cuándo estará vacía.", r"A pool holds 12,000 litres and drains at 400 litres per minute. Write the volume as a function of time and work out when it will be empty."),
       D(r"V(t)=12\,000-400t\qquad (t\ \text{%s},\ V\ \text{%s})" % (Lt('en minuts', 'en minutos', 'in minutes'), Lt('en litres', 'en litros', 'in litres'))),
       D(r"V(t)=0\Rightarrow 400t=12\,000\Rightarrow \boxed{t=30\ \text{min}}"),
       P(r"Té sentit per a \(t\) entre 0 i 30: abans no ha començat i després ja està buida.", r"Tiene sentido para \(t\) entre 0 y 30: antes no ha empezado y después ya está vacía.", r"It makes sense for \(t\) between 0 and 30: before that it hasn't started and after that it's empty."))])
for a, v in [(3, -1), (-1, 7), (0, 5)]: im('5-2x', a, v)
for a in range(-3, 4): im('x^2-1', a, a * a - 1)
im('3x-4', 5, 11); im('3x-4', Fr(4, 3), 0); im('12000-400x', 30, 0)
for a in range(5): im('2x+1', a, 2 * a + 1)
s2 += practice([
  ('★', L(r"a) Si \(f(x)=x^2+2x\), calcula \(f(2)\), \(f(-3)\) i \(f(\tfrac12)\).", r"a) Si \(f(x)=x^2+2x\), calcula \(f(2)\), \(f(-3)\) y \(f(\tfrac12)\).", r"a) If \(f(x)=x^2+2x\), work out \(f(2)\), \(f(-3)\) and \(f(\tfrac12)\).")),
  ('★★', L(r"b) Si \(g(x)=\dfrac{x+3}{2}\), troba l'antiimatge de 4. c) Escriu la fórmula del preu de \(x\) kg de taronges a 1,50 €/kg més una bossa de 0,10 €.", r"b) Si \(g(x)=\dfrac{x+3}{2}\), halla la antiimagen de 4. c) Escribe la fórmula del precio de \(x\) kg de naranjas a 1,50 €/kg más una bolsa de 0,10 €.", r"b) If \(g(x)=\dfrac{x+3}{2}\), find the preimage of 4. c) Write the formula for the price of \(x\) kg of oranges at €1.50/kg plus a €0.10 bag.")),
  ('★★★', L(r"d) Per a \(f(x)=x^2-4\), quins valors de \(x\) tenen imatge 5?", r"d) Para \(f(x)=x^2-4\), ¿qué valores de \(x\) tienen imagen 5?", r"d) For \(f(x)=x^2-4\), which values of \(x\) have image 5?"))],
  D(r"\text{a)}\ f(2)=8,\ \ f(-3)=3,\ \ f(\tfrac12)=\tfrac54\qquad \text{b)}\ \tfrac{x+3}{2}=4\Rightarrow x=5\qquad \text{c)}\ f(x)=1{,}5x+0{,}1")
  + D(r"\text{d)}\ x^2-4=5\Rightarrow x^2=9\Rightarrow x=3\ \ \text{%s}\ \ x=-3" % Lt('i', 'y', 'and')))
im('x^2+2x', 2, 8); im('x^2+2x', -3, 3); im('x^2+2x', Fr(1, 2), Fr(5, 4)); im('(x+3)/2', 5, 4); im('x^2-4', 3, 5); im('x^2-4', -3, 5)

# =====================================================================
# 7.3 Les funcions i els seus gràfics
# =====================================================================
para = 'x^2-2x-3'
s3 = box('prop', L("Com es representa una funció a partir de la fórmula", "Cómo se representa una función a partir de la fórmula", "How to graph a function from its formula"),
  ol(L(r"Fem una <strong>taula de valors</strong>: triem valors de \(x\) i calculem les imatges.", r"Hacemos una <strong>tabla de valores</strong>: elegimos valores de \(x\) y calculamos las imágenes.", r"Make a <strong>table of values</strong>: choose values of \(x\) and work out their images."),
     L(r"<strong>Dibuixem els punts</strong> \((x,\,y)\) en uns eixos de coordenades, amb una escala adequada.", r"<strong>Dibujamos los puntos</strong> \((x,\,y)\) en unos ejes de coordenadas, con una escala adecuada.", r"<strong>Plot the points</strong> \((x,\,y)\) on a pair of axes, with a suitable scale."),
     L(r"Si la variable pot prendre qualsevol valor (temps, longitud…), <strong>unim els punts</strong> amb una línia suau.", r"Si la variable puede tomar cualquier valor (tiempo, longitud…), <strong>unimos los puntos</strong> con una línea suave.", r"If the variable can take any value (time, length…), <strong>join the points</strong> with a smooth line."))
  + P(r"Per exemple, \(f(x)=x^2-2x-3\):", r"Por ejemplo, \(f(x)=x^2-2x-3\):", r"For example, \(f(x)=x^2-2x-3\):")
  + '<div class="gout">' + tvf(para, [-2, -1, 0, 1, 2, 3, 4], yl='f(x)')
  + svg((-3, 5, -5, 6), fns=[(para, 'c0')], dots=[(a, float(E(para).subs(x, a)), 'pt p0') for a in range(-2, 5)], W=260) + '</div>'
  + note(r"Si la variable només pren valors enters (nombre de persones, d'entrades…), la gràfica són <strong>punts solts</strong> i no els unim.", r"Si la variable solo toma valores enteros (número de personas, de entradas…), la gráfica son <strong>puntos sueltos</strong> y no los unimos.", r"If the variable only takes whole-number values (number of people, tickets…), the graph is a set of <strong>separate points</strong> and we don't join them."))
s3 += box('def', L('Punts de tall amb els eixos', 'Puntos de corte con los ejes', 'Where the graph crosses the axes'),
  ul(L(r"Amb l'<strong>eix \(Y\)</strong>: fem \(x=0\). El punt és \((0,\,f(0))\). Com a molt n'hi ha un.", r"Con el <strong>eje \(Y\)</strong>: hacemos \(x=0\). El punto es \((0,\,f(0))\). Como mucho hay uno.", r"With the <strong>\(Y\) axis</strong>: set \(x=0\). The point is \((0,\,f(0))\). There is at most one."),
     L(r"Amb l'<strong>eix \(X\)</strong>: fem \(y=0\), és a dir, resolem \(f(x)=0\). Pot haver-hi cap, un o més punts.", r"Con el <strong>eje \(X\)</strong>: hacemos \(y=0\), es decir, resolvemos \(f(x)=0\). Puede haber ninguno, uno o más puntos.", r"With the <strong>\(X\) axis</strong>: set \(y=0\), that is, solve \(f(x)=0\). There may be none, one or several points."))
  + D(r"f(x)=x^2-2x-3:\quad f(0)=-3\ \to\ (0,\,-3);\qquad x^2-2x-3=0\ \to\ x=3,\ x=-1\ \to\ (3,\,0),\ (-1,\,0)")
  + widget('w-plot', '📈', L('Taula de valors i gràfica', 'Tabla de valores y gráfica', 'Table of values and graph'),
           ['<div class="wrow">' + tin('f', 'f(x) =', 'x^2-2x-3') + tin('a', L('x des de', 'x desde', 'x from'), '-2', 's') + tin('b', L('fins a', 'hasta', 'to'), '4', 's') + '</div>', HELP,
            quick([('x^2-2x-3|-2|4', 'x²−2x−3'), ('2x-4|-1|5', '2x−4'), ('-x^2+4|-3|3', '−x²+4'), ('12/x|-6|6', '12/x'), ('sqrt(x)|0|9', '√x'), ('x^3-4x|-3|3', 'x³−4x')])],
           out='<div class="gout"></div>'))
assert sp.solve(E(para), x) == [-1, 3]; im(para, 0, -3)
exc = F(('c', [(0, 0), (2, 8), (3, 8), (4, 12), (5, 12), (8, 0)], 'c'))
s3 += box('prop', L('Interpretar una gràfica', 'Interpretar una gráfica', 'Reading a graph'),
  P(r"Moltes situacions de la vida real es descriuen amb una gràfica. Per a interpretar-la, llegim primer què representa cada eix i en quines unitats, i després la recorrem d'esquerra a dreta. La gràfica mostra la distància a casa d'una persona que fa una excursió:",
    r"Muchas situaciones de la vida real se describen con una gráfica. Para interpretarla, leemos primero qué representa cada eje y en qué unidades, y después la recorremos de izquierda a derecha. La gráfica muestra la distancia a casa de una persona que hace una excursión:",
    r"Many real-life situations are described by a graph. To read one, first check what each axis shows and in which units, then go through it from left to right. This graph shows how far from home someone is during a hike:")
  + figs(fig(svg((-0.5, 8.5, -1, 13), pls=[(exc, 'c0')], xl='t (h)', yl='d (km)', W=320, H=240)))
  + ul(L(r"De 0 a 2 h s'allunya 8 km (4 km/h). De 2 a 3 h descansa.", r"De 0 a 2 h se aleja 8 km (4 km/h). De 2 a 3 h descansa.", r"From 0 to 2 h they walk 8 km away (4 km/h). From 2 to 3 h they rest."),
       L(r"De 3 a 4 h fa 4 km més i arriba al punt més llunyà, a 12 km. Hi està 1 h.", r"De 3 a 4 h hace 4 km más y llega al punto más lejano, a 12 km. Está allí 1 h.", r"From 3 to 4 h they cover 4 more km and reach the farthest point, 12 km away. They stay 1 h."),
       L(r"De 5 a 8 h torna a casa: 12 km en 3 h (4 km/h).", r"De 5 a 8 h vuelve a casa: 12 km en 3 h (4 km/h).", r"From 5 to 8 h they walk back home: 12 km in 3 h (4 km/h)."))
  + widget('w-read', '🔎', L('Llig la gràfica', 'Lee la gráfica', 'Read the graph'),
           [seg([(str(i), n) for i, n in enumerate(['Excursió', 'Temperatura', "Dipòsit d'aigua"])]),
            '<div class="wrow"><label style="flex:1">' + L('Mou el punt', 'Mueve el punto', 'Move the point') + ' <input type="range" min="0" max="100" step="1" value="30" aria-label="t"></label></div>'],
           out='<div class="gout"></div>')
  + drill('read', 'Entrena: llig la imatge en la gràfica', 'Entrena: lee la imagen en la gráfica', 'Train: read the image off the graph'))
assert pl.value(exc, Fr(5, 2)) == 8 and pl.value(exc, Fr(13, 2)) == 6
s3 += levels(
 [prob(L(r"Fes una taula de valors i representa \(f(x)=2x-4\). En quins punts talla els eixos?", r"Haz una tabla de valores y representa \(f(x)=2x-4\). ¿En qué puntos corta los ejes?", r"Make a table of values and graph \(f(x)=2x-4\). Where does it cross the axes?"),
       tvf('2x-4', [-1, 0, 1, 2, 3, 4]),
       figs(fig(svg((-2, 5, -7, 5), fns=[('2x-4', 'c0')], dots=[(0, -4, 'cut', '(0, −4)'), (2, 0, 'cut', '(2, 0)')], W=220))),
       D(r"x=0\Rightarrow y=-4\ \to\ (0,\,-4)\qquad 2x-4=0\Rightarrow x=2\ \to\ (2,\,0)"))],
 [prob(L(r"Representa \(f(x)=-x^2+4\) per a \(x\) entre \(-3\) i \(3\) i troba els punts de tall amb els eixos.", r"Representa \(f(x)=-x^2+4\) para \(x\) entre \(-3\) y \(3\) y halla los puntos de corte con los ejes.", r"Graph \(f(x)=-x^2+4\) for \(x\) between \(-3\) and \(3\) and find where it crosses the axes."),
       tvf('-x^2+4', [-3, -2, -1, 0, 1, 2, 3]),
       figs(fig(svg((-4, 4, -6, 5), fns=[('-x^2+4', 'c0', -3, 3)], dots=[(0, 4, 'cut'), (-2, 0, 'cut'), (2, 0, 'cut')], W=220))),
       D(r"f(0)=4\to(0,\,4)\qquad -x^2+4=0\Rightarrow x^2=4\Rightarrow x=\pm2\to(-2,\,0),\ (2,\,0)")),
  prob(L(r"Llig la gràfica de l'excursió: a) a quina distància està a les 3,5 h? b) en quins moments està a 6 km de casa?", r"Lee la gráfica de la excursión: a) ¿a qué distancia está a las 3,5 h? b) ¿en qué momentos está a 6 km de casa?", r"Read the hike graph: a) how far away are they at 3.5 h? b) when are they 6 km from home?"),
       P(r"a) Entre 3 i 4 h passa de 8 a 12 km: a mitjan camí, a les 3,5 h, està a <strong>10 km</strong>.", r"a) Entre 3 y 4 h pasa de 8 a 12 km: a medio camino, a las 3,5 h, está a <strong>10 km</strong>.", r"a) Between 3 and 4 h it goes from 8 to 12 km: halfway, at 3.5 h, they're <strong>10 km</strong> away."),
       P(r"b) Tracem la recta horitzontal \(d=6\): la talla dues vegades, a l'anada (<strong>1,5 h</strong>) i a la tornada (<strong>6,5 h</strong>).", r"b) Trazamos la recta horizontal \(d=6\): la corta dos veces, a la ida (<strong>1,5 h</strong>) y a la vuelta (<strong>6,5 h</strong>).", r"b) Draw the horizontal line \(d=6\): it meets the graph twice, on the way out (<strong>1.5 h</strong>) and on the way back (<strong>6.5 h</strong>)."))],
 [prob(L(r"Un mòbil costa 300 € i perd 40 € de valor cada any. Escriu la fórmula, fes la taula i la gràfica, i digues quan valdrà 100 €.", r"Un móvil cuesta 300 € y pierde 40 € de valor cada año. Escribe la fórmula, haz la tabla y la gráfica, y di cuándo valdrá 100 €.", r"A phone costs €300 and loses €40 of value each year. Write the formula, make the table and graph, and say when it will be worth €100."),
       D(r"V(t)=300-40t"),
       tvf('300-40x', [0, 1, 2, 3, 4, 5], yl='V'),
       D(r"300-40t=100\Rightarrow 40t=200\Rightarrow \boxed{t=5\ \text{%s}}" % Lt('anys', 'años', 'years')))])
for a in range(-1, 5): im('2x-4', a, 2 * a - 4)
assert sorted(sp.solve(E('-x^2+4'), x)) == [-2, 2]; im('300-40x', 5, 100)
assert pl.value(exc, Fr(7, 2)) == 10 and pl.value(exc, Fr(3, 2)) == 6 and pl.value(exc, Fr(13, 2)) == 6
s3 += practice([
  ('★', L(r"a) Fes la taula de \(f(x)=3-x\) per a \(x=-2,\,-1,\,0,\,1,\,2,\,3\) i representa-la. On talla els eixos?", r"a) Haz la tabla de \(f(x)=3-x\) para \(x=-2,\,-1,\,0,\,1,\,2,\,3\) y represéntala. ¿Dónde corta los ejes?", r"a) Make the table of \(f(x)=3-x\) for \(x=-2,\,-1,\,0,\,1,\,2,\,3\) and graph it. Where does it cross the axes?")),
  ('★★', L(r"b) Troba els punts de tall amb els eixos de \(g(x)=x^2-9\).", r"b) Halla los puntos de corte con los ejes de \(g(x)=x^2-9\).", r"b) Find where \(g(x)=x^2-9\) crosses the axes.")),
  ('★★★', L(r"c) Una entrada de cine costa 7 €. Fes la gràfica del preu de 0 a 5 entrades. Unim els punts?", r"c) Una entrada de cine cuesta 7 €. Haz la gráfica del precio de 0 a 5 entradas. ¿Unimos los puntos?", r"c) A cinema ticket costs €7. Graph the price for 0 to 5 tickets. Do we join the points?"))],
  tvf('3-x', [-2, -1, 0, 1, 2, 3])
  + D(r"\text{a)}\ (0,\,3)\ \text{%s}\ (3,\,0)\qquad \text{b)}\ (0,\,-9),\ (3,\,0),\ (-3,\,0)" % Lt('i', 'y', 'and'))
  + P(r"c) Punts \((0,\,0),\ (1,\,7),\ (2,\,14),\ldots,\ (5,\,35)\). <strong>No</strong> els unim: no es poden comprar 2,5 entrades.", r"c) Puntos \((0,\,0),\ (1,\,7),\ (2,\,14),\ldots,\ (5,\,35)\). <strong>No</strong> los unimos: no se pueden comprar 2,5 entradas.", r"c) Points \((0,\,0),\ (1,\,7),\ (2,\,14),\ldots,\ (5,\,35)\). We do <strong>not</strong> join them: you can't buy 2.5 tickets."))
assert sorted(sp.solve(E('x^2-9'), x)) == [-3, 3]

# =====================================================================
# 7.4 Domini i recorregut
# =====================================================================
fA = F(('c', [(-4, 1), (-1, 4), (2, -2), (5, 3)], 'c'))
fB = F(('o', [(-3, -2), (0, 2), (4, 2)], 'c'))
sA, sB = st(fA), st(fB)
assert S(sA['dom']) == r'[-4,\,5]' and S(sA['rec']) == r'[-2,\,4]' and S(sB['dom']) == r'(-3,\,4]' and S(sB['rec']) == r'(-2,\,2]'
s4 = box('def', L('Domini i recorregut', 'Dominio y recorrido', 'Domain and range'),
  ul(L(r"El <strong>domini</strong> d'una funció, \(\mathrm{Dom}\,f\), és el conjunt de valors de \(x\) que <strong>tenen imatge</strong>. En la gràfica, és el que ocupa la gràfica <em>projectada sobre l'eix \(X\)</em>.", r"El <strong>dominio</strong> de una función, \(\mathrm{Dom}\,f\), es el conjunto de valores de \(x\) que <strong>tienen imagen</strong>. En la gráfica, es lo que ocupa la gráfica <em>proyectada sobre el eje \(X\)</em>.", r"The <strong>domain</strong> of a function, \(\mathrm{Dom}\,f\), is the set of \(x\) values that <strong>have an image</strong>. On the graph, it's what the graph covers <em>projected onto the \(X\) axis</em>."),
     L(r"El <strong>recorregut</strong> (o imatge), \(\mathrm{Rec}\,f\), és el conjunt de valors que <strong>pren la \(y\)</strong>. En la gràfica, és la projecció sobre l'<em>eix \(Y\)</em>.", r"El <strong>recorrido</strong> (o imagen), \(\mathrm{Rec}\,f\), es el conjunto de valores que <strong>toma la \(y\)</strong>. En la gráfica, es la proyección sobre el <em>eje \(Y\)</em>.", r"The <strong>range</strong>, \(\mathrm{Rec}\,f\), is the set of values that <strong>\(y\) takes</strong>. On the graph, it's the projection onto the <em>\(Y\) axis</em>."))
  + P(r"Els escrivim amb <strong>intervals</strong> (unitat 2). Un punt ple ● vol dir que l'extrem és de la gràfica (claudàtor \([\ ]\)); un punt buit ○, que no ho és (parèntesi \((\ )\)); una fletxa, que la gràfica continua indefinidament (\(\pm\infty\)).",
      r"Los escribimos con <strong>intervalos</strong> (unidad 2). Un punto lleno ● quiere decir que el extremo es de la gráfica (corchete \([\ ]\)); un punto vacío ○, que no lo es (paréntesis \((\ )\)); una flecha, que la gráfica continúa indefinidamente (\(\pm\infty\)).",
      r"We write them as <strong>intervals</strong> (unit 2). A filled dot ● means the endpoint belongs to the graph (square bracket \([\ ]\)); an empty dot ○ means it doesn't (round bracket \((\ )\)); an arrow means the graph goes on for ever (\(\pm\infty\)).")
  + figs(gr(fA, r'\(\mathrm{Dom}\,f=%s,\ \ \mathrm{Rec}\,f=%s\)' % (S(sA['dom']), S(sA['rec'])), bars={'dom': sA['dom'], 'rec': sA['rec']}, W=260),
         gr(fB, r'\(\mathrm{Dom}\,g=%s,\ \ \mathrm{Rec}\,g=%s\)' % (S(sB['dom']), S(sB['rec'])), bars={'dom': sB['dom'], 'rec': sB['rec']}, W=260))
  + anal('dom', L('Domini i recorregut d\'una gràfica', 'Dominio y recorrido de una gráfica', 'Domain and range of a graph'), 5)
  + drill('dom', 'Entrena: domini i recorregut', 'Entrena: dominio y recorrido', 'Train: domain and range', 'opts'))
s4 += box('prop', L('Domini a partir de la fórmula', 'Dominio a partir de la fórmula', 'Domain from the formula'),
  P(r"Busquem els valors de \(x\) per als quals <strong>no es pot fer</strong> l'operació:", r"Buscamos los valores de \(x\) para los que <strong>no se puede hacer</strong> la operación:", r"Look for the values of \(x\) for which the calculation <strong>can't be done</strong>:")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Tipus', 'Tipo', 'Type') + '</th><th>' + L('Condició', 'Condición', 'Condition') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + f'<tr><td>{L("Polinomis", "Polinomios", "Polynomials")}</td><td>{L("cap: sempre es poden calcular", "ninguna: siempre se pueden calcular", "none: always defined")}</td><td>\\(f(x)=x^2-3x\\Rightarrow \\mathrm{{Dom}}\\,f=\\mathbb{{R}}\\)</td></tr>'
  + f'<tr><td>{L("Fraccions", "Fracciones", "Fractions")}</td><td>{L("el denominador no pot ser 0", "el denominador no puede ser 0", "the denominator cannot be 0")}</td><td>\\(f(x)=\\dfrac{{5}}{{x-2}}\\Rightarrow \\mathrm{{Dom}}\\,f=\\mathbb{{R}}-\\{{2\\}}\\)</td></tr>'
  + f'<tr><td>{L("Arrels quadrades", "Raíces cuadradas", "Square roots")}</td><td>{L("el radicand ha de ser ≥ 0", "el radicando debe ser ≥ 0", "the number under the root must be ≥ 0")}</td><td>\\(f(x)=\\sqrt{{x+3}}:\\ x+3\\ge0\\Rightarrow \\mathrm{{Dom}}\\,f=[-3,\\,+\\infty)\\)</td></tr>'
  + '</tbody></table></div>'
  + note(r"En un problema, el domini també depén del <strong>context</strong>: si \(x\) és la longitud d'un costat, ha de ser positiva; si és un nombre d'entrades, ha de ser natural.", r"En un problema, el dominio también depende del <strong>contexto</strong>: si \(x\) es la longitud de un lado, tiene que ser positiva; si es un número de entradas, tiene que ser natural.", r"In a word problem, the domain also depends on the <strong>context</strong>: if \(x\) is the length of a side it must be positive; if it's a number of tickets it must be a whole number.")
  + drill('domf', 'Entrena: domini a partir de la fórmula', 'Entrena: dominio a partir de la fórmula', 'Train: domain from the formula', 'opts'))
fC = F(('a', [(-2, -3), (1, 3)], 'o'), ('c', [(3, 1), (6, -1)], 'a'))
sC = st(fC)
fD = F(('c', [(-5, 4), (-2, 1)], 'o'), ('c', [(-2, -1), (2, 3)], 'c'), pts=[(5, 2)])
sD = st(fD)
s4 += levels(
 [prob(L(r"Troba el domini i el recorregut d'aquesta funció.", r"Halla el dominio y el recorrido de esta función.", r"Find the domain and range of this function.") + figs(gr(fD, W=240)),
       P(r"Projectem sobre l'eix \(X\): la gràfica va de \(-5\) a \(2\) sense interrupcions (en \(x=-2\) hi ha el punt ple de baix) i, a més, hi ha el punt aïllat de \(x=5\).", r"Proyectamos sobre el eje \(X\): la gráfica va de \(-5\) a \(2\) sin interrupciones (en \(x=-2\) está el punto lleno de abajo) y, además, está el punto aislado de \(x=5\).", r"Project onto the \(X\) axis: the graph runs from \(-5\) to \(2\) without gaps (at \(x=-2\) there's the lower filled dot), plus the isolated point at \(x=5\)."),
       D(r"\mathrm{Dom}\,f=%s\qquad \mathrm{Rec}\,f=%s" % (S(sD['dom']), S(sD['rec']))),
       figs(gr(fD, bars={'dom': sD['dom'], 'rec': sD['rec']}, W=240)))],
 [prob(L(r"Calcula el domini de: a) \(f(x)=4x^3-x+7\); b) \(g(x)=\dfrac{3}{x+5}\); c) \(h(x)=\sqrt{x-4}\); d) \(k(x)=\dfrac{1}{x^2-9}\).", r"Calcula el dominio de: a) \(f(x)=4x^3-x+7\); b) \(g(x)=\dfrac{3}{x+5}\); c) \(h(x)=\sqrt{x-4}\); d) \(k(x)=\dfrac{1}{x^2-9}\).", r"Find the domain of: a) \(f(x)=4x^3-x+7\); b) \(g(x)=\dfrac{3}{x+5}\); c) \(h(x)=\sqrt{x-4}\); d) \(k(x)=\dfrac{1}{x^2-9}\)."),
       D(r"\text{a)}\ \text{%s}\Rightarrow \mathbb{R}\qquad \text{b)}\ x+5\neq0\Rightarrow \mathbb{R}-\{-5\}" % Lt('polinomi', 'polinomio', 'polynomial')),
       D(r"\text{c)}\ x-4\ge0\Rightarrow [4,\,+\infty)\qquad \text{d)}\ x^2\neq9\Rightarrow \mathbb{R}-\{-3,\,3\}"))],
 [prob(L(r"Troba el domini i el recorregut d'aquesta funció. Les fletxes indiquen que la gràfica continua.", r"Halla el dominio y el recorrido de esta función. Las flechas indican que la gráfica continúa.", r"Find the domain and range of this function. The arrows mean the graph carries on.") + figs(gr(fC, W=260)),
       P(r"En \(x=1\) el punt és buit i fins a \(x=3\) no hi ha gràfica: els valors de \(x\) entre 1 (inclòs) i 3 (no inclòs) no tenen imatge. Les fletxes allarguen el domini fins a \(\pm\infty\).", r"En \(x=1\) el punto es vacío y hasta \(x=3\) no hay gráfica: los valores de \(x\) entre 1 (incluido) y 3 (no incluido) no tienen imagen. Las flechas alargan el dominio hasta \(\pm\infty\).", r"At \(x=1\) the dot is empty and there's no graph until \(x=3\): the \(x\) values from 1 (included) to 3 (not included) have no image. The arrows stretch the domain out to \(\pm\infty\)."),
       D(r"\mathrm{Dom}\,f=%s\qquad \mathrm{Rec}\,f=%s" % (S(sC['dom']), S(sC['rec']))),
       P(r"El tros de l'esquerra pren tots els valors menors que 3 (el 3 no, perquè el punt és buit); el de la dreta comença en 1 i baixa indefinidament, i no hi afegeix cap valor nou.", r"El trozo de la izquierda toma todos los valores menores que 3 (el 3 no, porque el punto es vacío); el de la derecha empieza en 1 y baja indefinidamente, y no añade ningún valor nuevo.", r"The left piece takes every value below 3 (not 3 itself, since the dot is empty); the right piece starts at 1 and goes down for ever, adding no new values."),
       figs(gr(fC, bars={'dom': sC['dom'], 'rec': sC['rec']}, W=260)))])
assert S(sC['dom']) == r'(-\infty,\,1)\cup [3,\,+\infty)' and S(sC['rec']) == r'(-\infty,\,3)' and S(sD['dom']) == r'[-5,\,2]\cup \{5\}' and S(sD['rec']) == r'[-1,\,4]'
fP = F(('c', [(-3, 0), (0, 3), (2, -1)], 'c')); sP = st(fP)
s4 += practice([
  ('★', L(r"a) Escriu el domini i el recorregut de la funció que va del punt \((-3,\,0)\) al \((0,\,3)\) i d'ahí al \((2,\,-1)\), amb els dos extrems plens.", r"a) Escribe el dominio y el recorrido de la función que va del punto \((-3,\,0)\) al \((0,\,3)\) y de ahí al \((2,\,-1)\), con los dos extremos llenos.", r"a) Write the domain and range of the function going from \((-3,\,0)\) to \((0,\,3)\) and then to \((2,\,-1)\), with both endpoints filled.")),
  ('★★', L(r"b) Calcula el domini de \(f(x)=\dfrac{x}{x-6}\) i de \(g(x)=\sqrt{2x-8}\).", r"b) Calcula el dominio de \(f(x)=\dfrac{x}{x-6}\) y de \(g(x)=\sqrt{2x-8}\).", r"b) Find the domain of \(f(x)=\dfrac{x}{x-6}\) and of \(g(x)=\sqrt{2x-8}\).")),
  ('★★★', L(r"c) L'àrea d'un quadrat és \(A(x)=x^2\). Quin domini té aquesta funció si \(x\) és el costat? I la funció \(f(x)=x^2\) sense context?", r"c) El área de un cuadrado es \(A(x)=x^2\). ¿Qué dominio tiene esta función si \(x\) es el lado? ¿Y la función \(f(x)=x^2\) sin contexto?", r"c) The area of a square is \(A(x)=x^2\). What is the domain of this function if \(x\) is the side? And of \(f(x)=x^2\) with no context?"))],
  D(r"\text{a)}\ \mathrm{Dom}=%s,\ \ \mathrm{Rec}=%s\qquad \text{b)}\ \mathbb{R}-\{6\};\ \ 2x-8\ge0\Rightarrow [4,\,+\infty)" % (S(sP['dom']), S(sP['rec'])))
  + P(r"c) Com a costat, \(x>0\): \((0,\,+\infty)\). Sense context, \(\mathbb{R}\).", r"c) Como lado, \(x>0\): \((0,\,+\infty)\). Sin contexto, \(\mathbb{R}\).", r"c) As a side, \(x>0\): \((0,\,+\infty)\). With no context, \(\mathbb{R}\)."))
assert S(sP['dom']) == r'[-3,\,2]' and S(sP['rec']) == r'[-1,\,3]'

# =====================================================================
# 7.5 Creixement i decreixement
# =====================================================================
fM = F(('c', [(-5, -1), (-2, 3), (1, -2), (4, 2), (6, 2)], 'c')); sM = st(fM)
assert S(sM['mono']['+']) == r'(-5,\,-2)\cup (1,\,4)' and S(sM['mono']['-']) == r'(-2,\,1)' and S(sM['mono']['0']) == r'(4,\,6)'
s5 = box('def', L('Funció creixent, decreixent i constant', 'Función creciente, decreciente y constante', 'Increasing, decreasing and constant'),
  P(r"Recorrem la gràfica <strong>d'esquerra a dreta</strong> (quan la \(x\) augmenta). En un interval, una funció és:", r"Recorremos la gráfica <strong>de izquierda a derecha</strong> (cuando la \(x\) aumenta). En un intervalo, una función es:", r"Go along the graph <strong>from left to right</strong> (as \(x\) increases). On an interval, a function is:")
  + ul(L(r"<strong>creixent</strong> si, quan la \(x\) augmenta, la \(y\) també augmenta (la gràfica <em>puja</em>): si \(x_1<x_2\), aleshores \(f(x_1)<f(x_2)\);", r"<strong>creciente</strong> si, cuando la \(x\) aumenta, la \(y\) también aumenta (la gráfica <em>sube</em>): si \(x_1<x_2\), entonces \(f(x_1)<f(x_2)\);", r"<strong>increasing</strong> if, as \(x\) increases, \(y\) increases too (the graph <em>goes up</em>): if \(x_1<x_2\) then \(f(x_1)<f(x_2)\);"),
       L(r"<strong>decreixent</strong> si, quan la \(x\) augmenta, la \(y\) disminueix (la gràfica <em>baixa</em>): si \(x_1<x_2\), aleshores \(f(x_1)>f(x_2)\);", r"<strong>decreciente</strong> si, cuando la \(x\) aumenta, la \(y\) disminuye (la gráfica <em>baja</em>): si \(x_1<x_2\), entonces \(f(x_1)>f(x_2)\);", r"<strong>decreasing</strong> if, as \(x\) increases, \(y\) decreases (the graph <em>goes down</em>): if \(x_1<x_2\) then \(f(x_1)>f(x_2)\);"),
       L(r"<strong>constant</strong> si la \(y\) no canvia (la gràfica és <em>horitzontal</em>).", r"<strong>constante</strong> si la \(y\) no cambia (la gráfica es <em>horizontal</em>).", r"<strong>constant</strong> if \(y\) doesn't change (the graph is <em>horizontal</em>)."))
  + figs(gr(fM, None, mono=True, W=300))
  + D(r"\text{%s: }%s\qquad \text{%s: }%s\qquad \text{%s: }%s" % (Lt('Creixent', 'Creciente', 'Increasing'), S(sM['mono']['+']), Lt('Decreixent', 'Decreciente', 'Decreasing'), S(sM['mono']['-']), Lt('Constant', 'Constante', 'Constant'), S(sM['mono']['0'])))
  + note(r"Els intervals de creixement es donen sempre amb valors de la <strong>\(x\)</strong> (no de la \(y\)!) i amb <strong>intervals oberts</strong>.", r"Los intervalos de crecimiento se dan siempre con valores de la <strong>\(x\)</strong> (¡no de la \(y\)!) y con <strong>intervalos abiertos</strong>.", r"Intervals where a function increases or decreases are always given in <strong>\(x\)</strong> values (not \(y\)!) and as <strong>open intervals</strong>.", '⚠')
  + anal('mono', L('Creixement i decreixement', 'Crecimiento y decrecimiento', 'Increasing and decreasing'), 4)
  + drill('mono', 'Entrena: on creix i on decreix?', 'Entrena: ¿dónde crece y dónde decrece?', 'Train: where does it go up or down?', 'opts'))
fM2 = F(('a', [(-3, -2), (-1, 2), (2, 2), (4, -1)], 'a')); sM2 = st(fM2)
s5 += levels(
 [prob(L(r"Digues on creix i on decreix aquesta funció.", r"Di dónde crece y dónde decrece esta función.", r"Say where this function increases and where it decreases.") + figs(gr(fM2, W=260)),
       P(r"Les fletxes indiquen que continua: a l'esquerra puja des de \(-\infty\) i a la dreta baixa fins a \(+\infty\).", r"Las flechas indican que continúa: a la izquierda sube desde \(-\infty\) y a la derecha baja hasta \(+\infty\).", r"The arrows mean it carries on: on the left it rises from \(-\infty\) and on the right it falls to \(+\infty\)."),
       D(r"\text{%s: }%s\qquad \text{%s: }%s\qquad \text{%s: }%s" % (Lt('Creixent', 'Creciente', 'Increasing'), S(sM2['mono']['+']), Lt('Constant', 'Constante', 'Constant'), S(sM2['mono']['0']), Lt('Decreixent', 'Decreciente', 'Decreasing'), S(sM2['mono']['-']))))],
 [prob(L(r"Sense dibuixar-les, digues si són creixents o decreixents: a) \(f(x)=3x-2\); b) \(g(x)=5-x\).", r"Sin dibujarlas, di si son crecientes o decrecientes: a) \(f(x)=3x-2\); b) \(g(x)=5-x\).", r"Without drawing them, say whether they increase or decrease: a) \(f(x)=3x-2\); b) \(g(x)=5-x\)."),
       P(r"Comparem dues imatges: a) \(f(0)=-2\) i \(f(1)=1\): en augmentar la \(x\), augmenta la \(y\): <strong>creixent</strong>. b) \(g(0)=5\) i \(g(1)=4\): <strong>decreixent</strong>.", r"Comparamos dos imágenes: a) \(f(0)=-2\) y \(f(1)=1\): al aumentar la \(x\), aumenta la \(y\): <strong>creciente</strong>. b) \(g(0)=5\) y \(g(1)=4\): <strong>decreciente</strong>.", r"Compare two images: a) \(f(0)=-2\) and \(f(1)=1\): as \(x\) goes up, \(y\) goes up: <strong>increasing</strong>. b) \(g(0)=5\) and \(g(1)=4\): <strong>decreasing</strong>."),
       P(r"En una funció de la forma \(y=mx+n\), el signe de \(m\) ho decideix: \(m>0\) creix i \(m<0\) decreix.", r"En una función de la forma \(y=mx+n\), el signo de \(m\) lo decide: \(m>0\) crece y \(m<0\) decrece.", r"For a function of the form \(y=mx+n\), the sign of \(m\) decides: \(m>0\) increases and \(m<0\) decreases."))],
 [prob(L(r"Dibuixa la gràfica d'una funció de domini \([-4,\,4]\) que siga creixent en \((-4,\,0)\) i decreixent en \((0,\,4)\), amb \(f(0)=3\) i \(f(-4)=f(4)=-1\).", r"Dibuja la gráfica de una función de dominio \([-4,\,4]\) que sea creciente en \((-4,\,0)\) y decreciente en \((0,\,4)\), con \(f(0)=3\) y \(f(-4)=f(4)=-1\).", r"Sketch a function with domain \([-4,\,4]\) that increases on \((-4,\,0)\) and decreases on \((0,\,4)\), with \(f(0)=3\) and \(f(-4)=f(4)=-1\)."),
       P(r"Hi ha moltes respostes. La més senzilla uneix els punts \((-4,\,-1)\), \((0,\,3)\) i \((4,\,-1)\) amb segments:", r"Hay muchas respuestas. La más sencilla une los puntos \((-4,\,-1)\), \((0,\,3)\) y \((4,\,-1)\) con segmentos:", r"There are many answers. The simplest joins \((-4,\,-1)\), \((0,\,3)\) and \((4,\,-1)\) with straight segments:"),
       figs(gr(F(('c', [(-4, -1), (0, 3), (4, -1)], 'c')), mono=True, W=240)))])
assert S(sM2['mono']['+']) == r'(-\infty,\,-1)' and S(sM2['mono']['0']) == r'(-1,\,2)' and S(sM2['mono']['-']) == r'(2,\,+\infty)'
fR = F(('c', [(-4, -1), (0, 3), (4, -1)], 'c')); sR = st(fR); assert S(sR['mono']['+']) == r'(-4,\,0)' and S(sR['mono']['-']) == r'(0,\,4)'
fT = F(('c', [(-3, 2), (-1, -2), (2, 4), (4, 1)], 'c')); sT = st(fT)
s5 += practice([
  ('★', L(r"a) Una funció uneix amb segments els punts \((-3,\,2)\), \((-1,\,-2)\), \((2,\,4)\) i \((4,\,1)\). On creix i on decreix?", r"a) Una función une con segmentos los puntos \((-3,\,2)\), \((-1,\,-2)\), \((2,\,4)\) y \((4,\,1)\). ¿Dónde crece y dónde decrece?", r"a) A function joins \((-3,\,2)\), \((-1,\,-2)\), \((2,\,4)\) and \((4,\,1)\) with segments. Where does it increase and decrease?")),
  ('★★', L(r"b) És creixent o decreixent \(f(x)=-2x+7\)? I \(g(x)=\tfrac{x}{3}\)?", r"b) ¿Es creciente o decreciente \(f(x)=-2x+7\)? ¿Y \(g(x)=\tfrac{x}{3}\)?", r"b) Is \(f(x)=-2x+7\) increasing or decreasing? And \(g(x)=\tfrac{x}{3}\)?")),
  ('★★★', L(r"c) La Laura diu que la funció de l'apartat a) «creix en \((-2,\,4)\)». Quin error ha comés?", r"c) Laura dice que la función del apartado a) «crece en \((-2,\,4)\)». ¿Qué error ha cometido?", r"c) Laura says the function in a) “increases on \((-2,\,4)\)”. What mistake has she made?"))],
  D(r"\text{a)}\ \text{%s: }%s;\ \ \text{%s: }%s\qquad \text{b)}\ f\ \text{%s},\ \ g\ \text{%s}" % (Lt('creix', 'crece', 'increases'), S(sT['mono']['+']), Lt('decreix', 'decrece', 'decreases'), S(sT['mono']['-']), Lt('decreixent', 'decreciente', 'decreasing'), Lt('creixent', 'creciente', 'increasing')))
  + P(r"c) Ha donat els valors de la \(y\) (de \(-2\) a \(4\)) en lloc dels de la \(x\): l'interval correcte és \((-1,\,2)\).", r"c) Ha dado los valores de la \(y\) (de \(-2\) a \(4\)) en lugar de los de la \(x\): el intervalo correcto es \((-1,\,2)\).", r"c) She gave the \(y\) values (from \(-2\) to \(4\)) instead of the \(x\) values: the right interval is \((-1,\,2)\)."))
assert S(sT['mono']['+']) == r'(-1,\,2)' and S(sT['mono']['-']) == r'(-3,\,-1)\cup (2,\,4)'

# =====================================================================
# 7.6 Màxims i mínims
# =====================================================================
fX = F(('c', [(-5, 2), (-3, 5), (0, -1), (3, 3), (5, 1)], 'c')); sX = st(fX)
assert sX['max'] == [(-3, 5), (3, 3)] and sX['min'] == [(0, -1)] and sX['amax'] == (5, [-3]) and sX['amin'] == (-1, [0])
s6 = box('def', L('Màxims i mínims relatius', 'Máximos y mínimos relativos', 'Local maxima and minima'),
  ul(L(r"Una funció té un <strong>màxim relatiu</strong> en un punt si en aquest punt <strong>passa de creixent a decreixent</strong>: és més alt que tots els punts del voltant (un «cim»).", r"Una función tiene un <strong>máximo relativo</strong> en un punto si en ese punto <strong>pasa de creciente a decreciente</strong>: es más alto que todos los puntos de alrededor (una «cima»).", r"A function has a <strong>local maximum</strong> at a point if there it <strong>changes from increasing to decreasing</strong>: it's higher than all the nearby points (a “peak”)."),
     L(r"Té un <strong>mínim relatiu</strong> si <strong>passa de decreixent a creixent</strong>: és més baix que tots els punts del voltant (una «vall»).", r"Tiene un <strong>mínimo relativo</strong> si <strong>pasa de decreciente a creciente</strong>: es más bajo que todos los puntos de alrededor (un «valle»).", r"It has a <strong>local minimum</strong> if it <strong>changes from decreasing to increasing</strong>: lower than all the nearby points (a “valley”)."))
  + P(r"Els donem com a punts \((x,\,y)\): la \(x\) diu <em>on</em> és i la \(y\), <em>quant</em> val.", r"Los damos como puntos \((x,\,y)\): la \(x\) dice <em>dónde</em> está y la \(y\), <em>cuánto</em> vale.", r"We give them as points \((x,\,y)\): \(x\) says <em>where</em> and \(y\) says <em>how much</em>."))
s6 += box('def', L('Màxim i mínim absoluts', 'Máximo y mínimo absolutos', 'Absolute maximum and minimum'),
  P(r"El <strong>màxim absolut</strong> és el valor <strong>més alt</strong> que pren la funció en tot el domini, i el <strong>mínim absolut</strong>, el <strong>més baix</strong>. Pot ser que una funció no en tinga (si puja o baixa indefinidament, o si el valor no s'arriba a assolir perquè el punt és buit).",
    r"El <strong>máximo absoluto</strong> es el valor <strong>más alto</strong> que toma la función en todo el dominio, y el <strong>mínimo absoluto</strong>, el <strong>más bajo</strong>. Puede que una función no los tenga (si sube o baja indefinidamente, o si el valor no se llega a alcanzar porque el punto es vacío).",
    r"The <strong>absolute maximum</strong> is the <strong>highest</strong> value the function takes on its whole domain, and the <strong>absolute minimum</strong> the <strong>lowest</strong>. A function may have none (if it goes up or down for ever, or if the value isn't reached because the dot is empty).")
  + figs(fig(svg(win(fX), pls=[(fX, 'c0')], dots=[(-3, 5, 'mx', '(−3, 5)'), (3, 3, 'mx', '(3, 3)'), (0, -1, 'mn', '(0, −1)')], W=300)))
  + ul(L(r"Màxims relatius en \((-3,\,5)\) i \((3,\,3)\); mínim relatiu en \((0,\,-1)\).", r"Máximos relativos en \((-3,\,5)\) y \((3,\,3)\); mínimo relativo en \((0,\,-1)\).", r"Local maxima at \((-3,\,5)\) and \((3,\,3)\); local minimum at \((0,\,-1)\)."),
       L(r"Màxim absolut: \(5\), en \(x=-3\). Mínim absolut: \(-1\), en \(x=0\).", r"Máximo absoluto: \(5\), en \(x=-3\). Mínimo absoluto: \(-1\), en \(x=0\).", r"Absolute maximum: \(5\), at \(x=-3\). Absolute minimum: \(-1\), at \(x=0\)."))
  + note(r"Els extrems del domini, com \((5,\,1)\), no són màxims ni mínims relatius (no hi ha punts a tots dos costats), però sí que poden ser el màxim o el mínim absolut.", r"Los extremos del dominio, como \((5,\,1)\), no son máximos ni mínimos relativos (no hay puntos a ambos lados), pero sí pueden ser el máximo o el mínimo absoluto.", r"Endpoints of the domain, like \((5,\,1)\), aren't local maxima or minima (there are no points on both sides), but they can be the absolute maximum or minimum.")
  + anal('ext', L('Màxims i mínims', 'Máximos y mínimos', 'Maxima and minima'), 4)
  + drill('ext', 'Entrena: troba el màxim o el mínim', 'Entrena: halla el máximo o el mínimo', 'Train: find the maximum or minimum', 'pair'))
fX2 = F(('c', [(-4, -2), (-1, 4), (1, 2), (3, 4), (6, -3)], 'c')); sX2 = st(fX2)
assert sX2['max'] == [(-1, 4), (3, 4)] and sX2['min'] == [(1, 2)] and sX2['amax'] == (4, [-1, 3]) and sX2['amin'] == (-3, [6])
fX3 = F(('o', [(-4, 3), (-1, -2), (2, 3)], 'o')); sX3 = st(fX3)
assert sX3['min'] == [(-1, -2)] and sX3['amax'] is None and sX3['amin'] == (-2, [-1])
s6 += levels(
 [prob(L(r"Troba els màxims i mínims, relatius i absoluts, d'aquesta funció.", r"Halla los máximos y mínimos, relativos y absolutos, de esta función.", r"Find the local and absolute maxima and minima of this function.") + figs(gr(fX2, W=260)),
       P(r"Màxims relatius: \((-1,\,4)\) i \((3,\,4)\). Mínim relatiu: \((1,\,2)\).", r"Máximos relativos: \((-1,\,4)\) y \((3,\,4)\). Mínimo relativo: \((1,\,2)\).", r"Local maxima: \((-1,\,4)\) and \((3,\,4)\). Local minimum: \((1,\,2)\)."),
       P(r"Màxim absolut: \(4\), que s'assoleix dues vegades, en \(x=-1\) i en \(x=3\). Mínim absolut: \(-3\), en \(x=6\) (un extrem del domini).", r"Máximo absoluto: \(4\), que se alcanza dos veces, en \(x=-1\) y en \(x=3\). Mínimo absoluto: \(-3\), en \(x=6\) (un extremo del dominio).", r"Absolute maximum: \(4\), reached twice, at \(x=-1\) and at \(x=3\). Absolute minimum: \(-3\), at \(x=6\) (an endpoint of the domain)."))],
 [prob(L(r"Té màxim absolut aquesta funció? I mínim absolut?", r"¿Tiene máximo absoluto esta función? ¿Y mínimo absoluto?", r"Does this function have an absolute maximum? An absolute minimum?") + figs(gr(fX3, W=240)),
       P(r"Mínim relatiu i absolut en \((-1,\,-2)\). <strong>No té màxim absolut</strong>: s'acosta a 3 pels dos costats, però els extrems són buits i mai no arriba a valdre 3.", r"Mínimo relativo y absoluto en \((-1,\,-2)\). <strong>No tiene máximo absoluto</strong>: se acerca a 3 por los dos lados, pero los extremos son vacíos y nunca llega a valer 3.", r"Local and absolute minimum at \((-1,\,-2)\). <strong>No absolute maximum</strong>: it approaches 3 on both sides, but the endpoints are empty so it never actually equals 3."))],
 [prob(L(r"L'altura (en m) d'una pilota llançada cap amunt és \(h(t)=20t-5t^2\), amb \(t\) en segons. Fes una taula, dibuixa-la i troba l'altura màxima.", r"La altura (en m) de una pelota lanzada hacia arriba es \(h(t)=20t-5t^2\), con \(t\) en segundos. Haz una tabla, dibújala y halla la altura máxima.", r"The height (in m) of a ball thrown upwards is \(h(t)=20t-5t^2\), with \(t\) in seconds. Make a table, draw it and find the maximum height."),
       tvf('20x-5x^2', [0, 1, 2, 3, 4], yl='h'),
       figs(fig(svg((-0.5, 4.5, -2, 23), fns=[('20x-5x^2', 'c0', 0, 4)], dots=[(2, 20, 'mx', '(2, 20)')], xl='t (s)', yl='h (m)', W=260, H=220, ys=5, gy=5))),
       P(r"Puja fins a \(t=2\) i després baixa: el <strong>màxim</strong> és \((2,\,20)\). L'altura màxima és <strong>20 m</strong>, als 2 s. Torna a terra als 4 s.", r"Sube hasta \(t=2\) y después baja: el <strong>máximo</strong> es \((2,\,20)\). La altura máxima es <strong>20 m</strong>, a los 2 s. Vuelve al suelo a los 4 s.", r"It rises until \(t=2\) and then falls: the <strong>maximum</strong> is \((2,\,20)\). The maximum height is <strong>20 m</strong>, at 2 s. It's back on the ground at 4 s."))])
for a, v in [(0, 0), (1, 15), (2, 20), (3, 15), (4, 0)]: im('20x-5x^2', a, v)
assert sp.solve(sp.diff(E('20x-5x^2'), x), x) == [2]
fY = F(('a', [(-3, 1), (-1, -3), (2, 4), (4, 0)], 'a')); sY = st(fY)
assert sY['max'] == [(2, 4)] and sY['min'] == [(-1, -3)] and sY['amax'] is None and sY['amin'] is None
s6 += practice([
  ('★', L(r"a) Una funció uneix els punts \((-4,\,1)\), \((-2,\,-3)\), \((1,\,2)\) i \((3,\,0)\). Quins són els màxims i mínims relatius?", r"a) Una función une los puntos \((-4,\,1)\), \((-2,\,-3)\), \((1,\,2)\) y \((3,\,0)\). ¿Cuáles son los máximos y mínimos relativos?", r"a) A function joins \((-4,\,1)\), \((-2,\,-3)\), \((1,\,2)\) and \((3,\,0)\). What are the local maxima and minima?")),
  ('★★', L(r"b) I els absoluts, en la funció de l'apartat a), si els extrems són plens?", r"b) ¿Y los absolutos, en la función del apartado a), si los extremos son llenos?", r"b) And the absolute ones, for the function in a), if the endpoints are filled?")),
  ('★★★', L(r"c) Si, en lloc d'acabar en \((3,\,0)\), la gràfica continua baixant indefinidament (amb una fletxa), canvia la resposta?", r"c) Si, en lugar de acabar en \((3,\,0)\), la gráfica continúa bajando indefinidamente (con una flecha), ¿cambia la respuesta?", r"c) If, instead of ending at \((3,\,0)\), the graph carries on going down for ever (with an arrow), does the answer change?"))],
  P(r"a) Mínim relatiu \((-2,\,-3)\); màxim relatiu \((1,\,2)\). b) Màxim absolut \(2\) (en \(x=1\)) i mínim absolut \(-3\) (en \(x=-2\)). c) Els relatius no canvien; continua tenint màxim absolut 2, però ja no té mínim absolut.",
    r"a) Mínimo relativo \((-2,\,-3)\); máximo relativo \((1,\,2)\). b) Máximo absoluto \(2\) (en \(x=1\)) y mínimo absoluto \(-3\) (en \(x=-2\)). c) Los relativos no cambian; sigue teniendo máximo absoluto 2, pero ya no tiene mínimo absoluto.",
    r"a) Local minimum \((-2,\,-3)\); local maximum \((1,\,2)\). b) Absolute maximum \(2\) (at \(x=1\)) and absolute minimum \(-3\) (at \(x=-2\)). c) The local ones don't change; it still has absolute maximum 2, but no absolute minimum any more."))
fZ = F(('c', [(-4, 1), (-2, -3), (1, 2), (3, 0)], 'c')); sZ = st(fZ)
assert sZ['min'] == [(-2, -3)] and sZ['max'] == [(1, 2)] and sZ['amax'] == (2, [1]) and sZ['amin'] == (-3, [-2])
fZ3 = F(('c', [(-4, 1), (-2, -3), (1, 2), (3, 0)], 'a')); sZ3 = st(fZ3)
assert sZ3['amax'] == (2, [1]) and sZ3['amin'] is None and sZ3['min'] == [(-2, -3)] and sZ3['max'] == [(1, 2)]

# =====================================================================
# 7.7 Continuïtat
# =====================================================================
fJ = F(('c', [(-5, 1), (-1, 3)], 'c'), ('o', [(-1, -1), (3, 3)], 'c')); sJ = st(fJ)
fH = F(('c', [(-4, -1), (1, 4)], 'o'), ('o', [(1, 4), (5, 0)], 'c'), pts=[(1, 1)]); sH = st(fH)
assert sJ['disc'] == [(-1, 'salt')] and sH['disc'] == [(1, 'forat')]
s7 = box('def', L('Funció contínua', 'Función continua', 'Continuous function'),
  P(r"Una funció és <strong>contínua</strong> si la seua gràfica es pot dibuixar <strong>d'un sol traç, sense alçar el llapis</strong> del paper. Si en algun punt cal alçar-lo, diem que la funció és <strong>discontínua</strong> en aquest punt.",
    r"Una función es <strong>continua</strong> si su gráfica se puede dibujar <strong>de un solo trazo, sin levantar el lápiz</strong> del papel. Si en algún punto hay que levantarlo, decimos que la función es <strong>discontinua</strong> en ese punto.",
    r"A function is <strong>continuous</strong> if its graph can be drawn <strong>in one stroke, without lifting your pencil</strong>. If at some point you have to lift it, the function is <strong>discontinuous</strong> there.")
  + P(r"Els tipus de discontinuïtat més habituals són:", r"Los tipos de discontinuidad más habituales son:", r"The most common kinds of discontinuity are:")
  + figs(gr(fJ, L(r'Salt en \(x=-1\)', r'Salto en \(x=-1\)', r'Jump at \(x=-1\)'), guides=[-1], W=220),
         gr(fH, L(r'Punt desplaçat en \(x=1\)', r'Punto desplazado en \(x=1\)', r'Moved point at \(x=1\)'), guides=[1], W=220),
         fig(svg((-5, 5, -5, 5), fns=[('2/x', 'c0', -5, -0.01), ('2/x', 'c0', 0.01, 5)], guides=[0], W=220), L(r'\(f(x)=\frac{2}{x}\): branques en \(x=0\)', r'\(f(x)=\frac{2}{x}\): ramas en \(x=0\)', r'\(f(x)=\frac{2}{x}\): branches at \(x=0\)')), three=True)
  + ul(L(r"<strong>Salt</strong>: la gràfica «bota» d'una altura a una altra.", r"<strong>Salto</strong>: la gráfica «salta» de una altura a otra.", r"<strong>Jump</strong>: the graph “jumps” from one height to another."),
       L(r"<strong>Punt que falta o desplaçat</strong>: la gràfica arriba al punt pels dos costats, però el punt no hi és o és en un altre lloc.", r"<strong>Punto que falta o desplazado</strong>: la gráfica llega al punto por los dos lados, pero el punto no está o está en otro lugar.", r"<strong>Missing or moved point</strong>: the graph reaches the point from both sides, but the point isn't there or is somewhere else."),
       L(r"<strong>Branques infinites</strong>: la gràfica puja o baixa sense límit a prop d'un valor que no és del domini, com \(x=0\) en \(\frac{2}{x}\).", r"<strong>Ramas infinitas</strong>: la gráfica sube o baja sin límite cerca de un valor que no es del dominio, como \(x=0\) en \(\frac{2}{x}\).", r"<strong>Infinite branches</strong>: the graph shoots up or down near a value outside the domain, like \(x=0\) in \(\frac{2}{x}\).")))
park = F(('o', [(0, 2), (1, 2)], 'c'), ('o', [(1, 3.5), (2, 3.5)], 'c'), ('o', [(2, 5), (3, 5)], 'c'), ('o', [(3, 6.5), (4, 6.5)], 'c'))
sPk = st(park)
assert [d[0] for d in sPk['disc']] == [1, 2, 3] and all(d[1] == 'salt' for d in sPk['disc'])
s7 += box('prop', L('Funcions definides a trossos', 'Funciones definidas a trozos', 'Piecewise functions'),
  P(r"Moltes tarifes es calculen per trams. Un aparcament cobra <strong>2 € la primera hora</strong> (o fracció) i <strong>1,50 € cada hora més</strong> (o fracció). El preu és constant dins de cada hora i fa un salt quan comença l'hora següent: és una <strong>funció esglaonada</strong>, discontínua en \(t=1,\,2,\,3\ldots\)",
    r"Muchas tarifas se calculan por tramos. Un aparcamiento cobra <strong>2 € la primera hora</strong> (o fracción) y <strong>1,50 € cada hora más</strong> (o fracción). El precio es constante dentro de cada hora y da un salto cuando empieza la hora siguiente: es una <strong>función escalonada</strong>, discontinua en \(t=1,\,2,\,3\ldots\)",
    r"Many prices are charged in bands. A car park charges <strong>€2 for the first hour</strong> (or part of it) and <strong>€1.50 for each extra hour</strong> (or part). The price is constant within each hour and jumps when the next hour starts: it's a <strong>step function</strong>, discontinuous at \(t=1,\,2,\,3\ldots\)")
  + figs(fig(svg((-0.5, 4.5, -0.5, 7.5), pls=[(park, 'c0')], xl='t (h)', yl='€', W=280, H=240)))
  + P(r"Una funció a trossos també es pot donar amb una fórmula per a cada tros:", r"Una función a trozos también se puede dar con una fórmula para cada trozo:", r"A piecewise function can also be given by a formula for each piece:")
  + D(r"f(x)=\begin{cases}x+2 & \text{%s }x<1\\ 5-x & \text{%s }x\ge1\end{cases}\qquad f(0)=2,\quad f(1)=4,\quad f(3)=2" % (Lt('si', 'si', 'if'), Lt('si', 'si', 'if')))
  + P(r"Per l'esquerra de 1, el primer tros s'acosta a \(1+2=3\); en \(x=1\) i a la dreta val \(5-1=4\). Les altures no coincideixen: la funció fa un <strong>salt</strong> en \(x=1\).", r"Por la izquierda de 1, el primer trozo se acerca a \(1+2=3\); en \(x=1\) y a la derecha vale \(5-1=4\). Las alturas no coinciden: la función da un <strong>salto</strong> en \(x=1\).", r"To the left of 1 the first piece approaches \(1+2=3\); at \(x=1\) and to the right it's \(5-1=4\). The heights don't match: the function <strong>jumps</strong> at \(x=1\).")
  + figs(gr(F(('a', [(0, 2), (1, 3)], 'o'), ('c', [(1, 4), (3, 2)], 'a')), guides=[1], W=240))
  + anal('cont', L('Continuïtat', 'Continuidad', 'Continuity'), 4)
  + drill('cont', 'Entrena: és contínua?', 'Entrena: ¿es continua?', 'Train: is it continuous?', 'opts'))
fPw = F(('a', [(0, 2), (1, 3)], 'o'), ('c', [(1, 4), (3, 2)], 'a')); sPw = st(fPw); assert sPw['disc'] == [(1, 'salt')]
fK = F(('c', [(-4, 1), (0, 1)], 'o'), ('c', [(0, 2), (3, 2)], 'o'), ('c', [(3, 3), (6, 3)], 'c')); sK = st(fK)
assert [d[0] for d in sK['disc']] == [0, 3]
s7 += levels(
 [prob(L(r"És contínua aquesta funció? Si no ho és, digues on és discontínua i de quin tipus.", r"¿Es continua esta función? Si no lo es, di dónde es discontinua y de qué tipo.", r"Is this function continuous? If not, say where it's discontinuous and what kind.") + figs(gr(fK, W=260)),
       P(r"No: és discontínua en \(x=0\) i en \(x=3\), on fa dos <strong>salts</strong>. És una funció esglaonada.", r"No: es discontinua en \(x=0\) y en \(x=3\), donde da dos <strong>saltos</strong>. Es una función escalonada.", r"No: it's discontinuous at \(x=0\) and at \(x=3\), where it makes two <strong>jumps</strong>. It's a step function."))],
 [prob(L(r"Un servei de missatgeria cobra 4 € per paquets de fins a 2 kg (inclosos), 6 € de més de 2 kg fins a 5 kg i 9 € de més de 5 kg fins a 10 kg. Dibuixa la funció i digues on és discontínua.", r"Un servicio de mensajería cobra 4 € por paquetes de hasta 2 kg (incluidos), 6 € de más de 2 kg hasta 5 kg y 9 € de más de 5 kg hasta 10 kg. Dibuja la función y di dónde es discontinua.", r"A courier charges €4 for parcels up to 2 kg (inclusive), €6 for over 2 kg up to 5 kg and €9 for over 5 kg up to 10 kg. Draw the function and say where it's discontinuous."),
       figs(fig(svg((-0.5, 11, -1, 11), pls=[(F(('o', [(0, 4), (2, 4)], 'c'), ('o', [(2, 6), (5, 6)], 'c'), ('o', [(5, 9), (10, 9)], 'c')), 'c0')], xl='kg', yl='€', W=280, H=230, xs=2, ys=2))),
       P(r"Discontínua en \(x=2\) i en \(x=5\) (salts). El punt ple va a l'esquerra: un paquet de 2 kg justos paga 4 €.", r"Discontinua en \(x=2\) y en \(x=5\) (saltos). El punto lleno va a la izquierda: un paquete de 2 kg justos paga 4 €.", r"Discontinuous at \(x=2\) and \(x=5\) (jumps). The filled dot is on the left: a parcel of exactly 2 kg costs €4."))],
 [prob(L(r"Donada \(f(x)=\begin{cases}2x-1 & \text{si } x\le2\\ x+a & \text{si } x>2\end{cases}\), quin valor ha de tindre \(a\) perquè siga contínua?", r"Dada \(f(x)=\begin{cases}2x-1 & \text{si } x\le2\\ x+a & \text{si } x>2\end{cases}\), ¿qué valor tiene que tener \(a\) para que sea continua?", r"Given \(f(x)=\begin{cases}2x-1 & \text{if } x\le2\\ x+a & \text{if } x>2\end{cases}\), what must \(a\) be for it to be continuous?"),
       P(r"Cada tros és una recta, així que només pot fallar en \(x=2\). Els dos trossos han d'arribar a la mateixa altura:", r"Cada trozo es una recta, así que solo puede fallar en \(x=2\). Los dos trozos tienen que llegar a la misma altura:", r"Each piece is a straight line, so it can only break at \(x=2\). Both pieces must reach the same height:"),
       D(r"2\cdot2-1=3\qquad 2+a=3\Rightarrow \boxed{a=1}"))])
assert 2 * 2 - 1 == 2 + 1
fQ = F(('c', [(-3, -1), (0, 2)], 'o'), ('c', [(0, 0), (2, 2)], 'c')); sQ = st(fQ); assert sQ['disc'] == [(0, 'salt')]
s7 += practice([
  ('★', L(r"a) Un tros va de \((-3,\,-1)\) a \((0,\,2)\) amb el final buit, i un altre, de \((0,\,0)\) a \((2,\,2)\), amb els extrems plens. És contínua?", r"a) Un trozo va de \((-3,\,-1)\) a \((0,\,2)\) con el final vacío, y otro, de \((0,\,0)\) a \((2,\,2)\), con los extremos llenos. ¿Es continua?", r"a) One piece goes from \((-3,\,-1)\) to \((0,\,2)\) with an empty end, and another from \((0,\,0)\) to \((2,\,2)\) with filled ends. Is it continuous?")),
  ('★★', L(r"b) Calcula \(f(-2)\), \(f(1)\) i \(f(4)\) si \(f(x)=\begin{cases}x^2 & \text{si } x<1\\ 3x-2 & \text{si } x\ge1\end{cases}\). És contínua en \(x=1\)?", r"b) Calcula \(f(-2)\), \(f(1)\) y \(f(4)\) si \(f(x)=\begin{cases}x^2 & \text{si } x<1\\ 3x-2 & \text{si } x\ge1\end{cases}\). ¿Es continua en \(x=1\)?", r"b) Work out \(f(-2)\), \(f(1)\) and \(f(4)\) if \(f(x)=\begin{cases}x^2 & \text{if } x<1\\ 3x-2 & \text{if } x\ge1\end{cases}\). Is it continuous at \(x=1\)?")),
  ('★★★', L(r"c) És contínua la funció \(f(x)=\dfrac{1}{x-3}\)? On falla?", r"c) ¿Es continua la función \(f(x)=\dfrac{1}{x-3}\)? ¿Dónde falla?", r"c) Is \(f(x)=\dfrac{1}{x-3}\) continuous? Where does it break?"))],
  P(r"a) No: en \(x=0\) fa un salt (de 2 a 0). b) \(f(-2)=4\), \(f(1)=1\), \(f(4)=10\). Sí: \(1^2=1\) i \(3\cdot1-2=1\), els dos trossos s'uneixen. c) No és contínua en \(x=3\): no és del domini i la gràfica té branques infinites.",
    r"a) No: en \(x=0\) da un salto (de 2 a 0). b) \(f(-2)=4\), \(f(1)=1\), \(f(4)=10\). Sí: \(1^2=1\) y \(3\cdot1-2=1\), los dos trozos se unen. c) No es continua en \(x=3\): no es del dominio y la gráfica tiene ramas infinitas.",
    r"a) No: at \(x=0\) it jumps (from 2 to 0). b) \(f(-2)=4\), \(f(1)=1\), \(f(4)=10\). Yes: \(1^2=1\) and \(3\cdot1-2=1\), so the pieces join up. c) It isn't continuous at \(x=3\): 3 isn't in the domain and the graph has infinite branches."))
im('x^2', -2, 4); im('3x-2', 1, 1); im('3x-2', 4, 10)

# =====================================================================
# 7.8 Problemes amb funcions
# =====================================================================
temp = F(('c', [(0, 6), (6, 2), (14, 18), (18, 14), (24, 8)], 'c')); sTe = st(temp)
assert S(sTe['mono']['+']) == r'(6,\,14)' and S(sTe['mono']['-']) == r'(0,\,6)\cup (14,\,24)' and sTe['amax'] == (18, [14]) and sTe['amin'] == (2, [6])
s8 = box('prop', L("Estudi complet d'una gràfica", 'Estudio completo de una gráfica', 'Full study of a graph'),
  P(r"Per a estudiar una funció a partir de la gràfica, repassem en ordre totes les característiques: <strong>domini i recorregut</strong>, <strong>punts de tall</strong> amb els eixos, <strong>creixement</strong> i <strong>decreixement</strong>, <strong>màxims i mínims</strong> i <strong>continuïtat</strong>. Si la gràfica descriu una situació real, interpretem cada característica en el context.",
    r"Para estudiar una función a partir de la gráfica, repasamos en orden todas las características: <strong>dominio y recorrido</strong>, <strong>puntos de corte</strong> con los ejes, <strong>crecimiento</strong> y <strong>decrecimiento</strong>, <strong>máximos y mínimos</strong> y <strong>continuidad</strong>. Si la gráfica describe una situación real, interpretamos cada característica en el contexto.",
    r"To study a function from its graph, go through all its features in order: <strong>domain and range</strong>, <strong>axis crossings</strong>, where it <strong>increases</strong> and <strong>decreases</strong>, <strong>maxima and minima</strong> and <strong>continuity</strong>. If the graph describes a real situation, interpret each feature in context.")
  + P(r"La gràfica mostra la temperatura d'un dia de primavera (hores de 0 a 24):", r"La gráfica muestra la temperatura de un día de primavera (horas de 0 a 24):", r"The graph shows the temperature on a spring day (hours 0 to 24):")
  + figs(fig(svg((-1, 25, -2, 21), pls=[(temp, 'c0')], dots=[(14, 18, 'mx', '(14, 18)'), (6, 2, 'mn', '(6, 2)')], xl='h', yl='T (°C)', W=330, H=250, xs=2, ys=2)))
  + '<div class="tbl-wrap"><table class="data"><tbody>'
  + ''.join(f'<tr><th>{a}</th><td>{b}</td></tr>' for a, b in [
    (L('Domini', 'Dominio', 'Domain'), r'\(%s\)' % S(sTe['dom']) + ' ' + L('(les 24 hores del dia)', '(las 24 horas del día)', '(the 24 hours of the day)')),
    (L('Recorregut', 'Recorrido', 'Range'), r'\(%s\)' % S(sTe['rec']) + ' ' + L('(entre 2 °C i 18 °C)', '(entre 2 °C y 18 °C)', '(between 2 °C and 18 °C)')),
    (L('Creixent', 'Creciente', 'Increasing'), r'\(%s\)' % S(sTe['mono']['+']) + ' ' + L(': de 6 h a 14 h s\'escalfa', ': de 6 h a 14 h se calienta', ': it warms up from 6:00 to 14:00')),
    (L('Decreixent', 'Decreciente', 'Decreasing'), r'\(%s\)' % S(sTe['mono']['-'])),
    (L('Màxim', 'Máximo', 'Maximum'), r'\((14,\,18)\)' + ' ' + L(': a les 14 h hi ha la temperatura més alta, 18 °C', ': a las 14 h se da la temperatura más alta, 18 °C', ': the highest temperature, 18 °C, is at 14:00')),
    (L('Mínim', 'Mínimo', 'Minimum'), r'\((6,\,2)\)' + ' ' + L(': a les 6 h, la més baixa, 2 °C', ': a las 6 h, la más baja, 2 °C', ': the lowest, 2 °C, at 6:00')),
    (L('Continuïtat', 'Continuidad', 'Continuity'), L('contínua: la temperatura no canvia de cop', 'continua: la temperatura no cambia de golpe', 'continuous: the temperature doesn\'t change suddenly'))])
  + '</tbody></table></div>'
  + anal('all', L('Estudi complet', 'Estudio completo', 'Full study'), 3))
s8 += box('prop', L('Problemes amb fórmules', 'Problemas con fórmulas', 'Word problems with formulas'),
  P(r"Quan el problema dona (o ens fa trobar) la fórmula, les preguntes més habituals són de dos tipus:", r"Cuando el problema da (o nos hace hallar) la fórmula, las preguntas más habituales son de dos tipos:", r"When the problem gives us the formula (or we have to find it), the usual questions are of two kinds:")
  + ul(L(r"Donat el valor de la \(x\), calcular la \(y\): és una <strong>imatge</strong> (substituïm).", r"Dado el valor de la \(x\), calcular la \(y\): es una <strong>imagen</strong> (sustituimos).", r"Given \(x\), find \(y\): it's an <strong>image</strong> (substitute)."),
       L(r"Donat el valor de la \(y\), trobar la \(x\): és una <strong>antiimatge</strong> (resolem una equació).", r"Dado el valor de la \(y\), hallar la \(x\): es una <strong>antiimagen</strong> (resolvemos una ecuación).", r"Given \(y\), find \(x\): it's a <strong>preimage</strong> (solve an equation)."))
  + drill('prob', 'Entrena: problemes de tarifes', 'Entrena: problemas de tarifas', 'Train: pricing problems'))
s8 += levels(
 [prob(L(r"Una empresa de lloguer de bicis cobra 5 € fixos més 2 € per hora. a) Escriu la fórmula. b) Quant costen 3 h? c) Quantes hores pots llogar-la amb 17 €?", r"Una empresa de alquiler de bicis cobra 5 € fijos más 2 € por hora. a) Escribe la fórmula. b) ¿Cuánto cuestan 3 h? c) ¿Cuántas horas puedes alquilarla con 17 €?", r"A bike hire company charges a fixed €5 plus €2 per hour. a) Write the formula. b) How much do 3 hours cost? c) How many hours can you hire it for with €17?"),
       D(r"\text{a)}\ f(x)=5+2x\qquad \text{b)}\ f(3)=5+6=11\ €\qquad \text{c)}\ 5+2x=17\Rightarrow 2x=12\Rightarrow x=6\ \text{h}"))],
 [prob(L(r"Un dipòsit de 200 L té 50 L d'aigua. S'omple durant 10 min fins a dalt, es manté ple 15 min i després es buida en 15 min. Dibuixa la gràfica i estudia-la.", r"Un depósito de 200 L tiene 50 L de agua. Se llena durante 10 min hasta arriba, se mantiene lleno 15 min y después se vacía en 15 min. Dibuja la gráfica y estúdiala.", r"A 200 L tank holds 50 L of water. It fills to the top in 10 min, stays full for 15 min and then empties in 15 min. Draw the graph and study it."),
       figs(fig(svg((-2, 42, -20, 220), pls=[(F(('c', [(0, 50), (10, 200), (25, 200), (40, 0)], 'c')), 'c0')], xl='t (min)', yl='V (L)', W=300, H=230, xs=5, ys=50, gx=5, gy=25))),
       P(r"Domini \([0,\,40]\), recorregut \([0,\,200]\). Creix en \((0,\,10)\) (s'omple a 15 L/min), és constant en \((10,\,25)\) i decreix en \((25,\,40)\) (es buida a \(200:15\approx13{,}3\) L/min). Màxim absolut 200 L; mínim absolut 0 L, en el minut 40. És contínua.",
         r"Dominio \([0,\,40]\), recorrido \([0,\,200]\). Crece en \((0,\,10)\) (se llena a 15 L/min), es constante en \((10,\,25)\) y decrece en \((25,\,40)\) (se vacía a \(200:15\approx13{,}3\) L/min). Máximo absoluto 200 L; mínimo absoluto 0 L, en el minuto 40. Es continua.",
         r"Domain \([0,\,40]\), range \([0,\,200]\). It increases on \((0,\,10)\) (filling at 15 L/min), is constant on \((10,\,25)\) and decreases on \((25,\,40)\) (emptying at \(200\div15\approx13.3\) L/min). Absolute maximum 200 L; absolute minimum 0 L, at minute 40. It's continuous."))],
 [prob(L(r"Amb 40 m de tela metàl·lica volem tancar un hort rectangular. a) Escriu l'àrea en funció de la base \(x\). b) Fes una taula i digues quina base dona l'àrea màxima.", r"Con 40 m de tela metálica queremos cercar un huerto rectangular. a) Escribe el área en función de la base \(x\). b) Haz una tabla y di qué base da el área máxima.", r"We want to fence a rectangular vegetable patch with 40 m of wire mesh. a) Write the area as a function of the base \(x\). b) Make a table and say which base gives the largest area."),
       P(r"a) Base + altura = 20 m (la meitat del perímetre), així que l'altura és \(20-x\):", r"a) Base + altura = 20 m (la mitad del perímetro), así que la altura es \(20-x\):", r"a) Base + height = 20 m (half the perimeter), so the height is \(20-x\):"),
       D(r"A(x)=x\,(20-x)=20x-x^2,\qquad \mathrm{Dom}\,A=(0,\,20)"),
       tvf('20x-x^2', [2, 5, 8, 10, 12, 15, 18], yl='A'),
       P(r"b) L'àrea creix fins a \(x=10\) i després decreix: el màxim és \((10,\,100)\). L'hort més gran és un <strong>quadrat de 10 m</strong> de costat, amb 100 m².", r"b) El área crece hasta \(x=10\) y después decrece: el máximo es \((10,\,100)\). El huerto más grande es un <strong>cuadrado de 10 m</strong> de lado, con 100 m².", r"b) The area increases up to \(x=10\) and then decreases: the maximum is \((10,\,100)\). The biggest patch is a <strong>10 m square</strong>, with an area of 100 m²."))])
im('5+2x', 3, 11); im('5+2x', 6, 17); im('20x-x^2', 10, 100); assert sp.solve(sp.diff(E('20x-x^2'), x), x) == [10]
tank = F(('c', [(0, 50), (10, 200), (25, 200), (40, 0)], 'c')); sTk = st(tank)
assert S(sTk['dom']) == r'[0,\,40]' and S(sTk['rec']) == r'[0,\,200]' and S(sTk['mono']['+']) == r'(0,\,10)' and S(sTk['mono']['0']) == r'(10,\,25)' and S(sTk['mono']['-']) == r'(25,\,40)' and sTk['disc'] == []
s8 += practice([
  ('★', L(r"a) Una companyia de llum cobra 15 € al mes més 0,20 € per kWh. Escriu la fórmula i calcula la factura d'un mes amb 250 kWh.", r"a) Una compañía de luz cobra 15 € al mes más 0,20 € por kWh. Escribe la fórmula y calcula la factura de un mes con 250 kWh.", r"a) An electricity company charges €15 a month plus €0.20 per kWh. Write the formula and work out the bill for a month with 250 kWh.")),
  ('★★', L(r"b) En la mateixa companyia, quants kWh s'han gastat si la factura és de 71 €?", r"b) En la misma compañía, ¿cuántos kWh se han gastado si la factura es de 71 €?", r"b) With the same company, how many kWh were used if the bill is €71?")),
  ('★★★', L(r"c) Una pedra cau des de 45 m d'altura i la seua altura és \(h(t)=45-5t^2\). Quant tarda a arribar a terra? Quin és el domini que té sentit?", r"c) Una piedra cae desde 45 m de altura y su altura es \(h(t)=45-5t^2\). ¿Cuánto tarda en llegar al suelo? ¿Cuál es el dominio que tiene sentido?", r"c) A stone falls from a height of 45 m and its height is \(h(t)=45-5t^2\). How long does it take to hit the ground? What domain makes sense?"))],
  D(r"\text{a)}\ f(x)=15+0{,}2x;\ \ f(250)=65\ €\qquad \text{b)}\ 15+0{,}2x=71\Rightarrow x=280\ \text{kWh}")
  + D(r"\text{c)}\ 45-5t^2=0\Rightarrow t^2=9\Rightarrow t=3\ \text{s};\qquad \mathrm{Dom}=[0,\,3]"))
im('15+0.2*x', 250, 65); im('15+0.2*x', 280, 71); assert sp.solve(E('45-5x^2'), x) == [-3, 3]

# ============================================================ muntatge
SECS = [
  (L('Concepte de funció', 'Concepto de función', 'What is a function?'), s1),
  (L("Expressió d'una funció", 'Expresión de una función', 'Ways of describing a function'), s2),
  (L('Les funcions i els seus gràfics', 'Las funciones y sus gráficas', 'Functions and their graphs'), s3),
  (L('Domini i recorregut', 'Dominio y recorrido', 'Domain and range'), s4),
  (L('Creixement i decreixement', 'Crecimiento y decrecimiento', 'Increasing and decreasing'), s5),
  (L('Màxims i mínims', 'Máximos y mínimos', 'Maxima and minima'), s6),
  (L('Continuïtat', 'Continuidad', 'Continuity'), s7),
  (L('Problemes amb funcions', 'Problemas con funciones', 'Word problems with functions'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', "<title>Funcions · FentMates</title>")
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 7 (Funcions) de 3r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "f(x)";')
assert "Funcions · FentMates" in head and 'content: "f(x)"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
js = js.replace('/*QUIZ*/\n', open(os.path.join(HERE, 'quiz.js'), encoding='utf-8').read())
assert 'NSEC = %d' % NS in js and '/*QUIZ*/' not in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">7.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../3eso.html">{L("3r ESO", "3º ESO", "3rd ESO (Year 9)")}</a> / {L("Unitat 7", "Unidad 7", "Unit 7")}</span>
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
    <h1><span class="u">{L("Unitat 7", "Unidad 7", "Unit 7")}</span> · {L("Funcions", "Funciones", "Functions")}</h1>
    <p>{L("Concepte de funció, maneres d'expressar-la (enunciat, taula, gràfica i fórmula), representació i interpretació de gràfiques, domini i recorregut, creixement i decreixement, màxims i mínims, continuïtat i problemes amb funcions: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Concepto de función, maneras de expresarla (enunciado, tabla, gráfica y fórmula), representación e interpretación de gráficas, dominio y recorrido, crecimiento y decrecimiento, máximos y mínimos, continuidad y problemas con funciones: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "What a function is, ways of describing it (words, table, graph and formula), drawing and reading graphs, domain and range, increasing and decreasing, maxima and minima, continuity and word problems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 7: Funcions · 3r ESO", "Apuntes de teoría · Unidad 7: Funciones · 3º ESO", "Theory notes · Unit 7: Functions · 3rd ESO")}</p>
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
_tema.VERSION = "20261030f7"
_tema.aplica_fitxer(OUT)
