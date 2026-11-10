# Figures SVG dels enunciats (substitueixen @@FIGn@@ a an.txt). Colors amb currentColor i var(--c).
import math

def svg(w, h, body, maxw=None):
    return ('<figure style="margin:10px auto;text-align:center"><svg viewBox="0 0 %d %d" style="width:100%%;max-width:%dpx;'
            'font:13px Inter,sans-serif" role="img" aria-label="Figura de l\'enunciat">%s</svg></figure>' % (w, h, maxw or w, body))

L_ = '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="currentColor" stroke-width="%s"%s/>'
T_ = '<text x="%.1f" y="%.1f" fill="currentColor" text-anchor="middle"%s>%s</text>'

def ln_(x1, y1, x2, y2, w=2.2, dash=False, op=1):
    return L_ % (x1, y1, x2, y2, w, (' stroke-dasharray="5 4"' if dash else '') + ('' if op == 1 else ' stroke-opacity="%s"' % op))

def tx(x, y, s, it=True):
    return T_ % (x, y, ' font-style="italic"' if it else '', s)

FIG = {}

# 102: espill quadrat de 80 cm amb el cantó inferior esquerre trencat (catets 32 i 40)
k = 3; ox, oy = 40, 270   # (0,0) del dibuix
def P(x, y): return ox + k * x, oy - k * y
b = []
pts = [P(0, 40), P(32, 0), P(80, 0), P(80, 80), P(0, 80)]
b.append('<polygon points="%s" fill="none" stroke="currentColor" stroke-width="2.6"/>' % ' '.join('%.1f,%.1f' % p for p in pts))
b.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="currentColor" fill-opacity=".08" stroke="currentColor" stroke-opacity=".4" stroke-dasharray="4 3"/>' % (*P(0, 0), *P(32, 0), *P(0, 40)))
xr, yr = 12, 40 - 40 * 12 / 32
b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--c)" fill-opacity=".22" stroke="var(--c)" stroke-width="2.4"/>' % (P(xr, 80)[0], P(xr, 80)[1], k * (80 - xr), k * (80 - yr)))
b.append('<circle cx="%.1f" cy="%.1f" r="3.5" fill="var(--c)"/>' % P(xr, yr))
b.append(tx(P(xr, yr)[0] + 30, P(xr, yr)[1] + 18, '(x, y)'))
b.append(tx(P(46, 45)[0], P(46, 45)[1], 'R'))
b.append(ln_(*P(xr, 0), *P(xr, yr), 1.2, True, .6)); b.append(ln_(*P(0, yr), *P(xr, yr), 1.2, True, .6))
b.append(tx(P(xr / 2, 0)[0], oy + 16, 'x')); b.append(tx(ox - 12, P(0, yr / 2)[1] + 4, 'y'))
b.append(tx(P(16, 0)[0], oy + 34, '32', False)); b.append(ln_(*P(0, 0)[:1], oy + 22, P(32, 0)[0], oy + 22, 1, False, .6))
b.append(tx(ox - 26, P(0, 20)[1] + 4, '40', False)); b.append(ln_(ox - 18, P(0, 0)[1], ox - 18, P(0, 40)[1], 1, False, .6))
b.append(tx(P(40, 80)[0], P(40, 80)[1] - 8, '80', False))
FIG[102] = svg(320, 320, ''.join(b), 300)

# 104: camp de joc (rectangle x per y i dues semicircumferències de diàmetre y)
b = []; cx, cy, W, H = 170, 80, 150, 90
b.append('<path d="M %.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f" fill="none" stroke="currentColor" stroke-width="2.4"/>'
         % (cx - W / 2, cy - H / 2, H / 2, H / 2, cx - W / 2, cy + H / 2, cx + W / 2, cy - H / 2, H / 2, H / 2, cx + W / 2, cy + H / 2))
b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="currentColor" stroke-width="2.4"/>' % (cx - W / 2, cy - H / 2, W, H))
b.append(tx(cx, cy + H / 2 - 8, 'x')); b.append(tx(cx + W / 2 - 14, cy + 5, 'y'))
FIG[104] = svg(340, 160, ''.join(b), 320)

# 110: entrada parabòlica y = 12 - x^2 amb la porta rectangular
b = []; s = 26; ox, oy = 150, 345
def Q(x, y): return ox + s * x, oy - s * y
r12 = math.sqrt(12)
path = 'M ' + ' L '.join('%.1f %.1f' % Q(-r12 + 2 * r12 * i / 80, 12 - (-r12 + 2 * r12 * i / 80) ** 2) for i in range(81)) + ' Z'
b.append('<path d="%s" fill="currentColor" fill-opacity=".14" stroke="currentColor" stroke-width="2.4"/>' % path)
b.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="var(--surface)" stroke="var(--c)" stroke-width="2.4"/>' % (Q(-2, 8)[0], Q(-2, 8)[1], 4 * s, 8 * s))
b.append(ln_(ox - s * 4.3, oy, ox + s * 4.3, oy, 1.4))
b.append(tx(ox, oy - 4 * s, 'porta', False)); b.append(tx(ox + s * 2.9, oy - s * 6, 'pedra', False))
FIG[110] = svg(300, 360, ''.join(b), 220)

# 114: full de 16 x 10 amb quadrats de costat x als cantons
b = []; s = 18; ox, oy = 20, 20; xq = 2
b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="currentColor" fill-opacity=".06" stroke="currentColor" stroke-width="2.2"/>' % (ox, oy, 16 * s, 10 * s))
for (i, j) in ((0, 0), (16 - xq, 0), (0, 10 - xq), (16 - xq, 10 - xq)):
    b.append('<rect x="%d" y="%d" width="%d" height="%d" fill="var(--c)" fill-opacity=".25" stroke="var(--c)" stroke-width="1.6"/>' % (ox + i * s, oy + j * s, xq * s, xq * s))
for v in (xq, 16 - xq):
    b.append(ln_(ox + v * s, oy, ox + v * s, oy + 10 * s, 1.2, True, .6))
for v in (xq, 10 - xq):
    b.append(ln_(ox, oy + v * s, ox + 16 * s, oy + v * s, 1.2, True, .6))
b.append(tx(ox + xq * s / 2, oy + 10 * s - 6, 'x')); b.append(tx(ox + xq * s + 8, oy + (10 - xq / 2) * s + 4, 'x'))
b.append(tx(ox + 8 * s, oy + 10 * s + 18, '16 cm', False)); b.append(tx(ox + 16 * s + 22, oy + 5 * s + 4, '10', False))
FIG[114] = svg(340, 220, ''.join(b), 320)
