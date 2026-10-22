import os, re, sys

# Genera materials/1eso/t4-fraccions.html. Ús: python3 _eines/apunts/1eso-t4/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t4-fraccions.html")

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
def prob(q, *steps):
    return '<li><p class="prob-q">' + q + '</p><div class="steps">' + ''.join(f'<div class="step">{s}</div>' for s in steps) + '</div></li>\n'
def practice(items, sol):
    lis = ''.join(f'<li><span class="stars">{st}</span> {t}</li>' for st, t in items)
    return box('pr', '✍ ' + L('Practica', 'Practica', 'Practice'),
               f'<ol class="ex-list">{lis}</ol><details class="sol"><summary>{L("Mostra la solució", "Mostrar la solución", "Show the solution")}</summary><div>{sol}</div></details>')
def sec(i, title, body):
    return (f'\n<!-- ======================= 4.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">4.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def drill(kind, va, es, en):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin" type="text" inputmode="text" autocomplete="off" spellcheck="false" aria-label="resultat"></label><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs, attr='b'):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-{attr}="{v}">{t}</button>' for v, t in pairs) + '</div>'
def nin(k, va, es, en, val, cls='s', mode='numeric'):
    lab = L(va, es, en) + ' ' if va else ''
    return f'<label>{lab}<input class="tin {cls}" type="text" inputmode="{mode}" data-k="{k}" value="{val}" autocomplete="off" aria-label="{k}"></label>'
def fin(kn, kd, n, d, mode='numeric'):
    return (f'<span class="frin"><input class="tin s" type="text" inputmode="{mode}" data-k="{kn}" value="{n}" autocomplete="off" aria-label="numerador"><i></i>'
            f'<input class="tin s" type="text" inputmode="{mode}" data-k="{kd}" value="{d}" autocomplete="off" aria-label="denominador"></span>')
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def hier(presets):
    keys = ''.join(f'<button type="button" data-ins="{k}">{k}</button>' for k in ['/', '·', ':', '(', ')', '[', ']'])
    q = ''.join(f'<button type="button" data-e="{e}">{e.replace("-", "−")}</button>' for e in presets)
    return f'''<div class="widget w-hier">
  <div class="wt">🧮 {L("Calculadora pas a pas", "Calculadora paso a paso", "Step-by-step calculator")}</div>
  <div class="wrow"><label>{L("Expressió", "Expresión", "Expression")} <input class="tin w" type="text" value="{presets[0]}" autocomplete="off" spellcheck="false" aria-label="expressió"></label></div>
  <div class="quick kp"><span class="ql">⌨</span>{keys}</div>
  <div class="quick"><span class="ql">⚡</span>{q}</div>
  <div class="hsteps"></div>
  <div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><span class="step-count"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
D = r'\tri{de}{de}{of}'
MCD = r'\tri{MCD}{MCD}{gcd}'
MCM = r'\tri{mcm}{mcm}{lcm}'

# ---------- figures SVG estàtiques ----------
def svg_rect(rows, cols, on, c=26):
    W, H = cols * c, rows * c
    g = ''.join(f'<rect class="{"fr-on" if k < on else "fr-off"}" x="{(k % cols) * c}" y="{(k // cols) * c}" width="{c}" height="{c}"/>' for k in range(rows * cols))
    g += ''.join(f'<line class="fr-ln" x1="{i * c}" y1="0" x2="{i * c}" y2="{H}"/>' for i in range(1, cols))
    g += ''.join(f'<line class="fr-ln" x1="0" y1="{j * c}" x2="{W}" y2="{j * c}"/>' for j in range(1, rows))
    return f'<svg viewBox="-1 -1 {W + 2} {H + 2}" style="width:{W + 2}px"><g>{g}</g><rect class="fr-ln" x="0" y="0" width="{W}" height="{H}"/></svg>'
def svg_circ(n, on, R=46):
    import math
    cx = cy = R + 1; g = ''
    for k in range(n):
        a0 = -math.pi / 2 + k * 2 * math.pi / n; a1 = a0 + 2 * math.pi / n
        fill = 'var(--accent)' if k < on else 'var(--surface-2)'
        g += (f'<path class="fr-ln" style="fill:{fill}" d="M{cx} {cy} L{cx + R * math.cos(a0):.2f} {cy + R * math.sin(a0):.2f} '
              f'A{R} {R} 0 0 1 {cx + R * math.cos(a1):.2f} {cy + R * math.sin(a1):.2f} Z"/>')
    return f'<svg viewBox="0 0 {2 * R + 2} {2 * R + 2}" style="width:{2 * R + 2}px">{g}</svg>'
def svg_bar(n, on, W=220, H=30, cls='fr-on'):
    c = W / n
    g = ''.join(f'<rect class="{cls if k < on else "fr-off"}" x="{k * c:.2f}" y="0" width="{c:.2f}" height="{H}"/>' for k in range(n))
    g += ''.join(f'<line class="fr-ln" x1="{k * c:.2f}" y1="0" x2="{k * c:.2f}" y2="{H}"/>' for k in range(1, n))
    return f'<svg viewBox="-1 -1 {W + 2} {H + 2}" style="width:{W + 2}px">{g}<rect class="fr-ln" x="0" y="0" width="{W}" height="{H}"/></svg>'
def svg_line(den, units, on, W=420):
    X0, X1 = 14, W - 14; x = lambda v: X0 + v / units * (X1 - X0)
    g = f'<line class="nl-ax" x1="4" y1="22" x2="{W - 4}" y2="22"/><line class="nl-seg" x1="{x(0)}" y1="22" x2="{x(on / den)}" y2="22"/>'
    for k in range(units * den + 1):
        big = k % den == 0
        g += f'<line class="{"nl-tb" if big else "nl-tk"}" x1="{x(k / den):.1f}" y1="{14 if big else 17}" x2="{x(k / den):.1f}" y2="{30 if big else 27}"/>'
        if big: g += f'<text class="fr-t" x="{x(k / den):.1f}" y="48" text-anchor="middle">{k // den}</text>'
    g += f'<circle class="nl-dot" cx="{x(on / den):.1f}" cy="22" r="6" style="fill:var(--accent)"/>'
    return f'<svg viewBox="0 0 {W} 54" style="width:{W}px">{g}</svg>'
def figs(*items):
    return '<div class="figs">' + ''.join(f'<figure>{s}<figcaption>{c}</figcaption></figure>' for s, c in items) + '</div>'
def brows(*rows):
    return '<div style="max-width:460px;margin:10px auto">' + ''.join(f'<div class="brow"><span class="bl">\\(\\displaystyle {t}\\)</span>{s}</div>' for t, s in rows) + '</div>'

# ============================================================ 4.1
s1 = box('def', L('Què és una fracció?', '¿Qué es una fracción?', 'What is a fraction?'),
  P(r"Una <strong>fracció</strong> és una expressió \(\dfrac{a}{b}\) formada per dos nombres naturals separats per una ratlla, amb \(b\neq0\):",
    r"Una <strong>fracción</strong> es una expresión \(\dfrac{a}{b}\) formada por dos números naturales separados por una raya, con \(b\neq0\):",
    r"A <strong>fraction</strong> is an expression \(\dfrac{a}{b}\) made of two whole numbers separated by a bar, with \(b\neq0\):")
  + ul(L(r"El <strong>denominador</strong> \(b\) (baix) indica en quantes <strong>parts iguals</strong> dividim la unitat.", r"El <strong>denominador</strong> \(b\) (abajo) indica en cuántas <strong>partes iguales</strong> dividimos la unidad.", r"The <strong>denominator</strong> \(b\) (bottom) tells us how many <strong>equal parts</strong> the whole is split into."),
       L(r"El <strong>numerador</strong> \(a\) (dalt) indica quantes d'aquestes parts <strong>agafem</strong>.", r"El <strong>numerador</strong> \(a\) (arriba) indica cuántas de esas partes <strong>tomamos</strong>.", r"The <strong>numerator</strong> \(a\) (top) tells us how many of those parts we <strong>take</strong>."))
  + figs((svg_circ(4, 3), r'\(\frac{3}{4}\)'), (svg_rect(2, 4, 3), r'\(\frac{3}{8}\)'), (svg_bar(5, 2), r'\(\frac{2}{5}\)'))
  + note(r"Les parts han de ser <strong>iguals</strong>. Si partim una pizza en 4 trossos de mides diferents, cada tros <strong>no</strong> és \(\frac{1}{4}\).",
         r"Las partes tienen que ser <strong>iguales</strong>. Si partimos una pizza en 4 trozos de tamaños distintos, cada trozo <strong>no</strong> es \(\frac{1}{4}\).",
         r"The parts must be <strong>equal</strong>. If we cut a pizza into 4 pieces of different sizes, each piece is <strong>not</strong> \(\frac{1}{4}\)."))
s1 += sub('Els tres significats d\'una fracció', 'Los tres significados de una fracción', 'The three meanings of a fraction')
s1 += box('prop', L('Una fracció pot ser…', 'Una fracción puede ser…', 'A fraction can be…'),
  ol(L(r"<strong>Part de la unitat.</strong> \(\frac{3}{4}\) d'una pizza: la dividim en 4 parts iguals i en mengem 3.", r"<strong>Parte de la unidad.</strong> \(\frac{3}{4}\) de una pizza: la dividimos en 4 partes iguales y nos comemos 3.", r"<strong>Part of a whole.</strong> \(\frac{3}{4}\) of a pizza: cut it into 4 equal parts and eat 3."),
     L(r"<strong>Una divisió (quocient).</strong> \(\frac{3}{4}=3:4=0\dc75\). Si repartim 3 pizzes entre 4 amics, cadascú en menja \(\frac{3}{4}\). Si la divisió és exacta, la fracció és un nombre natural: \(\frac{12}{4}=12:4=3\).", r"<strong>Una división (cociente).</strong> \(\frac{3}{4}=3:4=0\dc75\). Si repartimos 3 pizzas entre 4 amigos, cada uno come \(\frac{3}{4}\). Si la división es exacta, la fracción es un número natural: \(\frac{12}{4}=12:4=3\).", r"<strong>A division (quotient).</strong> \(\frac{3}{4}=3:4=0\dc75\). If we share 3 pizzas among 4 friends, each one eats \(\frac{3}{4}\). If the division is exact, the fraction is a whole number: \(\frac{12}{4}=12:4=3\)."),
     L(r"<strong>Un operador.</strong> La fracció «actua» sobre una quantitat: \(\frac{3}{4}\) de \(20\) és \(15\) (dividim 20 entre 4 i multipliquem per 3). Ho veurem a l'apartat 4.2.", r"<strong>Un operador.</strong> La fracción «actúa» sobre una cantidad: \(\frac{3}{4}\) de \(20\) es \(15\) (dividimos 20 entre 4 y multiplicamos por 3). Lo veremos en el apartado 4.2.", r"<strong>An operator.</strong> The fraction “acts” on an amount: \(\frac{3}{4}\) of \(20\) is \(15\) (divide 20 by 4 and multiply by 3). We'll see this in section 4.2.")))
RD = [('1', '2', 'un mig', 'un medio', 'one half'), ('2', '3', 'dos terços', 'dos tercios', 'two thirds'), ('3', '4', 'tres quarts', 'tres cuartos', 'three quarters'),
      ('4', '5', 'quatre cinquens', 'cuatro quintos', 'four fifths'), ('5', '6', 'cinc sisens', 'cinco sextos', 'five sixths'), ('1', '7', 'un seté', 'un séptimo', 'one seventh'),
      ('3', '8', 'tres huitens', 'tres octavos', 'three eighths'), ('7', '9', 'set novens', 'siete novenos', 'seven ninths'), ('9', '10', 'nou desens', 'nueve décimos', 'nine tenths'),
      ('5', '12', 'cinc dotzens', 'cinco doceavos', 'five twelfths')]
s1 += box('def', L('Com es llegeixen les fraccions', 'Cómo se leen las fracciones', 'How to read fractions'),
  P(r"Llegim el numerador i després el denominador amb aquests noms. A partir d'11 afegim <em>-é / -ens</em>: onzens, dotzens, tretzens…",
    r"Leemos el numerador y después el denominador con estos nombres. A partir de 11 añadimos <em>-avo</em>: onceavos, doceavos, treceavos…",
    r"Read the numerator and then the denominator with these names. From 11 on we add <em>-th</em>: elevenths, twelfths, thirteenths…")
  + '<div class="tbl-wrap"><table class="data"><tbody>' + ''.join(f'<tr><td>\\(\\frac{{{a}}}{{{b}}}\\)</td><td class="l">{L(va, es, en)}</td></tr>' for a, b, va, es, en in RD) + '</tbody></table></div>')
s1 += box('prop', L('Fraccions pròpies i impròpies', 'Fracciones propias e impropias', 'Proper and improper fractions'),
  ul(L(r"Si el numerador és <strong>menor</strong> que el denominador, la fracció és <strong>pròpia</strong> i val menys que 1: \(\ \frac{3}{4}<1\).", r"Si el numerador es <strong>menor</strong> que el denominador, la fracción es <strong>propia</strong> y vale menos que 1: \(\ \frac{3}{4}<1\).", r"If the numerator is <strong>smaller</strong> than the denominator, the fraction is <strong>proper</strong> and worth less than 1: \(\ \frac{3}{4}<1\)."),
     L(r"Si numerador i denominador són <strong>iguals</strong>, la fracció val exactament 1: \(\ \frac{5}{5}=1\).", r"Si numerador y denominador son <strong>iguales</strong>, la fracción vale exactamente 1: \(\ \frac{5}{5}=1\).", r"If numerator and denominator are <strong>equal</strong>, the fraction is exactly 1: \(\ \frac{5}{5}=1\)."),
     L(r"Si el numerador és <strong>major</strong> que el denominador, la fracció és <strong>impròpia</strong> i val més que 1. Dividint, en traiem les unitats senceres: \(\ \frac{7}{4}=1+\frac{3}{4}\), perquè \(7:4\) dona quocient 1 i residu 3.", r"Si el numerador es <strong>mayor</strong> que el denominador, la fracción es <strong>impropia</strong> y vale más que 1. Dividiendo, sacamos las unidades enteras: \(\ \frac{7}{4}=1+\frac{3}{4}\), porque \(7:4\) da cociente 1 y resto 3.", r"If the numerator is <strong>bigger</strong> than the denominator, the fraction is <strong>improper</strong> and worth more than 1. Dividing gives the wholes: \(\ \frac{7}{4}=1+\frac{3}{4}\), because \(7:4\) gives quotient 1 and remainder 3."))
  + figs((svg_rect(1, 4, 4) + svg_rect(1, 4, 3), r'\(\frac{7}{4}=1+\frac{3}{4}\)'))
  + f'''<div class="widget" id="w-part">
  <div class="wt">🍕 {L("Representa una fracció", "Representa una fracción", "Draw a fraction")}</div>
  <div class="wrow">{nin("a", "Numerador", "Numerador", "Numerator", "3")}{nin("b", "Denominador", "Denominador", "Denominator", "4")}{seg([("rect", L("Rectangle", "Rectángulo", "Rectangle")), ("circ", L("Cercle", "Círculo", "Circle")), ("line", L("Recta", "Recta", "Number line"))], "rect")}</div>
  {quick([("3/4", "3/4"), ("5/8", "5/8"), ("2/3", "2/3"), ("9/10", "9/10"), ("6/6", "6/6"), ("7/4", "7/4"), ("11/5", "11/5"), ("12/4", "12/4")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''')
s1 += level(1, 1,
  prob(L("Quina fracció representa la part pintada de cada figura?", "¿Qué fracción representa la parte pintada de cada figura?", "What fraction does the shaded part of each figure show?")
       + figs((svg_rect(2, 4, 3), 'A'), (svg_circ(6, 5), 'B'), (svg_bar(5, 2), 'C'), (svg_rect(2, 2, 2), 'D')),
       P(r"Comptem les parts <strong>iguals</strong> (denominador) i les pintades (numerador):", r"Contamos las partes <strong>iguales</strong> (denominador) y las pintadas (numerador):", r"Count the <strong>equal</strong> parts (denominator) and the shaded ones (numerator):"),
       r'\[\text{A: }\frac{3}{8}\qquad\text{B: }\frac{5}{6}\qquad\text{C: }\frac{2}{5}\qquad\text{D: }\frac{2}{4}\]',
       P(r"En la D, la part pintada és la meitat: \(\frac{2}{4}\) i \(\frac{1}{2}\) representen la mateixa quantitat (són <em>equivalents</em>, apartat 4.4).", r"En la D, la parte pintada es la mitad: \(\frac{2}{4}\) y \(\frac{1}{2}\) representan la misma cantidad (son <em>equivalentes</em>, apartado 4.4).", r"In D the shaded part is a half: \(\frac{2}{4}\) and \(\frac{1}{2}\) are the same amount (they're <em>equivalent</em>, section 4.4).")),
  prob(L(r"Repartim 3 pizzes iguals entre 4 amics. Quina fracció de pizza menja cadascú? Escriu-la com a divisió.", r"Repartimos 3 pizzas iguales entre 4 amigos. ¿Qué fracción de pizza come cada uno? Escríbela como división.", r"We share 3 equal pizzas among 4 friends. What fraction of a pizza does each one eat? Write it as a division."),
       P(r"Repartir és dividir: cada amic menja \(3:4\) pizzes.", r"Repartir es dividir: cada amigo come \(3:4\) pizzas.", r"Sharing is dividing: each friend eats \(3:4\) pizzas."),
       r'\[3:4=\boxed{\frac{3}{4}}=0\dc75\ \tri{pizzes}{pizzas}{pizzas}\]'))
s1 += level(2, 3,
  prob(L(r"Classifica en pròpies, impròpies o iguals a la unitat: \(\ \frac{5}{8},\ \frac{9}{4},\ \frac{7}{7},\ \frac{12}{5},\ \frac{3}{10}\). Escriu les impròpies com a unitats senceres més una fracció pròpia.", r"Clasifica en propias, impropias o iguales a la unidad: \(\ \frac{5}{8},\ \frac{9}{4},\ \frac{7}{7},\ \frac{12}{5},\ \frac{3}{10}\). Escribe las impropias como unidades enteras más una fracción propia.", r"Sort into proper, improper or equal to one: \(\ \frac{5}{8},\ \frac{9}{4},\ \frac{7}{7},\ \frac{12}{5},\ \frac{3}{10}\). Write the improper ones as wholes plus a proper fraction."),
       P(r"Pròpies (numerador menor): \(\frac{5}{8}\) i \(\frac{3}{10}\). Igual a 1: \(\frac{7}{7}\). Impròpies: \(\frac{9}{4}\) i \(\frac{12}{5}\).", r"Propias (numerador menor): \(\frac{5}{8}\) y \(\frac{3}{10}\). Igual a 1: \(\frac{7}{7}\). Impropias: \(\frac{9}{4}\) y \(\frac{12}{5}\).", r"Proper (smaller numerator): \(\frac{5}{8}\) and \(\frac{3}{10}\). Equal to 1: \(\frac{7}{7}\). Improper: \(\frac{9}{4}\) and \(\frac{12}{5}\)."),
       P(r"Dividim: \(9:4\) dona 2 i residu 1; \(12:5\) dona 2 i residu 2.", r"Dividimos: \(9:4\) da 2 y resto 1; \(12:5\) da 2 y resto 2.", r"Divide: \(9:4\) gives 2 remainder 1; \(12:5\) gives 2 remainder 2.") + r'\[\frac{9}{4}=\boxed{2+\frac{1}{4}}\qquad \frac{12}{5}=\boxed{2+\frac{2}{5}}\]'))
s1 += level(3, 4,
  prob(L(r"Representa la fracció \(\frac{7}{4}\) en la recta numèrica.", r"Representa la fracción \(\frac{7}{4}\) en la recta numérica.", r"Show the fraction \(\frac{7}{4}\) on the number line."),
       P(r"Com que \(\frac{7}{4}=1+\frac{3}{4}\), estarà entre 1 i 2. Dividim cada unitat en 4 parts iguals (el denominador)…", r"Como \(\frac{7}{4}=1+\frac{3}{4}\), estará entre 1 y 2. Dividimos cada unidad en 4 partes iguales (el denominador)…", r"Since \(\frac{7}{4}=1+\frac{3}{4}\), it lies between 1 and 2. Split each whole into 4 equal parts (the denominator)…"),
       P(r"…i comptem 7 parts des del 0:", r"…y contamos 7 partes desde el 0:", r"…and count 7 parts from 0:") + figs((svg_line(4, 2, 7), r'\(\frac{7}{4}\)'))))
s1 += practice([
  ('★', L(r"a) Partim una pizza en 8 trossos iguals i ens en mengem 3. Quina fracció ens hem menjat? Com es llegeix? b) Quina fracció de la setmana són 3 dies?", r"a) Partimos una pizza en 8 trozos iguales y nos comemos 3. ¿Qué fracción nos hemos comido? ¿Cómo se lee? b) ¿Qué fracción de la semana son 3 días?", r"a) We cut a pizza into 8 equal slices and eat 3. What fraction have we eaten? How do you read it? b) What fraction of a week is 3 days?")),
  ('★★', L(r"c) Classifica: \(\frac{4}{9}\), \(\frac{11}{6}\), \(\frac{8}{8}\). d) Escriu \(\frac{13}{5}\) com a unitats senceres més una fracció pròpia.", r"c) Clasifica: \(\frac{4}{9}\), \(\frac{11}{6}\), \(\frac{8}{8}\). d) Escribe \(\frac{13}{5}\) como unidades enteras más una fracción propia.", r"c) Classify: \(\frac{4}{9}\), \(\frac{11}{6}\), \(\frac{8}{8}\). d) Write \(\frac{13}{5}\) as wholes plus a proper fraction.")),
  ('★★★', L(r"e) Quina fracció de l'hora són 25 minuts? f) Escriu una fracció amb denominador 7 que estiga entre 1 i 2.", r"e) ¿Qué fracción de la hora son 25 minutos? f) Escribe una fracción con denominador 7 que esté entre 1 y 2.", r"e) What fraction of an hour is 25 minutes? f) Write a fraction with denominator 7 that lies between 1 and 2."))],
  P(r"a) \(\frac{3}{8}\), tres huitens. &nbsp; b) \(\frac{3}{7}\).", r"a) \(\frac{3}{8}\), tres octavos. &nbsp; b) \(\frac{3}{7}\).", r"a) \(\frac{3}{8}\), three eighths. &nbsp; b) \(\frac{3}{7}\).")
  + P(r"c) Pròpia, impròpia, igual a 1. &nbsp; d) \(\frac{13}{5}=2+\frac{3}{5}\).", r"c) Propia, impropia, igual a 1. &nbsp; d) \(\frac{13}{5}=2+\frac{3}{5}\).", r"c) Proper, improper, equal to 1. &nbsp; d) \(\frac{13}{5}=2+\frac{3}{5}\).")
  + P(r"e) Una hora té 60 minuts: \(\frac{25}{60}\). &nbsp; f) Qualsevol de \(\frac{8}{7}\) a \(\frac{13}{7}\), per exemple \(\frac{10}{7}\).", r"e) Una hora tiene 60 minutos: \(\frac{25}{60}\). &nbsp; f) Cualquiera de \(\frac{8}{7}\) a \(\frac{13}{7}\), por ejemplo \(\frac{10}{7}\).", r"e) An hour has 60 minutes: \(\frac{25}{60}\). &nbsp; f) Any from \(\frac{8}{7}\) to \(\frac{13}{7}\), for example \(\frac{10}{7}\)."))

# ============================================================ 4.2
s2 = box('def', L("Fracció d'un nombre", 'Fracción de un número', 'Fraction of a number'),
  P(r"Per a calcular la fracció \(\frac{a}{b}\) d'un nombre, el <strong>dividim entre el denominador</strong> i <strong>multipliquem pel numerador</strong>:",
    r"Para calcular la fracción \(\frac{a}{b}\) de un número, lo <strong>dividimos entre el denominador</strong> y <strong>multiplicamos por el numerador</strong>:",
    r"To find the fraction \(\frac{a}{b}\) of a number, <strong>divide it by the denominator</strong> and <strong>multiply by the numerator</strong>:")
  + r'\[\frac{3}{5}\ ' + D + r'\ 40=(40:5)\cdot3=8\cdot3=\boxed{24}\]'
  + brows((r'40', svg_bar(5, 3, 360, 30)))
  + P(r"Cada cinqué de 40 val 8, i en volem 3. També podem multiplicar primer i dividir després, perquè «de» vol dir <strong>multiplicar</strong>:",
      r"Cada quinto de 40 vale 8, y queremos 3. También podemos multiplicar primero y dividir después, porque «de» quiere decir <strong>multiplicar</strong>:",
      r"Each fifth of 40 is 8, and we want 3. We can also multiply first and divide afterwards, because “of” means <strong>multiply</strong>:")
  + r'\[\frac{3}{5}\ ' + D + r'\ 40=\frac{3\cdot40}{5}=\frac{120}{5}=24\]')
s2 += box('prop', L('El problema invers: conéixer la part i calcular el total', 'El problema inverso: conocer la parte y calcular el total', 'The reverse problem: knowing the part, finding the whole'),
  P(r"Si sabem que \(\frac{3}{5}\) d'un nombre són \(24\): cada cinqué val \(24:3=8\), i el total són 5 cinquens: \(8\cdot5=40\).",
    r"Si sabemos que \(\frac{3}{5}\) de un número son \(24\): cada quinto vale \(24:3=8\), y el total son 5 quintos: \(8\cdot5=40\).",
    r"If we know that \(\frac{3}{5}\) of a number is \(24\): each fifth is \(24:3=8\), and the whole is 5 fifths: \(8\cdot5=40\).")
  + r'\[\text{Total}=(\text{Part}:\text{numerador})\cdot\text{denominador}\]'
  + note(r"Comprova sempre el resultat: \(\frac{3}{5}\) de \(40\) ha de donar \(24\).", r"Comprueba siempre el resultado: \(\frac{3}{5}\) de \(40\) tiene que dar \(24\).", r"Always check: \(\frac{3}{5}\) of \(40\) must give \(24\).")
  + f'''<div class="widget" id="w-of">
  <div class="wt">▤ {L("Model de barres: fracció d'una quantitat", "Modelo de barras: fracción de una cantidad", "Bar model: fraction of an amount")}</div>
  <div class="wrow">{seg([("of", L("Calcula la part", "Calcula la parte", "Find the part")), ("tot", L("Calcula el total", "Calcula el total", "Find the whole"))], "of")}</div>
  <div class="wrow" style="margin-top:8px"><label>{L("Fracció", "Fracción", "Fraction")} {fin("a", "b", "3", "5")}</label><label><span data-p="of">{L("Total", "Total", "Whole")}</span><span data-p="tot">{L("Part coneguda", "Parte conocida", "Known part")}</span> <input class="tin" type="text" inputmode="numeric" data-k="n" value="40" autocomplete="off" aria-label="quantitat"></label></div>
  {quick([("3,5,40", "3/5 · 40"), ("2,3,45", "2/3 · 45"), ("5,6,48", "5/6 · 48"), ("7,8,32", "7/8 · 32"), ("4,7,490", "4/7 · 490"), ("3,4,1000", "3/4 · 1000")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('of', 'Entrena: fracció d\'un nombre', 'Entrena: fracción de un número', 'Train: fraction of a number'))
s2 += level(1, 1,
  prob(L(r"Calcula: a) \(\frac{5}{6}\) de \(48\) &nbsp; b) \(\frac{7}{8}\) de \(32\)", r"Calcula: a) \(\frac{5}{6}\) de \(48\) &nbsp; b) \(\frac{7}{8}\) de \(32\)", r"Work out: a) \(\frac{5}{6}\) of \(48\) &nbsp; b) \(\frac{7}{8}\) of \(32\)"),
       r'\[\text{a) }\ (48:6)\cdot5=8\cdot5=\boxed{40}\]', r'\[\text{b) }\ (32:8)\cdot7=4\cdot7=\boxed{28}\]'))
s2 += level(2, 2,
  prob(L(r"En una classe de 28 alumnes, \(\frac{3}{7}\) porten ulleres. Quants alumnes <strong>no</strong> en porten?", r"En una clase de 28 alumnos, \(\frac{3}{7}\) llevan gafas. ¿Cuántos alumnos <strong>no</strong> llevan?", r"In a class of 28 students, \(\frac{3}{7}\) wear glasses. How many <strong>don't</strong>?"),
       r'\[\frac{3}{7}\ ' + D + r'\ 28=(28:7)\cdot3=4\cdot3=12\ \tri{porten ulleres}{llevan gafas}{wear glasses}\]',
       r'\[28-12=\boxed{16}\ \tri{no en porten}{no llevan}{don\'t}\]',
       P(r"També: no en porten \(\frac{4}{7}\), i \(\frac{4}{7}\) de 28 és \(4\cdot4=16\).", r"También: no llevan \(\frac{4}{7}\), y \(\frac{4}{7}\) de 28 es \(4\cdot4=16\).", r"Or: \(\frac{4}{7}\) don't, and \(\frac{4}{7}\) of 28 is \(4\cdot4=16\).")))
s2 += level(3, 3,
  prob(L(r"Ja he llegit \(\frac{2}{5}\) d'un llibre, que són 120 pàgines. Quantes pàgines té el llibre? Quantes me'n queden?", r"Ya he leído \(\frac{2}{5}\) de un libro, que son 120 páginas. ¿Cuántas páginas tiene el libro? ¿Cuántas me quedan?", r"I've read \(\frac{2}{5}\) of a book, which is 120 pages. How many pages does it have? How many are left?"),
       P(r"Coneixem la part i busquem el total. Dos cinquens són 120, així que un cinqué és:", r"Conocemos la parte y buscamos el total. Dos quintos son 120, así que un quinto es:", r"We know the part and want the whole. Two fifths are 120, so one fifth is:") + r'\[120:2=60\ \tri{pàgines}{páginas}{pages}\]',
       r'\[\text{Total}=60\cdot5=\boxed{300}\qquad 300-120=\boxed{180}\ \tri{per llegir}{por leer}{to read}\]'))
s2 += practice([
  ('★', L(r"a) \(\frac{3}{4}\) de \(60\) &nbsp; b) \(\frac{2}{5}\) de \(60\)", r"a) \(\frac{3}{4}\) de \(60\) &nbsp; b) \(\frac{2}{5}\) de \(60\)", r"a) \(\frac{3}{4}\) of \(60\) &nbsp; b) \(\frac{2}{5}\) of \(60\)")),
  ('★★', L(r"c) \(\frac{4}{7}\) de \(490\). d) Un cotxe ha fet \(\frac{5}{9}\) d'un viatge de 450 km. Quants quilòmetres li queden?", r"c) \(\frac{4}{7}\) de \(490\). d) Un coche ha hecho \(\frac{5}{9}\) de un viaje de 450 km. ¿Cuántos kilómetros le quedan?", r"c) \(\frac{4}{7}\) of \(490\). d) A car has done \(\frac{5}{9}\) of a 450 km trip. How many kilometres are left?")),
  ('★★★', L(r"e) Els \(\frac{3}{8}\) d'un nombre són 27. Quin és el nombre? f) Calcula \(\frac{2}{3}\) de \(\frac{3}{4}\) de \(120\).", r"e) Los \(\frac{3}{8}\) de un número son 27. ¿Cuál es el número? f) Calcula \(\frac{2}{3}\) de \(\frac{3}{4}\) de \(120\).", r"e) \(\frac{3}{8}\) of a number is 27. What is the number? f) Work out \(\frac{2}{3}\) of \(\frac{3}{4}\) of \(120\)."))],
  P(r"a) \(15\cdot3=45\). &nbsp; b) \(12\cdot2=24\).", r"a) \(15\cdot3=45\). &nbsp; b) \(12\cdot2=24\).", r"a) \(15\cdot3=45\). &nbsp; b) \(12\cdot2=24\).")
  + P(r"c) \(70\cdot4=280\). &nbsp; d) Ha fet \(50\cdot5=250\) km; en queden \(200\) km.", r"c) \(70\cdot4=280\). &nbsp; d) Ha hecho \(50\cdot5=250\) km; quedan \(200\) km.", r"c) \(70\cdot4=280\). &nbsp; d) It's done \(50\cdot5=250\) km; \(200\) km are left.")
  + P(r"e) \(27:3=9\), \(9\cdot8=72\). &nbsp; f) \(\frac{3}{4}\) de 120 és 90, i \(\frac{2}{3}\) de 90 és \(60\).", r"e) \(27:3=9\), \(9\cdot8=72\). &nbsp; f) \(\frac{3}{4}\) de 120 es 90, y \(\frac{2}{3}\) de 90 es \(60\).", r"e) \(27:3=9\), \(9\cdot8=72\). &nbsp; f) \(\frac{3}{4}\) of 120 is 90, and \(\frac{2}{3}\) of 90 is \(60\)."))

# ============================================================ 4.3
PC = [('50', r'\frac{50}{100}=\frac{1}{2}', 'la meitat', 'la mitad', 'half'), ('25', r'\frac{25}{100}=\frac{1}{4}', 'la quarta part', 'la cuarta parte', 'a quarter'),
      ('75', r'\frac{75}{100}=\frac{3}{4}', 'tres quarts', 'tres cuartos', 'three quarters'), ('20', r'\frac{20}{100}=\frac{1}{5}', 'la cinquena part', 'la quinta parte', 'a fifth'),
      ('10', r'\frac{10}{100}=\frac{1}{10}', 'la desena part', 'la décima parte', 'a tenth'), ('100', r'\frac{100}{100}=1', 'tot', 'todo', 'the whole')]
s3 = box('def', L('Percentatge', 'Porcentaje', 'Percentage'),
  P(r"Un <strong>percentatge</strong> és una fracció amb denominador 100. El 35 % (es llegeix «trenta-cinc per cent») vol dir <strong>35 de cada 100</strong>:",
    r"Un <strong>porcentaje</strong> es una fracción con denominador 100. El 35 % (se lee «treinta y cinco por ciento») quiere decir <strong>35 de cada 100</strong>:",
    r"A <strong>percentage</strong> is a fraction with denominator 100. 35% (read “thirty-five per cent”) means <strong>35 out of every 100</strong>:")
  + r'\[35\,\%=\frac{35}{100}\]'
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>%</th><th>' + L('Fracció', 'Fracción', 'Fraction') + '</th><th>' + L('És…', 'Es…', 'It is…') + '</th></tr></thead><tbody>'
  + ''.join(f'<tr><td>\\({p}\\,\\%\\)</td><td>\\({f}\\)</td><td>{L(va, es, en)}</td></tr>' for p, f, va, es, en in PC) + '</tbody></table></div>')
s3 += box('prop', L("Percentatge d'un nombre", 'Porcentaje de un número', 'Percentage of a number'),
  P(r"Calcular un percentatge és calcular una fracció d'un nombre: multipliquem pel percentatge i dividim entre 100.",
    r"Calcular un porcentaje es calcular una fracción de un número: multiplicamos por el porcentaje y dividimos entre 100.",
    r"Finding a percentage means finding a fraction of a number: multiply by the percentage and divide by 100.")
  + r'\[20\,\%\ ' + D + r'\ 180=\frac{20\cdot180}{100}=\frac{3600}{100}=\boxed{36}\]'
  + P(r"Per a passar una fracció a percentatge, busquem una fracció equivalent amb denominador 100 (o dividim i multipliquem per 100):",
      r"Para pasar una fracción a porcentaje, buscamos una fracción equivalente con denominador 100 (o dividimos y multiplicamos por 100):",
      r"To turn a fraction into a percentage, find an equivalent fraction with denominator 100 (or divide and multiply by 100):")
  + r'\[\frac{3}{5}=\frac{3\cdot20}{5\cdot20}=\frac{60}{100}=60\,\%\]'
  + note(r"Càlcul mental: el 10 % és dividir entre 10; el 50 %, la meitat; el 25 %, la quarta part. El 30 % de 70 és \(3\cdot7=21\).",
         r"Cálculo mental: el 10 % es dividir entre 10; el 50 %, la mitad; el 25 %, la cuarta parte. El 30 % de 70 es \(3\cdot7=21\).",
         r"Mental maths: 10% means dividing by 10; 50% is half; 25% is a quarter. 30% of 70 is \(3\cdot7=21\).")
  + f'''<div class="widget" id="w-pct">
  <div class="wt">💯 {L("El quadrat del 100", "El cuadrado del 100", "The hundred square")}</div>
  <div class="wrow">{nin("p", "Percentatge (%)", "Porcentaje (%)", "Percentage (%)", "20")}{nin("n", "de", "de", "of", "180", "")}</div>
  {quick([("20,180", "20 % · 180"), ("45,80", "45 % · 80"), ("12,350", "12 % · 350"), ("85,1300", "85 % · 1300"), ("25,64", "25 % · 64"), ("75,20", "75 % · 20"), ("10,350", "10 % · 350")])}
  <div class="pgrid"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('pct', 'Entrena: percentatges', 'Entrena: porcentajes', 'Train: percentages'))
s3 += level(1, 1,
  prob(L(r"Calcula: a) el 45 % de 80 &nbsp; b) el 12 % de 350", r"Calcula: a) el 45 % de 80 &nbsp; b) el 12 % de 350", r"Work out: a) 45% of 80 &nbsp; b) 12% of 350"),
       r'\[\text{a) }\ \frac{45\cdot80}{100}=\frac{3600}{100}=\boxed{36}\qquad \text{b) }\ \frac{12\cdot350}{100}=\frac{4200}{100}=\boxed{42}\]'))
s3 += level(2, 2,
  prob(L(r"Una jaqueta costa 60 € i la rebaixen un 15 %. Quants euros ens estalviem? Quant paguem?", r"Una chaqueta cuesta 60 € y la rebajan un 15 %. ¿Cuántos euros nos ahorramos? ¿Cuánto pagamos?", r"A jacket costs €60 and has a 15% discount. How much do we save? How much do we pay?"),
       r'\[15\,\%\ ' + D + r'\ 60=\frac{15\cdot60}{100}=\frac{900}{100}=\boxed{9\ \text{€}}\ \tri{d\'estalvi}{de ahorro}{saved}\]',
       r'\[60-9=\boxed{51\ \text{€}}\]'))
s3 += level(3, 3,
  prob(L(r"En una enquesta a 400 persones, \(\frac{3}{8}\) prefereixen la platja, el 45 % la muntanya i la resta no ho sap. Quantes persones hi ha en cada grup? Quin percentatge no ho sap?", r"En una encuesta a 400 personas, \(\frac{3}{8}\) prefieren la playa, el 45 % la montaña y el resto no lo sabe. ¿Cuántas personas hay en cada grupo? ¿Qué porcentaje no lo sabe?", r"In a survey of 400 people, \(\frac{3}{8}\) prefer the beach, 45% the mountains and the rest don't know. How many people are in each group? What percentage don't know?"),
       r'\[\tri{Platja}{Playa}{Beach}:\ (400:8)\cdot3=150\qquad \tri{Muntanya}{Montaña}{Mountains}:\ \frac{45\cdot400}{100}=180\]',
       r'\[\tri{No ho sap}{No lo sabe}{Don\'t know}:\ 400-150-180=\boxed{70}\]',
       P(r"\(\frac{70}{400}=\frac{17\dc5}{100}\): el <strong>17,5 %</strong>. (També: \(\frac{3}{8}=37\dc5\,\%\), i \(100-37\dc5-45=17\dc5\).)", r"\(\frac{70}{400}=\frac{17\dc5}{100}\): el <strong>17,5 %</strong>. (También: \(\frac{3}{8}=37\dc5\,\%\), y \(100-37\dc5-45=17\dc5\).)", r"\(\frac{70}{400}=\frac{17\dc5}{100}\): <strong>17.5%</strong>. (Or: \(\frac{3}{8}=37\dc5\,\%\), and \(100-37\dc5-45=17\dc5\).)")))
s3 += practice([
  ('★', L(r"a) Calcula el 20 % de 150. b) Escriu el 35 % com a fracció i simplifica-la.", r"a) Calcula el 20 % de 150. b) Escribe el 35 % como fracción y simplifícala.", r"a) Work out 20% of 150. b) Write 35% as a fraction and simplify it.")),
  ('★★', L(r"c) Calcula el 85 % de 1300. d) Expressa en percentatge \(\frac{3}{4}\) i \(\frac{2}{5}\).", r"c) Calcula el 85 % de 1300. d) Expresa en porcentaje \(\frac{3}{4}\) y \(\frac{2}{5}\).", r"c) Work out 85% of 1300. d) Write \(\frac{3}{4}\) and \(\frac{2}{5}\) as percentages.")),
  ('★★★', L(r"e) En una classe de 25 alumnes, 6 han suspés. Quin percentatge ha suspés? f) El 20 % d'un nombre és 14. Quin és el nombre?", r"e) En una clase de 25 alumnos, 6 han suspendido. ¿Qué porcentaje ha suspendido? f) El 20 % de un número es 14. ¿Cuál es el número?", r"e) In a class of 25 students, 6 failed. What percentage failed? f) 20% of a number is 14. What is the number?"))],
  P(r"a) \(30\). &nbsp; b) \(\frac{35}{100}=\frac{7}{20}\).", r"a) \(30\). &nbsp; b) \(\frac{35}{100}=\frac{7}{20}\).", r"a) \(30\). &nbsp; b) \(\frac{35}{100}=\frac{7}{20}\).")
  + P(r"c) \(1105\). &nbsp; d) \(\frac{75}{100}=75\,\%\) i \(\frac{40}{100}=40\,\%\).", r"c) \(1105\). &nbsp; d) \(\frac{75}{100}=75\,\%\) y \(\frac{40}{100}=40\,\%\).", r"c) \(1105\). &nbsp; d) \(\frac{75}{100}=75\,\%\) and \(\frac{40}{100}=40\,\%\).")
  + P(r"e) \(\frac{6}{25}=\frac{24}{100}=24\,\%\). &nbsp; f) \(20\,\%=\frac{1}{5}\): el nombre és \(14\cdot5=70\).", r"e) \(\frac{6}{25}=\frac{24}{100}=24\,\%\). &nbsp; f) \(20\,\%=\frac{1}{5}\): el número es \(14\cdot5=70\).", r"e) \(\frac{6}{25}=\frac{24}{100}=24\,\%\). &nbsp; f) \(20\,\%=\frac{1}{5}\): the number is \(14\cdot5=70\)."))

# ============================================================ 4.4
s4 = box('def', L('Fraccions equivalents', 'Fracciones equivalentes', 'Equivalent fractions'),
  P(r"Dues fraccions són <strong>equivalents</strong> quan representen la <strong>mateixa quantitat</strong>, encara que s'escriguen amb nombres diferents:",
    r"Dos fracciones son <strong>equivalentes</strong> cuando representan la <strong>misma cantidad</strong>, aunque se escriban con números distintos:",
    r"Two fractions are <strong>equivalent</strong> when they show the <strong>same amount</strong>, even though they're written with different numbers:")
  + brows((r'\frac{1}{2}', svg_bar(2, 1, 360, 28)), (r'\frac{2}{4}', svg_bar(4, 2, 360, 28, 'fr-on2')), (r'\frac{4}{8}', svg_bar(8, 4, 360, 28, 'fr-on3')))
  + r'\[\frac{1}{2}=\frac{2}{4}=\frac{4}{8}\]')
s4 += box('prop', L('Com obtenim fraccions equivalents', 'Cómo obtenemos fracciones equivalentes', 'How to get equivalent fractions'),
  ul(L(r"<strong>Amplificació:</strong> multipliquem el numerador i el denominador pel <strong>mateix</strong> nombre: \(\ \frac{2}{3}=\frac{2\cdot4}{3\cdot4}=\frac{8}{12}\).", r"<strong>Amplificación:</strong> multiplicamos el numerador y el denominador por el <strong>mismo</strong> número: \(\ \frac{2}{3}=\frac{2\cdot4}{3\cdot4}=\frac{8}{12}\).", r"<strong>Scaling up:</strong> multiply numerator and denominator by the <strong>same</strong> number: \(\ \frac{2}{3}=\frac{2\cdot4}{3\cdot4}=\frac{8}{12}\)."),
     L(r"<strong>Simplificació:</strong> dividim el numerador i el denominador entre un <strong>divisor comú</strong>: \(\ \frac{12}{18}=\frac{12:2}{18:2}=\frac{6}{9}=\frac{6:3}{9:3}=\frac{2}{3}\).", r"<strong>Simplificación:</strong> dividimos el numerador y el denominador entre un <strong>divisor común</strong>: \(\ \frac{12}{18}=\frac{12:2}{18:2}=\frac{6}{9}=\frac{6:3}{9:3}=\frac{2}{3}\).", r"<strong>Simplifying:</strong> divide numerator and denominator by a <strong>common divisor</strong>: \(\ \frac{12}{18}=\frac{12:2}{18:2}=\frac{6}{9}=\frac{6:3}{9:3}=\frac{2}{3}\).")))
s4 += box('def', L('Fracció irreductible', 'Fracción irreducible', 'Simplest form'),
  P(r"Una fracció és <strong>irreductible</strong> quan ja no es pot simplificar més: el numerador i el denominador només tenen l'1 com a divisor comú. Per a arribar-hi d'un sol pas, dividim entre el " + r"\(\text{" + MCD + r"}\)" + r" (unitat 2):",
    r"Una fracción es <strong>irreducible</strong> cuando ya no se puede simplificar más: el numerador y el denominador solo tienen el 1 como divisor común. Para llegar a ella de un solo paso, dividimos entre el " + r"\(\text{" + MCD + r"}\)" + r" (unidad 2):",
    r"A fraction is in its <strong>simplest form</strong> when it can't be simplified any more: numerator and denominator have no common divisor except 1. To get there in one step, divide by the " + r"\(\text{" + MCD + r"}\)" + r" (unit 2):")
  + r'\[\text{' + MCD + r'}(36,48)=12\qquad \frac{36}{48}=\frac{36:12}{48:12}=\boxed{\frac{3}{4}}\]'
  + note(r"Una fracció té <strong>infinites</strong> fraccions equivalents, però només <strong>una</strong> d'irreductible. Quan acabes una operació, dona sempre el resultat en forma irreductible.",
         r"Una fracción tiene <strong>infinitas</strong> fracciones equivalentes, pero solo <strong>una</strong> irreducible. Cuando acabes una operación, da siempre el resultado en forma irreducible.",
         r"A fraction has <strong>infinitely many</strong> equivalent fractions, but only <strong>one</strong> simplest form. When you finish a calculation, always give the answer in its simplest form.")
  + f'''<div class="widget" id="w-eq">
  <div class="wt">🟰 {L("Fàbrica de fraccions equivalents", "Fábrica de fracciones equivalentes", "Equivalent fraction factory")}</div>
  <div class="wrow"><label>{L("Fracció", "Fracción", "Fraction")} {fin("a", "b", "2", "3")}</label>{nin("k", "Amplifica per", "Amplifica por", "Scale by", "4")}</div>
  {quick([("2,3,4", "2/3 × 4"), ("1,2,4", "1/2 × 4"), ("3,5,3", "3/5 × 3"), ("12,18,1", "12/18"), ("36,48,1", "36/48"), ("75,100,1", "75/100"), ("4,6,2", "4/6 × 2")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('simp', 'Entrena: fracció irreductible', 'Entrena: fracción irreducible', 'Train: simplest form'))
s4 += level(1, 1,
  prob(L(r"Escriu quatre fraccions equivalents a \(\frac{2}{5}\) per amplificació.", r"Escribe cuatro fracciones equivalentes a \(\frac{2}{5}\) por amplificación.", r"Write four fractions equivalent to \(\frac{2}{5}\) by scaling up."),
       r'\[\frac{2}{5}=\frac{2\cdot2}{5\cdot2}=\frac{4}{10}=\frac{6}{15}=\frac{8}{20}=\frac{10}{25}\]'),
  prob(L(r"Simplifica \(\frac{75}{100}\) fins a la fracció irreductible.", r"Simplifica \(\frac{75}{100}\) hasta la fracción irreducible.", r"Simplify \(\frac{75}{100}\) to its simplest form."),
       P(r"Pas a pas: tots dos acaben en 0 o 5, dividim entre 5 (dues vegades):", r"Paso a paso: los dos acaban en 0 o 5, dividimos entre 5 (dos veces):", r"Step by step: both end in 0 or 5, so divide by 5 (twice):") + r'\[\frac{75}{100}=\frac{15}{20}=\boxed{\frac{3}{4}}\]',
       P(r"D'un sol pas: \(\text{" + MCD + r"}(75,100)=25\), i \(\frac{75:25}{100:25}=\frac{3}{4}\).", r"De un solo paso: \(\text{" + MCD + r"}(75,100)=25\), y \(\frac{75:25}{100:25}=\frac{3}{4}\).", r"In one step: \(\text{" + MCD + r"}(75,100)=25\), and \(\frac{75:25}{100:25}=\frac{3}{4}\).")))
s4 += level(2, 3,
  prob(L(r"Calcula la fracció irreductible de \(\frac{705}{120}\).", r"Calcula la fracción irreducible de \(\frac{705}{120}\).", r"Find the simplest form of \(\frac{705}{120}\)."),
       r'\[705=3\cdot5\cdot47\qquad 120=2^3\cdot3\cdot5\qquad \text{' + MCD + r'}=3\cdot5=15\]',
       r'\[\frac{705}{120}=\frac{705:15}{120:15}=\boxed{\frac{47}{8}}\]'))
s4 += level(3, 4,
  prob(L(r"Troba una fracció equivalent a \(\frac{15}{24}\) que tinga denominador 16, i una d'equivalent a \(\frac{5}{8}\) que tinga numerador 80.", r"Encuentra una fracción equivalente a \(\frac{15}{24}\) que tenga denominador 16, y una equivalente a \(\frac{5}{8}\) que tenga numerador 80.", r"Find a fraction equivalent to \(\frac{15}{24}\) with denominator 16, and one equivalent to \(\frac{5}{8}\) with numerator 80."),
       P(r"16 no és múltiple de 24: primer simplifiquem i després amplifiquem.", r"16 no es múltiplo de 24: primero simplificamos y después amplificamos.", r"16 isn't a multiple of 24: simplify first, then scale up.") + r'\[\frac{15}{24}=\frac{5}{8}=\frac{5\cdot2}{8\cdot2}=\boxed{\frac{10}{16}}\]',
       P(r"Per a passar de 5 a 80 multipliquem per \(80:5=16\):", r"Para pasar de 5 a 80 multiplicamos por \(80:5=16\):", r"To go from 5 to 80 multiply by \(80:5=16\):") + r'\[\frac{5}{8}=\frac{5\cdot16}{8\cdot16}=\boxed{\frac{80}{128}}\]'))
s4 += practice([
  ('★', L(r"a) Escriu tres fraccions equivalents a \(\frac{3}{7}\). b) Simplifica \(\frac{4}{16}\).", r"a) Escribe tres fracciones equivalentes a \(\frac{3}{7}\). b) Simplifica \(\frac{4}{16}\).", r"a) Write three fractions equivalent to \(\frac{3}{7}\). b) Simplify \(\frac{4}{16}\).")),
  ('★★', L(r"c) Fracció irreductible de \(\frac{54}{24}\). d) Fracció irreductible de \(\frac{170}{105}\).", r"c) Fracción irreducible de \(\frac{54}{24}\). d) Fracción irreducible de \(\frac{170}{105}\).", r"c) Simplest form of \(\frac{54}{24}\). d) Simplest form of \(\frac{170}{105}\).")),
  ('★★★', L(r"e) Una fracció equivalent a \(\frac{3}{4}\) amb denominador 28. f) Una fracció equivalent a \(\frac{12}{18}\) amb numerador 10.", r"e) Una fracción equivalente a \(\frac{3}{4}\) con denominador 28. f) Una fracción equivalente a \(\frac{12}{18}\) con numerador 10.", r"e) A fraction equivalent to \(\frac{3}{4}\) with denominator 28. f) A fraction equivalent to \(\frac{12}{18}\) with numerator 10."))],
  P(r"a) Per exemple \(\frac{6}{14},\ \frac{9}{21},\ \frac{12}{28}\). &nbsp; b) \(\frac{1}{4}\).", r"a) Por ejemplo \(\frac{6}{14},\ \frac{9}{21},\ \frac{12}{28}\). &nbsp; b) \(\frac{1}{4}\).", r"a) For example \(\frac{6}{14},\ \frac{9}{21},\ \frac{12}{28}\). &nbsp; b) \(\frac{1}{4}\).")
  + P(r"c) \(\text{" + MCD + r"}=6\): \(\frac{9}{4}\). &nbsp; d) \(\text{" + MCD + r"}=5\): \(\frac{34}{21}\).", r"c) \(\text{" + MCD + r"}=6\): \(\frac{9}{4}\). &nbsp; d) \(\text{" + MCD + r"}=5\): \(\frac{34}{21}\).", r"c) \(\text{" + MCD + r"}=6\): \(\frac{9}{4}\). &nbsp; d) \(\text{" + MCD + r"}=5\): \(\frac{34}{21}\).")
  + P(r"e) \(\frac{21}{28}\). &nbsp; f) \(\frac{12}{18}=\frac{2}{3}=\frac{10}{15}\).", r"e) \(\frac{21}{28}\). &nbsp; f) \(\frac{12}{18}=\frac{2}{3}=\frac{10}{15}\).", r"e) \(\frac{21}{28}\). &nbsp; f) \(\frac{12}{18}=\frac{2}{3}=\frac{10}{15}\)."))

# ============================================================ 4.5
s5 = box('def', L('Són equivalents? Productes creuats', '¿Son equivalentes? Productos cruzados', 'Are they equivalent? Cross products'),
  P(r"Dues fraccions són equivalents si i només si els seus <strong>productes creuats</strong> són iguals:",
    r"Dos fracciones son equivalentes si y solo si sus <strong>productos cruzados</strong> son iguales:",
    r"Two fractions are equivalent if and only if their <strong>cross products</strong> are equal:")
  + r'\[\frac{a}{b}=\frac{c}{d}\quad\Longleftrightarrow\quad a\cdot d=b\cdot c\]'
  + r'\[\frac{8}{32}\ \text{i}\ \frac{3}{12}:\quad 8\cdot12=96,\quad 32\cdot3=96\ \Rightarrow\ \tri{sí que són equivalents}{sí son equivalentes}{they are equivalent}\]'
  + r'\[\frac{6}{15}\ \text{i}\ \frac{26}{34}:\quad 6\cdot34=204,\quad 15\cdot26=390\ \Rightarrow\ \tri{no són equivalents}{no son equivalentes}{not equivalent}\]'
  + P(r"Un altre mètode: simplificar-les totes dues fins a la irreductible. Si dona la mateixa, són equivalents: \(\frac{8}{32}=\frac{1}{4}\) i \(\frac{3}{12}=\frac{1}{4}\).",
      r"Otro método: simplificar las dos hasta la irreducible. Si sale la misma, son equivalentes: \(\frac{8}{32}=\frac{1}{4}\) y \(\frac{3}{12}=\frac{1}{4}\).",
      r"Another method: simplify both to their simplest form. If you get the same one, they're equivalent: \(\frac{8}{32}=\frac{1}{4}\) and \(\frac{3}{12}=\frac{1}{4}\)."))
s5 += box('prop', L('Calcular un terme desconegut', 'Calcular un término desconocido', 'Finding a missing term'),
  P(r"Si dues fraccions han de ser equivalents i en falta un nombre, igualem els productes creuats:", r"Si dos fracciones tienen que ser equivalentes y falta un número, igualamos los productos cruzados:", r"If two fractions must be equivalent and one number is missing, set the cross products equal:")
  + r'\[\frac{3}{14}=\frac{x}{42}\ \Rightarrow\ 14\cdot x=3\cdot42=126\ \Rightarrow\ x=126:14=\boxed{9}\]'
  + note(r"Moltes vegades es veu de cap: \(42=14\cdot3\), així que el numerador també es multiplica per 3: \(x=3\cdot3=9\).",
         r"Muchas veces se ve de cabeza: \(42=14\cdot3\), así que el numerador también se multiplica por 3: \(x=3\cdot3=9\).",
         r"Often you can see it in your head: \(42=14\cdot3\), so the numerator is also multiplied by 3: \(x=3\cdot3=9\).")
  + f'''<div class="widget" id="w-check">
  <div class="wt">✖️ {L("Productes creuats", "Productos cruzados", "Cross products")}</div>
  <div class="wrow">{fin("a", "b", "8", "32", "text")}<span class="op">≟</span>{fin("c", "d", "3", "12", "text")}</div>
  {quick([("8,32,3,12", "8/32 · 3/12"), ("6,15,26,34", "6/15 · 26/34"), ("7,23,14,46", "7/23 · 14/46"), ("68,52,17,13", "68/52 · 17/13"), ("3,14,x,42", "3/14 = x/42"), ("6,8,24,x", "6/8 = 24/x")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('x', 'Entrena: calcula la x', 'Entrena: calcula la x', 'Train: find x'))
s5 += level(1, 1,
  prob(L(r"Comprova si són equivalents \(\frac{7}{23}\) i \(\frac{14}{46}\).", r"Comprueba si son equivalentes \(\frac{7}{23}\) y \(\frac{14}{46}\).", r"Check whether \(\frac{7}{23}\) and \(\frac{14}{46}\) are equivalent."),
       r'\[7\cdot46=322\qquad 23\cdot14=322\]', P(r"Els productes creuats són iguals: <strong>sí</strong> que són equivalents.", r"Los productos cruzados son iguales: <strong>sí</strong> son equivalentes.", r"The cross products are equal: <strong>yes</strong>, they're equivalent.")))
s5 += level(2, 2,
  prob(L(r"Calcula \(x\): \(\ \frac{6}{8}=\frac{24}{x}\)", r"Calcula \(x\): \(\ \frac{6}{8}=\frac{24}{x}\)", r"Find \(x\): \(\ \frac{6}{8}=\frac{24}{x}\)"),
       r'\[6\cdot x=8\cdot24=192\ \Rightarrow\ x=192:6=\boxed{32}\]', P(r"Comprovació: \(24=6\cdot4\) i \(32=8\cdot4\).", r"Comprobación: \(24=6\cdot4\) y \(32=8\cdot4\).", r"Check: \(24=6\cdot4\) and \(32=8\cdot4\).")),
  prob(L(r"Són equivalents \(\frac{68}{52}\) i \(\frac{17}{13}\)?", r"¿Son equivalentes \(\frac{68}{52}\) y \(\frac{17}{13}\)?", r"Are \(\frac{68}{52}\) and \(\frac{17}{13}\) equivalent?"),
       r'\[68\cdot13=884\qquad 52\cdot17=884\ \Rightarrow\ \tri{sí}{sí}{yes}\]', P(r"També: \(\frac{68}{52}=\frac{68:4}{52:4}=\frac{17}{13}\).", r"También: \(\frac{68}{52}=\frac{68:4}{52:4}=\frac{17}{13}\).", r"Also: \(\frac{68}{52}=\frac{68:4}{52:4}=\frac{17}{13}\).")))
s5 += level(3, 4,
  prob(L(r"Troba \(x\) i \(y\) perquè \(\ \frac{4}{6}=\frac{x}{15}=\frac{20}{y}\).", r"Encuentra \(x\) e \(y\) para que \(\ \frac{4}{6}=\frac{x}{15}=\frac{20}{y}\).", r"Find \(x\) and \(y\) so that \(\ \frac{4}{6}=\frac{x}{15}=\frac{20}{y}\)."),
       P(r"Simplifiquem primer: \(\frac{4}{6}=\frac{2}{3}\). Com que \(15=3\cdot5\) i \(20=2\cdot10\):", r"Simplificamos primero: \(\frac{4}{6}=\frac{2}{3}\). Como \(15=3\cdot5\) y \(20=2\cdot10\):", r"Simplify first: \(\frac{4}{6}=\frac{2}{3}\). Since \(15=3\cdot5\) and \(20=2\cdot10\):"),
       r'\[x=2\cdot5=\boxed{10}\qquad y=3\cdot10=\boxed{30}\]'))
s5 += practice([
  ('★', L(r"Són equivalents? a) \(\frac{1}{2}\) i \(\frac{15}{30}\) &nbsp; b) \(\frac{3}{29}\) i \(\frac{33}{67}\)", r"¿Son equivalentes? a) \(\frac{1}{2}\) y \(\frac{15}{30}\) &nbsp; b) \(\frac{3}{29}\) y \(\frac{33}{67}\)", r"Are they equivalent? a) \(\frac{1}{2}\) and \(\frac{15}{30}\) &nbsp; b) \(\frac{3}{29}\) and \(\frac{33}{67}\)")),
  ('★★', L(r"Calcula \(x\): c) \(\frac{3}{14}=\frac{x}{42}\) &nbsp; d) \(\frac{x}{9}=\frac{20}{36}\)", r"Calcula \(x\): c) \(\frac{3}{14}=\frac{x}{42}\) &nbsp; d) \(\frac{x}{9}=\frac{20}{36}\)", r"Find \(x\): c) \(\frac{3}{14}=\frac{x}{42}\) &nbsp; d) \(\frac{x}{9}=\frac{20}{36}\)")),
  ('★★★', L(r"e) Són equivalents \(\frac{12}{18}\), \(\frac{10}{15}\) i \(\frac{14}{21}\)? f) Troba una fracció equivalent a \(\frac{3}{5}\) en què el numerador i el denominador sumen 40.", r"e) ¿Son equivalentes \(\frac{12}{18}\), \(\frac{10}{15}\) y \(\frac{14}{21}\)? f) Encuentra una fracción equivalente a \(\frac{3}{5}\) en la que el numerador y el denominador sumen 40.", r"e) Are \(\frac{12}{18}\), \(\frac{10}{15}\) and \(\frac{14}{21}\) equivalent? f) Find a fraction equivalent to \(\frac{3}{5}\) whose numerator and denominator add up to 40."))],
  P(r"a) \(1\cdot30=2\cdot15=30\): sí. &nbsp; b) \(3\cdot67=201\), \(29\cdot33=957\): no.", r"a) \(1\cdot30=2\cdot15=30\): sí. &nbsp; b) \(3\cdot67=201\), \(29\cdot33=957\): no.", r"a) \(1\cdot30=2\cdot15=30\): yes. &nbsp; b) \(3\cdot67=201\), \(29\cdot33=957\): no.")
  + P(r"c) \(x=9\). &nbsp; d) \(36x=180\), \(x=5\).", r"c) \(x=9\). &nbsp; d) \(36x=180\), \(x=5\).", r"c) \(x=9\). &nbsp; d) \(36x=180\), \(x=5\).")
  + P(r"e) Sí: totes tres simplifiquen a \(\frac{2}{3}\). &nbsp; f) \(3+5=8\) i \(40=8\cdot5\): \(\frac{15}{25}\).", r"e) Sí: las tres simplifican a \(\frac{2}{3}\). &nbsp; f) \(3+5=8\) y \(40=8\cdot5\): \(\frac{15}{25}\).", r"e) Yes: all three simplify to \(\frac{2}{3}\). &nbsp; f) \(3+5=8\) and \(40=8\cdot5\): \(\frac{15}{25}\)."))

# ============================================================ 4.6
s6 = box('def', L('Reducció a comú denominador', 'Reducción a común denominador', 'Common denominators'),
  P(r"<strong>Reduir a comú denominador</strong> vol dir buscar fraccions equivalents a les donades que tinguen <strong>totes el mateix denominador</strong>. Ho fem amb el " + r"\(\text{" + MCM + r"}\)" + r":",
    r"<strong>Reducir a común denominador</strong> quiere decir buscar fracciones equivalentes a las dadas que tengan <strong>todas el mismo denominador</strong>. Lo hacemos con el " + r"\(\text{" + MCM + r"}\)" + r":",
    r"<strong>Finding a common denominator</strong> means writing equivalent fractions that <strong>all have the same denominator</strong>. We use the " + r"\(\text{" + MCM + r"}\)" + r":")
  + ol(L(r"Calculem el mcm dels denominadors: serà el <strong>nou denominador</strong>.", r"Calculamos el mcm de los denominadores: será el <strong>nuevo denominador</strong>.", r"Find the lcm of the denominators: it's the <strong>new denominator</strong>."),
       L(r"Per a cada fracció, <strong>dividim el mcm entre el seu denominador</strong> i multipliquem el numerador pel resultat.", r"Para cada fracción, <strong>dividimos el mcm entre su denominador</strong> y multiplicamos el numerador por el resultado.", r"For each fraction, <strong>divide the lcm by its denominator</strong> and multiply the numerator by the result."))
  + r'\[\frac{5}{6},\ \frac{3}{4},\ \frac{7}{10}\qquad \text{' + MCM + r'}(6,4,10)=60\]'
  + '<div class="tbl-wrap"><table class="data cdtab"><tbody>'
  + '<tr><th>' + L('Fracció', 'Fracción', 'Fraction') + r'</th><td>\(\frac{5}{6}\)</td><td>\(\frac{3}{4}\)</td><td>\(\frac{7}{10}\)</td></tr>'
  + '<tr><th>' + L('mcm : denominador', 'mcm : denominador', 'lcm : denominator') + r'</th><td>\(60:6=10\)</td><td>\(60:4=15\)</td><td>\(60:10=6\)</td></tr>'
  + '<tr><th>' + L('Equivalent', 'Equivalente', 'Equivalent') + r'</th><td>\(\frac{5\cdot10}{60}=\frac{50}{60}\)</td><td>\(\frac{3\cdot15}{60}=\frac{45}{60}\)</td><td>\(\frac{7\cdot6}{60}=\frac{42}{60}\)</td></tr></tbody></table></div>'
  + note(r"També podríem usar el producte dels denominadors (\(6\cdot4\cdot10=240\)), però amb el mcm els nombres són més xicotets. Un nombre natural té denominador 1: \(5=\frac{5}{1}\).",
         r"También podríamos usar el producto de los denominadores (\(6\cdot4\cdot10=240\)), pero con el mcm los números son más pequeños. Un número natural tiene denominador 1: \(5=\frac{5}{1}\).",
         r"We could also use the product of the denominators (\(6\cdot4\cdot10=240\)), but with the lcm the numbers stay smaller. A whole number has denominator 1: \(5=\frac{5}{1}\).")
  + f'''<div class="widget" id="w-cd">
  <div class="wt">🧩 {L("Reductor a comú denominador", "Reductor a común denominador", "Common denominator tool")}</div>
  <div class="wrow"><label>{L("Fraccions", "Fracciones", "Fractions")} <input class="tin w" type="text" value="5/6, 3/4, 7/10" autocomplete="off" spellcheck="false" aria-label="fraccions"></label></div>
  {quick([("1/5, 3/7", "1/5, 3/7"), ("2/9, 1/6", "2/9, 1/6"), ("7/24, 3/16", "7/24, 3/16"), ("1/2, 2/3, 5/8", "1/2, 2/3, 5/8"), ("3/7, 5", "3/7, 5"), ("5/3, 5/12, 3/4, 9/20", "5/3, 5/12, 3/4, 9/20")])}
  <div class="info" aria-live="polite"></div>
  <div class="fvis"></div>
</div>
''')
s6 += level(1, 1,
  prob(L(r"Redueix a comú denominador: \(\ \frac{2}{9}\) i \(\frac{1}{6}\).", r"Reduce a común denominador: \(\ \frac{2}{9}\) y \(\frac{1}{6}\).", r"Give a common denominator: \(\ \frac{2}{9}\) and \(\frac{1}{6}\)."),
       r'\[\text{' + MCM + r'}(9,6)=18\qquad 18:9=2,\quad 18:6=3\]', r'\[\frac{2}{9}=\frac{2\cdot2}{18}=\boxed{\frac{4}{18}}\qquad \frac{1}{6}=\frac{1\cdot3}{18}=\boxed{\frac{3}{18}}\]'))
s6 += level(2, 2,
  prob(L(r"Redueix a comú denominador: \(\ \frac{7}{24}\) i \(\frac{3}{16}\).", r"Reduce a común denominador: \(\ \frac{7}{24}\) y \(\frac{3}{16}\).", r"Give a common denominator: \(\ \frac{7}{24}\) and \(\frac{3}{16}\)."),
       r'\[24=2^3\cdot3\qquad 16=2^4\qquad \text{' + MCM + r'}=2^4\cdot3=48\]', r'\[\frac{7}{24}=\frac{7\cdot2}{48}=\boxed{\frac{14}{48}}\qquad \frac{3}{16}=\frac{3\cdot3}{48}=\boxed{\frac{9}{48}}\]'))
s6 += level(3, 3,
  prob(L(r"Redueix a comú denominador: \(\ \frac{5}{3},\ \frac{5}{12},\ \frac{3}{4},\ \frac{9}{20}\).", r"Reduce a común denominador: \(\ \frac{5}{3},\ \frac{5}{12},\ \frac{3}{4},\ \frac{9}{20}\).", r"Give a common denominator: \(\ \frac{5}{3},\ \frac{5}{12},\ \frac{3}{4},\ \frac{9}{20}\)."),
       r'\[\text{' + MCM + r'}(3,12,4,20)=2^2\cdot3\cdot5=60\]', P(r"Dividim 60 entre cada denominador: \(20,\ 5,\ 15,\ 3\).", r"Dividimos 60 entre cada denominador: \(20,\ 5,\ 15,\ 3\).", r"Divide 60 by each denominator: \(20,\ 5,\ 15,\ 3\)."),
       r'\[\boxed{\frac{100}{60},\ \frac{25}{60},\ \frac{45}{60},\ \frac{27}{60}}\]'))
s6 += practice([
  ('★', L(r"a) \(\frac{1}{5},\ \frac{3}{7}\) &nbsp; b) \(\frac{3}{4},\ \frac{3}{8}\)", r"a) \(\frac{1}{5},\ \frac{3}{7}\) &nbsp; b) \(\frac{3}{4},\ \frac{3}{8}\)", r"a) \(\frac{1}{5},\ \frac{3}{7}\) &nbsp; b) \(\frac{3}{4},\ \frac{3}{8}\)")),
  ('★★', L(r"c) \(\frac{3}{7}\) i \(5\) &nbsp; d) \(\frac{1}{2},\ \frac{2}{3},\ \frac{5}{8}\)", r"c) \(\frac{3}{7}\) y \(5\) &nbsp; d) \(\frac{1}{2},\ \frac{2}{3},\ \frac{5}{8}\)", r"c) \(\frac{3}{7}\) and \(5\) &nbsp; d) \(\frac{1}{2},\ \frac{2}{3},\ \frac{5}{8}\)")),
  ('★★★', L(r"e) \(\frac{3}{18},\ \frac{4}{30},\ \frac{7}{36}\) &nbsp; f) \(\frac{6}{7},\ \frac{2}{14},\ \frac{12}{28}\)", r"e) \(\frac{3}{18},\ \frac{4}{30},\ \frac{7}{36}\) &nbsp; f) \(\frac{6}{7},\ \frac{2}{14},\ \frac{12}{28}\)", r"e) \(\frac{3}{18},\ \frac{4}{30},\ \frac{7}{36}\) &nbsp; f) \(\frac{6}{7},\ \frac{2}{14},\ \frac{12}{28}\)"))],
  P(r"a) \(\frac{7}{35},\ \frac{15}{35}\). &nbsp; b) \(\frac{6}{8},\ \frac{3}{8}\).", r"a) \(\frac{7}{35},\ \frac{15}{35}\). &nbsp; b) \(\frac{6}{8},\ \frac{3}{8}\).", r"a) \(\frac{7}{35},\ \frac{15}{35}\). &nbsp; b) \(\frac{6}{8},\ \frac{3}{8}\).")
  + P(r"c) \(\frac{3}{7},\ \frac{35}{7}\). &nbsp; d) \(\frac{12}{24},\ \frac{16}{24},\ \frac{15}{24}\).", r"c) \(\frac{3}{7},\ \frac{35}{7}\). &nbsp; d) \(\frac{12}{24},\ \frac{16}{24},\ \frac{15}{24}\).", r"c) \(\frac{3}{7},\ \frac{35}{7}\). &nbsp; d) \(\frac{12}{24},\ \frac{16}{24},\ \frac{15}{24}\).")
  + P(r"e) mcm 180: \(\frac{30}{180},\ \frac{24}{180},\ \frac{35}{180}\). &nbsp; f) mcm 28: \(\frac{24}{28},\ \frac{4}{28},\ \frac{12}{28}\) (si simplifiques abans, n'hi ha prou amb 7: \(\frac{6}{7},\ \frac{1}{7},\ \frac{3}{7}\)).", r"e) mcm 180: \(\frac{30}{180},\ \frac{24}{180},\ \frac{35}{180}\). &nbsp; f) mcm 28: \(\frac{24}{28},\ \frac{4}{28},\ \frac{12}{28}\) (si simplificas antes, basta con 7: \(\frac{6}{7},\ \frac{1}{7},\ \frac{3}{7}\)).", r"e) lcm 180: \(\frac{30}{180},\ \frac{24}{180},\ \frac{35}{180}\). &nbsp; f) lcm 28: \(\frac{24}{28},\ \frac{4}{28},\ \frac{12}{28}\) (if you simplify first, 7 is enough: \(\frac{6}{7},\ \frac{1}{7},\ \frac{3}{7}\))."))

# ============================================================ 4.7
s7 = box('prop', L('Com comparem fraccions', 'Cómo comparamos fracciones', 'How to compare fractions'),
  ul(L(r"<strong>Mateix denominador:</strong> és més gran la que té el <strong>numerador més gran</strong>: \(\ \frac{3}{7}<\frac{5}{7}\).", r"<strong>Mismo denominador:</strong> es mayor la que tiene el <strong>numerador mayor</strong>: \(\ \frac{3}{7}<\frac{5}{7}\).", r"<strong>Same denominator:</strong> the one with the <strong>bigger numerator</strong> is bigger: \(\ \frac{3}{7}<\frac{5}{7}\)."),
     L(r"<strong>Mateix numerador:</strong> és més gran la que té el <strong>denominador més xicotet</strong> (les parts són més grans): \(\ \frac{3}{4}>\frac{3}{7}\).", r"<strong>Mismo numerador:</strong> es mayor la que tiene el <strong>denominador más pequeño</strong> (las partes son más grandes): \(\ \frac{3}{4}>\frac{3}{7}\).", r"<strong>Same numerator:</strong> the one with the <strong>smaller denominator</strong> is bigger (its parts are bigger): \(\ \frac{3}{4}>\frac{3}{7}\)."),
     L(r"<strong>Numeradors i denominadors diferents:</strong> les reduïm a <strong>comú denominador</strong> i comparem els numeradors: \(\ \frac{2}{5}\ ?\ \frac{5}{6}\to\frac{12}{30}<\frac{25}{30}\), així que \(\frac{2}{5}<\frac{5}{6}\).", r"<strong>Numeradores y denominadores distintos:</strong> las reducimos a <strong>común denominador</strong> y comparamos los numeradores: \(\ \frac{2}{5}\ ?\ \frac{5}{6}\to\frac{12}{30}<\frac{25}{30}\), así que \(\frac{2}{5}<\frac{5}{6}\).", r"<strong>Different numerators and denominators:</strong> give them a <strong>common denominator</strong> and compare numerators: \(\ \frac{2}{5}\ ?\ \frac{5}{6}\to\frac{12}{30}<\frac{25}{30}\), so \(\frac{2}{5}<\frac{5}{6}\)."))
  + brows((r'\frac{3}{4}', svg_bar(4, 3, 360, 26)), (r'\frac{3}{7}', svg_bar(7, 3, 360, 26, 'fr-on2')))
  + note(r"Truc: compara amb la unitat. \(\frac{8}{9}\) és menor que 1 i \(\frac{11}{9}\) és major, així que \(\frac{8}{9}<\frac{11}{9}\) sense fer cap càlcul. Amb dues fraccions també serveixen els productes creuats: \(\frac{2}{5}<\frac{5}{6}\) perquè \(2\cdot6<5\cdot5\).",
         r"Truco: compara con la unidad. \(\frac{8}{9}\) es menor que 1 y \(\frac{11}{9}\) es mayor, así que \(\frac{8}{9}<\frac{11}{9}\) sin hacer ningún cálculo. Con dos fracciones también sirven los productos cruzados: \(\frac{2}{5}<\frac{5}{6}\) porque \(2\cdot6<5\cdot5\).",
         r"Tip: compare with 1. \(\frac{8}{9}\) is less than 1 and \(\frac{11}{9}\) is more, so \(\frac{8}{9}<\frac{11}{9}\) without any working. With two fractions you can also cross-multiply: \(\frac{2}{5}<\frac{5}{6}\) because \(2\cdot6<5\cdot5\)."))
s7 += box('def', L('Ordenar fraccions', 'Ordenar fracciones', 'Ordering fractions'),
  P(r"Per a ordenar diverses fraccions, les reduïm a comú denominador i les ordenem pel numerador:", r"Para ordenar varias fracciones, las reducimos a común denominador y las ordenamos por el numerador:", r"To order several fractions, give them a common denominator and order them by numerator:")
  + r'\[\frac{3}{5},\ \frac{2}{7},\ \frac{11}{2}\ \xrightarrow{\ \text{' + MCM + r'}=70\ }\ \frac{42}{70},\ \frac{20}{70},\ \frac{385}{70}\qquad\Rightarrow\qquad \frac{2}{7}<\frac{3}{5}<\frac{11}{2}\]'
  + f'''<div class="widget" id="w-cmp">
  <div class="wt">📏 {L("Ordena fraccions en la recta", "Ordena fracciones en la recta", "Order fractions on the number line")}</div>
  <div class="wrow"><label>{L("Fraccions", "Fracciones", "Fractions")} <input class="tin w" type="text" value="4/5, 2/8, 3/10, 7/20" autocomplete="off" spellcheck="false" aria-label="fraccions"></label></div>
  {quick([("3/4, 3/7", "3/4, 3/7"), ("2/5, 5/6", "2/5, 5/6"), ("8/9, 11/12", "8/9, 11/12"), ("4/9, 5/6, 2/3", "4/9, 5/6, 2/3"), ("4/5, 2/8, 3/10, 7/20", "4/5, 2/8, 3/10, 7/20"), ("5/2, 2/3, 4/7, 5/4", "5/2, 2/3, 4/7, 5/4")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('cmp', 'Entrena: compara', 'Entrena: compara', 'Train: compare'))
s7 += level(1, 1,
  prob(L(r"Compara: a) \(\frac{6}{11}\ \square\ \frac{10}{11}\) &nbsp; b) \(\frac{3}{7}\ \square\ \frac{3}{4}\)", r"Compara: a) \(\frac{6}{11}\ \square\ \frac{10}{11}\) &nbsp; b) \(\frac{3}{7}\ \square\ \frac{3}{4}\)", r"Compare: a) \(\frac{6}{11}\ \square\ \frac{10}{11}\) &nbsp; b) \(\frac{3}{7}\ \square\ \frac{3}{4}\)"),
       P(r"a) Mateix denominador: \(6<10\), així que \(\frac{6}{11}<\frac{10}{11}\).", r"a) Mismo denominador: \(6<10\), así que \(\frac{6}{11}<\frac{10}{11}\).", r"a) Same denominator: \(6<10\), so \(\frac{6}{11}<\frac{10}{11}\)."),
       P(r"b) Mateix numerador: els setens són més xicotets que els quarts, així que \(\frac{3}{7}<\frac{3}{4}\).", r"b) Mismo numerador: los séptimos son más pequeños que los cuartos, así que \(\frac{3}{7}<\frac{3}{4}\).", r"b) Same numerator: sevenths are smaller than quarters, so \(\frac{3}{7}<\frac{3}{4}\).")))
s7 += level(2, 2,
  prob(L(r"Compara \(\frac{8}{9}\) i \(\frac{11}{12}\).", r"Compara \(\frac{8}{9}\) y \(\frac{11}{12}\).", r"Compare \(\frac{8}{9}\) and \(\frac{11}{12}\)."),
       r'\[\text{' + MCM + r'}(9,12)=36\qquad \frac{8}{9}=\frac{32}{36}\qquad \frac{11}{12}=\frac{33}{36}\]', r'\[32<33\ \Rightarrow\ \boxed{\frac{8}{9}<\frac{11}{12}}\]'))
s7 += level(3, 3,
  prob(L(r"Ordena de menor a major: \(\ \frac{4}{5},\ \frac{2}{8},\ \frac{3}{10},\ \frac{7}{20}\).", r"Ordena de menor a mayor: \(\ \frac{4}{5},\ \frac{2}{8},\ \frac{3}{10},\ \frac{7}{20}\).", r"Order from smallest to largest: \(\ \frac{4}{5},\ \frac{2}{8},\ \frac{3}{10},\ \frac{7}{20}\)."),
       P(r"Primer simplifiquem \(\frac{2}{8}=\frac{1}{4}\). Després, \(\text{" + MCM + r"}(5,4,10,20)=20\):", r"Primero simplificamos \(\frac{2}{8}=\frac{1}{4}\). Después, \(\text{" + MCM + r"}(5,4,10,20)=20\):", r"First simplify \(\frac{2}{8}=\frac{1}{4}\). Then \(\text{" + MCM + r"}(5,4,10,20)=20\):"),
       r'\[\frac{16}{20},\quad \frac{5}{20},\quad \frac{6}{20},\quad \frac{7}{20}\]',
       r'\[\boxed{\frac{2}{8}<\frac{3}{10}<\frac{7}{20}<\frac{4}{5}}\]'))
s7 += practice([
  ('★', L(r"Compara: a) \(\frac{9}{5}\ \square\ \frac{9}{8}\) &nbsp; b) \(\frac{4}{8}\ \square\ \frac{2}{16}\)", r"Compara: a) \(\frac{9}{5}\ \square\ \frac{9}{8}\) &nbsp; b) \(\frac{4}{8}\ \square\ \frac{2}{16}\)", r"Compare: a) \(\frac{9}{5}\ \square\ \frac{9}{8}\) &nbsp; b) \(\frac{4}{8}\ \square\ \frac{2}{16}\)")),
  ('★★', L(r"Compara: c) \(\frac{1}{3}\ \square\ \frac{3}{7}\) &nbsp; d) \(\frac{3}{4}\ \square\ \frac{24}{32}\)", r"Compara: c) \(\frac{1}{3}\ \square\ \frac{3}{7}\) &nbsp; d) \(\frac{3}{4}\ \square\ \frac{24}{32}\)", r"Compare: c) \(\frac{1}{3}\ \square\ \frac{3}{7}\) &nbsp; d) \(\frac{3}{4}\ \square\ \frac{24}{32}\)")),
  ('★★★', L(r"e) Ordena de menor a major: \(\frac{4}{9},\ \frac{5}{6},\ \frac{2}{3}\). f) Escriu una fracció compresa entre \(\frac{1}{3}\) i \(\frac{1}{2}\).", r"e) Ordena de menor a mayor: \(\frac{4}{9},\ \frac{5}{6},\ \frac{2}{3}\). f) Escribe una fracción comprendida entre \(\frac{1}{3}\) y \(\frac{1}{2}\).", r"e) Order from smallest to largest: \(\frac{4}{9},\ \frac{5}{6},\ \frac{2}{3}\). f) Write a fraction between \(\frac{1}{3}\) and \(\frac{1}{2}\)."))],
  P(r"a) \(>\) (mateix numerador). &nbsp; b) \(\frac{8}{16}>\frac{2}{16}\): \(>\).", r"a) \(>\) (mismo numerador). &nbsp; b) \(\frac{8}{16}>\frac{2}{16}\): \(>\).", r"a) \(>\) (same numerator). &nbsp; b) \(\frac{8}{16}>\frac{2}{16}\): \(>\).")
  + P(r"c) \(\frac{7}{21}<\frac{9}{21}\): \(<\). &nbsp; d) \(\frac{24}{32}=\frac{3}{4}\): \(=\).", r"c) \(\frac{7}{21}<\frac{9}{21}\): \(<\). &nbsp; d) \(\frac{24}{32}=\frac{3}{4}\): \(=\).", r"c) \(\frac{7}{21}<\frac{9}{21}\): \(<\). &nbsp; d) \(\frac{24}{32}=\frac{3}{4}\): \(=\).")
  + P(r"e) \(\frac{8}{18}<\frac{12}{18}<\frac{15}{18}\): \(\frac{4}{9}<\frac{2}{3}<\frac{5}{6}\). &nbsp; f) \(\frac{1}{3}=\frac{4}{12}\) i \(\frac{1}{2}=\frac{6}{12}\): per exemple \(\frac{5}{12}\).", r"e) \(\frac{8}{18}<\frac{12}{18}<\frac{15}{18}\): \(\frac{4}{9}<\frac{2}{3}<\frac{5}{6}\). &nbsp; f) \(\frac{1}{3}=\frac{4}{12}\) y \(\frac{1}{2}=\frac{6}{12}\): por ejemplo \(\frac{5}{12}\).", r"e) \(\frac{8}{18}<\frac{12}{18}<\frac{15}{18}\): \(\frac{4}{9}<\frac{2}{3}<\frac{5}{6}\). &nbsp; f) \(\frac{1}{3}=\frac{4}{12}\) and \(\frac{1}{2}=\frac{6}{12}\): for example \(\frac{5}{12}\)."))

# ============================================================ 4.8
def ops(ops_, on, a, b, c, d, presets, title):
    return f'''<div class="widget w-ops">
  <div class="wt">🧮 {title}</div>
  <div class="wrow">{seg(ops_, on)}</div>
  <div class="wrow" style="margin-top:8px">{fin("a", "b", a, b)}<span class="op opv">{on}</span>{fin("c", "d", c, d)}</div>
  {quick(presets)}
  <div class="info" aria-live="polite"></div>
  <div class="fvis"></div>
</div>
'''
s8 = box('def', L('Suma i resta de fraccions', 'Suma y resta de fracciones', 'Adding and subtracting fractions'),
  ul(L(r"<strong>Amb el mateix denominador:</strong> sumem (o restem) els numeradors i deixem el mateix denominador: \(\ \frac{4}{7}+\frac{8}{7}=\frac{12}{7}\).", r"<strong>Con el mismo denominador:</strong> sumamos (o restamos) los numeradores y dejamos el mismo denominador: \(\ \frac{4}{7}+\frac{8}{7}=\frac{12}{7}\).", r"<strong>With the same denominator:</strong> add (or subtract) the numerators and keep the denominator: \(\ \frac{4}{7}+\frac{8}{7}=\frac{12}{7}\)."),
     L(r"<strong>Amb denominadors diferents:</strong> primer les <strong>reduïm a comú denominador</strong> i després sumem o restem els numeradors.", r"<strong>Con denominadores distintos:</strong> primero las <strong>reducimos a común denominador</strong> y después sumamos o restamos los numeradores.", r"<strong>With different denominators:</strong> first <strong>give them a common denominator</strong>, then add or subtract the numerators."))
  + r'\[\frac{2}{3}+\frac{1}{5}=\frac{10}{15}+\frac{3}{15}=\frac{13}{15}\qquad\qquad \frac{3}{4}+\frac{6}{8}=\frac{6}{8}+\frac{6}{8}=\frac{12}{8}=\boxed{\frac{3}{2}}\]'
  + brows((r'\frac{2}{3}', svg_bar(15, 10, 360, 24)), (r'\frac{1}{5}', svg_bar(15, 3, 360, 24, 'fr-on2')), (r'\frac{13}{15}', svg_bar(15, 13, 360, 24, 'fr-on3')))
  + P(r"Amb un nombre natural, el convertim en fracció amb el mateix denominador: \(\ 4+\frac{25}{9}=\frac{36}{9}+\frac{25}{9}=\frac{61}{9}\). I amb més de dues fraccions, igual:",
      r"Con un número natural, lo convertimos en fracción con el mismo denominador: \(\ 4+\frac{25}{9}=\frac{36}{9}+\frac{25}{9}=\frac{61}{9}\). Y con más de dos fracciones, igual:",
      r"With a whole number, turn it into a fraction with the same denominator: \(\ 4+\frac{25}{9}=\frac{36}{9}+\frac{25}{9}=\frac{61}{9}\). With more than two fractions, the same:")
  + r'\[\frac{4}{5}+\frac{2}{7}-\frac{1}{2}=\frac{56}{70}+\frac{20}{70}-\frac{35}{70}=\frac{41}{70}\]'
  + note(r"<strong>Error típic:</strong> mai sumem numeradors i denominadors per separat. \(\frac{1}{2}+\frac{1}{3}\neq\frac{2}{5}\): és \(\frac{3}{6}+\frac{2}{6}=\frac{5}{6}\).",
         r"<strong>Error típico:</strong> nunca sumamos numeradores y denominadores por separado. \(\frac{1}{2}+\frac{1}{3}\neq\frac{2}{5}\): es \(\frac{3}{6}+\frac{2}{6}=\frac{5}{6}\).",
         r"<strong>Common mistake:</strong> never add numerators and denominators separately. \(\frac{1}{2}+\frac{1}{3}\neq\frac{2}{5}\): it's \(\frac{3}{6}+\frac{2}{6}=\frac{5}{6}\).", '⚠️'))
s8 += ops([("+", "+"), ("-", "−")], "+", "2", "3", "1", "5", [("2,3,1,5", "2/3 + 1/5"), ("4,7,8,7", "4/7 + 8/7"), ("5,2,1,8", "5/2 − 1/8"), ("3,4,6,8", "3/4 + 6/8"), ("14,15,2,3", "14/15 − 2/3"), ("1,2,1,3", "1/2 + 1/3")],
          L("Suma i resta pas a pas", "Suma y resta paso a paso", "Adding and subtracting step by step"))
s8 += drill('sum', 'Entrena: sumes i restes', 'Entrena: sumas y restas', 'Train: adding and subtracting')
s8 += level(1, 1,
  prob(L(r"Calcula: \(\ \frac{5}{8}+\frac{1}{5}\)", r"Calcula: \(\ \frac{5}{8}+\frac{1}{5}\)", r"Work out: \(\ \frac{5}{8}+\frac{1}{5}\)"),
       r'\[\text{' + MCM + r'}(8,5)=40\]', r'\[\frac{5}{8}+\frac{1}{5}=\frac{25}{40}+\frac{8}{40}=\boxed{\frac{33}{40}}\]'),
  prob(L(r"Calcula: \(\ \frac{14}{15}-\frac{2}{3}\)", r"Calcula: \(\ \frac{14}{15}-\frac{2}{3}\)", r"Work out: \(\ \frac{14}{15}-\frac{2}{3}\)"),
       r'\[\frac{14}{15}-\frac{2}{3}=\frac{14}{15}-\frac{10}{15}=\boxed{\frac{4}{15}}\]'))
s8 += level(2, 3,
  prob(L(r"Calcula i simplifica: \(\ \frac{6}{8}+\frac{4}{3}-\frac{8}{12}\)", r"Calcula y simplifica: \(\ \frac{6}{8}+\frac{4}{3}-\frac{8}{12}\)", r"Work out and simplify: \(\ \frac{6}{8}+\frac{4}{3}-\frac{8}{12}\)"),
       r'\[\text{' + MCM + r'}(8,3,12)=24\]', r'\[\frac{18}{24}+\frac{32}{24}-\frac{16}{24}=\frac{34}{24}\]', r'\[\frac{34}{24}=\frac{34:2}{24:2}=\boxed{\frac{17}{12}}\]'))
s8 += level(3, 4,
  prob(L(r"Calcula: \(\ 4-\frac{1}{2}+\frac{1}{3}+2\)", r"Calcula: \(\ 4-\frac{1}{2}+\frac{1}{3}+2\)", r"Work out: \(\ 4-\frac{1}{2}+\frac{1}{3}+2\)"),
       P(r"Els nombres naturals tenen denominador 1. El mcm de \(1,\ 2,\ 3,\ 1\) és 6:", r"Los números naturales tienen denominador 1. El mcm de \(1,\ 2,\ 3,\ 1\) es 6:", r"Whole numbers have denominator 1. The lcm of \(1,\ 2,\ 3,\ 1\) is 6:"),
       r'\[\frac{24}{6}-\frac{3}{6}+\frac{2}{6}+\frac{12}{6}=\frac{24-3+2+12}{6}=\boxed{\frac{35}{6}}\]'))
s8 += practice([
  ('★', L(r"a) \(\frac{2}{9}+\frac{5}{9}\) &nbsp; b) \(\frac{2}{3}+\frac{1}{5}\)", r"a) \(\frac{2}{9}+\frac{5}{9}\) &nbsp; b) \(\frac{2}{3}+\frac{1}{5}\)", r"a) \(\frac{2}{9}+\frac{5}{9}\) &nbsp; b) \(\frac{2}{3}+\frac{1}{5}\)")),
  ('★★', L(r"c) \(\frac{5}{3}-\frac{9}{24}\) &nbsp; d) \(\frac{3}{5}+1\)", r"c) \(\frac{5}{3}-\frac{9}{24}\) &nbsp; d) \(\frac{3}{5}+1\)", r"c) \(\frac{5}{3}-\frac{9}{24}\) &nbsp; d) \(\frac{3}{5}+1\)")),
  ('★★★', L(r"e) \(\frac{2}{10}+\frac{5}{60}-\frac{1}{30}\) &nbsp; f) \(\frac{10}{3}-\frac{2}{6}-\frac{4}{5}+\frac{1}{2}\)", r"e) \(\frac{2}{10}+\frac{5}{60}-\frac{1}{30}\) &nbsp; f) \(\frac{10}{3}-\frac{2}{6}-\frac{4}{5}+\frac{1}{2}\)", r"e) \(\frac{2}{10}+\frac{5}{60}-\frac{1}{30}\) &nbsp; f) \(\frac{10}{3}-\frac{2}{6}-\frac{4}{5}+\frac{1}{2}\)"))],
  P(r"a) \(\frac{7}{9}\). &nbsp; b) \(\frac{10}{15}+\frac{3}{15}=\frac{13}{15}\).", r"a) \(\frac{7}{9}\). &nbsp; b) \(\frac{10}{15}+\frac{3}{15}=\frac{13}{15}\).", r"a) \(\frac{7}{9}\). &nbsp; b) \(\frac{10}{15}+\frac{3}{15}=\frac{13}{15}\).")
  + P(r"c) \(\frac{40}{24}-\frac{9}{24}=\frac{31}{24}\). &nbsp; d) \(\frac{3}{5}+\frac{5}{5}=\frac{8}{5}\).", r"c) \(\frac{40}{24}-\frac{9}{24}=\frac{31}{24}\). &nbsp; d) \(\frac{3}{5}+\frac{5}{5}=\frac{8}{5}\).", r"c) \(\frac{40}{24}-\frac{9}{24}=\frac{31}{24}\). &nbsp; d) \(\frac{3}{5}+\frac{5}{5}=\frac{8}{5}\).")
  + P(r"e) \(\frac{12}{60}+\frac{5}{60}-\frac{2}{60}=\frac{15}{60}=\frac{1}{4}\). &nbsp; f) \(\frac{100}{30}-\frac{10}{30}-\frac{24}{30}+\frac{15}{30}=\frac{81}{30}=\frac{27}{10}\).", r"e) \(\frac{12}{60}+\frac{5}{60}-\frac{2}{60}=\frac{15}{60}=\frac{1}{4}\). &nbsp; f) \(\frac{100}{30}-\frac{10}{30}-\frac{24}{30}+\frac{15}{30}=\frac{81}{30}=\frac{27}{10}\).", r"e) \(\frac{12}{60}+\frac{5}{60}-\frac{2}{60}=\frac{15}{60}=\frac{1}{4}\). &nbsp; f) \(\frac{100}{30}-\frac{10}{30}-\frac{24}{30}+\frac{15}{30}=\frac{81}{30}=\frac{27}{10}\)."))

# ============================================================ 4.9
s9 = box('def', L('Multiplicació de fraccions', 'Multiplicación de fracciones', 'Multiplying fractions'),
  P(r"Multipliquem els numeradors entre si i els denominadors entre si:", r"Multiplicamos los numeradores entre sí y los denominadores entre sí:", r"Multiply the numerators together and the denominators together:")
  + r'\[\frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}\qquad\qquad \frac{6}{4}\cdot\frac{2}{5}=\frac{12}{20}=\boxed{\frac{3}{5}}\]'
  + ul(L(r"Un nombre natural per una fracció: multipliquem només el numerador. \(\ 2\cdot\frac{5}{6}=\frac{10}{6}=\frac{5}{3}\).", r"Un número natural por una fracción: multiplicamos solo el numerador. \(\ 2\cdot\frac{5}{6}=\frac{10}{6}=\frac{5}{3}\).", r"A whole number times a fraction: multiply only the numerator. \(\ 2\cdot\frac{5}{6}=\frac{10}{6}=\frac{5}{3}\)."),
       L(r"La <strong>fracció d'una fracció</strong> és un producte: \(\ \frac{2}{3}\) de \(\frac{3}{5}\) és \(\frac{2}{3}\cdot\frac{3}{5}=\frac{6}{15}=\frac{2}{5}\).", r"La <strong>fracción de una fracción</strong> es un producto: \(\ \frac{2}{3}\) de \(\frac{3}{5}\) es \(\frac{2}{3}\cdot\frac{3}{5}=\frac{6}{15}=\frac{2}{5}\).", r"A <strong>fraction of a fraction</strong> is a product: \(\ \frac{2}{3}\) of \(\frac{3}{5}\) is \(\frac{2}{3}\cdot\frac{3}{5}=\frac{6}{15}=\frac{2}{5}\)."),
       L(r"Truc: abans de multiplicar, podem <strong>simplificar</strong> un numerador amb un denominador: \(\ \frac{6}{4}\cdot\frac{2}{5}=\frac{6\cdot2}{4\cdot5}=\frac{3\cdot\cancel{2}\cdot\cancel{2}}{\cancel{2}\cdot\cancel{2}\cdot5}=\frac{3}{5}\).", r"Truco: antes de multiplicar, podemos <strong>simplificar</strong> un numerador con un denominador: \(\ \frac{6}{4}\cdot\frac{2}{5}=\frac{6\cdot2}{4\cdot5}=\frac{3\cdot\cancel{2}\cdot\cancel{2}}{\cancel{2}\cdot\cancel{2}\cdot5}=\frac{3}{5}\).", r"Tip: before multiplying, you can <strong>cancel</strong> a numerator with a denominator: \(\ \frac{6}{4}\cdot\frac{2}{5}=\frac{6\cdot2}{4\cdot5}=\frac{3\cdot\cancel{2}\cdot\cancel{2}}{\cancel{2}\cdot\cancel{2}\cdot5}=\frac{3}{5}\).")))
s9 += box('prop', L('Fracció inversa', 'Fracción inversa', 'Reciprocal'),
  P(r"La <strong>inversa</strong> de \(\frac{a}{b}\) és \(\frac{b}{a}\): girem la fracció. Una fracció per la seua inversa sempre dona 1:", r"La <strong>inversa</strong> de \(\frac{a}{b}\) es \(\frac{b}{a}\): damos la vuelta a la fracción. Una fracción por su inversa siempre da 1:", r"The <strong>reciprocal</strong> of \(\frac{a}{b}\) is \(\frac{b}{a}\): flip the fraction. A fraction times its reciprocal is always 1:")
  + r'\[\frac{3}{2}\cdot\frac{2}{3}=\frac{6}{6}=1\qquad\qquad \tri{La inversa de}{La inversa de}{The reciprocal of}\ 5=\frac{5}{1}\ \tri{és}{es}{is}\ \frac{1}{5}\]'
  + note(r"El 0 no té inversa, perquè no podem dividir entre 0.", r"El 0 no tiene inversa, porque no podemos dividir entre 0.", r"0 has no reciprocal, because we can't divide by 0."))
s9 += box('def', L('Divisió de fraccions', 'División de fracciones', 'Dividing fractions'),
  P(r"Dividir entre una fracció és <strong>multiplicar per la seua inversa</strong>. En la pràctica, fem els <strong>productes creuats</strong>:", r"Dividir entre una fracción es <strong>multiplicar por su inversa</strong>. En la práctica, hacemos los <strong>productos cruzados</strong>:", r"Dividing by a fraction means <strong>multiplying by its reciprocal</strong>. In practice we <strong>cross-multiply</strong>:")
  + r'\[\frac{a}{b}:\frac{c}{d}=\frac{a}{b}\cdot\frac{d}{c}=\frac{a\cdot d}{b\cdot c}\qquad\qquad \frac{4}{3}:\frac{5}{6}=\frac{4\cdot6}{3\cdot5}=\frac{24}{15}=\boxed{\frac{8}{5}}\]'
  + note(r"Té sentit: \(3:\frac{1}{4}=12\), perquè en 3 pizzes caben 12 quarts de pizza.", r"Tiene sentido: \(3:\frac{1}{4}=12\), porque en 3 pizzas caben 12 cuartos de pizza.", r"It makes sense: \(3:\frac{1}{4}=12\), because 3 pizzas hold 12 quarter-pizzas.")
  + ops([("·", "·"), (":", ":")], "·", "2", "3", "3", "4", [("6,4,2,5", "6/4 · 2/5"), ("2,3,3,4", "2/3 · 3/4"), ("3,2,2,3", "3/2 · 2/3"), ("4,3,5,6", "4/3 : 5/6"), ("5,4,2,1", "5/4 : 2"), ("3,1,1,4", "3 : 1/4")],
        L("Multiplica i divideix pas a pas", "Multiplica y divide paso a paso", "Multiply and divide step by step"))
  + drill('mul', 'Entrena: multiplicacions i divisions', 'Entrena: multiplicaciones y divisiones', 'Train: multiplying and dividing'))
s9 += level(1, 1,
  prob(L(r"Calcula: \(\ \frac{3}{2}\cdot\frac{4}{7}\cdot3\)", r"Calcula: \(\ \frac{3}{2}\cdot\frac{4}{7}\cdot3\)", r"Work out: \(\ \frac{3}{2}\cdot\frac{4}{7}\cdot3\)"),
       r'\[\frac{3\cdot4\cdot3}{2\cdot7\cdot1}=\frac{36}{14}=\boxed{\frac{18}{7}}\]'),
  prob(L(r"Calcula: \(\ \frac{5}{4}:2\)", r"Calcula: \(\ \frac{5}{4}:2\)", r"Work out: \(\ \frac{5}{4}:2\)"),
       r'\[\frac{5}{4}:\frac{2}{1}=\frac{5\cdot1}{4\cdot2}=\boxed{\frac{5}{8}}\]', P(r"Dividir entre 2 és el mateix que calcular la meitat.", r"Dividir entre 2 es lo mismo que calcular la mitad.", r"Dividing by 2 is the same as taking half.")))
s9 += level(2, 3,
  prob(L(r"Calcula i simplifica: \(\ \frac{3}{4}\cdot\frac{10}{2}\cdot\frac{1}{6}\)", r"Calcula y simplifica: \(\ \frac{3}{4}\cdot\frac{10}{2}\cdot\frac{1}{6}\)", r"Work out and simplify: \(\ \frac{3}{4}\cdot\frac{10}{2}\cdot\frac{1}{6}\)"),
       r'\[\frac{3\cdot10\cdot1}{4\cdot2\cdot6}=\frac{30}{48}=\boxed{\frac{5}{8}}\]'),
  prob(L(r"Calcula: \(\ \frac{2}{6}:\frac{5}{4}:\frac{1}{3}\)", r"Calcula: \(\ \frac{2}{6}:\frac{5}{4}:\frac{1}{3}\)", r"Work out: \(\ \frac{2}{6}:\frac{5}{4}:\frac{1}{3}\)"),
       P(r"Divisions seguides: d'esquerra a dreta.", r"Divisiones seguidas: de izquierda a derecha.", r"Consecutive divisions: from left to right."),
       r'\[\frac{2}{6}:\frac{5}{4}=\frac{8}{30}=\frac{4}{15}\qquad \frac{4}{15}:\frac{1}{3}=\frac{12}{15}=\boxed{\frac{4}{5}}\]'))
s9 += level(3, 5,
  prob(L(r"Quina fracció cal multiplicar per \(\frac{3}{4}\) per a obtindre \(\frac{9}{10}\)?", r"¿Qué fracción hay que multiplicar por \(\frac{3}{4}\) para obtener \(\frac{9}{10}\)?", r"What fraction must we multiply by \(\frac{3}{4}\) to get \(\frac{9}{10}\)?"),
       P(r"La divisió és l'operació inversa de la multiplicació:", r"La división es la operación inversa de la multiplicación:", r"Division undoes multiplication:"),
       r'\[\frac{9}{10}:\frac{3}{4}=\frac{9\cdot4}{10\cdot3}=\frac{36}{30}=\boxed{\frac{6}{5}}\]', P(r"Comprovació: \(\frac{6}{5}\cdot\frac{3}{4}=\frac{18}{20}=\frac{9}{10}\).", r"Comprobación: \(\frac{6}{5}\cdot\frac{3}{4}=\frac{18}{20}=\frac{9}{10}\).", r"Check: \(\frac{6}{5}\cdot\frac{3}{4}=\frac{18}{20}=\frac{9}{10}\).")))
s9 += practice([
  ('★', L(r"a) \(\frac{6}{4}\cdot\frac{2}{5}\). b) Escriu la inversa de \(\frac{4}{13}\) i la de \(7\).", r"a) \(\frac{6}{4}\cdot\frac{2}{5}\). b) Escribe la inversa de \(\frac{4}{13}\) y la de \(7\).", r"a) \(\frac{6}{4}\cdot\frac{2}{5}\). b) Write the reciprocal of \(\frac{4}{13}\) and of \(7\).")),
  ('★★', L(r"c) \(\frac{4}{8}:\frac{6}{3}\) &nbsp; d) \(6:\frac{2}{3}:\frac{1}{5}\)", r"c) \(\frac{4}{8}:\frac{6}{3}\) &nbsp; d) \(6:\frac{2}{3}:\frac{1}{5}\)", r"c) \(\frac{4}{8}:\frac{6}{3}\) &nbsp; d) \(6:\frac{2}{3}:\frac{1}{5}\)")),
  ('★★★', L(r"e) \(\frac{5}{4}:\frac{1}{3}\cdot\frac{6}{5}\). f) Quantes ampolles de \(\frac{3}{4}\) de litre podem omplir amb 12 litres?", r"e) \(\frac{5}{4}:\frac{1}{3}\cdot\frac{6}{5}\). f) ¿Cuántas botellas de \(\frac{3}{4}\) de litro podemos llenar con 12 litros?", r"e) \(\frac{5}{4}:\frac{1}{3}\cdot\frac{6}{5}\). f) How many \(\frac{3}{4}\)-litre bottles can we fill with 12 litres?"))],
  P(r"a) \(\frac{12}{20}=\frac{3}{5}\). &nbsp; b) \(\frac{13}{4}\) i \(\frac{1}{7}\).", r"a) \(\frac{12}{20}=\frac{3}{5}\). &nbsp; b) \(\frac{13}{4}\) y \(\frac{1}{7}\).", r"a) \(\frac{12}{20}=\frac{3}{5}\). &nbsp; b) \(\frac{13}{4}\) and \(\frac{1}{7}\).")
  + P(r"c) \(\frac{12}{48}=\frac{1}{4}\). &nbsp; d) \(6:\frac{2}{3}=\frac{18}{2}=9\); \(9:\frac{1}{5}=45\).", r"c) \(\frac{12}{48}=\frac{1}{4}\). &nbsp; d) \(6:\frac{2}{3}=\frac{18}{2}=9\); \(9:\frac{1}{5}=45\).", r"c) \(\frac{12}{48}=\frac{1}{4}\). &nbsp; d) \(6:\frac{2}{3}=\frac{18}{2}=9\); \(9:\frac{1}{5}=45\).")
  + P(r"e) \(\frac{15}{4}\cdot\frac{6}{5}=\frac{90}{20}=\frac{9}{2}\). &nbsp; f) \(12:\frac{3}{4}=\frac{48}{3}=16\) ampolles.", r"e) \(\frac{15}{4}\cdot\frac{6}{5}=\frac{90}{20}=\frac{9}{2}\). &nbsp; f) \(12:\frac{3}{4}=\frac{48}{3}=16\) botellas.", r"e) \(\frac{15}{4}\cdot\frac{6}{5}=\frac{90}{20}=\frac{9}{2}\). &nbsp; f) \(12:\frac{3}{4}=\frac{48}{3}=16\) bottles."))

# ============================================================ 4.10
s10 = box('prop', L("Jerarquia de les operacions", 'Jerarquía de las operaciones', 'Order of operations'),
  P(r"Amb fraccions seguim el mateix ordre que amb els nombres naturals (unitat 1):", r"Con fracciones seguimos el mismo orden que con los números naturales (unidad 1):", r"With fractions we follow the same order as with whole numbers (unit 1):")
  + ol(L(r"<strong>Parèntesis</strong> i claudàtors, de dins cap a fora.", r"<strong>Paréntesis</strong> y corchetes, de dentro hacia fuera.", r"<strong>Brackets</strong>, from the inside out."),
       L(r"<strong>Multiplicacions i divisions</strong>, d'esquerra a dreta.", r"<strong>Multiplicaciones y divisiones</strong>, de izquierda a derecha.", r"<strong>Multiplication and division</strong>, from left to right."),
       L(r"<strong>Sumes i restes</strong>, d'esquerra a dreta.", r"<strong>Sumas y restas</strong>, de izquierda a derecha.", r"<strong>Addition and subtraction</strong>, from left to right."))
  + r'\[\frac{5}{2}+\underbrace{\frac{1}{3}\cdot\frac{4}{5}}_{\frac{4}{15}}=\frac{75}{30}+\frac{8}{30}=\frac{83}{30}\qquad\qquad \frac{4}{3}\cdot\underbrace{\left(\frac{2}{5}+\frac{1}{3}\right)}_{\frac{11}{15}}=\frac{44}{45}\]'
  + note(r"Simplifica els resultats intermedis: els nombres es fan més xicotets i hi ha menys errors.", r"Simplifica los resultados intermedios: los números se hacen más pequeños y hay menos errores.", r"Simplify the intermediate results: the numbers stay smaller and you'll make fewer mistakes.")
  + hier(["5/2+1/3·4/5", "4/3·(2/5+1/3)", "21/4-2/5:4/3", "(2/5+1):8/3", "(5/4+1)·6/7", "(1/4+2/3-1/12)·3+(3/2-5/4):1/2", "3/2:1/4·4/20+3/2·7/5"])
  + drill('comb', 'Entrena: operacions combinades', 'Entrena: operaciones combinadas', 'Train: mixed operations'))
s10 += level(1, 1,
  prob(L(r"Calcula: \(\ \frac{21}{4}-\frac{2}{5}:\frac{4}{3}\)", r"Calcula: \(\ \frac{21}{4}-\frac{2}{5}:\frac{4}{3}\)", r"Work out: \(\ \frac{21}{4}-\frac{2}{5}:\frac{4}{3}\)"),
       P(r"Primer la divisió:", r"Primero la división:", r"Division first:") + r'\[\frac{2}{5}:\frac{4}{3}=\frac{6}{20}=\frac{3}{10}\]',
       P(r"Després la resta, amb \(\text{" + MCM + r"}(4,10)=20\):", r"Después la resta, con \(\text{" + MCM + r"}(4,10)=20\):", r"Then the subtraction, with \(\text{" + MCM + r"}(4,10)=20\):") + r'\[\frac{21}{4}-\frac{3}{10}=\frac{105}{20}-\frac{6}{20}=\boxed{\frac{99}{20}}\]'))
s10 += level(2, 2,
  prob(L(r"Calcula: \(\ \left(\frac{2}{5}+1\right):\frac{8}{3}\)", r"Calcula: \(\ \left(\frac{2}{5}+1\right):\frac{8}{3}\)", r"Work out: \(\ \left(\frac{2}{5}+1\right):\frac{8}{3}\)"),
       r'\[\frac{2}{5}+1=\frac{2}{5}+\frac{5}{5}=\frac{7}{5}\]', r'\[\frac{7}{5}:\frac{8}{3}=\frac{7\cdot3}{5\cdot8}=\boxed{\frac{21}{40}}\]'),
  prob(L(r"Calcula: \(\ \left(\frac{5}{4}+1\right)\cdot\frac{6}{7}\)", r"Calcula: \(\ \left(\frac{5}{4}+1\right)\cdot\frac{6}{7}\)", r"Work out: \(\ \left(\frac{5}{4}+1\right)\cdot\frac{6}{7}\)"),
       r'\[\frac{5}{4}+1=\frac{9}{4}\qquad \frac{9}{4}\cdot\frac{6}{7}=\frac{54}{28}=\boxed{\frac{27}{14}}\]'))
s10 += level(3, 4,
  prob(L(r"Calcula: \(\ \left(\frac{1}{4}+\frac{2}{3}-\frac{1}{12}\right)\cdot3+\left(\frac{3}{2}-\frac{5}{4}\right):\frac{1}{2}\)", r"Calcula: \(\ \left(\frac{1}{4}+\frac{2}{3}-\frac{1}{12}\right)\cdot3+\left(\frac{3}{2}-\frac{5}{4}\right):\frac{1}{2}\)", r"Work out: \(\ \left(\frac{1}{4}+\frac{2}{3}-\frac{1}{12}\right)\cdot3+\left(\frac{3}{2}-\frac{5}{4}\right):\frac{1}{2}\)"),
       P(r"Primer parèntesi (mcm 12):", r"Primer paréntesis (mcm 12):", r"First bracket (lcm 12):") + r'\[\frac{3}{12}+\frac{8}{12}-\frac{1}{12}=\frac{10}{12}=\frac{5}{6}\]',
       P(r"Segon parèntesi (mcm 4):", r"Segundo paréntesis (mcm 4):", r"Second bracket (lcm 4):") + r'\[\frac{6}{4}-\frac{5}{4}=\frac{1}{4}\]',
       P(r"Multiplicació i divisió:", r"Multiplicación y división:", r"Multiplication and division:") + r'\[\frac{5}{6}\cdot3=\frac{15}{6}=\frac{5}{2}\qquad \frac{1}{4}:\frac{1}{2}=\frac{2}{4}=\frac{1}{2}\]',
       P(r"Suma final:", r"Suma final:", r"Final addition:") + r'\[\frac{5}{2}+\frac{1}{2}=\frac{6}{2}=\boxed{3}\]'))
s10 += practice([
  ('★', L(r"a) \(\frac{2}{3}+\frac{1}{2}\cdot\frac{4}{5}\) &nbsp; b) \(\frac{4}{3}:\frac{2}{6}+\frac{1}{3}\cdot\frac{5}{4}\)", r"a) \(\frac{2}{3}+\frac{1}{2}\cdot\frac{4}{5}\) &nbsp; b) \(\frac{4}{3}:\frac{2}{6}+\frac{1}{3}\cdot\frac{5}{4}\)", r"a) \(\frac{2}{3}+\frac{1}{2}\cdot\frac{4}{5}\) &nbsp; b) \(\frac{4}{3}:\frac{2}{6}+\frac{1}{3}\cdot\frac{5}{4}\)")),
  ('★★', L(r"c) \(\left(\frac{3}{2}+\frac{1}{7}\right)\cdot\left(\frac{5}{3}-\frac{7}{15}\right)\) &nbsp; d) \(4\cdot\left(\frac{2}{3}+\frac{4}{6}-1\right)+\frac{2}{3}\)", r"c) \(\left(\frac{3}{2}+\frac{1}{7}\right)\cdot\left(\frac{5}{3}-\frac{7}{15}\right)\) &nbsp; d) \(4\cdot\left(\frac{2}{3}+\frac{4}{6}-1\right)+\frac{2}{3}\)", r"c) \(\left(\frac{3}{2}+\frac{1}{7}\right)\cdot\left(\frac{5}{3}-\frac{7}{15}\right)\) &nbsp; d) \(4\cdot\left(\frac{2}{3}+\frac{4}{6}-1\right)+\frac{2}{3}\)")),
  ('★★★', L(r"e) \(\frac{4}{3}+\frac{2}{5}\cdot\left(\frac{1}{3}+\frac{2}{5}\right)\) &nbsp; f) \(\left(\frac{4}{3}+\frac{2}{5}\cdot\frac{1}{3}\right):\frac{4}{12}\)", r"e) \(\frac{4}{3}+\frac{2}{5}\cdot\left(\frac{1}{3}+\frac{2}{5}\right)\) &nbsp; f) \(\left(\frac{4}{3}+\frac{2}{5}\cdot\frac{1}{3}\right):\frac{4}{12}\)", r"e) \(\frac{4}{3}+\frac{2}{5}\cdot\left(\frac{1}{3}+\frac{2}{5}\right)\) &nbsp; f) \(\left(\frac{4}{3}+\frac{2}{5}\cdot\frac{1}{3}\right):\frac{4}{12}\)"))],
  P(r"a) \(\frac{2}{3}+\frac{2}{5}=\frac{16}{15}\). &nbsp; b) \(4+\frac{5}{12}=\frac{53}{12}\).", r"a) \(\frac{2}{3}+\frac{2}{5}=\frac{16}{15}\). &nbsp; b) \(4+\frac{5}{12}=\frac{53}{12}\).", r"a) \(\frac{2}{3}+\frac{2}{5}=\frac{16}{15}\). &nbsp; b) \(4+\frac{5}{12}=\frac{53}{12}\).")
  + P(r"c) \(\frac{23}{14}\cdot\frac{6}{5}=\frac{138}{70}=\frac{69}{35}\). &nbsp; d) \(4\cdot\frac{1}{3}+\frac{2}{3}=\frac{6}{3}=2\).", r"c) \(\frac{23}{14}\cdot\frac{6}{5}=\frac{138}{70}=\frac{69}{35}\). &nbsp; d) \(4\cdot\frac{1}{3}+\frac{2}{3}=\frac{6}{3}=2\).", r"c) \(\frac{23}{14}\cdot\frac{6}{5}=\frac{138}{70}=\frac{69}{35}\). &nbsp; d) \(4\cdot\frac{1}{3}+\frac{2}{3}=\frac{6}{3}=2\).")
  + P(r"e) \(\frac{4}{3}+\frac{2}{5}\cdot\frac{11}{15}=\frac{4}{3}+\frac{22}{75}=\frac{122}{75}\). &nbsp; f) \(\frac{22}{15}:\frac{1}{3}=\frac{66}{15}=\frac{22}{5}\).", r"e) \(\frac{4}{3}+\frac{2}{5}\cdot\frac{11}{15}=\frac{4}{3}+\frac{22}{75}=\frac{122}{75}\). &nbsp; f) \(\frac{22}{15}:\frac{1}{3}=\frac{66}{15}=\frac{22}{5}\).", r"e) \(\frac{4}{3}+\frac{2}{5}\cdot\frac{11}{15}=\frac{4}{3}+\frac{22}{75}=\frac{122}{75}\). &nbsp; f) \(\frac{22}{15}:\frac{1}{3}=\frac{66}{15}=\frac{22}{5}\)."))

# ============================================================ 4.11
s11 = box('prop', L('Tipus de problemes amb fraccions', 'Tipos de problemas con fracciones', 'Kinds of fraction problems'),
  ul(L(r"<strong>Fracció d'una quantitat:</strong> «gasta \(\frac{2}{5}\) de 300 €» → \(\frac{2}{5}\cdot300=120\) €.", r"<strong>Fracción de una cantidad:</strong> «gasta \(\frac{2}{5}\) de 300 €» → \(\frac{2}{5}\cdot300=120\) €.", r"<strong>Fraction of an amount:</strong> “spends \(\frac{2}{5}\) of €300” → \(\frac{2}{5}\cdot300=120\) €."),
     L(r"<strong>Parts d'un total:</strong> si coneixem algunes parts, la que falta és \(1-\) (suma de les parts). El total sempre és \(1=\frac{b}{b}\).", r"<strong>Partes de un total:</strong> si conocemos algunas partes, la que falta es \(1-\) (suma de las partes). El total siempre es \(1=\frac{b}{b}\).", r"<strong>Parts of a whole:</strong> if we know some parts, the missing one is \(1-\) (sum of the parts). The whole is always \(1=\frac{b}{b}\)."),
     L(r"<strong>Fracció del que queda:</strong> primer calculem el que queda i després en calculem la fracció. Compte: no és el mateix «\(\frac{1}{3}\) del total» que «\(\frac{1}{3}\) del que queda».", r"<strong>Fracción de lo que queda:</strong> primero calculamos lo que queda y después calculamos su fracción. Cuidado: no es lo mismo «\(\frac{1}{3}\) del total» que «\(\frac{1}{3}\) de lo que queda».", r"<strong>Fraction of what's left:</strong> first find what's left, then take the fraction of it. Careful: “\(\frac{1}{3}\) of the total” is not the same as “\(\frac{1}{3}\) of what's left”."),
     L(r"<strong>Conéixer la part i buscar el total:</strong> dividim la part entre el numerador i multipliquem pel denominador.", r"<strong>Conocer la parte y buscar el total:</strong> dividimos la parte entre el numerador y multiplicamos por el denominador.", r"<strong>Knowing the part, finding the whole:</strong> divide the part by the numerator and multiply by the denominator."))
  + note(r"Llig l'enunciat dues vegades, fes un <strong>dibuix</strong> (una barra que representa el total) i, al final, <strong>comprova</strong> que la resposta té sentit.",
         r"Lee el enunciado dos veces, haz un <strong>dibujo</strong> (una barra que representa el total) y, al final, <strong>comprueba</strong> que la respuesta tiene sentido.",
         r"Read the problem twice, draw a <strong>picture</strong> (a bar for the whole) and, at the end, <strong>check</strong> that the answer makes sense.")
  + f'''<div class="widget" id="w-rest">
  <div class="wt">🛢️ {L("Fracció del que queda", "Fracción de lo que queda", "Fraction of what's left")}</div>
  <div class="wrow">{nin("t", "Total", "Total", "Total", "60", "")}<label>{L("1r: gastem", "1.º: gastamos", "1st: we use")} {fin("a", "b", "1", "2")}</label><label>{L("2n: gastem", "2.º: gastamos", "2nd: we use")} {fin("c", "d", "1", "3")} {L("del que queda", "de lo que queda", "of what's left")}</label></div>
  {quick([("60,1,2,1,3", "60 · 1/2 · 1/3"), ("120,2,5,3,4", "120 · 2/5 · 3/4"), ("900,1,4,2,3", "900 · 1/4 · 2/3"), ("5400,1,3,1,2", "5400 · 1/3 · 1/2")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''')
s11 += level(1, 1,
  prob(L(r"De tot un sopar, en Joan s'ha menjat \(\frac{1}{7}\), l'Elena \(\frac{2}{5}\) i la Maite \(\frac{1}{8}\). Quant s'han menjat entre tots tres? Quant n'ha sobrat? Qui ha menjat més?", r"De toda una cena, Joan se ha comido \(\frac{1}{7}\), Elena \(\frac{2}{5}\) y Maite \(\frac{1}{8}\). ¿Cuánto se han comido entre los tres? ¿Cuánto ha sobrado? ¿Quién ha comido más?", r"Of a whole dinner, Joan ate \(\frac{1}{7}\), Elena \(\frac{2}{5}\) and Maite \(\frac{1}{8}\). How much did they eat in total? How much is left? Who ate most?"),
       P(r"Sumem les tres parts amb \(\text{" + MCM + r"}(7,5,8)=280\):", r"Sumamos las tres partes con \(\text{" + MCM + r"}(7,5,8)=280\):", r"Add the three parts with \(\text{" + MCM + r"}(7,5,8)=280\):") + r'\[\frac{40}{280}+\frac{112}{280}+\frac{35}{280}=\boxed{\frac{187}{280}}\]',
       P(r"El total és \(1=\frac{280}{280}\):", r"El total es \(1=\frac{280}{280}\):", r"The whole is \(1=\frac{280}{280}\):") + r'\[\frac{280}{280}-\frac{187}{280}=\boxed{\frac{93}{280}}\ \tri{sobra}{sobra}{left}\]',
       P(r"Comparant numeradors (\(112>40>35\)), ha menjat més l'<strong>Elena</strong> i menys la <strong>Maite</strong>.", r"Comparando numeradores (\(112>40>35\)), ha comido más <strong>Elena</strong> y menos <strong>Maite</strong>.", r"Comparing numerators (\(112>40>35\)), <strong>Elena</strong> ate most and <strong>Maite</strong> least.")))
s11 += level(2, 2,
  prob(L(r"Un bidó de 60 litres està ple. Primer se'n gasten \(\frac{2}{4}\) i després \(\frac{1}{3}\) del que quedava. Finalment, el bidó bolca i es vessa la meitat del que hi ha. Quants litres queden?", r"Un bidón de 60 litros está lleno. Primero se gastan \(\frac{2}{4}\) y después \(\frac{1}{3}\) de lo que quedaba. Finalmente, el bidón vuelca y se derrama la mitad de lo que hay. ¿Cuántos litros quedan?", r"A 60-litre drum is full. First \(\frac{2}{4}\) is used, then \(\frac{1}{3}\) of what was left. Finally the drum tips over and half of what's in it spills. How many litres are left?"),
       r'\[\frac{2}{4}\ ' + D + r'\ 60=30\ \text{L}\ \to\ \tri{queden}{quedan}{left}\ 60-30=30\ \text{L}\]',
       r'\[\frac{1}{3}\ ' + D + r'\ 30=10\ \text{L}\ \to\ \tri{queden}{quedan}{left}\ 30-10=20\ \text{L}\]',
       r'\[\tri{Es vessa la meitat}{Se derrama la mitad}{Half spills}:\ 20:2=10\ \to\ \boxed{10\ \text{L}}\]'),
  prob(L(r"En un poble de 5250 habitants, la meitat tenen més de 65 anys i \(\frac{1}{5}\), menys de 18. Quina fracció representen els que tenen entre 18 i 65 anys? Quants n'hi ha de cada grup?", r"En un pueblo de 5250 habitantes, la mitad tienen más de 65 años y \(\frac{1}{5}\), menos de 18. ¿Qué fracción representan los que tienen entre 18 y 65 años? ¿Cuántos hay de cada grupo?", r"In a village of 5250 people, half are over 65 and \(\frac{1}{5}\) are under 18. What fraction are aged 18 to 65? How many are in each group?"),
       r'\[1-\frac{1}{2}-\frac{1}{5}=\frac{10}{10}-\frac{5}{10}-\frac{2}{10}=\boxed{\frac{3}{10}}\]',
       r'\[\frac{1}{2}\cdot5250=2625\qquad \frac{1}{5}\cdot5250=1050\qquad \frac{3}{10}\cdot5250=1575\]',
       P(r"Comprovació: \(2625+1050+1575=5250\).", r"Comprobación: \(2625+1050+1575=5250\).", r"Check: \(2625+1050+1575=5250\).")))
s11 += level(3, 4,
  prob(L(r"Una família ingressa 5400 € al mes. En gasta \(\frac{2}{6}\) en la hipoteca, \(\frac{1}{5}\) en menjar i \(\frac{1}{9}\) en el cotxe. Quants diners gasta en cada cosa? Quants en queden? Quina fracció representen?", r"Una familia ingresa 5400 € al mes. Gasta \(\frac{2}{6}\) en la hipoteca, \(\frac{1}{5}\) en comida y \(\frac{1}{9}\) en el coche. ¿Cuánto dinero gasta en cada cosa? ¿Cuánto queda? ¿Qué fracción representa?", r"A family earns €5400 a month. It spends \(\frac{2}{6}\) on the mortgage, \(\frac{1}{5}\) on food and \(\frac{1}{9}\) on the car. How much goes on each? How much is left? What fraction is that?"),
       r'\[\frac{2}{6}\cdot5400=1800\ \text{€}\qquad \frac{1}{5}\cdot5400=1080\ \text{€}\qquad \frac{1}{9}\cdot5400=600\ \text{€}\]',
       r'\[5400-1800-1080-600=\boxed{1920\ \text{€}}\]',
       r'\[\frac{1920}{5400}=\boxed{\frac{16}{45}}\qquad\left(1-\frac{15}{45}-\frac{9}{45}-\frac{5}{45}=\frac{16}{45}\right)\]'),
  prob(L(r"Una ciclista ha fet \(\frac{3}{8}\) d'una etapa i encara li queden 45 km. Quants quilòmetres té l'etapa?", r"Una ciclista ha hecho \(\frac{3}{8}\) de una etapa y aún le quedan 45 km. ¿Cuántos kilómetros tiene la etapa?", r"A cyclist has done \(\frac{3}{8}\) of a stage and still has 45 km to go. How long is the stage?"),
       P(r"Li queden \(1-\frac{3}{8}=\frac{5}{8}\) de l'etapa, que són 45 km.", r"Le quedan \(1-\frac{3}{8}=\frac{5}{8}\) de la etapa, que son 45 km.", r"She has \(1-\frac{3}{8}=\frac{5}{8}\) of the stage left, which is 45 km."),
       r'\[45:5=9\ \text{km}\ (\tri{cada huité}{cada octavo}{each eighth})\qquad 9\cdot8=\boxed{72\ \text{km}}\]'))
s11 += practice([
  ('★', L(r"a) D'un pastís de 24 porcions ens hem menjat \(\frac{5}{8}\). Quantes porcions queden? b) En un viatge de 360 km ja hem fet \(\frac{4}{9}\). Quants quilòmetres falten?", r"a) De una tarta de 24 porciones nos hemos comido \(\frac{5}{8}\). ¿Cuántas porciones quedan? b) En un viaje de 360 km ya hemos hecho \(\frac{4}{9}\). ¿Cuántos kilómetros faltan?", r"a) We've eaten \(\frac{5}{8}\) of a 24-slice cake. How many slices are left? b) On a 360 km trip we've done \(\frac{4}{9}\). How many kilometres are left?")),
  ('★★', L(r"c) D'una pizza, en Carles se'n menja \(\frac{3}{6}\), en Miquel \(\frac{3}{21}\) i la Lorena \(\frac{4}{14}\). Quina fracció en sobra? d) En una província de 378 000 persones, el 7 % són del Marroc, el 25 % de l'est d'Europa, el 12 % d'Alemanya i la resta d'ací. Quin percentatge són d'ací? Quantes persones hi ha de cada grup?", r"c) De una pizza, Carles se come \(\frac{3}{6}\), Miquel \(\frac{3}{21}\) y Lorena \(\frac{4}{14}\). ¿Qué fracción sobra? d) En una provincia de 378 000 personas, el 7 % son de Marruecos, el 25 % del este de Europa, el 12 % de Alemania y el resto de aquí. ¿Qué porcentaje son de aquí? ¿Cuántas personas hay de cada grupo?", r"c) Of a pizza, Carles eats \(\frac{3}{6}\), Miquel \(\frac{3}{21}\) and Lorena \(\frac{4}{14}\). What fraction is left? d) In a province of 378,000 people, 7% are from Morocco, 25% from Eastern Europe, 12% from Germany and the rest are local. What percentage are local? How many people are in each group?")),
  ('★★★', L(r"e) Un dipòsit està ple fins als \(\frac{3}{4}\). Gastem \(\frac{2}{3}\) del que hi ha i queden 50 litres. Quina capacitat té el dipòsit? f) Una família gasta \(\frac{2}{6}\) del sou en la hipoteca, \(\frac{1}{5}\) en menjar, \(\frac{2}{7}\) en el cotxe i la resta en altres despeses. Quina fracció representen les altres despeses?", r"e) Un depósito está lleno hasta los \(\frac{3}{4}\). Gastamos \(\frac{2}{3}\) de lo que hay y quedan 50 litros. ¿Qué capacidad tiene el depósito? f) Una familia gasta \(\frac{2}{6}\) del sueldo en la hipoteca, \(\frac{1}{5}\) en comida, \(\frac{2}{7}\) en el coche y el resto en otros gastos. ¿Qué fracción representan los otros gastos?", r"e) A tank is \(\frac{3}{4}\) full. We use \(\frac{2}{3}\) of what's in it and 50 litres are left. What is the tank's capacity? f) A family spends \(\frac{2}{6}\) of its pay on the mortgage, \(\frac{1}{5}\) on food, \(\frac{2}{7}\) on the car and the rest on other things. What fraction goes on other things?"))],
  P(r"a) Ens hem menjat \(15\): queden \(9\) porcions. &nbsp; b) Hem fet \(160\) km: en falten \(200\).", r"a) Nos hemos comido \(15\): quedan \(9\) porciones. &nbsp; b) Hemos hecho \(160\) km: faltan \(200\).", r"a) We've eaten \(15\): \(9\) slices are left. &nbsp; b) We've done \(160\) km: \(200\) are left.")
  + P(r"c) \(\frac{1}{2}+\frac{1}{7}+\frac{2}{7}=\frac{13}{14}\): en sobra \(\frac{1}{14}\). &nbsp; d) \(100-44=56\,\%\) d'ací; \(26\,460\), \(94\,500\), \(45\,360\) i \(211\,680\) persones.", r"c) \(\frac{1}{2}+\frac{1}{7}+\frac{2}{7}=\frac{13}{14}\): sobra \(\frac{1}{14}\). &nbsp; d) \(100-44=56\,\%\) de aquí; \(26\,460\), \(94\,500\), \(45\,360\) y \(211\,680\) personas.", r"c) \(\frac{1}{2}+\frac{1}{7}+\frac{2}{7}=\frac{13}{14}\): \(\frac{1}{14}\) is left. &nbsp; d) \(100-44=56\,\%\) local; \(26\,460\), \(94\,500\), \(45\,360\) and \(211\,680\) people.")
  + P(r"e) Queda \(\frac{1}{3}\) de \(\frac{3}{4}\), és a dir, \(\frac{1}{4}\) del dipòsit, que són 50 L: la capacitat és \(200\) L. &nbsp; f) \(1-\left(\frac{35}{105}+\frac{21}{105}+\frac{30}{105}\right)=\frac{19}{105}\).", r"e) Queda \(\frac{1}{3}\) de \(\frac{3}{4}\), es decir, \(\frac{1}{4}\) del depósito, que son 50 L: la capacidad es \(200\) L. &nbsp; f) \(1-\left(\frac{35}{105}+\frac{21}{105}+\frac{30}{105}\right)=\frac{19}{105}\).", r"e) \(\frac{1}{3}\) of \(\frac{3}{4}\) is left, i.e. \(\frac{1}{4}\) of the tank, which is 50 L: the capacity is \(200\) L. &nbsp; f) \(1-\left(\frac{35}{105}+\frac{21}{105}+\frac{30}{105}\right)=\frac{19}{105}\)."))

# ============================================================ muntatge
SECS = [
  (L('El concepte de fracció', 'El concepto de fracción', 'What a fraction is'), s1),
  (L("Fracció d'un nombre", 'Fracción de un número', 'Fraction of a number'), s2),
  (L('Percentatges i fraccions', 'Porcentajes y fracciones', 'Percentages and fractions'), s3),
  (L('Fraccions equivalents', 'Fracciones equivalentes', 'Equivalent fractions'), s4),
  (L('Comprovar si són equivalents', 'Comprobar si son equivalentes', 'Checking equivalence'), s5),
  (L('Reducció a comú denominador', 'Reducción a común denominador', 'Common denominators'), s6),
  (L('Comparar i ordenar fraccions', 'Comparar y ordenar fracciones', 'Comparing and ordering'), s7),
  (L('Sumes i restes', 'Sumas y restas', 'Addition and subtraction'), s8),
  (L('Multiplicació i divisió', 'Multiplicación y división', 'Multiplication and division'), s9),
  (L('Operacions combinades', 'Operaciones combinadas', 'Mixed operations'), s10),
  (L('Problemes amb fraccions', 'Problemas con fracciones', 'Fraction problems'), s11),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Fraccions · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 4 (Fraccions) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "½";')
assert 'Fraccions · FentMates' in head and 'content: "½"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">4.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 4", "Unidad 4", "Unit 4")}</span>
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
    <h1><span class="u">{L("Unitat 4", "Unidad 4", "Unit 4")}</span> · {L("Fraccions", "Fracciones", "Fractions")}</h1>
    <p>{L("Què és una fracció i els seus tres significats, fracció d'un nombre, percentatges, fraccions equivalents, reducció a comú denominador, comparació i ordenació, operacions amb fraccions i problemes: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Qué es una fracción y sus tres significados, fracción de un número, porcentajes, fracciones equivalentes, reducción a común denominador, comparación y ordenación, operaciones con fracciones y problemas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "What a fraction is and its three meanings, fraction of a number, percentages, equivalent fractions, common denominators, comparing and ordering, operations with fractions and problems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 4: Fraccions · 1r ESO", "Apuntes de teoría · Unidad 4: Fracciones · 1º ESO", "Theory notes · Unit 4: Fractions · 1st ESO")}</p>
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
