# Ajudes compartides pels apunts de la Unitat 6 de 1r ESO (alg.py, eq.py, build.py).
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

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
def D(s):
    """fórmula centrada; si porta diverses parts separades per \\qquad, cada part va en un bloc que salta de línia en pantalles estretes"""
    parts = s.split(r'\qquad')
    if len(parts) >= 3 and r'\begin' not in s:
        return '<div class="eqv">' + ''.join(r'<span>\(\displaystyle %s\)</span>' % p.strip() for p in parts) + '</div>'
    return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)
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
    return (f'\n<!-- ======================= 6.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">6.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def table(head, rows, cls='data'):
    h = '<thead><tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr></thead>' if head else ''
    return f'<div class="tbl-wrap"><table class="{cls}">{h}<tbody>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</tbody></table></div>'

# ---------- ginys ----------
def drill(kind, va, es, en, hint=''):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  {hint}<div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='w', mode='text'):
    lab = lab + ' ' if lab else ''
    return f'<label>{lab}<input class="tin {cls}" type="text" inputmode="{mode}" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls=''):
    return (f'<div class="widget{extra_cls}" id="{wid}">\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
def hint_s(va, es, en): return '<p class="hint-s">' + L(va, es, en) + '</p>'
HELP_E = hint_s("Escriu l'expressió amb la lletra x. El producte es pot escriure amb * o sense signe (3x), les potències amb ^ (x^2) i les fraccions amb / (x/2).",
                "Escribe la expresión con la letra x. El producto se puede escribir con * o sin signo (3x), las potencias con ^ (x^2) y las fracciones con / (x/2).",
                "Type the expression using the letter x. Products can be written with * or no sign (3x), powers with ^ (x^2) and fractions with / (x/2).")
HELP_Q = hint_s("Escriu l'equació amb el signe =. Exemples: 3x+5=20, 2(x-1)=x+4, x/2+x/3=5.",
                "Escribe la ecuación con el signo =. Ejemplos: 3x+5=20, 2(x-1)=x+4, x/2+x/3=5.",
                "Type the equation with an = sign. Examples: 3x+5=20, 2(x-1)=x+4, x/2+x/3=5.")

# ---------- comprovacions amb sympy ----------
x, y, a, b = sp.symbols('x y a b')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
LOC = {'x': x, 'y': y, 'a': a, 'b': b, 'n': sp.Symbol('n'), 'z': sp.Symbol('z'), 'l': sp.Symbol('l'), 'h': sp.Symbol('h'), 'k': sp.Symbol('k'), 't': sp.Symbol('t'), 'c': sp.Symbol('c')}
NCHK = [0]
def S(s): return parse_expr(s.replace('·', '*').replace(':', '/'), transformations=TR, local_dict=LOC) if isinstance(s, str) else s
def chk(lhs, rhs):
    """dues expressions iguals (p. ex. una reducció escrita a mà)"""
    NCHK[0] += 1
    assert sp.expand(S(lhs) - S(rhs)) == 0, (lhs, rhs, sp.expand(S(lhs)))
def cv(expr, vals, res):
    """valor numèric: cv('3x-5', {'x': 4}, 7)"""
    NCHK[0] += 1
    v = S(expr).subs({LOC[k]: sp.nsimplify(w) for k, w in vals.items()})
    assert sp.nsimplify(v) == sp.nsimplify(res), (expr, vals, v, res)
def ce(eq, sol):
    """equació de primer grau amb la solució indicada"""
    NCHK[0] += 1
    l, r = eq.split('=')
    e = sp.expand(S(l) - S(r))
    assert sp.degree(e, x) == 1, (eq, e)
    got = sp.solve(e, x)
    assert got == [sp.nsimplify(sol)], (eq, got, sol)
