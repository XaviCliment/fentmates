import os, re, sys

# Genera materials/1eso/t2-divisibilitat.html. Ús: python3 _eines/apunts/1eso-t2/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t2-divisibilitat.html")

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
def prob(q, *steps):
    return '<li><p class="prob-q">' + q + '</p><div class="steps">' + ''.join(f'<div class="step">{s}</div>' for s in steps) + '</div></li>\n'
def practice(items, sol):
    lis = ''.join(f'<li><span class="stars">{st}</span> {t}</li>' for st, t in items)
    return box('pr', '✍ ' + L('Practica', 'Practica', 'Practice'),
               f'<ol class="ex-list">{lis}</ol><details class="sol"><summary>{L("Mostra la solució", "Mostrar la solución", "Show the solution")}</summary><div>{sol}</div></details>')
def sec(i, title, body):
    return (f'\n<!-- ======================= 2.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">2.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def drill(kind, va, es, en):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="numeric" autocomplete="off" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs, attr='b'):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-{attr}="{v}">{t}</button>' for v, t in pairs) + '</div>'
def nin(k, va, es, en, val, cls='s'):
    return f'<label>{L(va, es, en)} <input class="tin {cls}" type="text" inputmode="numeric" data-k="{k}" value="{val}" autocomplete="off" aria-label="{k}"></label>'
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def col(rows):
    # mètode de la columna: [(nombre, factor primer), …, (1, '')]
    return r'\[\begin{array}{r|l}' + r'\\'.join(f'{a}&{b}' for a, b in rows) + r'\end{array}\]'
MCM = r'\tri{mcm}{mcm}{lcm}'
MCD = r'\tri{MCD}{MCD}{gcd}'
DV = r'\tri{Div}{Div}{Div}'
ML = r'\tri{M}{M}{M}'

# ============================================================ 2.1
s1 = box('def', L('La relació de divisibilitat', 'La relación de divisibilidad', 'The divisibility relation'),
  P(r"Dos nombres naturals \(a\) i \(b\) estan relacionats per <strong>divisibilitat</strong> quan la divisió \(a:b\) és <strong>exacta</strong>, és a dir, quan el residu és 0. Aleshores diem que:",
    r"Dos números naturales \(a\) y \(b\) están relacionados por <strong>divisibilidad</strong> cuando la división \(a:b\) es <strong>exacta</strong>, es decir, cuando el resto es 0. Entonces decimos que:",
    r"Two natural numbers \(a\) and \(b\) are related by <strong>divisibility</strong> when the division \(a:b\) is <strong>exact</strong>, that is, when the remainder is 0. Then we say that:")
  + ul(L(r"\(a\) <strong>és múltiple de</strong> \(b\)", r"\(a\) <strong>es múltiplo de</strong> \(b\)", r"\(a\) <strong>is a multiple of</strong> \(b\)"),
       L(r"\(b\) <strong>és divisor de</strong> \(a\) (o \(b\) <strong>divideix</strong> \(a\))", r"\(b\) <strong>es divisor de</strong> \(a\) (o \(b\) <strong>divide</strong> a \(a\))", r"\(b\) <strong>is a divisor</strong> (or factor) <strong>of</strong> \(a\), or \(b\) <strong>divides</strong> \(a\)"),
       L(r"\(a\) <strong>és divisible per</strong> \(b\)", r"\(a\) <strong>es divisible por</strong> \(b\)", r"\(a\) <strong>is divisible by</strong> \(b\)"))
  + r'\[\begin{array}{c|l}15&\,3\\\hline 0&\,5\end{array}\quad\Longleftrightarrow\quad 15=3\cdot5\]'
  + P(r"La divisió \(15:3=5\) és exacta: \(15\) és múltiple de \(3\) i \(3\) és divisor de \(15\). Com que \(15=3\cdot5\), també \(5\) és divisor de \(15\).",
      r"La división \(15:3=5\) es exacta: \(15\) es múltiplo de \(3\) y \(3\) es divisor de \(15\). Como \(15=3\cdot5\), también \(5\) es divisor de \(15\).",
      r"The division \(15:3=5\) is exact: \(15\) is a multiple of \(3\) and \(3\) is a divisor of \(15\). Since \(15=3\cdot5\), \(5\) is also a divisor of \(15\).")
  + r'\[15\ \xrightarrow{\ \tri{és múltiple de}{es múltiplo de}{is a multiple of}\ }\ 3\qquad\qquad 3\ \xrightarrow{\ \tri{és divisor de}{es divisor de}{is a divisor of}\ }\ 15\]'
  + P(r"En canvi, \(17:3\) dona quocient 5 i residu 2: <strong>no</strong> és exacta, així que \(17\) no és múltiple de \(3\) i \(3\) no és divisor de \(17\).",
      r"En cambio, \(17:3\) da cociente 5 y resto 2: <strong>no</strong> es exacta, así que \(17\) no es múltiplo de \(3\) y \(3\) no es divisor de \(17\).",
      r"However, \(17:3\) gives quotient 5 and remainder 2: it is <strong>not</strong> exact, so \(17\) is not a multiple of \(3\) and \(3\) is not a divisor of \(17\).")
  + note(r"«Ser múltiple de» i «ser divisor de» expliquen la mateixa relació, però llegida en sentits contraris: el múltiple és el nombre <strong>gran</strong> i el divisor, el <strong>xicotet</strong>.",
         r"«Ser múltiplo de» y «ser divisor de» explican la misma relación, pero leída en sentidos contrarios: el múltiplo es el número <strong>grande</strong> y el divisor, el <strong>pequeño</strong>.",
         r"“Being a multiple of” and “being a divisor of” describe the same relation read in opposite directions: the multiple is the <strong>big</strong> number and the divisor the <strong>small</strong> one."))
s1 += box('prop', L('Observa', 'Observa', 'Notice'),
  ul(L(r"Si \(a=b\cdot c\), aleshores \(a\) és múltiple de \(b\) i de \(c\), i \(b\) i \(c\) són divisors de \(a\): \(\ 42=6\cdot7\).", r"Si \(a=b\cdot c\), entonces \(a\) es múltiplo de \(b\) y de \(c\), y \(b\) y \(c\) son divisores de \(a\): \(\ 42=6\cdot7\).", r"If \(a=b\cdot c\), then \(a\) is a multiple of both \(b\) and \(c\), and \(b\) and \(c\) are divisors of \(a\): \(\ 42=6\cdot7\)."),
     L(r"L'<strong>1</strong> és divisor de tots els nombres, i cada nombre és divisor (i múltiple) d'<strong>ell mateix</strong>.", r"El <strong>1</strong> es divisor de todos los números, y cada número es divisor (y múltiplo) de <strong>sí mismo</strong>.", r"<strong>1</strong> is a divisor of every number, and every number is a divisor (and a multiple) of <strong>itself</strong>."),
     L(r"El <strong>0</strong> és múltiple de tots els nombres (\(0=b\cdot0\)), però no és divisor de cap, perquè no es pot dividir entre 0.", r"El <strong>0</strong> es múltiplo de todos los números (\(0=b\cdot0\)), pero no es divisor de ninguno, porque no se puede dividir entre 0.", r"<strong>0</strong> is a multiple of every number (\(0=b\cdot0\)), but it is not a divisor of any, because we can't divide by 0."))
  + f'''<div class="widget" id="w-rel">
  <div class="wt">🔗 {L("És múltiple? És divisor?", "¿Es múltiplo? ¿Es divisor?", "Multiple? Divisor?")}</div>
  <div class="wrow">{nin("a", "Nombre", "Número", "Number", "24")}<span class="op">:</span>{nin("b", "Divisor", "Divisor", "Divisor", "6")}</div>
  {quick([("24:6", "24 : 6"), ("30:4", "30 : 4"), ("91:7", "91 : 7"), ("45:1", "45 : 1"), ("9:9", "9 : 9"), ("0:5", "0 : 5"), ("100:8", "100 : 8"), ("143:11", "143 : 11")])}
  <div class="dots"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s1 += level(1, 1,
  prob(L(r"Comprova si \(72\) és múltiple de \(8\) i si \(9\) és divisor de \(75\).", r"Comprueba si \(72\) es múltiplo de \(8\) y si \(9\) es divisor de \(75\).", r"Check whether \(72\) is a multiple of \(8\) and whether \(9\) is a divisor of \(75\)."),
       P(r"\(72:8=9\) amb residu 0: la divisió és exacta, per tant <strong>sí</strong>, \(72\) és múltiple de \(8\) (\(72=8\cdot9\)).", r"\(72:8=9\) con resto 0: la división es exacta, por tanto <strong>sí</strong>, \(72\) es múltiplo de \(8\) (\(72=8\cdot9\)).", r"\(72:8=9\) with remainder 0: the division is exact, so <strong>yes</strong>, \(72\) is a multiple of \(8\) (\(72=8\cdot9\))."),
       P(r"\(75:9\) dona quocient 8 i residu 3 (\(9\cdot8+3=75\)): <strong>no</strong> és exacta, així que \(9\) no és divisor de \(75\).", r"\(75:9\) da cociente 8 y resto 3 (\(9\cdot8+3=75\)): <strong>no</strong> es exacta, así que \(9\) no es divisor de \(75\).", r"\(75:9\) gives quotient 8 and remainder 3 (\(9\cdot8+3=75\)): it is <strong>not</strong> exact, so \(9\) is not a divisor of \(75\).")),
  prob(L(r"A partir de la igualtat \(6\cdot7=42\), escriu quatre frases amb les paraules <em>múltiple</em> i <em>divisor</em>.", r"A partir de la igualdad \(6\cdot7=42\), escribe cuatro frases con las palabras <em>múltiplo</em> y <em>divisor</em>.", r"Starting from \(6\cdot7=42\), write four sentences using the words <em>multiple</em> and <em>divisor</em>."),
       P(r"\(42\) és múltiple de \(6\). &nbsp; \(42\) és múltiple de \(7\). &nbsp; \(6\) és divisor de \(42\). &nbsp; \(7\) és divisor de \(42\).", r"\(42\) es múltiplo de \(6\). &nbsp; \(42\) es múltiplo de \(7\). &nbsp; \(6\) es divisor de \(42\). &nbsp; \(7\) es divisor de \(42\).", r"\(42\) is a multiple of \(6\). &nbsp; \(42\) is a multiple of \(7\). &nbsp; \(6\) is a divisor of \(42\). &nbsp; \(7\) is a divisor of \(42\).")))
s1 += level(2, 3,
  prob(L(r"Quin és el nombre més xicotet que cal sumar a \(50\) perquè el resultat siga múltiple de \(7\)?", r"¿Cuál es el número más pequeño que hay que sumar a \(50\) para que el resultado sea múltiplo de \(7\)?", r"What is the smallest number we must add to \(50\) so that the result is a multiple of \(7\)?"),
       P(r"Dividim: \(50:7\) dona quocient 7 i residu 1, perquè \(7\cdot7=49\). El múltiple de 7 següent és \(7\cdot8=56\).", r"Dividimos: \(50:7\) da cociente 7 y resto 1, porque \(7\cdot7=49\). El múltiplo de 7 siguiente es \(7\cdot8=56\).", r"Divide: \(50:7\) gives quotient 7 and remainder 1, because \(7\cdot7=49\). The next multiple of 7 is \(7\cdot8=56\)."),
       r'\[56-50=\boxed{6}\]'),
  prob(L(r"Sense fer cap divisió, explica per què \(120\) és divisible per \(12\) i per \(10\).", r"Sin hacer ninguna división, explica por qué \(120\) es divisible por \(12\) y por \(10\).", r"Without dividing, explain why \(120\) is divisible by \(12\) and by \(10\)."),
       P(r"Perquè \(120=12\cdot10\). Si un nombre és el producte de dos factors, és múltiple de cadascun d'ells.", r"Porque \(120=12\cdot10\). Si un número es el producto de dos factores, es múltiplo de cada uno de ellos.", r"Because \(120=12\cdot10\). If a number is the product of two factors, it is a multiple of each of them.")))
s1 += level(3, 5,
  prob(L(r"En una divisió, el divisor és \(9\) i el quocient \(14\). Quin és el dividend si la divisió és exacta? I si el residu és el més gran possible?", r"En una división, el divisor es \(9\) y el cociente \(14\). ¿Cuál es el dividendo si la división es exacta? ¿Y si el resto es el mayor posible?", r"In a division the divisor is \(9\) and the quotient \(14\). What is the dividend if the division is exact? And if the remainder is as big as possible?"),
       P(r"Fem servir \(D=d\cdot q+r\). Si és exacta, \(r=0\):", r"Usamos \(D=d\cdot q+r\). Si es exacta, \(r=0\):", r"Use \(D=d\cdot q+r\). If it is exact, \(r=0\):") + r'\[D=9\cdot14=\boxed{126}\]',
       P(r"El residu sempre és menor que el divisor, així que com a molt val \(8\):", r"El resto siempre es menor que el divisor, así que como mucho vale \(8\):", r"The remainder is always less than the divisor, so it is at most \(8\):") + r'\[D=9\cdot14+8=\boxed{134}\]'))
s1 += practice([
  ('★', L(r"a) És \(91\) múltiple de \(7\)? b) És \(4\) divisor de \(50\)?", r"a) ¿Es \(91\) múltiplo de \(7\)? b) ¿Es \(4\) divisor de \(50\)?", r"a) Is \(91\) a multiple of \(7\)? b) Is \(4\) a divisor of \(50\)?")),
  ('★★', L(r"c) Escriu tots els nombres entre 50 i 80 dels quals \(8\) és divisor. d) Completa: «\(6\) és ___ de \(54\)» i «\(54\) és ___ de \(6\)».", r"c) Escribe todos los números entre 50 y 80 de los que \(8\) es divisor. d) Completa: «\(6\) es ___ de \(54\)» y «\(54\) es ___ de \(6\)».", r"c) Write all the numbers between 50 and 80 that have \(8\) as a divisor. d) Fill in: “\(6\) is a ___ of \(54\)” and “\(54\) is a ___ of \(6\)”.")),
  ('★★★', L(r"e) Vertader o fals: «\(0\) és múltiple de \(5\)», «\(0\) és divisor de \(5\)», «\(1\) és divisor de tots els nombres». f) Quin és el múltiple de \(25\) de tres xifres més gran?", r"e) Verdadero o falso: «\(0\) es múltiplo de \(5\)», «\(0\) es divisor de \(5\)», «\(1\) es divisor de todos los números». f) ¿Cuál es el mayor múltiplo de \(25\) de tres cifras?", r"e) True or false: “\(0\) is a multiple of \(5\)”, “\(0\) is a divisor of \(5\)”, “\(1\) is a divisor of every number”. f) What is the largest three-digit multiple of \(25\)?"))],
  P(r"a) Sí: \(91=7\cdot13\). &nbsp; b) No: \(50=4\cdot12+2\).", r"a) Sí: \(91=7\cdot13\). &nbsp; b) No: \(50=4\cdot12+2\).", r"a) Yes: \(91=7\cdot13\). &nbsp; b) No: \(50=4\cdot12+2\).")
  + P(r"c) \(56,\ 64,\ 72\). &nbsp; d) divisor; múltiple.", r"c) \(56,\ 64,\ 72\). &nbsp; d) divisor; múltiplo.", r"c) \(56,\ 64,\ 72\). &nbsp; d) divisor; multiple.")
  + P(r"e) V, F, V. &nbsp; f) \(975=25\cdot39\) (el següent, \(1000\), ja té quatre xifres).", r"e) V, F, V. &nbsp; f) \(975=25\cdot39\) (el siguiente, \(1000\), ya tiene cuatro cifras).", r"e) T, F, T. &nbsp; f) \(975=25\cdot39\) (the next one, \(1000\), has four digits)."))

# ============================================================ 2.2
s2 = box('def', L("Múltiples d'un nombre", 'Múltiplos de un número', 'Multiples of a number'),
  P(r"Els <strong>múltiples</strong> d'un nombre s'obtenen <strong>multiplicant-lo</strong> per \(0,\ 1,\ 2,\ 3,\ 4\ldots\) El conjunt dels múltiples de \(a\) s'escriu \(\text{M}(a)\):",
    r"Los <strong>múltiplos</strong> de un número se obtienen <strong>multiplicándolo</strong> por \(0,\ 1,\ 2,\ 3,\ 4\ldots\) El conjunto de los múltiplos de \(a\) se escribe \(\text{M}(a)\):",
    r"The <strong>multiples</strong> of a number are obtained by <strong>multiplying</strong> it by \(0,\ 1,\ 2,\ 3,\ 4\ldots\) The set of multiples of \(a\) is written \(\text{M}(a)\):")
  + r'\[\text{M}(6)=\{\,6\cdot0,\ 6\cdot1,\ 6\cdot2,\ 6\cdot3,\ \ldots\}=\{\,0,\ 6,\ 12,\ 18,\ 24,\ 30,\ 36,\ \ldots\}\]')
s2 += box('prop', L('Propietats dels múltiples', 'Propiedades de los múltiplos', 'Properties of multiples'),
  ul(L(r"Un nombre té <strong>infinits</strong> múltiples: la llista no s'acaba mai.", r"Un número tiene <strong>infinitos</strong> múltiplos: la lista no se acaba nunca.", r"A number has <strong>infinitely many</strong> multiples: the list never ends."),
     L(r"Tot nombre és múltiple d'ell mateix (\(a\cdot1=a\)) i el \(0\) és múltiple de tots (\(a\cdot0=0\)).", r"Todo número es múltiplo de sí mismo (\(a\cdot1=a\)) y el \(0\) es múltiplo de todos (\(a\cdot0=0\)).", r"Every number is a multiple of itself (\(a\cdot1=a\)) and \(0\) is a multiple of every number (\(a\cdot0=0\))."),
     L(r"Dos múltiples consecutius de \(a\) es diferencien en \(a\): anem «saltant de \(a\) en \(a\)».", r"Dos múltiplos consecutivos de \(a\) se diferencian en \(a\): vamos «saltando de \(a\) en \(a\)».", r"Two consecutive multiples of \(a\) differ by \(a\): we “jump in steps of \(a\)”."),
     L(r"La suma i la resta de dos múltiples de \(a\) també és múltiple de \(a\): \(\ 12+18=30\), tots múltiples de \(6\).", r"La suma y la resta de dos múltiplos de \(a\) también es múltiplo de \(a\): \(\ 12+18=30\), todos múltiplos de \(6\).", r"The sum and difference of two multiples of \(a\) are also multiples of \(a\): \(\ 12+18=30\), all multiples of \(6\)."))
  + note(r"Els múltiples de \(2\) són els nombres <strong>parells</strong>: \(0,\ 2,\ 4,\ 6,\ 8\ldots\) Els que no ho són, \(1,\ 3,\ 5,\ 7\ldots\), són els <strong>senars</strong>.",
         r"Los múltiplos de \(2\) son los números <strong>pares</strong>: \(0,\ 2,\ 4,\ 6,\ 8\ldots\) Los que no lo son, \(1,\ 3,\ 5,\ 7\ldots\), son los <strong>impares</strong>.",
         r"The multiples of \(2\) are the <strong>even</strong> numbers: \(0,\ 2,\ 4,\ 6,\ 8\ldots\) The rest, \(1,\ 3,\ 5,\ 7\ldots\), are the <strong>odd</strong> numbers.")
  + f'''<div class="widget" id="w-mult">
  <div class="wt">🟧 {L("Taula del 100: múltiples", "Tabla del 100: múltiplos", "Hundred square: multiples")}</div>
  <div class="wrow">{nin("n", "Múltiples de", "Múltiplos de", "Multiples of", "6")}{nin("m", "i de (opcional)", "y de (opcional)", "and of (optional)", "")}</div>
  {quick([("3", "3"), ("7", "7"), ("9", "9"), ("12", "12"), ("4,6", "4 i 6"), ("6,10", "6 i 10"), ("2,5", "2 i 5")])}
  <div class="hgrid"></div>
  <div class="legend"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('mult', 'Entrena: múltiples', 'Entrena: múltiplos', 'Train: multiples'))
s2 += level(1, 1,
  prob(L(r"Escriu els cinc primers múltiples de \(9\) diferents de zero.", r"Escribe los cinco primeros múltiplos de \(9\) distintos de cero.", r"Write the first five non-zero multiples of \(9\)."),
       r'\[9\cdot1=9,\quad 9\cdot2=18,\quad 9\cdot3=27,\quad 9\cdot4=36,\quad 9\cdot5=45\]'),
  prob(L(r"Quins d'aquests nombres són múltiples de \(7\)? \(\ 35,\ 47,\ 63,\ 70,\ 85\)", r"¿Cuáles de estos números son múltiplos de \(7\)? \(\ 35,\ 47,\ 63,\ 70,\ 85\)", r"Which of these numbers are multiples of \(7\)? \(\ 35,\ 47,\ 63,\ 70,\ 85\)"),
       P(r"Mirem si la divisió entre 7 és exacta: \(35=7\cdot5\), \(63=7\cdot9\) i \(70=7\cdot10\) sí; \(47=7\cdot6+5\) i \(85=7\cdot12+1\) no.", r"Miramos si la división entre 7 es exacta: \(35=7\cdot5\), \(63=7\cdot9\) y \(70=7\cdot10\) sí; \(47=7\cdot6+5\) y \(85=7\cdot12+1\) no.", r"Check whether dividing by 7 is exact: \(35=7\cdot5\), \(63=7\cdot9\) and \(70=7\cdot10\) yes; \(47=7\cdot6+5\) and \(85=7\cdot12+1\) no."),
       r'\[\boxed{35,\ 63,\ 70}\]'))
s2 += level(2, 3,
  prob(L(r"Escriu els múltiples de \(15\) compresos entre \(100\) i \(200\).", r"Escribe los múltiplos de \(15\) comprendidos entre \(100\) y \(200\).", r"Write the multiples of \(15\) between \(100\) and \(200\)."),
       P(r"Busquem el primer: \(100:15\) dona quocient 6 i residu 10 (\(15\cdot6=90\) encara no arriba). El primer és \(15\cdot7=105\).", r"Buscamos el primero: \(100:15\) da cociente 6 y resto 10 (\(15\cdot6=90\) todavía no llega). El primero es \(15\cdot7=105\).", r"Find the first one: \(100:15\) gives quotient 6 and remainder 10 (\(15\cdot6=90\) is still too small). The first is \(15\cdot7=105\)."),
       P(r"A partir d'ací, anem sumant 15 fins que ens passem de 200:", r"A partir de aquí, vamos sumando 15 hasta que nos pasamos de 200:", r"From there, keep adding 15 until we pass 200:") + r'\[\boxed{105,\ 120,\ 135,\ 150,\ 165,\ 180,\ 195}\]'))
s2 += level(3, 4,
  prob(L(r"Quin és el múltiple de \(23\) més pròxim a \(500\)?", r"¿Cuál es el múltiplo de \(23\) más próximo a \(500\)?", r"Which multiple of \(23\) is closest to \(500\)?"),
       P(r"\(500:23\) dona quocient 21 i residu 17. Els dos múltiples que «envolten» el 500 són:", r"\(500:23\) da cociente 21 y resto 17. Los dos múltiplos que «rodean» el 500 son:", r"\(500:23\) gives quotient 21 and remainder 17. The two multiples on either side of 500 are:") + r'\[23\cdot21=483\qquad 23\cdot22=506\]',
       P(r"Distàncies: \(500-483=17\) i \(506-500=6\). El més pròxim és \(\boxed{506}\).", r"Distancias: \(500-483=17\) y \(506-500=6\). El más próximo es \(\boxed{506}\).", r"Distances: \(500-483=17\) and \(506-500=6\). The closest is \(\boxed{506}\).")))
s2 += practice([
  ('★', L(r"a) Escriu els sis primers múltiples no nuls de \(12\). b) És \(84\) múltiple de \(4\)? I de \(6\)? I de \(9\)?", r"a) Escribe los seis primeros múltiplos no nulos de \(12\). b) ¿Es \(84\) múltiplo de \(4\)? ¿Y de \(6\)? ¿Y de \(9\)?", r"a) Write the first six non-zero multiples of \(12\). b) Is \(84\) a multiple of \(4\)? Of \(6\)? Of \(9\)?")),
  ('★★', L(r"c) Escriu els múltiples de \(11\) entre 50 i 100. d) Quants múltiples de \(8\) hi ha entre 1 i 100?", r"c) Escribe los múltiplos de \(11\) entre 50 y 100. d) ¿Cuántos múltiplos de \(8\) hay entre 1 y 100?", r"c) Write the multiples of \(11\) between 50 and 100. d) How many multiples of \(8\) are there from 1 to 100?")),
  ('★★★', L(r"e) Quin és el múltiple de \(37\) més xicotet que té quatre xifres? f) Escriu els múltiples comuns de \(4\) i de \(6\) menors que 50 (sense el 0).", r"e) ¿Cuál es el múltiplo de \(37\) más pequeño que tiene cuatro cifras? f) Escribe los múltiplos comunes de \(4\) y de \(6\) menores que 50 (sin el 0).", r"e) What is the smallest four-digit multiple of \(37\)? f) Write the common multiples of \(4\) and \(6\) below 50 (without 0)."))],
  P(r"a) \(12,\ 24,\ 36,\ 48,\ 60,\ 72\). &nbsp; b) De 4 sí (\(4\cdot21\)), de 6 sí (\(6\cdot14\)), de 9 no (\(84=9\cdot9+3\)).", r"a) \(12,\ 24,\ 36,\ 48,\ 60,\ 72\). &nbsp; b) De 4 sí (\(4\cdot21\)), de 6 sí (\(6\cdot14\)), de 9 no (\(84=9\cdot9+3\)).", r"a) \(12,\ 24,\ 36,\ 48,\ 60,\ 72\). &nbsp; b) Of 4 yes (\(4\cdot21\)), of 6 yes (\(6\cdot14\)), of 9 no (\(84=9\cdot9+3\)).")
  + P(r"c) \(55,\ 66,\ 77,\ 88,\ 99\). &nbsp; d) \(100:8\) dona quocient 12: n'hi ha \(12\) (del \(8\) al \(96\)).", r"c) \(55,\ 66,\ 77,\ 88,\ 99\). &nbsp; d) \(100:8\) da cociente 12: hay \(12\) (del \(8\) al \(96\)).", r"c) \(55,\ 66,\ 77,\ 88,\ 99\). &nbsp; d) \(100:8\) gives quotient 12: there are \(12\) (from \(8\) to \(96\)).")
  + P(r"e) \(37\cdot27=999\) encara té tres xifres: el següent, \(37\cdot28=1036\). &nbsp; f) \(12,\ 24,\ 36,\ 48\).", r"e) \(37\cdot27=999\) todavía tiene tres cifras: el siguiente, \(37\cdot28=1036\). &nbsp; f) \(12,\ 24,\ 36,\ 48\).", r"e) \(37\cdot27=999\) still has three digits: the next one is \(37\cdot28=1036\). &nbsp; f) \(12,\ 24,\ 36,\ 48\)."))

# ============================================================ 2.3
s3 = box('def', L("Divisors d'un nombre", 'Divisores de un número', 'Divisors of a number'),
  P(r"Els <strong>divisors</strong> d'un nombre són els nombres que el divideixen de manera exacta. El conjunt dels divisors de \(a\) s'escriu \(\text{Div}(a)\). Per a trobar-los tots, de manera ordenada:",
    r"Los <strong>divisores</strong> de un número son los números que lo dividen de forma exacta. El conjunto de los divisores de \(a\) se escribe \(\text{Div}(a)\). Para encontrarlos todos, de forma ordenada:",
    r"The <strong>divisors</strong> of a number are the numbers that divide it exactly. The set of divisors of \(a\) is written \(\text{Div}(a)\). To find them all in an orderly way:")
  + '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"Dividim el nombre entre \(1,\ 2,\ 3,\ 4\ldots\) per ordre.", r"Dividimos el número entre \(1,\ 2,\ 3,\ 4\ldots\) por orden.", r"Divide the number by \(1,\ 2,\ 3,\ 4\ldots\) in order."),
      L(r"Cada divisió <strong>exacta</strong> ens dona <strong>dos</strong> divisors: el divisor i el quocient.", r"Cada división <strong>exacta</strong> nos da <strong>dos</strong> divisores: el divisor y el cociente.", r"Each <strong>exact</strong> division gives us <strong>two</strong> divisors: the divisor and the quotient."),
      L(r"<strong>Parem</strong> quan el quocient es fa menor o igual que el divisor: a partir d'ací, les parelles es repetirien.", r"<strong>Paramos</strong> cuando el cociente se hace menor o igual que el divisor: a partir de ahí, las parejas se repetirían.", r"<strong>Stop</strong> when the quotient becomes less than or equal to the divisor: from then on, the pairs would repeat.")]) + '</ol>'
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Divisió', 'División', 'Division') + '</th>' + ''.join(f'<th>{t}</th>' for t in [r'\(36:1\)', r'\(36:2\)', r'\(36:3\)', r'\(36:4\)', r'\(36:5\)', r'\(36:6\)']) + '</tr></thead><tbody>'
  + '<tr><th>' + L('Resultat', 'Resultado', 'Result') + '</th>' + ''.join(f'<td>{t}</td>' for t in [r'\(36\)', r'\(18\)', r'\(12\)', r'\(9\)', r'\(7,\ r=1\)', r'\(6\)']) + '</tr>'
  + '<tr><th>' + L('Parella', 'Pareja', 'Pair') + '</th>' + ''.join(f'<td>{t}</td>' for t in [r'\(1\cdot36\)', r'\(2\cdot18\)', r'\(3\cdot12\)', r'\(4\cdot9\)', '✗', r'\(6\cdot6\)']) + '</tr></tbody></table></div>'
  + r'\[\text{Div}(36)=\{1,\ 2,\ 3,\ 4,\ 6,\ 9,\ 12,\ 18,\ 36\}\]'
  + P(r"En \(36:6\) el quocient (6) ja és igual que el divisor: parem. El \(6\) només el comptem una vegada.", r"En \(36:6\) el cociente (6) ya es igual que el divisor: paramos. El \(6\) solo lo contamos una vez.", r"In \(36:6\) the quotient (6) is already equal to the divisor: we stop. We only count \(6\) once."))
s3 += box('prop', L('Propietats dels divisors', 'Propiedades de los divisores', 'Properties of divisors'),
  ul(L(r"Un nombre té una quantitat <strong>finita</strong> de divisors.", r"Un número tiene una cantidad <strong>finita</strong> de divisores.", r"A number has a <strong>finite</strong> number of divisors."),
     L(r"El divisor més xicotet sempre és \(1\) i el més gran, el mateix nombre.", r"El divisor más pequeño siempre es \(1\) y el mayor, el propio número.", r"The smallest divisor is always \(1\) and the largest is the number itself."),
     L(r"Els divisors de \(a\) són les mesures dels <strong>rectangles</strong> que podem formar amb \(a\) quadrets: amb 12 quadrets podem fer rectangles de \(1\times12\), \(2\times6\) i \(3\times4\).", r"Los divisores de \(a\) son las medidas de los <strong>rectángulos</strong> que podemos formar con \(a\) cuadraditos: con 12 cuadraditos podemos hacer rectángulos de \(1\times12\), \(2\times6\) y \(3\times4\).", r"The divisors of \(a\) are the side lengths of the <strong>rectangles</strong> we can make with \(a\) squares: with 12 squares we can make \(1\times12\), \(2\times6\) and \(3\times4\) rectangles."))
  + f'''<div class="widget" id="w-divs">
  <div class="wt">🧱 {L("Buscador de divisors", "Buscador de divisores", "Divisor finder")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "36", "w")}</div>
  {quick([("12", "12"), ("24", "24"), ("36", "36"), ("48", "48"), ("17", "17"), ("60", "60"), ("100", "100"), ("360", "360")])}
  <div class="tbl-wrap dvt"></div>
  <div class="rects"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('divs', 'Entrena: quants divisors té?', 'Entrena: ¿cuántos divisores tiene?', 'Train: how many divisors?'))
s3 += level(1, 1,
  prob(L(r"Calcula tots els divisors de \(20\).", r"Calcula todos los divisores de \(20\).", r"Find all the divisors of \(20\)."),
       r'\[20:1=20\qquad 20:2=10\qquad 20:3\ (r=2)\qquad 20:4=5\qquad 20:5=4\ \ (\tri{parem}{paramos}{stop})\]',
       r'\[\text{Div}(20)=\boxed{\{1,\ 2,\ 4,\ 5,\ 10,\ 20\}}\]'),
  prob(L(r"És \(7\) divisor de \(63\)? I de \(64\)?", r"¿Es \(7\) divisor de \(63\)? ¿Y de \(64\)?", r"Is \(7\) a divisor of \(63\)? And of \(64\)?"),
       P(r"\(63=7\cdot9\): <strong>sí</strong>. &nbsp; \(64=7\cdot9+1\): <strong>no</strong>.", r"\(63=7\cdot9\): <strong>sí</strong>. &nbsp; \(64=7\cdot9+1\): <strong>no</strong>.", r"\(63=7\cdot9\): <strong>yes</strong>. &nbsp; \(64=7\cdot9+1\): <strong>no</strong>.")))
s3 += level(2, 3,
  prob(L(r"Calcula tots els divisors de \(60\). Quants en té?", r"Calcula todos los divisores de \(60\). ¿Cuántos tiene?", r"Find all the divisors of \(60\). How many are there?"),
       P(r"Parelles: \(1\cdot60,\ 2\cdot30,\ 3\cdot20,\ 4\cdot15,\ 5\cdot12,\ 6\cdot10\). Amb el 7 no és exacta, i en \(60:8\) el quocient (7) ja és menor que el divisor: parem.", r"Parejas: \(1\cdot60,\ 2\cdot30,\ 3\cdot20,\ 4\cdot15,\ 5\cdot12,\ 6\cdot10\). Con el 7 no es exacta, y en \(60:8\) el cociente (7) ya es menor que el divisor: paramos.", r"Pairs: \(1\cdot60,\ 2\cdot30,\ 3\cdot20,\ 4\cdot15,\ 5\cdot12,\ 6\cdot10\). Dividing by 7 isn't exact, and in \(60:8\) the quotient (7) is already less than the divisor: stop."),
       r'\[\text{Div}(60)=\{1,\ 2,\ 3,\ 4,\ 5,\ 6,\ 10,\ 12,\ 15,\ 20,\ 30,\ 60\}\ \to\ \boxed{12\ \tri{divisors}{divisores}{divisors}}\]'))
s3 += level(3, 4,
  prob(L(r"Amb 48 quadrats iguals, quants rectangles diferents podem formar si els fem servir tots? (Un rectangle de \(2\times24\) i un de \(24\times2\) compten com el mateix.)", r"Con 48 cuadrados iguales, ¿cuántos rectángulos diferentes podemos formar si los usamos todos? (Un rectángulo de \(2\times24\) y uno de \(24\times2\) cuentan como el mismo.)", r"With 48 equal squares, how many different rectangles can we make using all of them? (A \(2\times24\) and a \(24\times2\) rectangle count as the same one.)"),
       P(r"Cada rectangle correspon a una parella de divisors de 48 que, multiplicats, donen 48:", r"Cada rectángulo corresponde a una pareja de divisores de 48 que, multiplicados, dan 48:", r"Each rectangle is a pair of divisors of 48 whose product is 48:") + r'\[1\times48,\quad 2\times24,\quad 3\times16,\quad 4\times12,\quad 6\times8\]',
       P(r"Hi ha \(\boxed{5}\) rectangles diferents.", r"Hay \(\boxed{5}\) rectángulos diferentes.", r"There are \(\boxed{5}\) different rectangles.")))
s3 += practice([
  ('★', L(r"a) Calcula els divisors de \(18\). b) Calcula els divisors de \(13\).", r"a) Calcula los divisores de \(18\). b) Calcula los divisores de \(13\).", r"a) Find the divisors of \(18\). b) Find the divisors of \(13\).")),
  ('★★', L(r"c) Calcula els divisors de \(100\). d) Quin nombre entre 20 i 29 té més divisors?", r"c) Calcula los divisores de \(100\). d) ¿Qué número entre 20 y 29 tiene más divisores?", r"c) Find the divisors of \(100\). d) Which number from 20 to 29 has the most divisors?")),
  ('★★★', L(r"e) Una professora vol fer grups iguals amb els 30 alumnes de la classe, de 3 a 10 persones. Quines possibilitats té? f) Troba un nombre que tinga exactament 3 divisors.", r"e) Una profesora quiere hacer grupos iguales con los 30 alumnos de la clase, de 3 a 10 personas. ¿Qué posibilidades tiene? f) Encuentra un número que tenga exactamente 3 divisores.", r"e) A teacher wants to split the 30 students of a class into equal groups of 3 to 10 people. What are the options? f) Find a number with exactly 3 divisors."))],
  r'\[\text{a)}\ \{1,2,3,6,9,18\}\qquad \text{b)}\ \{1,13\}\qquad \text{c)}\ \{1,2,4,5,10,20,25,50,100\}\]'
  + P(r"d) El \(24\), amb 8 divisors: \(1,2,3,4,6,8,12,24\).", r"d) El \(24\), con 8 divisores: \(1,2,3,4,6,8,12,24\).", r"d) \(24\), with 8 divisors: \(1,2,3,4,6,8,12,24\).")
  + P(r"e) Divisors de 30 entre 3 i 10: grups de 3 (10 grups), de 5 (6 grups), de 6 (5 grups) o de 10 (3 grups). &nbsp; f) Per exemple \(4\) (\(1,2,4\)), \(9\) o \(25\): els quadrats de nombres primers.", r"e) Divisores de 30 entre 3 y 10: grupos de 3 (10 grupos), de 5 (6 grupos), de 6 (5 grupos) o de 10 (3 grupos). &nbsp; f) Por ejemplo \(4\) (\(1,2,4\)), \(9\) o \(25\): los cuadrados de números primos.", r"e) Divisors of 30 from 3 to 10: groups of 3 (10 groups), 5 (6 groups), 6 (5 groups) or 10 (3 groups). &nbsp; f) For example \(4\) (\(1,2,4\)), \(9\) or \(25\): the squares of prime numbers."))

# ============================================================ 2.4
CR = [
  ('2', L("L'última xifra és <strong>parella</strong>: 0, 2, 4, 6 o 8.", "La última cifra es <strong>par</strong>: 0, 2, 4, 6 u 8.", "The last digit is <strong>even</strong>: 0, 2, 4, 6 or 8."), r'\(3546\)', r'\(1237\)'),
  ('3', L("La <strong>suma de les xifres</strong> és múltiple de 3.", "La <strong>suma de las cifras</strong> es múltiplo de 3.", "The <strong>sum of the digits</strong> is a multiple of 3."), r'\(2715\to 15\)', r'\(1001\to 2\)'),
  ('5', L("L'última xifra és <strong>0 o 5</strong>.", "La última cifra es <strong>0 o 5</strong>.", "The last digit is <strong>0 or 5</strong>."), r'\(2715\)', r'\(552\)'),
  ('9', L("La <strong>suma de les xifres</strong> és múltiple de 9.", "La <strong>suma de las cifras</strong> es múltiplo de 9.", "The <strong>sum of the digits</strong> is a multiple of 9."), r'\(5481\to 18\)', r'\(2715\to 15\)'),
  ('11', L("Sumem les xifres de lloc <strong>senar</strong> i les de lloc <strong>parell</strong> (comptant des de la dreta). La <strong>diferència</strong> és 0 o múltiple d'11.", "Sumamos las cifras de lugar <strong>impar</strong> y las de lugar <strong>par</strong> (contando desde la derecha). La <strong>diferencia</strong> es 0 o múltiplo de 11.", "Add the digits in <strong>odd</strong> places and those in <strong>even</strong> places (counting from the right). The <strong>difference</strong> is 0 or a multiple of 11."), r'\(8261\to 14-3=11\)', r'\(1234\to 6-4=2\)'),
]
s4 = P(r"Els <strong>criteris de divisibilitat</strong> són regles que ens diuen si un nombre és divisible per un altre <strong>sense haver de fer la divisió</strong>.",
       r"Los <strong>criterios de divisibilidad</strong> son reglas que nos dicen si un número es divisible por otro <strong>sin tener que hacer la división</strong>.",
       r"<strong>Divisibility rules</strong> tell us whether a number is divisible by another one <strong>without doing the division</strong>.")
s4 += box('def', L('Criteris de divisibilitat', 'Criterios de divisibilidad', 'Divisibility rules'),
  '<div class="tbl-wrap"><table class="data crit-t"><thead><tr><th>' + L('Divisible per', 'Divisible por', 'Divisible by') + '</th><th>' + L('Criteri', 'Criterio', 'Rule') + '</th><th>' + L('Sí', 'Sí', 'Yes') + '</th><th>' + L('No', 'No', 'No') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><th class="cn">{n}</th><td class="l">{t}</td><td>{y}</td><td>{x}</td></tr>' for n, t, y, x in CR) + '</tbody></table></div>'
  + P(r"Exemple amb el 11: en \(8261\), les xifres de lloc senar són \(1\) i \(2\) (suma 3) i les de lloc parell, \(6\) i \(8\) (suma 14). La diferència és \(14-3=11\), així que \(8261\) és divisible per 11 (\(8261=11\cdot751\)).",
      r"Ejemplo con el 11: en \(8261\), las cifras de lugar impar son \(1\) y \(2\) (suma 3) y las de lugar par, \(6\) y \(8\) (suma 14). La diferencia es \(14-3=11\), así que \(8261\) es divisible por 11 (\(8261=11\cdot751\)).",
      r"Example with 11: in \(8261\), the digits in odd places are \(1\) and \(2\) (sum 3) and those in even places are \(6\) and \(8\) (sum 14). The difference is \(14-3=11\), so \(8261\) is divisible by 11 (\(8261=11\cdot751\))."))
s4 += box('prop', L('Trucs i observacions', 'Trucos y observaciones', 'Tips and remarks'),
  ul(L(r"Si la suma de les xifres és gran, podem tornar a sumar-ne les xifres: \(\ 98\,766\to36\to9\).", r"Si la suma de las cifras es grande, podemos volver a sumar sus cifras: \(\ 98\,766\to36\to9\).", r"If the digit sum is big, add its digits again: \(\ 98\,766\to36\to9\)."),
     L(r"Tot nombre divisible per <strong>9</strong> també ho és per <strong>3</strong>, però no al revés: \(12\) és divisible per 3 i no per 9.", r"Todo número divisible por <strong>9</strong> también lo es por <strong>3</strong>, pero no al revés: \(12\) es divisible por 3 y no por 9.", r"Every number divisible by <strong>9</strong> is also divisible by <strong>3</strong>, but not the other way round: \(12\) is divisible by 3 but not by 9."),
     L(r"Un nombre és divisible per <strong>10</strong> si acaba en 0. Aleshores també ho és per 2 i per 5.", r"Un número es divisible por <strong>10</strong> si acaba en 0. Entonces también lo es por 2 y por 5.", r"A number is divisible by <strong>10</strong> if it ends in 0. Then it is also divisible by 2 and 5."),
     L(r"En el criteri de l'11, restem sempre la suma <strong>més gran</strong> menys la <strong>més xicoteta</strong>.", r"En el criterio del 11, restamos siempre la suma <strong>mayor</strong> menos la <strong>menor</strong>.", r"In the rule for 11, always subtract the <strong>smaller</strong> sum from the <strong>bigger</strong> one."))
  + f'''<div class="widget" id="w-crit">
  <div class="wt">🔍 {L("Detector de divisibilitat", "Detector de divisibilidad", "Divisibility detector")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "4950", "w")}</div>
  {quick([("4950", "4950"), ("2715", "2715"), ("8261", "8261"), ("5481", "5481"), ("1001", "1001"), ("123456", "123 456"), ("98766", "98 766")])}
  <div class="cdig"></div>
  <div class="ccards"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('crit', 'Entrena: quina xifra falta?', 'Entrena: ¿qué cifra falta?', 'Train: which digit is missing?'))
s4 += level(1, 1,
  prob(L(r"Per quins d'aquests nombres és divisible \(4950\): 2, 3, 5, 9, 11?", r"¿Por cuáles de estos números es divisible \(4950\): 2, 3, 5, 9, 11?", r"Which of these numbers divide \(4950\): 2, 3, 5, 9, 11?"),
       P(r"Acaba en 0: és divisible per <strong>2</strong> i per <strong>5</strong>.", r"Acaba en 0: es divisible por <strong>2</strong> y por <strong>5</strong>.", r"It ends in 0: it is divisible by <strong>2</strong> and by <strong>5</strong>."),
       P(r"Suma de xifres: \(4+9+5+0=18\), que és múltiple de 3 i de 9: és divisible per <strong>3</strong> i per <strong>9</strong>.", r"Suma de cifras: \(4+9+5+0=18\), que es múltiplo de 3 y de 9: es divisible por <strong>3</strong> y por <strong>9</strong>.", r"Digit sum: \(4+9+5+0=18\), a multiple of 3 and of 9: it is divisible by <strong>3</strong> and <strong>9</strong>."),
       P(r"Lloc senar: \(0+9=9\); lloc parell: \(5+4=9\). Diferència \(9-9=0\): també és divisible per <strong>11</strong>. Ho és per tots!", r"Lugar impar: \(0+9=9\); lugar par: \(5+4=9\). Diferencia \(9-9=0\): también es divisible por <strong>11</strong>. ¡Lo es por todos!", r"Odd places: \(0+9=9\); even places: \(5+4=9\). Difference \(9-9=0\): it is also divisible by <strong>11</strong>. It's divisible by all of them!")),
  prob(L(r"Escriu tres nombres de tres xifres que siguen divisibles per 2 i per 5 alhora.", r"Escribe tres números de tres cifras que sean divisibles por 2 y por 5 a la vez.", r"Write three three-digit numbers that are divisible by both 2 and 5."),
       P(r"Per a ser divisible per 2 ha d'acabar en parell i per a ser-ho per 5, en 0 o 5. Totes dues coses alhora: ha d'<strong>acabar en 0</strong>. Per exemple, \(\boxed{120,\ 350,\ 990}\).", r"Para ser divisible por 2 tiene que acabar en par y para serlo por 5, en 0 o 5. Las dos cosas a la vez: tiene que <strong>acabar en 0</strong>. Por ejemplo, \(\boxed{120,\ 350,\ 990}\).", r"To be divisible by 2 it must end in an even digit, and by 5 it must end in 0 or 5. Both at once: it must <strong>end in 0</strong>. For example, \(\boxed{120,\ 350,\ 990}\).")))
s4 += level(2, 3,
  prob(L(r"Quines xifres podem posar en el lloc de \(\square\) perquè \(7\square2\) siga divisible per 3? I per 9?", r"¿Qué cifras podemos poner en el lugar de \(\square\) para que \(7\square2\) sea divisible por 3? ¿Y por 9?", r"Which digits can replace \(\square\) so that \(7\square2\) is divisible by 3? And by 9?"),
       P(r"Les xifres conegudes sumen \(7+2=9\). Necessitem que \(9+\square\) siga múltiple de 3: \(\square=0,\ 3,\ 6\) o \(9\) → \(\boxed{702,\ 732,\ 762,\ 792}\).", r"Las cifras conocidas suman \(7+2=9\). Necesitamos que \(9+\square\) sea múltiplo de 3: \(\square=0,\ 3,\ 6\) o \(9\) → \(\boxed{702,\ 732,\ 762,\ 792}\).", r"The known digits add up to \(7+2=9\). We need \(9+\square\) to be a multiple of 3: \(\square=0,\ 3,\ 6\) or \(9\) → \(\boxed{702,\ 732,\ 762,\ 792}\)."),
       P(r"Per a 9 cal que \(9+\square\) siga 9 o 18: \(\square=0\) o \(9\) → \(\boxed{702,\ 792}\).", r"Para 9 hace falta que \(9+\square\) sea 9 o 18: \(\square=0\) o \(9\) → \(\boxed{702,\ 792}\).", r"For 9 we need \(9+\square\) to be 9 or 18: \(\square=0\) or \(9\) → \(\boxed{702,\ 792}\).")),
  prob(L(r"És \(2728\) divisible per 11?", r"¿Es \(2728\) divisible por 11?", r"Is \(2728\) divisible by 11?"),
       P(r"Des de la dreta: lloc senar \(8+7=15\); lloc parell \(2+2=4\). Diferència: \(15-4=11\), que és múltiple d'11. <strong>Sí</strong>: \(2728=11\cdot248\).", r"Desde la derecha: lugar impar \(8+7=15\); lugar par \(2+2=4\). Diferencia: \(15-4=11\), que es múltiplo de 11. <strong>Sí</strong>: \(2728=11\cdot248\).", r"From the right: odd places \(8+7=15\); even places \(2+2=4\). Difference: \(15-4=11\), a multiple of 11. <strong>Yes</strong>: \(2728=11\cdot248\).")))
s4 += level(3, 5,
  prob(L(r"Troba el nombre més xicotet de quatre xifres que és divisible per 2, per 3, per 5 i per 9 alhora.", r"Encuentra el número más pequeño de cuatro cifras que es divisible por 2, por 3, por 5 y por 9 a la vez.", r"Find the smallest four-digit number that is divisible by 2, 3, 5 and 9 all at once."),
       P(r"Per 2 i per 5 → ha d'acabar en 0. Per 9 → la suma de les xifres ha de ser múltiple de 9 (i aleshores ja és divisible per 3).", r"Por 2 y por 5 → tiene que acabar en 0. Por 9 → la suma de las cifras tiene que ser múltiplo de 9 (y entonces ya es divisible por 3).", r"By 2 and 5 → it must end in 0. By 9 → the digit sum must be a multiple of 9 (and then it's already divisible by 3)."),
       P(r"Volem el més xicotet: comença per \(10\square0\). La suma és \(1+\square\), que ha de ser 9: \(\square=8\).", r"Queremos el menor: empieza por \(10\square0\). La suma es \(1+\square\), que tiene que ser 9: \(\square=8\).", r"We want the smallest: it starts \(10\square0\). The sum is \(1+\square\), which must be 9: \(\square=8\).") + r'\[\boxed{1080}\]'))
s4 += practice([
  ('★', L(r"a) És \(3465\) divisible per 3? I per 5? I per 9? b) Per quins dels nombres 2, 3 i 5 és divisible \(7020\)?", r"a) ¿Es \(3465\) divisible por 3? ¿Y por 5? ¿Y por 9? b) ¿Por cuáles de los números 2, 3 y 5 es divisible \(7020\)?", r"a) Is \(3465\) divisible by 3? By 5? By 9? b) Which of 2, 3 and 5 divide \(7020\)?")),
  ('★★', L(r"c) És \(5841\) divisible per 11? d) Quines xifres pot tindre \(\square\) perquè \(4\square5\) siga divisible per 9?", r"c) ¿Es \(5841\) divisible por 11? d) ¿Qué cifras puede tener \(\square\) para que \(4\square5\) sea divisible por 9?", r"c) Is \(5841\) divisible by 11? d) Which digits can \(\square\) be so that \(4\square5\) is divisible by 9?")),
  ('★★★', L(r"e) Troba tots els nombres de tres xifres divisibles per 2, 3, 5 i 11 alhora. f) Si un nombre és divisible per 9, ho és també per 3? I si és divisible per 3, ho és per 9?", r"e) Encuentra todos los números de tres cifras divisibles por 2, 3, 5 y 11 a la vez. f) Si un número es divisible por 9, ¿lo es también por 3? ¿Y si es divisible por 3, lo es por 9?", r"e) Find all three-digit numbers divisible by 2, 3, 5 and 11 at once. f) If a number is divisible by 9, is it divisible by 3? And if it's divisible by 3, is it divisible by 9?"))],
  P(r"a) Suma 18: per 3 sí, per 9 sí; acaba en 5: per 5 sí. &nbsp; b) Acaba en 0 i suma 9: per tots tres.", r"a) Suma 18: por 3 sí, por 9 sí; acaba en 5: por 5 sí. &nbsp; b) Acaba en 0 y suma 9: por los tres.", r"a) Digit sum 18: by 3 yes, by 9 yes; ends in 5: by 5 yes. &nbsp; b) Ends in 0 and digit sum 9: by all three.")
  + P(r"c) Lloc senar \(1+8=9\), lloc parell \(4+5=9\): diferència 0, sí (\(5841=11\cdot531\)). &nbsp; d) \(4+5+\square\) ha de ser 9 o 18: \(\square=0\) o \(9\) (\(405\) i \(495\)).", r"c) Lugar impar \(1+8=9\), lugar par \(4+5=9\): diferencia 0, sí (\(5841=11\cdot531\)). &nbsp; d) \(4+5+\square\) tiene que ser 9 o 18: \(\square=0\) o \(9\) (\(405\) y \(495\)).", r"c) Odd places \(1+8=9\), even places \(4+5=9\): difference 0, yes (\(5841=11\cdot531\)). &nbsp; d) \(4+5+\square\) must be 9 or 18: \(\square=0\) or \(9\) (\(405\) and \(495\)).")
  + P(r"e) Ha d'acabar en 0 i, per l'11, les dues primeres xifres han de ser iguals: \(110, 220, \ldots, 990\). Per 3, la suma (el doble de la xifra) ha de ser múltiple de 3: \(330,\ 660,\ 990\). &nbsp; f) Sí; no (per exemple, \(12\)).", r"e) Tiene que acabar en 0 y, por el 11, las dos primeras cifras tienen que ser iguales: \(110, 220, \ldots, 990\). Por 3, la suma (el doble de la cifra) tiene que ser múltiplo de 3: \(330,\ 660,\ 990\). &nbsp; f) Sí; no (por ejemplo, \(12\)).", r"e) It must end in 0 and, for 11, the first two digits must be equal: \(110, 220, \ldots, 990\). For 3, the digit sum (twice that digit) must be a multiple of 3: \(330,\ 660,\ 990\). &nbsp; f) Yes; no (for example, \(12\))."))

# ============================================================ 2.5
s5 = box('def', L('Nombres primers i compostos', 'Números primos y compuestos', 'Prime and composite numbers'),
  ul(L(r"Un nombre és <strong>primer</strong> si té exactament <strong>dos divisors</strong>: l'1 i ell mateix. &nbsp; \(\text{Div}(7)=\{1,\ 7\}\)", r"Un número es <strong>primo</strong> si tiene exactamente <strong>dos divisores</strong>: el 1 y él mismo. &nbsp; \(\text{Div}(7)=\{1,\ 7\}\)", r"A number is <strong>prime</strong> if it has exactly <strong>two divisors</strong>: 1 and itself. &nbsp; \(\text{Div}(7)=\{1,\ 7\}\)"),
     L(r"Un nombre és <strong>compost</strong> si té <strong>més de dos</strong> divisors. &nbsp; \(\text{Div}(12)=\{1,\ 2,\ 3,\ 4,\ 6,\ 12\}\)", r"Un número es <strong>compuesto</strong> si tiene <strong>más de dos</strong> divisores. &nbsp; \(\text{Div}(12)=\{1,\ 2,\ 3,\ 4,\ 6,\ 12\}\)", r"A number is <strong>composite</strong> if it has <strong>more than two</strong> divisors. &nbsp; \(\text{Div}(12)=\{1,\ 2,\ 3,\ 4,\ 6,\ 12\}\)"),
     L(r"L'<strong>1</strong> no és ni primer ni compost: només té un divisor.", r"El <strong>1</strong> no es ni primo ni compuesto: solo tiene un divisor.", r"<strong>1</strong> is neither prime nor composite: it only has one divisor."))
  + P(r"Un nombre compost es pot escriure com a producte de dos nombres més xicotets (\(12=3\cdot4\)); un primer, no.", r"Un número compuesto se puede escribir como producto de dos números más pequeños (\(12=3\cdot4\)); un primo, no.", r"A composite number can be written as a product of two smaller numbers (\(12=3\cdot4\)); a prime can't.")
  + note(r"El <strong>2</strong> és l'únic nombre primer parell: tots els altres parells són múltiples de 2.", r"El <strong>2</strong> es el único número primo par: todos los demás pares son múltiplos de 2.", r"<strong>2</strong> is the only even prime: every other even number is a multiple of 2."))
s5 += box('prop', L("El garbell d'Eratòstenes", 'La criba de Eratóstenes', 'The sieve of Eratosthenes'),
  P(r"Fa més de 2000 anys, el grec Eratòstenes va inventar un mètode per a trobar tots els primers fins a un nombre: escrivim els nombres, ratllem l'1 i, per ordre, encerclem cada primer i <strong>ratllem tots els seus múltiples</strong>. Els que no queden ratllats són primers.",
    r"Hace más de 2000 años, el griego Eratóstenes inventó un método para encontrar todos los primos hasta un número: escribimos los números, tachamos el 1 y, por orden, rodeamos cada primo y <strong>tachamos todos sus múltiplos</strong>. Los que no quedan tachados son primos.",
    r"Over 2000 years ago, the Greek Eratosthenes invented a method to find all the primes up to a number: write the numbers, cross out 1 and then, in order, circle each prime and <strong>cross out all its multiples</strong>. The numbers left uncrossed are prime.")
  + f'''<div class="widget" id="w-sieve">
  <div class="wt">🧹 {L("Garbell d'Eratòstenes fins a 100", "Criba de Eratóstenes hasta 100", "Sieve of Eratosthenes up to 100")}</div>
  <div class="sieve"></div>
  <div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><button class="btn" type="button" data-a="reset">↺</button></div>
  <div class="info" aria-live="polite"></div>
</div>'''
  + r'\[\tri{Primers menors que 100}{Primos menores que 100}{Primes below 100}:\ 2,\,3,\,5,\,7,\,11,\,13,\,17,\,19,\,23,\,29,\,31,\,37,\,41,\,43,\,47,\,53,\,59,\,61,\,67,\,71,\,73,\,79,\,83,\,89,\,97\]')
s5 += box('prop', L('Com sabem si un nombre és primer?', '¿Cómo sabemos si un número es primo?', 'How do we know if a number is prime?'),
  P(r"El dividim per ordre entre els primers \(2,\ 3,\ 5,\ 7,\ 11\ldots\) (amb ajuda dels criteris).", r"Lo dividimos por orden entre los primos \(2,\ 3,\ 5,\ 7,\ 11\ldots\) (con ayuda de los criterios).", r"Divide it in order by the primes \(2,\ 3,\ 5,\ 7,\ 11\ldots\) (using the divisibility rules).")
  + ul(L(r"Si alguna divisió és exacta, el nombre és <strong>compost</strong>.", r"Si alguna división es exacta, el número es <strong>compuesto</strong>.", r"If one division is exact, the number is <strong>composite</strong>."),
       L(r"Si arribem a una divisió on el <strong>quocient és menor que el divisor</strong> sense cap divisió exacta, el nombre és <strong>primer</strong>.", r"Si llegamos a una división donde el <strong>cociente es menor que el divisor</strong> sin ninguna división exacta, el número es <strong>primo</strong>.", r"If we reach a division where the <strong>quotient is less than the divisor</strong> without any exact division, the number is <strong>prime</strong>."))
  + P(r"Exemple: \(113\) no és divisible per 2, 3 (suma 5), 5 ni 7 (\(113=7\cdot16+1\)). En \(113:11\) el quocient és 10, menor que 11: \(113\) és <strong>primer</strong>.", r"Ejemplo: \(113\) no es divisible por 2, 3 (suma 5), 5 ni 7 (\(113=7\cdot16+1\)). En \(113:11\) el cociente es 10, menor que 11: \(113\) es <strong>primo</strong>.", r"Example: \(113\) is not divisible by 2, 3 (digit sum 5), 5 or 7 (\(113=7\cdot16+1\)). In \(113:11\) the quotient is 10, less than 11: \(113\) is <strong>prime</strong>.")
  + f'''<div class="widget" id="w-prime">
  <div class="wt">🔎 {L("És primer?", "¿Es primo?", "Is it prime?")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "113", "w")}</div>
  {quick([("91", "91"), ("97", "97"), ("113", "113"), ("127", "127"), ("221", "221"), ("323", "323"), ("1001", "1001"), ("2027", "2027")])}
  <div class="tbl-wrap pvt2"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s5 += level(1, 1,
  prob(L(r"Classifica en primers i compostos: \(\ 15,\ 17,\ 21,\ 29,\ 1,\ 51\).", r"Clasifica en primos y compuestos: \(\ 15,\ 17,\ 21,\ 29,\ 1,\ 51\).", r"Sort into primes and composites: \(\ 15,\ 17,\ 21,\ 29,\ 1,\ 51\)."),
       P(r"<strong>Primers:</strong> \(17\) i \(29\) (només són divisibles per 1 i per ells mateixos).", r"<strong>Primos:</strong> \(17\) y \(29\) (solo son divisibles por 1 y por sí mismos).", r"<strong>Primes:</strong> \(17\) and \(29\) (only divisible by 1 and themselves)."),
       P(r"<strong>Compostos:</strong> \(15=3\cdot5\), \(21=3\cdot7\) i \(51=3\cdot17\) (compte: la suma de xifres de 51 és 6, és divisible per 3!).", r"<strong>Compuestos:</strong> \(15=3\cdot5\), \(21=3\cdot7\) y \(51=3\cdot17\) (cuidado: la suma de cifras de 51 es 6, ¡es divisible por 3!).", r"<strong>Composite:</strong> \(15=3\cdot5\), \(21=3\cdot7\) and \(51=3\cdot17\) (careful: the digit sum of 51 is 6, so it's divisible by 3!)."),
       P(r"El \(1\) no és ni primer ni compost.", r"El \(1\) no es ni primo ni compuesto.", r"\(1\) is neither prime nor composite.")))
s5 += level(2, 2,
  prob(L(r"És \(127\) un nombre primer?", r"¿Es \(127\) un número primo?", r"Is \(127\) a prime number?"),
       P(r"Per 2 no (és senar); per 3 no (suma 10); per 5 no (acaba en 7); per 7 no (\(127=7\cdot18+1\)); per 11 no (\(127=11\cdot11+6\)).", r"Por 2 no (es impar); por 3 no (suma 10); por 5 no (acaba en 7); por 7 no (\(127=7\cdot18+1\)); por 11 no (\(127=11\cdot11+6\)).", r"Not by 2 (it's odd); not by 3 (digit sum 10); not by 5 (ends in 7); not by 7 (\(127=7\cdot18+1\)); not by 11 (\(127=11\cdot11+6\))."),
       P(r"Per 13: \(127=13\cdot9+10\). El quocient (9) ja és menor que el divisor (13): parem. \(127\) és <strong>primer</strong>.", r"Por 13: \(127=13\cdot9+10\). El cociente (9) ya es menor que el divisor (13): paramos. \(127\) es <strong>primo</strong>.", r"By 13: \(127=13\cdot9+10\). The quotient (9) is already less than the divisor (13): stop. \(127\) is <strong>prime</strong>.")),
  prob(L(r"Escriu tots els nombres primers compresos entre 40 i 60.", r"Escribe todos los números primos comprendidos entre 40 y 60.", r"Write all the prime numbers between 40 and 60."),
       P(r"Descartem els parells i els acabats en 5. Dels que queden, \(45, 51, 57\) són múltiples de 3 i \(49=7\cdot7\).", r"Descartamos los pares y los acabados en 5. De los que quedan, \(45, 51, 57\) son múltiplos de 3 y \(49=7\cdot7\).", r"Rule out even numbers and those ending in 5. Of the rest, \(45, 51, 57\) are multiples of 3 and \(49=7\cdot7\).") + r'\[\boxed{41,\ 43,\ 47,\ 53,\ 59}\]'))
s5 += level(3, 4,
  prob(L(r"Dos primers són <strong>bessons</strong> si es diferencien en 2, com l'11 i el 13. Troba totes les parelles de primers bessons menors que 50.", r"Dos primos son <strong>gemelos</strong> si se diferencian en 2, como el 11 y el 13. Encuentra todas las parejas de primos gemelos menores que 50.", r"Two primes are <strong>twins</strong> if they differ by 2, like 11 and 13. Find all the pairs of twin primes below 50."),
       P(r"Mirem la llista de primers i busquem els que estan a distància 2:", r"Miramos la lista de primos y buscamos los que están a distancia 2:", r"Look at the list of primes and find those 2 apart:") + r'\[\boxed{(3,5),\ (5,7),\ (11,13),\ (17,19),\ (29,31),\ (41,43)}\]'),
  prob(L(r"Escriu \(30\) com a suma de dos nombres primers de totes les maneres possibles.", r"Escribe \(30\) como suma de dos números primos de todas las formas posibles.", r"Write \(30\) as the sum of two primes in every possible way."),
       P(r"Provem amb cada primer menor que 15 i mirem si el que falta també és primer: \(30-2=28\) ✗, \(30-3=27\) ✗, \(30-5=25\) ✗, \(30-7=23\) ✓, \(30-11=19\) ✓, \(30-13=17\) ✓.", r"Probamos con cada primo menor que 15 y miramos si lo que falta también es primo: \(30-2=28\) ✗, \(30-3=27\) ✗, \(30-5=25\) ✗, \(30-7=23\) ✓, \(30-11=19\) ✓, \(30-13=17\) ✓.", r"Try each prime below 15 and check whether what's left is also prime: \(30-2=28\) ✗, \(30-3=27\) ✗, \(30-5=25\) ✗, \(30-7=23\) ✓, \(30-11=19\) ✓, \(30-13=17\) ✓."),
       r'\[\boxed{30=7+23=11+19=13+17}\]'))
s5 += practice([
  ('★', L(r"a) Escriu els divisors de \(23\) i de \(25\). Quin dels dos és primer? b) Escriu tots els nombres primers menors que 20.", r"a) Escribe los divisores de \(23\) y de \(25\). ¿Cuál de los dos es primo? b) Escribe todos los números primos menores que 20.", r"a) Write the divisors of \(23\) and \(25\). Which one is prime? b) Write all the primes below 20.")),
  ('★★', L(r"c) És primer el \(91\)? d) És primer el \(101\)?", r"c) ¿Es primo el \(91\)? d) ¿Es primo el \(101\)?", r"c) Is \(91\) prime? d) Is \(101\) prime?")),
  ('★★★', L(r"e) Quin és el primer nombre primer més gran que \(200\)? f) Pot ser primer la suma de dos primers més grans que 2? Per què?", r"e) ¿Cuál es el primer número primo mayor que \(200\)? f) ¿Puede ser primo la suma de dos primos mayores que 2? ¿Por qué?", r"e) What is the first prime greater than \(200\)? f) Can the sum of two primes greater than 2 be prime? Why?"))],
  P(r"a) \(\text{Div}(23)=\{1,23\}\), \(\text{Div}(25)=\{1,5,25\}\): el primer és el 23. &nbsp; b) \(2,3,5,7,11,13,17,19\).", r"a) \(\text{Div}(23)=\{1,23\}\), \(\text{Div}(25)=\{1,5,25\}\): el primo es el 23. &nbsp; b) \(2,3,5,7,11,13,17,19\).", r"a) \(\text{Div}(23)=\{1,23\}\), \(\text{Div}(25)=\{1,5,25\}\): 23 is prime. &nbsp; b) \(2,3,5,7,11,13,17,19\).")
  + P(r"c) No: \(91=7\cdot13\). &nbsp; d) Sí: no és divisible per 2, 3, 5 ni 7, i en \(101:11\) el quocient (9) ja és menor que 11.", r"c) No: \(91=7\cdot13\). &nbsp; d) Sí: no es divisible por 2, 3, 5 ni 7, y en \(101:11\) el cociente (9) ya es menor que 11.", r"c) No: \(91=7\cdot13\). &nbsp; d) Yes: it isn't divisible by 2, 3, 5 or 7, and in \(101:11\) the quotient (9) is already less than 11.")
  + P(r"e) \(201=3\cdot67\), \(203=7\cdot29\), \(207=3\cdot69\), \(209=11\cdot19\)… El \(211\) és primer. &nbsp; f) No: tots dos són senars i la suma de dos senars és parella (i més gran que 2).", r"e) \(201=3\cdot67\), \(203=7\cdot29\), \(207=3\cdot69\), \(209=11\cdot19\)… El \(211\) es primo. &nbsp; f) No: los dos son impares y la suma de dos impares es par (y mayor que 2).", r"e) \(201=3\cdot67\), \(203=7\cdot29\), \(207=3\cdot69\), \(209=11\cdot19\)… \(211\) is prime. &nbsp; f) No: both are odd and the sum of two odd numbers is even (and greater than 2)."))

# ============================================================ 2.6
s6 = box('def', L('Descomposició en factors primers', 'Descomposición en factores primos', 'Prime factorisation'),
  P(r"<strong>Descompondre un nombre en factors primers</strong> (o <strong>factoritzar-lo</strong>) és escriure'l com un producte de nombres primers. Tot nombre compost es pot descompondre, i d'<strong>una sola manera</strong> (sense comptar l'ordre dels factors).",
    r"<strong>Descomponer un número en factores primos</strong> (o <strong>factorizarlo</strong>) es escribirlo como un producto de números primos. Todo número compuesto se puede descomponer, y de <strong>una sola forma</strong> (sin contar el orden de los factores).",
    r"<strong>Prime factorisation</strong> means writing a number as a product of prime numbers. Every composite number can be factorised, and in <strong>only one way</strong> (apart from the order of the factors).")
  + P(r"<strong>Mètode de la columna:</strong> dividim el nombre entre el primer més xicotet possible (2, 3, 5, 7…) i repetim amb el quocient fins a arribar a 1. Els primers de la dreta són els factors.",
      r"<strong>Método de la columna:</strong> dividimos el número entre el primo más pequeño posible (2, 3, 5, 7…) y repetimos con el cociente hasta llegar a 1. Los primos de la derecha son los factores.",
      r"<strong>Column method:</strong> divide the number by the smallest possible prime (2, 3, 5, 7…) and repeat with the quotient until you reach 1. The primes on the right are the factors.")
  + '<div class="two-col"><div>' + col([(360, 2), (180, 2), (90, 2), (45, 3), (15, 3), (5, 5), (1, '')]) + '</div><div>'
  + r'\[360=2\cdot2\cdot2\cdot3\cdot3\cdot5\]\[\boxed{360=2^{3}\cdot3^{2}\cdot5}\]' + '</div></div>'
  + note(r"Escrivim els factors repetits en forma de <strong>potència</strong>, i els primers ordenats de menor a major.", r"Escribimos los factores repetidos en forma de <strong>potencia</strong>, y los primos ordenados de menor a mayor.", r"Write repeated factors as <strong>powers</strong>, with the primes in increasing order.", '✏️'))
s6 += box('prop', L("Mètode de l'arbre", 'Método del árbol', 'Factor tree'),
  P(r"També podem anar partint el nombre en dos factors qualssevol (\(360=36\cdot10\)) i continuar partint cada branca fins que totes acaben en un primer. Siga quin siga el camí, el resultat és el mateix.",
    r"También podemos ir partiendo el número en dos factores cualesquiera (\(360=36\cdot10\)) y continuar partiendo cada rama hasta que todas acaben en un primo. Sea cual sea el camino, el resultado es el mismo.",
    r"We can also split the number into any two factors (\(360=36\cdot10\)) and keep splitting each branch until they all end in a prime. Whatever path we take, the result is the same.")
  + f'''<div class="widget" id="w-fact">
  <div class="wt">🌳 {L("Factoritzador", "Factorizador", "Factoriser")}</div>
  <div class="wrow">{nin("n", "Nombre", "Número", "Number", "360", "w")}{seg([("col", L("Columna", "Columna", "Column")), ("tree", L("Arbre", "Árbol", "Tree"))], "col")}</div>
  {quick([("60", "60"), ("84", "84"), ("360", "360"), ("1050", "1050"), ("1001", "1001"), ("1024", "1024"), ("97", "97"), ("7560", "7560")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('fact', 'Entrena: descomposició', 'Entrena: descomposición', 'Train: factorisation'))
s6 += level(1, 1,
  prob(L(r"Descompon en factors primers \(84\) i \(90\).", r"Descompón en factores primos \(84\) y \(90\).", r"Write \(84\) and \(90\) as products of primes."),
       '<div class="two-col"><div>' + col([(84, 2), (42, 2), (21, 3), (7, 7), (1, '')]) + r'\[84=\boxed{2^{2}\cdot3\cdot7}\]</div><div>' + col([(90, 2), (45, 3), (15, 3), (5, 5), (1, '')]) + r'\[90=\boxed{2\cdot3^{2}\cdot5}\]</div></div>'))
s6 += level(2, 2,
  prob(L(r"Descompon \(1050\) en factors primers.", r"Descompón \(1050\) en factores primos.", r"Find the prime factorisation of \(1050\)."),
       P(r"Acaba en 0: dividim entre 2. Després, la suma de xifres de 525 és 12: entre 3. 175 acaba en 5…", r"Acaba en 0: dividimos entre 2. Después, la suma de cifras de 525 es 12: entre 3. 175 acaba en 5…", r"It ends in 0: divide by 2. Then the digit sum of 525 is 12: divide by 3. 175 ends in 5…")
       + col([(1050, 2), (525, 3), (175, 5), (35, 5), (7, 7), (1, '')]),
       r'\[1050=\boxed{2\cdot3\cdot5^{2}\cdot7}\]'),
  prob(L(r"Quin nombre té aquesta descomposició? \(\ 2^{3}\cdot3^{2}\cdot5\)", r"¿Qué número tiene esta descomposición? \(\ 2^{3}\cdot3^{2}\cdot5\)", r"Which number has this factorisation? \(\ 2^{3}\cdot3^{2}\cdot5\)"),
       r'\[2^{3}\cdot3^{2}\cdot5=8\cdot9\cdot5=72\cdot5=\boxed{360}\]'))
s6 += level(3, 4,
  prob(L(r"Quin és el nombre més xicotet pel qual cal multiplicar \(72\) perquè el resultat siga un quadrat perfecte?", r"¿Cuál es el número más pequeño por el que hay que multiplicar \(72\) para que el resultado sea un cuadrado perfecto?", r"What is the smallest number we must multiply \(72\) by to get a perfect square?"),
       P(r"Factoritzem: \(72=2^{3}\cdot3^{2}\). En un quadrat perfecte, tots els exponents són <strong>parells</strong> (es poden repartir en dos grups iguals).", r"Factorizamos: \(72=2^{3}\cdot3^{2}\). En un cuadrado perfecto, todos los exponentes son <strong>pares</strong> (se pueden repartir en dos grupos iguales).", r"Factorise: \(72=2^{3}\cdot3^{2}\). In a perfect square all the exponents are <strong>even</strong> (they can be split into two equal groups)."),
       P(r"Al 2 li falta un factor per a tindre exponent 4: multipliquem per \(\boxed{2}\).", r"Al 2 le falta un factor para tener exponente 4: multiplicamos por \(\boxed{2}\).", r"The 2 needs one more factor to reach exponent 4: multiply by \(\boxed{2}\).") + r'\[72\cdot2=2^{4}\cdot3^{2}=144=12^{2}\]'))
s6 += practice([
  ('★', L(r"a) Descompon \(48\). b) Descompon \(150\).", r"a) Descompón \(48\). b) Descompón \(150\).", r"a) Factorise \(48\). b) Factorise \(150\).")),
  ('★★', L(r"c) Descompon \(980\). d) Quin nombre és \(2^{2}\cdot3^{3}\cdot5\)?", r"c) Descompón \(980\). d) ¿Qué número es \(2^{2}\cdot3^{3}\cdot5\)?", r"c) Factorise \(980\). d) Which number is \(2^{2}\cdot3^{3}\cdot5\)?")),
  ('★★★', L(r"e) Descompon \(1001\). f) Per quin nombre més xicotet cal multiplicar \(50\) perquè siga un quadrat perfecte?", r"e) Descompón \(1001\). f) ¿Por qué número más pequeño hay que multiplicar \(50\) para que sea un cuadrado perfecto?", r"e) Factorise \(1001\). f) What is the smallest number to multiply \(50\) by to get a perfect square?"))],
  r'\[\text{a)}\ 2^{4}\cdot3\qquad \text{b)}\ 2\cdot3\cdot5^{2}\qquad \text{c)}\ 2^{2}\cdot5\cdot7^{2}\qquad \text{d)}\ 4\cdot27\cdot5=540\]'
  + r'\[\text{e)}\ 7\cdot11\cdot13\qquad \text{f)}\ 50=2\cdot5^{2}\ \to\ \cdot2:\ \ 100=10^{2}\]')

# ============================================================ 2.7
s7 = box('def', L('Mínim comú múltiple', 'Mínimo común múltiplo', 'Least common multiple'),
  P(r"El <strong>mínim comú múltiple</strong> de dos o més nombres, \(\text{mcm}\), és el <strong>més xicotet</strong> dels seus múltiples comuns, sense comptar el 0.",
    r"El <strong>mínimo común múltiplo</strong> de dos o más números, \(\text{mcm}\), es el <strong>menor</strong> de sus múltiplos comunes, sin contar el 0.",
    r"The <strong>least common multiple</strong> of two or more numbers, \(\text{lcm}\), is the <strong>smallest</strong> of their common multiples, not counting 0.")
  + P(r"<strong>Primera manera: amb la llista de múltiples.</strong>", r"<strong>Primera forma: con la lista de múltiplos.</strong>", r"<strong>First way: listing multiples.</strong>")
  + r'\[\begin{aligned}\text{M}(4)&=\{4,\ 8,\ \htmlClass{hl}{12},\ 16,\ 20,\ \htmlClass{hl}{24},\ 28,\ 32,\ \htmlClass{hl}{36},\ \ldots\}\\ \text{M}(6)&=\{6,\ \htmlClass{hl}{12},\ 18,\ \htmlClass{hl}{24},\ 30,\ \htmlClass{hl}{36},\ \ldots\}\end{aligned}\qquad ' + MCM + r'(4,6)=\boxed{12}\]'
  + P(r"Els múltiples comuns de 4 i 6 són \(12, 24, 36\ldots\) (els múltiples de 12). El més xicotet és el 12.", r"Los múltiplos comunes de 4 y 6 son \(12, 24, 36\ldots\) (los múltiplos de 12). El menor es el 12.", r"The common multiples of 4 and 6 are \(12, 24, 36\ldots\) (the multiples of 12). The smallest is 12."))
s7 += box('def', L("Càlcul del mcm a partir de la descomposició", "Cálculo del mcm a partir de la descomposición", "Finding the lcm from the factorisation"),
  P(r"Amb nombres grans, la llista es fa molt llarga. És més ràpid:", r"Con números grandes, la lista se hace muy larga. Es más rápido:", r"With big numbers the list gets very long. It's quicker to:")
  + '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"Descompondre cada nombre en factors primers.", r"Descomponer cada número en factores primos.", r"Factorise each number into primes."),
      L(r"Agafar els factors <strong>comuns i no comuns</strong>, cadascun amb el <strong>major exponent</strong>.", r"Tomar los factores <strong>comunes y no comunes</strong>, cada uno con el <strong>mayor exponente</strong>.", r"Take <strong>every</strong> prime factor that appears (common or not), each with its <strong>highest exponent</strong>."),
      L(r"Multiplicar-los.", r"Multiplicarlos.", r"Multiply them.")]) + '</ol>'
  + r'\[\left.\begin{aligned}12&=2^{2}\cdot3\\18&=2\cdot3^{2}\end{aligned}\right\}\ \ ' + MCM + r'(12,18)=2^{2}\cdot3^{2}=4\cdot9=\boxed{36}\]'
  + r'\[\left.\begin{aligned}40&=2^{3}\cdot5\\36&=2^{2}\cdot3^{2}\\30&=2\cdot3\cdot5\end{aligned}\right\}\ \ ' + MCM + r'(40,36,30)=2^{3}\cdot3^{2}\cdot5=\boxed{360}\]'
  + ul(L(r"Si un nombre és múltiple de l'altre, el mcm és el <strong>més gran</strong>: \(\ \text{mcm}(6,18)=18\).", r"Si un número es múltiplo del otro, el mcm es el <strong>mayor</strong>: \(\ \text{mcm}(6,18)=18\).", r"If one number is a multiple of the other, the lcm is the <strong>bigger</strong> one: \(\ \text{lcm}(6,18)=18\)."),
       L(r"Si no tenen cap factor comú, el mcm és el <strong>producte</strong>: \(\ \text{mcm}(8,15)=120\).", r"Si no tienen ningún factor común, el mcm es el <strong>producto</strong>: \(\ \text{mcm}(8,15)=120\).", r"If they share no factor, the lcm is their <strong>product</strong>: \(\ \text{lcm}(8,15)=120\)."))
  + f'''<div class="widget w-gcd" data-mode="mcm">
  <div class="wt">🧮 {L("Calculadora del mcm", "Calculadora del mcm", "LCM calculator")}</div>
  <div class="wrow">{nin("a", "a", "a", "a", "12")}{nin("b", "b", "b", "b", "18")}{nin("c", "c (opcional)", "c (opcional)", "c (optional)", "")}</div>
  <div class="wrow">{seg([("fac", L("Descomposició", "Descomposición", "Factorisation")), ("list", L("Llistes", "Listas", "Lists"))], "fac")}</div>
  {quick([("4,6", "4, 6"), ("12,18", "12, 18"), ("8,15", "8, 15"), ("6,18", "6, 18"), ("45,60", "45, 60"), ("12,30,42", "12, 30, 42"), ("40,36,30", "40, 36, 30")])}
  <div class="gout"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('mcm', 'Entrena: calcula el mcm', 'Entrena: calcula el mcm', 'Train: find the lcm'))
s7 += level(1, 1,
  prob(L(r"Calcula \(\text{mcm}(6,8)\) i \(\text{mcm}(10,15)\) amb la llista de múltiples.", r"Calcula \(\text{mcm}(6,8)\) y \(\text{mcm}(10,15)\) con la lista de múltiplos.", r"Find \(\text{lcm}(6,8)\) and \(\text{lcm}(10,15)\) by listing multiples."),
       r'\[\text{M}(6)=\{6,12,18,\htmlClass{hl}{24},\ldots\}\quad \text{M}(8)=\{8,16,\htmlClass{hl}{24},\ldots\}\ \to\ ' + MCM + r'(6,8)=\boxed{24}\]',
       r'\[\text{M}(10)=\{10,20,\htmlClass{hl}{30},\ldots\}\quad \text{M}(15)=\{15,\htmlClass{hl}{30},\ldots\}\ \to\ ' + MCM + r'(10,15)=\boxed{30}\]'))
s7 += level(2, 2,
  prob(L(r"Calcula \(\text{mcm}(45,60)\) a partir de la descomposició.", r"Calcula \(\text{mcm}(45,60)\) a partir de la descomposición.", r"Find \(\text{lcm}(45,60)\) using prime factorisation."),
       r'\[45=3^{2}\cdot5\qquad 60=2^{2}\cdot3\cdot5\]',
       P(r"Tots els factors (2, 3 i 5), cadascun amb l'exponent més gran:", r"Todos los factores (2, 3 y 5), cada uno con el exponente mayor:", r"All the factors (2, 3 and 5), each with its highest exponent:") + r'\[' + MCM + r'(45,60)=2^{2}\cdot3^{2}\cdot5=4\cdot9\cdot5=\boxed{180}\]'),
  prob(L(r"Calcula \(\text{mcm}(12,30,42)\).", r"Calcula \(\text{mcm}(12,30,42)\).", r"Find \(\text{lcm}(12,30,42)\)."),
       r'\[12=2^{2}\cdot3\qquad 30=2\cdot3\cdot5\qquad 42=2\cdot3\cdot7\]',
       r'\[' + MCM + r'(12,30,42)=2^{2}\cdot3\cdot5\cdot7=\boxed{420}\]'))
s7 += level(3, 4,
  prob(L(r"Calcula el mcm de \(\ a=2^{3}\cdot5,\ \ b=2\cdot3^{2}\cdot5\ \) i \(\ c=3\cdot7\) sense calcular abans els nombres.", r"Calcula el mcm de \(\ a=2^{3}\cdot5,\ \ b=2\cdot3^{2}\cdot5\ \) y \(\ c=3\cdot7\) sin calcular antes los números.", r"Find the lcm of \(\ a=2^{3}\cdot5,\ \ b=2\cdot3^{2}\cdot5\ \) and \(\ c=3\cdot7\) without working out the numbers first."),
       P(r"Factors que apareixen: 2 (major exponent 3), 3 (major exponent 2), 5 i 7.", r"Factores que aparecen: 2 (mayor exponente 3), 3 (mayor exponente 2), 5 y 7.", r"Factors that appear: 2 (highest exponent 3), 3 (highest exponent 2), 5 and 7."),
       r'\[' + MCM + r'=2^{3}\cdot3^{2}\cdot5\cdot7=8\cdot9\cdot35=\boxed{2520}\]'))
s7 += practice([
  ('★', L(r"a) \(\text{mcm}(4,10)\) b) \(\text{mcm}(9,12)\)", r"a) \(\text{mcm}(4,10)\) b) \(\text{mcm}(9,12)\)", r"a) \(\text{lcm}(4,10)\) b) \(\text{lcm}(9,12)\)")),
  ('★★', L(r"c) \(\text{mcm}(18,24)\) d) \(\text{mcm}(20,30,45)\)", r"c) \(\text{mcm}(18,24)\) d) \(\text{mcm}(20,30,45)\)", r"c) \(\text{lcm}(18,24)\) d) \(\text{lcm}(20,30,45)\)")),
  ('★★★', L(r"e) Calcula \(\text{mcm}(7,11)\) i \(\text{mcm}(15,45)\) sense descompondre. Explica com ho has fet. f) Troba dos nombres, cap dels dos igual a 30, que tinguen \(\text{mcm}=30\).", r"e) Calcula \(\text{mcm}(7,11)\) y \(\text{mcm}(15,45)\) sin descomponer. Explica cómo lo has hecho. f) Encuentra dos números, ninguno igual a 30, que tengan \(\text{mcm}=30\).", r"e) Find \(\text{lcm}(7,11)\) and \(\text{lcm}(15,45)\) without factorising. Explain how. f) Find two numbers, neither equal to 30, whose lcm is 30."))],
  r'\[\text{a)}\ 20\qquad \text{b)}\ 36\qquad \text{c)}\ 2^{3}\cdot3^{2}=72\qquad \text{d)}\ 2^{2}\cdot3^{2}\cdot5=180\]'
  + P(r"e) \(77\) (no tenen factors comuns: es multipliquen) i \(45\) (45 ja és múltiple de 15). &nbsp; f) Per exemple, \(6\) i \(10\), o \(10\) i \(15\), o \(5\) i \(6\).", r"e) \(77\) (no tienen factores comunes: se multiplican) y \(45\) (45 ya es múltiplo de 15). &nbsp; f) Por ejemplo, \(6\) y \(10\), o \(10\) y \(15\), o \(5\) y \(6\).", r"e) \(77\) (no common factors: multiply them) and \(45\) (45 is already a multiple of 15). &nbsp; f) For example \(6\) and \(10\), or \(10\) and \(15\), or \(5\) and \(6\)."))

# ============================================================ 2.8
s8 = box('prop', L('Com reconeixem un problema de mcm?', '¿Cómo reconocemos un problema de mcm?', 'How do we spot an lcm problem?'),
  P(r"Fem servir el <strong>mínim comú múltiple</strong> quan:", r"Usamos el <strong>mínimo común múltiplo</strong> cuando:", r"We use the <strong>least common multiple</strong> when:")
  + ul(L(r"Hi ha coses que es <strong>repeteixen</strong> cada cert temps i volem saber <strong>quan tornaran a coincidir</strong> (autobusos, llums, visites…).", r"Hay cosas que se <strong>repiten</strong> cada cierto tiempo y queremos saber <strong>cuándo volverán a coincidir</strong> (autobuses, luces, visitas…).", r"Things <strong>repeat</strong> every so often and we want to know <strong>when they'll coincide again</strong> (buses, lights, visits…)."),
       L(r"Busquem el nombre <strong>més xicotet</strong> que és múltiple de diversos nombres alhora (es pot agrupar de 3 en 3, de 4 en 4…).", r"Buscamos el número <strong>más pequeño</strong> que es múltiplo de varios números a la vez (se puede agrupar de 3 en 3, de 4 en 4…).", r"We want the <strong>smallest</strong> number that is a multiple of several numbers at once (it can be grouped in 3s, in 4s…)."))
  + note(r"Paraules clau: <em>tornaran a coincidir</em>, <em>alhora</em>, <em>com a mínim</em>, <em>el menor nombre</em>… El resultat sempre és <strong>més gran o igual</strong> que els nombres de l'enunciat.", r"Palabras clave: <em>volverán a coincidir</em>, <em>a la vez</em>, <em>como mínimo</em>, <em>el menor número</em>… El resultado siempre es <strong>mayor o igual</strong> que los números del enunciado.", r"Key words: <em>coincide again</em>, <em>at the same time</em>, <em>at least</em>, <em>the smallest number</em>… The answer is always <strong>greater than or equal to</strong> the numbers in the problem.", '🔑')
  + f'''<div class="widget" id="w-coin">
  <div class="wt">⏱ {L("Quan tornen a coincidir?", "¿Cuándo vuelven a coincidir?", "When do they coincide again?")}</div>
  <div class="wrow">{nin("a", "Cada", "Cada", "Every", "12")}{nin("b", "cada", "cada", "every", "18")}{nin("c", "cada (opcional)", "cada (opcional)", "every (optional)", "")}</div>
  <div class="wrow">{seg([("min", L("minuts", "minutos", "minutes")), ("d", L("dies", "días", "days")), ("s", L("segons", "segundos", "seconds"))], "min")}<label class="tstart">{L("Comencen a les", "Empiezan a las", "They start at")} <input class="tin s" type="text" data-k="t" value="8:00" autocomplete="off" aria-label="hora"></label></div>
  {quick([("12,18", "12 i 18"), ("4,6", "4 i 6"), ("15,20", "15 i 20"), ("8,12,15", "8, 12 i 15"), ("20,30,45", "20, 30 i 45")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s8 += level(1, 1,
  prob(L(r"Dos autobusos ixen junts de l'estació a les 8:00. Un passa cada 12 minuts i l'altre, cada 18. A quina hora tornaran a eixir junts?", r"Dos autobuses salen juntos de la estación a las 8:00. Uno pasa cada 12 minutos y el otro, cada 18. ¿A qué hora volverán a salir juntos?", r"Two buses leave the station together at 8:00. One runs every 12 minutes and the other every 18. When will they next leave together?"),
       P(r"Coincidiran en un temps que siga múltiple de 12 i de 18 alhora, i volem el primer: el mcm.", r"Coincidirán en un tiempo que sea múltiplo de 12 y de 18 a la vez, y queremos el primero: el mcm.", r"They'll coincide at a time that is a multiple of both 12 and 18, and we want the first: the lcm.") + r'\[12=2^{2}\cdot3\qquad 18=2\cdot3^{2}\qquad ' + MCM + r'(12,18)=2^{2}\cdot3^{2}=36\]',
       P(r"Al cap de 36 minuts: a les \(\boxed{8\text{:}36}\).", r"Al cabo de 36 minutos: a las \(\boxed{8\text{:}36}\).", r"After 36 minutes: at \(\boxed{8\text{:}36}\).")),
  prob(L(r"La Marta va a la piscina cada 4 dies i en Joan, cada 6. Hui hi han coincidit. D'ací a quants dies tornaran a coincidir?", r"Marta va a la piscina cada 4 días y Juan, cada 6. Hoy han coincidido. ¿Dentro de cuántos días volverán a coincidir?", r"Marta goes swimming every 4 days and Joan every 6. Today they met there. In how many days will they meet again?"),
       r'\[' + MCM + r'(4,6)=12\ \to\ \boxed{\tri{d\'ací a 12 dies}{dentro de 12 días}{in 12 days}}\]'))
s8 += level(2, 3,
  prob(L(r"Tres fars s'encenen cada 8, 12 i 15 segons. Si ara s'han encés tots alhora, quant de temps passarà fins que tornen a fer-ho?", r"Tres faros se encienden cada 8, 12 y 15 segundos. Si ahora se han encendido todos a la vez, ¿cuánto tiempo pasará hasta que vuelvan a hacerlo?", r"Three lighthouses flash every 8, 12 and 15 seconds. If they've just flashed together, how long until they do it again?"),
       r'\[8=2^{3}\qquad 12=2^{2}\cdot3\qquad 15=3\cdot5\]',
       r'\[' + MCM + r'(8,12,15)=2^{3}\cdot3\cdot5=\boxed{120\text{ s}}=2\text{ min}\]'),
  prob(L(r"Quin és el nombre més xicotet de caramels que podem repartir en bossetes de 6, de 8 o de 10, sense que en sobre cap?", r"¿Cuál es el menor número de caramelos que podemos repartir en bolsitas de 6, de 8 o de 10, sin que sobre ninguno?", r"What is the smallest number of sweets that can be packed in bags of 6, of 8 or of 10 with none left over?"),
       P(r"Ha de ser múltiple de 6, de 8 i de 10, i el més xicotet:", r"Tiene que ser múltiplo de 6, de 8 y de 10, y el menor:", r"It must be a multiple of 6, 8 and 10, and the smallest:") + r'\[6=2\cdot3\qquad 8=2^{3}\qquad 10=2\cdot5\qquad ' + MCM + r'=2^{3}\cdot3\cdot5=\boxed{120}\]'))
s8 += level(3, 5,
  prob(L(r"Si agrupem els bombons d'una caixa de 4 en 4, de 5 en 5 o de 6 en 6, sempre en sobra 1. Quants bombons hi ha, com a mínim, si n'hi ha més d'un?", r"Si agrupamos los bombones de una caja de 4 en 4, de 5 en 5 o de 6 en 6, siempre sobra 1. ¿Cuántos bombones hay, como mínimo, si hay más de uno?", r"If we group the chocolates in a box in 4s, 5s or 6s, there is always 1 left over. What is the smallest possible number of chocolates (more than one)?"),
       P(r"Si en llevem 1, el que queda es pot agrupar exactament de 4 en 4, de 5 en 5 i de 6 en 6: és múltiple comú de 4, 5 i 6.", r"Si quitamos 1, lo que queda se puede agrupar exactamente de 4 en 4, de 5 en 5 y de 6 en 6: es múltiplo común de 4, 5 y 6.", r"If we take 1 away, what's left can be grouped exactly in 4s, 5s and 6s: it's a common multiple of 4, 5 and 6.") + r'\[' + MCM + r'(4,5,6)=2^{2}\cdot3\cdot5=60\]',
       P(r"Tornem a sumar el que sobrava: \(60+1=\boxed{61}\) bombons.", r"Volvemos a sumar lo que sobraba: \(60+1=\boxed{61}\) bombones.", r"Add back the one left over: \(60+1=\boxed{61}\) chocolates.")),
  prob(L(r"Un cometa passa prop de la Terra cada 15 anys i un altre, cada 25. L'any 2020 hi van passar tots dos. Quin serà el pròxim any en què hi passaran junts?", r"Un cometa pasa cerca de la Tierra cada 15 años y otro, cada 25. En 2020 pasaron los dos. ¿Cuál será el próximo año en que pasarán juntos?", r"One comet passes near Earth every 15 years and another every 25. Both passed in 2020. In which year will they next pass together?"),
       r'\[' + MCM + r'(15,25)=3\cdot5^{2}=75\qquad 2020+75=\boxed{2095}\]'))
s8 += practice([
  ('★', L(r"a) Dos llums fan pampallugues cada 6 i cada 10 segons. Si ara s'han encés juntes, quan tornaran a coincidir? b) Quin és el nombre més xicotet d'alumnes que es poden organitzar en grups de 3, de 4 o de 5 sense que en sobre cap?", r"a) Dos luces parpadean cada 6 y cada 10 segundos. Si ahora se han encendido juntas, ¿cuándo volverán a coincidir? b) ¿Cuál es el menor número de alumnos que se pueden organizar en grupos de 3, de 4 o de 5 sin que sobre ninguno?", r"a) Two lights blink every 6 and every 10 seconds. If they've just blinked together, when will they coincide again? b) What is the smallest number of students that can be split into groups of 3, 4 or 5 with nobody left over?")),
  ('★★', L(r"c) L'Anna visita la seua àvia cada 10 dies i la seua cosina cada 15. Hui ha visitat totes dues. D'ací a quants dies tornarà a fer les dues visites el mateix dia? d) Dues rodes dentades tenen 12 i 18 dents. Quantes voltes ha de fer cadascuna perquè tornen a la posició inicial?", r"c) Ana visita a su abuela cada 10 días y a su prima cada 15. Hoy ha visitado a las dos. ¿Dentro de cuántos días volverá a hacer las dos visitas el mismo día? d) Dos ruedas dentadas tienen 12 y 18 dientes. ¿Cuántas vueltas tiene que dar cada una para que vuelvan a la posición inicial?", r"c) Anna visits her grandmother every 10 days and her cousin every 15. Today she visited both. In how many days will she visit both on the same day again? d) Two gear wheels have 12 and 18 teeth. How many turns must each make to return to the starting position?")),
  ('★★★', L(r"e) Troba un nombre entre 100 i 200 que siga múltiple de 6, de 8 i de 9. f) Tres trens ixen cada 20, 30 i 45 minuts. Si a les 7:00 han eixit junts, a quina hora tornaran a eixir junts?", r"e) Encuentra un número entre 100 y 200 que sea múltiplo de 6, de 8 y de 9. f) Tres trenes salen cada 20, 30 y 45 minutos. Si a las 7:00 han salido juntos, ¿a qué hora volverán a salir juntos?", r"e) Find a number between 100 and 200 that is a multiple of 6, 8 and 9. f) Three trains leave every 20, 30 and 45 minutes. If they left together at 7:00, when will they next leave together?"))],
  P(r"a) \(\text{mcm}(6,10)=30\) s. &nbsp; b) \(\text{mcm}(3,4,5)=60\) alumnes.", r"a) \(\text{mcm}(6,10)=30\) s. &nbsp; b) \(\text{mcm}(3,4,5)=60\) alumnos.", r"a) \(\text{lcm}(6,10)=30\) s. &nbsp; b) \(\text{lcm}(3,4,5)=60\) students.")
  + P(r"c) \(\text{mcm}(10,15)=30\) dies. &nbsp; d) \(\text{mcm}(12,18)=36\) dents: la primera fa \(36:12=3\) voltes i la segona \(36:18=2\).", r"c) \(\text{mcm}(10,15)=30\) días. &nbsp; d) \(\text{mcm}(12,18)=36\) dientes: la primera da \(36:12=3\) vueltas y la segunda \(36:18=2\).", r"c) \(\text{lcm}(10,15)=30\) days. &nbsp; d) \(\text{lcm}(12,18)=36\) teeth: the first makes \(36:12=3\) turns and the second \(36:18=2\).")
  + P(r"e) \(\text{mcm}(6,8,9)=72\); el múltiple de 72 entre 100 i 200 és \(144\). &nbsp; f) \(\text{mcm}(20,30,45)=180\) min = 3 h: a les 10:00.", r"e) \(\text{mcm}(6,8,9)=72\); el múltiplo de 72 entre 100 y 200 es \(144\). &nbsp; f) \(\text{mcm}(20,30,45)=180\) min = 3 h: a las 10:00.", r"e) \(\text{lcm}(6,8,9)=72\); the multiple of 72 between 100 and 200 is \(144\). &nbsp; f) \(\text{lcm}(20,30,45)=180\) min = 3 h: at 10:00."))

# ============================================================ 2.9
s9 = box('def', L('Màxim comú divisor', 'Máximo común divisor', 'Greatest common divisor'),
  P(r"El <strong>màxim comú divisor</strong> de dos o més nombres, \(\text{MCD}\), és el <strong>més gran</strong> dels seus divisors comuns.",
    r"El <strong>máximo común divisor</strong> de dos o más números, \(\text{MCD}\), es el <strong>mayor</strong> de sus divisores comunes.",
    r"The <strong>greatest common divisor</strong> of two or more numbers, \(\text{gcd}\) (also called highest common factor), is the <strong>largest</strong> of their common divisors.")
  + P(r"<strong>Primera manera: amb la llista de divisors.</strong>", r"<strong>Primera forma: con la lista de divisores.</strong>", r"<strong>First way: listing divisors.</strong>")
  + r'\[\begin{aligned}\text{Div}(12)&=\{\htmlClass{hl}{1},\ \htmlClass{hl}{2},\ \htmlClass{hl}{3},\ 4,\ \htmlClass{hl}{6},\ 12\}\\ \text{Div}(18)&=\{\htmlClass{hl}{1},\ \htmlClass{hl}{2},\ \htmlClass{hl}{3},\ \htmlClass{hl}{6},\ 9,\ 18\}\end{aligned}\qquad ' + MCD + r'(12,18)=\boxed{6}\]')
s9 += box('def', L("Càlcul del MCD a partir de la descomposició", "Cálculo del MCD a partir de la descomposición", "Finding the gcd from the factorisation"),
  '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"Descompondre cada nombre en factors primers.", r"Descomponer cada número en factores primos.", r"Factorise each number into primes."),
      L(r"Agafar <strong>només els factors comuns</strong>, cadascun amb el <strong>menor exponent</strong>.", r"Tomar <strong>solo los factores comunes</strong>, cada uno con el <strong>menor exponente</strong>.", r"Take <strong>only the common factors</strong>, each with its <strong>lowest exponent</strong>."),
      L(r"Multiplicar-los.", r"Multiplicarlos.", r"Multiply them.")]) + '</ol>'
  + r'\[\left.\begin{aligned}12&=2^{2}\cdot3\\18&=2\cdot3^{2}\end{aligned}\right\}\ \ ' + MCD + r'(12,18)=2\cdot3=\boxed{6}\]'
  + r'\[\left.\begin{aligned}60&=2^{2}\cdot3\cdot5\\72&=2^{3}\cdot3^{2}\\84&=2^{2}\cdot3\cdot7\end{aligned}\right\}\ \ ' + MCD + r'(60,72,84)=2^{2}\cdot3=\boxed{12}\]'
  + ul(L(r"Si dos nombres no tenen cap factor primer comú, el seu MCD és \(1\) i diem que són <strong>primers entre si</strong>: \(\ \text{MCD}(8,15)=1\).", r"Si dos números no tienen ningún factor primo común, su MCD es \(1\) y decimos que son <strong>primos entre sí</strong>: \(\ \text{MCD}(8,15)=1\).", r"If two numbers share no prime factor, their gcd is \(1\) and we say they are <strong>coprime</strong>: \(\ \text{gcd}(8,15)=1\)."),
       L(r"Si un nombre és divisor de l'altre, el MCD és el <strong>més xicotet</strong>: \(\ \text{MCD}(6,18)=6\).", r"Si un número es divisor del otro, el MCD es el <strong>menor</strong>: \(\ \text{MCD}(6,18)=6\).", r"If one number divides the other, the gcd is the <strong>smaller</strong> one: \(\ \text{gcd}(6,18)=6\)."),
       L(r"Per a dos nombres es compleix: \(\ \text{MCD}(a,b)\cdot\text{mcm}(a,b)=a\cdot b\). &nbsp; \(6\cdot36=12\cdot18=216\)", r"Para dos números se cumple: \(\ \text{MCD}(a,b)\cdot\text{mcm}(a,b)=a\cdot b\). &nbsp; \(6\cdot36=12\cdot18=216\)", r"For two numbers: \(\ \text{gcd}(a,b)\cdot\text{lcm}(a,b)=a\cdot b\). &nbsp; \(6\cdot36=12\cdot18=216\)"))
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th></th><th>' + L('mcm', 'mcm', 'lcm') + '</th><th>' + L('MCD', 'MCD', 'gcd') + '</th></tr></thead><tbody>'
  + '<tr><th>' + L('Factors', 'Factores', 'Factors') + '</th><td>' + L('comuns i no comuns', 'comunes y no comunes', 'all of them') + '</td><td>' + L('només els comuns', 'solo los comunes', 'only the common ones') + '</td></tr>'
  + '<tr><th>' + L('Exponent', 'Exponente', 'Exponent') + '</th><td>' + L('el major', 'el mayor', 'the highest') + '</td><td>' + L('el menor', 'el menor', 'the lowest') + '</td></tr>'
  + '<tr><th>' + L('Resultat', 'Resultado', 'Result') + '</th><td>' + L('més gran o igual que els nombres', 'mayor o igual que los números', 'at least as big as the numbers') + '</td><td>' + L('més xicotet o igual que els nombres', 'menor o igual que los números', 'no bigger than the numbers') + '</td></tr>'
  + '</tbody></table></div>'
  + f'''<div class="widget w-gcd" data-mode="mcd">
  <div class="wt">🧮 {L("Calculadora del MCD", "Calculadora del MCD", "GCD calculator")}</div>
  <div class="wrow">{nin("a", "a", "a", "a", "12")}{nin("b", "b", "b", "b", "18")}{nin("c", "c (opcional)", "c (opcional)", "c (optional)", "")}</div>
  <div class="wrow">{seg([("fac", L("Descomposició", "Descomposición", "Factorisation")), ("list", L("Llistes", "Listas", "Lists"))], "fac")}</div>
  {quick([("12,18", "12, 18"), ("16,24", "16, 24"), ("8,15", "8, 15"), ("6,18", "6, 18"), ("90,126", "90, 126"), ("48,60,72", "48, 60, 72"), ("60,72,84", "60, 72, 84")])}
  <div class="gout"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('mcd', 'Entrena: calcula el MCD', 'Entrena: calcula el MCD', 'Train: find the gcd'))
s9 += level(1, 1,
  prob(L(r"Calcula \(\text{MCD}(16,24)\) amb la llista de divisors.", r"Calcula \(\text{MCD}(16,24)\) con la lista de divisores.", r"Find \(\text{gcd}(16,24)\) by listing divisors."),
       r'\[\text{Div}(16)=\{1,2,4,\htmlClass{hl}{8},16\}\qquad \text{Div}(24)=\{1,2,3,4,6,\htmlClass{hl}{8},12,24\}\]',
       P(r"Divisors comuns: \(1, 2, 4, 8\). El més gran: \(\text{MCD}(16,24)=\boxed{8}\).", r"Divisores comunes: \(1, 2, 4, 8\). El mayor: \(\text{MCD}(16,24)=\boxed{8}\).", r"Common divisors: \(1, 2, 4, 8\). The largest: \(\text{gcd}(16,24)=\boxed{8}\).")),
  prob(L(r"Calcula \(\text{MCD}(9,20)\). Com són aquests nombres?", r"Calcula \(\text{MCD}(9,20)\). ¿Cómo son estos números?", r"Find \(\text{gcd}(9,20)\). What do we call these numbers?"),
       r'\[9=3^{2}\qquad 20=2^{2}\cdot5\]',
       P(r"No tenen cap factor comú: \(\text{MCD}(9,20)=\boxed{1}\). Són <strong>primers entre si</strong> (encara que cap dels dos és primer!).", r"No tienen ningún factor común: \(\text{MCD}(9,20)=\boxed{1}\). Son <strong>primos entre sí</strong> (¡aunque ninguno de los dos es primo!).", r"They share no factor: \(\text{gcd}(9,20)=\boxed{1}\). They are <strong>coprime</strong> (even though neither is prime!).")))
s9 += level(2, 3,
  prob(L(r"Calcula \(\text{MCD}(90,126)\) a partir de la descomposició.", r"Calcula \(\text{MCD}(90,126)\) a partir de la descomposición.", r"Find \(\text{gcd}(90,126)\) using prime factorisation."),
       r'\[90=2\cdot3^{2}\cdot5\qquad 126=2\cdot3^{2}\cdot7\]',
       P(r"Factors comuns: 2 i 3 (el 5 i el 7 no ho són), amb el menor exponent:", r"Factores comunes: 2 y 3 (el 5 y el 7 no lo son), con el menor exponente:", r"Common factors: 2 and 3 (not 5 or 7), with the lowest exponent:") + r'\[' + MCD + r'(90,126)=2\cdot3^{2}=\boxed{18}\]'),
  prob(L(r"Calcula \(\text{MCD}(48,60,72)\).", r"Calcula \(\text{MCD}(48,60,72)\).", r"Find \(\text{gcd}(48,60,72)\)."),
       r'\[48=2^{4}\cdot3\qquad 60=2^{2}\cdot3\cdot5\qquad 72=2^{3}\cdot3^{2}\]',
       r'\[' + MCD + r'(48,60,72)=2^{2}\cdot3=\boxed{12}\]'))
s9 += level(3, 5,
  prob(L(r"Calcula el MCD i el mcm de 24 i 36, i comprova que el seu producte és igual a \(24\cdot36\).", r"Calcula el MCD y el mcm de 24 y 36, y comprueba que su producto es igual a \(24\cdot36\).", r"Find the gcd and the lcm of 24 and 36, and check that their product equals \(24\cdot36\)."),
       r'\[24=2^{3}\cdot3\qquad 36=2^{2}\cdot3^{2}\]',
       r'\[' + MCD + r'=2^{2}\cdot3=12\qquad ' + MCM + r'=2^{3}\cdot3^{2}=72\]',
       r'\[12\cdot72=864\qquad 24\cdot36=864\ \ ✓\]'))
s9 += practice([
  ('★', L(r"a) \(\text{MCD}(12,16)\) b) \(\text{MCD}(15,25)\)", r"a) \(\text{MCD}(12,16)\) b) \(\text{MCD}(15,25)\)", r"a) \(\text{gcd}(12,16)\) b) \(\text{gcd}(15,25)\)")),
  ('★★', L(r"c) \(\text{MCD}(56,84)\) d) \(\text{MCD}(30,45,75)\)", r"c) \(\text{MCD}(56,84)\) d) \(\text{MCD}(30,45,75)\)", r"c) \(\text{gcd}(56,84)\) d) \(\text{gcd}(30,45,75)\)")),
  ('★★★', L(r"e) Són 35 i 48 primers entre si? f) Si \(\text{MCD}(a,{b})=6\) i \(a\cdot b=360\), quant val \(\text{mcm}(a,{b})\)?", r"e) ¿Son 35 y 48 primos entre sí? f) Si \(\text{MCD}(a,{b})=6\) y \(a\cdot b=360\), ¿cuánto vale \(\text{mcm}(a,{b})\)?", r"e) Are 35 and 48 coprime? f) If \(\text{gcd}(a,{b})=6\) and \(a\cdot b=360\), what is \(\text{lcm}(a,{b})\)?"))],
  r'\[\text{a)}\ 4\qquad \text{b)}\ 5\qquad \text{c)}\ 2^{2}\cdot7=28\qquad \text{d)}\ 3\cdot5=15\]'
  + P(r"e) Sí: \(35=5\cdot7\) i \(48=2^{4}\cdot3\) no tenen factors comuns, \(\text{MCD}=1\). &nbsp; f) \(360:6=60\).", r"e) Sí: \(35=5\cdot7\) y \(48=2^{4}\cdot3\) no tienen factores comunes, \(\text{MCD}=1\). &nbsp; f) \(360:6=60\).", r"e) Yes: \(35=5\cdot7\) and \(48=2^{4}\cdot3\) share no factors, \(\text{gcd}=1\). &nbsp; f) \(360:6=60\)."))

# ============================================================ 2.10
s10 = box('prop', L('Com reconeixem un problema de MCD?', '¿Cómo reconocemos un problema de MCD?', 'How do we spot a gcd problem?'),
  P(r"Fem servir el <strong>màxim comú divisor</strong> quan volem <strong>repartir</strong> o <strong>dividir</strong> diverses quantitats en parts <strong>iguals</strong>, <strong>sense que en sobre res</strong>, i que les parts siguen <strong>el més grans possible</strong> (o que hi haja el major nombre de grups).",
    r"Usamos el <strong>máximo común divisor</strong> cuando queremos <strong>repartir</strong> o <strong>dividir</strong> varias cantidades en partes <strong>iguales</strong>, <strong>sin que sobre nada</strong>, y que las partes sean <strong>lo más grandes posible</strong> (o que haya el mayor número de grupos).",
    r"We use the <strong>greatest common divisor</strong> when we want to <strong>share</strong> or <strong>split</strong> several amounts into <strong>equal</strong> parts, <strong>with nothing left over</strong>, and make the parts <strong>as big as possible</strong> (or have the greatest number of groups).")
  + note(r"Paraules clau: <em>repartir</em>, <em>tallar en trossos iguals</em>, <em>sense que en sobre</em>, <em>el més gran possible</em>, <em>el màxim nombre</em>… El resultat sempre és <strong>més xicotet o igual</strong> que els nombres de l'enunciat.", r"Palabras clave: <em>repartir</em>, <em>cortar en trozos iguales</em>, <em>sin que sobre</em>, <em>lo más grande posible</em>, <em>el máximo número</em>… El resultado siempre es <strong>menor o igual</strong> que los números del enunciado.", r"Key words: <em>share</em>, <em>cut into equal pieces</em>, <em>nothing left over</em>, <em>as big as possible</em>, <em>the greatest number</em>… The answer is always <strong>less than or equal to</strong> the numbers in the problem.", '🔑')
  + f'''<div class="widget" id="w-tile">
  <div class="wt">🟦 {L("Rajoles quadrades el més grans possible", "Baldosas cuadradas lo más grandes posible", "The biggest possible square tiles")}</div>
  <div class="wrow">{nin("a", "Llarg (cm)", "Largo (cm)", "Length (cm)", "120")}<span class="op">×</span>{nin("b", "Ample (cm)", "Ancho (cm)", "Width (cm)", "84")}</div>
  {quick([("120,84", "120 × 84"), ("60,36", "60 × 36"), ("90,60", "90 × 60"), ("420,300", "420 × 300"), ("100,75", "100 × 75"), ("35,24", "35 × 24")])}
  <div class="tchips"></div>
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s10 += level(1, 1,
  prob(L(r"Una floristeria té 24 roses i 36 margarides. Vol fer el màxim nombre de rams iguals, sense que sobre cap flor. Quants rams pot fer? Quantes flors de cada tipus portarà cada ram?", r"Una floristería tiene 24 rosas y 36 margaritas. Quiere hacer el máximo número de ramos iguales, sin que sobre ninguna flor. ¿Cuántos ramos puede hacer? ¿Cuántas flores de cada tipo llevará cada ramo?", r"A florist has 24 roses and 36 daisies and wants to make as many identical bunches as possible, using every flower. How many bunches? How many flowers of each kind in each bunch?"),
       P(r"El nombre de rams ha de dividir 24 i 36 (perquè no sobre res), i el volem màxim: el MCD.", r"El número de ramos tiene que dividir 24 y 36 (para que no sobre nada), y lo queremos máximo: el MCD.", r"The number of bunches must divide 24 and 36 (so nothing is left), and we want the largest: the gcd.") + r'\[24=2^{3}\cdot3\qquad 36=2^{2}\cdot3^{2}\qquad ' + MCD + r'(24,36)=2^{2}\cdot3=12\]',
       P(r"\(\boxed{12\text{ rams}}\), cadascun amb \(24:12=2\) roses i \(36:12=3\) margarides.", r"\(\boxed{12\text{ ramos}}\), cada uno con \(24:12=2\) rosas y \(36:12=3\) margaritas.", r"\(\boxed{12\text{ bunches}}\), each with \(24:12=2\) roses and \(36:12=3\) daisies.")))
s10 += level(2, 2,
  prob(L(r"Volem enrajolar una paret de 120 cm per 84 cm amb rajoles quadrades, el més grans possible, sense tallar-ne cap. Quant ha de fer el costat de cada rajola? Quantes rajoles calen?", r"Queremos alicatar una pared de 120 cm por 84 cm con baldosas cuadradas, lo más grandes posible, sin cortar ninguna. ¿Cuánto tiene que medir el lado de cada baldosa? ¿Cuántas baldosas hacen falta?", r"We want to tile a 120 cm by 84 cm wall with square tiles, as big as possible, without cutting any. How long must each side be? How many tiles do we need?"),
       P(r"El costat ha de cabre un nombre exacte de vegades en 120 i en 84: és un divisor comú, i el volem màxim.", r"El lado tiene que caber un número exacto de veces en 120 y en 84: es un divisor común, y lo queremos máximo.", r"The side must fit an exact number of times into 120 and 84: it's a common divisor, and we want the largest.") + r'\[120=2^{3}\cdot3\cdot5\qquad 84=2^{2}\cdot3\cdot7\qquad ' + MCD + r'=2^{2}\cdot3=\boxed{12\text{ cm}}\]',
       P(r"En el llarg caben \(120:12=10\) rajoles i en l'ample, \(84:12=7\):", r"En el largo caben \(120:12=10\) baldosas y en el ancho, \(84:12=7\):", r"Along the length \(120:12=10\) tiles fit, and along the width \(84:12=7\):") + r'\[10\cdot7=\boxed{70\ \tri{rajoles}{baldosas}{tiles}}\]'),
  prob(L(r"Tenim tres cordes de 30, 45 i 60 m i volem tallar-les en trossos iguals, el més llargs possible, sense que en sobre res. Quant farà cada tros? Quants trossos tindrem?", r"Tenemos tres cuerdas de 30, 45 y 60 m y queremos cortarlas en trozos iguales, lo más largos posible, sin que sobre nada. ¿Cuánto medirá cada trozo? ¿Cuántos trozos tendremos?", r"We have three ropes of 30, 45 and 60 m and want to cut them into equal pieces, as long as possible, with nothing left over. How long is each piece? How many pieces will we get?"),
       r'\[30=2\cdot3\cdot5\qquad 45=3^{2}\cdot5\qquad 60=2^{2}\cdot3\cdot5\qquad ' + MCD + r'=3\cdot5=\boxed{15\text{ m}}\]',
       r'\[30:15+45:15+60:15=2+3+4=\boxed{9\ \tri{trossos}{trozos}{pieces}}\]'))
s10 += level(3, 4,
  prob(L(r"Una mestra reparteix 63 caramels i 90 bombons entre l'alumnat, de manera que tots reben la mateixa quantitat de cada tipus. Li sobren 3 caramels i 6 bombons. Quants alumnes pot haver-hi, com a màxim? Quants caramels i bombons rep cadascú?", r"Una maestra reparte 63 caramelos y 90 bombones entre el alumnado, de forma que todos reciben la misma cantidad de cada tipo. Le sobran 3 caramelos y 6 bombones. ¿Cuántos alumnos puede haber, como máximo? ¿Cuántos caramelos y bombones recibe cada uno?", r"A teacher shares 63 sweets and 90 chocolates among the class so that everyone gets the same amount of each. There are 3 sweets and 6 chocolates left over. What is the greatest possible number of students? How many of each does each one get?"),
       P(r"Els que s'han repartit exactament són \(63-3=60\) caramels i \(90-6=84\) bombons.", r"Los que se han repartido exactamente son \(63-3=60\) caramelos y \(90-6=84\) bombones.", r"The ones shared out exactly are \(63-3=60\) sweets and \(90-6=84\) chocolates."),
       r'\[60=2^{2}\cdot3\cdot5\qquad 84=2^{2}\cdot3\cdot7\qquad ' + MCD + r'(60,84)=2^{2}\cdot3=\boxed{12}\]',
       P(r"Com a màxim 12 alumnes (i 12 és més gran que el que sobra, 3 i 6, com ha de ser). Cadascú rep \(60:12=5\) caramels i \(84:12=7\) bombons.", r"Como máximo 12 alumnos (y 12 es mayor que lo que sobra, 3 y 6, como tiene que ser). Cada uno recibe \(60:12=5\) caramelos y \(84:12=7\) bombones.", r"At most 12 students (and 12 is bigger than what's left over, 3 and 6, as it must be). Each one gets \(60:12=5\) sweets and \(84:12=7\) chocolates.")))
s10 += box('prop', L('mcm o MCD?', '¿mcm o MCD?', 'lcm or gcd?'),
  '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Si el problema…', 'Si el problema…', 'If the problem…') + '</th><th>' + L('Fem servir', 'Usamos', 'Use') + '</th></tr></thead><tbody>'
  + '<tr><td class="l">' + L('parla de coses que es repeteixen i tornen a <strong>coincidir</strong>', 'habla de cosas que se repiten y vuelven a <strong>coincidir</strong>', 'is about things that repeat and <strong>coincide</strong> again') + '</td><td><strong>' + L('mcm', 'mcm', 'lcm') + '</strong></td></tr>'
  + '<tr><td class="l">' + L('busca el nombre <strong>més xicotet</strong> que és múltiple de diversos', 'busca el número <strong>más pequeño</strong> que es múltiplo de varios', 'asks for the <strong>smallest</strong> number that is a multiple of several') + '</td><td><strong>' + L('mcm', 'mcm', 'lcm') + '</strong></td></tr>'
  + '<tr><td class="l">' + L('vol <strong>repartir</strong> o <strong>tallar</strong> en parts iguals, sense que sobre res', 'quiere <strong>repartir</strong> o <strong>cortar</strong> en partes iguales, sin que sobre nada', 'wants to <strong>share</strong> or <strong>cut</strong> into equal parts, with nothing left') + '</td><td><strong>' + L('MCD', 'MCD', 'gcd') + '</strong></td></tr>'
  + '<tr><td class="l">' + L('busca el nombre <strong>més gran</strong> que divideix diversos', 'busca el número <strong>más grande</strong> que divide a varios', 'asks for the <strong>biggest</strong> number that divides several') + '</td><td><strong>' + L('MCD', 'MCD', 'gcd') + '</strong></td></tr>'
  + '</tbody></table></div>')
s10 += practice([
  ('★', L(r"a) En una classe hi ha 18 xics i 24 xiques. Volem fer el màxim nombre d'equips, tots amb el mateix nombre de xics i de xiques. Quants equips farem? b) Volem tallar dues cintes de 40 i 56 cm en trossos iguals, el més llargs possible. Quant farà cada tros? Quants en tindrem?", r"a) En una clase hay 18 chicos y 24 chicas. Queremos hacer el máximo número de equipos, todos con el mismo número de chicos y de chicas. ¿Cuántos equipos haremos? b) Queremos cortar dos cintas de 40 y 56 cm en trozos iguales, lo más largos posible. ¿Cuánto medirá cada trozo? ¿Cuántos tendremos?", r"a) A class has 18 boys and 24 girls. We want as many teams as possible, all with the same number of boys and of girls. How many teams? b) We want to cut two ribbons of 40 and 56 cm into equal pieces, as long as possible. How long is each piece? How many pieces?")),
  ('★★', L(r"c) Una habitació fa 420 cm per 300 cm. Volem posar-hi rajoles quadrades el més grans possible sense tallar-ne cap. Quin costat tindran? Quantes en calen? d) Digues si cal el mcm o el MCD i resol: «Volem dividir dues barres de 30 i 42 cm en trossos iguals el més llargs possible».", r"c) Una habitación mide 420 cm por 300 cm. Queremos poner baldosas cuadradas lo más grandes posible sin cortar ninguna. ¿Qué lado tendrán? ¿Cuántas hacen falta? d) Di si hace falta el mcm o el MCD y resuelve: «Queremos dividir dos barras de 30 y 42 cm en trozos iguales lo más largos posible».", r"c) A room is 420 cm by 300 cm. We want the biggest square tiles possible without cutting any. What side will they have? How many are needed? d) Say whether you need the lcm or the gcd and solve: “We want to split two bars of 30 and 42 cm into equal pieces as long as possible”.")),
  ('★★★', L(r"e) Un fuster té dos taulons de 180 i 240 cm. Els vol tallar en trossos iguals, el més llargs possible. Quants trossos obtindrà? Si cada tall li costa 1 minut, quants minuts tardarà? f) Quin és el nombre més gran que divideix 100 i 136 i dona residu 4 en tots dos casos?", r"e) Un carpintero tiene dos tablones de 180 y 240 cm. Los quiere cortar en trozos iguales, lo más largos posible. ¿Cuántos trozos obtendrá? Si cada corte le cuesta 1 minuto, ¿cuántos minutos tardará? f) ¿Cuál es el mayor número que divide a 100 y a 136 y da resto 4 en los dos casos?", r"e) A carpenter has two planks of 180 and 240 cm and wants to cut them into equal pieces, as long as possible. How many pieces? If each cut takes 1 minute, how many minutes will it take? f) What is the largest number that divides 100 and 136 leaving remainder 4 in both cases?"))],
  P(r"a) \(\text{MCD}(18,24)=6\) equips, de 3 xics i 4 xiques. &nbsp; b) \(\text{MCD}(40,56)=8\) cm; \(5+7=12\) trossos.", r"a) \(\text{MCD}(18,24)=6\) equipos, de 3 chicos y 4 chicas. &nbsp; b) \(\text{MCD}(40,56)=8\) cm; \(5+7=12\) trozos.", r"a) \(\text{gcd}(18,24)=6\) teams, of 3 boys and 4 girls. &nbsp; b) \(\text{gcd}(40,56)=8\) cm; \(5+7=12\) pieces.")
  + P(r"c) \(\text{MCD}(420,300)=60\) cm; \(7\cdot5=35\) rajoles. &nbsp; d) MCD: \(\text{MCD}(30,42)=6\) cm (5 i 7 trossos).", r"c) \(\text{MCD}(420,300)=60\) cm; \(7\cdot5=35\) baldosas. &nbsp; d) MCD: \(\text{MCD}(30,42)=6\) cm (5 y 7 trozos).", r"c) \(\text{gcd}(420,300)=60\) cm; \(7\cdot5=35\) tiles. &nbsp; d) gcd: \(\text{gcd}(30,42)=6\) cm (5 and 7 pieces).")
  + P(r"e) \(\text{MCD}(180,240)=60\) cm: \(3+4=7\) trossos; talls: \(2+3=5\) minuts. &nbsp; f) \(\text{MCD}(96,132)=12\) (i \(12>4\)).", r"e) \(\text{MCD}(180,240)=60\) cm: \(3+4=7\) trozos; cortes: \(2+3=5\) minutos. &nbsp; f) \(\text{MCD}(96,132)=12\) (y \(12>4\)).", r"e) \(\text{gcd}(180,240)=60\) cm: \(3+4=7\) pieces; cuts: \(2+3=5\) minutes. &nbsp; f) \(\text{gcd}(96,132)=12\) (and \(12>4\))."))

# ============================================================ muntatge
SECS = [
  (L('La relació de divisibilitat', 'La relación de divisibilidad', 'The divisibility relation'), s1),
  (L("Múltiples d'un nombre", 'Múltiplos de un número', 'Multiples of a number'), s2),
  (L("Divisors d'un nombre", 'Divisores de un número', 'Divisors of a number'), s3),
  (L('Criteris de divisibilitat', 'Criterios de divisibilidad', 'Divisibility rules'), s4),
  (L('Nombres primers i compostos', 'Números primos y compuestos', 'Prime and composite numbers'), s5),
  (L('Descomposició en factors primers', 'Descomposición en factores primos', 'Prime factorisation'), s6),
  (L('Mínim comú múltiple', 'Mínimo común múltiplo', 'Least common multiple'), s7),
  (L('Problemes de mcm', 'Problemas de mcm', 'LCM problems'), s8),
  (L('Màxim comú divisor', 'Máximo común divisor', 'Greatest common divisor'), s9),
  (L('Problemes de MCD', 'Problemas de MCD', 'GCD problems'), s10),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Divisibilitat · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 2 (Divisibilitat) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "÷";')
assert 'Divisibilitat · FentMates' in head and 'content: "÷"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">2.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 2", "Unidad 2", "Unit 2")}</span>
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
    <span class="kicker">{L("Apunts de teoria · 1r ESO · Matemàtiques", "Apuntes de teoría · 1º ESO · Matemáticas", "Theory notes · 1st ESO · Mathematics")}</span>
    <h1><span class="u">{L("Unitat 2", "Unidad 2", "Unit 2")}</span> · {L("Divisibilitat", "Divisibilidad", "Divisibility")}</h1>
    <p>{L("Múltiples i divisors, criteris de divisibilitat, nombres primers i compostos, descomposició en factors primers, mínim comú múltiple i màxim comú divisor, i com fer-los servir per a resoldre problemes: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Múltiplos y divisores, criterios de divisibilidad, números primos y compuestos, descomposición en factores primos, mínimo común múltiplo y máximo común divisor, y cómo usarlos para resolver problemas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "Multiples and divisors, divisibility rules, prime and composite numbers, prime factorisation, least common multiple and greatest common divisor, and how to use them to solve problems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 2: Divisibilitat · 1r ESO", "Apuntes de teoría · Unidad 2: Divisibilidad · 1º ESO", "Theory notes · Unit 2: Divisibility · 1st ESO")}</p>
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

# FentMates: enllaça el tema comú (logo i colors del bloc) a les pàgines generades
import runpy as _runpy, os as _os
_d = _os.path.dirname(_os.path.abspath(__file__))
while _os.path.basename(_d) != "_eines":
    _d = _os.path.dirname(_d)
_runpy.run_path(_os.path.join(_d, "tema", "aplica.py"), run_name="__main__")
