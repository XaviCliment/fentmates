# Ajudes compartides pels apunts de la Unitat 3 de 2n ESO (alg.py, pol.py, build.py).
# Fetes a partir de ../3eso-t4/build.py (mateixos ginys i el mateix estil), amb la numeració 3.x.
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
    return (f'\n<!-- ======================= 3.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">3.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'

# ---------- ginys ----------
def drill(kind, va, es, en):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='w'):
    return f'<label>{lab} <input class="tin {cls}" type="text" inputmode="text" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls=''):
    return (f'<div class="widget{extra_cls}" id="{wid}">\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
HELP = '<p class="hint-s">' + L("Escriu les potències amb ^ (x^2) i el producte amb * o sense signe (3x).", "Escribe las potencias con ^ (x^2) y el producto con * o sin signo (3x).", "Type powers with ^ (x^2) and products with * or no sign (3x).") + '</p>'
STEPCTL = '<div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><span class="step-count"></span></div>'

# ---------- àlgebra amb sympy (per a comprovar i escriure resultats) ----------
x, y, z = sp.symbols('x y z')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s, transformations=TR, local_dict={'x': x, 'y': y, 'z': z, 'a': sp.Symbol('a'), 'b': sp.Symbol('b')}) if isinstance(s, str) else s
def chk(lhs, rhs):
    assert sp.expand(S(lhs) - S(rhs)) == 0, (lhs, rhs, sp.expand(S(lhs)))
def ntex(c):
    c = sp.Rational(c)
    if c.q == 1: return str(c.p)
    return ('-' if c < 0 else '') + r'\frac{%d}{%d}' % (abs(c.p), c.q)
def pt(e):
    """polinomi en TeX, ordenat de grau més alt a més baix"""
    e = sp.expand(S(e))
    if e == 0: return '0'
    gens = sorted(e.free_symbols, key=str)
    if not gens: return ntex(e)
    out = ''
    for mon, c in sp.Poly(e, *gens).terms(order='grlex'):
        lit = ''.join(str(g) if k == 1 else '%s^{%d}' % (g, k) for g, k in zip(gens, mon) if k)
        a = abs(sp.Rational(c))
        s = (ntex(a) if a != 1 or not lit else '') + lit
        out += ('-' if c < 0 else ('+' if out else '')) + s
    return out

# ---------- taules de Ruffini i de divisió (HTML) ----------
def tt(c, k, v='x', first=False):
    c = Fr(c)
    if c == 0: return ''
def svg_sq():
    A, B = 130, 70; T = A + B
    g = (f'<rect class="ar-a" x="0" y="0" width="{A}" height="{A}"/><rect class="ar-ab" x="{A}" y="0" width="{B}" height="{A}"/>'
         f'<rect class="ar-ab" x="0" y="{A}" width="{A}" height="{B}"/><rect class="ar-b" x="{A}" y="{A}" width="{B}" height="{B}"/>'
         f'<rect class="ar-ln" x="0" y="0" width="{T}" height="{T}"/><line class="ar-ln" x1="{A}" y1="0" x2="{A}" y2="{T}"/><line class="ar-ln" x1="0" y1="{A}" x2="{T}" y2="{A}"/>'
         f'<text class="ar-t" x="{A/2}" y="{A/2+5}" text-anchor="middle">a²</text><text class="ar-t" x="{A+B/2}" y="{A/2+5}" text-anchor="middle">ab</text>'
         f'<text class="ar-t" x="{A/2}" y="{A+B/2+5}" text-anchor="middle">ab</text><text class="ar-t" x="{A+B/2}" y="{A+B/2+5}" text-anchor="middle">b²</text>'
         f'<text class="ar-tm" x="{A/2}" y="-8" text-anchor="middle">a</text><text class="ar-tm" x="{A+B/2}" y="-8" text-anchor="middle">b</text>'
         f'<text class="ar-tm" x="-10" y="{A/2+4}" text-anchor="middle">a</text><text class="ar-tm" x="-10" y="{A+B/2+4}" text-anchor="middle">b</text>')
    return f'<svg viewBox="-22 -24 {T+30} {T+32}" style="width:{T+30}px">{g}</svg>'
def svg_dif():
    A, B = 150, 60
    l = (f'<rect class="ar-a" x="0" y="0" width="{A}" height="{A-B}"/><rect class="ar-a" x="0" y="{A-B}" width="{A-B}" height="{B}"/>'
         f'<rect class="ar-cut" x="{A-B}" y="{A-B}" width="{B}" height="{B}"/><path class="ar-ln" d="M0 0 H{A} V{A-B} H{A-B} V{A} H0 Z"/>'
         f'<text class="ar-t" x="{(A-B)/2+20}" y="{(A-B)/2+10}" text-anchor="middle">a² − b²</text><text class="ar-tm" x="{A-B/2}" y="{A-B/2+5}" text-anchor="middle">b²</text>'
         f'<text class="ar-tm" x="{A/2}" y="-8" text-anchor="middle">a</text><text class="ar-tm" x="{A-B/2}" y="{A+16}" text-anchor="middle">b</text>')
    r = (f'<rect class="ar-a" x="0" y="0" width="{A+B}" height="{A-B}"/><rect class="ar-ln" x="0" y="0" width="{A+B}" height="{A-B}"/><line class="ar-ln" x1="{A}" y1="0" x2="{A}" y2="{A-B}" stroke-dasharray="4 4"/>'
         f'<text class="ar-t" x="{(A+B)/2}" y="{(A-B)/2+5}" text-anchor="middle">(a+b)(a−b)</text>'
         f'<text class="ar-tm" x="{(A+B)/2}" y="-8" text-anchor="middle">a + b</text><text class="ar-tm" x="{A+B+8}" y="{(A-B)/2+4}">a − b</text>')
    return (f'<figure><svg viewBox="-12 -24 {A+30} {A+46}" style="width:{A+30}px">{l}</svg><figcaption>{L("Al quadrat de costat a li llevem el de costat b", "Al cuadrado de lado a le quitamos el de lado b", "Remove the b-square from the a-square")}</figcaption></figure>'
            f'<figure><svg viewBox="-12 -24 {A+B+70} {A-B+40}" style="width:{A+B+70}px">{r}</svg><figcaption>{L("Movem el tros de baix al costat: és un rectangle", "Movemos el trozo de abajo al lado: es un rectángulo", "Move the bottom strip to the side: it’s a rectangle")}</figcaption></figure>')

def table(head, rows, cls='data narrow'):
    h = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr></thead>' if head else ''
    return f'<div class="tbl-wrap"><table class="{cls}">{h}<tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'
def ol(*items): return '<ol>' + ''.join(f'<li>{i}</li>' for i in items) + '</ol>'
