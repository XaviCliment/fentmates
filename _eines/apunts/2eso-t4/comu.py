# Ajudes compartides pels apunts de la Unitat 4 de 2n ESO (eq1.py, eq2.py, build.py).
# Fetes a partir de ../3eso-t5/build.py (mateixos ginys i el mateix estil), amb la numeració 4.x.
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
def sub(va, es, en): return f'<h3 class="sub">{L(va, es, en)}</h3>\n'
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
    return (f'\n<!-- ======================= 4.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">4.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)

# ---------- ginys ----------
def drill(kind, va, es, en, hint=''):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  {hint}<div class="info" aria-live="polite"></div>
</div>
'''
SETHINT = '<p class="hint-s">' + L("Si hi ha més d'una solució, separa-les amb punt i coma (3; −2). Si no en té, escriu «cap».", "Si hay más de una solución, sepáralas con punto y coma (3; −2). Si no tiene, escribe «ninguna».", "If there is more than one solution, separate them with semicolons (3; −2). If there is none, type “none”.") + '</p>'
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='w'):
    return f'<label>{lab} <input class="tin {cls}" type="text" inputmode="text" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def rng(k, lab, lo, hi, val):
    return f'<label>{lab} <input type="range" min="{lo}" max="{hi}" step="1" value="{val}" data-k="{k}"> <strong class="rv" data-v="{k}">{val}</strong></label>'
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls=''):
    return (f'<div class="widget{extra_cls}" id="{wid}">\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
HELP = '<p class="hint-s">' + L("Escriu l'equació amb el signe =. Potències amb ^ (x^2), fraccions amb / ((x+1)/2) i el producte amb * o sense signe (3x).", "Escribe la ecuación con el signo =. Potencias con ^ (x^2), fracciones con / ((x+1)/2) y el producto con * o sin signo (3x).", "Type the equation with an = sign. Powers with ^ (x^2), fractions with / ((x+1)/2) and products with * or no sign (3x).") + '</p>'

# ---------- comprovació amb sympy ----------
x = sp.symbols('x')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s, transformations=TR, local_dict={'x': x}) if isinstance(s, str) else s
def chk(lhs, rhs):
    assert sp.expand(S(lhs) - S(rhs)) == 0, (lhs, rhs, sp.expand(S(lhs)))
def ce(eq, sols):
    """comprova les solucions reals d'una equació: sols = llista, 'totes' (identitat) o [] (cap)"""
    l, r = eq.split('=')
    e = sp.expand(S(l) - S(r))
    if sols == 'totes':
        assert e == 0, (eq, e); return
    assert e != 0, eq
    got = sorted(set(v for v in sp.solve(e, x) if v.is_real), key=float)
    want = sorted(set(sp.nsimplify(S(v) if isinstance(v, str) else sp.Rational(v)) for v in sols), key=float)
    assert got == want, (eq, got, want)

