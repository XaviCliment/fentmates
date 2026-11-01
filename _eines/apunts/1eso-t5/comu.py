# Ajudes compartides pels apunts de la Unitat 5 de 1r ESO (dec.py, prop.py, build.py).
import math
from decimal import Decimal as Dm, getcontext
from fractions import Fraction as Fr
getcontext().prec = 40

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
def prob(q, *steps):
    return '<li><p class="prob-q">' + q + '</p><div class="steps">' + ''.join(f'<div class="step">{s}</div>' for s in steps) + '</div></li>\n'
def practice(items, sol):
    lis = ''.join(f'<li><span class="stars">{st}</span> {t}</li>' for st, t in items)
    return box('pr', '✍ ' + L('Practica', 'Practica', 'Practice'),
               f'<ol class="ex-list">{lis}</ol><details class="sol"><summary>{L("Mostra la solució", "Mostrar la solución", "Show the solution")}</summary><div>{sol}</div></details>')
def sec(i, title, body):
    return (f'\n<!-- ======================= 5.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">5.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def drill(kind, va, es, en):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs, attr='b'):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-{attr}="{v}">{t}</button>' for v, t in pairs) + '</div>'
def nin(k, va, es, en, val, cls='s', mode='decimal'):
    lab = L(va, es, en) + ' ' if va else ''
    return f'<label>{lab}<input class="tin {cls}" type="text" inputmode="{mode}" data-k="{k}" value="{val}" autocomplete="off" aria-label="{k}"></label>'
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def widget(wid, icon, title, inner):
    return f'<div class="widget" id="{wid}">\n  <div class="wt">{icon} {title}</div>\n{inner}  <div class="fvis"></div>\n  <div class="info" aria-live="polite"></div>\n</div>\n'
def figs(*items):
    return '<div class="figs">' + ''.join(f'<figure>{s}<figcaption>{c}</figcaption></figure>' for s, c in items) + '</div>'
def table(head, rows, cls='data'):
    h = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr></thead>' if head else ''
    return f'<div class="tbl-wrap"><table class="{cls}">{h}<tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'

# ---------- nombres decimals en TeX ----------
def n(x):
    """'1234.5' o Decimal -> 1\\,234\\dc5 (espai de milers a partir de 5 xifres)"""
    s = str(x) if not isinstance(x, str) else x
    neg = s.startswith('-'); s = s.lstrip('-')
    ip, _, fp = s.partition('.')
    if len(ip) > 4: ip = '{:,}'.format(int(ip)).replace(',', '\\,')
    return ('-' if neg else '') + ip + (r'\dc' + fp if fp else '')
def m(x): return r'\(' + n(x) + r'\)'

def ck(a, b):
    """comprova un resultat escrit a mà: a (Decimal/Fraction/int) == b (text o nombre)"""
    bb = Dm(b) if isinstance(b, str) else b
    assert Dm(str(a)) == Dm(str(bb)) if not isinstance(a, Fr) else a == Fr(str(bb)), (a, b)

# ---------- figures SVG ----------
def svg_hund(on, c=13, cols_on=None):
    """quadrat d'una unitat dividit en 100: les primeres «on» centèsimes pintades (per columnes)"""
    g = ''
    for k in range(100):
        col, row = k // 10, k % 10
        cls = 'fr-on' if k < on else 'fr-off'
        g += f'<rect class="{cls}" x="{col * c}" y="{row * c}" width="{c}" height="{c}"/>'
    g += ''.join(f'<line class="fr-thin" x1="{i * c}" y1="0" x2="{i * c}" y2="{10 * c}"/><line class="fr-thin" x1="0" y1="{i * c}" x2="{10 * c}" y2="{i * c}"/>' for i in range(1, 10))
    W = 10 * c
    return f'<svg viewBox="-1 -1 {W + 2} {W + 2}" style="width:{W + 2}px">{g}<rect class="fr-ln" x="0" y="0" width="{W}" height="{W}"/></svg>'
def svg_tenths(on, c=13):
    g = ''.join(f'<rect class="{"fr-on" if k < on else "fr-off"}" x="{k * c}" y="0" width="{c}" height="{10 * c}"/>' for k in range(10))
    g += ''.join(f'<line class="fr-ln" x1="{i * c}" y1="0" x2="{i * c}" y2="{10 * c}"/>' for i in range(1, 10))
    W = 10 * c
    return f'<svg viewBox="-1 -1 {W + 2} {W + 2}" style="width:{W + 2}px">{g}<rect class="fr-ln" x="0" y="0" width="{W}" height="{W}"/></svg>'
def fmt_lab(v, k):
    s = f'{v:.{k}f}'.replace('.', ',')
    return s
def svg_nl(a, b, parts, marks, k=1, W=460, labels='ends'):
    """recta de a a b dividida en «parts»; marks = [(valor, text)]"""
    X0, X1 = 18, W - 18
    x = lambda v: X0 + (v - a) / (b - a) * (X1 - X0)
    g = f'<line class="nl-ax" x1="4" y1="24" x2="{W - 4}" y2="24"/>'
    for j in range(parts + 1):
        v = a + (b - a) * j / parts
        big = j in (0, parts) or (labels == 'all')
        g += f'<line class="{"nl-tb" if j in (0, parts) else "nl-tk"}" x1="{x(v):.1f}" y1="{15 if j in (0, parts) else 18}" x2="{x(v):.1f}" y2="{33 if j in (0, parts) else 30}"/>'
        if big: g += f'<text class="{"fr-t" if j in (0, parts) else "fr-tm"}" x="{x(v):.1f}" y="50" text-anchor="middle">{fmt_lab(v, k)}</text>'
    for v, t in marks:
        g += f'<circle class="nl-dot" cx="{x(v):.1f}" cy="24" r="6" style="fill:var(--accent)"/><text class="fr-t" x="{x(v):.1f}" y="9" text-anchor="middle" style="fill:var(--accent)">{t}</text>'
    return f'<svg viewBox="0 -4 {W} 58" style="width:{W}px">{g}</svg>'
def svg_points(pts, xmax, ymax, xl, yl, line=True, W=300, H=210, curve=None):
    """gràfic de punts (proporcionalitat directa o inversa)"""
    X0, Y0, X1, Y1 = 40, H - 30, W - 12, 12
    x = lambda v: X0 + v / xmax * (X1 - X0)
    y = lambda v: Y0 - v / ymax * (Y0 - Y1)
    g = f'<line class="nl-ax" x1="{X0}" y1="{Y0}" x2="{X1 + 6}" y2="{Y0}"/><line class="nl-ax" x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y1 - 6}"/>'
    g += f'<text class="fr-tm" x="{X1}" y="{Y0 + 24}" text-anchor="end">{xl}</text><text class="fr-tm" x="{X0 + 6}" y="{Y1 - 2}">{yl}</text>'
    if line: g += f'<line class="nl-seg" style="stroke-width:2.5" x1="{x(0)}" y1="{y(0)}" x2="{x(xmax):.1f}" y2="{y(line * xmax):.1f}"/>'
    if curve:
        d = ' '.join(f'{"M" if i == 0 else "L"}{x(v):.1f} {y(curve / v):.1f}' for i, v in enumerate([curve / ymax + j * (xmax - curve / ymax) / 60 for j in range(61)]))
        g += f'<path class="nl-seg" style="stroke-width:2.5;fill:none" d="{d}"/>'
    for px, py in pts:
        g += f'<line class="fr-thin" stroke-dasharray="3 3" x1="{x(px):.1f}" y1="{Y0}" x2="{x(px):.1f}" y2="{y(py):.1f}"/><line class="fr-thin" stroke-dasharray="3 3" x1="{X0}" y1="{y(py):.1f}" x2="{x(px):.1f}" y2="{y(py):.1f}"/>'
        g += f'<circle class="nl-dot" cx="{x(px):.1f}" cy="{y(py):.1f}" r="5" style="fill:var(--accent)"/>'
        g += f'<text class="fr-tm" x="{x(px):.1f}" y="{Y0 + 15}" text-anchor="middle">{fmt_lab(px, 0 if px == int(px) else 1)}</text><text class="fr-tm" x="{X0 - 5}" y="{y(py) + 4:.1f}" text-anchor="end">{fmt_lab(py, 0 if py == int(py) else 1)}</text>'
    return f'<svg viewBox="0 0 {W} {H}" style="width:{W}px">{g}</svg>'
def pgrid(on):
    return '<div class="pgrid">' + ''.join('<i class="on"></i>' if k < on else '<i></i>' for k in range(100)) + '</div>'
