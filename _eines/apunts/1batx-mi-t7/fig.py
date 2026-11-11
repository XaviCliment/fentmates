# Gràfiques de la Unitat 7 de 1r Batx MI (Estudi de funcions). Una mateixa definició (classe Plot) dibuixa la figura en SVG
# per als apunts interactius (build.py) i en TikZ per a la fitxa (_eines/fonts-latex/1batx-mi-t7/genera.py).
import math

SVGCOL = {"a": "var(--accent)", "b": "#3b82f6", "g": "#16a34a", "v": "#7c3aed", "o": "#f97316", "m": "var(--muted)", "t": "var(--text)"}
TIKZCOL = {"a": "accent", "b": "blue!70!black", "g": "green!55!black", "v": "violet", "o": "orange!85!black", "m": "muted", "t": "navy"}


def _f(x):
    s = "%.1f" % x
    return s[:-2] if s.endswith(".0") else s


def _t(x):
    s = "%.3f" % x
    return s.rstrip("0").rstrip(".")


def _rdp(pts, eps):
    """simplifica una poligonal (Ramer-Douglas-Peucker): lleva els punts que s'aparten menys de eps de la recta"""
    if len(pts) < 3: return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (x1, y1), (x2, y2) = pts[a], pts[b]
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1e-12
        best, bi = -1, -1
        for i in range(a + 1, b):
            d = abs(dy * (pts[i][0] - x1) - dx * (pts[i][1] - y1)) / L
            if d > best: best, bi = d, i
        if best > eps:
            keep[bi] = True
            stack += [(a, bi), (bi, b)]
    return [p for p, k in zip(pts, keep) if k]


class Plot:
    """Pla cartesià en [x0,x1]×[y0,y1]. ticks=False dibuixa només els eixos (per als esquemes)."""

    def __init__(self, x0, x1, y0, y1, sx=1, sy=1, ticks=True, grid=True, W=240, xlab=None, lx=None, ly=None):
        self.x0, self.x1, self.y0, self.y1, self.sx, self.sy = x0, x1, y0, y1, sx, sy
        self.ticks, self.grid, self.W, self.xlab = ticks, grid, W, xlab
        self.lx = lx or sx   # cada quant s'escriu el número dels eixos
        self.ly = ly or sy
        self.items = []

    # ---- elements ----
    def fn(self, f, a=None, b=None, col="a", dash=False, n=500, w=None):
        a = self.x0 if a is None else a
        b = self.x1 if b is None else b
        pts = [(a + (b - a) * i / n,) for i in range(n + 1)]
        return self._add_curve([(p[0], self._ev(f, p[0])) for p in pts], col, dash, w)

    def param(self, fx, fy, t0, t1, col="a", dash=False, n=500):
        return self._add_curve([(fx(t0 + (t1 - t0) * i / n), fy(t0 + (t1 - t0) * i / n)) for i in range(n + 1)], col, dash, None)

    @staticmethod
    def _ev(f, x):
        try:
            y = f(x)
        except (ValueError, ZeroDivisionError, OverflowError, TypeError):  # TypeError: operació amb None (fora del domini)
            return None
        return y if isinstance(y, (int, float)) and math.isfinite(y) else None

    def _add_curve(self, pts, col, dash, w):
        M = self.y1 - self.y0
        paths, cur, py = [], [], None
        for x, y in pts:
            if y is None or abs(y) > 1e6:
                if cur: paths.append(cur)
                cur, py = [], None
                continue
            if py is not None and abs(y - py) > M * 1.5:
                if cur: paths.append(cur)
                cur = []
            py = y
            cur.append((x, max(self.y0 - M, min(self.y1 + M, y))))
        if cur: paths.append(cur)
        self.items.append(("curve", paths, col, dash, w))
        return self

    def seg(self, x1, y1, x2, y2, col="a", dash=False):
        self.items.append(("curve", [[(x1, y1), (x2, y2)]], col, dash, None))
        return self

    def dot(self, x, y, col="a", open=False):
        self.items.append(("dot", x, y, col, open))
        return self

    def vl(self, x):  # recta vertical discontínua (asímptota, canvi de tros)
        self.items.append(("gd", x, self.y0, x, self.y1))
        return self

    def hl(self, y):
        self.items.append(("gd", self.x0, y, self.x1, y))
        return self

    def gd(self, x1, y1, x2, y2):
        self.items.append(("gd", x1, y1, x2, y2))
        return self

    def text(self, x, y, s, col="t", tex=None):
        self.items.append(("text", x, y, s, col, tex))
        return self

    def xbar(self, a, b, col="b"):  # segment gruixut sobre l'eix X (domini)
        self.items.append(("bar", a, 0, b, 0, col))
        return self

    def ybar(self, a, b, col="o"):  # segment gruixut sobre l'eix Y (recorregut)
        self.items.append(("bar", 0, a, 0, b, col))
        return self

    def _tick_range(self, a, b, s):
        v = math.ceil(a / s - 1e-9) * s
        while v <= b + 1e-9:
            yield round(v, 6)
            v += s

    @staticmethod
    def _lab(v):
        s = ("%g" % v).replace("-", "−")
        return s

    # ---- SVG ----
    def svg(self, label=""):
        ux = (self.x1 - self.x0)
        uy = (self.y1 - self.y0)
        pl, pr, pt, pb = (24, 8, 8, 18) if self.ticks else (8, 8, 8, 8)
        W = self.W
        H = round(W * min(1.15, max(.62, uy / ux)))

        def X(x): return pl + (x - self.x0) / ux * (W - pl - pr)

        def Y(y): return H - pb - (y - self.y0) / uy * (H - pt - pb)
        o = ['<svg class="tg-svg" viewBox="0 0 %d %d" role="img" aria-label="%s">' % (W, H, label or "Gràfica")]
        if self.grid and self.ticks:
            for v in self._tick_range(self.x0, self.x1, self.sx):
                o.append('<line class="g" x1="%s" x2="%s" y1="%s" y2="%s"/>' % (_f(X(v)), _f(X(v)), _f(Y(self.y0)), _f(Y(self.y1))))
            for v in self._tick_range(self.y0, self.y1, self.sy):
                o.append('<line class="g" x1="%s" x2="%s" y1="%s" y2="%s"/>' % (_f(X(self.x0)), _f(X(self.x1)), _f(Y(v)), _f(Y(v))))
        ay = max(self.y0, min(self.y1, 0))
        ax = max(self.x0, min(self.x1, 0))
        o.append('<line class="ax" x1="%s" x2="%s" y1="%s" y2="%s"/>' % (_f(X(self.x0)), _f(X(self.x1)), _f(Y(ay)), _f(Y(ay))))
        o.append('<line class="ax" x1="%s" x2="%s" y1="%s" y2="%s"/>' % (_f(X(ax)), _f(X(ax)), _f(Y(self.y0)), _f(Y(self.y1))))
        if self.ticks:
            if self.xlab:
                for v, s in self.xlab:
                    o.append('<text x="%s" y="%s" text-anchor="middle">%s</text>' % (_f(X(v)), _f(min(H - 3, Y(ay) + 13)), s))
            else:
                for v in self._tick_range(self.x0, self.x1, self.lx):
                    if abs(v) > 1e-9:
                        o.append('<text x="%s" y="%s" text-anchor="middle">%s</text>' % (_f(X(v)), _f(min(H - 3, Y(ay) + 13)), self._lab(v)))
            for v in self._tick_range(self.y0, self.y1, self.ly):
                if abs(v) > 1e-9:
                    o.append('<text x="%s" y="%s" text-anchor="end">%s</text>' % (_f(max(pl - 2, X(ax) - 4)), _f(Y(v) + 3.5), self._lab(v)))
        cid = "c%x" % (abs(hash((id(self), W, H))) % (16 ** 7))
        o.append('<defs><clipPath id="%s"><rect x="%s" y="%s" width="%s" height="%s"/></clipPath></defs><g clip-path="url(#%s)">' % (cid, _f(X(self.x0)), _f(Y(self.y1)), _f(X(self.x1) - X(self.x0)), _f(Y(self.y0) - Y(self.y1)), cid))
        late = []
        for it in self.items:
            if it[0] == "curve":
                _, paths, col, dash, w = it
                d = "".join("M" + "L".join("%s %s" % (_f(x), _f(y)) for x, y in _rdp([(X(x), Y(y)) for x, y in p], .35)) for p in paths)
                o.append('<path class="cv" d="%s" style="stroke:%s%s"%s/>' % (d, SVGCOL[col], ";stroke-width:%s" % w if w else "", ' stroke-dasharray="5 4"' if dash else ""))
            elif it[0] == "gd":
                _, a, b, c, d = it
                o.append('<line class="gd" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (_f(X(a)), _f(Y(b)), _f(X(c)), _f(Y(d))))
            elif it[0] == "bar":
                _, a, b, c, d, col = it
                o.append('<line x1="%s" y1="%s" x2="%s" y2="%s" style="stroke:%s;stroke-width:5;stroke-linecap:round;opacity:.75"/>' % (_f(X(a)), _f(Y(b)), _f(X(c)), _f(Y(d)), SVGCOL[col]))
            elif it[0] == "dot":
                _, x, y, col, op = it
                if op: late.append('<circle cx="%s" cy="%s" r="4" style="fill:var(--bg);stroke:%s;stroke-width:2"/>' % (_f(X(x)), _f(Y(y)), SVGCOL[col]))
                else: late.append('<circle cx="%s" cy="%s" r="4" style="fill:%s;stroke:var(--bg);stroke-width:1.2"/>' % (_f(X(x)), _f(Y(y)), SVGCOL[col]))
            elif it[0] == "text":
                _, x, y, s, col, _tx = it
                late.append('<text class="lb" x="%s" y="%s" text-anchor="middle" style="fill:%s">%s</text>' % (_f(X(x)), _f(Y(y)), SVGCOL[col], s))
        o.append("".join(late))
        o.append("</g></svg>")
        return "".join(o)

    # ---- TikZ ----
    def tikz(self, width=4.6, height=None):
        ux, uy = self.x1 - self.x0, self.y1 - self.y0
        if height is None:
            height = width * min(1.15, max(.62, uy / ux))
        sx, sy = width / ux, height / uy
        o = [r"\begin{tikzpicture}[x=%scm,y=%scm,baseline={(current bounding box.center)},font=\scriptsize]" % (_t(sx), _t(sy))]
        if self.grid and self.ticks:
            for v in self._tick_range(self.x0, self.x1, self.sx):
                o.append(r"\draw[muted!25,line width=.3pt] (%s,%s)--(%s,%s);" % (_t(v), _t(self.y0), _t(v), _t(self.y1)))
            for v in self._tick_range(self.y0, self.y1, self.sy):
                o.append(r"\draw[muted!25,line width=.3pt] (%s,%s)--(%s,%s);" % (_t(self.x0), _t(v), _t(self.x1), _t(v)))
        ay, ax = max(self.y0, min(self.y1, 0)), max(self.x0, min(self.x1, 0))
        o.append(r"\draw[-latex,muted] (%s,%s)--(%s,%s);" % (_t(self.x0), _t(ay), _t(self.x1), _t(ay)))
        o.append(r"\draw[-latex,muted] (%s,%s)--(%s,%s);" % (_t(ax), _t(self.y0), _t(ax), _t(self.y1)))
        if self.ticks:
            if self.xlab:
                for v, s in self.xlab:
                    o.append(r"\node[below=-1pt,text=muted] at (%s,%s) {$%s$};" % (_t(v), _t(ay), s))
            else:
                for v in self._tick_range(self.x0, self.x1, self.lx):
                    if abs(v) > 1e-9: o.append(r"\node[below=-1pt,text=muted] at (%s,%s) {$%g$};" % (_t(v), _t(ay), v))
            for v in self._tick_range(self.y0, self.y1, self.ly):
                if abs(v) > 1e-9: o.append(r"\node[left=-1pt,text=muted] at (%s,%s) {$%g$};" % (_t(ax), _t(v), v))
        o.append(r"\begin{scope}\clip (%s,%s) rectangle (%s,%s);" % (_t(self.x0), _t(self.y0), _t(self.x1), _t(self.y1)))
        late = []
        for it in self.items:
            if it[0] == "curve":
                _, paths, col, dash, _w = it
                for p in paths:
                    step = max(1, len(p) // 120)
                    q = p[::step]
                    if q[-1] != p[-1]: q.append(p[-1])
                    o.append(r"\draw[%s,line width=1.1pt%s,line join=round] %s;" % (TIKZCOL[col], ",dashed" if dash else "", "--".join("(%s,%s)" % (_t(x), _t(y)) for x, y in q)))
            elif it[0] == "gd":
                _, a, b, c, d = it
                o.append(r"\draw[muted,dashed,line width=.5pt] (%s,%s)--(%s,%s);" % (_t(a), _t(b), _t(c), _t(d)))
            elif it[0] == "bar":
                _, a, b, c, d, col = it
                o.append(r"\draw[%s,line width=2.2pt,opacity=.7] (%s,%s)--(%s,%s);" % (TIKZCOL[col], _t(a), _t(b), _t(c), _t(d)))
            elif it[0] == "dot":
                _, x, y, col, op = it
                late.append(r"\filldraw[fill=%s,draw=%s,line width=.8pt] (%s,%s) circle (1.5pt);" % ("white" if op else TIKZCOL[col], TIKZCOL[col], _t(x), _t(y)))
            elif it[0] == "text":
                _, x, y, s, col, tx = it
                late.append(r"\node[text=%s] at (%s,%s) {%s};" % (TIKZCOL[col], _t(x), _t(y), tx or s))
        o += late
        o.append(r"\end{scope}\end{tikzpicture}")
        return "\n".join(o)


PI = math.pi
sqrt = math.sqrt


def sq(x): return sqrt(x) if x >= 0 else None


def lg(b, x): return math.log(x) / math.log(b) if x > 0 else None


def pw(b, x):
    return b ** x


def cbrt(x): return math.copysign(abs(x) ** (1 / 3), x)


def piece(p, pieces, col="a"):
    """pieces: [(f, a, b, a_tancat, b_tancat)], a/b poden ser None (infinit)"""
    for f, a, b, ac, bc in pieces:
        p.fn(f, a, b, col)
        if a is not None and ac is not None: p.dot(a, f(a), col, open=not ac)
        if b is not None and bc is not None: p.dot(b, f(b), col, open=not bc)
    return p


PIX = [(k * PI / 2, s) for k, s in [(-4, "−2π"), (-2, "−π"), (2, "π"), (4, "2π")]]


def figures():
    F = {}
    P = Plot
    # 7.1 funció o no
    p = P(-5, 5, -4, 4, grid=True, ly=2, lx=2)
    for x in range(-4, 5): p.dot(x, 2)
    F["rel1"] = p
    p = P(-5, 5, -4, 4, ly=2, lx=2)
    for x, y in [(-4, 1), (-3, 2), (-2, 1), (-1, 1), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]: p.dot(x, y)
    F["rel2"] = p
    F["rel3"] = P(-5, 5, -4, 4, ly=2, lx=2).fn(lambda x: -3 * math.sin(x * PI / 4), -4, 4)
    F["rel4"] = P(-5, 5, -4, 4, ly=2, lx=2).param(lambda t: t * t * t * .13 * (-1) + t * 1.45, lambda t: t, -4, 4)
    # 7.2 domini i recorregut
    F["domdef"] = piece(P(-1, 9, -1, 5, W=300), [(lambda x: 2 + 2 * math.sin((x - 1) * PI / 4), 1, 8, True, True)]).xbar(1, 8).ybar(0, 4).gd(3, 0, 3, 4).gd(0, 4, 3, 4).gd(7, 0, 7, 0).gd(0, 0, 7, 0)
    F["doma"] = P(-1.6, .9, -.4, 2.4, sx=.5, sy=1, W=220).fn(lambda x: 16 * x * x * (x + 1) ** 2)
    pb = P(-2, 7, -3, 4, W=220)
    pb.fn(lambda x: x - 1, -2, 1).fn(lambda x: (x - 2) ** 2 - 1, 1, 4).dot(4, 3).seg(4, -1, 6, -1).dot(4, -1, open=True).dot(6, -1, open=True)
    F["domb"] = pb
    F["domc"] = P(-5, 5, -4, 4, W=220, ly=2, lx=2).fn(lambda x: 1 / x if x else None)
    fd = lambda: P(-5, 7, -2, 5, W=220).fn(lambda x: (x + 2) ** 2 - 1, -4, 0).dot(-4, 3).dot(0, 3, open=True).seg(0, 4, 3, 4).dot(0, 4).dot(3, 4).seg(3, 3, 6, 0).dot(3, 3, open=True).dot(6, 0, open=True)
    F["domd"] = fd()
    fe = lambda: P(-2.5, 5, -2, 4, W=220).fn(lambda x: x / 2, -2.5, 2).fn(lambda x: 1 + 1 / (x - 2), 2.01, 5).dot(2, 1, open=True).vl(2).hl(1)
    F["dome"] = fe()
    ff = lambda: P(-3.5, 3.5, -2.5, 3, W=220).fn(lambda x: -x - 1, -3.5, -1).fn(lambda x: 2 * x * x - 2, -1, 1).fn(lambda x: x - 1, 1, 3.5)
    F["domf"] = ff()
    # 7.3 talls
    t = ff().dot(-1, 0, "b").dot(1, 0, "b").dot(0, -2, "g")
    F["cut1"] = t
    t = fd().dot(-3, 0, "b").dot(-1, 0, "b")
    t.dot(0, 4, "g")
    F["cut2"] = t
    # 7.4 monotonia
    F["mono1"] = ff()
    F["mono2"] = fd()
    pts = [12, 15, 13, 6, 10, 20, 15, 18, 10, 12, 7]
    p = P(-.5, 10.5, -1, 22, sy=2, ly=4, W=320)
    for i in range(10): p.seg(i, pts[i], i + 1, pts[i + 1])
    for i in range(11): p.dot(i, pts[i])
    F["mono3"] = p
    # 7.5 continuïtat
    F["cont1"] = ff()
    F["cont2"] = fd()
    F["cont3"] = fe()
    c = lambda: P(-.5, 6, -.5, 5, ticks=False, grid=False, W=170)
    g1 = lambda x: 2 + .5 * math.sin(x * .9)
    F["de1"] = c().fn(g1, -.3, 5.5).dot(3, g1(3), open=True).gd(3, 0, 3, g1(3)).text(3, -.2, "c")
    F["de2"] = c().fn(g1, -.3, 5.5).dot(3, g1(3), open=True).dot(3, 1).gd(3, 0, 3, g1(3)).text(3, -.2, "c")
    l1 = lambda x: 3 + .25 * (x - 2) ** 2 - .4
    r1 = lambda x: 1.6 + .15 * (x - 4) ** 2
    F["ds1"] = c().fn(l1, -.3, 3).fn(r1, 3, 5.7).dot(3, l1(3)).dot(3, r1(3), open=True).gd(3, 0, 3, l1(3)).text(3, -.2, "c")
    F["ds2"] = c().fn(l1, -.3, 3).fn(r1, 3, 5.7).dot(3, l1(3), open=True).dot(3, r1(3), open=True).gd(3, 0, 3, l1(3)).text(3, -.2, "c")
    li = lambda x: .6 / (3 - x) + .5
    F["di1"] = c().fn(li, -.3, 2.99).fn(r1, 3, 5.7).dot(3, r1(3)).vl(3).text(3.25, -.2, "a")
    F["di2"] = c().fn(li, -.3, 2.99).fn(r1, 3, 5.7).dot(3, r1(3), open=True).vl(3).text(3.25, -.2, "a")
    F["da1"] = c().fn(lambda x: 1.4 + .8 / (x - 3) if x != 3 else None).vl(3).hl(1.4).text(3.25, -.2, "a")
    F["da2"] = c().fn(lambda x: .5 + .6 / (x - 3) ** 2 if x != 3 else None).vl(3).text(3.25, -.2, "a")
    # 7.6 simetries i periodicitat
    F["par1"] = P(-5, 5, -1, 12, ly=2, sy=2, lx=2, W=220).fn(lambda x: x * x + 1)
    F["par2"] = P(-2.6, 2.6, -4, 4, sx=.5, lx=1, W=220).fn(lambda x: x * x / (x ** 4 - 1) if abs(abs(x) - 1) > 1e-9 else None).vl(-1).vl(1)
    F["sen1"] = P(-3, 3, -3.5, 3.5, W=220).fn(lambda x: x ** 3 + x)
    F["sen2"] = P(-6, 6, -.45, .45, sx=1, sy=.1, lx=2, ly=.2, W=240).fn(lambda x: x / (x * x + 3))
    F["per1"] = P(-2 * PI - .3, 4 * PI + .3, -2, 2, sx=PI / 2, xlab=[(k * PI, s) for k, s in [(-2, "−2π"), (-1, "−π"), (1, "π"), (2, "2π"), (3, "3π"), (4, "4π")]], W=380).fn(math.cos)
    # 7.7 lineals
    F["const"] = P(-5, 8, -2, 6, W=240, lx=2, ly=2).fn(lambda x: 3).text(-2.6, 3.6, "y = 3")
    F["lin"] = P(-6, 6, -5, 6, W=240, lx=2, ly=2).fn(lambda x: x / 2, col="a").fn(lambda x: 3 * x, col="g").fn(lambda x: -x, col="b")
    F["afi"] = P(-4, 5, -2, 6, W=240).fn(lambda x: 2 * x + 3).dot(0, 3, "b").text(3, 4.8, "y = 2x + 3")
    p = P(-2, 5, -1, 8, W=260).fn(lambda x: 2 * x + 1).dot(1, 3, "b").dot(3, 7, "b").gd(1, 3, 3, 3).gd(3, 3, 3, 7).text(2, 2.4, "2").text(3.35, 5, "4").text(.45, 3.7, "A").text(3.45, 7.4, "B")
    F["pend"] = p
    F["rec1"] = P(-3, 7, -3, 7, W=240).fn(lambda x: 3 * x - 8).dot(3, 1, "b").dot(4, 4, "b")
    F["rec2"] = P(-2, 9, -6, 7, W=240).fn(lambda x: -2 * x + 12).dot(4, 4, "b").dot(6, 0, "b")
    # 7.8 quadràtica i cúbica
    F["q1"] = P(-5, 7, -3, 7, W=240).fn(lambda x: (x - 3) ** 2, col="g").fn(lambda x: 2 - x * x, col="b")
    p = P(-5, 3.5, -5, 6, W=260).fn(lambda x: x * x + 2 * x - 3).dot(-3, 0, "b").dot(1, 0, "b").dot(0, -3, "g").dot(-1, -4, "v").gd(-1, -5, -1, 6)
    F["q2"] = p
    F["cat"] = P(-3, 3, 0, 7, W=280).fn(lambda x: .6 * (x * x) + 1, col="b").fn(lambda x: math.cosh(x), col="a")
    F["qt1"] = P(-4, 4, -5, 6, W=210).fn(lambda x: 2 * x * x, col="g").fn(lambda x: -x * x, col="b")
    F["qt2"] = P(-4, 4, -6, 8, W=210, ly=2, sy=2).fn(lambda x: x * x + 4, col="g").fn(lambda x: -x * x / 2 - 1, col="b")
    F["qt3"] = P(-3, 3, -6, 6, W=210, ly=2, sy=2).fn(lambda x: 2 * x * x - 3 * x, col="g").fn(lambda x: -2 * x * x - 2 * x, col="b")
    F["c1"] = P(-3, 3, -6, 6, W=210, ly=2, sy=2).fn(lambda x: -x ** 3 - 1)
    F["c2"] = P(-3.5, 3, -5, 5, W=210).fn(lambda x: x ** 3 + 2.5 * x * x)
    # 7.9 racionals
    hyp = lambda f, h, v, a=-7, b=7, y0=-6, y1=6: (lambda p: (p.vl(h) if h else p, p.hl(v) if v else p, p)[2])(P(a, b, y0, y1, W=210, lx=2, ly=2).fn(f))
    F["h1"] = hyp(lambda x: 3 / x if x else None, 0, 0)
    F["h2"] = hyp(lambda x: -1 / x if x else None, 0, 0)
    F["hv1"] = hyp(lambda x: 3 / x + 2 if x else None, 0, 2)
    F["hv2"] = hyp(lambda x: 3 / x - 1 if x else None, 0, -1)
    F["hh1"] = hyp(lambda x: 3 / (x - 1) if x != 1 else None, 1, 0)
    F["hh2"] = hyp(lambda x: 3 / (x + 4) if x != -4 else None, -4, 0)
    F["hd1"] = hyp(lambda x: 3 / (x - 2) + 1 if x != 2 else None, 2, 1)
    F["hd2"] = hyp(lambda x: 3 / (x + 3) - 2 if x != -3 else None, -3, -2)
    # 7.10 radicals
    R = lambda a=-2, b=10, y0=-2, y1=6: P(a, b, y0, y1, W=210, lx=2, ly=2)
    F["r2"] = R().fn(lambda x: sq(x), 0, 10, "a").fn(lambda x: sq(2 * x), 0, 10, "b").fn(lambda x: 2 * sq(x) if x >= 0 else None, 0, 10, "o")
    F["r4"] = R(-1, 8, -1, 3).fn(lambda x: x ** .25 if x >= 0 else None, 0, 8, "g").fn(lambda x: (2 * x) ** .25 if x >= 0 else None, 0, 8, "m")
    F["r3"] = P(-6, 7, -3, 3, W=260).fn(cbrt, col="o").fn(lambda x: 1.3 * cbrt(x), col="t")
    rs = lambda f, a, x0, y0: R().fn(f, a, 10).dot(x0, y0, "b")
    F["rv1"] = R(-2, 9, -1, 7).fn(lambda x: sq(x) + 3 if x >= 0 else None, 0, 9).dot(0, 3, "b")
    F["rv2"] = R(-2, 9, -2, 4).fn(lambda x: sq(x) - 1 if x >= 0 else None, 0, 9).dot(0, -1, "b")
    F["rh1"] = R(-4, 7, -2, 5).fn(lambda x: sq(x + 3) if x >= -3 else None, -3, 7).dot(-3, 0, "b")
    F["rh2"] = R(-2, 9, -2, 5).fn(lambda x: sq(x - 1) if x >= 1 else None, 1, 9).dot(1, 0, "b")
    F["rd1"] = R(-3, 7, -4, 2).fn(lambda x: sq(x + 2) - 3 if x >= -2 else None, -2, 7).dot(-2, -3, "b").gd(-2, 0, -2, -3).gd(0, -3, -2, -3)
    F["rd2"] = R(-1, 9, -1, 6).fn(lambda x: sq(x - 1) + 2 if x >= 1 else None, 1, 9).dot(1, 2, "b").gd(1, 0, 1, 2).gd(0, 2, 1, 2)
    F["rr1"] = R(-1, 10, -4, 2).fn(lambda x: -sq(x) if x >= 0 else None, 0, 10)
    F["rr2"] = R(-9, 2, -2, 4).fn(lambda x: sq(-x) if x <= 0 else None, -9, 0)
    F["rr3"] = R(-9, 2, -4, 2).fn(lambda x: -sq(-x) if x <= 0 else None, -9, 0)
    F["rr4"] = R(-3, 7, -4, 2).fn(lambda x: -sq(x + 2) if x >= -2 else None, -2, 7).dot(-2, 0, "b")
    F["rr5"] = R(-7, 4, -2, 4).fn(lambda x: sq(-x + 3) if x <= 3 else None, -7, 3).dot(3, 0, "b")
    F["rr6"] = R(-9, 2, -3, 2).fn(lambda x: -sq(-x - 1) + 1 if x <= -1 else None, -9, -1).dot(-1, 1, "b")
    # 7.11 exponencials
    E = lambda a=-4, b=4, y0=-2, y1=7: P(a, b, y0, y1, W=210, ly=2, lx=2)
    F["e1"] = E().fn(lambda x: 2 ** x).dot(0, 1, "b").hl(0)
    F["e2"] = E().fn(lambda x: .5 ** x).dot(0, 1, "b")
    F["ev1"] = E().fn(lambda x: 3 ** x + 2).dot(0, 3, "b").hl(2)
    F["ev2"] = E().fn(lambda x: 3 ** x - 1).dot(0, 0, "b").hl(-1)
    F["eh1"] = E().fn(lambda x: 3 ** (x + 2)).dot(-2, 1, "b").gd(-2, 0, -2, 1).gd(0, 1, -2, 1)
    F["eh2"] = E().fn(lambda x: 3 ** (x - 1)).dot(1, 1, "b").gd(1, 0, 1, 1).gd(0, 1, 1, 1)
    F["ed1"] = E(-5, 3, -4, 6).fn(lambda x: 3 ** (x + 1) - 2).dot(-1, -1, "b").hl(-2)
    F["ed2"] = E(-3, 5, -1, 8).fn(lambda x: 3 ** (x - 2) + 1).dot(2, 2, "b").hl(1)
    F["ed3"] = E(-3, 9, -3, 7).fn(lambda x: .5 ** (x - 3) - 1).dot(3, 0, "b").hl(-1)
    F["ed4"] = E(-6, 5, -5, 5).fn(lambda x: .5 ** (x + 1) - 3).dot(-1, -2, "b").hl(-3)
    F["es1"] = E(-4, 4, -6, 2).fn(lambda x: -2 ** x).dot(0, -1, "b")
    F["es2"] = E(-4, 4, -6, 2).fn(lambda x: -.5 ** x).dot(0, -1, "b")
    F["es3"] = E().fn(lambda x: 2 ** -x).dot(0, 1, "b")
    F["es4"] = E().fn(lambda x: .5 ** -x).dot(0, 1, "b")
    # 7.12 logarítmiques
    Lg = lambda a=-2, b=7, y0=-5, y1=4: P(a, b, y0, y1, W=210, ly=2, lx=2)
    F["l1"] = Lg().fn(lambda x: lg(2, x), .01, 7).dot(1, 0, "b").vl(0)
    F["l2"] = Lg().fn(lambda x: lg(.5, x), .01, 7).dot(1, 0, "b").vl(0)
    F["lv1"] = Lg().fn(lambda x: lg(2, x) + 1, .01, 7).dot(1, 1, "b").gd(1, 0, 1, 1).gd(0, 1, 1, 1)
    F["lv2"] = Lg(-2, 7, -7, 2).fn(lambda x: lg(2, x) - 3, .01, 7).dot(1, -3, "b").gd(1, 0, 1, -3).gd(0, -3, 1, -3)
    F["lh1"] = Lg(-3, 6).fn(lambda x: lg(2, x + 1), -.99, 6).dot(0, 0, "b").vl(-1)
    F["lh2"] = Lg(-1, 9).fn(lambda x: lg(2, x - 3), 3.01, 9).dot(4, 0, "b").vl(3)
    F["ld1"] = Lg(-1, 8, -4, 5).fn(lambda x: lg(2, x - 1) + 2, 1.01, 8).dot(2, 2, "b").vl(1)
    F["ld2"] = Lg(-5, 6, -5, 3).fn(lambda x: lg(2, x + 3) - 1, -2.99, 6).dot(-2, -1, "b").vl(-3)
    F["ld3"] = Lg(-1, 8, -6, 4).fn(lambda x: lg(.5, x - 2) - 3, 2.01, 8).dot(3, -3, "b").vl(2)
    F["ld4"] = Lg(-3, 6, -2, 7).fn(lambda x: lg(.5, x + 1) + 2, -.99, 6).dot(0, 2, "b").vl(-1)
    # 7.13 trigonomètriques
    T = lambda y0=-2.5, y1=2.5: P(-2 * PI - .4, 2 * PI + .4, y0, y1, sx=PI / 2, xlab=PIX, W=340)
    F["sin"] = T().fn(math.sin, col="g")
    F["cos"] = T().fn(math.cos, col="b")
    pt = P(-2 * PI - .4, 2 * PI + .4, -6, 6, sx=PI / 2, xlab=PIX, W=340, sy=2).fn(math.tan, col="o", n=1400)
    for k in (-3, -1, 1, 3): pt.vl(k * PI / 2)
    F["tan"] = pt
    # 7.14 a trossos i valor absolut
    F["t1"] = P(-3.5, 6.5, -1, 7, W=240).fn(lambda x: x * x, -3.5, 2).seg(2, 4, 6.5, 4).dot(2, 4, open=True)
    t = lambda: P(-7, 8, -5, 10, W=260, sy=1, ly=2, lx=2).vl(-2).vl(3)
    F["t2"] = t()
    F["t3"] = t().fn(lambda x: -x + 1, -7, -2).dot(-2, 3, open=True)
    F["t4"] = t().fn(lambda x: -x + 1, -7, -2).dot(-2, 3, open=True).fn(lambda x: x * x - x - 2, -2, 3).dot(-2, 4).dot(3, 4)
    F["t5"] = t().fn(lambda x: -x + 1, -7, -2).dot(-2, 3, open=True).fn(lambda x: x * x - x - 2, -2, 3).dot(-2, 4).dot(3, 4).seg(3, 2, 8, 2).dot(3, 2, open=True)
    F["a1"] = P(-4.5, 4, -4, 3.5, W=230).fn(lambda x: -x * x - x + 2, col="v")
    F["a2"] = P(-4.5, 4, -3, 5.5, W=230).fn(lambda x: -x * x - x + 2, col="v", dash=True).fn(lambda x: abs(-x * x - x + 2), col="a")
    # 7.16 inversa
    I = lambda: P(-3, 6, -3, 6, W=240).seg(-3, -3, 6, 6, "m", True)
    F["i1"] = I().fn(lambda x: 2 ** x + 1, col="a").fn(lambda x: lg(2, x - 1), 1.001, 6, "g")
    F["i2"] = I().fn(lambda x: x * x + 3, 0, 3, "b").fn(lambda x: x * x + 3, -3, 0, "b", dash=True).fn(lambda x: sq(x - 3), 3, 6, "o")
    F["i3"] = P(-2, 5, -2, 5, W=240).seg(-2, -2, 5, 5, "m", True).fn(lambda x: 3 * x - 1, col="o").fn(lambda x: (x + 1) / 3, col="g")
    return F
