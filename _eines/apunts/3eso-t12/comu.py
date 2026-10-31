# Funcions comunes dels apunts de la Unitat 12 (3r ESO, Probabilitat): HTML trilingüe, ginys, figures (arbres,
# taula de dos daus, bosses de boles en SVG) i comprovacions exactes de cada probabilitat amb fraccions (ck).
import math
from fractions import Fraction as Fr

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
    return (f'\n<!-- ======================= 12.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">12.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)

# ---------- ginys ----------
def drill(kind, va, es, en, mode='dec'):
    if mode == 'opts':
        row = f'<div class="wrow dopts"></div><div class="wrow"><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>'
    else:
        hint = (L("Escriu la probabilitat com a fracció (3/8) o com a decimal arrodonit a les centèsimes (0,38).",
                  "Escribe la probabilidad como fracción (3/8) o como decimal redondeado a las centésimas (0,38).",
                  "Type the probability as a fraction (3/8) or as a decimal rounded to 2 places (0.38).") if mode == 'dec'
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
def ck(v, w, d=None):
    """v: probabilitat calculada (Fraction); w: el que escrivim (Fraction, enter, o text amb coma); d: decimals (None = exacte)"""
    v = Fr(v)
    if isinstance(w, str): w = Fr(w.replace(',', '.'))
    if d is None: assert v == Fr(w), (v, w)
    else: assert abs(float(v) - float(w)) <= 0.5 * 10 ** -d + 1e-9, (v, float(v), w, d)
    return v
def fr(f):
    """fracció en TeX (irreductible)"""
    f = Fr(f)
    return str(f.numerator) if f.denominator == 1 else r'\frac{%d}{%d}' % (f.numerator, f.denominator)
def frs(n, d):
    """n/d en TeX i, si es pot, simplificada: \\frac{6}{36}=\\frac{1}{6}"""
    f = Fr(n, d)
    s = r'\frac{%d}{%d}' % (n, d)
    return s if (f.numerator, f.denominator) == (n, d) else s + '=' + fr(f)
def dc(x, d=2):
    """decimal amb coma TeX: 0{,}33"""
    s = ('%.' + str(d) + 'f') % float(x)
    return s.replace('.', '{,}')

# ---------- figures (SVG) ----------
def ptree(kids, W=330, rowh=34, colw=None, cap=None, leaf=True):
    """diagrama d'arbre. kids = [(etiqueta, probabilitat (text), fills, text final)], fills amb la mateixa forma.
    Les etiquetes poden dur una classe: 'R|ball-r' pinta una boleta roja amb el text R."""
    depth = [0]
    def dep(ks, d):
        depth[0] = max(depth[0], d)
        for k in ks: dep(k[2], d + 1)
    dep(kids, 1)
    D = depth[0]; cw = colw or (W - 120 if leaf else W - 30) / D
    out = []; txt = []
    # posició: fulles equiespaiades
    cnt = [0]
    def place(ks, d):
        pos = []
        for k in ks:
            if k[2]:
                cy = place(k[2], d + 1)
                y = sum(c[1] for c in cy) / len(cy)
                pos.append((k, y, d, cy))
            else:
                y = 16 + cnt[0] * rowh; cnt[0] += 1
                pos.append((k, y, d, []))
        return pos
    top = place(kids, 1)
    H = 16 + (cnt[0] - 1) * rowh + 16
    ry = sum(p[1] for p in top) / len(top)
    def X(d): return 14 + d * cw
    def draw(pos, px, py):
        for k, y, d, ch in pos:
            x = X(d)
            out.append(f'<line class="tl" x1="{px + 9:.1f}" y1="{py:.1f}" x2="{x - 12:.1f}" y2="{y:.1f}"/>')
            mx, my = (px + 9 + x - 12) / 2, (py + y) / 2
            if k[1]: txt.append(f'<text class="tp" x="{mx:.1f}" y="{my + (13 if y > py + 1 else -5):.1f}" text-anchor="middle">{k[1]}</text>')
            lab = k[0]; cls = ''
            if '|' in lab: lab, cls = lab.split('|')
            if cls: out.append(f'<circle class="ball {cls}" cx="{x:.1f}" cy="{y:.1f}" r="9"/>')
            txt.append(f'<text class="tn{" on" if cls else ""}" x="{x:.1f}" y="{y + 4.5:.1f}" text-anchor="middle">{lab}</text>')
            if ch: draw(ch, x, y)
            elif len(k) > 3 and k[3]:
                txt.append(f'<text class="te" x="{x + 18:.1f}" y="{y + 4.5:.1f}">{k[3]}</text>')
    out.append(f'<circle class="troot" cx="{X(0) - 4:.1f}" cy="{ry:.1f}" r="3.5"/>')
    draw(top, X(0) - 13, ry)
    svg = f'<svg class="ptree" viewBox="0 0 {W} {H}" style="max-width:{W}px" role="img" aria-label="diagrama d\'arbre">' + ''.join(out) + ''.join(txt) + '</svg>'
    return f'<figure>{svg}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{svg}</figure>'

def dgrid(op, hit, sym='+'):
    """taula de doble entrada dels dos daus: op(a, b) a cada casella; hit(a, b) -> casella marcada"""
    h = f'<th class="corner">{sym}</th>' + ''.join(f'<th>{b}</th>' for b in range(1, 7))
    rows = ''
    for a in range(1, 7):
        rows += f'<tr><th>{a}</th>' + ''.join(('<td class="hit">' if hit(a, b) else '<td>') + f'{op(a, b)}</td>' for b in range(1, 7)) + '</tr>'
    return f'<div class="tbl-wrap"><table class="dgrid"><thead><tr>{h}</tr></thead><tbody>{rows}</tbody></table></div>'

BALLC = {'R': 'ball-r', 'B': 'ball-b', 'V': 'ball-g', 'G': 'ball-y', 'N': 'ball-k'}
def bag(spec, cap=None, per=5):
    """bossa amb boles: spec = 'RRRBB' (R roja, B blava, V verda, G groga, N negra)"""
    n = len(spec); cols = min(per, n); rows = (n + cols - 1) // cols
    W = 30 + cols * 26; H = 34 + rows * 26
    out = [f'<path class="bagp" d="M8 18 Q8 {H - 4} {W / 2:.0f} {H - 4} Q{W - 8} {H - 4} {W - 8} 18 Z"/>',
           f'<path class="bagt" d="M4 18 H{W - 4}"/>']
    for i, c in enumerate(spec):
        r, k = divmod(i, cols)
        cx = W / 2 + (k - (cols - 1) / 2) * 26; cy = 34 + r * 26
        out.append(f'<circle class="ball {BALLC[c]}" cx="{cx:.1f}" cy="{cy:.1f}" r="10"/>')
    svg = f'<svg class="bag" viewBox="0 0 {W} {H}" style="max-width:{W}px" role="img" aria-label="bossa">' + ''.join(out) + '</svg>'
    return f'<figure>{svg}<figcaption>{cap}</figcaption></figure>' if cap else f'<figure>{svg}</figure>'

def chips(E, A=(), B=(), cls=''):
    """elements d'un espai mostral com a fitxes; els d'A i de B es marquen"""
    o = ''
    for e in E:
        c = 'el' + (' a' if e in A else '') + (' b' if e in B else '')
        o += f'<span class="{c}">{e}</span>'
    return f'<div class="chips-e {cls}">{o}</div>'
def figs(*f, three=False): return '<div class="figs%s">' % (' three' if three else '') + ''.join(f) + '</div>'
