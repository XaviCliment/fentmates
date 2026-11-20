"""Programació lineal exacta (Fraction) + figures SVG per a les pàgines del Global de PL.

Una restricció és una tupla (a, b, op, c):  a·x + b·y  op  c,  op ∈ {"<=", ">="}.
Un problema (dict) té:
  cons   llista de restriccions
  names  noms dels vèrtexs en l'ordre que volem (es comprova que coincideixen)
  verts  vèrtexs esperats [(x, y), ...] (Fraction o int) — CHK
  view   (xmin, xmax, ymin, ymax) per a la figura
  obj    {"f": (a, b, c)}  ->  f(x, y) = a·x + b·y + c
"""
from fractions import Fraction as F
from itertools import combinations

CHECKS = [0]


def ck(cond, msg):
    if not cond:
        raise SystemExit("CHK falla: " + msg)
    CHECKS[0] += 1


def fr(v):
    return v if isinstance(v, F) else F(v).limit_denominator(1000)


def ok(cons, p):
    x, y = p
    for a, b, op, c in cons:
        v = fr(a) * x + fr(b) * y
        if op == "<=" and v > fr(c):
            return False
        if op == ">=" and v < fr(c):
            return False
    return True


def meet(r, s):
    a1, b1, _, c1 = r
    a2, b2, _, c2 = s
    a1, b1, c1, a2, b2, c2 = map(fr, (a1, b1, c1, a2, b2, c2))
    d = a1 * b2 - a2 * b1
    if d == 0:
        return None
    return ((c1 * b2 - c2 * b1) / d, (a1 * c2 - a2 * c1) / d)


def vertices(cons):
    """Vèrtexs de la regió factible, en ordre antihorari, amb les rectes que s'hi tallen."""
    out = {}
    for i, j in combinations(range(len(cons)), 2):
        p = meet(cons[i], cons[j])
        if p is not None and ok(cons, p):
            out.setdefault(p, set()).update((i, j))
    pts = list(out)
    if not pts:
        return []
    cx = sum(p[0] for p in pts) / len(pts)
    cy = sum(p[1] for p in pts) / len(pts)
    import math
    pts.sort(key=lambda p: math.atan2(float(p[1] - cy), float(p[0] - cx)))
    return [(p, sorted(out[p])) for p in pts]


def ev(f, p):
    a, b, c = (list(f) + [0])[:3]
    return fr(a) * p[0] + fr(b) * p[1] + fr(c)


def check_problem(P, key):
    vs = [p for p, _ in vertices(P["cons"])]
    exp = [tuple(map(fr, v)) for v in P["verts"]]
    ck(sorted(vs) == sorted(exp), "%s: vèrtexs %s != %s" % (key, fmt_pts(vs), fmt_pts(exp)))
    ck(len(P["names"]) == len(exp), key + ": noms")


def opt(P, f, kind):
    """(valor, [vèrtexs on s'assoleix]) sobre els vèrtexs esperats."""
    vals = [(ev(f, tuple(map(fr, v))), n) for v, n in zip(P["verts"], P["names"])]
    best = (max if kind == "max" else min)(v for v, _ in vals)
    return best, [n for v, n in vals if v == best]


# ---------------- format ----------------
def num(v, tex=True):
    v = fr(v)
    if v.denominator == 1:
        s = str(v.numerator)
    elif tex:
        s = ("-" if v < 0 else "") + "\\frac{%d}{%d}" % (abs(v.numerator), v.denominator)
    else:
        s = "%d/%d" % (v.numerator, v.denominator)
    return s if tex else s.replace("-", "−")


def fmt_pts(ps):
    return ", ".join("(%s, %s)" % (num(x, False), num(y, False)) for x, y in ps)


def lin_tex(a, b, c=None, rhs=None, op="="):
    """Expressió a·x + b·y (+ c) [op rhs] en TeX."""
    terms = []
    for k, v in (("x", a), ("y", b)):
        v = fr(v)
        if v == 0:
            continue
        mag = "" if abs(v) == 1 else num(abs(v))
        terms.append(("-" if v < 0 else "+", mag + k))
    if c:
        c = fr(c)
        terms.append(("-" if c < 0 else "+", num(abs(c))))
    s = ""
    for i, (sg, t) in enumerate(terms):
        s += ("-" if sg == "-" else "") + t if i == 0 else sg + t
    if rhs is not None:
        s += {"=": "=", "<=": "\\le ", ">=": "\\ge "}[op] + num(rhs)
    return s


def con_tex(r, op=None):
    a, b, o, c = r
    return lin_tex(a, b, rhs=c, op=op or o)


# ---------------- HTML generat ----------------
def vtx_html(P):
    """Sistemes que donen cada vèrtex (fórmules, sense text)."""
    vs = vertices(P["cons"])
    byp = {p: ln for p, ln in vs}
    rows = []
    for n, v in zip(P["names"], P["verts"]):
        p = tuple(map(fr, v))
        ln = byp[p]
        i, j = ln[0], ln[1]
        sysx = "\\begin{cases}%s\\\\ %s\\end{cases}" % (con_tex(P["cons"][i], "="), con_tex(P["cons"][j], "="))
        rows.append("%s\\ \\Rightarrow\\ %s(%s,\\,%s)" % (sysx, n, num(p[0]), num(p[1])))
    return '<div class="vtx">' + "".join("<span>\\(\\displaystyle %s\\)</span>" % r for r in rows) + "</div>"


def tab_html(P, fname, fs, marks=None):
    """Taula «vèrtex → valor de f». fs = [(a,b,c), ...] admet diverses funcions."""
    if not isinstance(fs[0], (list, tuple)):
        fs = [fs]
        fname = [fname]
    marks = marks or {}
    head = "<th></th>" + "".join("<th>\\(%s(x,y)\\)</th>" % n if len(n) == 1 else "<th>\\(%s\\)</th>" % n for n in fname)
    body = ""
    for n, v in zip(P["names"], P["verts"]):
        p = tuple(map(fr, v))
        tds = ""
        for k, f in enumerate(fs):
            val = ev(f, p)
            cls = marks.get((n, k), "")
            tds += '<td%s>\\(%s\\)</td>' % (' class="%s"' % cls if cls else "", num(val))
        body += "<tr><th>\\(%s(%s,\\,%s)\\)</th>%s</tr>" % (n, num(p[0]), num(p[1]), tds)
    return '<div class="tbl-wrap"><table class="data vt"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (head, body)


# ---------------- figura SVG ----------------
def clip_poly(poly, a, b, op, c):
    """Sutherland–Hodgman amb un semiplà (floats)."""
    def inside(p):
        v = a * p[0] + b * p[1]
        return v <= c + 1e-9 if op == "<=" else v >= c - 1e-9
    out = []
    for i in range(len(poly)):
        P, Q = poly[i], poly[(i + 1) % len(poly)]
        ip, iq = inside(P), inside(Q)
        if ip:
            out.append(P)
        if ip != iq:
            d = a * (Q[0] - P[0]) + b * (Q[1] - P[1])
            t = (c - a * P[0] - b * P[1]) / d
            out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
    return out


def seg_in_box(a, b, c, box):
    x0, x1, y0, y1 = box
    pts = []
    if b != 0:
        for x in (x0, x1):
            y = (c - a * x) / b
            if y0 - 1e-9 <= y <= y1 + 1e-9:
                pts.append((x, y))
    if a != 0:
        for y in (y0, y1):
            x = (c - b * y) / a
            if x0 - 1e-9 <= x <= x1 + 1e-9:
                pts.append((x, y))
    uniq = []
    for p in pts:
        if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) > 1e-7 for q in uniq):
            uniq.append(p)
    return uniq[:2] if len(uniq) >= 2 else None


def nice_step(span):
    for s in (1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500):
        if span / s <= 14:
            return s
    return 1000


def svg(P, level=None, best=None, seg=None, show_lines=True, labels=True, extra_pts=(),
        W=440, region=True, line_names=True, hide_vertex_coords=False):
    """level = (a, b, k): recta de nivell a·x+b·y = k (discontínua).
    best = nom del vèrtex òptim (es ressalta); seg = (nom1, nom2) costat òptim."""
    x0, x1, y0, y1 = map(float, P["view"])
    H = W * (y1 - y0) / (x1 - x0)
    if H > 1.15 * W:   # escales diferents si cal (problemes amb enunciat)
        H = 1.0 * W
    if H < 0.55 * W:
        H = 0.62 * W
    pad = 26
    sx = (W - 2 * pad) / (x1 - x0)
    sy = (H - 2 * pad) / (y1 - y0)
    X = lambda x: pad + (x - x0) * sx
    Y = lambda y: H - pad - (y - y0) * sy
    o = ['<svg class="lpfig" viewBox="0 0 %.0f %.0f" role="img" aria-label="regió factible">' % (W, H)]
    # quadrícula
    stx, sty = nice_step(x1 - x0), nice_step(y1 - y0)
    import math
    gx = [k * stx for k in range(math.ceil(x0 / stx), math.floor(x1 / stx) + 1)]
    gy = [k * sty for k in range(math.ceil(y0 / sty), math.floor(y1 / sty) + 1)]
    for g in gx:
        o.append('<line class="g" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (X(g), Y(y0), X(g), Y(y1)))
    for g in gy:
        o.append('<line class="g" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (X(x0), Y(g), X(x1), Y(g)))
    # regió
    if region:
        poly = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        for a, b, op, c in P["cons"]:
            poly = clip_poly(poly, float(a), float(b), op, float(c))
        if poly:
            o.append('<polygon class="reg" points="%s"/>' % " ".join("%.1f,%.1f" % (X(p[0]), Y(p[1])) for p in poly))
    # eixos
    if x0 <= 0 <= x1:
        o.append('<line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (X(0), Y(y0), X(0), Y(y1)))
    if y0 <= 0 <= y1:
        o.append('<line class="ax" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (X(x0), Y(0), X(x1), Y(0)))
    for g in gx:
        if g != 0 and y0 <= 0 <= y1:
            o.append('<text class="tk" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (X(g), Y(0) + 13, num(g, False)))
    for g in gy:
        if g != 0 and x0 <= 0 <= x1:
            o.append('<text class="tk" x="%.1f" y="%.1f" text-anchor="end">%s</text>' % (X(0) - 4, Y(g) + 4, num(g, False)))
    o.append('<text class="tk" x="%.1f" y="%.1f">x</text>' % (X(x1) - 10, (Y(0) if y0 <= 0 <= y1 else Y(y0)) - 5))
    o.append('<text class="tk" x="%.1f" y="%.1f">y</text>' % ((X(0) if x0 <= 0 <= x1 else X(x0)) + 5, Y(y1) + 11))
    # rectes
    placed = []
    if show_lines:
        for k, (a, b, op, c) in enumerate(P["cons"]):
            if (a == 0 and c == 0) or (b == 0 and c == 0):
                continue    # eixos
            s = seg_in_box(float(a), float(b), float(c), (x0, x1, y0, y1))
            if not s:
                continue
            (ax_, ay_), (bx_, by_) = s
            o.append('<line class="ln l%d" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (k % 6, X(ax_), Y(ay_), X(bx_), Y(by_)))
            if line_names:
                txt = plain(a, b, c)
                wlab = 6.1 * len(txt)
                best_s, best_p = None, None
                for t in (0.88, 0.8, 0.72, 0.12, 0.2, 0.3, 0.62, 0.4, 0.5):
                    px, py = X(ax_ + t * (bx_ - ax_)), Y(ay_ + t * (by_ - ay_))
                    anc_end = px > W - wlab - 12
                    lx0 = px - wlab - 4 if anc_end else px + 4
                    cx_, cy_ = lx0 + wlab / 2, py - 9
                    if lx0 < 2 or lx0 + wlab > W - 2 or cy_ < 8 or cy_ > H - 6:
                        continue
                    sc = min([abs(cx_ - X(float(v[0]))) / (wlab / 2 + 18) + abs(cy_ - Y(float(v[1]))) / 20
                              for v in P["verts"]] + [9])
                    sc = min([sc] + [abs(cx_ - q[0]) / (wlab / 2 + q[2] / 2 + 4) + abs(cy_ - q[1]) / 14 for q in placed])
                    if y0 <= 0 <= y1 and abs(cy_ - Y(0)) < 16:
                        sc -= 0.6
                    if x0 <= 0 <= x1 and lx0 - 22 < X(0) < lx0 + wlab + 4:
                        sc -= 0.3
                    if best_s is None or sc > best_s + 1e-9:
                        best_s, best_p = sc, (px, py, anc_end, cx_, cy_)
                if best_p:
                    px, py, anc_end, cx_, cy_ = best_p
                    placed.append((cx_, cy_, wlab))
                    o.append('<text class="lt l%d" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (
                        k % 6, px + (-4 if anc_end else 4), py - 5, "end" if anc_end else "start", txt))
    for lev in ([] if not level else level if isinstance(level[0], (list, tuple)) else [level]):
        a, b, kk = map(float, lev)
        s = seg_in_box(a, b, kk, (x0, x1, y0, y1))
        if s:
            o.append('<line class="lv" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (X(s[0][0]), Y(s[0][1]), X(s[1][0]), Y(s[1][1])))
    # costat òptim
    if seg:
        d = dict(zip(P["names"], P["verts"]))
        p, q = d[seg[0]], d[seg[1]]
        o.append('<line class="opt" x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (X(float(p[0])), Y(float(p[1])), X(float(q[0])), Y(float(q[1]))))
    # vèrtexs
    if labels:
        vs = [(n, tuple(map(float, v))) for n, v in zip(P["names"], P["verts"])]
        cx = sum(v[0] for _, v in vs) / len(vs)
        cy = sum(v[1] for _, v in vs) / len(vs)
        for n, v in vs:
            if not (x0 <= v[0] <= x1 and y0 <= v[1] <= y1):
                continue
            dx, dy = X(v[0]) - X(cx), Y(v[1]) - Y(cy)
            r = max((dx * dx + dy * dy) ** .5, 1)
            tx, ty = X(v[0]) + 15 * dx / r, Y(v[1]) + 15 * dy / r + 4
            anc = "start" if dx > 8 else ("end" if dx < -8 else "middle")
            cls = "pt best" if (best and n in (best if isinstance(best, (list, tuple)) else [best])) else "pt"
            o.append('<circle class="%s" cx="%.1f" cy="%.1f" r="4.2"/>' % (cls, X(v[0]), Y(v[1])))
            lab = n if hide_vertex_coords else "%s(%s, %s)" % (n, num(fr(v[0]), False) if False else dec(dict(zip(P["names"], P["verts"]))[n][0]),
                                                           dec(dict(zip(P["names"], P["verts"]))[n][1]))
            wl = 6.6 * len(lab)
            left = tx - (wl if anc == "end" else wl / 2 if anc == "middle" else 0)
            if left < 3:
                tx, anc = X(v[0]) + 7, "start"
                ty = Y(v[1]) + (16 if dy >= 0 else -8)
            elif left + wl > W - 3:
                tx, anc = X(v[0]) - 7, "end"
                ty = Y(v[1]) + (16 if dy >= 0 else -8)
            ty = min(max(ty, 12), H - 4)
            o.append('<text class="vl" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (tx, ty, anc, lab))
    for (px, py, name, cls) in extra_pts:
        o.append('<circle class="%s" cx="%.1f" cy="%.1f" r="4"/>' % (cls, X(px), Y(py)))
        o.append('<text class="vl %s" x="%.1f" y="%.1f">%s</text>' % (cls, X(px) + 7, Y(py) - 6, name))
    o.append("</svg>")
    return '<figure class="lpf">' + "".join(o) + "</figure>"


def dec(v):
    v = fr(v)
    if v.denominator == 1:
        return str(v.numerator).replace("-", "−")
    if (v * 100).denominator == 1:
        return ("%g" % float(v)).replace(".", ",").replace("-", "−")
    return num(v, False)


def plain(a, b, c):
    """Equació de la recta en text pla (per a l'SVG)."""
    s = ""
    for k, v in (("x", a), ("y", b)):
        v = fr(v)
        if v == 0:
            continue
        m = "" if abs(v) == 1 else dec(abs(v))
        if s:
            s += (" − " if v < 0 else " + ") + m + k
        else:
            s += ("−" if v < 0 else "") + m + k
    return s + " = " + dec(c)
