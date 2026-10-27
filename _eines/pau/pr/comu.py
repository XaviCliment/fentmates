# Eines comunes per a escriure les solucions de les pàgines PAU de probabilitat (unitats 9 i 10).
# Les solucions són HTML amb fórmules KaTeX entre $...$ o $$...$$, com a ../sol.txt.
# Per evitar els conflictes de les claus de LaTeX amb el format de Python, els valors s'insereixen amb L():
#   L("$P(A)=@a$", a=N(x))  substitueix @a pel text donat.
from fractions import Fraction as F
import math

def p10(d):
    while d % 2 == 0: d //= 2
    while d % 5 == 0: d //= 5
    return d == 1
def dec(x, k=4):
    s = ('%.*f' % (k, float(x))).rstrip('0').rstrip('.')
    return s.replace('.', '{,}')
def N(x, k=4):
    """valor: decimal exacte, o fracció i valor aproximat"""
    x = F(x)
    if p10(x.denominator) and x.denominator <= 10**6: return dec(x, 6)
    return r'\dfrac{%d}{%d}\approx %s' % (x.numerator, x.denominator, dec(x, k))
def Q(x):
    """només la fracció (o el decimal exacte)"""
    x = F(x)
    if p10(x.denominator) and x.denominator <= 10**6: return dec(x, 6)
    return r'\dfrac{%d}{%d}' % (x.numerator, x.denominator)
def pc(x): return dec(F(x) * 100, 2) + r'\,\%'
def L(s, **k):
    for key in sorted(k, key=len, reverse=True): s = s.replace('@' + key, str(k[key]))
    assert '@' not in s, s
    return s
def st(t, b=''): return '<strong>%s</strong> %s' % (t, b)
def SOL(items, res):
    items = [('<strong>Diagrama d’arbre.</strong>' + i) if i.startswith('<svg') else i for i in items]
    return '<ol class="steps">' + ''.join('<li>%s</li>' % i for i in items) + '</ol><p class="res"><strong>Solució:</strong> ' + res + '</p>'

CHK = []
def ck(x, y, tol=None):
    """comprova un resultat amb el valor esperat (calculat a mà o de la solució oficial)"""
    if tol is None: assert F(x) == F(y), (x, y)
    else: assert abs(float(x) - float(y)) < tol, (x, y)
    CHK.append(1)
    return x

def taula(rl, cl, M, fmt=Q):
    """taula de contingència HTML; M inclou la fila i la columna de totals"""
    h = '<div class="tbl"><table><tr><th></th>' + ''.join('<th>$%s$</th>' % c for c in cl) + '<th>Total</th></tr>'
    for i, r in enumerate(rl + ['Total']):
        h += '<tr><th>%s</th>' % ('$%s$' % r if i < len(rl) else r) + ''.join('<td>$%s$</td>' % fmt(v) for v in M[i]) + '</tr>'
    return h + '</table></div>'
def ct(a, b, ab, la='A', lb='B', fmt=Q, tot=1):
    a, b, ab, tot = F(a), F(b), F(ab), F(tot)
    M = [[ab, a - ab, a], [b - ab, tot - a - b + ab, tot - a], [b, tot - b, tot]]
    assert all(v >= 0 for r in M for v in r), M
    return taula([la, r'\overline{%s}' % la], [lb, r'\overline{%s}' % lb], M, fmt)

def arbre(br, w=420):
    """diagrama d'arbre en SVG: br = [(etiqueta, prob, [(etiqueta, prob, destacada), ...]), ...]
    Les probabilitats poden ser Fraction o text. Les fulles mostren el producte del camí."""
    leaves = sum(len(k) for _, _, k in br) or len(br)
    step = 36; H = leaves * step + 16; x0, x1, x2 = 14, 140, 300
    o = ['<svg viewBox="0 0 %d %d" style="width:100%%;max-width:%dpx;display:block;margin:8px auto;font:13px Inter,sans-serif" role="img" aria-label="Diagrama d\'arbre">' % (w, H, w)]
    def lab(p): return p if isinstance(p, str) else (str(p.numerator) + '/' + str(p.denominator) if not p10(p.denominator) else dec(p).replace('{,}', ','))
    y = 8 + step / 2; ys = []
    for name, p, kids in br:
        ky = []
        for kn, kp, hl in kids:
            ky.append((kn, kp, hl, y)); y += step
        if not kids: ky = []; y += step
        cy = (ky[0][3] + ky[-1][3]) / 2 if ky else y - step
        ys.append((name, p, cy, ky))
    ry = (ys[0][2] + ys[-1][2]) / 2
    for name, p, cy, ky in ys:
        o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="currentColor" stroke-opacity=".45" stroke-width="1.5"/>' % (x0 + 4, ry, x1 - 14, cy))
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle" fill="currentColor" opacity=".8" style="font-size:12px">%s</text>' % ((x0 + x1) / 2 - 6, (ry + cy) / 2 - 5, lab(p)))
        o.append('<text x="%d" y="%.1f" text-anchor="middle" fill="currentColor" style="font-weight:700">%s</text>' % (x1, cy + 4, name))
        for j, (kn, kp, hl, yy) in enumerate(ky):
            dy = -6 if 2 * j + 1 < len(ky) else (14 if 2 * j + 1 > len(ky) else -6)
            col = 'var(--c)' if hl else 'currentColor'
            o.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-opacity="%s" stroke-width="%s"/>' % (x1 + 14 + 4 * len(name), cy, x2 - 12, yy, col, '1' if hl else '.45', '2.4' if hl else '1.5'))
            o.append('<text x="%.1f" y="%.1f" text-anchor="middle" fill="currentColor" opacity=".8" style="font-size:12px">%s</text>' % ((x1 + x2) / 2 + 14, (cy + yy) / 2 + dy, lab(kp)))
            o.append('<text x="%d" y="%.1f" fill="currentColor" style="font-weight:700">%s</text>' % (x2 - 6, yy + 4, kn))
            if not isinstance(p, str) and not isinstance(kp, str):
                o.append('<text x="%d" y="%.1f" fill="%s" style="font-size:12px">%s</text>' % (x2 + 22 + 7 * len(kn), yy + 4, col, '→ ' + lab(F(p) * F(kp))))
    o.append('<circle cx="%d" cy="%.1f" r="4" fill="currentColor"/>' % (x0, ry))
    o.append('</svg>')
    return ''.join(o)
def bayes(causes, ev='B', nev=None, hl=True):
    """arbre de probabilitat total: causes = [(nom, P(causa), P(ev|causa))]"""
    nev = nev or r'B̄'
    return arbre([(c, F(p), [(ev, F(q), hl), (nev, 1 - F(q), False)]) for c, p, q in causes])

# taula de la normal N(0,1) amb quatre decimals, com la que es dona a la PAU
def Phi(z): return round(0.5 * (1 + math.erf(z / math.sqrt(2))), 4)
