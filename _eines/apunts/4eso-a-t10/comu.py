# Funcions comunes dels apunts de la Unitat 10 de 4t ESO Matemàtiques A (Estadística bidimensional). Parteixen del comu.py de la
# unitat 9 (HTML trilingüe, ginys, comprovacions ck()/ckr() i estadística exacta amb Fraction); al final hi ha les funcions
# bidimensionals (bi, rl) i els núvols de punts en SVG (nuvol, nuvolR; app.js en té una còpia: cloud()).
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

def ckr(v, w, d=2):
    """v: valor (pot ser irracional); w: el valor arrodonit a d decimals que escrivim"""
    NCK[0] += 1
    assert abs(float(v) - float(fr(w))) <= 0.5 * 10 ** -d + 1e-9, (float(v), w)
    return v

# ---------- nombres ----------
def tn(v):
    r"""nombre en TeX amb coma decimal (\dc: en anglés es veu un punt); ha de ser exacte"""
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
def var(data):
    """variància (poblacional): mitjana dels quadrats de les desviacions"""
    m = mean(data); return Fraction(sum((fr(x) - m) ** 2 for x in data), len(data))
def sd(data): return math.sqrt(var(data))
def cv(data): return sd(data) / float(mean(data))
def pctl(data, k):
    """percentil k (k en %): posició k·N/100; si és entera, mitjana d'eixa dada i la següent; si no, la dada de la posició
    següent (el mateix criteri que la mediana; Q1 = pctl(25), Q3 = pctl(75))"""
    d = sorted(fr(x) for x in data); n = len(d); pos = Fraction(k * n, 100)
    if pos.denominator == 1:
        p = int(pos); return (d[p - 1] + d[p]) / 2 if p < n else d[-1]
    return d[math.ceil(pos) - 1]
def five(data):
    d = sorted(fr(x) for x in data); return (d[0], pctl(data, 25), pctl(data, 50), pctl(data, 75), d[-1])
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

def caixes(rows, lo, hi, step=1, W=300, lab=''):
    """diagrama de caixes: rows = [(etiqueta, (mín, Q1, Me, Q3, màx))]; app.js en té una còpia (caixes())"""
    L0 = 26 if any(r[0] for r in rows) else 14; R0 = 14; w = W - L0 - R0; rh = 44
    X = lambda v: L0 + w * (float(v) - lo) / (hi - lo)
    H = rh * len(rows) + 34; base = H - 26; g = ''
    v = lo
    while v <= hi + 1e-9:
        g += f'<line class="grid" x1="{X(v):.1f}" y1="6" x2="{X(v):.1f}" y2="{base}"/><text class="tk" x="{X(v):.1f}" y="{base + 15}" text-anchor="middle">{num(Fraction(v).limit_denominator(100))}</text>'
        v += step
    g += f'<line class="ax" x1="{L0 - 4}" y1="{base}" x2="{W - R0 + 4}" y2="{base}"/>'
    for j, (t, (a, q1, me, q3, b)) in enumerate(rows):
        y = 10 + rh * j + 14
        g += (f'<line class="whis" x1="{X(a):.1f}" y1="{y}" x2="{X(q1):.1f}" y2="{y}"/><line class="whis" x1="{X(q3):.1f}" y1="{y}" x2="{X(b):.1f}" y2="{y}"/>'
              f'<line class="whis" x1="{X(a):.1f}" y1="{y - 7}" x2="{X(a):.1f}" y2="{y + 7}"/><line class="whis" x1="{X(b):.1f}" y1="{y - 7}" x2="{X(b):.1f}" y2="{y + 7}"/>'
              f'<rect class="bx b{j % 4}" x="{X(q1):.1f}" y="{y - 12}" width="{X(q3) - X(q1):.1f}" height="24" rx="2"/>'
              f'<line class="bmed" x1="{X(me):.1f}" y1="{y - 12}" x2="{X(me):.1f}" y2="{y + 12}"/>')
        if t: g += f'<text class="lg" x="4" y="{y + 4}">{t}</text>'
    if lab: g += f'<text class="tk ax-t" x="{W - R0}" y="{H - 1}" text-anchor="end">{lab}</text>'
    return f'<svg class="sgraf stat boxp" viewBox="0 0 {W} {H}" role="img" aria-label="diagrama de caixes">{g}</svg>'

# ---------- estadística bidimensional (exacta) ----------
def bi(xs, ys):
    """paràmetres d'una distribució bidimensional (fraccions exactes; sdx, sdy i r, decimals)"""
    assert len(xs) == len(ys)
    N = len(xs); X = [fr(x) for x in xs]; Y = [fr(y) for y in ys]
    S = dict(N=N, sx=sum(X), sy=sum(Y), sx2=sum(x * x for x in X), sy2=sum(y * y for y in Y), sxy=sum(x * y for x, y in zip(X, Y)))
    S['mx'] = S['sx'] / N; S['my'] = S['sy'] / N
    S['vx'] = S['sx2'] / N - S['mx'] ** 2; S['vy'] = S['sy2'] / N - S['my'] ** 2
    S['c'] = S['sxy'] / N - S['mx'] * S['my']
    S['sdx'] = math.sqrt(S['vx']); S['sdy'] = math.sqrt(S['vy'])
    S['r'] = float(S['c']) / (S['sdx'] * S['sdy']) if S['vx'] and S['vy'] else float('nan')
    return S
def rl(S):
    """recta de regressió de Y sobre X: y = m·x + n (fraccions exactes)"""
    m = S['c'] / S['vx']; return m, S['my'] - m * S['mx']

# ---------- núvols de punts (SVG); app.js en té una còpia (cloud) ----------
def _nstep(lo, hi):
    span = hi - lo; st = 10 ** math.floor(math.log10(span / 5))
    for k in (1, 2, 5, 10):
        if span / (st * k) <= 6: return st * k
    return st * 10
def nuvol(pts, xr, yr, axes=('X', 'Y'), means=False, reg=False, line=None, mark=None, hl=None, W=340, H=250, rad=4.5, est=None):
    """núvol de punts: xr, yr = (mín, màx, pas); means: rectes de les mitjanes i centre de gravetat; reg: recta de regressió;
    line: una altra recta (m, n); mark: punt estimat (x, y); hl: índex del punt destacat; est: (x0, y0) amb línies de lectura"""
    ML, MR, MT, MB = 40, 14, 14, 32
    (x0, x1, xs), (y0, y1, ys) = xr, yr
    X = lambda v: ML + (float(v) - x0) / (x1 - x0) * (W - ML - MR)
    Y = lambda v: H - MB - (float(v) - y0) / (y1 - y0) * (H - MT - MB)
    g = ''
    v = x0
    while v <= x1 + 1e-9:
        g += f'<line class="grid" x1="{X(v):.1f}" y1="{MT}" x2="{X(v):.1f}" y2="{H - MB}"/><text class="tk" x="{X(v):.1f}" y="{H - MB + 15}" text-anchor="middle">{num(Fraction(v).limit_denominator(1000))}</text>'
        v += xs
    v = y0
    while v <= y1 + 1e-9:
        g += f'<line class="grid" x1="{ML}" y1="{Y(v):.1f}" x2="{W - MR}" y2="{Y(v):.1f}"/><text class="tk" x="{ML - 5}" y="{Y(v) + 4:.1f}" text-anchor="end">{num(Fraction(v).limit_denominator(1000))}</text>'
        v += ys
    g += f'<line class="ax" x1="{ML}" y1="{H - MB}" x2="{W - MR}" y2="{H - MB}"/><line class="ax" x1="{ML}" y1="{MT}" x2="{ML}" y2="{H - MB}"/>'
    if axes:
        g += f'<text class="tk ax-t" x="{W - MR}" y="{H - MB - 6}" text-anchor="end">{axes[0]}</text><text class="tk ax-t" x="{ML + 6}" y="{MT + 11}">{axes[1]}</text>'
    S = bi([p[0] for p in pts], [p[1] for p in pts]) if len(pts) > 1 else None
    def seg(m, n, cls):
        m, n = float(m), float(n); a, b = x0, x1
        if m:
            c1, c2 = (y0 - n) / m, (y1 - n) / m; a = max(a, min(c1, c2)); b = min(b, max(c1, c2))
        return f'<line class="{cls}" x1="{X(a):.1f}" y1="{Y(m * a + n):.1f}" x2="{X(b):.1f}" y2="{Y(m * b + n):.1f}"/>' if b > a else ''
    if means and S:
        g += f'<line class="meanl" x1="{X(S["mx"]):.1f}" y1="{MT}" x2="{X(S["mx"]):.1f}" y2="{H - MB}"/><line class="meanl" x1="{ML}" y1="{Y(S["my"]):.1f}" x2="{W - MR}" y2="{Y(S["my"]):.1f}"/>'
    if line: g += seg(line[0], line[1], 'eyel')
    if reg and S and S['vx']:
        m, n = rl(S); g += seg(m, n, 'regl')
    if est:
        ex, ey = est
        g += f'<line class="estl" x1="{X(ex):.1f}" y1="{H - MB}" x2="{X(ex):.1f}" y2="{Y(ey):.1f}"/><line class="estl" x1="{X(ex):.1f}" y1="{Y(ey):.1f}" x2="{ML}" y2="{Y(ey):.1f}"/>'
        mark = est
    for i, (a, b) in enumerate(pts):
        g += f'<circle class="pt{" hl" if hl == i else ""}" cx="{X(a):.1f}" cy="{Y(b):.1f}" r="{rad}"/>'
    if means and S: g += f'<circle class="cg" cx="{X(S["mx"]):.1f}" cy="{Y(S["my"]):.1f}" r="5.5"/>'
    if mark: g += f'<circle class="est" cx="{X(mark[0]):.1f}" cy="{Y(mark[1]):.1f}" r="6"/>'
    return f'<svg class="sgraf nv" viewBox="0 0 {W} {H}" role="img" aria-label="núvol de punts">{g}</svg>'

import random
def nuvolR(n, r, seed, f=None):
    """n punts (escala 0-10) amb coeficient de correlació exactament r; f: si es dona, punts sobre una corba y = f(x) amb soroll"""
    rnd = random.Random(seed)
    if f:
        out = []
        for i in range(n):
            x = 0.3 + 9.4 * (i + rnd.random() * 0.8) / n; out.append((x, f(x) + r * (rnd.random() * 2 - 1)))
        return out
    z1 = [rnd.gauss(0, 1) for _ in range(n)]; z2 = [rnd.gauss(0, 1) for _ in range(n)]
    def st(a):
        m = sum(a) / n; s = math.sqrt(sum((v - m) ** 2 for v in a) / n); return [(v - m) / s for v in a]
    z1 = st(z1); dd = sum(a * b for a, b in zip(z1, z2)) / n; z2 = st([b - dd * a for a, b in zip(z1, z2)])
    return [(5 + 1.5 * a, 5 + 1.5 * (r * a + math.sqrt(max(0, 1 - r * r)) * b)) for a, b in zip(z1, z2)]
def nv0(pts, **k):
    """núvol petit sense eixos amb nom (figures de tipus de correlació)"""
    return nuvol([p for p in pts if 0 <= p[0] <= 10 and 0 <= p[1] <= 10], (0, 10, 2), (0, 10, 2), axes=None, W=220, H=180, rad=3.4, **k)
def btab(xs, ys, cols=('x2', 'y2', 'xy'), xl=None, yl=None):
    """taula de càlcul bidimensional: xi, yi i les columnes x², y², x·y, amb la fila de totals"""
    S = bi(xs, ys)
    H = {'x2': M('x_i^2'), 'y2': M('y_i^2'), 'xy': M(r'x_i\cdot y_i')}
    V = {'x2': lambda x, y: x * x, 'y2': lambda x, y: y * y, 'xy': lambda x, y: x * y}
    TT = {'x2': S['sx2'], 'y2': S['sy2'], 'xy': S['sxy']}
    rows = [[M(tn(x)), M(tn(y))] + [M(tn(V[c](fr(x), fr(y)))) for c in cols] for x, y in zip(xs, ys)]
    rows.append([M(r'\textstyle\sum=%s' % tn(S['sx'])), M(r'\textstyle\sum=%s' % tn(S['sy']))] + [M(r'\textstyle\sum=%s' % tn(TT[c])) for c in cols])
    return tbl([xl or M('x_i'), yl or M('y_i')] + [H[c] for c in cols], rows, 'c freq')
def ptab(xs, ys, xl, yl):
    """taula horitzontal de parelles (dues files)"""
    return ('<div class="tbl-wrap"><table class="data c freq ptab"><tbody><tr><th>' + xl + '</th>' + ''.join(f'<td>{M(tn(x))}</td>' for x in xs) + '</tr><tr><th>' + yl + '</th>'
            + ''.join(f'<td>{M(tn(y))}</td>' for y in ys) + '</tr></tbody></table></div>')
def sgn(v):
    """+ 3 / − 3 per a escriure rectes: 0,9x + 1,3"""
    v = fr(v); return ('+' if v >= 0 else '-') + tn(abs(v))
