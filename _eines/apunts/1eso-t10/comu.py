# Funcions comunes dels apunts de la Unitat 10 de 1r ESO (Estadística): HTML trilingüe, ginys, càlculs estadístics
# exactes (Fraction) amb comprovacions ck(), i gràfics estadístics en SVG (app.js en té còpies: barres(), sectors()...).
import math
from fractions import Fraction

def L(va, es, en):
    return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
def Ls(va, es, en):
    """text trilingüe dins d'un <text> SVG"""
    return f'<tspan data-l="va">{va}</tspan><tspan data-l="es">{es}</tspan><tspan data-l="en">{en}</tspan>'
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
    return (f'\n<!-- ======================= 10.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">10.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s):
    """fórmula centrada; si té parts separades per \\qquad, cada part va en una fórmula i es reparteixen en una fila que es plega"""
    parts = [p.strip() for p in s.split(r'\qquad')]
    if len(parts) == 1: return r'\[' + s + r'\]'
    return '<div class="eqv">' + ''.join(r'\[' + p + r'\]' for p in parts) + '</div>'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)

# ---------- ginys ----------
def drill(kind, va, es, en, mode='dec'):
    nb = f'<button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span>'
    if mode == 'opts':
        row = f'<div class="wrow dopts"></div><div class="wrow">{nb}</div>'
    elif mode == 'click':
        row = (f'<div class="wrow">{nb}</div>'
               + '<p class="hint-s">' + L("Toca el pla en el lloc on va el punt.", "Toca el plano en el lugar donde va el punto.", "Tap the plane where the point goes.") + '</p>')
    else:
        hint = (L("Escriu el punt entre parèntesis: (2, −3).", "Escribe el punto entre paréntesis: (2, −3).", "Type the point in brackets: (2, −3).") if mode == 'pair'
                else L("Escriu un nombre (pots fer servir decimals: 8,5 o 8.5).", "Escribe un número (puedes usar decimales: 8,5 u 8.5).", "Type a number (decimals are fine: 8.5 or 8,5)."))
        im = 'text' if mode == 'pair' else 'decimal'
        row = (f'<div class="wrow"><label>{L("Resposta", "Respuesta", "Answer")} <input class="tin" type="text" inputmode="{im}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat" placeholder="…"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button>{nb}</div>'
               + '<p class="hint-s">' + hint + '</p>')
    return f'''<div class="widget w-drill" data-kind="{kind}" data-mode="{mode}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  {row}<div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='s'):
    return f'<label>{lab} <input class="tin {cls}" type="text" inputmode="decimal" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def rng(k, lo, hi, step, val, lab=''):
    # el nom i el valor els escriu el giny (showRv) dins de .rv; lab només serveix d'etiqueta accessible
    return f'<label style="flex:1"><span class="rval {k}v"></span><input type="range" data-k="{k}" min="{lo}" max="{hi}" step="{step}" value="{val}" aria-label="{lab or k}"></label>'
def widget(wid, icon, title, rows, out='<div class="gout"></div>', extra_cls='', attrs=''):
    idattr = f' id="{wid}"' if wid else ''
    return (f'<div class="widget{extra_cls}"{idattr}{attrs}>\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
def seg(items, first=0):
    return '<div class="wrow"><div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{str(i == first).lower()}">{t}</button>' for i, (k, t) in enumerate(items)) + '</div></div>'
def tbl(head, rows, cls=''):
    return ('<div class="tbl-wrap"><table class="data %s"><thead><tr>' % cls + ''.join(f'<th>{h}</th>' for h in head) + '</tr></thead><tbody>'
            + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>')

# ---------- comprovacions ----------
Fr = Fraction
NCK = [0]
def fr(v): return v if isinstance(v, Fraction) else Fraction(str(v).replace('\\dc ', '.').replace('{,}', '.').replace(',', '.'))
def ck(v, w):
    """v: valor calculat; w: el que escrivim als apunts (nombre o text «2,5»)"""
    NCK[0] += 1
    assert fr(v) == fr(w), (v, w)
    return v

# ---------- nombres ----------
def tn(v):
    """nombre en TeX amb coma decimal (\dc: en anglés es veu un punt); ha de ser exacte"""
    v = fr(v)
    if v.denominator == 1: return str(v.numerator)
    t = ('%.6f' % float(v)).rstrip('0').rstrip('.')
    assert fr(t) == v, v
    return t.replace('.', r'\dc ')
def tr(v, d=2):
    """nombre arrodonit a d decimals (TeX)"""
    t = ('%.*f' % (d, float(fr(v)))).rstrip('0').rstrip('.')
    return t.replace('.', r'\dc ')
def tx(v):
    """nombre en text (fora de fórmules): 2,5 / 2.5 segons l'idioma"""
    t = tn(v)
    return L(t.replace(r'\dc ', ','), t.replace(r'\dc ', ','), t.replace(r'\dc ', '.')) if r'\dc' in t else t
def M(s): return r'\(' + s + r'\)'

# ---------- estadística (exacta) ----------
def freqs(data, order=None):
    """[(valor, fi)] en l'ordre donat o creixent"""
    keys = order or sorted(set(data))
    return [(k, data.count(k)) for k in keys]
def mean(data): return Fraction(sum(fr(x) for x in data), len(data))
def median(data):
    d = sorted(fr(x) for x in data); n = len(d)
    return d[n // 2] if n % 2 else (d[n // 2 - 1] + d[n // 2]) / 2
def modes(data):
    c = {x: data.count(x) for x in data}; m = max(c.values())
    return sorted(k for k in c if c[k] == m)
def rang(data): return fr(max(data)) - fr(min(data))
def dm(data):
    m = mean(data); return Fraction(sum(abs(fr(x) - m) for x in data), len(data))
def expand(tab):
    """taula [(xi, fi)] → llista de dades"""
    return [x for x, f in tab for _ in range(f)]

# ---------- recompte (palets) ----------
def tally(n):
    """n en palets: grups de 4 ratlles i una de travessera"""
    out, x = '', 2
    for g in range(0, n, 5):
        k = min(5, n - g); x0 = x
        for j in range(min(k, 4)):
            out += f'<line x1="{x}" y1="3" x2="{x}" y2="17"/>'; x += 5
        if k == 5: out += f'<line x1="{x0 - 3}" y1="14" x2="{x0 + 18}" y2="6"/>'
        x += 7
    return f'<svg class="tally" viewBox="0 0 {max(x, 10)} 20" width="{max(x, 10)}" height="20" aria-label="{n}">{out}</svg>'

# ---------- gràfics estadístics (SVG); app.js en té còpies ----------
def _nice(top):
    for st in (1, 2, 5, 10, 20, 25, 50, 100, 200, 500):
        if top / st <= 8: return st
    return 1000
def _esc(t): return str(t)
def barres(cats, vals, W=300, H=190, kind='bar', yl='', xl='', step=None, hl=None, cls=None, top=None, y0=0):
    """kind: 'bar' (diagrama de barres), 'poly' (polígon de freqüències), 'both' (barres + polígon).
    cats: etiquetes de l'eix X (text), vals: alçades"""
    n = len(cats); top = top or max(vals); st = step or _nice(top - y0); top = math.ceil(top / st) * st
    L0, R0, T0, B0 = 34, 10, 16, 30
    w, h = W - L0 - R0, H - T0 - B0
    X = lambda i: L0 + w * (i + 0.5) / n
    Y = lambda v: T0 + h - h * (float(v) - y0) / (top - y0)
    g = ''
    k = y0
    while k <= top + 1e-9:
        g += f'<line class="grid" x1="{L0}" y1="{Y(k):.1f}" x2="{W - R0}" y2="{Y(k):.1f}"/><text class="tk" x="{L0 - 5}" y="{Y(k) + 4:.1f}" text-anchor="end">{num(k)}</text>'
        k += st
    g += f'<line class="ax" x1="{L0}" y1="{T0 + h}" x2="{W - R0}" y2="{T0 + h}"/><line class="ax" x1="{L0}" y1="{T0 - 6}" x2="{L0}" y2="{T0 + h}"/>'
    bw = min(34, w / n * 0.6)
    for i, (c, v) in enumerate(zip(cats, vals)):
        if kind in ('bar', 'both'):
            cc = (cls[i] if cls else 'b0') + (' hl' if hl is not None and i == hl else '')
            g += f'<rect class="bar {cc}" x="{X(i) - bw / 2:.1f}" y="{Y(v):.1f}" width="{bw:.1f}" height="{T0 + h - Y(v):.1f}"/>'
        g += f'<text class="tk xl" x="{X(i):.1f}" y="{T0 + h + 14}" text-anchor="middle">{c}</text>'
    if kind in ('poly', 'both'):
        g += '<polyline class="fpoly" points="' + ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(vals)) + '"/>'
        g += ''.join(f'<circle class="fdot" cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4"/>' for i, v in enumerate(vals))
    if yl: g += f'<text class="tk ax-t" x="{L0 + 4}" y="{T0 - 6}">{yl}</text>'
    if xl: g += f'<text class="tk ax-t" x="{W - R0}" y="{H - 2}" text-anchor="end">{xl}</text>'
    return f'<svg class="sgraf stat" viewBox="0 0 {W} {H}" role="img" aria-label="diagrama">{g}</svg>'
def hist(edges, vals, W=300, H=190, poly=False, yl='', xl='', step=None):
    """histograma: intervals [edges[i], edges[i+1]) amb freqüències vals"""
    a, b = edges[0], edges[-1]; top = max(vals); st = step or _nice(top); top = math.ceil(top / st) * st
    L0, R0, T0, B0 = 34, 14, 16, 30
    w, h = W - L0 - R0 - 16, H - T0 - B0
    X = lambda x: L0 + 8 + w * (float(x) - a) / (b - a)
    Y = lambda v: T0 + h - h * float(v) / top
    g, k = '', 0
    while k <= top + 1e-9:
        g += f'<line class="grid" x1="{L0}" y1="{Y(k):.1f}" x2="{W - R0}" y2="{Y(k):.1f}"/><text class="tk" x="{L0 - 5}" y="{Y(k) + 4:.1f}" text-anchor="end">{num(k)}</text>'
        k += st
    g += f'<line class="ax" x1="{L0}" y1="{T0 + h}" x2="{W - R0}" y2="{T0 + h}"/><line class="ax" x1="{L0}" y1="{T0 - 6}" x2="{L0}" y2="{T0 + h}"/>'
    for i, v in enumerate(vals):
        g += f'<rect class="bar b{i % 4} hist" x="{X(edges[i]):.1f}" y="{Y(v):.1f}" width="{X(edges[i + 1]) - X(edges[i]):.1f}" height="{T0 + h - Y(v):.1f}"/>'
    for e in edges: g += f'<text class="tk xl" x="{X(e):.1f}" y="{T0 + h + 14}" text-anchor="middle">{num(e)}</text>'
    if poly:
        d = edges[1] - edges[0]
        P = [(edges[0] - d / 2, 0)] + [((edges[i] + edges[i + 1]) / 2, v) for i, v in enumerate(vals)] + [(edges[-1] + d / 2, 0)]
        P = [(max(min(x, b + 8 * (b - a) / w), a - 8 * (b - a) / w), y) for x, y in P]
        g += '<polyline class="fpoly" points="' + ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in P) + '"/>'
        g += ''.join(f'<circle class="fdot" cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.5"/>' for x, y in P[1:-1])
    if yl: g += f'<text class="tk ax-t" x="{L0 + 4}" y="{T0 - 6}">{yl}</text>'
    if xl: g += f'<text class="tk ax-t" x="{W - R0}" y="{H - 2}" text-anchor="end">{xl}</text>'
    return f'<svg class="sgraf stat" viewBox="0 0 {W} {H}" role="img" aria-label="histograma">{g}</svg>'
def sectors(cats, vals, W=300, R=78, angles=False, pct=False):
    """diagrama de sectors amb llegenda; angles/pct: escriu l'angle o el percentatge dins de cada sector"""
    N = sum(vals); cx, cy = R + 8, R + 8; g = ''; a0 = -90.0
    for i, v in enumerate(vals):
        a1 = a0 + 360 * v / N
        p0 = (cx + R * math.cos(math.radians(a0)), cy + R * math.sin(math.radians(a0)))
        p1 = (cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1)))
        big = 1 if a1 - a0 > 180 else 0
        if v == N: g += f'<circle class="sec s{i % 6}" cx="{cx}" cy="{cy}" r="{R}"/>'
        elif v: g += f'<path class="sec s{i % 6}" d="M{cx} {cy}L{p0[0]:.1f} {p0[1]:.1f}A{R} {R} 0 {big} 1 {p1[0]:.1f} {p1[1]:.1f}Z"/>'
        if (angles or pct) and v:
            am = math.radians((a0 + a1) / 2); r = R * 0.64
            t = num(Fraction(360 * v, N)) + '°' if angles else num(Fraction(100 * v, N)) + ' %'
            g += f'<text class="slab" x="{cx + r * math.cos(am):.1f}" y="{cy + r * math.sin(am) + 4:.1f}" text-anchor="middle">{t}</text>'
        a0 = a1
    lx = 2 * R + 28; ly = max(cy - 11 * len(cats), 6)
    for i, c in enumerate(cats):
        g += f'<rect class="sec s{i % 6}" x="{lx}" y="{ly + 22 * i}" width="13" height="13" rx="3"/><text class="lg" x="{lx + 19}" y="{ly + 22 * i + 11}">{c}</text>'
    return f'<svg class="sgraf stat pie" viewBox="0 0 {W} {2 * R + 16}" role="img" aria-label="diagrama de sectors">{g}</svg>'
def picto(cats, vals, unit, icon='●', W=300):
    """pictograma: cada icona val unit (es dibuixen mitges icones si cal)"""
    rh = 30; g = ''
    for i, (c, v) in enumerate(zip(cats, vals)):
        y = 8 + rh * i
        g += f'<text class="lg" x="4" y="{y + 18}">{c}</text>'
        q = Fraction(v, unit); k = 0
        while q > 0:
            part = min(q, 1)
            x = 92 + 26 * k
            if part == 1: g += f'<text class="pic" x="{x}" y="{y + 20}">{icon}</text>'
            else: g += f'<svg x="{x}" y="{y}" width="{float(part) * 22:.1f}" height="28" overflow="hidden"><text class="pic" x="0" y="20">{icon}</text></svg>'
            q -= part; k += 1
    return f'<svg class="sgraf stat picto" viewBox="0 0 {W} {rh * len(cats) + 12}" role="img" aria-label="pictograma">{g}</svg>'
def num(v):
    v = fr(v)
    t = str(v.numerator) if v.denominator == 1 else ('%g' % float(v))
    return t.replace('-', '−').replace('.', ',')
def dots(data, lo, hi, W=300, mean_=None, med=None, dev=False, step=1, lab=''):
    """diagrama de punts: cada dada és un punt apilat sobre el seu valor; mean_: triangle (punt d'equilibri); med: marca de la mediana;
    dev: dibuixa la distància de cada dada a la mitjana"""
    L0, R0 = 16, 16; w = W - L0 - R0
    X = lambda v: L0 + w * (float(v) - lo) / (hi - lo)
    cnt = {}; pts = []
    for d in data:
        cnt[d] = cnt.get(d, 0) + 1; pts.append((d, cnt[d]))
    top = max(cnt.values()); H = 46 + 15 * top + (12 * len(data) if dev else 0)
    base = H - 32
    g = f'<line class="ax" x1="{L0 - 6}" y1="{base}" x2="{W - R0 + 6}" y2="{base}"/>'
    v = lo
    while v <= hi + 1e-9:
        g += f'<line class="ax" x1="{X(v):.1f}" y1="{base - 3}" x2="{X(v):.1f}" y2="{base + 3}"/><text class="tk" x="{X(v):.1f}" y="{base + 15}" text-anchor="middle">{num(Fraction(v).limit_denominator(100))}</text>'
        v += step
    for d, k in pts:
        g += f'<circle class="ddot" cx="{X(d):.1f}" cy="{base - 9 - 15 * (k - 1)}" r="6"/>'
    if dev and mean_ is not None:
        y = base - 15 * top - 12
        for j, d in enumerate(sorted(data)):
            yy = y - 12 * j
            g += f'<line class="dev" x1="{X(mean_):.1f}" y1="{yy}" x2="{X(d):.1f}" y2="{yy}"/><circle class="ddot sm" cx="{X(d):.1f}" cy="{yy}" r="3"/>'
    if med is not None:
        g += f'<line class="medl" x1="{X(med):.1f}" y1="{8}" x2="{X(med):.1f}" y2="{base}"/>'
    if mean_ is not None:
        g += f'<path class="fulc" d="M{X(mean_):.1f} {base + 2}l-8 13h16z"/>'
    if lab: g += f'<text class="tk ax-t" x="{W - R0}" y="{H - 2}" text-anchor="end">{lab}</text>'
    return f'<svg class="sgraf stat dots" viewBox="0 0 {W} {H}" role="img" aria-label="diagrama de punts">{g}</svg>'
def fig(s, cap=None): return f'<figure>{s}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{s}</figure>'
def figs(*f): return '<div class="figs">' + ''.join(f) + '</div>'
