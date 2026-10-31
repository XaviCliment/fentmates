# Figures etiquetades dels cossos de la Unitat 11 (llistes d'elements per a G() o per a tz() de la fitxa).
import math
from solids import *

def _mid(A, B): return ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)

def f_prism(n, l, h, ll='l', lh='h', th=TH, ph=PH):
    """prisma regular amb l'aresta de la base i l'altura etiquetades"""
    it, P = polyhedron(prism(n, l, h), th=th, ph=ph)
    k = min(range(n), key=lambda i: _mid(P[i], P[(i + 1) % n])[1])   # aresta de la base més baixa en el dibuix
    if ll: it.append(('txt', _mid(P[k], P[(k + 1) % n]), ll, {'dy': 15}))
    r = max(range(n), key=lambda i: P[i][0])                          # aresta lateral de més a la dreta
    if lh: it.append(('txt', _mid(P[r], P[r + n]), lh, {'dx': 8, 'a': 'start'}))
    return it, P

def f_cuboid(a, b, c, la='a', lb='b', lc='c', diag=False, th=TH, ph=PH):
    V = cuboid(a, b, c)
    it, P = polyhedron(V, th=th, ph=ph)
    # V: índex = x + 2y + 4z
    if la: it.append(('txt', _mid(P[0], P[1]), la, {'dy': 15}))
    if lb: it.append(('txt', _mid(P[1], P[3]), lb, {'dx': 8, 'a': 'start', 'dy': 10}))
    if lc: it.append(('txt', _mid(P[1], P[5]), lc, {'dx': 8, 'a': 'start'}))
    if diag:
        it += [('seg', P[0], P[7], 'ax'), ('seg', P[0], P[3], 'ax2'), ('txt', _mid(P[0], P[7]), 'D', {'dx': -8, 'a': 'end', 'cls': 'hot'})]
    return it, P

SUB = lambda a, b: a + '<tspan dy="3" font-size="10">' + b + '</tspan>'
def f_pyramid(n, l, h, labs=('l', 'h', SUB('a', 'b'), SUB('a', 'p')), th=TH, ph=PH, inner=True):
    V = pyramid(n, l, h)
    it, P = polyhedron(V, th=th, ph=ph)
    k = min(range(n), key=lambda i: _mid(P[i], P[(i + 1) % n])[1])            # aresta de baix: s'hi escriu l
    j = max(range(n), key=lambda i: _mid(P[i], P[(i + 1) % n])[0])            # aresta de la dreta: s'hi dibuixa l'apotema
    A, B = P[k], P[(k + 1) % n]; M = _mid(P[j], P[(j + 1) % n])
    O = proj((0, 0, 0), th, ph); Ap = P[n]
    if labs[0]: it.append(('txt', _mid(A, B), labs[0], {'dy': 15}))
    if inner:
        it += [('seg', O, Ap, 'ax'), ('seg', O, M, 'ax'), ('seg', M, Ap, 'ax2'), ('dot', O)]
        if labs[1]: it.append(('txt', _mid(O, Ap), labs[1], {'dx': -7, 'a': 'end', 'cls': 'ax'}))
        if labs[2]: it.append(('txt', _mid(O, M), labs[2], {'dx': -7, 'dy': -3, 'a': 'end', 'cls': 'ax'}))
        if labs[3]: it.append(('txt', _mid(M, Ap), labs[3], {'dx': 8, 'a': 'start', 'cls': 'ax2'}))
    return it, P

def f_cylinder(r, h, lr='r', lh='h', ph=PH):
    it, K = cylinder(r, h, ph)
    it += [('seg', K['B'], K['R'], 'ax'), ('dot', K['B'])]
    if lr: it.append(('txt', _mid(K['B'], K['R']), lr, {'dy': -5, 'cls': 'ax'}))
    if lh: it.append(('txt', _mid(K['R'], K['RT']), lh, {'dx': 8, 'a': 'start'}))
    return it, K

def f_cone(r, h, lr='r', lh='h', lg='g', ph=PH):
    it, K = cone(r, h, ph)
    it += [('seg', K['B'], K['R'], 'ax'), ('seg', K['B'], K['A'], 'ax'), ('dot', K['B'])]
    if lr: it.append(('txt', _mid(K['B'], K['R']), lr, {'dy': -5, 'cls': 'ax'}))
    if lh: it.append(('txt', _mid(K['B'], K['A']), lh, {'dx': -7, 'a': 'end', 'cls': 'ax'}))
    if lg: it.append(('txt', _mid(K['R'], K['A']), lg, {'dx': 8, 'a': 'start'}))
    return it, K

def f_sphere(r, lr='r', ph=PH):
    it, K = sphere(r, ph)
    it += [('seg', K['C'], K['R'], 'ax'), ('dot', K['C'])]
    if lr: it.append(('txt', _mid(K['C'], K['R']), lr, {'dy': -5, 'cls': 'ax'}))
    return it, K
