# Funcions comunes dels apunts de la Unitat 7 de 1r ESO (Geometria bàsica del pla): HTML trilingüe, ginys,
# figures geomètriques (SVG, a partir del G() de 3eso-t9 amb rectes amb fletxes i marques de costats iguals)
# i comprovacions de cada resultat (ck, sexagesimal).
import math
import sympy as sp

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
    return (f'\n<!-- ======================= 7.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">7.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)

# ---------- ginys ----------
def drill(kind, va, es, en, mode='dec'):
    if mode == 'opts':
        row = f'<div class="wrow dopts"></div><div class="wrow"><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
    elif mode == 'sx':
        row = (f'<div class="wrow"><label>{L("Resposta", "Respuesta", "Answer")} <input class="tin m" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat" placeholder="…"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
               + '<p class="hint-s">' + L("Escriu l'angle en forma complexa amb els símbols ° ' '' o separant els nombres amb espais: 12° 30' 15'' o 12 30 15.",
                                         "Escribe el ángulo en forma compleja con los símbolos ° ' '' o separando los números con espacios: 12° 30' 15'' o 12 30 15.",
                                         "Type the angle in compound form using ° ' '' or with spaces between the numbers: 12° 30' 15'' or 12 30 15.") + '</p>')
    else:
        hint = (L("Escriu un nombre (pots fer servir decimals: 8,5 o 8.5).", "Escribe un número (puedes usar decimales: 8,5 u 8.5).", "Type a number (decimals are fine: 8.5 or 8,5).") if mode == 'dec'
                else L("Escriu el nombre exacte.", "Escribe el número exacto.", "Type the exact number."))
        row = (f'<div class="wrow"><label>{L("Resposta", "Respuesta", "Answer")} <input class="tin" type="text" inputmode="decimal" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat" placeholder="…"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
               + '<p class="hint-s">' + hint + '</p>')
    return f'''<div class="widget w-drill" data-kind="{kind}">
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
pi = sp.pi
S = sp.sqrt
R = sp.Rational
def ck(v, w, d=None):
    """v: valor calculat (sympy o nombre); w: el que escrivim als apunts. d: decimals de l'arrodoniment (None = exacte)"""
    w = float(str(w).replace(',', '.')) if isinstance(w, str) else w
    if d is None:
        assert sp.simplify(sp.nsimplify(v) - sp.nsimplify(w)) == 0, (v, w)
    else:
        assert abs(float(v) - float(w)) <= 0.5 * 10 ** -d + 1e-9, (v, float(v), w, d)
    return v

# ---------- figures geomètriques (SVG) ----------
# elements: ('poly', pts, cls) · ('seg', A, B, cls) · ('ra', V, A, B) angle recte · ('txt', P, text, opts)
# ('circ', C, r, cls) · ('sect', C, r, a0, a1, cls) · ('arc', C, r, a0, a1, cls) · ('lens', A, B, r, cls) · ('dot', P, cls)
# ('ln', A, B, cls, ends) segment amb fletxa a l'extrem B ('e') o als dos ('b': recta) · ('tick', A, B, n) n marques de costat igual
def G(items, W=240, pad=16, cap=None, maxh=None):
    xs, ys = [], []
    for it in items:
        k = it[0]
        if k == 'poly': xs += [p[0] for p in it[1]]; ys += [p[1] for p in it[1]]
        elif k in ('seg', 'ln'): xs += [it[1][0], it[2][0]]; ys += [it[1][1], it[2][1]]
        elif k == 'circ': C, r = it[1], it[2]; xs += [C[0] - r, C[0] + r]; ys += [C[1] - r, C[1] + r]
        elif k in ('sect', 'arc'):
            C, r, a0, a1 = it[1], it[2], it[3], it[4]
            for j in range(41):
                t = math.radians(a0 + (a1 - a0) * j / 40); xs.append(C[0] + r * math.cos(t)); ys.append(C[1] + r * math.sin(t))
            if k == 'sect': xs.append(C[0]); ys.append(C[1])
        elif k in ('dot', 'txt'): xs.append(it[1][0]); ys.append(it[1][1])
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = (W - 2 * pad) / max(x1 - x0, 1e-9)
    if maxh and (y1 - y0) * s + 2 * pad > maxh: s = (maxh - 2 * pad) / (y1 - y0)
    Wd = round((x1 - x0) * s + 2 * pad); H = round((y1 - y0) * s + 2 * pad)
    X = lambda v: round((float(v) - x0) * s + pad, 1)
    Y = lambda v: round(H - ((float(v) - y0) * s + pad), 1)
    out = ''
    def arcpath(C, r, a0, a1):
        a0r, a1r = math.radians(a0), math.radians(a1)
        Pa = (C[0] + r * math.cos(a0r), C[1] + r * math.sin(a0r)); Pb = (C[0] + r * math.cos(a1r), C[1] + r * math.sin(a1r))
        big = 1 if (a1 - a0) % 360 > 180 else 0
        return Pa, Pb, f'A{round(r * s, 1)} {round(r * s, 1)} 0 {big} 0 {X(Pb[0])} {Y(Pb[1])}'
    for it in items:
        k = it[0]
        if k == 'poly':
            out += f'<polygon class="gp {it[2] if len(it) > 2 else ""}" points="' + ' '.join(f'{X(p[0])},{Y(p[1])}' for p in it[1]) + '"/>'
        elif k == 'seg':
            out += f'<line class="gs {it[3] if len(it) > 3 else ""}" x1="{X(it[1][0])}" y1="{Y(it[1][1])}" x2="{X(it[2][0])}" y2="{Y(it[2][1])}"/>'
        elif k == 'ra':
            V, A, B = it[1], it[2], it[3]; k_ = 9 / s
            def u(Pp):
                dx, dy = Pp[0] - V[0], Pp[1] - V[1]; n = math.hypot(dx, dy); return dx / n * k_, dy / n * k_
            ua, ub = u(A), u(B)
            pts = [(V[0] + ua[0], V[1] + ua[1]), (V[0] + ua[0] + ub[0], V[1] + ua[1] + ub[1]), (V[0] + ub[0], V[1] + ub[1])]
            out += '<polyline class="gra" points="' + ' '.join(f'{X(p[0])},{Y(p[1])}' for p in pts) + '"/>'
        elif k == 'circ':
            out += f'<circle class="gp {it[3] if len(it) > 3 else ""}" cx="{X(it[1][0])}" cy="{Y(it[1][1])}" r="{round(it[2] * s, 1)}"/>'
        elif k == 'sect':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]; Pa, Pb, A_ = arcpath(C, r, a0, a1)
            out += f'<path class="gp {it[5] if len(it) > 5 else ""}" d="M{X(C[0])} {Y(C[1])}L{X(Pa[0])} {Y(Pa[1])}{A_}Z"/>'
        elif k == 'arc':
            C, r, a0, a1 = it[1], it[2], it[3], it[4]; Pa, Pb, A_ = arcpath(C, r, a0, a1)
            out += f'<path class="garc {it[5] if len(it) > 5 else ""}" d="M{X(Pa[0])} {Y(Pa[1])}{A_}"/>'
        elif k == 'lens':
            A, B, r = it[1], it[2], it[3]; rr = round(r * s, 1)
            out += f'<path class="gp {it[4] if len(it) > 4 else ""}" d="M{X(A[0])} {Y(A[1])}A{rr} {rr} 0 0 1 {X(B[0])} {Y(B[1])}A{rr} {rr} 0 0 1 {X(A[0])} {Y(A[1])}Z"/>'
        elif k == 'ln':
            A, B = it[1], it[2]; ends = it[4] if len(it) > 4 else 'b'
            out += f'<line class="gs {it[3] if len(it) > 3 else ""}" x1="{X(A[0])}" y1="{Y(A[1])}" x2="{X(B[0])}" y2="{Y(B[1])}"/>'
            for P0, P1 in ([(A, B), (B, A)] if ends == 'b' else [(A, B)] if ends == 'e' else []):
                ux, uy = X(P1[0]) - X(P0[0]), Y(P1[1]) - Y(P0[1]); n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
                tx, ty = X(P1[0]), Y(P1[1])
                out += f'<polygon class="gah {it[3] if len(it) > 3 else ""}" points="{round(tx, 1)},{round(ty, 1)} {round(tx - 9 * ux - 4 * uy, 1)},{round(ty - 9 * uy + 4 * ux, 1)} {round(tx - 9 * ux + 4 * uy, 1)},{round(ty - 9 * uy - 4 * ux, 1)}"/>'
        elif k == 'tick':
            A, B, nt = it[1], it[2], it[3]
            ux, uy = X(B[0]) - X(A[0]), Y(B[1]) - Y(A[1]); n = math.hypot(ux, uy); ux, uy = ux / n, uy / n
            mx, my = (X(A[0]) + X(B[0])) / 2, (Y(A[1]) + Y(B[1])) / 2
            for j in range(nt):
                o = (j - (nt - 1) / 2) * 4
                cx, cy = mx + o * ux, my + o * uy
                out += f'<line class="gtk" x1="{round(cx - 5 * uy, 1)}" y1="{round(cy + 5 * ux, 1)}" x2="{round(cx + 5 * uy, 1)}" y2="{round(cy - 5 * ux, 1)}"/>'
        elif k == 'dot':
            out += f'<circle class="gd {it[2] if len(it) > 2 else ""}" cx="{X(it[1][0])}" cy="{Y(it[1][1])}" r="3.5"/>'
    for it in items:
        if it[0] == 'txt':
            o = it[3] if len(it) > 3 else {}
            out += (f'<text class="gt {o.get("cls", "")}" x="{round(X(it[1][0]) + o.get("dx", 0), 1)}" y="{round(Y(it[1][1]) + o.get("dy", 4), 1)}" '
                    f'text-anchor="{o.get("a", "middle")}">{it[2]}</text>')
    svg = f'<svg class="gfig" viewBox="0 0 {Wd} {H}" style="max-width:{Wd}px" role="img" aria-label="figura">{out}</svg>'
    return f'<figure>{svg}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{svg}</figure>'
def figs(*f, three=False): return '<div class="figs%s">' % (' three' if three else '') + ''.join(f) + '</div>'
def mid(A, B, f=0.5): return (A[0] + (B[0] - A[0]) * f, A[1] + (B[1] - A[1]) * f)
def off(A, B, d):
    """punt mitjà del costat AB desplaçat d cap a l'esquerra (mirant d'A a B)"""
    M = mid(A, B); dx, dy = B[0] - A[0], B[1] - A[1]; n = math.hypot(dx, dy)
    return (M[0] - dy / n * d, M[1] + dx / n * d)
def pol(C, r, a): return (C[0] + r * math.cos(math.radians(a)), C[1] + r * math.sin(math.radians(a)))
def reg(n, r=1, rot=None):
    """vèrtexs d'un polígon regular de n costats (base horitzontal)"""
    rot = -90 - 180 / n if rot is None else rot
    return [pol((0, 0), r, rot + 360 * k / n) for k in range(n)]
def angfig(V, a0, a1, r=1.6, R=0.55, lab=None, cls='af', labr=None):
    """angle de vèrtex V entre les direccions a0 i a1 (graus, en sentit antihorari): costats amb fletxa i arc ple"""
    it = [('sect', V, R, a0, a1, cls), ('ln', V, pol(V, r, a0), '', 'e'), ('ln', V, pol(V, r, a1), '', 'e'), ('dot', V)]
    if lab: it.append(('txt', pol(V, labr or R + 0.32, (a0 + a1) / 2), lab, {'cls': 'hot'}))
    return it

# ---------- sistema sexagesimal (tot en segons) ----------
def sx(d, m=0, s=0): return d * 3600 + m * 60 + s
def dms(t):
    assert t >= 0 and t == int(t), t
    t = int(t); return t // 3600, t % 3600 // 60, t % 60
def ftex(t, zeros=False):
    """angle en forma complexa en TeX: 12°30'15''"""
    d, m, s = dms(t); out = []
    if d or (not m and not s) or zeros: out.append(r'%d^\circ' % d)
    if m or (zeros and s): out.append(r"%d'" % m)
    if s: out.append(r"%d''" % s)
    return r'\,'.join(out)
