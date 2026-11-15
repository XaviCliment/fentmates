# Ajudes compartides pels apunts de la Unitat 5 de 2n ESO (sis1.py, sis2.py, build.py).
# Fetes a partir de ../3eso-t6/build.py (mateixos ginys i el mateix estil), amb la numeració 5.x.
import re
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

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
    return (f'\n<!-- ======================= 5.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">5.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)
def SY(a, b): return r'\begin{cases}%s\\[2pt] %s\end{cases}' % (a, b)
def R(s): return r'\ \Rightarrow\ '.join(s)
def BX(xv, yv): return r'\boxed{x=%s,\ \ y=%s}' % (xv, yv)

# ---------- ginys ----------
def drill(kind, va, es, en, opts=False):
    row = (f'<div class="wrow dopts"></div><div class="wrow"><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>' if opts else
           f'<div class="wrow"><label>{L("Solució", "Solución", "Solution")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat" placeholder="x = …, y = …"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
           + '<p class="hint-s">' + L("Escriu x = 3, y = −2 o bé 3; −2. Les fraccions, amb / (5/2).", "Escribe x = 3, y = −2 o bien 3; −2. Las fracciones, con / (5/2).", "Type x = 3, y = −2 or 3; −2. Fractions with / (5/2).") + '</p>')
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
    return (f'<div class="widget{extra_cls}" id="{wid}"{attrs}>\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
HELP = '<p class="hint-s">' + L("Escriu cada equació amb el signe =, amb les incògnites x i y. Fraccions amb / ((x+1)/2) i el producte amb * o sense signe (3x).", "Escribe cada ecuación con el signo =, con las incógnitas x e y. Fracciones con / ((x+1)/2) y el producto con * o sin signo (3x).", "Type each equation with an = sign, using the unknowns x and y. Fractions with / ((x+1)/2) and products with * or no sign (3x).") + '</p>'
def two(e1, e2): return '<div class="wrow">' + tin('e1', L('1a equació', '1.ª ecuación', '1st equation'), e1) + tin('e2', L('2a equació', '2.ª ecuación', '2nd equation'), e2) + '</div>'
def solver(wid, m, title, e1, e2, qs):
    rows = [two(e1, e2), HELP, quick([(f'{a}|{b}', f'{a.replace("-", "−")} ; {b.replace("-", "−")}') for a, b in qs])]
    if m is None:
        rows.insert(0, '<div class="wrow"><div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{str(k == "auto").lower()}">{t}</button>' for k, t in [('auto', L('El més adequat', 'El más adecuado', 'Best one')), ('sub', L('Substitució', 'Sustitución', 'Substitution')), ('igu', L('Igualació', 'Igualación', 'Equalisation')), ('red', L('Reducció', 'Reducción', 'Elimination'))]) + '</div></div>')
    return widget(wid, '🧮', title, rows, extra_cls=' w-solve', attrs=f' data-m="{m}"' if m else '')
def grafw(wid, e1, e2, qs, ratio=False):
    return widget(wid, '📈', L('Mètode gràfic', 'Método gráfico', 'Graphical method'),
                  [two(e1, e2), HELP, quick([(f'{a}|{b}', f'{a.replace("-", "−")} ; {b.replace("-", "−")}') for a, b in qs])],
                  out='<div class="gout"></div>', extra_cls=' w-graf', attrs=' data-ratio' if ratio else '')

# ---------- comprovació amb sympy ----------
x, y, k = sp.symbols('x y k')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s.replace('[', '(').replace(']', ')'), transformations=TR, local_dict={'x': x, 'y': y, 'k': k}) if isinstance(s, str) else s
def EQ(e): l, r = e.split('='); return sp.expand(S(l) - S(r))
def cs(e1, e2, want):
    """want: (x, y) o 'SCI' / 'SI'"""
    A, B = EQ(e1), EQ(e2)
    sol = sp.solve([A, B], [x, y], dict=True)
    if want == 'SI': assert sol == [], (e1, e2, sol); return
    if want == 'SCI': assert len(sol) == 1 and len(sol[0]) == 1, (e1, e2, sol); return
    assert sol == [{x: sp.nsimplify(want[0]), y: sp.nsimplify(want[1])}], (e1, e2, sol, want)
def ok(e, xv, yv): assert EQ(e).subs({x: sp.nsimplify(xv), y: sp.nsimplify(yv)}) == 0, (e, xv, yv)
def nok(e, xv, yv): assert EQ(e).subs({x: sp.nsimplify(xv), y: sp.nsimplify(yv)}) != 0, (e, xv, yv)
def same(a, b): assert sp.expand(EQ(a) - EQ(b)) == 0, (a, b)
def prop(a, b):
    """dues equacions equivalents (una múltiple de l'altra)"""
    A, B = EQ(a), EQ(b); r = sp.simplify(A / B); assert r.is_number and r != 0, (a, b, r)

# ---------- gràfiques estàtiques (SVG) ----------
def svg_graph(lines, pts=(), R=6, cap=None):
    W = H = 300
    sx = lambda v: (v + R) / (2 * R) * W
    sy = lambda v: H - (v + R) / (2 * R) * H
    g = ''
    for i in range(-R, R + 1):
        g += f'<line class="grid" x1="{sx(i):.1f}" y1="0" x2="{sx(i):.1f}" y2="{H}"/><line class="grid" x1="0" y1="{sy(i):.1f}" x2="{W}" y2="{sy(i):.1f}"/>'
    g += f'<line class="ax" x1="0" y1="{sy(0):.1f}" x2="{W}" y2="{sy(0):.1f}"/><line class="ax" x1="{sx(0):.1f}" y1="0" x2="{sx(0):.1f}" y2="{H}"/>'
    for i in range(-R + 1, R):
        if i: g += f'<text class="tk" x="{sx(i):.1f}" y="{sy(0) + 13:.1f}" text-anchor="middle">{i}</text><text class="tk" x="{sx(0) - 5:.1f}" y="{sy(i) + 4:.1f}" text-anchor="end">{i}</text>'
    g += f'<text class="tk ax-l" x="{W - 6}" y="{sy(0) - 6:.1f}" text-anchor="end">x</text><text class="tk ax-l" x="{sx(0) + 6:.1f}" y="12">y</text>'
    for j, (a, b, c, *opt) in enumerate(lines):
        X = R + 1
        p = (-X, (c + a * X) / b, X, (c - a * X) / b) if b else (c / a, -X, c / a, X)
        cls = f'ln ln{opt[0] if opt else j}' + (' dash' if len(opt) > 1 and opt[1] else '')
        g += f'<line class="{cls}" x1="{sx(p[0]):.1f}" y1="{sy(p[1]):.1f}" x2="{sx(p[2]):.1f}" y2="{sy(p[3]):.1f}"/>'
        if b: assert True
    for px, py, cls, lab in pts:
        g += f'<circle class="{cls}" cx="{sx(px):.1f}" cy="{sy(py):.1f}" r="{7 if cls == "cut" else 4}"/>'
        if lab: g += f'<text class="plab" x="{sx(px) + 8:.1f}" y="{sy(py) - 8:.1f}">{lab}</text>'
    fig = f'<svg class="sgraf" viewBox="0 0 {W} {H}" role="img" aria-label="gràfica">{g}</svg>'
    return f'<figure>{fig}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{fig}</figure>'
def figs(*f): return '<div class="figs">' + ''.join(f) + '</div>'
def tv(xs, ys, cls=''):
    return ('<div class="tbl-wrap"><table class="data tv %s"><tbody><tr><th>\\(x\\)</th>' % cls + ''.join(f'<td>\\({v}\\)</td>' for v in xs)
            + '</tr><tr><th>\\(y\\)</th>' + ''.join(f'<td>\\({v}\\)</td>' for v in ys) + '</tr></tbody></table></div>')
def tvc(e, xs, cls=''):
    """taula de valors d'una equació ax+by=c (comprovada)"""
    ys = []
    for xv in xs:
        sol = sp.solve(EQ(e).subs(x, xv), y); assert len(sol) == 1; ys.append(sol[0])
    return tv(xs, [str(v) for v in ys], cls)

