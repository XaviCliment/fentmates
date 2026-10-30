import os, re, sys
from fractions import Fraction as Fr
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

# Genera materials/3eso/t5-equacions.html. Ús: python3 _eines/apunts/3eso-t5/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
# Les solucions de totes les equacions resoltes es comproven amb sympy (ce).
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/3eso/t5-equacions.html")

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
    return (f'\n<!-- ======================= 5.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">5.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def D(s): return r'\[' + s + r'\]'
def Lt(va, es, en): return r'\tri{%s}{%s}{%s}' % (va, es, en)

# ---------- ginys ----------
def drill(kind, va, es, en, hint=''):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  {hint}<div class="info" aria-live="polite"></div>
</div>
'''
SETHINT = '<p class="hint-s">' + L("Si hi ha més d'una solució, separa-les amb punt i coma (3; −2). Si no en té, escriu «cap».", "Si hay más de una solución, sepáralas con punto y coma (3; −2). Si no tiene, escribe «ninguna».", "If there is more than one solution, separate them with semicolons (3; −2). If there is none, type “none”.") + '</p>'
def quick(pairs):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-b="{v}">{t}</button>' for v, t in pairs) + '</div>'
def tin(k, lab, val, cls='w'):
    return f'<label>{lab} <input class="tin {cls}" type="text" inputmode="text" data-k="{k}" value="{val}" autocomplete="off" spellcheck="false" autocapitalize="off" aria-label="{k}"></label>'
def rng(k, lab, lo, hi, val):
    return f'<label>{lab} <input type="range" min="{lo}" max="{hi}" step="1" value="{val}" data-k="{k}"> <strong class="rv" data-v="{k}">{val}</strong></label>'
def widget(wid, icon, title, rows, out='<div class="hsteps"></div>', extra_cls=''):
    return (f'<div class="widget{extra_cls}" id="{wid}">\n  <div class="wt">{icon} {title}</div>\n'
            + ''.join(f'  {r}\n' for r in rows) + f'  {out}\n  <div class="info" aria-live="polite"></div>\n</div>\n')
HELP = '<p class="hint-s">' + L("Escriu l'equació amb el signe =. Potències amb ^ (x^2), fraccions amb / ((x+1)/2) i el producte amb * o sense signe (3x).", "Escribe la ecuación con el signo =. Potencias con ^ (x^2), fracciones con / ((x+1)/2) y el producto con * o sin signo (3x).", "Type the equation with an = sign. Powers with ^ (x^2), fractions with / ((x+1)/2) and products with * or no sign (3x).") + '</p>'

# ---------- comprovació amb sympy ----------
x = sp.symbols('x')
TR = standard_transformations + (implicit_multiplication_application, convert_xor)
def S(s): return parse_expr(s, transformations=TR, local_dict={'x': x}) if isinstance(s, str) else s
def chk(lhs, rhs):
    assert sp.expand(S(lhs) - S(rhs)) == 0, (lhs, rhs, sp.expand(S(lhs)))
def ce(eq, sols):
    """comprova les solucions reals d'una equació: sols = llista, 'totes' (identitat) o [] (cap)"""
    l, r = eq.split('=')
    e = sp.expand(S(l) - S(r))
    if sols == 'totes':
        assert e == 0, (eq, e); return
    assert e != 0, eq
    got = sorted(set(v for v in sp.solve(e, x) if v.is_real), key=float)
    want = sorted(set(sp.nsimplify(S(v) if isinstance(v, str) else sp.Rational(v)) for v in sols), key=float)
    assert got == want, (eq, got, want)

# ---------- taules de Ruffini (HTML) ----------
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
    assert b[-1] == 0, (cs, a)
    return '<div class="mfig"><table class="ruf"><tbody><tr>%s</tr><tr>%s</tr><tr class="rb">%s</tr></tbody></table></div>' % (r1, r2, r3)

# =====================================================================
# 5.1 Equacions i identitats
# =====================================================================
s1 = box('def', L('Igualtats algebraiques: identitats i equacions', 'Igualdades algebraicas: identidades y ecuaciones', 'Algebraic equalities: identities and equations'),
  P(r"Una <strong>igualtat algebraica</strong> està formada per dues expressions algebraiques unides pel signe \(=\). N'hi ha de dos tipus:",
    r"Una <strong>igualdad algebraica</strong> está formada por dos expresiones algebraicas unidas por el signo \(=\). Las hay de dos tipos:",
    r"An <strong>algebraic equality</strong> is made of two algebraic expressions joined by an \(=\) sign. There are two kinds:")
  + ul(L(r"Una <strong>identitat</strong> és una igualtat que es compleix per a <strong>qualsevol valor</strong> de les lletres. Per exemple, \(2(x+3)=2x+6\) o \((x+1)^2=x^2+2x+1\).",
         r"Una <strong>identidad</strong> es una igualdad que se cumple para <strong>cualquier valor</strong> de las letras. Por ejemplo, \(2(x+3)=2x+6\) o \((x+1)^2=x^2+2x+1\).",
         r"An <strong>identity</strong> is an equality that holds for <strong>every value</strong> of the letters. For example, \(2(x+3)=2x+6\) or \((x+1)^2=x^2+2x+1\)."),
       L(r"Una <strong>equació</strong> és una igualtat que només es compleix per a <strong>alguns valors</strong> (o per a cap). Per exemple, \(2x+3=11\) només és certa si \(x=4\).",
         r"Una <strong>ecuación</strong> es una igualdad que solo se cumple para <strong>algunos valores</strong> (o para ninguno). Por ejemplo, \(2x+3=11\) solo es cierta si \(x=4\).",
         r"An <strong>equation</strong> is an equality that only holds for <strong>some values</strong> (or none). For example, \(2x+3=11\) is only true when \(x=4\)."))
  + note(r"Per a saber si una igualtat és una identitat, operem i simplifiquem cada membre: si queden <strong>exactament iguals</strong>, és una identitat. Les identitats notables de la unitat anterior en són exemples.",
         r"Para saber si una igualdad es una identidad, operamos y simplificamos cada miembro: si quedan <strong>exactamente iguales</strong>, es una identidad. Las identidades notables de la unidad anterior son ejemplos.",
         r"To tell whether an equality is an identity, work out and simplify each side: if they end up <strong>exactly the same</strong>, it's an identity. The special products from the last unit are examples."))
s1 += box('def', L("Elements d'una equació", 'Elementos de una ecuación', 'Parts of an equation'),
  D(r"\underbrace{3x^2-5}_{\text{%s}}=\underbrace{2x+3}_{\text{%s}}" % (Lt('1r membre', '1.er miembro', 'left side'), Lt('2n membre', '2.º miembro', 'right side')))
  + ul(L(r"Els <strong>membres</strong> són les expressions que hi ha a cada costat del signe igual: el <strong>primer membre</strong> (a l'esquerra) i el <strong>segon membre</strong> (a la dreta).", r"Los <strong>miembros</strong> son las expresiones que hay a cada lado del signo igual: el <strong>primer miembro</strong> (a la izquierda) y el <strong>segundo miembro</strong> (a la derecha).", r"The <strong>sides</strong> are the expressions on each side of the equals sign: the <strong>left-hand side</strong> and the <strong>right-hand side</strong>."),
       L(r"Els <strong>termes</strong> són cadascun dels sumands: \(3x^2,\ -5,\ 2x,\ 3\). Els que no tenen lletra són <strong>termes independents</strong>.", r"Los <strong>términos</strong> son cada uno de los sumandos: \(3x^2,\ -5,\ 2x,\ 3\). Los que no tienen letra son <strong>términos independientes</strong>.", r"The <strong>terms</strong> are the parts being added: \(3x^2,\ -5,\ 2x,\ 3\). Those with no letter are <strong>constant terms</strong>."),
       L(r"La <strong>incògnita</strong> és la lletra el valor de la qual volem trobar (ací, \(x\)).", r"La <strong>incógnita</strong> es la letra cuyo valor queremos hallar (aquí, \(x\)).", r"The <strong>unknown</strong> is the letter whose value we want to find (here, \(x\))."),
       L(r"El <strong>grau</strong> és el major exponent de la incògnita <strong>un cop reduïda</strong> l'equació (ací, grau 2).", r"El <strong>grado</strong> es el mayor exponente de la incógnita <strong>una vez reducida</strong> la ecuación (aquí, grado 2).", r"The <strong>degree</strong> is the highest power of the unknown <strong>once the equation is simplified</strong> (here, degree 2)."),
       L(r"Una <strong>solució</strong> és un valor de la incògnita que fa certa la igualtat. <strong>Resoldre</strong> una equació és trobar <em>totes</em> les seues solucions (pot tindre'n una, diverses o cap).", r"Una <strong>solución</strong> es un valor de la incógnita que hace cierta la igualdad. <strong>Resolver</strong> una ecuación es hallar <em>todas</em> sus soluciones (puede tener una, varias o ninguna).", r"A <strong>solution</strong> is a value of the unknown that makes the equality true. <strong>Solving</strong> an equation means finding <em>all</em> its solutions (it may have one, several or none)."))
  + note(r"Compte amb el grau: \(x(x+2)=x^2+5\) sembla de grau 2, però en operar queda \(x^2+2x=x^2+5\Rightarrow 2x=5\): és de <strong>primer grau</strong>.",
         r"Cuidado con el grado: \(x(x+2)=x^2+5\) parece de grado 2, pero al operar queda \(x^2+2x=x^2+5\Rightarrow 2x=5\): es de <strong>primer grado</strong>.",
         r"Careful with the degree: \(x(x+2)=x^2+5\) looks like degree 2, but working it out gives \(x^2+2x=x^2+5\Rightarrow 2x=5\): it's <strong>first degree</strong>.", '⚠'))
s1 += box('prop', L('Com comprovem si un nombre és solució?', '¿Cómo comprobamos si un número es solución?', 'How do we check whether a number is a solution?'),
  P(r"<strong>Substituïm</strong> la incògnita pel nombre en <strong>cada membre</strong> per separat i calculem. Si els dos resultats coincideixen, és solució.",
    r"<strong>Sustituimos</strong> la incógnita por el número en <strong>cada miembro</strong> por separado y calculamos. Si los dos resultados coinciden, es solución.",
    r"<strong>Substitute</strong> the number for the unknown in <strong>each side</strong> separately and work them out. If both results match, it's a solution.")
  + D(r"x^2+1=3x-1:\qquad x=2\ \to\ 2^2+1=5,\quad 3\cdot2-1=5\ \checkmark\qquad x=3\ \to\ 3^2+1=10,\quad 3\cdot3-1=8\ \times")
  + P(r"Per tant, \(x=2\) és solució i \(x=3\) no ho és. (Aquesta equació també té la solució \(x=1\): comprova-ho!)",
      r"Por tanto, \(x=2\) es solución y \(x=3\) no lo es. (Esta ecuación también tiene la solución \(x=1\): ¡compruébalo!)",
      r"So \(x=2\) is a solution and \(x=3\) isn't. (This equation also has the solution \(x=1\): check it!)")
  + widget('w-check', '🔍', L('És solució?', '¿Es solución?', 'Is it a solution?'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), 'x^2+1=3x-1') + tin('x', 'x =', '2', 's') + '</div>', HELP,
            quick([('x^2+1=3x-1|2', 'x²+1 = 3x−1, x = 2'), ('x^2+1=3x-1|3', 'x²+1 = 3x−1, x = 3'), ('2(x+3)=2x+6|5', '2(x+3) = 2x+6'), ('x/2+x/3=5|6', 'x/2 + x/3 = 5, x = 6'), ('x^3-x=6|-2', 'x³ − x = 6, x = −2')])]))
ce('x^2+1=3x-1', [1, 2]); ce('2x+3=11', [4]); ce('2(x+3)=2x+6', 'totes'); ce('x(x+2)=x^2+5', ['5/2'])
s1 += box('prop', L('Equacions equivalents: les regles de la transposició', 'Ecuaciones equivalentes: las reglas de la transposición', 'Equivalent equations: the rules for moving terms'),
  P(r"Dues equacions són <strong>equivalents</strong> si tenen les mateixes solucions. Per a resoldre una equació la transformem en altres d'equivalents cada vegada més senzilles, fins que la incògnita queda aïllada. Ho fem amb dues regles:",
    r"Dos ecuaciones son <strong>equivalentes</strong> si tienen las mismas soluciones. Para resolver una ecuación la transformamos en otras equivalentes cada vez más sencillas, hasta que la incógnita queda aislada. Lo hacemos con dos reglas:",
    r"Two equations are <strong>equivalent</strong> if they have the same solutions. To solve an equation we turn it into simpler and simpler equivalent ones until the unknown is on its own. We use two rules:")
  + ul(L(r"<strong>Regla de la suma</strong>: si sumem o restem el mateix nombre (o expressió) als dos membres, obtenim una equació equivalent. En la pràctica: <em>el que està sumant en un membre passa a l'altre restant, i viceversa</em>.",
         r"<strong>Regla de la suma</strong>: si sumamos o restamos el mismo número (o expresión) a los dos miembros, obtenemos una ecuación equivalente. En la práctica: <em>lo que está sumando en un miembro pasa al otro restando, y viceversa</em>.",
         r"<strong>Addition rule</strong>: adding or subtracting the same number (or expression) on both sides gives an equivalent equation. In practice: <em>a term that is added on one side moves to the other side subtracted, and vice versa</em>."),
       L(r"<strong>Regla del producte</strong>: si multipliquem o dividim els dos membres pel mateix nombre (diferent de 0), obtenim una equació equivalent. En la pràctica: <em>el que està multiplicant tot un membre passa a l'altre dividint, i viceversa</em>.",
         r"<strong>Regla del producto</strong>: si multiplicamos o dividimos los dos miembros por el mismo número (distinto de 0), obtenemos una ecuación equivalente. En la práctica: <em>lo que está multiplicando a todo un miembro pasa al otro dividiendo, y viceversa</em>.",
         r"<strong>Multiplication rule</strong>: multiplying or dividing both sides by the same (non-zero) number gives an equivalent equation. In practice: <em>a number multiplying a whole side moves to the other side dividing, and vice versa</em>."))
  + D(r"3x+5=17\ \xrightarrow{-5}\ 3x=17-5=12\ \xrightarrow{:3}\ x=\frac{12}{3}=4")
  + note(r"Quan un nombre canvia de membre, el que canvia és l'<strong>operació</strong> (suma ↔ resta, producte ↔ divisió), no el signe del nombre: en \(-2x=8\), el \(-2\) passa dividint amb el seu signe: \(x=\frac{8}{-2}=-4\).",
         r"Cuando un número cambia de miembro, lo que cambia es la <strong>operación</strong> (suma ↔ resta, producto ↔ división), no el signo del número: en \(-2x=8\), el \(-2\) pasa dividiendo con su signo: \(x=\frac{8}{-2}=-4\).",
         r"When a number moves to the other side, what changes is the <strong>operation</strong> (add ↔ subtract, multiply ↔ divide), not the sign of the number: in \(-2x=8\), the \(-2\) moves across dividing, sign included: \(x=\frac{8}{-2}=-4\).", '⚠'))
s1 += levels(
 [prob(L(r"Indica quines igualtats són identitats i quines són equacions: a) \(3(x-2)=3x-6\); b) \(3x-2=7\); c) \((x-1)^2=x^2-2x+1\); d) \(x^2=9\).",
         r"Indica qué igualdades son identidades y cuáles son ecuaciones: a) \(3(x-2)=3x-6\); b) \(3x-2=7\); c) \((x-1)^2=x^2-2x+1\); d) \(x^2=9\).",
         r"Say which equalities are identities and which are equations: a) \(3(x-2)=3x-6\); b) \(3x-2=7\); c) \((x-1)^2=x^2-2x+1\); d) \(x^2=9\)."),
       P(r"a) En operar, el primer membre és \(3x-6\), igual que el segon: <strong>identitat</strong>. c) És una identitat notable: <strong>identitat</strong>.",
         r"a) Al operar, el primer miembro es \(3x-6\), igual que el segundo: <strong>identidad</strong>. c) Es una identidad notable: <strong>identidad</strong>.",
         r"a) Working it out, the left side is \(3x-6\), the same as the right: <strong>identity</strong>. c) It's a special product: <strong>identity</strong>."),
       P(r"b) Només es compleix per a \(x=3\): <strong>equació</strong>. d) Només per a \(x=3\) i \(x=-3\): <strong>equació</strong>.",
         r"b) Solo se cumple para \(x=3\): <strong>ecuación</strong>. d) Solo para \(x=3\) y \(x=-3\): <strong>ecuación</strong>.",
         r"b) Only true for \(x=3\): <strong>equation</strong>. d) Only for \(x=3\) and \(x=-3\): <strong>equation</strong>.")),
  prob(L(r"Comprova si \(x=-1\) i \(x=2\) són solucions de \(x^2-2x=3\).", r"Comprueba si \(x=-1\) y \(x=2\) son soluciones de \(x^2-2x=3\).", r"Check whether \(x=-1\) and \(x=2\) are solutions of \(x^2-2x=3\)."),
       D(r"x=-1:\quad (-1)^2-2\cdot(-1)=1+2=3\ \checkmark\qquad\Rightarrow\ \boxed{\text{%s}}" % Lt('sí és solució', 'sí es solución', 'it is a solution')),
       D(r"x=2:\quad 2^2-2\cdot2=0\neq3\qquad\Rightarrow\ \boxed{\text{%s}}" % Lt('no és solució', 'no es solución', "it isn't a solution")))],
 [prob(L(r"Quin és el grau de cada equació? a) \(2x^3-x=5\); b) \(x(x-3)=x^2+6\). Resol la b).", r"¿Cuál es el grado de cada ecuación? a) \(2x^3-x=5\); b) \(x(x-3)=x^2+6\). Resuelve la b).", r"What is the degree of each equation? a) \(2x^3-x=5\); b) \(x(x-3)=x^2+6\). Solve b)."),
       P(r"a) El major exponent de \(x\) és 3: <strong>grau 3</strong>.", r"a) El mayor exponente de \(x\) es 3: <strong>grado 3</strong>.", r"a) The highest power of \(x\) is 3: <strong>degree 3</strong>."),
       D(r"\text{b)}\ x^2-3x=x^2+6\ \Rightarrow\ -3x=6\ \Rightarrow\ x=\frac{6}{-3}=\boxed{-2}"),
       P(r"Els termes \(x^2\) es cancel·len: és de <strong>grau 1</strong>.", r"Los términos \(x^2\) se cancelan: es de <strong>grado 1</strong>.", r"The \(x^2\) terms cancel: it's <strong>degree 1</strong>."))],
 [prob(L(r"Troba el valor de \(k\) perquè \(x=2\) siga solució de l'equació \(kx^2-3x+k=4\).", r"Halla el valor de \(k\) para que \(x=2\) sea solución de la ecuación \(kx^2-3x+k=4\).", r"Find \(k\) so that \(x=2\) is a solution of \(kx^2-3x+k=4\)."),
       P(r"Si \(x=2\) és solució, en substituir s'ha de complir la igualtat:", r"Si \(x=2\) es solución, al sustituir se tiene que cumplir la igualdad:", r"If \(x=2\) is a solution, substituting must make the equality true:"),
       D(r"k\cdot2^2-3\cdot2+k=4\ \Rightarrow\ 4k-6+k=4\ \Rightarrow\ 5k=10\ \Rightarrow\ \boxed{k=2}"))])
ce('x^2=9', [3, -3]); ce('3x-2=7', [3]); chk('(x-1)**2', 'x^2-2x+1'); ce('x^2-2x=3', [-1, 3]); ce('x(x-3)=x^2+6', [-2]); ce('2x^2-3x+2=4', [2, '-1/2'])
s1 += practice([
  ('★', L(r"Identitat o equació? a) \(5x-x=4x\); b) \(5x-1=4x\); c) \((x+2)(x-2)=x^2-4\); d) \(x^2+1=0\).", r"¿Identidad o ecuación? a) \(5x-x=4x\); b) \(5x-1=4x\); c) \((x+2)(x-2)=x^2-4\); d) \(x^2+1=0\).", r"Identity or equation? a) \(5x-x=4x\); b) \(5x-1=4x\); c) \((x+2)(x-2)=x^2-4\); d) \(x^2+1=0\).")),
  ('★★', L(r"e) Comprova quins dels nombres \(-3,\ 0,\ 1,\ 3\) són solució de \(x^3-9x=0\). f) Quin grau té \((x+1)^2=x^2+7\)? Resol-la.", r"e) Comprueba cuáles de los números \(-3,\ 0,\ 1,\ 3\) son solución de \(x^3-9x=0\). f) ¿Qué grado tiene \((x+1)^2=x^2+7\)? Resuélvela.", r"e) Check which of the numbers \(-3,\ 0,\ 1,\ 3\) are solutions of \(x^3-9x=0\). f) What degree is \((x+1)^2=x^2+7\)? Solve it.")),
  ('★★★', L(r"g) Troba \(m\) perquè \(x=-1\) siga solució de \(2x^2+mx-5=m\).", r"g) Halla \(m\) para que \(x=-1\) sea solución de \(2x^2+mx-5=m\).", r"g) Find \(m\) so that \(x=-1\) is a solution of \(2x^2+mx-5=m\)."))],
  P(r"a) identitat; b) equació (\(x=1\)); c) identitat; d) equació sense solució (\(x^2\) no pot valdre \(-1\)).", r"a) identidad; b) ecuación (\(x=1\)); c) identidad; d) ecuación sin solución (\(x^2\) no puede valer \(-1\)).", r"a) identity; b) equation (\(x=1\)); c) identity; d) equation with no solution (\(x^2\) can't be \(-1\)).")
  + P(r"e) \(-3,\ 0\) i \(3\) ho són; \(1\) no (\(1-9=-8\neq0\)). f) \(x^2+2x+1=x^2+7\Rightarrow 2x=6\): grau 1, \(x=3\).", r"e) \(-3,\ 0\) y \(3\) lo son; \(1\) no (\(1-9=-8\neq0\)). f) \(x^2+2x+1=x^2+7\Rightarrow 2x=6\): grado 1, \(x=3\).", r"e) \(-3,\ 0\) and \(3\) are; \(1\) isn't (\(1-9=-8\neq0\)). f) \(x^2+2x+1=x^2+7\Rightarrow 2x=6\): degree 1, \(x=3\).")
  + D(r"\text{g)}\ 2\cdot(-1)^2+m\cdot(-1)-5=m\ \Rightarrow\ 2-m-5=m\ \Rightarrow\ -3=2m\ \Rightarrow\ m=-\frac{3}{2}"))
chk('5x-x', '4x'); ce('5x-1=4x', [1]); chk('(x+2)(x-2)', 'x^2-4'); ce('x^2+1=0', []); ce('x^3-9x=0', [-3, 0, 3]); ce('(x+1)^2=x^2+7', [3])
assert sp.solve(sp.Eq(2 - sp.Symbol('m') - 5, sp.Symbol('m'))) == [sp.Rational(-3, 2)]

# =====================================================================
# 5.2 Equacions de primer grau
# =====================================================================
s2 = box('def', L('Equació de primer grau', 'Ecuación de primer grado', 'First-degree (linear) equations'),
  P(r"Una <strong>equació de primer grau</strong> amb una incògnita és la que, un cop reduïda, es pot escriure així:", r"Una <strong>ecuación de primer grado</strong> con una incógnita es la que, una vez reducida, se puede escribir así:", r"A <strong>first-degree equation</strong> in one unknown is one that, once simplified, can be written as:")
  + D(r"ax=b\quad(a\neq0)\qquad\Longrightarrow\qquad x=\frac{b}{a}")
  + P(r"Sempre té <strong>una única solució</strong>. Per a arribar a la forma \(ax=b\) seguim aquests passos:", r"Siempre tiene <strong>una única solución</strong>. Para llegar a la forma \(ax=b\) seguimos estos pasos:", r"It always has <strong>exactly one solution</strong>. To get to the form \(ax=b\) we follow these steps:")
  + ol(L(r"<strong>Traiem parèntesis</strong> (propietat distributiva).", r"<strong>Quitamos paréntesis</strong> (propiedad distributiva).", r"<strong>Remove brackets</strong> (distributive property)."),
       L(r"<strong>Transposem</strong>: passem els termes amb \(x\) a un membre i els nombres a l'altre.", r"<strong>Transponemos</strong>: pasamos los términos con \(x\) a un miembro y los números al otro.", r"<strong>Rearrange</strong>: move the \(x\) terms to one side and the numbers to the other."),
       L(r"<strong>Reduïm</strong> (sumem els termes semblants) fins a tindre \(ax=b\).", r"<strong>Reducimos</strong> (sumamos los términos semejantes) hasta tener \(ax=b\).", r"<strong>Simplify</strong> (collect like terms) until you have \(ax=b\)."),
       L(r"<strong>Aïllem</strong> la \(x\): \(x=\frac{b}{a}\), i simplifiquem la fracció.", r"<strong>Despejamos</strong> la \(x\): \(x=\frac{b}{a}\), y simplificamos la fracción.", r"<strong>Isolate</strong> \(x\): \(x=\frac{b}{a}\), and simplify the fraction."),
       L(r"<strong>Comprovem</strong> la solució substituint-la en l'equació inicial.", r"<strong>Comprobamos</strong> la solución sustituyéndola en la ecuación inicial.", r"<strong>Check</strong> the solution by substituting it into the original equation."))
  + D(r"5x-3=2x+9\ \Rightarrow\ 5x-2x=9+3\ \Rightarrow\ 3x=12\ \Rightarrow\ x=\frac{12}{3}=4"))
ce('5x-3=2x+9', [4])
s2 += box('prop', L('Equacions amb parèntesis', 'Ecuaciones con paréntesis', 'Equations with brackets'),
  D(r"3(x-2)-2(x+1)=4-x")
  + D(r"3x-6-2x-2=4-x\ \Rightarrow\ 3x-2x+x=4+6+2\ \Rightarrow\ 2x=12\ \Rightarrow\ x=6")
  + P(r"Comprovació: \(3\cdot4-2\cdot7=12-14=-2\) i \(4-6=-2\) ✓", r"Comprobación: \(3\cdot4-2\cdot7=12-14=-2\) y \(4-6=-2\) ✓", r"Check: \(3\cdot4-2\cdot7=12-14=-2\) and \(4-6=-2\) ✓")
  + note(r"Un signe \(-\) davant d'un parèntesi <strong>canvia el signe de tots</strong> els termes de dins: \(-2(x+1)=-2x-2\) i \(-(3-x)=-3+x\).",
         r"Un signo \(-\) delante de un paréntesis <strong>cambia el signo de todos</strong> los términos de dentro: \(-2(x+1)=-2x-2\) y \(-(3-x)=-3+x\).",
         r"A \(-\) sign in front of a bracket <strong>changes the sign of every</strong> term inside: \(-2(x+1)=-2x-2\) and \(-(3-x)=-3+x\).", '⚠'))
ce('3(x-2)-2(x+1)=4-x', [6])
s2 += box('prop', L('Casos especials: cap solució o infinites solucions', 'Casos especiales: ninguna solución o infinitas soluciones', 'Special cases: no solution or infinitely many'),
  P(r"De vegades, en transposar i reduir, les \(x\) es cancel·len i arribem a \(0x=b\):", r"A veces, al transponer y reducir, las \(x\) se cancelan y llegamos a \(0x=b\):", r"Sometimes, when you rearrange and simplify, the \(x\) terms cancel and you get \(0x=b\):")
  + ul(L(r"Si \(b\neq0\), cap nombre multiplicat per 0 dona \(b\): l'equació <strong>no té solució</strong>. Exemple: \(2(x+1)=2x+5\Rightarrow 2x+2=2x+5\Rightarrow 0x=3\).",
         r"Si \(b\neq0\), ningún número multiplicado por 0 da \(b\): la ecuación <strong>no tiene solución</strong>. Ejemplo: \(2(x+1)=2x+5\Rightarrow 2x+2=2x+5\Rightarrow 0x=3\).",
         r"If \(b\neq0\), no number times 0 gives \(b\): the equation has <strong>no solution</strong>. Example: \(2(x+1)=2x+5\Rightarrow 2x+2=2x+5\Rightarrow 0x=3\)."),
       L(r"Si \(b=0\), tot nombre la compleix: <strong>infinites solucions</strong> (en realitat és una identitat). Exemple: \(3(x+2)-x=2x+6\Rightarrow 2x+6=2x+6\Rightarrow 0x=0\).",
         r"Si \(b=0\), todo número la cumple: <strong>infinitas soluciones</strong> (en realidad es una identidad). Ejemplo: \(3(x+2)-x=2x+6\Rightarrow 2x+6=2x+6\Rightarrow 0x=0\).",
         r"If \(b=0\), every number works: <strong>infinitely many solutions</strong> (it's really an identity). Example: \(3(x+2)-x=2x+6\Rightarrow 2x+6=2x+6\Rightarrow 0x=0\)."))
  + widget('w-lin', '🧮', L('Resolució pas a pas', 'Resolución paso a paso', 'Step-by-step solver'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), '3(x-2)-2(x+1)=4-x') + '</div>', HELP,
            quick([('5x-3=2x+9', '5x−3 = 2x+9'), ('3(x-2)-2(x+1)=4-x', '3(x−2)−2(x+1) = 4−x'), ('7-(2x-3)=4(1-x)+12', '7−(2x−3) = 4(1−x)+12'), ('(x+1)/2-(x-2)/3=2', '(x+1)/2 − (x−2)/3 = 2'), ('2(x+1)=2x+5', '2(x+1) = 2x+5'), ('3(x+2)-x=2x+6', '3(x+2)−x = 2x+6')])])
  + drill('lin1', 'Entrena: equacions de primer grau', 'Entrena: ecuaciones de primer grado', 'Train: linear equations'))
ce('2(x+1)=2x+5', []); ce('3(x+2)-x=2x+6', 'totes'); ce('7-(2x-3)=4(1-x)+12', [3])
s2 += levels(
 [prob(L(r"Resol \(7x-4=3x+8\).", r"Resuelve \(7x-4=3x+8\).", r"Solve \(7x-4=3x+8\)."),
       D(r"7x-3x=8+4\ \Rightarrow\ 4x=12\ \Rightarrow\ x=\frac{12}{4}=\boxed{3}"),
       P(r"Comprovació: \(7\cdot3-4=17\) i \(3\cdot3+8=17\) ✓", r"Comprobación: \(7\cdot3-4=17\) y \(3\cdot3+8=17\) ✓", r"Check: \(7\cdot3-4=17\) and \(3\cdot3+8=17\) ✓")),
  prob(L(r"Resol \(2(x+5)=3x-1\).", r"Resuelve \(2(x+5)=3x-1\).", r"Solve \(2(x+5)=3x-1\)."),
       D(r"2x+10=3x-1\ \Rightarrow\ 2x-3x=-1-10\ \Rightarrow\ -x=-11\ \Rightarrow\ \boxed{x=11}"))],
 [prob(L(r"Resol \(5-3(2x-1)=4(x+2)-10\).", r"Resuelve \(5-3(2x-1)=4(x+2)-10\).", r"Solve \(5-3(2x-1)=4(x+2)-10\)."),
       P(r"Traiem parèntesis (compte amb el \(-3\): canvia el signe dels dos termes):", r"Quitamos paréntesis (cuidado con el \(-3\): cambia el signo de los dos términos):", r"Remove brackets (careful with the \(-3\): it changes the sign of both terms):"),
       D(r"5-6x+3=4x+8-10\ \Rightarrow\ -6x-4x=8-10-5-3\ \Rightarrow\ -10x=-10\ \Rightarrow\ \boxed{x=1}"))],
 [prob(L(r"Resol \(2(3x-1)-(x+4)=5(x-1)+1\).", r"Resuelve \(2(3x-1)-(x+4)=5(x-1)+1\).", r"Solve \(2(3x-1)-(x+4)=5(x-1)+1\)."),
       D(r"6x-2-x-4=5x-5+1\ \Rightarrow\ 5x-6=5x-4\ \Rightarrow\ 5x-5x=-4+6\ \Rightarrow\ 0x=2"),
       P(r"Cap nombre multiplicat per 0 dona 2: l'equació <strong>no té solució</strong>.", r"Ningún número multiplicado por 0 da 2: la ecuación <strong>no tiene solución</strong>.", r"No number times 0 gives 2: the equation has <strong>no solution</strong>."))])
ce('7x-4=3x+8', [3]); ce('2(x+5)=3x-1', [11]); ce('5-3(2x-1)=4(x+2)-10', [1]); ce('2(3x-1)-(x+4)=5(x-1)+1', [])
s2 += practice([
  ('★', L(r"Resol: a) \(4x+7=x-5\); b) \(6-2x=3x-9\).", r"Resuelve: a) \(4x+7=x-5\); b) \(6-2x=3x-9\).", r"Solve: a) \(4x+7=x-5\); b) \(6-2x=3x-9\).")),
  ('★★', L(r"c) \(3(x-4)=2(x+1)-5\); d) \(7-(2x-3)=4(1-x)+12\).", r"c) \(3(x-4)=2(x+1)-5\); d) \(7-(2x-3)=4(1-x)+12\).", r"c) \(3(x-4)=2(x+1)-5\); d) \(7-(2x-3)=4(1-x)+12\).")),
  ('★★★', L(r"e) \(2(x+3)-x=x+6\); f) \(5(x-1)-2(x+3)=3(x-4)\). Què els passa?", r"e) \(2(x+3)-x=x+6\); f) \(5(x-1)-2(x+3)=3(x-4)\). ¿Qué les pasa?", r"e) \(2(x+3)-x=x+6\); f) \(5(x-1)-2(x+3)=3(x-4)\). What happens?"))],
  D(r"\text{a)}\ 3x=-12\Rightarrow x=-4\qquad \text{b)}\ -5x=-15\Rightarrow x=3")
  + D(r"\text{c)}\ 3x-12=2x-3\Rightarrow x=9\qquad \text{d)}\ 10-2x=16-4x\Rightarrow 2x=6\Rightarrow x=3")
  + D(r"\text{e)}\ x+6=x+6\Rightarrow 0x=0:\ \text{%s}\qquad \text{f)}\ 3x-11=3x-12\Rightarrow 0x=-1:\ \text{%s}" % (Lt('infinites solucions', 'infinitas soluciones', 'infinitely many solutions'), Lt('cap solució', 'ninguna solución', 'no solution'))))
ce('4x+7=x-5', [-4]); ce('6-2x=3x-9', [3]); ce('3(x-4)=2(x+1)-5', [9]); ce('2(x+3)-x=x+6', 'totes'); ce('5(x-1)-2(x+3)=3(x-4)', [])

# =====================================================================
# 5.3 Equacions de primer grau amb denominadors
# =====================================================================
s3 = box('prop', L('Com eliminem els denominadors', 'Cómo eliminamos los denominadores', 'How to clear the denominators'),
  P(r"Quan hi ha fraccions, primer les eliminem multiplicant <strong>tots els termes</strong> dels dos membres pel <strong>mínim comú múltiple</strong> (m.c.m.) dels denominadors. Així obtenim una equació equivalent sense denominadors.",
    r"Cuando hay fracciones, primero las eliminamos multiplicando <strong>todos los términos</strong> de los dos miembros por el <strong>mínimo común múltiplo</strong> (m.c.m.) de los denominadores. Así obtenemos una ecuación equivalente sin denominadores.",
    r"When there are fractions, first clear them by multiplying <strong>every term</strong> on both sides by the <strong>lowest common multiple</strong> (LCM) of the denominators. This gives an equivalent equation with no denominators.")
  + ol(L(r"Calculem el m.c.m. dels denominadors.", r"Calculamos el m.c.m. de los denominadores.", r"Find the LCM of the denominators."),
       L(r"Per a cada fracció, <strong>dividim el m.c.m. entre el denominador</strong> i multipliquem el resultat pel numerador, que posem <strong>entre parèntesis</strong>. Els termes sense denominador es multipliquen pel m.c.m.",
         r"Para cada fracción, <strong>dividimos el m.c.m. entre el denominador</strong> y multiplicamos el resultado por el numerador, que ponemos <strong>entre paréntesis</strong>. Los términos sin denominador se multiplican por el m.c.m.",
         r"For each fraction, <strong>divide the LCM by the denominator</strong> and multiply the result by the numerator, written <strong>in brackets</strong>. Terms with no denominator are multiplied by the LCM."),
       L(r"Continuem com abans: parèntesis, transposició, reducció i aïllament.", r"Continuamos como antes: paréntesis, transposición, reducción y despeje.", r"Carry on as before: brackets, rearranging, simplifying and isolating."))
  + D(r"\frac{x+1}{2}-\frac{x-2}{3}=2\qquad \text{m.c.m.}(2,3)=6")
  + D(r"3(x+1)-2(x-2)=12\ \Rightarrow\ 3x+3-2x+4=12\ \Rightarrow\ x=12-7=5")
  + note(r"El signe \(-\) davant d'una fracció afecta <strong>tot el numerador</strong>: \(-\frac{x-2}{3}\) es converteix en \(-2(x-2)=-2x+4\), no en \(-2x-4\). Per això el numerador va sempre entre parèntesis.",
         r"El signo \(-\) delante de una fracción afecta a <strong>todo el numerador</strong>: \(-\frac{x-2}{3}\) se convierte en \(-2(x-2)=-2x+4\), no en \(-2x-4\). Por eso el numerador va siempre entre paréntesis.",
         r"A \(-\) sign in front of a fraction affects <strong>the whole numerator</strong>: \(-\frac{x-2}{3}\) becomes \(-2(x-2)=-2x+4\), not \(-2x-4\). That's why the numerator always goes in brackets.", '⚠')
  + note(r"No oblides multiplicar també els termes <strong>sense denominador</strong> (com el 2 del segon membre, que es converteix en 12).",
         r"No olvides multiplicar también los términos <strong>sin denominador</strong> (como el 2 del segundo miembro, que se convierte en 12).",
         r"Don't forget to multiply the terms <strong>with no denominator</strong> too (like the 2 on the right, which becomes 12).", '⚠')
  + P(r"Pots fer servir la calculadora pas a pas de l'apartat anterior: també elimina els denominadors.", r"Puedes usar la calculadora paso a paso del apartado anterior: también elimina los denominadores.", r"You can use the step-by-step solver in the previous section: it also clears denominators.")
  + drill('lin2', 'Entrena: amb parèntesis i denominadors', 'Entrena: con paréntesis y denominadores', 'Train: brackets and denominators'))
ce('(x+1)/2-(x-2)/3=2', [5])
s3 += levels(
 [prob(L(r"Resol \(\dfrac{x}{3}+\dfrac{x}{2}=10\).", r"Resuelve \(\dfrac{x}{3}+\dfrac{x}{2}=10\).", r"Solve \(\dfrac{x}{3}+\dfrac{x}{2}=10\)."),
       D(r"\text{m.c.m.}(3,2)=6:\quad 2x+3x=60\ \Rightarrow\ 5x=60\ \Rightarrow\ \boxed{x=12}"))],
 [prob(L(r"Resol \(\dfrac{x-1}{4}-\dfrac{x-3}{6}=1\).", r"Resuelve \(\dfrac{x-1}{4}-\dfrac{x-3}{6}=1\).", r"Solve \(\dfrac{x-1}{4}-\dfrac{x-3}{6}=1\)."),
       D(r"\text{m.c.m.}(4,6)=12:\quad 3(x-1)-2(x-3)=12"),
       D(r"3x-3-2x+6=12\ \Rightarrow\ x+3=12\ \Rightarrow\ \boxed{x=9}"))],
 [prob(L(r"Resol \(\dfrac{x-3}{2}-\dfrac{2(x-1)}{3}=\dfrac{x}{6}-3\).", r"Resuelve \(\dfrac{x-3}{2}-\dfrac{2(x-1)}{3}=\dfrac{x}{6}-3\).", r"Solve \(\dfrac{x-3}{2}-\dfrac{2(x-1)}{3}=\dfrac{x}{6}-3\)."),
       D(r"\text{m.c.m.}(2,3,6)=6:\quad 3(x-3)-2\cdot2(x-1)=x-18"),
       D(r"3x-9-4x+4=x-18\ \Rightarrow\ -x-5=x-18\ \Rightarrow\ -2x=-13\ \Rightarrow\ \boxed{x=\frac{13}{2}}"),
       P(r"La solució no ha de ser entera: una fracció també és una solució vàlida.", r"La solución no tiene por qué ser entera: una fracción también es una solución válida.", r"The solution needn't be a whole number: a fraction is a perfectly good solution."))])
ce('x/3+x/2=10', [12]); ce('(x-1)/4-(x-3)/6=1', [9]); ce('(x-3)/2-2(x-1)/3=x/6-3', ['13/2'])
s3 += practice([
  ('★', L(r"Resol: a) \(\dfrac{x}{2}-\dfrac{x}{5}=3\); b) \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\).", r"Resuelve: a) \(\dfrac{x}{2}-\dfrac{x}{5}=3\); b) \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\).", r"Solve: a) \(\dfrac{x}{2}-\dfrac{x}{5}=3\); b) \(\dfrac{x+3}{4}=\dfrac{x-1}{2}\).")),
  ('★★', L(r"c) \(\dfrac{x+2}{3}-\dfrac{x-1}{4}=2\); d) \(x-\dfrac{x+1}{3}=\dfrac{x+4}{2}\).", r"c) \(\dfrac{x+2}{3}-\dfrac{x-1}{4}=2\); d) \(x-\dfrac{x+1}{3}=\dfrac{x+4}{2}\).", r"c) \(\dfrac{x+2}{3}-\dfrac{x-1}{4}=2\); d) \(x-\dfrac{x+1}{3}=\dfrac{x+4}{2}\).")),
  ('★★★', L(r"e) \(\dfrac{2(x-1)}{3}-\dfrac{x+1}{4}=\dfrac{x}{2}-\dfrac{3}{4}\).", r"e) \(\dfrac{2(x-1)}{3}-\dfrac{x+1}{4}=\dfrac{x}{2}-\dfrac{3}{4}\).", r"e) \(\dfrac{2(x-1)}{3}-\dfrac{x+1}{4}=\dfrac{x}{2}-\dfrac{3}{4}\)."))],
  D(r"\text{a)}\ 5x-2x=30\Rightarrow x=10\qquad \text{b)}\ x+3=2(x-1)\Rightarrow x=5")
  + D(r"\text{c)}\ 4(x+2)-3(x-1)=24\Rightarrow x+11=24\Rightarrow x=13\qquad \text{d)}\ 6x-2(x+1)=3(x+4)\Rightarrow 4x-2=3x+12\Rightarrow x=14")
  + D(r"\text{e)}\ 8(x-1)-3(x+1)=6x-9\Rightarrow 5x-11=6x-9\Rightarrow x=-2"))
ce('x/2-x/5=3', [10]); ce('(x+3)/4=(x-1)/2', [5]); ce('(x+2)/3-(x-1)/4=2', [13]); ce('x-(x+1)/3=(x+4)/2', [14]); ce('2(x-1)/3-(x+1)/4=x/2-3/4', [-2])

# =====================================================================
# 5.4 Equacions de segon grau incompletes
# =====================================================================
s4 = box('def', L('Equació de segon grau', 'Ecuación de segundo grado', 'Quadratic equations'),
  P(r"Una <strong>equació de segon grau</strong> amb una incògnita és la que, un cop reduïda, té la <strong>forma general</strong>:", r"Una <strong>ecuación de segundo grado</strong> con una incógnita es la que, una vez reducida, tiene la <strong>forma general</strong>:", r"A <strong>second-degree (quadratic) equation</strong> in one unknown is one that, once simplified, has the <strong>general form</strong>:")
  + D(r"ax^2+bx+c=0\qquad(a\neq0)")
  + P(r"\(a\) és el coeficient de \(x^2\), \(b\) el de \(x\) i \(c\) el terme independent. Té, com a màxim, <strong>dues solucions</strong>.", r"\(a\) es el coeficiente de \(x^2\), \(b\) el de \(x\) y \(c\) el término independiente. Tiene, como máximo, <strong>dos soluciones</strong>.", r"\(a\) is the coefficient of \(x^2\), \(b\) the coefficient of \(x\) and \(c\) the constant term. It has at most <strong>two solutions</strong>.")
  + ul(L(r"És <strong>completa</strong> si \(b\neq0\) i \(c\neq0\): \(\ 2x^2-7x+3=0\).", r"Es <strong>completa</strong> si \(b\neq0\) y \(c\neq0\): \(\ 2x^2-7x+3=0\).", r"It's <strong>complete</strong> if \(b\neq0\) and \(c\neq0\): \(\ 2x^2-7x+3=0\)."),
       L(r"És <strong>incompleta</strong> si \(b=0\) o \(c=0\): \(\ x^2-9=0,\quad 3x^2+5x=0\).", r"Es <strong>incompleta</strong> si \(b=0\) o \(c=0\): \(\ x^2-9=0,\quad 3x^2+5x=0\).", r"It's <strong>incomplete</strong> if \(b=0\) or \(c=0\): \(\ x^2-9=0,\quad 3x^2+5x=0\)."))
  + note(r"Abans d'identificar \(a,\ b,\ c\), l'equació ha d'estar en forma general: tot en el primer membre, ordenat, i 0 en el segon. En \(5x-x^2=2\) passem el 2: \(-x^2+5x-2=0\), i \(a=-1,\ b=5,\ c=-2\).",
         r"Antes de identificar \(a,\ b,\ c\), la ecuación tiene que estar en forma general: todo en el primer miembro, ordenado, y 0 en el segundo. En \(5x-x^2=2\) pasamos el 2: \(-x^2+5x-2=0\), y \(a=-1,\ b=5,\ c=-2\).",
         r"Before reading off \(a,\ b,\ c\), the equation must be in general form: everything on the left, in order, and 0 on the right. In \(5x-x^2=2\) move the 2: \(-x^2+5x-2=0\), so \(a=-1,\ b=5,\ c=-2\)."))
s4 += box('prop', L('Incompletes sense terme en x: ax² + c = 0', 'Incompletas sin término en x: ax² + c = 0', 'No x term: ax² + c = 0'),
  P(r"Aïllem \(x^2\) i fem l'<strong>arrel quadrada</strong>, sense oblidar les <strong>dues</strong> arrels, la positiva i la negativa:", r"Despejamos \(x^2\) y hacemos la <strong>raíz cuadrada</strong>, sin olvidar las <strong>dos</strong> raíces, la positiva y la negativa:", r"Isolate \(x^2\) and take the <strong>square root</strong>, remembering <strong>both</strong> roots, positive and negative:")
  + D(r"ax^2+c=0\ \Rightarrow\ x^2=-\frac{c}{a}\ \Rightarrow\ x=\pm\sqrt{-\frac{c}{a}}")
  + D(r"2x^2-18=0\ \Rightarrow\ x^2=\frac{18}{2}=9\ \Rightarrow\ x=\pm\sqrt9=\pm3")
  + P(r"Si \(-\frac{c}{a}\) és <strong>negatiu</strong>, l'equació <strong>no té solució</strong>, perquè cap nombre al quadrat és negatiu: \(x^2+4=0\Rightarrow x^2=-4\), sense solució.", r"Si \(-\frac{c}{a}\) es <strong>negativo</strong>, la ecuación <strong>no tiene solución</strong>, porque ningún número al cuadrado es negativo: \(x^2+4=0\Rightarrow x^2=-4\), sin solución.", r"If \(-\frac{c}{a}\) is <strong>negative</strong>, the equation has <strong>no solution</strong>, because no square is negative: \(x^2+4=0\Rightarrow x^2=-4\), no solution."))
s4 += box('prop', L('Incompletes sense terme independent: ax² + bx = 0', 'Incompletas sin término independiente: ax² + bx = 0', 'No constant term: ax² + bx = 0'),
  P(r"Traiem <strong>factor comú</strong> \(x\) i fem servir que, si un producte val zero, algun dels factors ha de valdre zero:", r"Sacamos <strong>factor común</strong> \(x\) y usamos que, si un producto vale cero, alguno de los factores tiene que valer cero:", r"Take out the <strong>common factor</strong> \(x\) and use the fact that if a product is zero, one of the factors must be zero:")
  + D(r"ax^2+bx=0\ \Rightarrow\ x\,(ax+b)=0\ \Rightarrow\ \begin{cases}x=0\\ ax+b=0\ \Rightarrow\ x=-\dfrac{b}{a}\end{cases}")
  + D(r"3x^2-12x=0\ \Rightarrow\ 3x\,(x-4)=0\ \Rightarrow\ x=0,\quad x=4")
  + note(r"<strong>No dividisques</strong> els dos membres entre \(x\): perdries la solució \(x=0\). Aquestes equacions <strong>sempre</strong> tenen la solució \(x=0\).",
         r"<strong>No dividas</strong> los dos miembros entre \(x\): perderías la solución \(x=0\). Estas ecuaciones <strong>siempre</strong> tienen la solución \(x=0\).",
         r"<strong>Don't divide</strong> both sides by \(x\): you'd lose the solution \(x=0\). These equations <strong>always</strong> have the solution \(x=0\).", '⚠')
  + P(r"Si \(b=c=0\), l'equació és \(ax^2=0\) i l'única solució és \(x=0\).", r"Si \(b=c=0\), la ecuación es \(ax^2=0\) y la única solución es \(x=0\).", r"If \(b=c=0\), the equation is \(ax^2=0\) and the only solution is \(x=0\).")
  + drill('inc', 'Entrena: equacions incompletes', 'Entrena: ecuaciones incompletas', 'Train: incomplete quadratics', SETHINT))
ce('2x^2-18=0', [3, -3]); ce('x^2+4=0', []); ce('3x^2-12x=0', [0, 4]); ce('5x-x^2=2', ['(5+sqrt(17))/2', '(5-sqrt(17))/2'])
s4 += levels(
 [prob(L(r"Resol: a) \(5x^2-45=0\); b) \(x^2+7x=0\).", r"Resuelve: a) \(5x^2-45=0\); b) \(x^2+7x=0\).", r"Solve: a) \(5x^2-45=0\); b) \(x^2+7x=0\)."),
       D(r"\text{a)}\ x^2=\frac{45}{5}=9\ \Rightarrow\ \boxed{x=\pm3}"),
       D(r"\text{b)}\ x(x+7)=0\ \Rightarrow\ \boxed{x=0},\quad x+7=0\Rightarrow\boxed{x=-7}"))],
 [prob(L(r"Resol \((x+2)^2=4x+29\).", r"Resuelve \((x+2)^2=4x+29\).", r"Solve \((x+2)^2=4x+29\)."),
       P(r"Primer la reduïm a la forma general:", r"Primero la reducimos a la forma general:", r"First put it in general form:"),
       D(r"x^2+4x+4=4x+29\ \Rightarrow\ x^2-25=0\ \Rightarrow\ x^2=25\ \Rightarrow\ \boxed{x=\pm5}"))],
 [prob(L(r"Resol \(\dfrac{x^2}{3}-\dfrac{x}{2}=\dfrac{x^2+x}{6}\).", r"Resuelve \(\dfrac{x^2}{3}-\dfrac{x}{2}=\dfrac{x^2+x}{6}\).", r"Solve \(\dfrac{x^2}{3}-\dfrac{x}{2}=\dfrac{x^2+x}{6}\)."),
       D(r"\text{m.c.m.}=6:\quad 2x^2-3x=x^2+x\ \Rightarrow\ x^2-4x=0"),
       D(r"x(x-4)=0\ \Rightarrow\ \boxed{x=0},\ \boxed{x=4}"))])
ce('5x^2-45=0', [3, -3]); ce('x^2+7x=0', [0, -7]); ce('(x+2)^2=4x+29', [5, -5]); ce('x^2/3-x/2=(x^2+x)/6', [0, 4])
s4 += practice([
  ('★', L(r"Resol: a) \(x^2-49=0\); b) \(4x^2-20x=0\); c) \(9x^2-4=0\).", r"Resuelve: a) \(x^2-49=0\); b) \(4x^2-20x=0\); c) \(9x^2-4=0\).", r"Solve: a) \(x^2-49=0\); b) \(4x^2-20x=0\); c) \(9x^2-4=0\).")),
  ('★★', L(r"d) \(2x^2+50=0\); e) \((x-3)(x+3)=7\); f) \(x(2x-5)=3x\).", r"d) \(2x^2+50=0\); e) \((x-3)(x+3)=7\); f) \(x(2x-5)=3x\).", r"d) \(2x^2+50=0\); e) \((x-3)(x+3)=7\); f) \(x(2x-5)=3x\).")),
  ('★★★', L(r"g) \((2x-1)^2=1-6x\); h) \(\dfrac{x^2-1}{3}-\dfrac{x^2+1}{4}=1\).", r"g) \((2x-1)^2=1-6x\); h) \(\dfrac{x^2-1}{3}-\dfrac{x^2+1}{4}=1\).", r"g) \((2x-1)^2=1-6x\); h) \(\dfrac{x^2-1}{3}-\dfrac{x^2+1}{4}=1\)."))],
  D(r"\text{a)}\ x=\pm7\qquad \text{b)}\ 4x(x-5)=0\Rightarrow x=0,\ x=5\qquad \text{c)}\ x^2=\frac49\Rightarrow x=\pm\frac23")
  + D(r"\text{d)}\ x^2=-25:\ \text{%s}\qquad \text{e)}\ x^2-9=7\Rightarrow x^2=16\Rightarrow x=\pm4\qquad \text{f)}\ 2x^2-8x=0\Rightarrow x=0,\ x=4" % Lt('cap solució', 'ninguna solución', 'no solution'))
  + D(r"\text{g)}\ 4x^2-4x+1=1-6x\Rightarrow 4x^2+2x=0\Rightarrow 2x(2x+1)=0\Rightarrow x=0,\ x=-\frac12")
  + D(r"\text{h)}\ 4(x^2-1)-3(x^2+1)=12\Rightarrow x^2=19\Rightarrow x=\pm\sqrt{19}"))
ce('x^2-49=0', [7, -7]); ce('4x^2-20x=0', [0, 5]); ce('9x^2-4=0', ['2/3', '-2/3']); ce('2x^2+50=0', []); ce('(x-3)(x+3)=7', [4, -4]); ce('x(2x-5)=3x', [0, 4])
ce('(2x-1)^2=1-6x', [0, '-1/2']); ce('(x^2-1)/3-(x^2+1)/4=1', ['sqrt(19)', '-sqrt(19)'])

# =====================================================================
# 5.5 Equacions de segon grau completes
# =====================================================================
s5 = box('def', L('La fórmula de les equacions de segon grau', 'La fórmula de las ecuaciones de segundo grado', 'The quadratic formula'),
  P(r"Les solucions de \(ax^2+bx+c=0\) s'obtenen amb la fórmula:", r"Las soluciones de \(ax^2+bx+c=0\) se obtienen con la fórmula:", r"The solutions of \(ax^2+bx+c=0\) are given by the formula:")
  + D(r"\boxed{x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}}")
  + P(r"El signe \(\pm\) ens dona les dues solucions: una amb \(+\) i l'altra amb \(-\). Exemple: \(x^2-5x+6=0\), amb \(a=1,\ b=-5,\ c=6\):", r"El signo \(\pm\) nos da las dos soluciones: una con \(+\) y la otra con \(-\). Ejemplo: \(x^2-5x+6=0\), con \(a=1,\ b=-5,\ c=6\):", r"The \(\pm\) sign gives both solutions: one with \(+\) and the other with \(-\). Example: \(x^2-5x+6=0\), with \(a=1,\ b=-5,\ c=6\):")
  + D(r"x=\frac{-(-5)\pm\sqrt{(-5)^2-4\cdot1\cdot6}}{2\cdot1}=\frac{5\pm\sqrt{1}}{2}=\frac{5\pm1}{2}\ \Rightarrow\ x_1=\frac{6}{2}=3,\quad x_2=\frac{4}{2}=2")
  + note(r"Errors típics: \(-b\) és l'<strong>oposat</strong> de \(b\) (si \(b=-5\), \(-b=5\)); \(b^2\) sempre és positiu, \((-5)^2=25\); i la ratlla de fracció va davall de <strong>tot</strong> el numerador.",
         r"Errores típicos: \(-b\) es el <strong>opuesto</strong> de \(b\) (si \(b=-5\), \(-b=5\)); \(b^2\) siempre es positivo, \((-5)^2=25\); y la raya de fracción va debajo de <strong>todo</strong> el numerador.",
         r"Common mistakes: \(-b\) is the <strong>opposite</strong> of \(b\) (if \(b=-5\), \(-b=5\)); \(b^2\) is always positive, \((-5)^2=25\); and the fraction bar goes under the <strong>whole</strong> numerator.", '⚠')
  + note(r"La fórmula també serveix per a les incompletes, però per a aquestes els mètodes de l'apartat anterior són més ràpids.", r"La fórmula también sirve para las incompletas, pero para estas los métodos del apartado anterior son más rápidos.", r"The formula also works for incomplete equations, but the methods in the previous section are quicker."))
ce('x^2-5x+6=0', [2, 3])
s5 += box('prop', L('El discriminant: quantes solucions hi ha?', 'El discriminante: ¿cuántas soluciones hay?', 'The discriminant: how many solutions?'),
  P(r"El nombre de dins de l'arrel, \(\Delta=b^2-4ac\), s'anomena <strong>discriminant</strong> i ens diu quantes solucions té l'equació sense haver-la de resoldre:", r"El número de dentro de la raíz, \(\Delta=b^2-4ac\), se llama <strong>discriminante</strong> y nos dice cuántas soluciones tiene la ecuación sin tener que resolverla:", r"The number under the square root, \(\Delta=b^2-4ac\), is called the <strong>discriminant</strong>; it tells us how many solutions there are without solving:")
  + '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>\\(\\Delta=b^2-4ac\\)</th><th>' + L('Solucions', 'Soluciones', 'Solutions') + '</th><th>' + L('Exemple', 'Ejemplo', 'Example') + '</th></tr></thead><tbody>'
  + '<tr><td>\\(\\Delta>0\\)</td><td class="l">' + L('Dues solucions diferents', 'Dos soluciones distintas', 'Two different solutions') + '</td><td>\\(x^2-5x+6=0:\\ \\Delta=1\\)</td></tr>'
  + '<tr><td>\\(\\Delta=0\\)</td><td class="l">' + L('Una solució (doble)', 'Una solución (doble)', 'One (repeated) solution') + '</td><td>\\(x^2-6x+9=0:\\ \\Delta=0,\\ x=3\\)</td></tr>'
  + '<tr><td>\\(\\Delta<0\\)</td><td class="l">' + L('Cap solució', 'Ninguna solución', 'No solution') + '</td><td>\\(x^2+x+1=0:\\ \\Delta=-3\\)</td></tr></tbody></table></div>'
  + P(r"Gràficament, les solucions de \(ax^2+bx+c=0\) són els punts on la paràbola \(y=ax^2+bx+c\) talla l'eix \(X\). Mou els coeficients i observa-ho:",
      r"Gráficamente, las soluciones de \(ax^2+bx+c=0\) son los puntos donde la parábola \(y=ax^2+bx+c\) corta al eje \(X\). Mueve los coeficientes y obsérvalo:",
      r"Graphically, the solutions of \(ax^2+bx+c=0\) are the points where the parabola \(y=ax^2+bx+c\) crosses the \(x\)-axis. Move the coefficients and see:")
  + widget('w-disc', '📈', L('El discriminant i la paràbola', 'El discriminante y la parábola', 'The discriminant and the parabola'),
           ['<div class="wrow">' + rng('a', 'a', -3, 3, 1) + rng('b', 'b', -8, 8, -2) + rng('c', 'c', -9, 9, -3) + '</div>'],
           out='<div class="disc-out"><div class="disc-eq"></div><svg class="parab" viewBox="0 0 340 260" role="img" aria-label="paràbola"></svg></div>'))
ce('x^2-6x+9=0', [3]); ce('x^2+x+1=0', [])
s5 += box('prop', L('Equacions de segon grau no reduïdes', 'Ecuaciones de segundo grado no reducidas', 'Quadratics that need simplifying first'),
  P(r"Si hi ha parèntesis o denominadors, primer els eliminem (com a les de primer grau) i passem tots els termes al primer membre. Si el coeficient \(a\) queda negatiu, podem multiplicar-ho tot per \(-1\); i si tots els coeficients tenen un divisor comú, podem simplificar.",
    r"Si hay paréntesis o denominadores, primero los eliminamos (como en las de primer grado) y pasamos todos los términos al primer miembro. Si el coeficiente \(a\) queda negativo, podemos multiplicarlo todo por \(-1\); y si todos los coeficientes tienen un divisor común, podemos simplificar.",
    r"If there are brackets or denominators, clear them first (as with linear equations) and move all the terms to the left. If \(a\) ends up negative, you can multiply everything by \(-1\); and if all the coefficients share a factor, you can simplify.")
  + D(r"\frac{x(x-1)}{2}-\frac{x+1}{3}=1\ \xrightarrow{\cdot6}\ 3x^2-3x-2x-2=6\ \Rightarrow\ 3x^2-5x-8=0")
  + D(r"x=\frac{5\pm\sqrt{25+96}}{6}=\frac{5\pm11}{6}\ \Rightarrow\ x_1=\frac{16}{6}=\frac83,\quad x_2=\frac{-6}{6}=-1")
  + widget('w-q2', '🧮', L('Resolució pas a pas de qualsevol equació de 2n grau', 'Resolución paso a paso de cualquier ecuación de 2.º grado', 'Step-by-step solver for any quadratic'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), 'x^2-5x+6=0') + '</div>', HELP,
            quick([('x^2-5x+6=0', 'x²−5x+6 = 0'), ('2x^2-7x+3=0', '2x²−7x+3 = 0'), ('x^2-6x+9=0', 'x²−6x+9 = 0'), ('x^2+x+1=0', 'x²+x+1 = 0'), ('x^2-3x-1=0', 'x²−3x−1 = 0'), ('x(x-1)/2-(x+1)/3=1', 'x(x−1)/2 − (x+1)/3 = 1'), ('5x-x^2=2', '5x−x² = 2'), ('3x^2-12x=0', '3x²−12x = 0')])])
  + drill('q2', 'Entrena: equacions completes', 'Entrena: ecuaciones completas', 'Train: complete quadratics', SETHINT)
  + drill('disc', 'Entrena: quantes solucions té?', 'Entrena: ¿cuántas soluciones tiene?', 'Train: how many solutions?'))
ce('x(x-1)/2-(x+1)/3=1', ['8/3', -1])
s5 += levels(
 [prob(L(r"Resol \(x^2+2x-15=0\).", r"Resuelve \(x^2+2x-15=0\).", r"Solve \(x^2+2x-15=0\)."),
       D(r"x=\frac{-2\pm\sqrt{4+60}}{2}=\frac{-2\pm8}{2}\ \Rightarrow\ \boxed{x_1=3},\quad \boxed{x_2=-5}")),
  prob(L(r"Resol \(2x^2-7x+3=0\).", r"Resuelve \(2x^2-7x+3=0\).", r"Solve \(2x^2-7x+3=0\)."),
       D(r"x=\frac{7\pm\sqrt{49-24}}{4}=\frac{7\pm5}{4}\ \Rightarrow\ \boxed{x_1=3},\quad \boxed{x_2=\frac{2}{4}=\frac12}"))],
 [prob(L(r"Sense resoldre-les, digues quantes solucions té cada equació: a) \(x^2-4x+4=0\); b) \(3x^2+2x+1=0\); c) \(x^2-3x-1=0\). Resol la c).",
         r"Sin resolverlas, di cuántas soluciones tiene cada ecuación: a) \(x^2-4x+4=0\); b) \(3x^2+2x+1=0\); c) \(x^2-3x-1=0\). Resuelve la c).",
         r"Without solving, say how many solutions each equation has: a) \(x^2-4x+4=0\); b) \(3x^2+2x+1=0\); c) \(x^2-3x-1=0\). Solve c)."),
       D(r"\text{a)}\ \Delta=16-16=0\ \to\ \text{%s}\qquad \text{b)}\ \Delta=4-12=-8\ \to\ \text{%s}" % (Lt('una solució', 'una solución', 'one solution'), Lt('cap', 'ninguna', 'none'))),
       D(r"\text{c)}\ \Delta=9+4=13>0\ \to\ x=\frac{3\pm\sqrt{13}}{2}\ \Rightarrow\ x_1\approx3\dc30,\quad x_2\approx-0\dc30"),
       P(r"Quan \(\Delta\) no és un quadrat perfecte, les solucions són irracionals: les deixem amb l'arrel (i, si cal, en donem una aproximació).", r"Cuando \(\Delta\) no es un cuadrado perfecto, las soluciones son irracionales: las dejamos con la raíz (y, si hace falta, damos una aproximación).", r"When \(\Delta\) isn't a perfect square, the solutions are irrational: leave them with the root (and give an approximation if needed).")),
  prob(L(r"Resol \((x+1)(x-2)=2x+2\).", r"Resuelve \((x+1)(x-2)=2x+2\).", r"Solve \((x+1)(x-2)=2x+2\)."),
       D(r"x^2-x-2=2x+2\ \Rightarrow\ x^2-3x-4=0"),
       D(r"x=\frac{3\pm\sqrt{9+16}}{2}=\frac{3\pm5}{2}\ \Rightarrow\ \boxed{x_1=4},\quad \boxed{x_2=-1}"))],
 [prob(L(r"Troba el valor de \(k\) perquè l'equació \(x^2-6x+k=0\) tinga una única solució. Quina és?", r"Halla el valor de \(k\) para que la ecuación \(x^2-6x+k=0\) tenga una única solución. ¿Cuál es?", r"Find \(k\) so that \(x^2-6x+k=0\) has exactly one solution. What is it?"),
       P(r"Ha de ser \(\Delta=0\):", r"Tiene que ser \(\Delta=0\):", r"We need \(\Delta=0\):"),
       D(r"(-6)^2-4\cdot1\cdot k=0\ \Rightarrow\ 36-4k=0\ \Rightarrow\ \boxed{k=9}"),
       D(r"x^2-6x+9=0\ \Rightarrow\ x=\frac{6\pm0}{2}=\boxed{3}\qquad(\text{%s: }(x-3)^2=0)" % Lt('és', 'es', 'it is')))])
ce('x^2+2x-15=0', [3, -5]); ce('2x^2-7x+3=0', [3, '1/2']); ce('x^2-4x+4=0', [2]); ce('3x^2+2x+1=0', []); ce('x^2-3x-1=0', ['(3+sqrt(13))/2', '(3-sqrt(13))/2'])
ce('(x+1)(x-2)=2x+2', [4, -1]); ce('x^2-6x+9=0', [3])
s5 += practice([
  ('★', L(r"Resol: a) \(x^2-7x+10=0\); b) \(x^2+4x-21=0\); c) \(3x^2+5x-2=0\).", r"Resuelve: a) \(x^2-7x+10=0\); b) \(x^2+4x-21=0\); c) \(3x^2+5x-2=0\).", r"Solve: a) \(x^2-7x+10=0\); b) \(x^2+4x-21=0\); c) \(3x^2+5x-2=0\).")),
  ('★★', L(r"d) \(-x^2+2x+8=0\); e) \(4x^2-4x+1=0\); f) \(x^2+x+3=0\); g) \((x-2)^2+(x+1)^2=17\).", r"d) \(-x^2+2x+8=0\); e) \(4x^2-4x+1=0\); f) \(x^2+x+3=0\); g) \((x-2)^2+(x+1)^2=17\).", r"d) \(-x^2+2x+8=0\); e) \(4x^2-4x+1=0\); f) \(x^2+x+3=0\); g) \((x-2)^2+(x+1)^2=17\).")),
  ('★★★', L(r"h) \(\dfrac{x^2-2}{3}-\dfrac{x+1}{2}=\dfrac{x-4}{6}\); i) Troba \(m\) perquè \(x^2+mx+9=0\) tinga una solució doble.", r"h) \(\dfrac{x^2-2}{3}-\dfrac{x+1}{2}=\dfrac{x-4}{6}\); i) Halla \(m\) para que \(x^2+mx+9=0\) tenga una solución doble.", r"h) \(\dfrac{x^2-2}{3}-\dfrac{x+1}{2}=\dfrac{x-4}{6}\); i) Find \(m\) so that \(x^2+mx+9=0\) has a repeated solution."))],
  D(r"\text{a)}\ x=\frac{7\pm3}{2}:\ 5,\ 2\qquad \text{b)}\ x=\frac{-4\pm10}{2}:\ 3,\ -7\qquad \text{c)}\ x=\frac{-5\pm7}{6}:\ \frac13,\ -2")
  + D(r"\text{d)}\ x^2-2x-8=0:\ 4,\ -2\qquad \text{e)}\ \Delta=0:\ x=\frac12\qquad \text{f)}\ \Delta=-11:\ \text{%s}" % Lt('cap solució', 'ninguna solución', 'no solution'))
  + D(r"\text{g)}\ 2x^2-2x-12=0\Rightarrow x^2-x-6=0:\ 3,\ -2")
  + D(r"\text{h)}\ 2x^2-4-3x-3=x-4\Rightarrow 2x^2-4x-3=0\Rightarrow x=\frac{4\pm\sqrt{40}}{4}=\frac{2\pm\sqrt{10}}{2}\qquad \text{i)}\ m^2-36=0\Rightarrow m=\pm6"))
ce('x^2-7x+10=0', [5, 2]); ce('x^2+4x-21=0', [3, -7]); ce('3x^2+5x-2=0', ['1/3', -2]); ce('-x^2+2x+8=0', [4, -2]); ce('4x^2-4x+1=0', ['1/2']); ce('x^2+x+3=0', [])
ce('(x-2)^2+(x+1)^2=17', [3, -2]); ce('(x^2-2)/3-(x+1)/2=(x-4)/6', ['(2+sqrt(10))/2', '(2-sqrt(10))/2']); ce('x^2+6x+9=0', [-3]); ce('x^2-6x+9=0', [3])

# =====================================================================
# 5.6 Equacions de tercer grau (Ruffini)
# =====================================================================
s6 = box('prop', L('Resoldre equacions factoritzant', 'Resolver ecuaciones factorizando', 'Solving equations by factorising'),
  P(r"Una equació de tercer grau té, com a màxim, <strong>tres solucions</strong>. No hi ha una fórmula senzilla, però moltes es poden resoldre <strong>factoritzant</strong> el polinomi amb el que vam aprendre a la unitat anterior, perquè:",
    r"Una ecuación de tercer grado tiene, como máximo, <strong>tres soluciones</strong>. No hay una fórmula sencilla, pero muchas se pueden resolver <strong>factorizando</strong> el polinomio con lo que aprendimos en la unidad anterior, porque:",
    r"A third-degree (cubic) equation has at most <strong>three solutions</strong>. There's no simple formula, but many can be solved by <strong>factorising</strong> the polynomial with what we learned last unit, because:")
  + D(r"A\cdot B=0\ \Longleftrightarrow\ A=0\ \ \text{%s}\ \ B=0" % Lt('o', 'o', 'or'))
  + ol(L(r"Passem tots els termes al primer membre: \(P(x)=0\).", r"Pasamos todos los términos al primer miembro: \(P(x)=0\).", r"Move all the terms to the left: \(P(x)=0\)."),
       L(r"Si <strong>no hi ha terme independent</strong>, traiem factor comú \(x\): \(x\cdot(ax^2+bx+c)=0\). Una solució és \(x=0\) i les altres són les de l'equació de segon grau.",
         r"Si <strong>no hay término independiente</strong>, sacamos factor común \(x\): \(x\cdot(ax^2+bx+c)=0\). Una solución es \(x=0\) y las otras son las de la ecuación de segundo grado.",
         r"If there's <strong>no constant term</strong>, take out the common factor \(x\): \(x\cdot(ax^2+bx+c)=0\). One solution is \(x=0\) and the others come from the quadratic."),
       L(r"Si n'hi ha, busquem una solució entera entre els <strong>divisors del terme independent</strong>, provant amb el teorema del residu (\(P(a)=0\)) o directament amb <strong>Ruffini</strong>.",
         r"Si lo hay, buscamos una solución entera entre los <strong>divisores del término independiente</strong>, probando con el teorema del resto (\(P(a)=0\)) o directamente con <strong>Ruffini</strong>.",
         r"If there is one, look for a whole-number solution among the <strong>divisors of the constant term</strong>, testing with the remainder theorem (\(P(a)=0\)) or straight away with <strong>Ruffini's rule</strong>."),
       L(r"Si \(x=a\) és solució, Ruffini ens dona \(P(x)=(x-a)\cdot C(x)\), on \(C(x)\) és de segon grau. Resolem \(C(x)=0\) amb la fórmula.",
         r"Si \(x=a\) es solución, Ruffini nos da \(P(x)=(x-a)\cdot C(x)\), donde \(C(x)\) es de segundo grado. Resolvemos \(C(x)=0\) con la fórmula.",
         r"If \(x=a\) is a solution, Ruffini gives \(P(x)=(x-a)\cdot C(x)\), where \(C(x)\) is quadratic. Solve \(C(x)=0\) with the formula.")))
s6 += box('def', L('Exemple resolt', 'Ejemplo resuelto', 'Worked example'),
  D(r"x^3-2x^2-5x+6=0")
  + P(r"Divisors de 6: \(\pm1,\ \pm2,\ \pm3,\ \pm6\). Provem \(x=1\): \(\ 1-2-5+6=0\ \checkmark\). Dividim per Ruffini:", r"Divisores de 6: \(\pm1,\ \pm2,\ \pm3,\ \pm6\). Probamos \(x=1\): \(\ 1-2-5+6=0\ \checkmark\). Dividimos por Ruffini:", r"Divisors of 6: \(\pm1,\ \pm2,\ \pm3,\ \pm6\). Try \(x=1\): \(\ 1-2-5+6=0\ \checkmark\). Divide with Ruffini:")
  + ruf_html([1, -2, -5, 6], 1)
  + D(r"(x-1)(x^2-x-6)=0\ \Rightarrow\ x=1\quad\text{%s}\quad x=\frac{1\pm\sqrt{1+24}}{2}=\frac{1\pm5}{2}=\begin{cases}3\\-2\end{cases}" % Lt('i', 'y', 'and'))
  + P(r"Solucions: \(x=1,\ x=3,\ x=-2\). Fixa't que el polinomi queda factoritzat: \(x^3-2x^2-5x+6=(x-1)(x-3)(x+2)\).", r"Soluciones: \(x=1,\ x=3,\ x=-2\). Fíjate en que el polinomio queda factorizado: \(x^3-2x^2-5x+6=(x-1)(x-3)(x+2)\).", r"Solutions: \(x=1,\ x=3,\ x=-2\). Notice the polynomial is now factorised: \(x^3-2x^2-5x+6=(x-1)(x-3)(x+2)\).")
  + note(r"Si el terme independent és 0, no cal Ruffini: \(x^3-x^2-6x=0\Rightarrow x(x^2-x-6)=0\Rightarrow x=0,\ x=3,\ x=-2\).", r"Si el término independiente es 0, no hace falta Ruffini: \(x^3-x^2-6x=0\Rightarrow x(x^2-x-6)=0\Rightarrow x=0,\ x=3,\ x=-2\).", r"If the constant term is 0, you don't need Ruffini: \(x^3-x^2-6x=0\Rightarrow x(x^2-x-6)=0\Rightarrow x=0,\ x=3,\ x=-2\).")
  + note(r"Una equació de tercer grau pot tindre menys de tres solucions: si l'equació de segon grau que queda té \(\Delta<0\), o si alguna solució es repeteix (solució <strong>doble</strong>).", r"Una ecuación de tercer grado puede tener menos de tres soluciones: si la ecuación de segundo grado que queda tiene \(\Delta<0\), o si alguna solución se repite (solución <strong>doble</strong>).", r"A cubic can have fewer than three solutions: if the leftover quadratic has \(\Delta<0\), or if a solution is repeated (a <strong>double</strong> solution).", '⚠')
  + widget('w-cub', '📐', L('Equacions de grau 3 (o 4) amb Ruffini', 'Ecuaciones de grado 3 (o 4) con Ruffini', 'Cubic (or quartic) equations with Ruffini'),
           ['<div class="wrow">' + tin('e', L('Equació', 'Ecuación', 'Equation'), 'x^3-2x^2-5x+6=0') + '</div>', HELP,
            quick([('x^3-2x^2-5x+6=0', 'x³−2x²−5x+6 = 0'), ('x^3-x^2-6x=0', 'x³−x²−6x = 0'), ('x^3-3x+2=0', 'x³−3x+2 = 0'), ('2x^3-3x^2-11x+6=0', '2x³−3x²−11x+6 = 0'), ('x^3+x^2+x+1=0', 'x³+x²+x+1 = 0'), ('x^4-5x^2+4=0', 'x⁴−5x²+4 = 0')])])
  + drill('cub', 'Entrena: equacions de tercer grau', 'Entrena: ecuaciones de tercer grado', 'Train: cubic equations', SETHINT))
ce('x^3-2x^2-5x+6=0', [1, 3, -2]); ce('x^3-x^2-6x=0', [0, 3, -2]); chk('(x-1)(x-3)(x+2)', 'x^3-2x^2-5x+6')
s6 += levels(
 [prob(L(r"Resol \(x^3-4x=0\).", r"Resuelve \(x^3-4x=0\).", r"Solve \(x^3-4x=0\)."),
       D(r"x(x^2-4)=0\ \Rightarrow\ \boxed{x=0}\quad\text{%s}\quad x^2=4\Rightarrow\boxed{x=\pm2}" % Lt('i', 'y', 'and')))],
 [prob(L(r"Resol \(x^3+2x^2-x-2=0\).", r"Resuelve \(x^3+2x^2-x-2=0\).", r"Solve \(x^3+2x^2-x-2=0\)."),
       P(r"Divisors de \(-2\): \(\pm1,\ \pm2\). Provem \(x=1\): \(1+2-1-2=0\ \checkmark\)", r"Divisores de \(-2\): \(\pm1,\ \pm2\). Probamos \(x=1\): \(1+2-1-2=0\ \checkmark\)", r"Divisors of \(-2\): \(\pm1,\ \pm2\). Try \(x=1\): \(1+2-1-2=0\ \checkmark\)"),
       ruf_html([1, 2, -1, -2], 1),
       D(r"x^2+3x+2=0\ \Rightarrow\ x=\frac{-3\pm1}{2}=\begin{cases}-1\\-2\end{cases}\qquad\boxed{x=1,\ x=-1,\ x=-2}")),
  prob(L(r"Resol \(x^3-3x+2=0\).", r"Resuelve \(x^3-3x+2=0\).", r"Solve \(x^3-3x+2=0\)."),
       P(r"Falta el terme en \(x^2\): a Ruffini hi posem un 0. Provem \(x=1\): \(1-3+2=0\ \checkmark\)", r"Falta el término en \(x^2\): en Ruffini ponemos un 0. Probamos \(x=1\): \(1-3+2=0\ \checkmark\)", r"There's no \(x^2\) term: put a 0 in Ruffini. Try \(x=1\): \(1-3+2=0\ \checkmark\)"),
       ruf_html([1, 0, -3, 2], 1),
       D(r"x^2+x-2=0\ \Rightarrow\ x=\frac{-1\pm3}{2}=\begin{cases}1\\-2\end{cases}"),
       P(r"La solució \(x=1\) ix dues vegades: és <strong>doble</strong>. Solucions: \(\boxed{x=1\ (\text{doble}),\ x=-2}\), perquè \(x^3-3x+2=(x-1)^2(x+2)\).", r"La solución \(x=1\) sale dos veces: es <strong>doble</strong>. Soluciones: \(\boxed{x=1\ (\text{doble}),\ x=-2}\), porque \(x^3-3x+2=(x-1)^2(x+2)\).", r"The solution \(x=1\) comes up twice: it's a <strong>double</strong> solution. Solutions: \(\boxed{x=1\ (\text{double}),\ x=-2}\), since \(x^3-3x+2=(x-1)^2(x+2)\)."))],
 [prob(L(r"Resol \(2x^3-3x^2-11x+6=0\).", r"Resuelve \(2x^3-3x^2-11x+6=0\).", r"Solve \(2x^3-3x^2-11x+6=0\)."),
       P(r"Provem els divisors de 6: \(P(1)=-6,\ P(-1)=12,\ P(2)=-12,\ P(-2)=-16-12+22+6=0\ \checkmark\)", r"Probamos los divisores de 6: \(P(1)=-6,\ P(-1)=12,\ P(2)=-12,\ P(-2)=-16-12+22+6=0\ \checkmark\)", r"Try the divisors of 6: \(P(1)=-6,\ P(-1)=12,\ P(2)=-12,\ P(-2)=-16-12+22+6=0\ \checkmark\)"),
       ruf_html([2, -3, -11, 6], -2),
       D(r"2x^2-7x+3=0\ \Rightarrow\ x=\frac{7\pm5}{4}=\begin{cases}3\\ \frac12\end{cases}\qquad\boxed{x=-2,\ x=3,\ x=\tfrac12}"),
       P(r"Quan el coeficient de \(x^3\) no és 1, també hi pot haver solucions fraccionàries, com \(\frac12\).", r"Cuando el coeficiente de \(x^3\) no es 1, también puede haber soluciones fraccionarias, como \(\frac12\).", r"When the coefficient of \(x^3\) isn't 1, there can also be fractional solutions, like \(\frac12\)."))])
ce('x^3-4x=0', [0, 2, -2]); ce('x^3+2x^2-x-2=0', [1, -1, -2]); ce('x^3-3x+2=0', [1, -2]); chk('(x-1)**2*(x+2)', 'x^3-3x+2'); ce('2x^3-3x^2-11x+6=0', [-2, 3, '1/2'])
assert [S('2x^3-3x^2-11x+6').subs(x, v) for v in (1, -1, 2)] == [-6, 12, -12]
s6 += practice([
  ('★', L(r"Resol: a) \(x^3-9x=0\); b) \(x^3+5x^2+6x=0\).", r"Resuelve: a) \(x^3-9x=0\); b) \(x^3+5x^2+6x=0\).", r"Solve: a) \(x^3-9x=0\); b) \(x^3+5x^2+6x=0\).")),
  ('★★', L(r"c) \(x^3-6x^2+11x-6=0\); d) \(x^3+x^2-4x-4=0\); e) \(x^3-3x^2+4=0\).", r"c) \(x^3-6x^2+11x-6=0\); d) \(x^3+x^2-4x-4=0\); e) \(x^3-3x^2+4=0\).", r"c) \(x^3-6x^2+11x-6=0\); d) \(x^3+x^2-4x-4=0\); e) \(x^3-3x^2+4=0\).")),
  ('★★★', L(r"f) \(x^3+x^2+x+1=0\); g) \(2x^3+x^2-5x+2=0\); h) \(x(x+1)(x-1)=6\).", r"f) \(x^3+x^2+x+1=0\); g) \(2x^3+x^2-5x+2=0\); h) \(x(x+1)(x-1)=6\).", r"f) \(x^3+x^2+x+1=0\); g) \(2x^3+x^2-5x+2=0\); h) \(x(x+1)(x-1)=6\)."))],
  D(r"\text{a)}\ x(x^2-9)=0:\ 0,\ \pm3\qquad \text{b)}\ x(x^2+5x+6)=0:\ 0,\ -2,\ -3")
  + D(r"\text{c)}\ (x-1)(x^2-5x+6)=0:\ 1,\ 2,\ 3\qquad \text{d)}\ (x+1)(x^2-4)=0:\ -1,\ \pm2\qquad \text{e)}\ (x+1)(x^2-4x+4)=0:\ -1,\ 2\ (\text{doble})")
  + D(r"\text{f)}\ (x+1)(x^2+1)=0:\ \text{%s}\ x=-1\qquad \text{g)}\ (x-1)(2x^2+3x-2)=0:\ 1,\ \frac12,\ -2" % Lt('només', 'solo', 'only'))
  + D(r"\text{h)}\ x^3-x-6=0\Rightarrow (x-2)(x^2+2x+3)=0\ (\Delta=-8):\ \text{%s}\ x=2" % Lt('només', 'solo', 'only')))
ce('x^3-9x=0', [0, 3, -3]); ce('x^3+5x^2+6x=0', [0, -2, -3]); ce('x^3-6x^2+11x-6=0', [1, 2, 3]); ce('x^3+x^2-4x-4=0', [-1, 2, -2]); ce('x^3-3x^2+4=0', [-1, 2])
ce('x^3+x^2+x+1=0', [-1]); ce('2x^3+x^2-5x+2=0', [1, '1/2', -2]); ce('x(x+1)(x-1)=6', [2]); chk('(x-2)(x^2+2x+3)', 'x^3-x-6'); chk('(x-1)(2x^2+3x-2)', '2x^3+x^2-5x+2')

# =====================================================================
# 5.7 Problemes amb equacions
# =====================================================================
TR7 = [("Un nombre i el seu doble", "Un número y su doble", "A number and twice it", r"x,\ 2x"),
       ("Dos nombres consecutius", "Dos números consecutivos", "Two consecutive numbers", r"x,\ x+1"),
       ("Dos nombres parells consecutius", "Dos números pares consecutivos", "Two consecutive even numbers", r"2x,\ 2x+2"),
       ("Dos nombres que sumen 20", "Dos números que suman 20", "Two numbers adding up to 20", r"x,\ 20-x"),
       ("Edat ara / d'ací a 5 anys / fa 3 anys", "Edad ahora / dentro de 5 años / hace 3 años", "Age now / in 5 years / 3 years ago", r"x,\ x+5,\ x-3"),
       ("Una fracció (2/5) d'una quantitat", "Una fracción (2/5) de una cantidad", "A fraction (2/5) of an amount", r"\frac{2}{5}x"),
       ("Rectangle d'altura x i base 3 m més llarga", "Rectángulo de altura x y base 3 m más larga", "Rectangle of height x and a base 3 m longer", r"P=2x+2(x+3),\ \ A=x(x+3)"),
       ("Triangle rectangle de catets x, y i hipotenusa h", "Triángulo rectángulo de catetos x, y e hipotenusa h", "Right triangle with legs x, y and hypotenuse h", r"x^2+y^2=h^2")]
s7 = box('prop', L('Com resolem un problema amb equacions', 'Cómo resolvemos un problema con ecuaciones', 'How to solve a word problem with equations'),
  ol(L(r"<strong>Llegim i entenem</strong> l'enunciat: quines dades tenim i què ens pregunten.", r"<strong>Leemos y entendemos</strong> el enunciado: qué datos tenemos y qué nos preguntan.", r"<strong>Read and understand</strong> the problem: what data you have and what you're asked."),
     L(r"<strong>Triem la incògnita</strong>: escrivim clarament què és \(x\) (normalment, el que ens pregunten) i expressem les altres quantitats en funció de \(x\).", r"<strong>Elegimos la incógnita</strong>: escribimos claramente qué es \(x\) (normalmente, lo que nos preguntan) y expresamos las otras cantidades en función de \(x\).", r"<strong>Choose the unknown</strong>: write down clearly what \(x\) is (usually what you're asked for) and express the other quantities in terms of \(x\)."),
     L(r"<strong>Plantegem l'equació</strong>: traduïm al llenguatge algebraic la relació de l'enunciat.", r"<strong>Planteamos la ecuación</strong>: traducimos al lenguaje algebraico la relación del enunciado.", r"<strong>Set up the equation</strong>: translate the relationship in the problem into algebra."),
     L(r"<strong>Resolem</strong> l'equació.", r"<strong>Resolvemos</strong> la ecuación.", r"<strong>Solve</strong> the equation."),
     L(r"<strong>Comprovem i interpretem</strong> la solució en el context: responem la pregunta amb una frase i descartem les solucions sense sentit (longituds negatives, persones decimals…).", r"<strong>Comprobamos e interpretamos</strong> la solución en el contexto: respondemos la pregunta con una frase y descartamos las soluciones sin sentido (longitudes negativas, personas decimales…).", r"<strong>Check and interpret</strong> the solution in context: answer the question in a sentence and discard solutions that make no sense (negative lengths, fractions of people…).")))
s7 += box('prop', L('Traduccions útils', 'Traducciones útiles', 'Useful translations'),
  '<div class="tbl-wrap"><table class="data narrow"><thead><tr><th>' + L('Enunciat', 'Enunciado', 'In words') + '</th><th>' + L('Expressió', 'Expresión', 'Expression') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td class="l">{L(va, es, en)}</td><td>\\({e}\\)</td></tr>' for va, es, en, e in TR7) + '</tbody></table></div>'
  + drill('prob', 'Entrena: planteja i resol', 'Entrena: plantea y resuelve', 'Train: set up and solve'))
s7 += levels(
 [prob(L(r"La suma de tres nombres consecutius és 84. Quins són?", r"La suma de tres números consecutivos es 84. ¿Cuáles son?", r"Three consecutive numbers add up to 84. What are they?"),
       P(r"Incògnita: \(x\) = el menor; els altres són \(x+1\) i \(x+2\).", r"Incógnita: \(x\) = el menor; los otros son \(x+1\) y \(x+2\).", r"Unknown: \(x\) = the smallest; the others are \(x+1\) and \(x+2\)."),
       D(r"x+(x+1)+(x+2)=84\ \Rightarrow\ 3x+3=84\ \Rightarrow\ 3x=81\ \Rightarrow\ x=27"),
       P(r"Els nombres són <strong>27, 28 i 29</strong>. Comprovació: \(27+28+29=84\) ✓", r"Los números son <strong>27, 28 y 29</strong>. Comprobación: \(27+28+29=84\) ✓", r"The numbers are <strong>27, 28 and 29</strong>. Check: \(27+28+29=84\) ✓")),
  prob(L(r"Una mare té 38 anys i el seu fill, 10. Quants anys han de passar perquè l'edat de la mare siga el doble que la del fill?", r"Una madre tiene 38 años y su hijo, 10. ¿Cuántos años tienen que pasar para que la edad de la madre sea el doble que la del hijo?", r"A mother is 38 and her son is 10. How many years until the mother is twice as old as her son?"),
       P(r"\(x\) = anys que han de passar. Aleshores la mare tindrà \(38+x\) i el fill \(10+x\).", r"\(x\) = años que tienen que pasar. Entonces la madre tendrá \(38+x\) y el hijo \(10+x\).", r"\(x\) = number of years. Then the mother will be \(38+x\) and the son \(10+x\)."),
       D(r"38+x=2(10+x)\ \Rightarrow\ 38+x=20+2x\ \Rightarrow\ 18=x"),
       P(r"D'ací a <strong>18 anys</strong>: la mare en tindrà 56 i el fill 28, que és la meitat ✓", r"Dentro de <strong>18 años</strong>: la madre tendrá 56 y el hijo 28, que es la mitad ✓", r"In <strong>18 years</strong>: the mother will be 56 and the son 28, which is half ✓"))],
 [prob(L(r"En una classe, \(\frac13\) de l'alumnat ve en autobús, \(\frac25\) a peu i els 8 restants en bicicleta. Quants alumnes hi ha?", r"En una clase, \(\frac13\) del alumnado viene en autobús, \(\frac25\) a pie y los 8 restantes en bicicleta. ¿Cuántos alumnos hay?", r"In a class, \(\frac13\) of the students come by bus, \(\frac25\) on foot and the other 8 by bike. How many students are there?"),
       P(r"\(x\) = nombre total d'alumnes. La suma de les tres parts és el total:", r"\(x\) = número total de alumnos. La suma de las tres partes es el total:", r"\(x\) = total number of students. The three parts add up to the total:"),
       D(r"\frac{x}{3}+\frac{2x}{5}+8=x\ \xrightarrow{\cdot15}\ 5x+6x+120=15x\ \Rightarrow\ 120=4x\ \Rightarrow\ x=30"),
       P(r"Hi ha <strong>30 alumnes</strong>: 10 en autobús, 12 a peu i 8 en bici ✓", r"Hay <strong>30 alumnos</strong>: 10 en autobús, 12 a pie y 8 en bici ✓", r"There are <strong>30 students</strong>: 10 by bus, 12 on foot and 8 by bike ✓")),
  prob(L(r"Un rectangle fa 3 m més de llarg que d'ample i la seua àrea és 40 m². Quines dimensions té?", r"Un rectángulo mide 3 m más de largo que de ancho y su área es 40 m². ¿Qué dimensiones tiene?", r"A rectangle is 3 m longer than it is wide and its area is 40 m². What are its dimensions?"),
       P(r"\(x\) = amplada; la llargària és \(x+3\).", r"\(x\) = anchura; la longitud es \(x+3\).", r"\(x\) = width; the length is \(x+3\)."),
       D(r"x(x+3)=40\ \Rightarrow\ x^2+3x-40=0\ \Rightarrow\ x=\frac{-3\pm\sqrt{9+160}}{2}=\frac{-3\pm13}{2}=\begin{cases}5\\-8\end{cases}"),
       P(r"Una longitud no pot ser negativa: descartem \(-8\). El rectangle fa <strong>5 m × 8 m</strong> ✓", r"Una longitud no puede ser negativa: descartamos \(-8\). El rectángulo mide <strong>5 m × 8 m</strong> ✓", r"A length can't be negative: discard \(-8\). The rectangle is <strong>5 m × 8 m</strong> ✓"))],
 [prob(L(r"Els catets d'un triangle rectangle mesuren \(x\) i \(x+7\) cm, i la hipotenusa 13 cm. Quant mesuren els catets?", r"Los catetos de un triángulo rectángulo miden \(x\) y \(x+7\) cm, y la hipotenusa 13 cm. ¿Cuánto miden los catetos?", r"The legs of a right triangle are \(x\) and \(x+7\) cm long and the hypotenuse is 13 cm. How long are the legs?"),
       P(r"Pel teorema de Pitàgores:", r"Por el teorema de Pitágoras:", r"By Pythagoras' theorem:"),
       D(r"x^2+(x+7)^2=13^2\ \Rightarrow\ 2x^2+14x+49=169\ \Rightarrow\ x^2+7x-60=0"),
       D(r"x=\frac{-7\pm\sqrt{49+240}}{2}=\frac{-7\pm17}{2}=\begin{cases}5\\-12\ (\text{%s})\end{cases}" % Lt('no val', 'no vale', 'not valid')),
       P(r"Els catets fan <strong>5 cm i 12 cm</strong>. Comprovació: \(25+144=169\) ✓", r"Los catetos miden <strong>5 cm y 12 cm</strong>. Comprobación: \(25+144=169\) ✓", r"The legs are <strong>5 cm and 12 cm</strong>. Check: \(25+144=169\) ✓")),
  prob(L(r"El producte de tres nombres naturals consecutius és 120. Quins són?", r"El producto de tres números naturales consecutivos es 120. ¿Cuáles son?", r"The product of three consecutive natural numbers is 120. What are they?"),
       D(r"x(x+1)(x+2)=120\ \Rightarrow\ x^3+3x^2+2x-120=0"),
       P(r"Provem divisors de 120: \(x=4\): \(64+48+8-120=0\ \checkmark\)", r"Probamos divisores de 120: \(x=4\): \(64+48+8-120=0\ \checkmark\)", r"Try divisors of 120: \(x=4\): \(64+48+8-120=0\ \checkmark\)"),
       ruf_html([1, 3, 2, -120], 4),
       P(r"Queda \(x^2+7x+30=0\), amb \(\Delta=49-120<0\): no té més solucions. Els nombres són <strong>4, 5 i 6</strong> (\(4\cdot5\cdot6=120\) ✓).", r"Queda \(x^2+7x+30=0\), con \(\Delta=49-120<0\): no tiene más soluciones. Los números son <strong>4, 5 y 6</strong> (\(4\cdot5\cdot6=120\) ✓).", r"That leaves \(x^2+7x+30=0\), with \(\Delta=49-120<0\): no more solutions. The numbers are <strong>4, 5 and 6</strong> (\(4\cdot5\cdot6=120\) ✓)."))])
ce('x+(x+1)+(x+2)=84', [27]); ce('38+x=2(10+x)', [18]); ce('x/3+2x/5+8=x', [30]); ce('x(x+3)=40', [5, -8]); ce('x^2+(x+7)^2=169', [5, -12]); ce('x(x+1)(x+2)=120', [4])
s7 += practice([
  ('★', L(r"a) Si al triple d'un nombre li restem 7, obtenim el mateix que si al seu doble li sumem 5. Quin nombre és? b) Pere té el triple de diners que Anna i entre els dos tenen 64 €. Quant en té cadascun?",
          r"a) Si al triple de un número le restamos 7, obtenemos lo mismo que si a su doble le sumamos 5. ¿Qué número es? b) Pedro tiene el triple de dinero que Ana y entre los dos tienen 64 €. ¿Cuánto tiene cada uno?",
          r"a) Three times a number minus 7 is the same as twice the number plus 5. What is the number? b) Pere has three times as much money as Anna and together they have €64. How much does each have?")),
  ('★★', L(r"c) Un pare té 42 anys i el seu fill 12. Fa quants anys l'edat del pare era el quàdruple de la del fill? d) La suma d'un nombre i el seu quadrat és 56. Quin nombre pot ser? e) En una granja hi ha gallines i conills: 30 caps i 84 potes. Quants animals hi ha de cada tipus?",
           r"c) Un padre tiene 42 años y su hijo 12. ¿Hace cuántos años la edad del padre era el cuádruple de la del hijo? d) La suma de un número y su cuadrado es 56. ¿Qué número puede ser? e) En una granja hay gallinas y conejos: 30 cabezas y 84 patas. ¿Cuántos animales hay de cada tipo?",
           r"c) A father is 42 and his son is 12. How many years ago was the father four times as old as his son? d) A number plus its square is 56. What could the number be? e) A farm has hens and rabbits: 30 heads and 84 legs. How many of each are there?")),
  ('★★★', L(r"f) Un jardí rectangular de 12 m × 8 m està envoltat per un camí d'amplada constant. Si l'àrea total (jardí i camí) és 165 m², quina amplada té el camí? g) Si augmentem 2 cm l'aresta d'un cub, el seu volum augmenta 98 cm³. Quant fa l'aresta?",
            r"f) Un jardín rectangular de 12 m × 8 m está rodeado por un camino de anchura constante. Si el área total (jardín y camino) es 165 m², ¿qué anchura tiene el camino? g) Si aumentamos 2 cm la arista de un cubo, su volumen aumenta 98 cm³. ¿Cuánto mide la arista?",
            r"f) A 12 m × 8 m rectangular garden is surrounded by a path of constant width. If the total area (garden and path) is 165 m², how wide is the path? g) Increasing the edge of a cube by 2 cm increases its volume by 98 cm³. How long is the edge?"))],
  D(r"\text{a)}\ 3x-7=2x+5\Rightarrow x=12\qquad \text{b)}\ x+3x=64\Rightarrow x=16:\ \text{Anna } 16\text{ €},\ \text{Pere } 48\text{ €}")
  + D(r"\text{c)}\ 42-x=4(12-x)\Rightarrow 3x=6\Rightarrow x=2\ \text{%s}\qquad \text{d)}\ x^2+x-56=0\Rightarrow x=7\ \text{%s}\ x=-8" % (Lt('anys', 'años', 'years'), Lt('o', 'o', 'or')))
  + D(r"\text{e)}\ 2x+4(30-x)=84\Rightarrow x=18:\ 18\ \text{%s},\ 12\ \text{%s}" % (Lt('gallines', 'gallinas', 'hens'), Lt('conills', 'conejos', 'rabbits')))
  + D(r"\text{f)}\ (12+2x)(8+2x)=165\Rightarrow 4x^2+40x-69=0\Rightarrow x=\frac{-40\pm52}{8}:\ x=1\dc5\ \text{m}")
  + D(r"\text{g)}\ (x+2)^3-x^3=98\Rightarrow 6x^2+12x-90=0\Rightarrow x^2+2x-15=0:\ x=3\ \text{cm}"))
ce('3x-7=2x+5', [12]); ce('x+3x=64', [16]); ce('42-x=4(12-x)', [2]); ce('x^2+x=56', [7, -8]); ce('2x+4(30-x)=84', [18]); ce('(12+2x)(8+2x)=165', ['3/2', '-23/2']); ce('(x+2)^3-x^3=98', [3, -5])

# ============================================================ muntatge
SECS = [
  (L('Equacions i identitats', 'Ecuaciones e identidades', 'Equations and identities'), s1),
  (L('Equacions de primer grau', 'Ecuaciones de primer grado', 'Linear equations'), s2),
  (L('Equacions de primer grau amb denominadors', 'Ecuaciones de primer grado con denominadores', 'Linear equations with fractions'), s3),
  (L('Equacions de segon grau incompletes', 'Ecuaciones de segundo grado incompletas', 'Incomplete quadratic equations'), s4),
  (L('Equacions de segon grau completes', 'Ecuaciones de segundo grado completas', 'Complete quadratic equations'), s5),
  (L('Equacions de tercer grau (Ruffini)', 'Ecuaciones de tercer grado (Ruffini)', "Cubic equations (Ruffini's rule)"), s6),
  (L('Problemes amb equacions', 'Problemas con ecuaciones', 'Word problems with equations'), s7),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Equacions · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 5 (Equacions) de 3r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "x=?";')
assert 'Equacions · FentMates' in head and 'content: "x=?"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()
assert 'NSEC = %d' % NS in js

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">5.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../3eso.html">{L("3r ESO", "3º ESO", "3rd ESO (Year 9)")}</a> / {L("Unitat 5", "Unidad 5", "Unit 5")}</span>
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
    <h1><span class="u">{L("Unitat 5", "Unidad 5", "Unit 5")}</span> · {L("Equacions", "Ecuaciones", "Equations")}</h1>
    <p>{L("Equacions i identitats, equacions de primer grau (amb parèntesis i denominadors), equacions de segon grau incompletes i completes, equacions de tercer grau amb Ruffini i problemes amb equacions: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Ecuaciones e identidades, ecuaciones de primer grado (con paréntesis y denominadores), ecuaciones de segundo grado incompletas y completas, ecuaciones de tercer grado con Ruffini y problemas con ecuaciones: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Equations and identities, linear equations (with brackets and fractions), incomplete and complete quadratic equations, cubic equations with Ruffini's rule and word problems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 5: Equacions · 3r ESO", "Apuntes de teoría · Unidad 5: Ecuaciones · 3º ESO", "Theory notes · Unit 5: Equations · 3rd ESO")}</p>
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
