import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# Genera materials/3eso/t4-polinomis.html. Ús: python3 _eines/apunts/3eso-t4/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
# Els resultats dels problemes resolts es comproven amb sympy (chk).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/3eso/t4-polinomis.html")

def L(va, es, en):
    return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
def P(va, es, en): return '<p>' + L(va, es, en) + '</p>'
def box(cls, title, body):
    head = f'<div class="bh">{title}</div>' if title else ''
    return f'<div class="box {cls}">{head}<div class="bb">{body}</div></div>\n'
def note(va, es, en, icon='💡'): return f'<div class="note"><p>{icon} {L(va, es, en)}</p></div>'
def sub(va, es, en): return f'<h3 class="sub">{L(va, es, en)}</h3>\n'
def ul(*items): return '<ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul>'
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
    return (f'\n<!-- ======================= 4.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">4.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'

# ---------- ginys ----------
def drill(kind, va, es, en):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='w'):
    return f'<label>{lab} <input class="tin {cls}" type="text" inputmode="text" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls=''):
    return (f'<div class="widget{extra_cls}" id="{wid}">\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
HELP = '<p class="hint-s">' + L("Escriu les potències amb ^ (x^2) i el producte amb * o sense signe (3x).", "Escribe las potencias con ^ (x^2) y el producto con * o sin signo (3x).", "Type powers with ^ (x^2) and products with * or no sign (3x).") + '</p>'
STEPCTL = '<div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><span class="step-count"></span></div>'

# ---------- àlgebra amb sympy (per a comprovar i escriure resultats) ----------
x, y, z = sp.symbols('x y z')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s, transformations=TR, local_dict={'x': x, 'y': y, 'z': z, 'a': sp.Symbol('a'), 'b': sp.Symbol('b')}) if isinstance(s, str) else s
def chk(lhs, rhs):
    assert sp.expand(S(lhs) - S(rhs)) == 0, (lhs, rhs, sp.expand(S(lhs)))
def ntex(c):
    c = sp.Rational(c)
    if c.q == 1: return str(c.p)
    return ('-' if c < 0 else '') + r'\frac{%d}{%d}' % (abs(c.p), c.q)
def pt(e):
    """polinomi en TeX, ordenat de grau més alt a més baix"""
    e = sp.expand(S(e))
    if e == 0: return '0'
    gens = sorted(e.free_symbols, key=str)
    if not gens: return ntex(e)
    out = ''
    for mon, c in sp.Poly(e, *gens).terms(order='grlex'):
        lit = ''.join(str(g) if k == 1 else '%s^{%d}' % (g, k) for g, k in zip(gens, mon) if k)
        a = abs(sp.Rational(c))
        s = (ntex(a) if a != 1 or not lit else '') + lit
        out += ('-' if c < 0 else ('+' if out else '')) + s
    return out

# ---------- taules de Ruffini i de divisió (HTML) ----------
def tt(c, k, v='x', first=False):
    c = Fr(c)
    if c == 0: return ''
    lit = '' if k == 0 else (v if k == 1 else '%s^{%d}' % (v, k))
    a = abs(c); num = (str(a.numerator) if a.denominator == 1 else r'\frac{%d}{%d}' % (a.numerator, a.denominator))
    s = (num if a != 1 or not lit else '') + lit
    return ('-' if c < 0 else ('' if first else '+')) + s
def ctex(cs, v='x'):
    """coeficients (de grau alt a baix) -> TeX"""
    n = len(cs) - 1; out = ''
    for i, c in enumerate(cs):
        t = tt(c, n - i, v, first=not out)
        out += t
    return out or '0'
def fn(c): c = Fr(c); return str(c.numerator) if c.denominator == 1 else r'\frac{%d}{%d}' % (c.numerator, c.denominator)
def ruffini(cs, a):
    b = [Fr(cs[0])]; mid = [None]
    for c in cs[1:]:
        m = b[-1] * a; mid.append(m); b.append(Fr(c) + m)
    return mid, b
def ruf_html(cs, a):
    mid, b = ruffini(cs, a); n = len(cs) - 1
    def td(cls, t): return '<td%s>%s</td>' % (' class="%s"' % cls if cls else '', t)
    m = lambda t: '\\(' + t + '\\)'
    r1 = td('ra', '') + ''.join(td('rl' if i == n else '', m(fn(c))) for i, c in enumerate(cs))
    r2 = td('ra', m(fn(a))) + ''.join(td('m rl' if i == n else 'm', '' if v is None else m(fn(v))) for i, v in enumerate(mid))
    r3 = td('ra', '') + ''.join(td('rl rr' if i == n else '', m(fn(c))) for i, c in enumerate(b))
    return '<div class="mfig"><table class="ruf"><tbody><tr>%s</tr><tr>%s</tr><tr class="rb">%s</tr></tbody></table></div>' % (r1, r2, r3)
def divide(A, B):
    A = [Fr(c) for c in A]; B = [Fr(c) for c in B]
    n, m = len(A) - 1, len(B) - 1
    r = A[:]; q = [Fr(0)] * (n - m + 1); steps = []
    def deg(v):
        for i, c in enumerate(v):
            if c != 0: return n - i
        return -1
    while deg(r) >= m:
        d = deg(r); c = r[n - d] / B[0]; s = d - m
        q[n - m - s] = c
        sub = [Fr(0)] * (n + 1)
        for i in range(m + 1): sub[n - d + i] = -c * B[i]
        r = [ri + si for ri, si in zip(r, sub)]
        steps.append((d, s, sub, r[:]))
    return q, r[n - m + 1:] if m else [r[-1]], steps
def ldiv_html(A, B, v='x'):
    q, rr, steps = divide(A, B); n = len(A) - 1
    def row(arr, cls, hi, lo):
        return '<tr class="%s">' % cls + ''.join('<td>%s</td>' % ('\\(' + tt(arr[n - k], k, v) + '\\)' if lo <= k <= hi and arr[n - k] != 0 else '') for k in range(n, -1, -1))
    h = '<div class="mfig"><table class="ldiv"><tbody>' + row(A, '', n, 0).replace('\\(+', '\\(', 1) + '<td class="dv">\\(%s\\)</td></tr>' % ctex(B, v)
    for j, (d, s, sub, r) in enumerate(steps):
        h += row(sub, 'sub', d, s) + ('<td class="qt">\\(%s\\)</td>' % ctex(q, v) if j == 0 else '<td></td>') + '</tr>'
        h += row(r, 'rem', d - 1, 0) + '<td></td></tr>'
    return h + '</tbody></table></div>'

# ---------- figures de les identitats ----------
def svg_sq():
    A, B = 130, 70; T = A + B
    g = (f'<rect class="ar-a" x="0" y="0" width="{A}" height="{A}"/><rect class="ar-ab" x="{A}" y="0" width="{B}" height="{A}"/>'
         f'<rect class="ar-ab" x="0" y="{A}" width="{A}" height="{B}"/><rect class="ar-b" x="{A}" y="{A}" width="{B}" height="{B}"/>'
         f'<rect class="ar-ln" x="0" y="0" width="{T}" height="{T}"/><line class="ar-ln" x1="{A}" y1="0" x2="{A}" y2="{T}"/><line class="ar-ln" x1="0" y1="{A}" x2="{T}" y2="{A}"/>'
         f'<text class="ar-t" x="{A/2}" y="{A/2+5}" text-anchor="middle">a²</text><text class="ar-t" x="{A+B/2}" y="{A/2+5}" text-anchor="middle">ab</text>'
         f'<text class="ar-t" x="{A/2}" y="{A+B/2+5}" text-anchor="middle">ab</text><text class="ar-t" x="{A+B/2}" y="{A+B/2+5}" text-anchor="middle">b²</text>'
         f'<text class="ar-tm" x="{A/2}" y="-8" text-anchor="middle">a</text><text class="ar-tm" x="{A+B/2}" y="-8" text-anchor="middle">b</text>'
         f'<text class="ar-tm" x="-10" y="{A/2+4}" text-anchor="middle">a</text><text class="ar-tm" x="-10" y="{A+B/2+4}" text-anchor="middle">b</text>')
    return f'<svg viewBox="-22 -24 {T+30} {T+32}" style="width:{T+30}px">{g}</svg>'
def svg_dif():
    A, B = 150, 60
    l = (f'<rect class="ar-a" x="0" y="0" width="{A}" height="{A-B}"/><rect class="ar-a" x="0" y="{A-B}" width="{A-B}" height="{B}"/>'
         f'<rect class="ar-cut" x="{A-B}" y="{A-B}" width="{B}" height="{B}"/><path class="ar-ln" d="M0 0 H{A} V{A-B} H{A-B} V{A} H0 Z"/>'
         f'<text class="ar-t" x="{(A-B)/2+20}" y="{(A-B)/2+10}" text-anchor="middle">a² − b²</text><text class="ar-tm" x="{A-B/2}" y="{A-B/2+5}" text-anchor="middle">b²</text>'
         f'<text class="ar-tm" x="{A/2}" y="-8" text-anchor="middle">a</text><text class="ar-tm" x="{A-B/2}" y="{A+16}" text-anchor="middle">b</text>')
    r = (f'<rect class="ar-a" x="0" y="0" width="{A+B}" height="{A-B}"/><rect class="ar-ln" x="0" y="0" width="{A+B}" height="{A-B}"/><line class="ar-ln" x1="{A}" y1="0" x2="{A}" y2="{A-B}" stroke-dasharray="4 4"/>'
         f'<text class="ar-t" x="{(A+B)/2}" y="{(A-B)/2+5}" text-anchor="middle">(a+b)(a−b)</text>'
         f'<text class="ar-tm" x="{(A+B)/2}" y="-8" text-anchor="middle">a + b</text><text class="ar-tm" x="{A+B+8}" y="{(A-B)/2+4}">a − b</text>')
    return (f'<figure><svg viewBox="-12 -24 {A+30} {A+46}" style="width:{A+30}px">{l}</svg><figcaption>{L("Al quadrat de costat a li llevem el de costat b", "Al cuadrado de lado a le quitamos el de lado b", "Remove the b-square from the a-square")}</figcaption></figure>'
            f'<figure><svg viewBox="-12 -24 {A+B+70} {A-B+40}" style="width:{A+B+70}px">{r}</svg><figcaption>{L("Movem el tros de baix al costat: és un rectangle", "Movemos el trozo de abajo al lado: es un rectángulo", "Move the bottom strip to the side: it’s a rectangle")}</figcaption></figure>')

# =====================================================================
# 4.1 Llenguatge algebraic
# =====================================================================
TR1 = [("El doble d'un nombre", "El doble de un número", "Twice a number", "2x"),
       ("El triple d'un nombre", "El triple de un número", "Three times a number", "3x"),
       ("La meitat d'un nombre", "La mitad de un número", "Half a number", r"\frac{x}{2}"),
       ("La tercera part d'un nombre", "La tercera parte de un número", "A third of a number", r"\frac{x}{3}"),
       ("El quadrat d'un nombre", "El cuadrado de un número", "The square of a number", "x^2"),
       ("El cub d'un nombre", "El cubo de un número", "The cube of a number", "x^3"),
       ("El següent (consecutiu) d'un nombre", "El siguiente (consecutivo) de un número", "The next number", "x+1"),
       ("L'anterior d'un nombre", "El anterior de un número", "The previous number", "x-1"),
       ("Un nombre parell", "Un número par", "An even number", "2x"),
       ("Un nombre senar", "Un número impar", "An odd number", "2x+1"),
       ("L'oposat d'un nombre", "El opuesto de un número", "The opposite of a number", "-x"),
       ("El 20 % d'un nombre", "El 20 % de un número", "20 % of a number", r"0\dc2x"),
       ("La suma de dos nombres", "La suma de dos números", "The sum of two numbers", "x+y"),
       ("El producte de dos nombres", "El producto de dos números", "The product of two numbers", "x\\cdot y=xy")]
s1 = box('def', L('Què és el llenguatge algebraic?', '¿Qué es el lenguaje algebraico?', 'What is algebraic language?'),
  P(r"El <strong>llenguatge algebraic</strong> utilitza <strong>lletres</strong> (normalment \(x,\ y,\ a,\ b\ldots\)) per a representar nombres que no coneixem o que poden prendre qualsevol valor. Les lletres s'anomenen <strong>variables</strong> (o <strong>incògnites</strong> quan volem trobar-ne el valor).",
    r"El <strong>lenguaje algebraico</strong> utiliza <strong>letras</strong> (normalmente \(x,\ y,\ a,\ b\ldots\)) para representar números que no conocemos o que pueden tomar cualquier valor. Las letras se llaman <strong>variables</strong> (o <strong>incógnitas</strong> cuando queremos hallar su valor).",
    r"<strong>Algebraic language</strong> uses <strong>letters</strong> (usually \(x,\ y,\ a,\ b\ldots\)) to stand for numbers we don't know or that can take any value. The letters are called <strong>variables</strong> (or <strong>unknowns</strong> when we want to find their value).")
  + P(r"Una <strong>expressió algebraica</strong> és una combinació de nombres i lletres units per les operacions de sumar, restar, multiplicar, dividir i elevar a potències. Per exemple: \(\ 3x-5,\quad 2a+b^2,\quad \frac{x+1}{2}\).",
      r"Una <strong>expresión algebraica</strong> es una combinación de números y letras unidos por las operaciones de sumar, restar, multiplicar, dividir y elevar a potencias. Por ejemplo: \(\ 3x-5,\quad 2a+b^2,\quad \frac{x+1}{2}\).",
      r"An <strong>algebraic expression</strong> combines numbers and letters with addition, subtraction, multiplication, division and powers. For example: \(\ 3x-5,\quad 2a+b^2,\quad \frac{x+1}{2}\).")
  + P("Serveix per a:", "Sirve para:", "We use it to:")
  + ul(L(r"<strong>Expressar propietats generals</strong>: \(a+b=b+a\) és vàlid per a qualsevol parell de nombres.", r"<strong>Expresar propiedades generales</strong>: \(a+b=b+a\) es válido para cualquier par de números.", r"<strong>State general properties</strong>: \(a+b=b+a\) holds for any two numbers."),
       L(r"<strong>Escriure fórmules</strong>: l'àrea d'un rectangle és \(A=b\cdot h\); el perímetre d'un quadrat, \(P=4\ell\).", r"<strong>Escribir fórmulas</strong>: el área de un rectángulo es \(A=b\cdot h\); el perímetro de un cuadrado, \(P=4\ell\).", r"<strong>Write formulas</strong>: the area of a rectangle is \(A=b\cdot h\); the perimeter of a square is \(P=4\ell\)."),
       L(r"<strong>Plantejar equacions</strong> per a resoldre problemes (ho veurem a la unitat següent).", r"<strong>Plantear ecuaciones</strong> para resolver problemas (lo veremos en la unidad siguiente).", r"<strong>Set up equations</strong> to solve problems (next unit).")))
s1 += box('prop', L('Del llenguatge habitual al llenguatge algebraic', 'Del lenguaje habitual al lenguaje algebraico', 'From words to algebra'),
  '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>' + L('Enunciat', 'Enunciado', 'In words') + '</th><th>' + L('Expressió', 'Expresión', 'Expression') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td class="l">{L(va, es, en)}</td><td>\\({e}\\)</td></tr>' for va, es, en, e in TR1) + '</tbody></table></div>'
  + note(r"Convenis: el signe de multiplicar entre un nombre i una lletra (o entre lletres) no s'escriu, \(3\cdot x=3x\); i el 1 tampoc: \(1x=x\). Compte amb l'ordre: «el doble d'un nombre més 3» és \(2x+3\), però «el doble de la suma d'un nombre i 3» és \(2(x+3)\).",
         r"Convenios: el signo de multiplicar entre un número y una letra (o entre letras) no se escribe, \(3\cdot x=3x\); y el 1 tampoco: \(1x=x\). Cuidado con el orden: «el doble de un número más 3» es \(2x+3\), pero «el doble de la suma de un número y 3» es \(2(x+3)\).",
         r"Conventions: we don't write the multiplication sign between a number and a letter (or between letters), \(3\cdot x=3x\); nor the 1: \(1x=x\). Watch the order: “twice a number plus 3” is \(2x+3\), but “twice the sum of a number and 3” is \(2(x+3)\)."))
s1 += box('def', L("Valor numèric d'una expressió algebraica", 'Valor numérico de una expresión algebraica', 'Evaluating an expression'),
  P(r"El <strong>valor numèric</strong> d'una expressió algebraica és el nombre que obtenim quan <strong>substituïm</strong> les lletres per nombres concrets i fem les operacions (respectant la jerarquia).",
    r"El <strong>valor numérico</strong> de una expresión algebraica es el número que obtenemos cuando <strong>sustituimos</strong> las letras por números concretos y hacemos las operaciones (respetando la jerarquía).",
    r"The <strong>value</strong> of an algebraic expression is the number we get when we <strong>substitute</strong> numbers for the letters and work it out (in the right order of operations).")
  + D(r"3x^2-5x+1\quad\tri{per a}{para}{for}\ x=-2:\quad 3\cdot(-2)^2-5\cdot(-2)+1=12+10+1=23")
  + note(r"Quan substituïm un nombre negatiu, l'escrivim <strong>entre parèntesis</strong>: \((-2)^2=4\), en canvi \(-2^2=-4\).",
         r"Cuando sustituimos un número negativo, lo escribimos <strong>entre paréntesis</strong>: \((-2)^2=4\), en cambio \(-2^2=-4\).",
         r"When you substitute a negative number, write it <strong>in brackets</strong>: \((-2)^2=4\), whereas \(-2^2=-4\).", '⚠')
  + widget('w-val', '🔢', L('Calculadora de valor numèric', 'Calculadora de valor numérico', 'Expression evaluator'),
           ['<div class="wrow">' + tin('p', L('Expressió', 'Expresión', 'Expression'), '3x^2-5x+1') + tin('x', 'x =', '-2', 's') + tin('y', 'y =', '1', 's') + '</div>', HELP,
            quick([('3x^2-5x+1|-2|0', '3x²−5x+1'), ('2x^3-x|3|0', '2x³−x'), ('x^2+2xy-y^2|2|-3', 'x²+2xy−y²'), ('(x+1)/2|5|0', '(x+1)/2'), ('-x^2+4|-3|0', '−x²+4')])])
  + drill('lang', 'Entrena: del text a l\'expressió', 'Entrena: del texto a la expresión', 'Train: from words to algebra')
  + drill('val', 'Entrena: valor numèric', 'Entrena: valor numérico', 'Train: evaluating'))
chk('3*(-2)**2-5*(-2)+1', 23)
s1 += levels(
 [prob(L(r"Escriu en llenguatge algebraic: a) el doble d'un nombre menys 7; b) la meitat d'un nombre més la seua tercera part; c) el quadrat de la diferència de dos nombres.",
         r"Escribe en lenguaje algebraico: a) el doble de un número menos 7; b) la mitad de un número más su tercera parte; c) el cuadrado de la diferencia de dos números.",
         r"Write in algebra: a) twice a number minus 7; b) half a number plus a third of it; c) the square of the difference of two numbers."),
       D(r"\text{a)}\ \boxed{2x-7}\qquad \text{b)}\ \boxed{\frac{x}{2}+\frac{x}{3}}\qquad \text{c)}\ \boxed{(x-y)^2}"),
       P(r"Fixa't en c): primer restem i després elevem al quadrat. «La diferència dels quadrats» seria \(x^2-y^2\), que és una altra cosa.", r"Fíjate en c): primero restamos y después elevamos al cuadrado. «La diferencia de los cuadrados» sería \(x^2-y^2\), que es otra cosa.", r"Look at c): first subtract, then square. “The difference of the squares” would be \(x^2-y^2\), which is different.")),
  prob(L(r"Calcula el valor numèric de \(2x^2-3x+4\) per a \(x=3\) i per a \(x=-1\).", r"Calcula el valor numérico de \(2x^2-3x+4\) para \(x=3\) y para \(x=-1\).", r"Evaluate \(2x^2-3x+4\) for \(x=3\) and for \(x=-1\)."),
       D(r"x=3:\quad 2\cdot3^2-3\cdot3+4=18-9+4=\boxed{13}"),
       D(r"x=-1:\quad 2\cdot(-1)^2-3\cdot(-1)+4=2+3+4=\boxed{9}"))],
 [prob(L(r"Escriu l'expressió algebraica de: a) la suma de tres nombres consecutius; b) el perímetre i l'àrea d'un rectangle la base del qual fa 4 cm més que l'altura.",
         r"Escribe la expresión algebraica de: a) la suma de tres números consecutivos; b) el perímetro y el área de un rectángulo cuya base mide 4 cm más que la altura.",
         r"Write an expression for: a) the sum of three consecutive numbers; b) the perimeter and area of a rectangle whose base is 4 cm longer than its height."),
       D(r"\text{a)}\ x+(x+1)+(x+2)=\boxed{3x+3}"),
       P(r"b) Si l'altura és \(x\), la base és \(x+4\):", r"b) Si la altura es \(x\), la base es \(x+4\):", r"b) If the height is \(x\), the base is \(x+4\):") + D(r"P=2x+2(x+4)=\boxed{4x+8}\qquad A=\boxed{x(x+4)}")),
  prob(L(r"Una empresa de taxis cobra 3,50 € per baixada de bandera i 1,20 € per quilòmetre. Escriu l'expressió del preu d'un viatge de \(x\) km i calcula quant costa un viatge de 15 km.",
         r"Una empresa de taxis cobra 3,50 € por bajada de bandera y 1,20 € por kilómetro. Escribe la expresión del precio de un viaje de \(x\) km y calcula cuánto cuesta un viaje de 15 km.",
         r"A taxi firm charges €3.50 to start plus €1.20 per kilometre. Write an expression for the price of an \(x\) km trip and work out the cost of a 15 km trip."),
       D(r"\text{Preu}=1\dc20x+3\dc50"), D(r"x=15:\quad 1\dc20\cdot15+3\dc50=18+3\dc50=\boxed{21\dc50\ \text{€}}"))],
 [prob(L(r"Demostra que la suma de dos nombres senars qualssevol sempre és parell.", r"Demuestra que la suma de dos números impares cualesquiera siempre es par.", r"Show that the sum of any two odd numbers is always even."),
       P(r"Un nombre senar és \(2x+1\) i un altre (diferent) \(2y+1\):", r"Un número impar es \(2x+1\) y otro (distinto) \(2y+1\):", r"An odd number is \(2x+1\) and another one is \(2y+1\):")
       + D(r"(2x+1)+(2y+1)=2x+2y+2=2(x+y+1)"),
       P(r"És el doble d'un nombre enter, per tant <strong>és parell</strong>. Per això fem servir lletres: el raonament val per a <em>tots</em> els nombres alhora.", r"Es el doble de un número entero, por tanto <strong>es par</strong>. Por eso usamos letras: el razonamiento vale para <em>todos</em> los números a la vez.", r"It's twice a whole number, so <strong>it's even</strong>. That's why we use letters: the argument works for <em>all</em> numbers at once."))])
chk('x+(x+1)+(x+2)', '3x+3'); chk('2x+2(x+4)', '4x+8'); chk('(2x+1)+(2y+1)', '2(x+y+1)')
s1 += practice([
  ('★', L(r"Escriu en llenguatge algebraic: a) el triple d'un nombre més 5; b) un nombre menys la seua quarta part; c) el quadrat d'un nombre menys el seu doble.", r"Escribe en lenguaje algebraico: a) el triple de un número más 5; b) un número menos su cuarta parte; c) el cuadrado de un número menos su doble.", r"Write in algebra: a) three times a number plus 5; b) a number minus a quarter of it; c) the square of a number minus twice the number.")),
  ('★★', L(r"Calcula el valor numèric de d) \(x^3-2x+1\) per a \(x=-2\); e) \(3x^2y-xy^2\) per a \(x=1,\ y=-2\).", r"Calcula el valor numérico de d) \(x^3-2x+1\) para \(x=-2\); e) \(3x^2y-xy^2\) para \(x=1,\ y=-2\).", r"Evaluate d) \(x^3-2x+1\) for \(x=-2\); e) \(3x^2y-xy^2\) for \(x=1,\ y=-2\).")),
  ('★★★', L(r"f) L'Anna té \(x\) anys, el seu germà en té 3 menys i sa mare té el triple que l'Anna. Escriu la suma de les tres edats i la suma que tindran d'ací a 5 anys.", r"f) Ana tiene \(x\) años, su hermano tiene 3 menos y su madre tiene el triple que Ana. Escribe la suma de las tres edades y la suma que tendrán dentro de 5 años.", r"f) Anna is \(x\) years old, her brother is 3 years younger and her mother is three times Anna's age. Write the sum of the three ages and the sum in 5 years' time."))],
  D(r"\text{a)}\ 3x+5\qquad \text{b)}\ x-\frac{x}{4}\qquad \text{c)}\ x^2-2x")
  + D(r"\text{d)}\ (-2)^3-2\cdot(-2)+1=-8+4+1=-3\qquad \text{e)}\ 3\cdot1^2\cdot(-2)-1\cdot(-2)^2=-6-4=-10")
  + D(r"\text{f)}\ x+(x-3)+3x=5x-3;\qquad (x+5)+(x-3+5)+(3x+5)=5x+12"))
chk('(-2)**3-2*(-2)+1', -3); chk('3*1*(-2)-1*4', -10); chk('x+(x-3)+3x', '5x-3'); chk('(x+5)+(x+2)+(3x+5)', '5x+12')

# =====================================================================
# 4.2 Monomis
# =====================================================================
s2 = box('def', L('Monomi: coeficient, part literal i grau', 'Monomio: coeficiente, parte literal y grado', 'Monomials: coefficient, variable part and degree'),
  P(r"Un <strong>monomi</strong> és una expressió algebraica formada pel <strong>producte</strong> d'un nombre per una o més lletres elevades a exponents naturals. Té tres elements:",
    r"Un <strong>monomio</strong> es una expresión algebraica formada por el <strong>producto</strong> de un número por una o más letras elevadas a exponentes naturales. Tiene tres elementos:",
    r"A <strong>monomial</strong> is an algebraic expression made of the <strong>product</strong> of a number and one or more letters raised to whole-number powers. It has three parts:")
  + ul(L(r"El <strong>coeficient</strong>: el nombre (amb el seu signe).", r"El <strong>coeficiente</strong>: el número (con su signo).", r"The <strong>coefficient</strong>: the number (with its sign)."),
       L(r"La <strong>part literal</strong>: les lletres amb els seus exponents.", r"La <strong>parte literal</strong>: las letras con sus exponentes.", r"The <strong>variable part</strong>: the letters with their exponents."),
       L(r"El <strong>grau</strong>: la <strong>suma dels exponents</strong> de la part literal.", r"El <strong>grado</strong>: la <strong>suma de los exponentes</strong> de la parte literal.", r"The <strong>degree</strong>: the <strong>sum of the exponents</strong> of the variable part."))
  + D(r"\underbrace{-5}_{\tri{coeficient}{coeficiente}{coefficient}}\ \underbrace{x^{2}y}_{\tri{part literal}{parte literal}{variable part}}\qquad \tri{grau}{grado}{degree}=2+1=3")
  + '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>' + L('Monomi', 'Monomio', 'Monomial') + '</th><th>' + L('Coeficient', 'Coeficiente', 'Coefficient') + '</th><th>' + L('Part literal', 'Parte literal', 'Variable part') + '</th><th>' + L('Grau', 'Grado', 'Degree') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>\\({m}\\)</td><td>\\({c}\\)</td><td>\\({p}\\)</td><td>{g}</td></tr>' for m, c, p, g in [
      ('7x^4', '7', 'x^4', '4'), ('-a^2b^3', '-1', 'a^2b^3', '2 + 3 = 5'), ('x', '1', 'x', '1'), (r'\frac{3}{4}xyz', r'\frac{3}{4}', 'xyz', '1 + 1 + 1 = 3'), ('-6', '-6', '\\text{—}', '0')]) + '</tbody></table></div>'
  + note(r"Si no hi ha coeficient escrit, val 1 (\(x^2=1x^2\)); si només hi ha un signe menys, val \(-1\). Un nombre tot sol és un monomi de grau 0. També es parla del <strong>grau respecte d'una variable</strong>: \(-5x^2y\) té grau 2 respecte de \(x\) i grau 1 respecte de \(y\).",
         r"Si no hay coeficiente escrito, vale 1 (\(x^2=1x^2\)); si solo hay un signo menos, vale \(-1\). Un número solo es un monomio de grado 0. También se habla del <strong>grado respecto de una variable</strong>: \(-5x^2y\) tiene grado 2 respecto de \(x\) y grado 1 respecto de \(y\).",
         r"If no coefficient is written, it's 1 (\(x^2=1x^2\)); a lone minus sign means \(-1\). A number on its own is a monomial of degree 0. We also talk about the <strong>degree in one variable</strong>: \(-5x^2y\) has degree 2 in \(x\) and degree 1 in \(y\)."))
s2 += box('prop', L('Què <u>no</u> és un monomi', 'Qué <u>no</u> es un monomio', 'What is <u>not</u> a monomial'),
  ul(L(r"\(\dfrac{3}{x}=3x^{-1}\) o \(x^{-2}\): la lletra divideix (exponent negatiu).", r"\(\dfrac{3}{x}=3x^{-1}\) o \(x^{-2}\): la letra divide (exponente negativo).", r"\(\dfrac{3}{x}=3x^{-1}\) or \(x^{-2}\): the letter divides (negative exponent)."),
       L(r"\(\sqrt{x}\): l'exponent no és natural.", r"\(\sqrt{x}\): el exponente no es natural.", r"\(\sqrt{x}\): the exponent isn't a whole number."),
       L(r"\(2x+3\): té dos termes, és una suma (un polinomi).", r"\(2x+3\): tiene dos términos, es una suma (un polinomio).", r"\(2x+3\): it has two terms; it's a sum (a polynomial).")))
s2 += box('def', L('Monomis semblants', 'Monomios semejantes', 'Like terms'),
  P(r"Dos monomis són <strong>semblants</strong> si tenen <strong>la mateixa part literal</strong> (les mateixes lletres amb els mateixos exponents). Només es poden sumar i restar els monomis semblants.",
    r"Dos monomios son <strong>semejantes</strong> si tienen <strong>la misma parte literal</strong> (las mismas letras con los mismos exponentes). Solo se pueden sumar y restar los monomios semejantes.",
    r"Two monomials are <strong>like terms</strong> if they have <strong>the same variable part</strong> (same letters with the same exponents). Only like terms can be added and subtracted.")
  + D(r"3x^2y\ \ \tri{i}{y}{and}\ \ -\frac12x^2y\ \ \tri{són semblants}{son semejantes}{are like terms}\qquad 3x^2y\ \ \tri{i}{y}{and}\ \ 3xy^2\ \ \tri{no ho són}{no lo son}{are not}")
  + widget('w-mono', '🔎', L('Analitzador de monomis', 'Analizador de monomios', 'Monomial analyser'),
           ['<div class="wrow">' + tin('m', L('Monomi', 'Monomio', 'Monomial'), '-5x^2y') + '</div>', HELP,
            quick([('-5x^2y', '−5x²y'), ('3/4ab^3', '¾ab³'), ('x', 'x'), ('-x^3yz^2', '−x³yz²'), ('7', '7'), ('2x*3x^2', '2x·3x²'), ('4/x', '4/x'), ('2x+3', '2x+3')])], out='<div class="cards"></div>'))
s2 += levels(
 [prob(L(r"Indica el coeficient, la part literal i el grau de: \(\ -4x^3,\quad ab^2,\quad \frac{2}{5}x^2y^3,\quad -z\).", r"Indica el coeficiente, la parte literal y el grado de: \(\ -4x^3,\quad ab^2,\quad \frac{2}{5}x^2y^3,\quad -z\).", r"Give the coefficient, variable part and degree of: \(\ -4x^3,\quad ab^2,\quad \frac{2}{5}x^2y^3,\quad -z\)."),
       D(r"-4x^3:\ \ \text{coef. } -4,\ \ x^3,\ \ \text{grau } 3\qquad ab^2:\ \ \text{coef. } 1,\ \ ab^2,\ \ \text{grau } 3"),
       D(r"\tfrac{2}{5}x^2y^3:\ \ \text{coef. } \tfrac25,\ \ x^2y^3,\ \ \text{grau } 5\qquad -z:\ \ \text{coef. } -1,\ \ z,\ \ \text{grau } 1"))],
 [prob(L(r"Agrupa els monomis semblants: \(\ 3x^2,\ \ -xy,\ \ 5x,\ \ \frac12x^2,\ \ 4yx,\ \ -x,\ \ 2xy^2\).", r"Agrupa los monomios semejantes: \(\ 3x^2,\ \ -xy,\ \ 5x,\ \ \frac12x^2,\ \ 4yx,\ \ -x,\ \ 2xy^2\).", r"Group the like terms: \(\ 3x^2,\ \ -xy,\ \ 5x,\ \ \frac12x^2,\ \ 4yx,\ \ -x,\ \ 2xy^2\)."),
       D(r"\{3x^2,\ \tfrac12x^2\}\qquad \{-xy,\ 4yx\}\qquad \{5x,\ -x\}\qquad \{2xy^2\}"),
       P(r"Atenció: \(4yx=4xy\) (l'ordre de les lletres no importa), però \(2xy^2\) no és semblant a \(xy\): l'exponent de \(y\) és diferent.", r"Atención: \(4yx=4xy\) (el orden de las letras no importa), pero \(2xy^2\) no es semejante a \(xy\): el exponente de \(y\) es distinto.", r"Note: \(4yx=4xy\) (the order of letters doesn't matter), but \(2xy^2\) isn't a like term of \(xy\): the exponent of \(y\) differs."))],
 [prob(L(r"Escriu un monomi de grau 5, amb dues variables, coeficient \(-3\) i que tinga grau 2 respecte de \(y\). És únic?", r"Escribe un monomio de grado 5, con dos variables, coeficiente \(-3\) y que tenga grado 2 respecto de \(y\). ¿Es único?", r"Write a monomial of degree 5 in two variables, with coefficient \(-3\) and degree 2 in \(y\). Is it unique?"),
       P(r"Si l'exponent de \(y\) és 2, el de l'altra variable ha de ser \(5-2=3\):", r"Si el exponente de \(y\) es 2, el de la otra variable debe ser \(5-2=3\):", r"If \(y\) has exponent 2, the other variable needs \(5-2=3\):") + D(r"\boxed{-3x^3y^2}"),
       P(r"No és únic: l'altra lletra no ha de ser \(x\) per força (\(-3a^3y^2\) també compleix).", r"No es único: la otra letra no tiene por qué ser \(x\) (\(-3a^3y^2\) también cumple).", r"It isn't unique: the other letter doesn't have to be \(x\) (\(-3a^3y^2\) works too)."))])
s2 += practice([
  ('★', L(r"Coeficient, part literal i grau de: a) \(6x^2y\); b) \(-x^5\); c) \(\frac{3}{4}xz^3\); d) \(10\).", r"Coeficiente, parte literal y grado de: a) \(6x^2y\); b) \(-x^5\); c) \(\frac{3}{4}xz^3\); d) \(10\).", r"Coefficient, variable part and degree of: a) \(6x^2y\); b) \(-x^5\); c) \(\frac{3}{4}xz^3\); d) \(10\).")),
  ('★★', L(r"e) Quins són monomis? \(\ 3x^{-2},\ \ \frac{x^2}{5},\ \ \frac{5}{x^2},\ \ -\sqrt{2}\,x,\ \ x+x^2\). f) Escriu dos monomis semblants a \(-2x^3y\).", r"e) ¿Cuáles son monomios? \(\ 3x^{-2},\ \ \frac{x^2}{5},\ \ \frac{5}{x^2},\ \ -\sqrt{2}\,x,\ \ x+x^2\). f) Escribe dos monomios semejantes a \(-2x^3y\).", r"e) Which are monomials? \(\ 3x^{-2},\ \ \frac{x^2}{5},\ \ \frac{5}{x^2},\ \ -\sqrt{2}\,x,\ \ x+x^2\). f) Write two like terms of \(-2x^3y\).")),
  ('★★★', L(r"g) Troba \(k\) perquè \(4x^{k+1}y^3\) siga de grau 7. h) Quin valor té el monomi \(-2x^3y\) per a \(x=-1\), \(y=5\)?", r"g) Halla \(k\) para que \(4x^{k+1}y^3\) sea de grado 7. h) ¿Qué valor tiene el monomio \(-2x^3y\) para \(x=-1\), \(y=5\)?", r"g) Find \(k\) so that \(4x^{k+1}y^3\) has degree 7. h) What is the value of \(-2x^3y\) when \(x=-1\), \(y=5\)?"))],
  D(r"\text{a)}\ 6;\ x^2y;\ 3\qquad \text{b)}\ -1;\ x^5;\ 5\qquad \text{c)}\ \tfrac34;\ xz^3;\ 4\qquad \text{d)}\ 10;\ \text{—};\ 0")
  + P(r"e) Són monomis \(\frac{x^2}{5}=\frac15x^2\) i \(-\sqrt2\,x\) (el coeficient pot ser qualsevol nombre). No ho són \(3x^{-2}\), \(\frac{5}{x^2}\) ni \(x+x^2\). &nbsp; f) Per exemple \(5x^3y\) i \(\frac12x^3y\).",
      r"e) Son monomios \(\frac{x^2}{5}=\frac15x^2\) y \(-\sqrt2\,x\) (el coeficiente puede ser cualquier número). No lo son \(3x^{-2}\), \(\frac{5}{x^2}\) ni \(x+x^2\). &nbsp; f) Por ejemplo \(5x^3y\) y \(\frac12x^3y\).",
      r"e) \(\frac{x^2}{5}=\frac15x^2\) and \(-\sqrt2\,x\) are monomials (the coefficient can be any number). \(3x^{-2}\), \(\frac{5}{x^2}\) and \(x+x^2\) aren't. &nbsp; f) For example \(5x^3y\) and \(\frac12x^3y\).")
  + D(r"\text{g)}\ (k+1)+3=7\Rightarrow k=3\qquad \text{h)}\ -2\cdot(-1)^3\cdot5=10"))

# =====================================================================
# 4.3 Operacions amb monomis
# =====================================================================
s3 = box('def', L('Suma i resta de monomis', 'Suma y resta de monomios', 'Adding and subtracting monomials'),
  P(r"Només podem sumar o restar monomis <strong>semblants</strong>: sumem (o restem) els coeficients i deixem la <strong>mateixa part literal</strong>.",
    r"Solo podemos sumar o restar monomios <strong>semejantes</strong>: sumamos (o restamos) los coeficientes y dejamos la <strong>misma parte literal</strong>.",
    r"We can only add or subtract <strong>like terms</strong>: add (or subtract) the coefficients and keep <strong>the same variable part</strong>.")
  + D(r"5x^2+3x^2=(5+3)x^2=8x^2\qquad 4ab-7ab=-3ab")
  + P(r"Si no són semblants, la suma es deixa indicada: \(\ 5x^2+3x\) no es pot simplificar (és un polinomi).",
      r"Si no son semejantes, la suma se deja indicada: \(\ 5x^2+3x\) no se puede simplificar (es un polinomio).",
      r"If they aren't like terms, the sum stays as it is: \(\ 5x^2+3x\) can't be simplified (it's a polynomial).")
  + note(r"Error típic: \(5x^2+3x^2\neq 8x^4\). Quan sumem, els exponents <strong>no canvien</strong>.", r"Error típico: \(5x^2+3x^2\neq 8x^4\). Cuando sumamos, los exponentes <strong>no cambian</strong>.", r"Common mistake: \(5x^2+3x^2\neq 8x^4\). When adding, the exponents <strong>don't change</strong>.", '⚠'))
s3 += box('def', L('Producte i quocient de monomis', 'Producto y cociente de monomios', 'Multiplying and dividing monomials'),
  ul(L(r"<strong>Producte:</strong> multipliquem els coeficients i, per a cada lletra, <strong>sumem els exponents</strong> (\(x^m\cdot x^n=x^{m+n}\)). Es poden multiplicar monomis qualssevol, semblants o no.",
       r"<strong>Producto:</strong> multiplicamos los coeficientes y, para cada letra, <strong>sumamos los exponentes</strong> (\(x^m\cdot x^n=x^{m+n}\)). Se pueden multiplicar monomios cualesquiera, semejantes o no.",
       r"<strong>Product:</strong> multiply the coefficients and, for each letter, <strong>add the exponents</strong> (\(x^m\cdot x^n=x^{m+n}\)). Any two monomials can be multiplied."),
     L(r"<strong>Quocient:</strong> dividim els coeficients i, per a cada lletra, <strong>restem els exponents</strong> (\(x^m:x^n=x^{m-n}\)). El resultat només és un monomi si cap exponent queda negatiu.",
       r"<strong>Cociente:</strong> dividimos los coeficientes y, para cada letra, <strong>restamos los exponentes</strong> (\(x^m:x^n=x^{m-n}\)). El resultado solo es un monomio si ningún exponente queda negativo.",
       r"<strong>Quotient:</strong> divide the coefficients and, for each letter, <strong>subtract the exponents</strong> (\(x^m:x^n=x^{m-n}\)). The result is only a monomial if no exponent goes negative."),
     L(r"<strong>Potència:</strong> elevem el coeficient i <strong>multipliquem cada exponent</strong> (\((x^m)^n=x^{m\cdot n}\)).", r"<strong>Potencia:</strong> elevamos el coeficiente y <strong>multiplicamos cada exponente</strong> (\((x^m)^n=x^{m\cdot n}\)).", r"<strong>Power:</strong> raise the coefficient and <strong>multiply each exponent</strong> (\((x^m)^n=x^{m\cdot n}\))."))
  + D(r"(-3x^2y)\cdot(4xy^3)=-12x^{3}y^{4}\qquad 15x^5y^2:(3x^2y)=5x^3y\qquad (2x^3)^2=4x^6")
  + note(r"Recorda que \(x^0=1\): \(\ 6x^2y:(2x^2)=3x^0y=3y\).", r"Recuerda que \(x^0=1\): \(\ 6x^2y:(2x^2)=3x^0y=3y\).", r"Remember \(x^0=1\): \(\ 6x^2y:(2x^2)=3x^0y=3y\).")
  + widget('w-monops', '🧮', L('Operacions amb monomis pas a pas', 'Operaciones con monomios paso a paso', 'Monomial operations step by step'),
           ['<div class="wrow">' + tin('a', 'A =', '6x^3y', 's') + seg([('+', '+'), ('-', '−'), ('*', '·'), (':', ':')], '*') + tin('b', 'B =', '-2xy', 's') + '</div>', HELP,
            quick([('5x^2|3x^2|+', '5x² + 3x²'), ('4ab|7ab|-', '4ab − 7ab'), ('5x^2|3x|+', '5x² + 3x'), ('-3x^2y|4xy^3|*', '(−3x²y)·(4xy³)'), ('15x^5y^2|3x^2y|:', '15x⁵y² : 3x²y'), ('6x^2y|2x^2|:', '6x²y : 2x²'), ('4x^2|8x^3|:', '4x² : 8x³')])])
  + drill('mono', 'Entrena: operacions amb monomis', 'Entrena: operaciones con monomios', 'Train: monomial operations'))
for a_, b_ in [('(-3x^2y)*(4xy^3)', '-12x^3y^4'), ('(15x^5y^2)/(3x^2y)', '5x^3y'), ('(2x^3)^2', '4x^6')]: chk(a_, b_)
s3 += levels(
 [prob(L(r"Redueix: \(\ 3x-5x+7x\qquad 2a^2b+a^2b-6a^2b\qquad 4x^2-x+2x^2+3x\).", r"Reduce: \(\ 3x-5x+7x\qquad 2a^2b+a^2b-6a^2b\qquad 4x^2-x+2x^2+3x\).", r"Simplify: \(\ 3x-5x+7x\qquad 2a^2b+a^2b-6a^2b\qquad 4x^2-x+2x^2+3x\)."),
       D(r"3x-5x+7x=(3-5+7)x=\boxed{5x}\qquad 2a^2b+a^2b-6a^2b=\boxed{-3a^2b}"),
       P(r"En l'últim hi ha dos grups de semblants: els termes en \(x^2\) i els termes en \(x\).", r"En el último hay dos grupos de semejantes: los términos en \(x^2\) y los términos en \(x\).", r"The last one has two groups of like terms: the \(x^2\) terms and the \(x\) terms.") + D(r"(4x^2+2x^2)+(-x+3x)=\boxed{6x^2+2x}")),
  prob(L(r"Calcula: \(\ 2x^3\cdot5x^4\qquad (-6ab^2)\cdot\left(-\frac12a^3b\right)\).", r"Calcula: \(\ 2x^3\cdot5x^4\qquad (-6ab^2)\cdot\left(-\frac12a^3b\right)\).", r"Work out: \(\ 2x^3\cdot5x^4\qquad (-6ab^2)\cdot\left(-\frac12a^3b\right)\)."),
       D(r"2x^3\cdot5x^4=(2\cdot5)\,x^{3+4}=\boxed{10x^7}"), D(r"(-6ab^2)\cdot\left(-\tfrac12a^3b\right)=\left((-6)\cdot\left(-\tfrac12\right)\right)a^{1+3}b^{2+1}=\boxed{3a^4b^3}"))],
 [prob(L(r"Calcula: \(\ 20x^6y^3:(-4x^2y)\qquad 9a^4b^2:(6a^4b)\).", r"Calcula: \(\ 20x^6y^3:(-4x^2y)\qquad 9a^4b^2:(6a^4b)\).", r"Work out: \(\ 20x^6y^3:(-4x^2y)\qquad 9a^4b^2:(6a^4b)\)."),
       D(r"20x^6y^3:(-4x^2y)=(20:(-4))\,x^{6-2}y^{3-1}=\boxed{-5x^4y^2}"), D(r"9a^4b^2:(6a^4b)=\frac{9}{6}a^{0}b^{1}=\boxed{\frac32b}")),
  prob(L(r"Opera i redueix: \(\ 3x\cdot(-2x^2)+5x^4:x\).", r"Opera y reduce: \(\ 3x\cdot(-2x^2)+5x^4:x\).", r"Work out and simplify: \(\ 3x\cdot(-2x^2)+5x^4:x\)."),
       P(r"Primer els productes i quocients (jerarquia) i després sumem els semblants:", r"Primero los productos y cocientes (jerarquía) y después sumamos los semejantes:", r"First the products and quotients (order of operations), then add like terms:") + D(r"-6x^3+5x^3=\boxed{-x^3}"))],
 [prob(L(r"Simplifica: \(\ (2x^2y)^3:(4x^5y^2)-3xy\cdot x^0y^0\).", r"Simplifica: \(\ (2x^2y)^3:(4x^5y^2)-3xy\cdot x^0y^0\).", r"Simplify: \(\ (2x^2y)^3:(4x^5y^2)-3xy\cdot x^0y^0\)."),
       D(r"(2x^2y)^3=2^3x^{6}y^{3}=8x^6y^3"), D(r"8x^6y^3:(4x^5y^2)=2xy\qquad 3xy\cdot x^0y^0=3xy\cdot1=3xy"), D(r"2xy-3xy=\boxed{-xy}"))])
for a_, b_ in [('3x-5x+7x', '5x'), ('4x^2-x+2x^2+3x', '6x^2+2x'), ('2x^3*5x^4', '10x^7'), ('(-6x*y^2)*(-x^3*y/2)', '3x^4y^3'), ('20x^6y^3/(-4x^2y)', '-5x^4y^2'), ('3x*(-2x^2)+5x^4/x', '-x^3'), ('(2x^2y)^3/(4x^5y^2)-3xy', '-xy')]: chk(a_, b_)
s3 += practice([
  ('★', L(r"Redueix: a) \(7x^2-3x^2+x^2\); b) \(5xy-2x+3xy+6x\); c) \(2x\cdot(-3x^2)\cdot x\).", r"Reduce: a) \(7x^2-3x^2+x^2\); b) \(5xy-2x+3xy+6x\); c) \(2x\cdot(-3x^2)\cdot x\).", r"Simplify: a) \(7x^2-3x^2+x^2\); b) \(5xy-2x+3xy+6x\); c) \(2x\cdot(-3x^2)\cdot x\).")),
  ('★★', L(r"Calcula: d) \(-18x^5y^2:(6x^3y^2)\); e) \((-3x^2)^3\); f) \(12x^3:(8x)\).", r"Calcula: d) \(-18x^5y^2:(6x^3y^2)\); e) \((-3x^2)^3\); f) \(12x^3:(8x)\).", r"Work out: d) \(-18x^5y^2:(6x^3y^2)\); e) \((-3x^2)^3\); f) \(12x^3:(8x)\).")),
  ('★★★', L(r"g) Simplifica \(\ 4x^2\cdot3x-(6x^4:2x)+x\cdot x^2\). h) Per quin monomi hem de multiplicar \(-3x^2y\) per a obtindre \(12x^5y^3\)?", r"g) Simplifica \(\ 4x^2\cdot3x-(6x^4:2x)+x\cdot x^2\). h) ¿Por qué monomio hay que multiplicar \(-3x^2y\) para obtener \(12x^5y^3\)?", r"g) Simplify \(\ 4x^2\cdot3x-(6x^4:2x)+x\cdot x^2\). h) What monomial must we multiply \(-3x^2y\) by to get \(12x^5y^3\)?"))],
  D(r"\text{a)}\ 5x^2\qquad \text{b)}\ 8xy+4x\qquad \text{c)}\ -6x^4\qquad \text{d)}\ -3x^2\qquad \text{e)}\ -27x^6\qquad \text{f)}\ \tfrac32x^2")
  + D(r"\text{g)}\ 12x^3-3x^3+x^3=10x^3\qquad \text{h)}\ 12x^5y^3:(-3x^2y)=-4x^3y^2"))
for a_, b_ in [('7x^2-3x^2+x^2', '5x^2'), ('5xy-2x+3xy+6x', '8xy+4x'), ('2x*(-3x^2)*x', '-6x^4'), ('-18x^5y^2/(6x^3y^2)', '-3x^2'), ('(-3x^2)^3', '-27x^6'), ('12x^3/(8x)', '3x^2/2'), ('4x^2*3x-(6x^4/(2x))+x*x^2', '10x^3'), ('-3x^2y*(-4x^3y^2)', '12x^5y^3')]: chk(a_, b_)

# =====================================================================
# 4.4 Polinomis
# =====================================================================
s4 = box('def', L('Polinomis: termes, grau i variable', 'Polinomios: términos, grado y variable', 'Polynomials: terms, degree and variable'),
  P(r"Un <strong>polinomi</strong> és una suma de monomis no semblants. Cada monomi és un <strong>terme</strong> del polinomi. Si té dos termes es diu <strong>binomi</strong>; si en té tres, <strong>trinomi</strong>.",
    r"Un <strong>polinomio</strong> es una suma de monomios no semejantes. Cada monomio es un <strong>término</strong> del polinomio. Si tiene dos términos se llama <strong>binomio</strong>; si tiene tres, <strong>trinomio</strong>.",
    r"A <strong>polynomial</strong> is a sum of unlike monomials. Each monomial is a <strong>term</strong>. With two terms it's a <strong>binomial</strong>; with three, a <strong>trinomial</strong>.")
  + P(r"Els polinomis d'una sola <strong>variable</strong> (normalment \(x\)) s'escriuen \(P(x),\ Q(x)\ldots\) Per exemple:", r"Los polinomios de una sola <strong>variable</strong> (normalmente \(x\)) se escriben \(P(x),\ Q(x)\ldots\) Por ejemplo:", r"Polynomials in one <strong>variable</strong> (usually \(x\)) are written \(P(x),\ Q(x)\ldots\) For example:")
  + D(r"P(x)=\underbrace{4x^3}_{\tri{grau 3}{grado 3}{degree 3}}\underbrace{-2x^2}_{\tri{grau 2}{grado 2}{degree 2}}\underbrace{+x}_{\tri{grau 1}{grado 1}{degree 1}}\underbrace{-7}_{\tri{t. indep.}{t. indep.}{constant}}")
  + ul(L(r"<strong>Grau</strong> del polinomi: el grau més alt dels seus termes. \(P(x)\) té grau 3.", r"<strong>Grado</strong> del polinomio: el mayor grado de sus términos. \(P(x)\) tiene grado 3.", r"<strong>Degree</strong> of the polynomial: the highest degree of its terms. \(P(x)\) has degree 3."),
       L(r"<strong>Coeficient principal</strong>: el coeficient del terme de grau més alt (ací, 4).", r"<strong>Coeficiente principal</strong>: el coeficiente del término de mayor grado (aquí, 4).", r"<strong>Leading coefficient</strong>: the coefficient of the highest-degree term (here, 4)."),
       L(r"<strong>Terme independent</strong>: el terme sense lletra, de grau 0 (ací, \(-7\)).", r"<strong>Término independiente</strong>: el término sin letra, de grado 0 (aquí, \(-7\)).", r"<strong>Constant term</strong>: the term with no letter, of degree 0 (here, \(-7\))."),
       L(r"És <strong>ordenat</strong> si els termes van de major a menor grau, i <strong>complet</strong> si hi són tots els graus, des del grau del polinomi fins a 0. \(P(x)\) és ordenat i complet; \(x^4-3x+1\) no és complet (falten \(x^3\) i \(x^2\)).",
         r"Es <strong>ordenado</strong> si los términos van de mayor a menor grado, y <strong>completo</strong> si están todos los grados, desde el grado del polinomio hasta 0. \(P(x)\) es ordenado y completo; \(x^4-3x+1\) no es completo (faltan \(x^3\) y \(x^2\)).",
         r"It's <strong>in order</strong> if the terms go from highest to lowest degree, and <strong>complete</strong> if every degree from the top down to 0 appears. \(P(x)\) is in order and complete; \(x^4-3x+1\) isn't complete (no \(x^3\) or \(x^2\))."))
  + note(r"Si un polinomi té diverses variables, el grau de cada terme és la suma dels seus exponents: \(\ 3x^2y^3-xy+5\) té grau 5.", r"Si un polinomio tiene varias variables, el grado de cada término es la suma de sus exponentes: \(\ 3x^2y^3-xy+5\) tiene grado 5.", r"With several variables, each term's degree is the sum of its exponents: \(\ 3x^2y^3-xy+5\) has degree 5."))
s4 += box('def', L("Valor numèric d'un polinomi. Arrels", 'Valor numérico de un polinomio. Raíces', 'Value of a polynomial. Roots'),
  P(r"El <strong>valor numèric</strong> de \(P(x)\) per a \(x=a\) s'escriu \(P(a)\): substituïm \(x\) per \(a\). Si \(P(a)=0\), diem que \(a\) és una <strong>arrel</strong> (o zero) del polinomi.",
    r"El <strong>valor numérico</strong> de \(P(x)\) para \(x=a\) se escribe \(P(a)\): sustituimos \(x\) por \(a\). Si \(P(a)=0\), decimos que \(a\) es una <strong>raíz</strong> (o cero) del polinomio.",
    r"The <strong>value</strong> of \(P(x)\) at \(x=a\) is written \(P(a)\): substitute \(a\) for \(x\). If \(P(a)=0\), \(a\) is a <strong>root</strong> (or zero) of the polynomial.")
  + D(r"P(x)=x^2-5x+6:\qquad P(1)=1-5+6=2\qquad P(2)=4-10+6=0\ \Rightarrow\ x=2\ \tri{és una arrel}{es una raíz}{is a root}")
  + widget('w-poly', '🔬', L("Analitzador de polinomis", 'Analizador de polinomios', 'Polynomial analyser'),
           ['<div class="wrow">' + tin('p', 'P(x) =', '2x^3-x^5+7') + tin('a', L('Valor de x', 'Valor de x', 'Value of x'), '-1', 's') + '</div>', HELP,
            quick([('2x^3-x^5+7|-1', '2x³−x⁵+7'), ('4x^3-2x^2+x-7|2', '4x³−2x²+x−7'), ('x^2-5x+6|2', 'x²−5x+6'), ('x^4-3x+1|1', 'x⁴−3x+1'), ('3x-2x^2+x+5x^2|0', '3x−2x²+x+5x²')])], out='<div class="cards"></div><div class="hsteps"></div>'))
s4 += levels(
 [prob(L(r"Ordena el polinomi \(P(x)=5x-3x^4+2-x^2\) i indica'n el grau, el coeficient principal, el terme independent i si és complet.", r"Ordena el polinomio \(P(x)=5x-3x^4+2-x^2\) e indica su grado, el coeficiente principal, el término independiente y si es completo.", r"Put \(P(x)=5x-3x^4+2-x^2\) in order and give its degree, leading coefficient, constant term and whether it's complete."),
       D(r"P(x)=-3x^4-x^2+5x+2"),
       P(r"Grau 4, coeficient principal \(-3\), terme independent 2. No és complet: falta el terme en \(x^3\) (el podem escriure \(-3x^4+0x^3-x^2+5x+2\)).", r"Grado 4, coeficiente principal \(-3\), término independiente 2. No es completo: falta el término en \(x^3\) (lo podemos escribir \(-3x^4+0x^3-x^2+5x+2\)).", r"Degree 4, leading coefficient \(-3\), constant term 2. It isn't complete: there's no \(x^3\) term (we can write \(-3x^4+0x^3-x^2+5x+2\))."))],
 [prob(L(r"Si \(P(x)=2x^3-x^2+3\), calcula \(P(0)\), \(P(2)\) i \(P(-1)\).", r"Si \(P(x)=2x^3-x^2+3\), calcula \(P(0)\), \(P(2)\) y \(P(-1)\).", r"If \(P(x)=2x^3-x^2+3\), find \(P(0)\), \(P(2)\) and \(P(-1)\)."),
       D(r"P(0)=\boxed{3}\quad(\tri{el terme independent}{el término independiente}{the constant term})"),
       D(r"P(2)=2\cdot8-4+3=\boxed{15}\qquad P(-1)=2\cdot(-1)-1+3=\boxed{0}"),
       P(r"Com que \(P(-1)=0\), \(x=-1\) és una arrel de \(P\).", r"Como \(P(-1)=0\), \(x=-1\) es una raíz de \(P\).", r"Since \(P(-1)=0\), \(x=-1\) is a root of \(P\)."))],
 [prob(L(r"Troba \(m\) perquè el polinomi \(P(x)=x^3+mx^2-4\) complisca \(P(2)=12\).", r"Halla \(m\) para que el polinomio \(P(x)=x^3+mx^2-4\) cumpla \(P(2)=12\).", r"Find \(m\) so that \(P(x)=x^3+mx^2-4\) satisfies \(P(2)=12\)."),
       D(r"P(2)=8+4m-4=4+4m"), D(r"4+4m=12\ \Rightarrow\ 4m=8\ \Rightarrow\ \boxed{m=2}"))])
chk('2*8-4+3', 15); chk('2*(-1)-1+3', 0)
s4 += practice([
  ('★', L(r"Per a \(Q(x)=x^2-6+4x^3\): a) ordena'l; b) grau, coeficient principal i terme independent; c) és complet?", r"Para \(Q(x)=x^2-6+4x^3\): a) ordénalo; b) grado, coeficiente principal y término independiente; c) ¿es completo?", r"For \(Q(x)=x^2-6+4x^3\): a) put it in order; b) degree, leading coefficient and constant term; c) is it complete?")),
  ('★★', L(r"d) Calcula \(P(3)\) i \(P(-2)\) si \(P(x)=x^3-2x^2-x+2\). e) Quin és el grau de \(5x^2y^2-2xy^3+x^4y\)?", r"d) Calcula \(P(3)\) y \(P(-2)\) si \(P(x)=x^3-2x^2-x+2\). e) ¿Cuál es el grado de \(5x^2y^2-2xy^3+x^4y\)?", r"d) Find \(P(3)\) and \(P(-2)\) if \(P(x)=x^3-2x^2-x+2\). e) What is the degree of \(5x^2y^2-2xy^3+x^4y\)?")),
  ('★★★', L(r"f) Comprova si \(1\), \(-1\) i \(2\) són arrels de \(P(x)=x^3-2x^2-x+2\). g) Escriu un polinomi de grau 3, complet, amb coeficient principal \(-2\) i terme independent 5.", r"f) Comprueba si \(1\), \(-1\) y \(2\) son raíces de \(P(x)=x^3-2x^2-x+2\). g) Escribe un polinomio de grado 3, completo, con coeficiente principal \(-2\) y término independiente 5.", r"f) Check whether \(1\), \(-1\) and \(2\) are roots of \(P(x)=x^3-2x^2-x+2\). g) Write a complete degree-3 polynomial with leading coefficient \(-2\) and constant term 5."))],
  D(r"\text{a)}\ 4x^3+x^2-6\qquad \text{b)}\ 3;\ 4;\ -6\qquad \text{c)}\ \text{No (falta } x\text{)}")
  + D(r"\text{d)}\ P(3)=27-18-3+2=8;\quad P(-2)=-8-8+2+2=-12\qquad \text{e)}\ 5")
  + D(r"\text{f)}\ P(1)=0,\ P(-1)=0,\ P(2)=0:\ \text{les tres són arrels}\qquad \text{g)}\ \text{p. ex. } -2x^3+x^2-3x+5"))
for v_, r_ in [(3, 8), (-2, -12), (1, 0), (-1, 0), (2, 0)]: chk(f'({v_})**3-2*({v_})**2-({v_})+2', r_)

# =====================================================================
# 4.5 Suma i resta de polinomis
# =====================================================================
s5 = box('def', L('Suma i resta de polinomis', 'Suma y resta de polinomios', 'Adding and subtracting polynomials'),
  ul(L(r"<strong>Suma:</strong> ajuntem els dos polinomis i <strong>reduïm els termes semblants</strong>.", r"<strong>Suma:</strong> juntamos los dos polinomios y <strong>reducimos los términos semejantes</strong>.", r"<strong>Sum:</strong> put both polynomials together and <strong>collect like terms</strong>."),
     L(r"<strong>Resta:</strong> sumem l'<strong>oposat</strong> del segon: canviem el signe de <strong>tots</strong> els seus termes. \(\ P-Q=P+(-Q)\).", r"<strong>Resta:</strong> sumamos el <strong>opuesto</strong> del segundo: cambiamos el signo de <strong>todos</strong> sus términos. \(\ P-Q=P+(-Q)\).", r"<strong>Difference:</strong> add the <strong>opposite</strong> of the second: change the sign of <strong>every</strong> term. \(\ P-Q=P+(-Q)\)."))
  + P(r"Amb \(P(x)=3x^3-2x^2+5\) i \(Q(x)=x^3+4x^2-3x-1\), podem fer-ho en línia o col·locant els termes semblants en columna:", r"Con \(P(x)=3x^3-2x^2+5\) y \(Q(x)=x^3+4x^2-3x-1\), podemos hacerlo en línea o colocando los términos semejantes en columna:", r"With \(P(x)=3x^3-2x^2+5\) and \(Q(x)=x^3+4x^2-3x-1\), we can do it in a line or in columns of like terms:")
  + D(r"P+Q=(3x^3-2x^2+5)+(x^3+4x^2-3x-1)=4x^3+2x^2-3x+4")
  + D(r"P-Q=3x^3-2x^2+5-x^3-4x^2+3x+1=2x^3-6x^2+3x+6")
  + D(r"\begin{array}{rrrrr} & 3x^3 & -2x^2 & & +5\\ -Q: & -x^3 & -4x^2 & +3x & +1\\ \hline & 2x^3 & -6x^2 & +3x & +6\end{array}")
  + note(r"L'error més freqüent és canviar el signe només del primer terme quan restem: \(-(x^3+4x^2-3x-1)=-x^3-4x^2+3x+1\). El signe menys afecta <strong>tot</strong> el parèntesi.", r"El error más frecuente es cambiar el signo solo del primer término al restar: \(-(x^3+4x^2-3x-1)=-x^3-4x^2+3x+1\). El signo menos afecta a <strong>todo</strong> el paréntesis.", r"The most common mistake is changing the sign of only the first term: \(-(x^3+4x^2-3x-1)=-x^3-4x^2+3x+1\). The minus sign affects the <strong>whole</strong> bracket.", '⚠')
  + widget('w-addsub', '➕', L('Suma i resta en columna', 'Suma y resta en columna', 'Adding and subtracting in columns'),
           ['<div class="wrow">' + tin('p', 'P =', '3x^3-2x^2+5') + seg([('+', 'P + Q'), ('-', 'P − Q')], '+') + tin('q', 'Q =', 'x^3+4x^2-3x-1') + '</div>', HELP,
            quick([('3x^3-2x^2+5|x^3+4x^2-3x-1', 'P, Q'), ('x^2-3x+2|-x^2+5x-7', 'x²−3x+2, −x²+5x−7'), ('5x^4-x|2x^3+x-3', '5x⁴−x, 2x³+x−3'), ('2x^2y-xy+3|x^2y+4xy', '2x²y−xy+3, x²y+4xy')])])
  + drill('addsub', 'Entrena: suma i resta de polinomis', 'Entrena: suma y resta de polinomios', 'Train: adding and subtracting'))
chk('(3x^3-2x^2+5)+(x^3+4x^2-3x-1)', '4x^3+2x^2-3x+4'); chk('(3x^3-2x^2+5)-(x^3+4x^2-3x-1)', '2x^3-6x^2+3x+6')
s5 += levels(
 [prob(L(r"Siguen \(A(x)=2x^2-5x+3\) i \(B(x)=-x^2+2x-7\). Calcula \(A+B\).", r"Sean \(A(x)=2x^2-5x+3\) y \(B(x)=-x^2+2x-7\). Calcula \(A+B\).", r"Let \(A(x)=2x^2-5x+3\) and \(B(x)=-x^2+2x-7\). Find \(A+B\)."),
       D(r"(2x^2-x^2)+(-5x+2x)+(3-7)=\boxed{x^2-3x-4}"))],
 [prob(L(r"Amb els mateixos polinomis, calcula \(A-B\) i \(B-A\). Què observes?", r"Con los mismos polinomios, calcula \(A-B\) y \(B-A\). ¿Qué observas?", r"With the same polynomials, find \(A-B\) and \(B-A\). What do you notice?"),
       D(r"A-B=2x^2-5x+3+x^2-2x+7=\boxed{3x^2-7x+10}"), D(r"B-A=-x^2+2x-7-2x^2+5x-3=\boxed{-3x^2+7x-10}"),
       P(r"Són oposats: \(B-A=-(A-B)\). La resta no és commutativa.", r"Son opuestos: \(B-A=-(A-B)\). La resta no es conmutativa.", r"They're opposites: \(B-A=-(A-B)\). Subtraction isn't commutative."))],
 [prob(L(r"Si \(P(x)=x^3-2x+1\), \(Q(x)=3x^2+x\) i \(R(x)=x^3-x^2+4\), calcula \(P-(Q-R)\).", r"Si \(P(x)=x^3-2x+1\), \(Q(x)=3x^2+x\) y \(R(x)=x^3-x^2+4\), calcula \(P-(Q-R)\).", r"If \(P(x)=x^3-2x+1\), \(Q(x)=3x^2+x\) and \(R(x)=x^3-x^2+4\), find \(P-(Q-R)\)."),
       D(r"Q-R=3x^2+x-x^3+x^2-4=-x^3+4x^2+x-4"), D(r"P-(Q-R)=x^3-2x+1+x^3-4x^2-x+4=\boxed{2x^3-4x^2-3x+5}"))])
chk('(2x^2-5x+3)+(-x^2+2x-7)', 'x^2-3x-4'); chk('(2x^2-5x+3)-(-x^2+2x-7)', '3x^2-7x+10'); chk('(3x^2+x)-(x^3-x^2+4)', '-x^3+4x^2+x-4'); chk('(x^3-2x+1)-((3x^2+x)-(x^3-x^2+4))', '2x^3-4x^2-3x+5')
s5 += practice([
  ('★', L(r"Amb \(P(x)=4x^3-x+2\) i \(Q(x)=x^3+2x^2-5\), calcula a) \(P+Q\); b) \(P-Q\).", r"Con \(P(x)=4x^3-x+2\) y \(Q(x)=x^3+2x^2-5\), calcula a) \(P+Q\); b) \(P-Q\).", r"With \(P(x)=4x^3-x+2\) and \(Q(x)=x^3+2x^2-5\), find a) \(P+Q\); b) \(P-Q\).")),
  ('★★', L(r"c) \((5x^2-3xy+y^2)-(2x^2+xy-4y^2)\). d) Quin polinomi hem de sumar a \(x^2-3x\) per a obtindre \(4x^2+x-1\)?", r"c) \((5x^2-3xy+y^2)-(2x^2+xy-4y^2)\). d) ¿Qué polinomio hay que sumar a \(x^2-3x\) para obtener \(4x^2+x-1\)?", r"c) \((5x^2-3xy+y^2)-(2x^2+xy-4y^2)\). d) What polynomial must we add to \(x^2-3x\) to get \(4x^2+x-1\)?")),
  ('★★★', L(r"e) Amb els polinomis de l'exercici 1, calcula \(2P-3Q\).", r"e) Con los polinomios del ejercicio 1, calcula \(2P-3Q\).", r"e) With the polynomials from exercise 1, find \(2P-3Q\)."))],
  D(r"\text{a)}\ 5x^3+2x^2-x-3\qquad \text{b)}\ 3x^3-2x^2-x+7\qquad \text{c)}\ 3x^2-4xy+5y^2")
  + D(r"\text{d)}\ (4x^2+x-1)-(x^2-3x)=3x^2+4x-1\qquad \text{e)}\ 8x^3-2x+4-3x^3-6x^2+15=5x^3-6x^2-2x+19"))
for a_, b_ in [('(4x^3-x+2)+(x^3+2x^2-5)', '5x^3+2x^2-x-3'), ('(4x^3-x+2)-(x^3+2x^2-5)', '3x^3-2x^2-x+7'), ('(5x^2-3x*y+y^2)-(2x^2+x*y-4y^2)', '3x^2-4x*y+5y^2'), ('(4x^2+x-1)-(x^2-3x)', '3x^2+4x-1'), ('2(4x^3-x+2)-3(x^3+2x^2-5)', '5x^3-6x^2-2x+19')]: chk(a_, b_)

# =====================================================================
# 4.6 Producte de polinomis
# =====================================================================
s6 = box('def', L('Producte de polinomis', 'Producto de polinomios', 'Multiplying polynomials'),
  ul(L(r"<strong>Monomi per polinomi:</strong> multipliquem el monomi per <strong>cada terme</strong> del polinomi (propietat distributiva).", r"<strong>Monomio por polinomio:</strong> multiplicamos el monomio por <strong>cada término</strong> del polinomio (propiedad distributiva).", r"<strong>Monomial times polynomial:</strong> multiply the monomial by <strong>each term</strong> of the polynomial (distributive law)."),
     L(r"<strong>Polinomi per polinomi:</strong> multipliquem <strong>cada terme</strong> del primer per <strong>cada terme</strong> del segon i, després, reduïm els termes semblants.", r"<strong>Polinomio por polinomio:</strong> multiplicamos <strong>cada término</strong> del primero por <strong>cada término</strong> del segundo y, después, reducimos los términos semejantes.", r"<strong>Polynomial times polynomial:</strong> multiply <strong>each term</strong> of the first by <strong>each term</strong> of the second, then collect like terms."))
  + D(r"-2x\,(3x^2-x+4)=-6x^3+2x^2-8x")
  + D(r"(2x-3)(x^2+4x-1)=2x^3+8x^2-2x-3x^2-12x+3=2x^3+5x^2-14x+3")
  + P(r"També es pot fer com una multiplicació de nombres, en columna (posant els semblants un davall de l'altre):", r"También se puede hacer como una multiplicación de números, en columna (colocando los semejantes uno debajo del otro):", r"You can also set it out like long multiplication, in columns (like terms underneath each other):")
  + D(r"\begin{array}{rrrrr} & & x^2 & +4x & -1\\ & & & 2x & -3\\ \hline & & -3x^2 & -12x & +3\\ & 2x^3 & +8x^2 & -2x & \\ \hline & 2x^3 & +5x^2 & -14x & +3\end{array}")
  + note(r"El grau del producte és la <strong>suma dels graus</strong>: grau 1 per grau 2 dona grau 3. Si dos polinomis tenen \(m\) i \(n\) termes, abans de reduir n'obtenim \(m\cdot n\).", r"El grado del producto es la <strong>suma de los grados</strong>: grado 1 por grado 2 da grado 3. Si dos polinomios tienen \(m\) y \(n\) términos, antes de reducir obtenemos \(m\cdot n\).", r"The degree of the product is the <strong>sum of the degrees</strong>: degree 1 times degree 2 gives degree 3. If the polynomials have \(m\) and \(n\) terms, we get \(m\cdot n\) products before collecting.")
  + widget('w-mul', '✖', L('Producte amb taula', 'Producto con tabla', 'Multiplying with a grid'),
           ['<div class="wrow">' + tin('p', 'P =', '2x-3') + tin('q', 'Q =', 'x^2+4x-1') + '</div>', HELP,
            quick([('2x-3|x^2+4x-1', '(2x−3)(x²+4x−1)'), ('-2x|3x^2-x+4', '−2x·(3x²−x+4)'), ('x+2|x-5', '(x+2)(x−5)'), ('x^2-x+1|x^2+x+1', '(x²−x+1)(x²+x+1)'), ('3xy|2x-y+1', '3xy·(2x−y+1)')])])
  + drill('mul', 'Entrena: producte de polinomis', 'Entrena: producto de polinomios', 'Train: multiplying polynomials'))
chk('-2x(3x^2-x+4)', '-6x^3+2x^2-8x'); chk('(2x-3)(x^2+4x-1)', '2x^3+5x^2-14x+3')
s6 += levels(
 [prob(L(r"Calcula: \(\ 3x^2(2x^2-5x+1)\qquad -xy\,(4x-3y)\).", r"Calcula: \(\ 3x^2(2x^2-5x+1)\qquad -xy\,(4x-3y)\).", r"Work out: \(\ 3x^2(2x^2-5x+1)\qquad -xy\,(4x-3y)\)."),
       D(r"3x^2\cdot2x^2+3x^2\cdot(-5x)+3x^2\cdot1=\boxed{6x^4-15x^3+3x^2}"), D(r"-xy\cdot4x-xy\cdot(-3y)=\boxed{-4x^2y+3xy^2}")),
  prob(L(r"Multiplica \((x+4)(x-6)\).", r"Multiplica \((x+4)(x-6)\).", r"Multiply \((x+4)(x-6)\)."), D(r"x^2-6x+4x-24=\boxed{x^2-2x-24}"))],
 [prob(L(r"Calcula \((3x^2-x+2)(2x-5)\) i comprova que el grau és la suma dels graus.", r"Calcula \((3x^2-x+2)(2x-5)\) y comprueba que el grado es la suma de los grados.", r"Work out \((3x^2-x+2)(2x-5)\) and check that the degree is the sum of the degrees."),
       D(r"6x^3-15x^2-2x^2+5x+4x-10=\boxed{6x^3-17x^2+9x-10}"),
       P(r"Grau \(2+1=3\). ✓", r"Grado \(2+1=3\). ✓", r"Degree \(2+1=3\). ✓"))],
 [prob(L(r"Calcula \((x-1)(x+2)(x-3)\).", r"Calcula \((x-1)(x+2)(x-3)\).", r"Work out \((x-1)(x+2)(x-3)\)."),
       P(r"Multipliquem primer els dos primers i després pel tercer:", r"Multiplicamos primero los dos primeros y después por el tercero:", r"Multiply the first two, then multiply by the third:") + D(r"(x-1)(x+2)=x^2+x-2"),
       D(r"(x^2+x-2)(x-3)=x^3-3x^2+x^2-3x-2x+6=\boxed{x^3-2x^2-5x+6}"))])
for a_, b_ in [('3x^2(2x^2-5x+1)', '6x^4-15x^3+3x^2'), ('-x*y*(4x-3y)', '-4x^2*y+3x*y^2'), ('(x+4)(x-6)', 'x^2-2x-24'), ('(3x^2-x+2)(2x-5)', '6x^3-17x^2+9x-10'), ('(x-1)(x+2)(x-3)', 'x^3-2x^2-5x+6')]: chk(a_, b_)
s6 += practice([
  ('★', L(r"Calcula: a) \(-4x(x^3-2x+3)\); b) \((x+3)(x-7)\); c) \((2x+1)(3x-4)\).", r"Calcula: a) \(-4x(x^3-2x+3)\); b) \((x+3)(x-7)\); c) \((2x+1)(3x-4)\).", r"Work out: a) \(-4x(x^3-2x+3)\); b) \((x+3)(x-7)\); c) \((2x+1)(3x-4)\).")),
  ('★★', L(r"d) \((x^2-3x+2)(x+4)\); e) \((x^3-2x)(2x^2+x-1)\).", r"d) \((x^2-3x+2)(x+4)\); e) \((x^3-2x)(2x^2+x-1)\).", r"d) \((x^2-3x+2)(x+4)\); e) \((x^3-2x)(2x^2+x-1)\).")),
  ('★★★', L(r"f) Si \(P(x)=x^2-1\) i \(Q(x)=2x+3\), calcula \(P\cdot Q-3P\). g) Escriu l'àrea d'un rectangle de costats \(2x+1\) i \(x-3\) com un polinomi.", r"f) Si \(P(x)=x^2-1\) y \(Q(x)=2x+3\), calcula \(P\cdot Q-3P\). g) Escribe el área de un rectángulo de lados \(2x+1\) y \(x-3\) como un polinomio.", r"f) If \(P(x)=x^2-1\) and \(Q(x)=2x+3\), find \(P\cdot Q-3P\). g) Write the area of a rectangle with sides \(2x+1\) and \(x-3\) as a polynomial."))],
  D(r"\text{a)}\ -4x^4+8x^2-12x\qquad \text{b)}\ x^2-4x-21\qquad \text{c)}\ 6x^2-5x-4")
  + D(r"\text{d)}\ x^3+x^2-10x+8\qquad \text{e)}\ 2x^5+x^4-5x^3-2x^2+2x")
  + D(r"\text{f)}\ 2x^3+3x^2-2x-3-3x^2+3=2x^3-2x\qquad \text{g)}\ 2x^2-5x-3"))
for a_, b_ in [('-4x(x^3-2x+3)', '-4x^4+8x^2-12x'), ('(x+3)(x-7)', 'x^2-4x-21'), ('(2x+1)(3x-4)', '6x^2-5x-4'), ('(x^2-3x+2)(x+4)', 'x^3+x^2-10x+8'), ('(x^3-2x)(2x^2+x-1)', '2x^5+x^4-5x^3-2x^2+2x'), ('(x^2-1)(2x+3)-3(x^2-1)', '2x^3-2x'), ('(2x+1)(x-3)', '2x^2-5x-3')]: chk(a_, b_)

# =====================================================================
# 4.7 Identitats notables
# =====================================================================
s7 = box('def', L('Les tres identitats notables', 'Las tres identidades notables', 'The three special products'),
  P(r"Hi ha productes que apareixen tan sovint que convé saber-los de memòria. S'anomenen <strong>identitats notables</strong>:", r"Hay productos que aparecen tan a menudo que conviene sabérselos de memoria. Se llaman <strong>identidades notables</strong>:", r"Some products come up so often that it's worth knowing them by heart. They are the <strong>special products</strong> (identities):")
  + D(r"\boxed{(a+b)^2=a^2+2ab+b^2}\qquad \tri{quadrat d'una suma}{cuadrado de una suma}{square of a sum}")
  + D(r"\boxed{(a-b)^2=a^2-2ab+b^2}\qquad \tri{quadrat d'una diferència}{cuadrado de una diferencia}{square of a difference}")
  + D(r"\boxed{(a+b)(a-b)=a^2-b^2}\qquad \tri{suma per diferència}{suma por diferencia}{sum times difference}")
  + P(r"En paraules: «el quadrat del primer, més (o menys) el doble del primer pel segon, més el quadrat del segon» i «suma per diferència és igual a diferència de quadrats».", r"En palabras: «el cuadrado del primero, más (o menos) el doble del primero por el segundo, más el cuadrado del segundo» y «suma por diferencia es igual a diferencia de cuadrados».", r"In words: “first squared, plus (or minus) twice first times second, plus second squared” and “sum times difference equals the difference of the squares”.")
  + P(r"Les tres es demostren multiplicant: \((a+b)^2=(a+b)(a+b)=a^2+ab+ba+b^2=a^2+2ab+b^2\). I també es poden veure amb àrees:", r"Las tres se demuestran multiplicando: \((a+b)^2=(a+b)(a+b)=a^2+ab+ba+b^2=a^2+2ab+b^2\). Y también se pueden ver con áreas:", r"All three can be proved by multiplying: \((a+b)^2=(a+b)(a+b)=a^2+ab+ba+b^2=a^2+2ab+b^2\). You can also see them with areas:")
  + '<div class="figs"><figure>' + svg_sq() + '<figcaption>' + L("(a + b)² = a² + 2ab + b²", "(a + b)² = a² + 2ab + b²", "(a + b)² = a² + 2ab + b²") + '</figcaption></figure>' + svg_dif() + '</div>')
s7 += box('prop', L('Com aplicar-les', 'Cómo aplicarlas', 'How to use them'),
  P(r"Identifiquem qui fa de \(a\) i qui fa de \(b\) (poden ser monomis qualssevol) i substituïm, amb parèntesis:", r"Identificamos quién hace de \(a\) y quién de \(b\) (pueden ser monomios cualesquiera) y sustituimos, con paréntesis:", r"Decide what plays the role of \(a\) and of \(b\) (any monomials) and substitute, using brackets:")
  + D(r"(3x+2)^2=(3x)^2+2\cdot3x\cdot2+2^2=9x^2+12x+4")
  + D(r"(x^2-5)^2=(x^2)^2-2\cdot x^2\cdot5+5^2=x^4-10x^2+25")
  + D(r"(2x+3y)(2x-3y)=(2x)^2-(3y)^2=4x^2-9y^2")
  + note(r"Errors típics: \((x+3)^2\neq x^2+9\) (falta el doble producte) i \((3x)^2\neq3x^2\) (el 3 també s'eleva: \(9x^2\)).", r"Errores típicos: \((x+3)^2\neq x^2+9\) (falta el doble producto) y \((3x)^2\neq3x^2\) (el 3 también se eleva: \(9x^2\)).", r"Common mistakes: \((x+3)^2\neq x^2+9\) (the middle term is missing) and \((3x)^2\neq3x^2\) (the 3 is squared too: \(9x^2\)).", '⚠')
  + widget('w-id', '🟧', L('Desenvolupa una identitat notable', 'Desarrolla una identidad notable', 'Expand a special product'),
           ['<div class="wrow">' + seg([('sq+', '(a + b)²'), ('sq-', '(a − b)²'), ('dif', '(a + b)(a − b)')], 'sq+') + '</div>',
            '<div class="wrow">' + tin('a', 'a =', '3x', 's') + tin('b', 'b =', '2', 's') + '</div>',
            quick([('3x|2|sq+', '(3x+2)²'), ('x^2|5|sq-', '(x²−5)²'), ('2x|3y|dif', '(2x+3y)(2x−3y)'), ('x|1/2|sq+', '(x+½)²'), ('5|x|sq-', '(5−x)²')])])
  + drill('id', 'Entrena: identitats notables', 'Entrena: identidades notables', 'Train: special products'))
for a_, b_ in [('(3x+2)^2', '9x^2+12x+4'), ('(x^2-5)^2', 'x^4-10x^2+25'), ('(2x+3y)(2x-3y)', '4x^2-9y^2')]: chk(a_, b_)
s7 += levels(
 [prob(L(r"Desenvolupa: \(\ (x+5)^2\qquad (x-4)^2\qquad (x+6)(x-6)\).", r"Desarrolla: \(\ (x+5)^2\qquad (x-4)^2\qquad (x+6)(x-6)\).", r"Expand: \(\ (x+5)^2\qquad (x-4)^2\qquad (x+6)(x-6)\)."),
       D(r"(x+5)^2=x^2+2\cdot x\cdot5+25=\boxed{x^2+10x+25}"), D(r"(x-4)^2=x^2-8x+16\qquad (x+6)(x-6)=x^2-36"))],
 [prob(L(r"Desenvolupa: \(\ (2x-3)^2\qquad \left(x+\frac12\right)^2\qquad (5-3x)(5+3x)\).", r"Desarrolla: \(\ (2x-3)^2\qquad \left(x+\frac12\right)^2\qquad (5-3x)(5+3x)\).", r"Expand: \(\ (2x-3)^2\qquad \left(x+\frac12\right)^2\qquad (5-3x)(5+3x)\)."),
       D(r"(2x-3)^2=(2x)^2-2\cdot2x\cdot3+3^2=\boxed{4x^2-12x+9}"),
       D(r"\left(x+\tfrac12\right)^2=x^2+2\cdot x\cdot\tfrac12+\tfrac14=\boxed{x^2+x+\tfrac14}\qquad (5-3x)(5+3x)=\boxed{25-9x^2}"))],
 [prob(L(r"Escriu com a quadrat d'un binomi o com a producte: \(\ x^2+14x+49\qquad 9x^2-12x+4\qquad x^2-16\).", r"Escribe como cuadrado de un binomio o como producto: \(\ x^2+14x+49\qquad 9x^2-12x+4\qquad x^2-16\).", r"Write as the square of a binomial or as a product: \(\ x^2+14x+49\qquad 9x^2-12x+4\qquad x^2-16\)."),
       P(r"Llegim la identitat «al revés»: busquem dos quadrats i comprovem el doble producte.", r"Leemos la identidad «al revés»: buscamos dos cuadrados y comprobamos el doble producto.", r"Read the identity “backwards”: look for two squares and check the middle term."),
       D(r"x^2+14x+49=x^2+2\cdot x\cdot7+7^2=\boxed{(x+7)^2}"),
       D(r"9x^2-12x+4=(3x)^2-2\cdot3x\cdot2+2^2=\boxed{(3x-2)^2}\qquad x^2-16=\boxed{(x+4)(x-4)}"))])
for a_, b_ in [('(x+5)^2', 'x^2+10x+25'), ('(x-4)^2', 'x^2-8x+16'), ('(x+6)(x-6)', 'x^2-36'), ('(2x-3)^2', '4x^2-12x+9'), ('(x+1/2)^2', 'x^2+x+1/4'), ('(5-3x)(5+3x)', '25-9x^2'), ('(x+7)^2', 'x^2+14x+49'), ('(3x-2)^2', '9x^2-12x+4'), ('(x+4)(x-4)', 'x^2-16')]: chk(a_, b_)
s7 += practice([
  ('★', L(r"Desenvolupa: a) \((x+2)^2\); b) \((x-9)^2\); c) \((x+10)(x-10)\).", r"Desarrolla: a) \((x+2)^2\); b) \((x-9)^2\); c) \((x+10)(x-10)\).", r"Expand: a) \((x+2)^2\); b) \((x-9)^2\); c) \((x+10)(x-10)\).")),
  ('★★', L(r"d) \((4x+1)^2\); e) \((3x-2y)^2\); f) \((x^2+3)(x^2-3)\).", r"d) \((4x+1)^2\); e) \((3x-2y)^2\); f) \((x^2+3)(x^2-3)\).", r"d) \((4x+1)^2\); e) \((3x-2y)^2\); f) \((x^2+3)(x^2-3)\).")),
  ('★★★', L(r"Expressa com a identitat notable: g) \(x^2-10x+25\); h) \(4x^2-25\). i) Simplifica \((x+3)^2-(x-3)^2\).", r"Expresa como identidad notable: g) \(x^2-10x+25\); h) \(4x^2-25\). i) Simplifica \((x+3)^2-(x-3)^2\).", r"Write as a special product: g) \(x^2-10x+25\); h) \(4x^2-25\). i) Simplify \((x+3)^2-(x-3)^2\)."))],
  D(r"\text{a)}\ x^2+4x+4\qquad \text{b)}\ x^2-18x+81\qquad \text{c)}\ x^2-100")
  + D(r"\text{d)}\ 16x^2+8x+1\qquad \text{e)}\ 9x^2-12xy+4y^2\qquad \text{f)}\ x^4-9")
  + D(r"\text{g)}\ (x-5)^2\qquad \text{h)}\ (2x+5)(2x-5)\qquad \text{i)}\ x^2+6x+9-(x^2-6x+9)=12x"))
for a_, b_ in [('(x+2)^2', 'x^2+4x+4'), ('(x-9)^2', 'x^2-18x+81'), ('(x+10)(x-10)', 'x^2-100'), ('(4x+1)^2', '16x^2+8x+1'), ('(3x-2y)^2', '9x^2-12x*y+4y^2'), ('(x^2+3)(x^2-3)', 'x^4-9'), ('(x-5)^2', 'x^2-10x+25'), ('(2x+5)(2x-5)', '4x^2-25'), ('(x+3)^2-(x-3)^2', '12x')]: chk(a_, b_)

# =====================================================================
# 4.8 Extracció de factor comú
# =====================================================================
s8 = box('def', L('Traure factor comú', 'Sacar factor común', 'Taking out a common factor'),
  P(r"<strong>Traure factor comú</strong> és aplicar la propietat distributiva al revés: \(\ a\cdot b+a\cdot c=a\,(b+c)\). Transformem una suma en un <strong>producte</strong> (diem que <strong>factoritzem</strong>).",
    r"<strong>Sacar factor común</strong> es aplicar la propiedad distributiva al revés: \(\ a\cdot b+a\cdot c=a\,(b+c)\). Transformamos una suma en un <strong>producto</strong> (decimos que <strong>factorizamos</strong>).",
    r"<strong>Taking out a common factor</strong> is the distributive law backwards: \(\ a\cdot b+a\cdot c=a\,(b+c)\). We turn a sum into a <strong>product</strong> (we <strong>factorise</strong>).")
  + '<ol>' + ''.join('<li>' + t + '</li>' for t in [
      L(r"<strong>Part numèrica:</strong> el MCD dels coeficients.", r"<strong>Parte numérica:</strong> el MCD de los coeficientes.", r"<strong>Number part:</strong> the gcd of the coefficients."),
      L(r"<strong>Part literal:</strong> les lletres que apareixen en <strong>tots</strong> els termes, amb el <strong>menor exponent</strong>.", r"<strong>Parte literal:</strong> las letras que aparecen en <strong>todos</strong> los términos, con el <strong>menor exponente</strong>.", r"<strong>Variable part:</strong> the letters that appear in <strong>every</strong> term, with the <strong>lowest exponent</strong>."),
      L(r"Dins del parèntesi escrivim el resultat de <strong>dividir cada terme</strong> entre el factor comú.", r"Dentro del paréntesis escribimos el resultado de <strong>dividir cada término</strong> entre el factor común.", r"Inside the bracket write each term <strong>divided</strong> by the common factor.")]) + '</ol>'
  + D(r"12x^3-18x^2+6x=6x\,(2x^2-3x+1)")
  + P(r"Comprovació: si multipliquem \(6x\,(2x^2-3x+1)\) tornem al polinomi inicial. Fixa't que, com que \(6x:6x=1\), dins del parèntesi queda un 1 (no un 0!).", r"Comprobación: si multiplicamos \(6x\,(2x^2-3x+1)\) volvemos al polinomio inicial. Fíjate que, como \(6x:6x=1\), dentro del paréntesis queda un 1 (¡no un 0!).", r"Check: multiplying \(6x\,(2x^2-3x+1)\) gives back the original. Notice that \(6x:6x=1\), so a 1 (not a 0!) stays inside the bracket."))
s8 += box('prop', L('Factor comú i identitats notables', 'Factor común e identidades notables', 'Common factor and special products'),
  P(r"Per a <strong>factoritzar</strong> un polinomi del tot, primer traiem factor comú i després mirem si el que queda dins és una identitat notable:", r"Para <strong>factorizar</strong> un polinomio del todo, primero sacamos factor común y después miramos si lo que queda dentro es una identidad notable:", r"To <strong>factorise</strong> fully, first take out the common factor, then check whether what's left is a special product:")
  + D(r"x^3-9x=x\,(x^2-9)=x\,(x+3)(x-3)\qquad 2x^2+12x+18=2\,(x^2+6x+9)=2\,(x+3)^2")
  + widget('w-fc', '🧲', L('Traure factor comú pas a pas', 'Sacar factor común paso a paso', 'Taking out a common factor step by step'),
           ['<div class="wrow">' + tin('p', 'P =', '12x^3-18x^2+6x') + '</div>', HELP,
            quick([('12x^3-18x^2+6x', '12x³−18x²+6x'), ('6x^2y-9xy^2', '6x²y−9xy²'), ('x^3-9x', 'x³−9x'), ('2x^2+12x+18', '2x²+12x+18'), ('5x^4-20x^2', '5x⁴−20x²'), ('3x^2+5y', '3x²+5y')])])
  + drill('fc', 'Entrena: el factor comú', 'Entrena: el factor común', 'Train: the common factor'))
for a_, b_ in [('6x(2x^2-3x+1)', '12x^3-18x^2+6x'), ('x(x+3)(x-3)', 'x^3-9x'), ('2(x+3)^2', '2x^2+12x+18')]: chk(a_, b_)
s8 += levels(
 [prob(L(r"Trau factor comú: \(\ 5x^2-15x\qquad 8x^4+4x^3-12x^2\).", r"Saca factor común: \(\ 5x^2-15x\qquad 8x^4+4x^3-12x^2\).", r"Take out the common factor: \(\ 5x^2-15x\qquad 8x^4+4x^3-12x^2\)."),
       D(r"\text{MCD}(5,15)=5,\quad x^{\min(2,1)}=x\ \Rightarrow\ 5x^2-15x=\boxed{5x\,(x-3)}"),
       D(r"\text{MCD}(8,4,12)=4,\quad x^2\ \Rightarrow\ 8x^4+4x^3-12x^2=\boxed{4x^2\,(2x^2+x-3)}"))],
 [prob(L(r"Trau factor comú: \(\ 6x^2y^3-9xy^2+3xy\).", r"Saca factor común: \(\ 6x^2y^3-9xy^2+3xy\).", r"Take out the common factor: \(\ 6x^2y^3-9xy^2+3xy\)."),
       P(r"MCD\((6,9,3)=3\); \(x\) i \(y\) estan en tots els termes, amb exponent mínim 1:", r"MCD\((6,9,3)=3\); \(x\) e \(y\) están en todos los términos, con exponente mínimo 1:", r"gcd\((6,9,3)=3\); \(x\) and \(y\) are in every term, with lowest exponent 1:") + D(r"\boxed{3xy\,(2xy^2-3y+1)}")),
  prob(L(r"Trau factor comú un binomi: \(\ 2x(x-5)+3(x-5)\).", r"Saca factor común un binomio: \(\ 2x(x-5)+3(x-5)\).", r"Take out a common binomial: \(\ 2x(x-5)+3(x-5)\)."),
       P(r"El factor comú no ha de ser un monomi: ací tots dos termes tenen \((x-5)\).", r"El factor común no tiene por qué ser un monomio: aquí los dos términos tienen \((x-5)\).", r"The common factor needn't be a monomial: both terms contain \((x-5)\).") + D(r"\boxed{(x-5)(2x+3)}"))],
 [prob(L(r"Factoritza al màxim: \(\ 3x^3-12x\qquad x^4-2x^3+x^2\).", r"Factoriza al máximo: \(\ 3x^3-12x\qquad x^4-2x^3+x^2\).", r"Factorise fully: \(\ 3x^3-12x\qquad x^4-2x^3+x^2\)."),
       D(r"3x^3-12x=3x\,(x^2-4)=\boxed{3x\,(x+2)(x-2)}"),
       D(r"x^4-2x^3+x^2=x^2\,(x^2-2x+1)=\boxed{x^2\,(x-1)^2}"))])
for a_, b_ in [('5x(x-3)', '5x^2-15x'), ('4x^2(2x^2+x-3)', '8x^4+4x^3-12x^2'), ('3x*y*(2x*y^2-3y+1)', '6x^2*y^3-9x*y^2+3x*y'), ('(x-5)(2x+3)', '2x(x-5)+3(x-5)'), ('3x(x+2)(x-2)', '3x^3-12x'), ('x^2(x-1)^2', 'x^4-2x^3+x^2')]: chk(a_, b_)
s8 += practice([
  ('★', L(r"Trau factor comú: a) \(7x^2+14x\); b) \(x^3-4x^2+x\); c) \(10x^3y-15x^2y^2\).", r"Saca factor común: a) \(7x^2+14x\); b) \(x^3-4x^2+x\); c) \(10x^3y-15x^2y^2\).", r"Take out the common factor: a) \(7x^2+14x\); b) \(x^3-4x^2+x\); c) \(10x^3y-15x^2y^2\).")),
  ('★★', L(r"d) \(12x^4-8x^3+20x^2\); e) \(x(x+1)-4(x+1)\).", r"d) \(12x^4-8x^3+20x^2\); e) \(x(x+1)-4(x+1)\).", r"d) \(12x^4-8x^3+20x^2\); e) \(x(x+1)-4(x+1)\).")),
  ('★★★', L(r"Factoritza al màxim: f) \(2x^3-50x\); g) \(5x^3+30x^2+45x\); h) \(x^5-x^3\).", r"Factoriza al máximo: f) \(2x^3-50x\); g) \(5x^3+30x^2+45x\); h) \(x^5-x^3\).", r"Factorise fully: f) \(2x^3-50x\); g) \(5x^3+30x^2+45x\); h) \(x^5-x^3\)."))],
  D(r"\text{a)}\ 7x(x+2)\qquad \text{b)}\ x(x^2-4x+1)\qquad \text{c)}\ 5x^2y(2x-3y)")
  + D(r"\text{d)}\ 4x^2(3x^2-2x+5)\qquad \text{e)}\ (x+1)(x-4)")
  + D(r"\text{f)}\ 2x(x+5)(x-5)\qquad \text{g)}\ 5x(x+3)^2\qquad \text{h)}\ x^3(x+1)(x-1)"))
for a_, b_ in [('7x(x+2)', '7x^2+14x'), ('x(x^2-4x+1)', 'x^3-4x^2+x'), ('5x^2*y*(2x-3y)', '10x^3*y-15x^2*y^2'), ('4x^2(3x^2-2x+5)', '12x^4-8x^3+20x^2'), ('(x+1)(x-4)', 'x(x+1)-4(x+1)'), ('2x(x+5)(x-5)', '2x^3-50x'), ('5x(x+3)^2', '5x^3+30x^2+45x'), ('x^3(x+1)(x-1)', 'x^5-x^3')]: chk(a_, b_)

# =====================================================================
# 4.9 Divisió de polinomis
# =====================================================================
DA, DB = [2, -3, 0, 5, -1], [1, -1, 2]          # (2x^4-3x^3+5x-1):(x^2-x+2)
s9 = box('def', L('Divisió de polinomis', 'División de polinomios', 'Polynomial division'),
  P(r"Dividir \(D(x)\) (dividend) entre \(d(x)\) (divisor) és trobar el <strong>quocient</strong> \(C(x)\) i el <strong>residu</strong> \(R(x)\) tals que",
    r"Dividir \(D(x)\) (dividendo) entre \(d(x)\) (divisor) es hallar el <strong>cociente</strong> \(C(x)\) y el <strong>resto</strong> \(R(x)\) tales que",
    r"Dividing \(D(x)\) (dividend) by \(d(x)\) (divisor) means finding the <strong>quotient</strong> \(C(x)\) and the <strong>remainder</strong> \(R(x)\) such that")
  + D(r"\boxed{D(x)=d(x)\cdot C(x)+R(x)}\qquad \tri{amb}{con}{with}\ \ \text{grau}\,R<\text{grau}\,d")
  + P(r"Com amb els nombres, si el residu és 0 la divisió és <strong>exacta</strong> i \(d(x)\) és un divisor de \(D(x)\). Per a fer-la:", r"Como con los números, si el resto es 0 la división es <strong>exacta</strong> y \(d(x)\) es un divisor de \(D(x)\). Para hacerla:", r"As with numbers, if the remainder is 0 the division is <strong>exact</strong> and \(d(x)\) divides \(D(x)\). To do it:")
  + '<ol>' + ''.join('<li>' + t + '</li>' for t in [
      L(r"Ordenem dividend i divisor. Si al dividend li falta algun grau, deixem el buit (o hi posem 0).", r"Ordenamos dividendo y divisor. Si al dividendo le falta algún grado, dejamos el hueco (o ponemos 0).", r"Put both in order. If the dividend is missing a degree, leave a gap (or write 0)."),
      L(r"Dividim el <strong>primer terme</strong> del dividend entre el <strong>primer terme</strong> del divisor: és el primer terme del quocient.", r"Dividimos el <strong>primer término</strong> del dividendo entre el <strong>primer término</strong> del divisor: es el primer término del cociente.", r"Divide the <strong>first term</strong> of the dividend by the <strong>first term</strong> of the divisor: that's the first term of the quotient."),
      L(r"Multipliquem aquest terme per tot el divisor i ho escrivim davall <strong>canviat de signe</strong>; sumem.", r"Multiplicamos ese término por todo el divisor y lo escribimos debajo <strong>cambiado de signo</strong>; sumamos.", r"Multiply that term by the whole divisor, write it underneath <strong>with the signs changed</strong> and add."),
      L(r"Repetim amb el polinomi que ha quedat fins que el seu grau siga <strong>menor</strong> que el del divisor: aquest és el residu.", r"Repetimos con el polinomio que ha quedado hasta que su grado sea <strong>menor</strong> que el del divisor: ese es el resto.", r"Repeat with what's left until its degree is <strong>lower</strong> than the divisor's: that's the remainder.")]) + '</ol>'
  + P(r"Exemple: \(\ (2x^4-3x^3+5x-1):(x^2-x+2)\)", r"Ejemplo: \(\ (2x^4-3x^3+5x-1):(x^2-x+2)\)", r"Example: \(\ (2x^4-3x^3+5x-1):(x^2-x+2)\)")
  + ldiv_html(DA, DB)
  + D(r"C(x)=2x^2-x-5\qquad R(x)=2x+9")
  + P(r"Comprovació: \((x^2-x+2)(2x^2-x-5)+(2x+9)=2x^4-3x^3+5x-1\) ✓", r"Comprobación: \((x^2-x+2)(2x^2-x-5)+(2x+9)=2x^4-3x^3+5x-1\) ✓", r"Check: \((x^2-x+2)(2x^2-x-5)+(2x+9)=2x^4-3x^3+5x-1\) ✓")
  + widget('w-div', '➗', L('Divisió de polinomis pas a pas', 'División de polinomios paso a paso', 'Polynomial division step by step'),
           ['<div class="wrow">' + tin('p', 'D(x) =', '2x^4-3x^3+5x-1') + tin('q', 'd(x) =', 'x^2-x+2') + '</div>', HELP,
            quick([('2x^4-3x^3+5x-1|x^2-x+2', '(2x⁴−3x³+5x−1) : (x²−x+2)'), ('x^3-2x^2+4x-5|x-2', '(x³−2x²+4x−5) : (x−2)'), ('6x^3+x^2-4x+1|2x-1', '(6x³+x²−4x+1) : (2x−1)'), ('x^4-1|x^2+1', '(x⁴−1) : (x²+1)'), ('x^3+2x+3|x^2+x', '(x³+2x+3) : (x²+x)')])],
           out='<div class="ldiv-out"></div>' + STEPCTL + '<div class="hsteps"></div>'))
q_, r_ = sp.div(S('2x^4-3x^3+5x-1'), S('x^2-x+2'), x); assert sp.expand(q_ - S('2x^2-x-5')) == 0 and sp.expand(r_ - S('2x+9')) == 0
def dv(a_, b_, q2, r2):
    q_, r_ = sp.div(S(a_), S(b_), x); assert sp.expand(q_ - S(q2)) == 0 and sp.expand(r_ - S(r2)) == 0, (a_, b_, q_, r_)
s9 += levels(
 [prob(L(r"Divideix \(\ (x^3-2x^2+4x-5):(x-2)\).", r"Divide \(\ (x^3-2x^2+4x-5):(x-2)\).", r"Divide \(\ (x^3-2x^2+4x-5):(x-2)\)."),
       ldiv_html([1, -2, 4, -5], [1, -2]),
       D(r"C(x)=\boxed{x^2+4}\qquad R=\boxed{3}"),
       P(r"Comprovació: \((x-2)(x^2+4)+3=x^3+4x-2x^2-8+3\) ✓", r"Comprobación: \((x-2)(x^2+4)+3=x^3+4x-2x^2-8+3\) ✓", r"Check: \((x-2)(x^2+4)+3=x^3+4x-2x^2-8+3\) ✓"))],
 [prob(L(r"Divideix \(\ (6x^3+x^2-4x+1):(2x-1)\).", r"Divide \(\ (6x^3+x^2-4x+1):(2x-1)\).", r"Divide \(\ (6x^3+x^2-4x+1):(2x-1)\)."),
       ldiv_html([6, 1, -4, 1], [2, -1]),
       D(r"C(x)=\boxed{3x^2+2x-1}\qquad R=\boxed{0}"),
       P(r"La divisió és <strong>exacta</strong>: \(6x^3+x^2-4x+1=(2x-1)(3x^2+2x-1)\).", r"La división es <strong>exacta</strong>: \(6x^3+x^2-4x+1=(2x-1)(3x^2+2x-1)\).", r"The division is <strong>exact</strong>: \(6x^3+x^2-4x+1=(2x-1)(3x^2+2x-1)\)."))],
 [prob(L(r"Divideix \(\ (x^4-3x^2+2x):(x^2+x-1)\).", r"Divide \(\ (x^4-3x^2+2x):(x^2+x-1)\).", r"Divide \(\ (x^4-3x^2+2x):(x^2+x-1)\)."),
       P(r"Al dividend li falten els termes de grau 3 i 0: deixem els buits.", r"Al dividendo le faltan los términos de grado 3 y 0: dejamos los huecos.", r"The dividend has no degree-3 or degree-0 term: leave gaps."),
       ldiv_html([1, 0, -3, 2, 0], [1, 1, -1]),
       D(r"C(x)=\boxed{x^2-x-1}\qquad R(x)=\boxed{2x-1}"))])
dv('x^3-2x^2+4x-5', 'x-2', 'x^2+4', 3); dv('6x^3+x^2-4x+1', '2x-1', '3x^2+2x-1', 0); dv('x^4-3x^2+2x', 'x^2+x-1', 'x^2-x-1', '2x-1')
s9 += practice([
  ('★', L(r"Divideix: a) \((x^2+5x+7):(x+2)\); b) \((2x^3-x^2+3x-4):(x-1)\).", r"Divide: a) \((x^2+5x+7):(x+2)\); b) \((2x^3-x^2+3x-4):(x-1)\).", r"Divide: a) \((x^2+5x+7):(x+2)\); b) \((2x^3-x^2+3x-4):(x-1)\).")),
  ('★★', L(r"c) \((4x^3-2x+5):(2x+1)\); d) \((x^4+x^3-x+2):(x^2-x+1)\).", r"c) \((4x^3-2x+5):(2x+1)\); d) \((x^4+x^3-x+2):(x^2-x+1)\).", r"c) \((4x^3-2x+5):(2x+1)\); d) \((x^4+x^3-x+2):(x^2-x+1)\).")),
  ('★★★', L(r"e) En una divisió el divisor és \(x^2+1\), el quocient \(x-3\) i el residu \(2x\). Quin és el dividend? f) Comprova que \(x^2-x+3\) és divisor de \(x^4-x^3+2x^2+x-3\).", r"e) En una división el divisor es \(x^2+1\), el cociente \(x-3\) y el resto \(2x\). ¿Cuál es el dividendo? f) Comprueba que \(x^2-x+3\) es divisor de \(x^4-x^3+2x^2+x-3\).", r"e) In a division the divisor is \(x^2+1\), the quotient \(x-3\) and the remainder \(2x\). What is the dividend? f) Check that \(x^2-x+3\) divides \(x^4-x^3+2x^2+x-3\)."))],
  D(r"\text{a)}\ C=x+3,\ R=1\qquad \text{b)}\ C=2x^2+x+4,\ R=0")
  + D(r"\text{c)}\ C=2x^2-x-\tfrac12,\ R=\tfrac{11}{2}\qquad \text{d)}\ C=x^2+2x+1,\ R=-2x+1")
  + D(r"\text{e)}\ (x^2+1)(x-3)+2x=x^3-3x^2+3x-3\qquad \text{f)}\ C=x^2-1,\ R=0\ \checkmark"))
dv('x^2+5x+7', 'x+2', 'x+3', 1); dv('2x^3-x^2+3x-4', 'x-1', '2x^2+x+4', 0); dv('4x^3-2x+5', '2x+1', '2x^2-x-1/2', '11/2'); dv('x^4+x^3-x+2', 'x^2-x+1', 'x^2+2x+1', '-2x+1')
chk('(x^2+1)(x-3)+2x', 'x^3-3x^2+3x-3'); dv('x^4-x^3+2x^2+x-3', 'x^2-x+3', 'x^2-1', 0)

# =====================================================================
# 4.10 Regla de Ruffini
# =====================================================================
s10 = box('def', L('La regla de Ruffini', 'La regla de Ruffini', "Ruffini's rule"),
  P(r"Quan el divisor és de la forma \(\boldsymbol{x-a}\), podem fer la divisió molt més ràpid amb la <strong>regla de Ruffini</strong>, treballant només amb els coeficients. Exemple: \(\ (2x^3-5x^2+4):(x-3)\).",
    r"Cuando el divisor es de la forma \(\boldsymbol{x-a}\), podemos hacer la división mucho más rápido con la <strong>regla de Ruffini</strong>, trabajando solo con los coeficientes. Ejemplo: \(\ (2x^3-5x^2+4):(x-3)\).",
    r"When the divisor has the form \(\boldsymbol{x-a}\), we can divide much faster with <strong>Ruffini's rule</strong> (synthetic division), using only the coefficients. Example: \(\ (2x^3-5x^2+4):(x-3)\).")
  + '<ol>' + ''.join('<li>' + t + '</li>' for t in [
      L(r"Escrivim els coeficients del dividend <strong>ordenat i complet</strong> (amb 0 on falten termes): \(2,\ -5,\ 0,\ 4\).", r"Escribimos los coeficientes del dividendo <strong>ordenado y completo</strong> (con 0 donde faltan términos): \(2,\ -5,\ 0,\ 4\).", r"Write the coefficients of the dividend <strong>in order and complete</strong> (0 for missing terms): \(2,\ -5,\ 0,\ 4\)."),
      L(r"A l'esquerra posem \(a\). Compte amb el signe: per a \(x-3\) posem \(3\); per a \(x+2=x-(-2)\) posem \(-2\).", r"A la izquierda ponemos \(a\). Cuidado con el signo: para \(x-3\) ponemos \(3\); para \(x+2=x-(-2)\) ponemos \(-2\).", r"Put \(a\) on the left. Watch the sign: for \(x-3\) use \(3\); for \(x+2=x-(-2)\) use \(-2\)."),
      L(r"<strong>Baixem</strong> el primer coeficient. Després, repetim: <strong>multipliquem</strong> per \(a\), ho escrivim davall del coeficient següent i <strong>sumem</strong>.", r"<strong>Bajamos</strong> el primer coeficiente. Después, repetimos: <strong>multiplicamos</strong> por \(a\), lo escribimos debajo del coeficiente siguiente y <strong>sumamos</strong>.", r"<strong>Bring down</strong> the first coefficient. Then repeat: <strong>multiply</strong> by \(a\), write it under the next coefficient and <strong>add</strong>."),
      L(r"L'últim nombre és el <strong>residu</strong>; els altres són els coeficients del <strong>quocient</strong>, que té un grau menys que el dividend.", r"El último número es el <strong>resto</strong>; los demás son los coeficientes del <strong>cociente</strong>, que tiene un grado menos que el dividendo.", r"The last number is the <strong>remainder</strong>; the others are the coefficients of the <strong>quotient</strong>, one degree lower than the dividend.")]) + '</ol>'
  + ruf_html([2, -5, 0, 4], 3)
  + D(r"C(x)=2x^2+x+3\qquad R=13"))
s10 += box('prop', L('Teorema del residu', 'Teorema del resto', 'The remainder theorem'),
  P(r"El residu de dividir \(P(x)\) entre \(x-a\) és igual al valor numèric \(P(a)\):", r"El resto de dividir \(P(x)\) entre \(x-a\) es igual al valor numérico \(P(a)\):", r"The remainder when \(P(x)\) is divided by \(x-a\) equals the value \(P(a)\):")
  + D(r"\boxed{R=P(a)}\qquad P(3)=2\cdot27-5\cdot9+4=13\ \checkmark")
  + P(r"Per tant, si \(P(a)=0\) la divisió entre \(x-a\) és exacta: \(x=a\) és una <strong>arrel</strong> de \(P\) i \(x-a\) és un <strong>factor</strong>: \(P(x)=(x-a)\cdot C(x)\).", r"Por tanto, si \(P(a)=0\) la división entre \(x-a\) es exacta: \(x=a\) es una <strong>raíz</strong> de \(P\) y \(x-a\) es un <strong>factor</strong>: \(P(x)=(x-a)\cdot C(x)\).", r"So if \(P(a)=0\) the division by \(x-a\) is exact: \(x=a\) is a <strong>root</strong> of \(P\) and \(x-a\) is a <strong>factor</strong>: \(P(x)=(x-a)\cdot C(x)\).")
  + widget('w-ruf', '📐', L('Regla de Ruffini pas a pas', 'Regla de Ruffini paso a paso', "Ruffini's rule step by step"),
           ['<div class="wrow">' + tin('p', 'P(x) =', '2x^3-5x^2+4') + tin('q', L('Divisor', 'Divisor', 'Divisor'), 'x-3', 's') + '</div>', HELP,
            quick([('2x^3-5x^2+4|x-3', '(2x³−5x²+4) : (x−3)'), ('x^3-7x+6|x-2', '(x³−7x+6) : (x−2)'), ('x^4-1|x+1', '(x⁴−1) : (x+1)'), ('3x^3+2x^2-x+5|x+2', '(3x³+2x²−x+5) : (x+2)'), ('x^3-2x^2-5x+6|x-1', '(x³−2x²−5x+6) : (x−1)')])],
           out='<div class="ruf-out"></div>' + STEPCTL + '<div class="hsteps"></div>')
  + drill('ruf', 'Entrena: el residu', 'Entrena: el resto', 'Train: the remainder'))
dv('2x^3-5x^2+4', 'x-3', '2x^2+x+3', 13)
s10 += levels(
 [prob(L(r"Divideix per Ruffini \(\ (x^3+2x^2-5x-6):(x-2)\).", r"Divide por Ruffini \(\ (x^3+2x^2-5x-6):(x-2)\).", r"Use Ruffini's rule: \(\ (x^3+2x^2-5x-6):(x-2)\)."),
       ruf_html([1, 2, -5, -6], 2), D(r"C(x)=\boxed{x^2+4x+3}\qquad R=\boxed{0}"),
       P(r"Divisió exacta: \(x^3+2x^2-5x-6=(x-2)(x^2+4x+3)\).", r"División exacta: \(x^3+2x^2-5x-6=(x-2)(x^2+4x+3)\).", r"Exact division: \(x^3+2x^2-5x-6=(x-2)(x^2+4x+3)\)."))],
 [prob(L(r"Divideix per Ruffini \(\ (2x^4-3x^2+x-5):(x+1)\).", r"Divide por Ruffini \(\ (2x^4-3x^2+x-5):(x+1)\).", r"Use Ruffini's rule: \(\ (2x^4-3x^2+x-5):(x+1)\)."),
       P(r"Falta el terme en \(x^3\) (hi posem 0) i, com que \(x+1=x-(-1)\), a l'esquerra va \(-1\):", r"Falta el término en \(x^3\) (ponemos 0) y, como \(x+1=x-(-1)\), a la izquierda va \(-1\):", r"There's no \(x^3\) term (write 0) and, since \(x+1=x-(-1)\), \(-1\) goes on the left:"),
       ruf_html([2, 0, -3, 1, -5], -1), D(r"C(x)=\boxed{2x^3-2x^2-x+2}\qquad R=\boxed{-7}"),
       P(r"Comprovació amb el teorema del residu: \(P(-1)=2-3-1-5=-7\) ✓", r"Comprobación con el teorema del resto: \(P(-1)=2-3-1-5=-7\) ✓", r"Check with the remainder theorem: \(P(-1)=2-3-1-5=-7\) ✓"))],
 [prob(L(r"Troba \(k\) perquè la divisió \(\ (x^3-4x^2+kx+6):(x-3)\) siga exacta.", r"Halla \(k\) para que la división \(\ (x^3-4x^2+kx+6):(x-3)\) sea exacta.", r"Find \(k\) so that \(\ (x^3-4x^2+kx+6):(x-3)\) is exact."),
       P(r"Pel teorema del residu, cal que \(P(3)=0\):", r"Por el teorema del resto, hace falta que \(P(3)=0\):", r"By the remainder theorem we need \(P(3)=0\):"),
       D(r"P(3)=27-36+3k+6=3k-3=0\ \Rightarrow\ \boxed{k=1}"),
       P(r"Comprovació: \((x^3-4x^2+x+6):(x-3)\) dona \(C(x)=x^2-x-2\) i \(R=0\).", r"Comprobación: \((x^3-4x^2+x+6):(x-3)\) da \(C(x)=x^2-x-2\) y \(R=0\).", r"Check: \((x^3-4x^2+x+6):(x-3)\) gives \(C(x)=x^2-x-2\) and \(R=0\).") + ruf_html([1, -4, 1, 6], 3))])
dv('x^3+2x^2-5x-6', 'x-2', 'x^2+4x+3', 0); dv('2x^4-3x^2+x-5', 'x+1', '2x^3-2x^2-x+2', -7); dv('x^3-4x^2+x+6', 'x-3', 'x^2-x-2', 0)
s10 += practice([
  ('★', L(r"Divideix per Ruffini: a) \((x^3-3x^2+2x-4):(x-2)\); b) \((x^2+6x+5):(x+1)\).", r"Divide por Ruffini: a) \((x^3-3x^2+2x-4):(x-2)\); b) \((x^2+6x+5):(x+1)\).", r"Use Ruffini's rule: a) \((x^3-3x^2+2x-4):(x-2)\); b) \((x^2+6x+5):(x+1)\).")),
  ('★★', L(r"c) \((3x^4-x^3+2x-1):(x+2)\); d) \((x^5-32):(x-2)\). e) Calcula, sense dividir, el residu de \((x^{3}-5x+7):(x+3)\).", r"c) \((3x^4-x^3+2x-1):(x+2)\); d) \((x^5-32):(x-2)\). e) Calcula, sin dividir, el resto de \((x^{3}-5x+7):(x+3)\).", r"c) \((3x^4-x^3+2x-1):(x+2)\); d) \((x^5-32):(x-2)\). e) Without dividing, find the remainder of \((x^{3}-5x+7):(x+3)\).")),
  ('★★★', L(r"f) Troba \(m\) perquè \(x^3+mx^2-x+6\) siga divisible per \(x+2\). g) Comprova que \(x=1\) és arrel de \(x^3-2x^2-5x+6\) i descompon-lo en producte de tres factors de grau 1.", r"f) Halla \(m\) para que \(x^3+mx^2-x+6\) sea divisible por \(x+2\). g) Comprueba que \(x=1\) es raíz de \(x^3-2x^2-5x+6\) y descomponlo en producto de tres factores de grado 1.", r"f) Find \(m\) so that \(x^3+mx^2-x+6\) is divisible by \(x+2\). g) Check that \(x=1\) is a root of \(x^3-2x^2-5x+6\) and write it as a product of three linear factors."))],
  D(r"\text{a)}\ C=x^2-x,\ R=-4\qquad \text{b)}\ C=x+5,\ R=0")
  + D(r"\text{c)}\ C=3x^3-7x^2+14x-26,\ R=51\qquad \text{d)}\ C=x^4+2x^3+4x^2+8x+16,\ R=0\qquad \text{e)}\ R=P(-3)=-27+15+7=-5")
  + D(r"\text{f)}\ P(-2)=-8+4m+2+6=4m=0\Rightarrow m=0\qquad \text{g)}\ x^3-2x^2-5x+6=(x-1)(x^2-x-6)=(x-1)(x+2)(x-3)"))
dv('x^3-3x^2+2x-4', 'x-2', 'x^2-x', -4); dv('x^2+6x+5', 'x+1', 'x+5', 0); dv('3x^4-x^3+2x-1', 'x+2', '3x^3-7x^2+14x-26', 51); dv('x^5-32', 'x-2', 'x^4+2x^3+4x^2+8x+16', 0)
chk('(-3)**3-5*(-3)+7', -5); dv('x^3-x+6', 'x+2', 'x^2-2x+3', 0); chk('(x-1)(x+2)(x-3)', 'x^3-2x^2-5x+6')

# ============================================================ muntatge
SECS = [
  (L('Llenguatge algebraic', 'Lenguaje algebraico', 'Algebraic language'), s1),
  (L('Monomis', 'Monomios', 'Monomials'), s2),
  (L('Operacions amb monomis', 'Operaciones con monomios', 'Operations with monomials'), s3),
  (L('Polinomis', 'Polinomios', 'Polynomials'), s4),
  (L('Suma i resta de polinomis', 'Suma y resta de polinomios', 'Adding and subtracting polynomials'), s5),
  (L('Producte de polinomis', 'Producto de polinomios', 'Multiplying polynomials'), s6),
  (L('Identitats notables', 'Identidades notables', 'Special products'), s7),
  (L('Extracció de factor comú', 'Extracción de factor común', 'Taking out a common factor'), s8),
  (L('Divisió de polinomis', 'División de polinomios', 'Polynomial division'), s9),
  (L('Regla de Ruffini', 'Regla de Ruffini', "Ruffini's rule"), s10),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Polinomis · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 4 (Àlgebra: polinomis) de 3r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "x²";')
assert 'Polinomis · FentMates' in head and 'content: "x²"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
assert 'NSEC = %d' % NS in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">4.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../3eso.html">{L("3r ESO", "3º ESO", "3rd ESO (Year 9)")}</a> / {L("Unitat 4", "Unidad 4", "Unit 4")}</span>
    <span class="spacer"></span>
    <div class="lang-switch" role="group" aria-label="Idioma / Language">
      <button type="button" data-setlang="va">VA</button><button type="button" data-setlang="es">ES</button><button type="button" data-setlang="en">EN</button>
    </div>
    <button class="icon-btn" type="button" id="theme-btn" aria-label="Mode clar / fosc"></button>
  </div>
  <div class="progress" id="progress"></div>
</header>

<section class="hero">
  <div class="in">
    <span class="kicker">{L("Apunts de teoria · 3r ESO · Matemàtiques", "Apuntes de teoría · 3º ESO · Matemáticas", "Theory notes · 3rd ESO · Mathematics")}</span>
    <h1><span class="u">{L("Unitat 4", "Unidad 4", "Unit 4")}</span> · {L("Àlgebra: polinomis", "Álgebra: polinomios", "Algebra: polynomials")}</h1>
    <p>{L("Llenguatge algebraic, monomis i les seues operacions, polinomis, suma, resta i producte, identitats notables, factor comú, divisió de polinomis i regla de Ruffini: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Lenguaje algebraico, monomios y sus operaciones, polinomios, suma, resta y producto, identidades notables, factor común, división de polinomios y regla de Ruffini: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Algebraic language, monomials and their operations, polynomials, adding, subtracting and multiplying, special products, common factors, polynomial division and Ruffini's rule: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
    <div class="chips"><span>{L(f"{NS} apartats", f"{NS} apartados", f"{NS} sections")}</span><span>{L(f"{ntools} eines interactives", f"{ntools} herramientas interactivas", f"{ntools} interactive tools")}</span><span>{L("Problemes per nivells ★☆☆ → ★★★", "Problemas por niveles ★☆☆ → ★★★", "Problems by level ★☆☆ → ★★★")}</span><span>{L("Autoavaluació final", "Autoevaluación final", "Final self-check")}</span></div>
  </div>
</section>

<div class="layout">
  <nav class="toc" aria-label="Índex">
    <details open id="toc-d">
      <summary>{L("Índex", "Índice", "Contents")}</summary>
      <ol id="toc-list">
{toc}        <li><a href="#quiz"><span class="n">?</span>{L("Autoavaluació", "Autoevaluación", "Self-check")}</a></li>
      </ol>
      <div class="meter"><i id="meter"></i></div>
      <div class="meter-l"><span id="meter-n">0</span>/{NS} {L("apartats estudiats", "apartados estudiados", "sections studied")}</div>
    </details>
  </nav>

<article>
{''.join(sec(i, t, b) for i, (t, b) in enumerate(SECS, 1))}
<!-- ======================= QUIZ ======================= -->
<section class="unit quiz-sec" id="quiz">
  <div class="sec-head"><span class="num">?</span><h2>{L("Autoavaluació", "Autoevaluación", "Self-check")}</h2></div>
  {P("Respon i comprova a l'instant si ho has entés. Les preguntes van de més fàcils a més difícils.", "Responde y comprueba al instante si lo has entendido. Las preguntas van de más fáciles a más difíciles.", "Answer and instantly check whether you've understood. The questions go from easier to harder.")}
  <div class="quiz" id="quiz-box"></div>
  <div class="score" id="quiz-score"></div>
  <button class="btn" type="button" id="quiz-reset">↺ {L("Torna a començar", "Volver a empezar", "Start again")}</button>
</section>

</article>
</div>

<footer class="foot">
  <p>{L("Apunts de teoria · Unitat 4: Àlgebra · 3r ESO", "Apuntes de teoría · Unidad 4: Álgebra · 3º ESO", "Theory notes · Unit 4: Algebra · 3rd ESO")}</p>
  <p><a href="../../index.html">FentMates</a> · {L("Fet amb ♥ per a l'alumnat", "Hecho con ♥ para el alumnado", "Made with ♥ for students")}</p>
</footer>
<button class="icon-btn to-top" type="button" id="to-top" aria-label="↑">↑</button>

<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/katex.min.js"></script>
<script defer src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.16.9/contrib/auto-render.min.js"></script>
<script>
{js}</script>
</body>
</html>
'''
html = head + '\n' + css + '\n' + wide + '\n</style>\n</head>\n' + body
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, 'w', encoding='utf-8').write(html)
print('ok', OUT, len(html.split('\n')), 'lines,', ntools, 'tools')

sys.path.insert(0, os.path.dirname(HERE))
import relabel
print('\n'.join(relabel.fix_file(OUT)))

# FentMates: enllaça el tema comú (logo i colors del bloc) només a aquesta pàgina; aplica.py sencer
# reescriuria la versió de totes les altres pàgines de materials/.
import importlib.util as _ilu
_d = os.path.dirname(HERE)
while os.path.basename(_d) != "_eines":
    _d = os.path.dirname(_d)
_sp = _ilu.spec_from_file_location("aplica", os.path.join(_d, "tema", "aplica.py"))
_tema = _ilu.module_from_spec(_sp); _sp.loader.exec_module(_tema)
_tema.VERSION = "20261030a"
_tema.aplica_fitxer(OUT)
