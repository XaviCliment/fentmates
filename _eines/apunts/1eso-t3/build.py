import os, re, sys
from fractions import Fraction

# Genera materials/1eso/t3-nombres-enters.html. Ús: python3 _eines/apunts/1eso-t3/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t3-nombres-enters.html")

def L(va, es, en):
    return f'<span data-l="va">{va}</span><span data-l="es">{es}</span><span data-l="en">{en}</span>'
def P(va, es, en): return '<p>' + L(va, es, en) + '</p>'
def P1(t): return '<p>' + t + '</p>'
def box(cls, title, body):
    head = f'<div class="bh">{title}</div>' if title else ''
    return f'<div class="box {cls}">{head}<div class="bb">{body}</div></div>\n'
def note(va, es, en, icon='💡'): return f'<div class="note"><p>{icon} {L(va, es, en)}</p></div>'
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
    return (f'\n<!-- ======================= 3.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">3.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
def drill(kind, va, es, en):
    return f'''<div class="widget w-drill" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin m" type="text" autocomplete="off" aria-label="resultat"></label><button class="btn drill-neg" type="button" data-a="neg" aria-label="±">±</button><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''
def quick(pairs, attr='b'):
    return '<div class="quick"><span class="ql">⚡</span>' + ''.join(f'<button type="button" data-{attr}="{v}">{t}</button>' for v, t in pairs) + '</div>'
def nin(k, va, es, en, val, cls='s'):
    return f'<label>{L(va, es, en)} <input class="tin {cls}" type="text" data-k="{k}" value="{val}" autocomplete="off" aria-label="{k}"></label>'
def seg(pairs, on):
    return '<div class="seg" role="group">' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == on else "false"}">{t}</button>' for k, t in pairs) + '</div>'
def hier(presets):
    keys = ''.join(f'<button type="button" data-ins="{k}">{k}</button>' for k in ['−', '·', ':', '(', ')', '[', ']'])
    q = ''.join(f'<button type="button" data-e="{e}">{e.replace("-", "−")}</button>' for e in presets)
    return f'''<div class="widget w-hier">
  <div class="wt">🧮 {L("Calculadora pas a pas", "Calculadora paso a paso", "Step-by-step calculator")}</div>
  <div class="wrow"><label>{L("Expressió", "Expresión", "Expression")} <input class="tin w" type="text" value="{presets[0].replace("-", "−")}" autocomplete="off" spellcheck="false" aria-label="expressió"></label></div>
  <div class="quick kp"><span class="ql">⌨</span>{keys}</div>
  <div class="quick"><span class="ql">⚡</span>{q}</div>
  <div class="hsteps"></div>
  <div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><span class="step-count"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''

# ---------- aritmètica per a les solucions (evita errors de càlcul) ----------
def ev(e):
    s = re.sub(r'(\d+)', r'F(\1)', e.replace('·', '*').replace(':', '/').replace('[', '(').replace(']', ')'))
    v = eval(s, {'F': Fraction})
    assert v.denominator == 1, e
    return int(v)
def tx(e): return e.replace('·', r'\cdot ')
def eq(e): return tx(e) + '=' + str(ev(e))
def OP(x): return r'\text{op}(' + x + ')'

# ---------- recta numèrica estàtica ----------
def nline(lo, hi, pts=(), arcs='', h=78):
    X0, X1 = 40, 580
    x = lambda v: X0 + (v - lo) * (X1 - X0) / (hi - lo)
    s = (f'<div class="nline"><svg viewBox="0 0 620 {h}" role="img" aria-label="recta"><line class="sv-ax" x1="16" y1="40" x2="604" y2="40"/>'
         '<path class="sv-ax" d="M596 34 L606 40 L596 46" fill="none"/><path class="sv-ax" d="M24 34 L14 40 L24 46" fill="none"/>')
    for v in range(lo, hi + 1):
        c = 'sv-tb' if v == 0 else 'sv-t'
        s += f'<line class="sv-ax" x1="{x(v):.1f}" y1="33" x2="{x(v):.1f}" y2="47"/><text class="{c}" x="{x(v):.1f}" y="68" text-anchor="middle">{str(v).replace("-", "−")}</text>'
    s += arcs if isinstance(arcs, str) else arcs(x)
    for v in pts:
        s += f'<circle class="{"sv-neg" if v < 0 else "sv-pos" if v > 0 else "sv-dot"}" cx="{x(v):.1f}" cy="40" r="6"/>'
    return s + '</svg></div>'

# ============================================================ 3.1
CTX = [  # (situació va, es, en, enter)
  ('Fa 5 °C sobre zero', 'Hace 5 °C sobre cero', 'It is 5 °C above zero', '+5'),
  ('Fa 3 °C baix zero', 'Hace 3 °C bajo cero', 'It is 3 °C below zero', '-3'),
  ('Vivim a la quarta planta', 'Vivimos en la cuarta planta', 'We live on the fourth floor', '+4'),
  ('El cotxe està al segon soterrani', 'El coche está en el segundo sótano', 'The car is on the second basement level', '-2'),
  ('Tinc 20 € estalviats', 'Tengo 20 € ahorrados', 'I have €20 saved', '+20'),
  ('Dec 15 € a la meua germana', 'Debo 15 € a mi hermana', 'I owe my sister €15', '-15'),
  ('Una muntanya de 800 m d\'altitud', 'Una montaña de 800 m de altitud', 'A mountain 800 m high', '+800'),
  ('Un submarí a 50 m de profunditat', 'Un submarino a 50 m de profundidad', 'A submarine 50 m deep', '-50'),
  ('L\'any 2026 d. C.', 'El año 2026 d. C.', 'The year 2026 AD', '+2026'),
  ('Sòcrates va nàixer el 470 a. C.', 'Sócrates nació en el 470 a. C.', 'Socrates was born in 470 BC', '-470'),
  ('Guanyem per 3 gols de diferència', 'Ganamos por 3 goles de diferencia', 'We win by 3 goals', '+3'),
  ('Ens resten 2 punts per una falta', 'Nos restan 2 puntos por una falta', 'We lose 2 points for a foul', '-2'),
]
ctx_tab = ('<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Situació', 'Situación', 'Situation') + '</th><th>' + L('Nombre enter', 'Número entero', 'Integer')
           + '</th><th>' + L('Situació', 'Situación', 'Situation') + '</th><th>' + L('Nombre enter', 'Número entero', 'Integer') + '</th></tr></thead><tbody>'
           + ''.join('<tr><td class="l">' + L(*CTX[i][:3]) + r'</td><td>\(' + CTX[i][3] + r'\)</td><td class="l">' + L(*CTX[i + 1][:3]) + r'</td><td>\(' + CTX[i + 1][3] + r'\)</td></tr>' for i in range(0, len(CTX), 2))
           + '</tbody></table></div>')

s1 = box('def', L('Per què necessitem els nombres enters?', '¿Por qué necesitamos los números enteros?', 'Why do we need integers?'),
  P(r"Amb els nombres naturals no podem expressar moltes situacions de la vida real: una temperatura <strong>baix zero</strong>, un <strong>soterrani</strong>, un <strong>deute</strong>, una <strong>profunditat</strong> sota el nivell de la mar o un any <strong>abans de Crist</strong>. Tampoc podem fer restes com \(3-5\).",
    r"Con los números naturales no podemos expresar muchas situaciones de la vida real: una temperatura <strong>bajo cero</strong>, un <strong>sótano</strong>, una <strong>deuda</strong>, una <strong>profundidad</strong> bajo el nivel del mar o un año <strong>antes de Cristo</strong>. Tampoco podemos hacer restas como \(3-5\).",
    r"Natural numbers can't describe many real-life situations: a temperature <strong>below zero</strong>, a <strong>basement</strong>, a <strong>debt</strong>, a <strong>depth</strong> below sea level or a year <strong>BC</strong>. Nor can we work out subtractions like \(3-5\).")
  + P(r"Per a això fem servir nombres amb <strong>signe</strong>: el signe \(+\) indica que estem <em>per damunt</em> d'una referència (el zero) i el signe \(-\), que estem <em>per davall</em>.",
      r"Para ello usamos números con <strong>signo</strong>: el signo \(+\) indica que estamos <em>por encima</em> de una referencia (el cero) y el signo \(-\), que estamos <em>por debajo</em>.",
      r"For this we use numbers with a <strong>sign</strong>: the \(+\) sign means we are <em>above</em> a reference point (zero) and the \(-\) sign means we are <em>below</em> it."))
s1 += box('def', L('Definició: nombres enters', 'Definición: números enteros', 'Definition: integers'),
  P(r"Els <strong>nombres enters</strong> són els nombres naturals amb signe positiu, els seus oposats amb signe negatiu i el zero. El conjunt dels enters es representa amb la lletra \(\mathbb{Z}\):",
    r"Los <strong>números enteros</strong> son los números naturales con signo positivo, sus opuestos con signo negativo y el cero. El conjunto de los enteros se representa con la letra \(\mathbb{Z}\):",
    r"<strong>Integers</strong> are the natural numbers with a positive sign, their opposites with a negative sign, and zero. The set of integers is written with the letter \(\mathbb{Z}\):")
  + r'\[\mathbb{Z}=\{\,\ldots,\ -4,\ -3,\ -2,\ -1,\ 0,\ +1,\ +2,\ +3,\ +4,\ \ldots\}\]'
  + ul(L(r"<strong>Enters positius:</strong> \(+1,\ +2,\ +3\ldots\) Coincideixen amb els naturals i el signe \(+\) es pot ometre: \(+7=7\).",
         r"<strong>Enteros positivos:</strong> \(+1,\ +2,\ +3\ldots\) Coinciden con los naturales y el signo \(+\) se puede omitir: \(+7=7\).",
         r"<strong>Positive integers:</strong> \(+1,\ +2,\ +3\ldots\) They are the natural numbers, and the \(+\) sign can be left out: \(+7=7\)."),
       L(r"<strong>Enters negatius:</strong> \(-1,\ -2,\ -3\ldots\) El signe \(-\) <strong>sempre</strong> s'ha d'escriure.",
         r"<strong>Enteros negativos:</strong> \(-1,\ -2,\ -3\ldots\) El signo \(-\) <strong>siempre</strong> se tiene que escribir.",
         r"<strong>Negative integers:</strong> \(-1,\ -2,\ -3\ldots\) The \(-\) sign must <strong>always</strong> be written."),
       L(r"<strong>El zero</strong>, \(0\), no és ni positiu ni negatiu.",
         r"<strong>El cero</strong>, \(0\), no es ni positivo ni negativo.",
         r"<strong>Zero</strong>, \(0\), is neither positive nor negative."))
  + P(r"<strong>Exemples (sense context):</strong> \(\ -8,\ \ +15,\ \ 0,\ \ -1,\ \ 23,\ \ -100\). Tots són enters; només \(+15\), \(0\) i \(23\) són, a més, naturals.",
      r"<strong>Ejemplos (sin contexto):</strong> \(\ -8,\ \ +15,\ \ 0,\ \ -1,\ \ 23,\ \ -100\). Todos son enteros; solo \(+15\), \(0\) y \(23\) son, además, naturales.",
      r"<strong>Examples (no context):</strong> \(\ -8,\ \ +15,\ \ 0,\ \ -1,\ \ 23,\ \ -100\). They are all integers; only \(+15\), \(0\) and \(23\) are natural numbers too.")
  + note(r"Tots els nombres naturals són enters, però no tots els enters són naturals: \(\mathbb{N}\subset\mathbb{Z}\).",
         r"Todos los números naturales son enteros, pero no todos los enteros son naturales: \(\mathbb{N}\subset\mathbb{Z}\).",
         r"Every natural number is an integer, but not every integer is a natural number: \(\mathbb{N}\subset\mathbb{Z}\)."))
s1 += box('prop', L('Exemples amb context', 'Ejemplos con contexto', 'Examples in context'),
  P(r"Per a passar d'una situació a un enter, primer cal saber quin és el <strong>zero</strong> (la referència): 0 °C, la planta baixa, el nivell de la mar, no tindre ni deure diners, el naixement de Crist… Després, el que està <em>per damunt</em> és positiu i el que està <em>per davall</em>, negatiu.",
    r"Para pasar de una situación a un entero, primero hay que saber cuál es el <strong>cero</strong> (la referencia): 0 °C, la planta baja, el nivel del mar, no tener ni deber dinero, el nacimiento de Cristo… Después, lo que está <em>por encima</em> es positivo y lo que está <em>por debajo</em>, negativo.",
    r"To turn a situation into an integer, first find the <strong>zero</strong> (the reference point): 0 °C, the ground floor, sea level, having no money and no debt, the birth of Christ… Then whatever is <em>above</em> it is positive and whatever is <em>below</em> it is negative.")
  + ctx_tab
  + note(r"Paraules que solen indicar un <strong>negatiu</strong>: <em>baix zero, soterrani, deute, dec, profunditat, sota el nivell de la mar, abans de Crist, perdre, baixar, gastar, retirar</em>.",
         r"Palabras que suelen indicar un <strong>negativo</strong>: <em>bajo cero, sótano, deuda, debo, profundidad, bajo el nivel del mar, antes de Cristo, perder, bajar, gastar, retirar</em>.",
         r"Words that usually point to a <strong>negative</strong>: <em>below zero, basement, debt, owe, depth, below sea level, BC, lose, go down, spend, withdraw</em>.", '🔎')
  + f'''<div class="widget" id="w-ctx">
  <div class="wt">🌡 {L("De la situació al nombre enter", "De la situación al número entero", "From the situation to the integer")}</div>
  <div class="wrow">{seg([("temp", L("Temperatura", "Temperatura", "Temperature")), ("floor", L("Plantes", "Plantas", "Floors")), ("alt", L("Altitud", "Altitud", "Altitude")), ("money", L("Diners", "Dinero", "Money")), ("year", L("Anys", "Años", "Years"))], "temp")}</div>
  <div class="wrow">{nin("v", "Nombre enter", "Número entero", "Integer", "-6", "m")}</div>
  {quick([("temp|-6", "−6 °C"), ("floor|-3", L("3r soterrani", "3.er sótano", "3rd basement")), ("alt|432", "432 m"), ("alt|-120", "−120 m"), ("money|-25", L("dec 25 €", "debo 25 €", "owe €25")), ("year|-470", "470 a. C."), ("year|0", L("any 0?", "¿año 0?", "year 0?"))])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>
''')
s1 += level(1, 1,
  prob(L(r"Expressa amb un nombre enter: a) Un avió vola a 3000 m d'altura. b) Aquesta nit el termòmetre ha marcat 6 °C baix zero. c) El cotxe està aparcat al tercer soterrani. d) M'he gastat tots els diners.",
         r"Expresa con un número entero: a) Un avión vuela a 3000 m de altura. b) Esta noche el termómetro ha marcado 6 °C bajo cero. c) El coche está aparcado en el tercer sótano. d) Me he gastado todo el dinero.",
         r"Write an integer for each one: a) A plane flies at a height of 3000 m. b) Tonight the thermometer read 6 °C below zero. c) The car is parked on the third basement level. d) I've spent all my money."),
       P(r"Busquem la referència (el zero) i mirem si estem per damunt o per davall:", r"Buscamos la referencia (el cero) y miramos si estamos por encima o por debajo:", r"Find the reference point (zero) and check whether we are above or below it:"),
       r'\[\text{a)}\ +3000\qquad \text{b)}\ -6\qquad \text{c)}\ -3\qquad \text{d)}\ 0\]'
       + P(r"En d) no tinc diners, però tampoc en dec: estic justament en el zero.", r"En d) no tengo dinero, pero tampoco debo: estoy justo en el cero.", r"In d) I have no money, but I don't owe any either: I'm exactly at zero.")),
  prob(L(r"Classifica aquests nombres en positius, negatius i zero. Quins són naturals? \(\ -8,\ \ 15,\ \ 0,\ \ +3,\ \ -1,\ \ 100\)",
         r"Clasifica estos números en positivos, negativos y cero. ¿Cuáles son naturales? \(\ -8,\ \ 15,\ \ 0,\ \ +3,\ \ -1,\ \ 100\)",
         r"Sort these numbers into positive, negative and zero. Which are natural numbers? \(\ -8,\ \ 15,\ \ 0,\ \ +3,\ \ -1,\ \ 100\)"),
       P(r"Positius: \(15,\ +3,\ 100\). &nbsp; Negatius: \(-8,\ -1\). &nbsp; Zero: \(0\).", r"Positivos: \(15,\ +3,\ 100\). &nbsp; Negativos: \(-8,\ -1\). &nbsp; Cero: \(0\).", r"Positive: \(15,\ +3,\ 100\). &nbsp; Negative: \(-8,\ -1\). &nbsp; Zero: \(0\)."),
       P(r"Naturals són els positius i el zero: \(\boxed{15,\ +3,\ 100,\ 0}\).", r"Naturales son los positivos y el cero: \(\boxed{15,\ +3,\ 100,\ 0}\).", r"The natural numbers are the positives and zero: \(\boxed{15,\ +3,\ 100,\ 0}\).")))
s1 += level(2, 3,
  prob(L(r"Inventa una situació de la vida real per a cada enter: \(\ -10,\ \ +2500,\ \ -3\).", r"Inventa una situación de la vida real para cada entero: \(\ -10,\ \ +2500,\ \ -3\).", r"Make up a real-life situation for each integer: \(\ -10,\ \ +2500,\ \ -3\)."),
       P(r"Hi ha moltes respostes possibles. Per exemple: \(-10\): «Fa 10 graus baix zero». \(+2500\): «El cim d'una muntanya està a 2500 m d'altitud». \(-3\): «Dec 3 € a un amic».",
         r"Hay muchas respuestas posibles. Por ejemplo: \(-10\): «Hace 10 grados bajo cero». \(+2500\): «La cima de una montaña está a 2500 m de altitud». \(-3\): «Debo 3 € a un amigo».",
         r"There are many possible answers. For example: \(-10\): “It's 10 degrees below zero”. \(+2500\): “A mountain top is 2500 m above sea level”. \(-3\): “I owe a friend €3”.")),
  prob(L(r"Escriu l'enter anterior i el següent de \(-1\) i de \(-20\).", r"Escribe el entero anterior y el siguiente de \(-1\) y de \(-20\).", r"Write the integer just before and just after \(-1\) and \(-20\)."),
       P(r"L'<strong>anterior</strong> és una unitat menys i el <strong>següent</strong>, una unitat més. Amb negatius, «una unitat menys» vol dir allunyar-se del zero:", r"El <strong>anterior</strong> es una unidad menos y el <strong>siguiente</strong>, una unidad más. Con negativos, «una unidad menos» significa alejarse del cero:", r"The number <strong>before</strong> is one less and the number <strong>after</strong> is one more. With negatives, “one less” means moving away from zero:"),
       r'\[-2,\ \underline{-1},\ 0\qquad\qquad -21,\ \underline{-20},\ -19\]'))
s1 += level(3, 5,
  prob(L(r"Escriu tots els enters compresos entre \(-4\) i \(2\). Quants n'hi ha? I entre \(-15\) i \(15\)?", r"Escribe todos los enteros comprendidos entre \(-4\) y \(2\). ¿Cuántos hay? ¿Y entre \(-15\) y \(15\)?", r"Write all the integers between \(-4\) and \(2\). How many are there? And between \(-15\) and \(15\)?"),
       r'\[-3,\ -2,\ -1,\ 0,\ 1\ \ \to\ \ \boxed{5}\]',
       P(r"Entre \(-15\) i \(15\) hi ha els negatius del \(-14\) al \(-1\) (14), el zero (1) i els positius de l'1 al 14 (14): \(14+1+14=\boxed{29}\).", r"Entre \(-15\) y \(15\) están los negativos del \(-14\) al \(-1\) (14), el cero (1) y los positivos del 1 al 14 (14): \(14+1+14=\boxed{29}\).", r"Between \(-15\) and \(15\) there are the negatives from \(-14\) to \(-1\) (14), zero (1) and the positives from 1 to 14 (14): \(14+1+14=\boxed{29}\).")))
s1 += practice([
  ('★', L(r"Escriu l'enter que correspon a: a) Un bussejador a 12 m de profunditat. b) He guanyat 5 € en una aposta amb mon pare.", r"Escribe el entero que corresponde a: a) Un buceador a 12 m de profundidad. b) He ganado 5 € en una apuesta con mi padre.", r"Write the integer for: a) A diver 12 m deep. b) I won €5 in a bet with my dad.")),
  ('★★', L(r"c) Escriu l'anterior i el següent de \(-9\) i de \(0\). d) Inventa una situació per al nombre \(-25\).", r"c) Escribe el anterior y el siguiente de \(-9\) y de \(0\). d) Inventa una situación para el número \(-25\).", r"c) Write the integers just before and after \(-9\) and \(0\). d) Make up a situation for the number \(-25\).")),
  ('★★★', L(r"e) Quants enters hi ha compresos entre \(-10\) i \(10\)? f) Quin és el major enter negatiu? I el menor enter positiu?", r"e) ¿Cuántos enteros hay comprendidos entre \(-10\) y \(10\)? f) ¿Cuál es el mayor entero negativo? ¿Y el menor entero positivo?", r"e) How many integers are there between \(-10\) and \(10\)? f) Which is the largest negative integer? And the smallest positive integer?"))],
  P(r"a) \(-12\) &nbsp; b) \(+5\)", r"a) \(-12\) &nbsp; b) \(+5\)", r"a) \(-12\) &nbsp; b) \(+5\)")
  + P(r"c) \(-10\) i \(-8\); \(\ -1\) i \(1\). &nbsp; d) Per exemple: «Al compte del banc hi ha un deute de 25 €».", r"c) \(-10\) y \(-8\); \(\ -1\) y \(1\). &nbsp; d) Por ejemplo: «En la cuenta del banco hay una deuda de 25 €».", r"c) \(-10\) and \(-8\); \(\ -1\) and \(1\). &nbsp; d) For example: “The bank account is €25 overdrawn”.")
  + P(r"e) \(9+1+9=19\) (del \(-9\) al \(9\)). &nbsp; f) \(-1\) i \(+1\).", r"e) \(9+1+9=19\) (del \(-9\) al \(9\)). &nbsp; f) \(-1\) y \(+1\).", r"e) \(9+1+9=19\) (from \(-9\) to \(9\)). &nbsp; f) \(-1\) and \(+1\)."))

# ============================================================ 3.2
s2 = box('def', L('Els enters en la recta numèrica', 'Los enteros en la recta numérica', 'Integers on the number line'),
  P(r"Per a representar els enters dibuixem una recta i hi marquem el <strong>0</strong>. Els <strong>positius</strong> es col·loquen a la <strong>dreta</strong> del zero i els <strong>negatius</strong>, a l'<strong>esquerra</strong>, sempre a la mateixa distància l'un de l'altre:",
    r"Para representar los enteros dibujamos una recta y marcamos el <strong>0</strong>. Los <strong>positivos</strong> se colocan a la <strong>derecha</strong> del cero y los <strong>negativos</strong>, a la <strong>izquierda</strong>, siempre a la misma distancia unos de otros:",
    r"To show integers we draw a line and mark <strong>0</strong>. <strong>Positive</strong> numbers go to the <strong>right</strong> of zero and <strong>negative</strong> numbers to the <strong>left</strong>, always equally spaced:")
  + nline(-7, 7, range(-7, 8))
  + P(r"És com un termòmetre tombat o un edifici amb plantes i soterranis: el zero és la frontera entre els positius i els negatius.", r"Es como un termómetro tumbado o un edificio con plantas y sótanos: el cero es la frontera entre los positivos y los negativos.", r"It's like a thermometer lying on its side, or a building with floors and basements: zero is the border between positives and negatives.")
  + P(r"<strong>Exemple:</strong> representem \(-5,\ -2,\ 0,\ 3\) i \(6\):", r"<strong>Ejemplo:</strong> representamos \(-5,\ -2,\ 0,\ 3\) y \(6\):", r"<strong>Example:</strong> we plot \(-5,\ -2,\ 0,\ 3\) and \(6\):")
  + nline(-7, 7, [-5, -2, 0, 3, 6]))
s2 += box('prop', L('Ordre i comparació d\'enters', 'Orden y comparación de enteros', 'Ordering and comparing integers'),
  P(r"De dos enters, és <strong>més gran</strong> el que està <strong>més a la dreta</strong> en la recta. Ho escrivim amb els símbols \(<\) (menor que) i \(>\) (major que). Per tant:",
    r"De dos enteros, es <strong>mayor</strong> el que está <strong>más a la derecha</strong> en la recta. Lo escribimos con los símbolos \(<\) (menor que) y \(>\) (mayor que). Por tanto:",
    r"Of two integers, the <strong>bigger</strong> one is the one <strong>further to the right</strong> on the line. We write \(<\) (less than) and \(>\) (greater than). So:")
  + ul(L(r"Qualsevol <strong>positiu</strong> és més gran que el zero, i el zero és més gran que qualsevol <strong>negatiu</strong>: \(\ 2>0>-100\).", r"Cualquier <strong>positivo</strong> es mayor que el cero, y el cero es mayor que cualquier <strong>negativo</strong>: \(\ 2>0>-100\).", r"Any <strong>positive</strong> number is bigger than zero, and zero is bigger than any <strong>negative</strong>: \(\ 2>0>-100\)."),
       L(r"De dos <strong>positius</strong>, és més gran el que té més valor (com amb els naturals): \(\ 8>3\).", r"De dos <strong>positivos</strong>, es mayor el que tiene más valor (como con los naturales): \(\ 8>3\).", r"Of two <strong>positives</strong>, the one with the larger value is bigger (as with natural numbers): \(\ 8>3\)."),
       L(r"De dos <strong>negatius</strong>, és més gran el que està <strong>més a prop del zero</strong>: \(\ -3>-8\).", r"De dos <strong>negativos</strong>, es mayor el que está <strong>más cerca del cero</strong>: \(\ -3>-8\).", r"Of two <strong>negatives</strong>, the bigger one is the one <strong>closer to zero</strong>: \(\ -3>-8\)."))
  + nline(-9, 2, [-8, -3], h=78)
  + note(r"Pensa en temperatures: a \(-3\) °C fa menys fred que a \(-8\) °C, així que \(-3>-8\). I en diners: és millor deure 3 € que deure'n 8!",
         r"Piensa en temperaturas: a \(-3\) °C hace menos frío que a \(-8\) °C, así que \(-3>-8\). Y en dinero: ¡es mejor deber 3 € que deber 8!",
         r"Think of temperatures: \(-3\) °C is less cold than \(-8\) °C, so \(-3>-8\). And money: owing €3 is better than owing €8!", '🌡')
  + P(r"Per a <strong>ordenar</strong> diversos enters de menor a major, escrivim primer els negatius (del més allunyat del zero al més pròxim), després el zero i després els positius:",
      r"Para <strong>ordenar</strong> varios enteros de menor a mayor, escribimos primero los negativos (del más alejado del cero al más cercano), después el cero y después los positivos:",
      r"To <strong>order</strong> several integers from smallest to largest, write the negatives first (from furthest from zero to closest), then zero, then the positives:")
  + r'\[-7<-5<-4<-2<0<1<3<6\]'
  + f'''<div class="widget" id="w-line">
  <div class="wt">📏 {L("Representa i ordena", "Representa y ordena", "Plot and order")}</div>
  <div class="wrow"><label>{L("Nombres", "Números", "Numbers")} <input class="tin w" type="text" data-k="v" value="−2, 0, 4, −1, 8, −3, −7, 1" autocomplete="off" spellcheck="false" aria-label="nombres"></label>{seg([("asc", L("menor → major", "menor → mayor", "smallest → largest")), ("desc", L("major → menor", "mayor → menor", "largest → smallest"))], "asc")}</div>
  {quick([("−7, 3, 1, −4, 6, −5, −2, 0", "−7, 3, 1, −4…"), ("−7, 0, 1, −1, 8, −4, −9, 3", "−7, 0, 1, −1…"), ("−8, −9", "−8 ? −9"), ("−6, 6", "−6 ? 6"), ("−15, −51", "−15 ? −51"), ("−120, 35, −300, 0, 210", "−120, 35, −300…")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('ord', 'Entrena: el més gran i el més xicotet', 'Entrena: el mayor y el menor', 'Train: largest and smallest'))
s2 += level(1, 1,
  prob(L(r"Representa en la recta i ordena de menor a major: \(\ -4,\ 2,\ 0,\ -1,\ 5\).", r"Representa en la recta y ordena de menor a mayor: \(\ -4,\ 2,\ 0,\ -1,\ 5\).", r"Plot on the number line and order from smallest to largest: \(\ -4,\ 2,\ 0,\ -1,\ 5\)."),
       nline(-6, 6, [-4, 2, 0, -1, 5]),
       P(r"Els llegim d'esquerra a dreta:", r"Los leemos de izquierda a derecha:", r"Read them from left to right:") + r'\[\boxed{-4<-1<0<2<5}\]'),
  prob(L(r"Compara amb \(<\) o \(>\): \(\ \text{a)}\ -5\ \square\ 2\qquad \text{b)}\ -7\ \square\ -3\qquad \text{c)}\ 0\ \square\ -9\)", r"Compara con \(<\) o \(>\): \(\ \text{a)}\ -5\ \square\ 2\qquad \text{b)}\ -7\ \square\ -3\qquad \text{c)}\ 0\ \square\ -9\)", r"Compare using \(<\) or \(>\): \(\ \text{a)}\ -5\ \square\ 2\qquad \text{b)}\ -7\ \square\ -3\qquad \text{c)}\ 0\ \square\ -9\)"),
       P(r"a) Un negatiu sempre és menor que un positiu. b) Dos negatius: és més gran el més pròxim al zero. c) El zero és més gran que qualsevol negatiu.", r"a) Un negativo siempre es menor que un positivo. b) Dos negativos: es mayor el más cercano al cero. c) El cero es mayor que cualquier negativo.", r"a) A negative is always less than a positive. b) Two negatives: the one closer to zero is bigger. c) Zero is bigger than any negative."),
       r'\[\text{a)}\ -5<2\qquad \text{b)}\ -7<-3\qquad \text{c)}\ 0>-9\]'))
s2 += level(2, 3,
  prob(L(r"Ordena de major a menor: \(\ -12,\ 5,\ -3,\ 0,\ -20,\ 8,\ -1\).", r"Ordena de mayor a menor: \(\ -12,\ 5,\ -3,\ 0,\ -20,\ 8,\ -1\).", r"Order from largest to smallest: \(\ -12,\ 5,\ -3,\ 0,\ -20,\ 8,\ -1\)."),
       P(r"Primer els positius (el més gran davant), després el zero i després els negatius (del més pròxim al zero al més allunyat):", r"Primero los positivos (el mayor delante), después el cero y después los negativos (del más cercano al cero al más alejado):", r"First the positives (largest first), then zero, then the negatives (from closest to zero to furthest):"),
       r'\[\boxed{8>5>0>-1>-3>-12>-20}\]'),
  prob(L(r"Escriu tots els enters \(x\) que complixen \(-6<x<-2\).", r"Escribe todos los enteros \(x\) que cumplen \(-6<x<-2\).", r"Write all the integers \(x\) such that \(-6<x<-2\)."),
       P(r"Són els que estan a la dreta de \(-6\) i a l'esquerra de \(-2\) (sense incloure'ls):", r"Son los que están a la derecha de \(-6\) y a la izquierda de \(-2\) (sin incluirlos):", r"They are the ones to the right of \(-6\) and to the left of \(-2\) (not including them):"),
       r'\[\boxed{-5,\ -4,\ -3}\]'))
s2 += level(3, 5,
  prob(L(r"Quin enter està 4 unitats a l'esquerra de \(-3\)? Quins enters estan a 5 unitats de \(-1\)?", r"¿Qué entero está 4 unidades a la izquierda de \(-3\)? ¿Qué enteros están a 5 unidades de \(-1\)?", r"Which integer is 4 units to the left of \(-3\)? Which integers are 5 units away from \(-1\)?"),
       nline(-8, 5, [-7, -3]) + P(r"Moure's a l'esquerra és anar cap als nombres més xicotets: \(\boxed{-7}\).", r"Moverse a la izquierda es ir hacia los números más pequeños: \(\boxed{-7}\).", r"Moving left means going towards smaller numbers: \(\boxed{-7}\)."),
       nline(-8, 5, [-6, -1, 4]) + P(r"N'hi ha dos, un a cada costat: \(\boxed{-6}\) i \(\boxed{4}\).", r"Hay dos, uno a cada lado: \(\boxed{-6}\) y \(\boxed{4}\).", r"There are two, one on each side: \(\boxed{-6}\) and \(\boxed{4}\).")))
s2 += practice([
  ('★', L(r"a) Ordena de menor a major: \(\ 3,\ -6,\ 0,\ -2,\ 7,\ -9\). b) Compara: \(\ -10\ \square\ -1\), \(\ \ 4\ \square\ -4\).", r"a) Ordena de menor a mayor: \(\ 3,\ -6,\ 0,\ -2,\ 7,\ -9\). b) Compara: \(\ -10\ \square\ -1\), \(\ \ 4\ \square\ -4\).", r"a) Order from smallest to largest: \(\ 3,\ -6,\ 0,\ -2,\ 7,\ -9\). b) Compare: \(\ -10\ \square\ -1\), \(\ \ 4\ \square\ -4\).")),
  ('★★', L(r"c) Ordena de major a menor: \(\ -15,\ 12,\ -51,\ 0,\ -5\). d) Escriu tres enters compresos entre \(-11\) i \(-7\).", r"c) Ordena de mayor a menor: \(\ -15,\ 12,\ -51,\ 0,\ -5\). d) Escribe tres enteros comprendidos entre \(-11\) y \(-7\).", r"c) Order from largest to smallest: \(\ -15,\ 12,\ -51,\ 0,\ -5\). d) Write three integers between \(-11\) and \(-7\).")),
  ('★★★', L(r"e) Vertader o fals: «\(-20>-2\)», «el major dels negatius és \(-1\)», «entre \(-3\) i \(3\) hi ha 5 enters». f) Quin enter està 6 unitats a la dreta de \(-4\)?", r"e) Verdadero o falso: «\(-20>-2\)», «el mayor de los negativos es \(-1\)», «entre \(-3\) y \(3\) hay 5 enteros». f) ¿Qué entero está 6 unidades a la derecha de \(-4\)?", r"e) True or false: “\(-20>-2\)”, “the largest negative is \(-1\)”, “there are 5 integers between \(-3\) and \(3\)”. f) Which integer is 6 units to the right of \(-4\)?"))],
  r'\[\text{a)}\ -9<-6<-2<0<3<7\qquad \text{b)}\ -10<-1,\ \ 4>-4\]'
  + r'\[\text{c)}\ 12>0>-5>-15>-51\qquad \text{d)}\ -10,\ -9,\ -8\]'
  + P(r"e) F, V, V (\(-2,-1,0,1,2\)). &nbsp; f) \(2\).", r"e) F, V, V (\(-2,-1,0,1,2\)). &nbsp; f) \(2\).", r"e) F, T, T (\(-2,-1,0,1,2\)). &nbsp; f) \(2\)."))

# ============================================================ 3.3
def abs_arcs(a):
    def f(x):
        s = ''
        for v, cls in ((a, 'ab-a'), (-a, 'ab-op')):
            s += f'<path class="{cls}" fill="none" d="M{x(0):.1f} 36 Q {(x(0) + x(v)) / 2:.1f} -14 {x(v):.1f} 36"/>'
            s += f'<text class="ab-t {cls}t" x="{(x(0) + x(v)) / 2:.1f}" y="24" text-anchor="middle">{abs(a)}</text>'
        return s
    return f
s3 = box('def', L('Valor absolut', 'Valor absoluto', 'Absolute value'),
  P(r"El <strong>valor absolut</strong> d'un enter és la <strong>distància</strong> que hi ha entre aquest nombre i el zero en la recta. S'escriu entre dues barres verticals: \(|a|\).",
    r"El <strong>valor absoluto</strong> de un entero es la <strong>distancia</strong> que hay entre ese número y el cero en la recta. Se escribe entre dos barras verticales: \(|a|\).",
    r"The <strong>absolute value</strong> of an integer is its <strong>distance</strong> from zero on the number line. It is written between two vertical bars: \(|a|\).")
  + r'\[|-5|=5\qquad |+5|=5\qquad |0|=0\qquad |-23|=23\]'
  + nline(-7, 7, [-5, 5], abs_arcs(5))
  + ul(L(r"Com que és una distància, el valor absolut <strong>mai no és negatiu</strong>.", r"Como es una distancia, el valor absoluto <strong>nunca es negativo</strong>.", r"Since it's a distance, the absolute value is <strong>never negative</strong>."),
       L(r"A la pràctica, el valor absolut és el nombre <strong>sense el signe</strong>.", r"En la práctica, el valor absoluto es el número <strong>sin el signo</strong>.", r"In practice, the absolute value is the number <strong>without its sign</strong>.")))
s3 += box('def', L('Oposat d\'un enter', 'Opuesto de un entero', 'Opposite of an integer'),
  P(r"L'<strong>oposat</strong> d'un enter és el nombre que està a la <strong>mateixa distància</strong> del zero, però a l'<strong>altre costat</strong>. Té el mateix valor absolut i el signe contrari. S'escriu \(\text{op}(a)\) o \(-a\):",
    r"El <strong>opuesto</strong> de un entero es el número que está a la <strong>misma distancia</strong> del cero, pero al <strong>otro lado</strong>. Tiene el mismo valor absoluto y el signo contrario. Se escribe \(\text{op}(a)\) o \(-a\):",
    r"The <strong>opposite</strong> of an integer is the number at the <strong>same distance</strong> from zero but on the <strong>other side</strong>. It has the same absolute value and the opposite sign. It is written \(\text{op}(a)\) or \(-a\):")
  + r'\[\text{op}(-8)=8\qquad \text{op}(4)=-4\qquad \text{op}(0)=0\qquad -(-3)=3\]'
  + ul(L(r"Per a calcular l'oposat, <strong>canviem el signe</strong>.", r"Para calcular el opuesto, <strong>cambiamos el signo</strong>.", r"To find the opposite, <strong>change the sign</strong>."),
       L(r"L'oposat de l'oposat és el mateix nombre: \(\ \text{op}(\text{op}(-7))=\text{op}(7)=-7\).", r"El opuesto del opuesto es el mismo número: \(\ \text{op}(\text{op}(-7))=\text{op}(7)=-7\).", r"The opposite of the opposite is the number itself: \(\ \text{op}(\text{op}(-7))=\text{op}(7)=-7\)."),
       L(r"Un nombre i el seu oposat <strong>sumen zero</strong>: \(\ 5+(-5)=0\).", r"Un número y su opuesto <strong>suman cero</strong>: \(\ 5+(-5)=0\).", r"A number and its opposite <strong>add up to zero</strong>: \(\ 5+(-5)=0\)."),
       L(r"Entre dos oposats hi ha el <strong>doble</strong> del seu valor absolut: entre \(-5\) i \(5\) hi ha 10 unitats.", r"Entre dos opuestos hay el <strong>doble</strong> de su valor absoluto: entre \(-5\) y \(5\) hay 10 unidades.", r"Two opposites are <strong>twice</strong> their absolute value apart: \(-5\) and \(5\) are 10 units apart."))
  + note(r"Compte: \(|-4|=4\), però \(\text{op}(4)=-4\). El valor absolut sempre dona un nombre positiu (o zero); l'oposat pot ser positiu o negatiu.",
         r"Cuidado: \(|-4|=4\), pero \(\text{op}(4)=-4\). El valor absoluto siempre da un número positivo (o cero); el opuesto puede ser positivo o negativo.",
         r"Careful: \(|-4|=4\), but \(\text{op}(4)=-4\). The absolute value is always positive (or zero); the opposite can be positive or negative.", '⚠️')
  + f'''<div class="widget" id="w-abs">
  <div class="wt">↔ {L("Valor absolut i oposat", "Valor absoluto y opuesto", "Absolute value and opposite")}</div>
  <div class="wrow">{nin("a", "Nombre enter", "Número entero", "Integer", "-5", "m")}</div>
  {quick([("-5", "−5"), ("8", "8"), ("-23", "−23"), ("0", "0"), ("-100", "−100"), ("18", "18")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('abs', 'Entrena: valor absolut i oposat', 'Entrena: valor absoluto y opuesto', 'Train: absolute value and opposite'))
s3 += level(1, 1,
  prob(L(r"Calcula: \(\ |-12|,\ \ |9|,\ \ \text{op}(-6),\ \ \text{op}(15)\).", r"Calcula: \(\ |-12|,\ \ |9|,\ \ \text{op}(-6),\ \ \text{op}(15)\).", r"Work out: \(\ |-12|,\ \ |9|,\ \ \text{op}(-6),\ \ \text{op}(15)\)."),
       P(r"Per al valor absolut, traiem el signe; per a l'oposat, el canviem:", r"Para el valor absoluto, quitamos el signo; para el opuesto, lo cambiamos:", r"For the absolute value, drop the sign; for the opposite, change it:"),
       r'\[|-12|=12\qquad |9|=9\qquad \text{op}(-6)=6\qquad \text{op}(15)=-15\]'),
  prob(L(r"Dos nombres oposats estan a 36 unitats l'un de l'altre. Quins nombres són?", r"Dos números opuestos están a 36 unidades el uno del otro. ¿Qué números son?", r"Two opposite numbers are 36 units apart. Which numbers are they?"),
       P(r"Cadascun està a la mateixa distància del zero, és a dir, a la meitat: \(36:2=18\).", r"Cada uno está a la misma distancia del cero, es decir, a la mitad: \(36:2=18\).", r"Each one is the same distance from zero, that is, half of it: \(36:2=18\)."),
       r'\[\boxed{18\ \text{\tri{i}{y}{and}}\ -18}\]'))
s3 += level(2, 3,
  prob(L(r"Ordena de menor a major fent abans els càlculs: \(\ \text{op}(3),\ \ |-5|,\ \ -4,\ \ |2|,\ \ \text{op}(-1)\).", r"Ordena de menor a mayor haciendo antes los cálculos: \(\ \text{op}(3),\ \ |-5|,\ \ -4,\ \ |2|,\ \ \text{op}(-1)\).", r"Order from smallest to largest, working each one out first: \(\ \text{op}(3),\ \ |-5|,\ \ -4,\ \ |2|,\ \ \text{op}(-1)\)."),
       r'\[\text{op}(3)=-3\qquad |-5|=5\qquad -4\qquad |2|=2\qquad \text{op}(-1)=1\]',
       r'\[\boxed{-4<\text{op}(3)<\text{op}(-1)<|2|<|-5|}\]'),
  prob(L(r"Compara: \(\ \text{a)}\ |-4|\ \square\ \text{op}(2)\qquad \text{b)}\ \text{op}(\text{op}(-1))\ \square\ 0\qquad \text{c)}\ -8\ \square\ \text{op}(8)\)", r"Compara: \(\ \text{a)}\ |-4|\ \square\ \text{op}(2)\qquad \text{b)}\ \text{op}(\text{op}(-1))\ \square\ 0\qquad \text{c)}\ -8\ \square\ \text{op}(8)\)", r"Compare: \(\ \text{a)}\ |-4|\ \square\ \text{op}(2)\qquad \text{b)}\ \text{op}(\text{op}(-1))\ \square\ 0\qquad \text{c)}\ -8\ \square\ \text{op}(8)\)"),
       r'\[\text{a)}\ 4>-2\qquad \text{b)}\ -1<0\qquad \text{c)}\ -8=-8\]'))
s3 += level(3, 5,
  prob(L(r"Troba tots els enters que completen: \(\ \text{a)}\ |\ \square\ |=7\qquad \text{b)}\ \text{op}(|\ \square\ |)=-2\qquad \text{c)}\ |\ \square\ |=\text{op}(5)\)", r"Encuentra todos los enteros que completan: \(\ \text{a)}\ |\ \square\ |=7\qquad \text{b)}\ \text{op}(|\ \square\ |)=-2\qquad \text{c)}\ |\ \square\ |=\text{op}(5)\)", r"Find every integer that fits: \(\ \text{a)}\ |\ \square\ |=7\qquad \text{b)}\ \text{op}(|\ \square\ |)=-2\qquad \text{c)}\ |\ \square\ |=\text{op}(5)\)"),
       P(r"a) Hi ha dos nombres a 7 unitats del zero: \(\boxed{7\text{ i }-7}\).", r"a) Hay dos números a 7 unidades del cero: \(\boxed{7\text{ y }-7}\).", r"a) Two numbers are 7 units from zero: \(\boxed{7\text{ and }-7}\)."),
       P(r"b) Si l'oposat de \(|\square|\) és \(-2\), aleshores \(|\square|=2\): \(\boxed{2\text{ i }-2}\).", r"b) Si el opuesto de \(|\square|\) es \(-2\), entonces \(|\square|=2\): \(\boxed{2\text{ y }-2}\).", r"b) If the opposite of \(|\square|\) is \(-2\), then \(|\square|=2\): \(\boxed{2\text{ and }-2}\)."),
       P(r"c) \(\text{op}(5)=-5\), i un valor absolut no pot ser negatiu: <strong>no hi ha cap</strong> nombre.", r"c) \(\text{op}(5)=-5\), y un valor absoluto no puede ser negativo: <strong>no hay ningún</strong> número.", r"c) \(\text{op}(5)=-5\), and an absolute value can't be negative: <strong>there is no</strong> such number.")))
s3 += practice([
  ('★', L(r"a) Calcula \(|-31|\), \(|0|\), \(\text{op}(-100)\) i \(\text{op}(7)\). b) Dos oposats estan a 50 unitats. Quins són?", r"a) Calcula \(|-31|\), \(|0|\), \(\text{op}(-100)\) y \(\text{op}(7)\). b) Dos opuestos están a 50 unidades. ¿Cuáles son?", r"a) Work out \(|-31|\), \(|0|\), \(\text{op}(-100)\) and \(\text{op}(7)\). b) Two opposites are 50 units apart. Which are they?")),
  ('★★', L(r"c) Ordena de menor a major: \(\ 3,\ \text{op}(4),\ |-6|,\ \text{op}(5),\ -2,\ |-2|\). d) Compara \(\ |-3|\ \square\ 3\ \) i \(\ \text{op}(-2)\ \square\ -1\).", r"c) Ordena de menor a mayor: \(\ 3,\ \text{op}(4),\ |-6|,\ \text{op}(5),\ -2,\ |-2|\). d) Compara \(\ |-3|\ \square\ 3\ \) y \(\ \text{op}(-2)\ \square\ -1\).", r"c) Order from smallest to largest: \(\ 3,\ \text{op}(4),\ |-6|,\ \text{op}(5),\ -2,\ |-2|\). d) Compare \(\ |-3|\ \square\ 3\ \) and \(\ \text{op}(-2)\ \square\ -1\).")),
  ('★★★', L(r"e) Quins enters tenen valor absolut menor que 4? f) Completa: \(\ \text{op}(\text{op}(\square))=-7\).", r"e) ¿Qué enteros tienen valor absoluto menor que 4? f) Completa: \(\ \text{op}(\text{op}(\square))=-7\).", r"e) Which integers have an absolute value less than 4? f) Fill in: \(\ \text{op}(\text{op}(\square))=-7\)."))],
  P(r"a) \(31,\ 0,\ 100,\ -7\). &nbsp; b) \(25\) i \(-25\).", r"a) \(31,\ 0,\ 100,\ -7\). &nbsp; b) \(25\) y \(-25\).", r"a) \(31,\ 0,\ 100,\ -7\). &nbsp; b) \(25\) and \(-25\).")
  + P(r"c) \(\text{op}(5)=-5<\text{op}(4)=-4<-2<|-2|=2<3<|-6|=6\). &nbsp; d) \(=\); \(\ 2>-1\).", r"c) \(\text{op}(5)=-5<\text{op}(4)=-4<-2<|-2|=2<3<|-6|=6\). &nbsp; d) \(=\); \(\ 2>-1\).", r"c) \(\text{op}(5)=-5<\text{op}(4)=-4<-2<|-2|=2<3<|-6|=6\). &nbsp; d) \(=\); \(\ 2>-1\).")
  + P(r"e) \(-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 3\). &nbsp; f) \(-7\).", r"e) \(-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 3\). &nbsp; f) \(-7\).", r"e) \(-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 3\). &nbsp; f) \(-7\)."))

# ============================================================ 3.4
def jump(a, b):
    def f(x):
        x1, x2 = x(a), x(a + b); d = 1 if b > 0 else -1
        return (f'<path class="ad-arr" fill="none" d="M{x1:.1f} 34 Q {(x1 + x2) / 2:.1f} -6 {x2 - 4 * d:.1f} 30"/>'
                f'<path class="ad-hd" d="M{x2:.1f} 32 l{-9 * d} -5 l0 10 z"/>'
                f'<text class="ad-t" x="{(x1 + x2) / 2:.1f}" y="12" text-anchor="middle">{("+" if b > 0 else "−") + str(abs(b))}</text>')
    return f
s4 = box('def', L('Suma d\'enters', 'Suma de enteros', 'Adding integers'),
  P(r"Pensem en diners: els positius són el que <strong>tinc</strong> (o guanye) i els negatius, el que <strong>dec</strong> (o perd). Hi ha dos casos:",
    r"Pensemos en dinero: los positivos son lo que <strong>tengo</strong> (o gano) y los negativos, lo que <strong>debo</strong> (o pierdo). Hay dos casos:",
    r"Think of money: positives are what I <strong>have</strong> (or win) and negatives what I <strong>owe</strong> (or lose). There are two cases:")
  + '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"<strong>Mateix signe:</strong> se <strong>sumen</strong> els valors absoluts i es posa el <strong>signe comú</strong>.<br>\(3+5=8\) (guanye 3 i guanye 5: guanye 8) &nbsp; \(-3-5=-8\) (dec 3 i dec 5: dec 8)",
        r"<strong>Mismo signo:</strong> se <strong>suman</strong> los valores absolutos y se pone el <strong>signo común</strong>.<br>\(3+5=8\) (gano 3 y gano 5: gano 8) &nbsp; \(-3-5=-8\) (debo 3 y debo 5: debo 8)",
        r"<strong>Same sign:</strong> <strong>add</strong> the absolute values and keep the <strong>common sign</strong>.<br>\(3+5=8\) (win 3 and win 5: win 8) &nbsp; \(-3-5=-8\) (owe 3 and owe 5: owe 8)"),
      L(r"<strong>Signes diferents:</strong> se <strong>resten</strong> els valors absoluts (el gran menys el xicotet) i es posa el signe del que té <strong>major valor absolut</strong>.<br>\(-7+4=-3\) (dec 7 i en pague 4: encara en dec 3) &nbsp; \(-2+6=4\)",
        r"<strong>Signos distintos:</strong> se <strong>restan</strong> los valores absolutos (el grande menos el pequeño) y se pone el signo del que tiene <strong>mayor valor absoluto</strong>.<br>\(-7+4=-3\) (debo 7 y pago 4: aún debo 3) &nbsp; \(-2+6=4\)",
        r"<strong>Different signs:</strong> <strong>subtract</strong> the absolute values (big minus small) and take the sign of the one with the <strong>larger absolute value</strong>.<br>\(-7+4=-3\) (I owe 7 and pay back 4: I still owe 3) &nbsp; \(-2+6=4\)")]) + '</ol>'
  + P(r"En la recta, sumar un <strong>positiu</strong> és moure's cap a la <strong>dreta</strong> i sumar un <strong>negatiu</strong>, cap a l'<strong>esquerra</strong>. Per exemple, \(-2+6=4\):",
      r"En la recta, sumar un <strong>positivo</strong> es moverse hacia la <strong>derecha</strong> y sumar un <strong>negativo</strong>, hacia la <strong>izquierda</strong>. Por ejemplo, \(-2+6=4\):",
      r"On the number line, adding a <strong>positive</strong> means moving <strong>right</strong> and adding a <strong>negative</strong> means moving <strong>left</strong>. For example, \(-2+6=4\):")
  + nline(-4, 6, [-2, 4], jump(-2, 6), h=78))
s4 += box('def', L('Resta d\'enters', 'Resta de enteros', 'Subtracting integers'),
  P(r"<strong>Restar</strong> un enter és el mateix que <strong>sumar el seu oposat</strong>:", r"<strong>Restar</strong> un entero es lo mismo que <strong>sumar su opuesto</strong>:", r"<strong>Subtracting</strong> an integer is the same as <strong>adding its opposite</strong>:")
  + r'\[a-b=a+\text{op}(b)\qquad\qquad 5-7=5+(-7)=-2\qquad\qquad 4-(-6)=4+6=10\]'
  + P(r"Per això, quan escrivim \(5-7\) podem llegir-ho com «tinc 5 i en dec 7»: el resultat és \(-2\). Ara ja podem restar un nombre més gran d'un de més xicotet!",
      r"Por eso, cuando escribimos \(5-7\) podemos leerlo como «tengo 5 y debo 7»: el resultado es \(-2\). ¡Ahora ya podemos restar un número mayor de uno más pequeño!",
      r"That's why we can read \(5-7\) as “I have 5 and owe 7”: the result is \(-2\). Now we can subtract a bigger number from a smaller one!"))
s4 += box('prop', L('Sumes i restes de diversos termes', 'Sumas y restas de varios términos', 'Sums with several terms'),
  P(r"Hi ha dues maneres de fer-ho:", r"Hay dos maneras de hacerlo:", r"There are two ways:")
  + ul(L(r"<strong>D'esquerra a dreta</strong>, de dos en dos: \(\ 5-9+8-2=-4+8-2=4-2=2\)", r"<strong>De izquierda a derecha</strong>, de dos en dos: \(\ 5-9+8-2=-4+8-2=4-2=2\)", r"<strong>Left to right</strong>, two at a time: \(\ 5-9+8-2=-4+8-2=4-2=2\)"),
       L(r"<strong>Agrupant</strong> positius i negatius: \(\ 5-9+8-2=(5+8)-(9+2)=13-11=2\)", r"<strong>Agrupando</strong> positivos y negativos: \(\ 5-9+8-2=(5+8)-(9+2)=13-11=2\)", r"<strong>Grouping</strong> positives and negatives: \(\ 5-9+8-2=(5+8)-(9+2)=13-11=2\)"))
  + note(r"La segona manera és molt pràctica quan hi ha molts termes: és com sumar tot el que guanyes, sumar tot el que perds i fer el balanç.",
         r"La segunda manera es muy práctica cuando hay muchos términos: es como sumar todo lo que ganas, sumar todo lo que pierdes y hacer el balance.",
         r"The second way is very handy when there are many terms: it's like adding up everything you win, everything you lose, and finding the balance.")
  + f'''<div class="widget" id="w-add">
  <div class="wt">➕ {L("Sumes i restes en la recta", "Sumas y restas en la recta", "Adding and subtracting on the number line")}</div>
  <div class="wrow">{nin("a", "Partim de", "Partimos de", "Start at", "-2")}{seg([("+", "+"), ("-", "−")], "+")}{nin("b", "Nombre", "Número", "Number", "6")}</div>
  {quick([("-2|+|6", "−2 + 6"), ("5|-|7", "5 − 7"), ("-8|-|9", "−8 − 9"), ("-3|+|-4", "−3 + (−4)"), ("4|-|-6", "4 − (−6)"), ("-5|+|5", "−5 + 5")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('add', 'Entrena: sumes i restes', 'Entrena: sumas y restas', 'Train: addition and subtraction'))
s4 += level(1, 1,
  prob(L(r"Calcula: \(\ \text{a)}\ -8+3\qquad \text{b)}\ -4-6\qquad \text{c)}\ 7-12\)", r"Calcula: \(\ \text{a)}\ -8+3\qquad \text{b)}\ -4-6\qquad \text{c)}\ 7-12\)", r"Work out: \(\ \text{a)}\ -8+3\qquad \text{b)}\ -4-6\qquad \text{c)}\ 7-12\)"),
       P(r"a) Signes diferents: \(8-3=5\), amb el signe del 8 (negatiu).", r"a) Signos distintos: \(8-3=5\), con el signo del 8 (negativo).", r"a) Different signs: \(8-3=5\), with the sign of 8 (negative).") + r'\[-8+3=\boxed{-5}\]',
       P(r"b) Mateix signe: \(4+6=10\), amb el signe comú (negatiu).", r"b) Mismo signo: \(4+6=10\), con el signo común (negativo).", r"b) Same sign: \(4+6=10\), with the common sign (negative).") + r'\[-4-6=\boxed{-10}\]',
       P(r"c) Signes diferents: \(12-7=5\), amb el signe del 12 (negatiu).", r"c) Signos distintos: \(12-7=5\), con el signo del 12 (negativo).", r"c) Different signs: \(12-7=5\), with the sign of 12 (negative).") + r'\[7-12=\boxed{-5}\]'),
  prob(L(r"Calcula \(\ -10+8+6\ \) d'esquerra a dreta.", r"Calcula \(\ -10+8+6\ \) de izquierda a derecha.", r"Work out \(\ -10+8+6\ \) from left to right."),
       r'\[\underbrace{-10+8}_{-2}+6=-2+6=\boxed{4}\]'))
s4 += level(2, 3,
  prob(L(r"Calcula de les dues maneres: \(\ 10-14+6-3+2-9\).", r"Calcula de las dos maneras: \(\ 10-14+6-3+2-9\).", r"Work it out both ways: \(\ 10-14+6-3+2-9\)."),
       P(r"<strong>D'esquerra a dreta:</strong>", r"<strong>De izquierda a derecha:</strong>", r"<strong>Left to right:</strong>") + r'\[10-14+6-3+2-9=-4+6-3+2-9=2-3+2-9=-1+2-9=1-9=\boxed{-8}\]',
       P(r"<strong>Agrupant:</strong>", r"<strong>Agrupando:</strong>", r"<strong>Grouping:</strong>") + r'\[(10+6+2)-(14+3+9)=18-26=\boxed{-8}\]'))
s4 += level(3, 4,
  prob(L(r"Quin nombre falta? \(\ \text{a)}\ -3+\square=5\qquad \text{b)}\ \square-7=-2\qquad \text{c)}\ 4+\square=-6\)", r"¿Qué número falta? \(\ \text{a)}\ -3+\square=5\qquad \text{b)}\ \square-7=-2\qquad \text{c)}\ 4+\square=-6\)", r"Which number is missing? \(\ \text{a)}\ -3+\square=5\qquad \text{b)}\ \square-7=-2\qquad \text{c)}\ 4+\square=-6\)"),
       P(r"a) Per a anar de \(-3\) a \(5\) en la recta, cal avançar 8 cap a la dreta: \(\square=\boxed{8}\).", r"a) Para ir de \(-3\) a \(5\) en la recta, hay que avanzar 8 hacia la derecha: \(\square=\boxed{8}\).", r"a) To get from \(-3\) to \(5\) on the line, move 8 to the right: \(\square=\boxed{8}\)."),
       P(r"b) Un nombre que, si li llevem 7, dona \(-2\): \(-2+7=\boxed{5}\).", r"b) Un número que, si le quitamos 7, da \(-2\): \(-2+7=\boxed{5}\).", r"b) A number that gives \(-2\) when you take 7 away: \(-2+7=\boxed{5}\)."),
       P(r"c) Per a anar de \(4\) a \(-6\) cal retrocedir 10: \(\square=\boxed{-10}\).", r"c) Para ir de \(4\) a \(-6\) hay que retroceder 10: \(\square=\boxed{-10}\).", r"c) To get from \(4\) to \(-6\) move 10 back: \(\square=\boxed{-10}\).")))
PR4a, PR4b, PR4c = ['5-7', '-8-9', '-3+7'], ['10-3-5', '-4-3-2', '-13+6+4'], ['5+7-2-4', '-24+15+13-8']
s4 += practice([
  ('★', L(r"a) \(5-7\) &nbsp; b) \(-8-9\) &nbsp; c) \(-3+7\)", r"a) \(5-7\) &nbsp; b) \(-8-9\) &nbsp; c) \(-3+7\)", r"a) \(5-7\) &nbsp; b) \(-8-9\) &nbsp; c) \(-3+7\)")),
  ('★★', L(r"d) \(10-3-5\) &nbsp; e) \(-4-3-2\) &nbsp; f) \(-13+6+4\)", r"d) \(10-3-5\) &nbsp; e) \(-4-3-2\) &nbsp; f) \(-13+6+4\)", r"d) \(10-3-5\) &nbsp; e) \(-4-3-2\) &nbsp; f) \(-13+6+4\)")),
  ('★★★', L(r"g) \(5+7-2-4\) &nbsp; h) \(-24+15+13-8\) &nbsp; i) Completa: \(\ \square-9=-15\)", r"g) \(5+7-2-4\) &nbsp; h) \(-24+15+13-8\) &nbsp; i) Completa: \(\ \square-9=-15\)", r"g) \(5+7-2-4\) &nbsp; h) \(-24+15+13-8\) &nbsp; i) Fill in: \(\ \square-9=-15\)"))],
  r'\[' + r'\qquad '.join(r'\text{%s)}\ %s' % (k, eq(e)) for k, e in zip('abc', PR4a)) + r'\]'
  + r'\[' + r'\qquad '.join(r'\text{%s)}\ %s' % (k, eq(e)) for k, e in zip('def', PR4b)) + r'\]'
  + r'\[\text{g)}\ (5+7)-(2+4)=6\qquad \text{h)}\ (15+13)-(24+8)=-4\qquad \text{i)}\ -6\]')
assert ev('5+7-2-4') == 6 and ev('-24+15+13-8') == -4

# ============================================================ 3.5
s5 = box('def', L('Com s\'eliminen els parèntesis', 'Cómo se eliminan los paréntesis', 'How to remove brackets'),
  P(r"Moltes vegades els enters s'escriuen entre parèntesis per a no ajuntar dos signes: \((+7)+(-4)\). Per a traure el parèntesi, mirem el signe de <strong>fora</strong> i el de <strong>dins</strong>, i fem servir la <strong>regla dels signes</strong>:",
    r"Muchas veces los enteros se escriben entre paréntesis para no juntar dos signos: \((+7)+(-4)\). Para quitar el paréntesis, miramos el signo de <strong>fuera</strong> y el de <strong>dentro</strong>, y usamos la <strong>regla de los signos</strong>:",
    r"Integers are often written in brackets so that two signs don't touch: \((+7)+(-4)\). To remove the brackets, look at the sign <strong>outside</strong> and the sign <strong>inside</strong>, and use the <strong>sign rule</strong>:")
  + '<div class="sgrule"><div class="pos">\\(+\\,(+\\ \\to\\ +\\)</div><div class="neg">\\(+\\,(-\\ \\to\\ -\\)</div><div class="neg">\\(-\\,(+\\ \\to\\ -\\)</div><div class="pos">\\(-\\,(-\\ \\to\\ +\\)</div></div>'
  + P(r"Signes <strong>iguals</strong> donen \(+\) i signes <strong>diferents</strong> donen \(-\). Si no hi ha signe davant del parèntesi (al principi), és com si hi haguera un \(+\).",
      r"Signos <strong>iguales</strong> dan \(+\) y signos <strong>distintos</strong> dan \(-\). Si no hay signo delante del paréntesis (al principio), es como si hubiera un \(+\).",
      r"<strong>Same</strong> signs give \(+\) and <strong>different</strong> signs give \(-\). If there's no sign before the bracket (at the start), it counts as \(+\).")
  + r'\[(+7)+(-4)=7-4=3\qquad\qquad 3-(-1)=3+1=4\]'
  + r'\[-(+4)+(-8)-(-6)=-4-8+6=6-12=-6\]'
  + note(r"«Restar un deute és com guanyar diners»: si et perdonen un deute de 6 €, és com si te'n donaren 6. Per això \(-(-6)=+6\).",
         r"«Restar una deuda es como ganar dinero»: si te perdonan una deuda de 6 €, es como si te dieran 6. Por eso \(-(-6)=+6\).",
         r"“Taking away a debt is like gaining money”: if someone cancels a €6 debt you owe, it's as if they gave you €6. That's why \(-(-6)=+6\).", '💶')
  + f'''<div class="widget" id="w-par">
  <div class="wt">🧹 {L("Lleva els parèntesis", "Quita los paréntesis", "Remove the brackets")}</div>
  <div class="wrow"><label>{L("Expressió", "Expresión", "Expression")} <input class="tin w" type="text" value="−(+4) + (−8) − (−6) + 4 − 1" autocomplete="off" spellcheck="false" aria-label="expressió"></label></div>
  <div class="quick"><span class="ql">⚡</span>{"".join(f'<button type="button" data-e="{e}">{e}</button>' for e in ["(−6) + (−3)", "(+7) + (−4)", "3 − (−1)", "−(−5) + 3", "(−2) − (+3) + (−6)", "−(−3) + (−1) − (+3) − (−8)", "12 − 25 + 3 − 8 − (−6)"])}</div>
  <div class="pchips"></div>
  <div class="info" aria-live="polite"></div>
</div>
''')
s5 += box('prop', L('Parèntesis amb operacions a dins i claudàtors', 'Paréntesis con operaciones dentro y corchetes', 'Brackets with operations inside, and square brackets'),
  P(r"Si dins del parèntesi hi ha una operació, tenim dues opcions:", r"Si dentro del paréntesis hay una operación, tenemos dos opciones:", r"If there's an operation inside the brackets, there are two options:")
  + ul(L(r"<strong>Primer, l'operació de dins:</strong> \(\ 15-(2-9)=15-(-7)=15+7=22\)", r"<strong>Primero, la operación de dentro:</strong> \(\ 15-(2-9)=15-(-7)=15+7=22\)", r"<strong>Work out the inside first:</strong> \(\ 15-(2-9)=15-(-7)=15+7=22\)"),
       L(r"<strong>Traure el parèntesi:</strong> si davant hi ha un \(-\), <strong>canviem el signe de tots els termes</strong> de dins: \(\ 15-(2-9)=15-2+9=22\)", r"<strong>Quitar el paréntesis:</strong> si delante hay un \(-\), <strong>cambiamos el signo de todos los términos</strong> de dentro: \(\ 15-(2-9)=15-2+9=22\)", r"<strong>Remove the brackets:</strong> if there's a \(-\) in front, <strong>change the sign of every term</strong> inside: \(\ 15-(2-9)=15-2+9=22\)"))
  + P(r"Quan hi ha parèntesis dins d'altres parèntesis fem servir <strong>claudàtors</strong> \([\ ]\) i comencem <strong>des de dins cap a fora</strong>:",
      r"Cuando hay paréntesis dentro de otros paréntesis usamos <strong>corchetes</strong> \([\ ]\) y empezamos <strong>desde dentro hacia fuera</strong>:",
      r"When there are brackets inside brackets we use <strong>square brackets</strong> \([\ ]\) and work <strong>from the inside out</strong>:")
  + r'\[15-[2-(6-10)]=15-[2-(-4)]=15-[2+4]=15-6=9\]'
  + note(r"L'error més freqüent és oblidar-se de canviar el signe del <strong>segon</strong> terme: \(\ 6-(9-7)\) no és \(6-9-7\), sinó \(6-9+7=4\).",
         r"El error más frecuente es olvidarse de cambiar el signo del <strong>segundo</strong> término: \(\ 6-(9-7)\) no es \(6-9-7\), sino \(6-9+7=4\).",
         r"The most common mistake is forgetting to change the sign of the <strong>second</strong> term: \(\ 6-(9-7)\) is not \(6-9-7\) but \(6-9+7=4\).", '⚠️')
  + hier(['15-[2-(6-10)]', '6-(9-7)', '(8-12)-(2-5)', '-(6-2)-(7-9)', '(-7)-[3-(4-9)]', '2-[6-(-1-21)]'])
  + drill('par', 'Entrena: lleva els parèntesis', 'Entrena: quita los paréntesis', 'Train: remove the brackets'))
s5 += level(1, 1,
  prob(L(r"Calcula traient els parèntesis: \(\ (-8)+(-3)-(-17)+(+1)\)", r"Calcula quitando los paréntesis: \(\ (-8)+(-3)-(-17)+(+1)\)", r"Work out by removing the brackets: \(\ (-8)+(-3)-(-17)+(+1)\)"),
       P(r"Apliquem la regla a cada parèntesi: \(+(-\to-\), \(\ +(-\to-\), \(\ -(-\to+\), \(\ +(+\to+\).", r"Aplicamos la regla a cada paréntesis: \(+(-\to-\), \(\ +(-\to-\), \(\ -(-\to+\), \(\ +(+\to+\).", r"Apply the rule to each bracket: \(+(-\to-\), \(\ +(-\to-\), \(\ -(-\to+\), \(\ +(+\to+\)."),
       r'\[-8-3+17+1=(17+1)-(8+3)=18-11=\boxed{7}\]'),
  prob(L(r"Calcula: \(\ 11-(-6+3)\)", r"Calcula: \(\ 11-(-6+3)\)", r"Work out: \(\ 11-(-6+3)\)"),
       r'\[11-(-6+3)=11-(-3)=11+3=\boxed{14}\]',
       P(r"O bé, canviant els signes de dins: \(\ 11+6-3=\boxed{14}\).", r"O bien, cambiando los signos de dentro: \(\ 11+6-3=\boxed{14}\).", r"Or, changing the signs inside: \(\ 11+6-3=\boxed{14}\).")))
s5 += level(2, 3,
  prob(L(r"Calcula: \(\ (10-7)-(-2-6)\)", r"Calcula: \(\ (10-7)-(-2-6)\)", r"Work out: \(\ (10-7)-(-2-6)\)"),
       r'\[(10-7)-(-2-6)=3-(-8)=3+8=\boxed{11}\]'),
  prob(L(r"Calcula: \(\ -(-7-1)-(2-10)\)", r"Calcula: \(\ -(-7-1)-(2-10)\)", r"Work out: \(\ -(-7-1)-(2-10)\)"),
       r'\[-(-8)-(-8)=8+8=\boxed{16}\]'))
s5 += level(3, 5,
  prob(L(r"Calcula: \(\ (2-10)+[5-(8+2)]\)", r"Calcula: \(\ (2-10)+[5-(8+2)]\)", r"Work out: \(\ (2-10)+[5-(8+2)]\)"),
       P(r"Primer els parèntesis de dins, després el claudàtor:", r"Primero los paréntesis de dentro, después el corchete:", r"Inner brackets first, then the square bracket:"),
       r'\[(2-10)+[5-(8+2)]=-8+[5-10]=-8+(-5)=-8-5=\boxed{-13}\]'),
  prob(L(r"Calcula: \(\ [10-(-2)]-[5-(+12)]\)", r"Calcula: \(\ [10-(-2)]-[5-(+12)]\)", r"Work out: \(\ [10-(-2)]-[5-(+12)]\)"),
       r'\[[10+2]-[5-12]=12-(-7)=12+7=\boxed{19}\]'))
PR5 = [('a', '-15-(-3)+7'), ('b', '-(-6)+(-1)-7+(-3)'), ('c', '-6-(2-7)'), ('d', '(17-12)-(-7-8)'), ('e', '12-[7-(2-10)]'), ('f', '-1+[-5-(2-13)]')]
s5 += practice([
  ('★', L(r"a) \(-15-(-3)+7\) &nbsp; b) \(-(-6)+(-1)-7+(-3)\)", r"a) \(-15-(-3)+7\) &nbsp; b) \(-(-6)+(-1)-7+(-3)\)", r"a) \(-15-(-3)+7\) &nbsp; b) \(-(-6)+(-1)-7+(-3)\)")),
  ('★★', L(r"c) \(-6-(2-7)\) &nbsp; d) \((17-12)-(-7-8)\)", r"c) \(-6-(2-7)\) &nbsp; d) \((17-12)-(-7-8)\)", r"c) \(-6-(2-7)\) &nbsp; d) \((17-12)-(-7-8)\)")),
  ('★★★', L(r"e) \(12-[7-(2-10)]\) &nbsp; f) \(-1+[-5-(2-13)]\)", r"e) \(12-[7-(2-10)]\) &nbsp; f) \(-1+[-5-(2-13)]\)", r"e) \(12-[7-(2-10)]\) &nbsp; f) \(-1+[-5-(2-13)]\)"))],
  r'\[\text{a)}\ -15+3+7=-5\qquad \text{b)}\ 6-1-7-3=-5\]'
  + r'\[\text{c)}\ -6-(-5)=-6+5=-1\qquad \text{d)}\ 5-(-15)=20\]'
  + r'\[\text{e)}\ 12-[7-(-8)]=12-15=-3\qquad \text{f)}\ -1+[-5-(-11)]=-1+6=5\]')
assert [ev(e) for _, e in PR5] == [-5, -5, -1, 20, -3, 5]

# ============================================================ 3.6
SGT = ('<div class="tbl-wrap"><table class="data sgtab"><thead><tr><th class="sop">·</th><th>+</th><th>−</th></tr></thead><tbody>'
       '<tr><th>+</th><td class="pos" data-c="pp">+</td><td class="neg" data-c="pn">−</td></tr>'
       '<tr><th>−</th><td class="neg" data-c="np">−</td><td class="pos" data-c="nn">+</td></tr></tbody></table></div>')
s6 = box('def', L('Multiplicació i divisió d\'enters', 'Multiplicación y división de enteros', 'Multiplying and dividing integers'),
  P(r"Per a multiplicar o dividir dos enters:", r"Para multiplicar o dividir dos enteros:", r"To multiply or divide two integers:")
  + '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"Multipliquem (o dividim) els <strong>valors absoluts</strong>.", r"Multiplicamos (o dividimos) los <strong>valores absolutos</strong>.", r"Multiply (or divide) the <strong>absolute values</strong>."),
      L(r"Posem el signe que diu la <strong>regla dels signes</strong>: signes <strong>iguals</strong> donen \(+\) i signes <strong>diferents</strong> donen \(-\).", r"Ponemos el signo que dice la <strong>regla de los signos</strong>: signos <strong>iguales</strong> dan \(+\) y signos <strong>distintos</strong> dan \(-\).", r"Use the <strong>sign rule</strong>: <strong>same</strong> signs give \(+\) and <strong>different</strong> signs give \(-\).")]) + '</ol>'
  + '<div class="sgrule"><div class="pos">\\(+\\cdot+\\ \\to\\ +\\)</div><div class="neg">\\(+\\cdot-\\ \\to\\ -\\)</div><div class="neg">\\(-\\cdot+\\ \\to\\ -\\)</div><div class="pos">\\(-\\cdot-\\ \\to\\ +\\)</div></div>'
  + r'\[(-4)\cdot(+7)=-28\qquad (-5)\cdot(-7)=+35\qquad (+20):(-10)=-2\qquad (-12):(-4)=+3\]'
  + P(r"La regla és la mateixa per a la divisió. I recorda: la divisió entre enters només té com a resultat un enter si és <strong>exacta</strong>, i <strong>no es pot dividir entre 0</strong>.",
      r"La regla es la misma para la división. Y recuerda: la división entre enteros solo da como resultado un entero si es <strong>exacta</strong>, y <strong>no se puede dividir entre 0</strong>.",
      r"The rule is the same for division. And remember: dividing integers only gives an integer if it is <strong>exact</strong>, and <strong>you can't divide by 0</strong>.")
  + note(r"Un truc per a recordar-ho: «els amics dels meus amics són els meus amics (\(+\cdot+\)); els enemics dels meus enemics també són els meus amics (\(-\cdot-\)); els amics dels meus enemics i els enemics dels meus amics són els meus enemics (\(+\cdot-\), \(-\cdot+\))».",
         r"Un truco para recordarlo: «los amigos de mis amigos son mis amigos (\(+\cdot+\)); los enemigos de mis enemigos también son mis amigos (\(-\cdot-\)); los amigos de mis enemigos y los enemigos de mis amigos son mis enemigos (\(+\cdot-\), \(-\cdot+\))».",
         r"A memory trick: “the friends of my friends are my friends (\(+\cdot+\)); the enemies of my enemies are my friends too (\(-\cdot-\)); the friends of my enemies and the enemies of my friends are my enemies (\(+\cdot-\), \(-\cdot+\))”.", '🤝')
  + f'''<div class="widget" id="w-sign">
  <div class="wt">✖ {L("La regla dels signes", "La regla de los signos", "The sign rule")}</div>
  <div class="wrow">{nin("a", "a", "a", "a", "-6")}{seg([("·", "·"), (":", ":")], "·")}{nin("b", "b", "b", "b", "4")}</div>
  {quick([("-6|·|4", "(−6)·(+4)"), ("-5|·|-7", "(−5)·(−7)"), ("3|·|-8", "(+3)·(−8)"), ("-36|:|9", "(−36):(+9)"), ("-48|:|-8", "(−48):(−8)"), ("42|:|-7", "(+42):(−7)"), ("-7|:|2", "(−7):(+2)")])}
  {SGT}
  <div class="info" aria-live="polite"></div>
</div>
''')
s6 += box('prop', L('Diversos factors', 'Varios factores', 'Several factors'),
  P(r"Si multipliquem més de dos enters, podem anar de dos en dos, o bé <strong>comptar els factors negatius</strong>: si n'hi ha un nombre <strong>parell</strong>, el resultat és positiu; si n'hi ha un nombre <strong>senar</strong>, és negatiu.",
    r"Si multiplicamos más de dos enteros, podemos ir de dos en dos, o bien <strong>contar los factores negativos</strong>: si hay un número <strong>par</strong>, el resultado es positivo; si hay un número <strong>impar</strong>, es negativo.",
    r"When multiplying more than two integers, go two at a time, or <strong>count the negative factors</strong>: an <strong>even</strong> number of them gives a positive result; an <strong>odd</strong> number gives a negative one.")
  + r'\[(-2)\cdot(-7)\cdot(-2)=\underbrace{(+14)}_{(-)\cdot(-)}\cdot(-2)=-28\qquad (+5)\cdot(-4)\cdot(-3)=+60\]'
  + P(r"Quan hi ha multiplicacions i divisions seguides (sense parèntesis), es fan <strong>d'esquerra a dreta</strong>:", r"Cuando hay multiplicaciones y divisiones seguidas (sin paréntesis), se hacen <strong>de izquierda a derecha</strong>:", r"When multiplications and divisions come one after another (no brackets), work <strong>from left to right</strong>:")
  + r'\[24:(-2)\cdot(-3)=(-12)\cdot(-3)=36\]'
  + drill('mul', 'Entrena: multiplicacions i divisions', 'Entrena: multiplicaciones y divisiones', 'Train: multiplication and division'))
s6 += level(1, 1,
  prob(L(r"Calcula: \(\ \text{a)}\ (-9)\cdot(-3)\qquad \text{b)}\ 8\cdot(-6)\qquad \text{c)}\ (-36):(+9)\qquad \text{d)}\ (-48):(-8)\)", r"Calcula: \(\ \text{a)}\ (-9)\cdot(-3)\qquad \text{b)}\ 8\cdot(-6)\qquad \text{c)}\ (-36):(+9)\qquad \text{d)}\ (-48):(-8)\)", r"Work out: \(\ \text{a)}\ (-9)\cdot(-3)\qquad \text{b)}\ 8\cdot(-6)\qquad \text{c)}\ (-36):(+9)\qquad \text{d)}\ (-48):(-8)\)"),
       P(r"a) i d) tenen signes iguals (resultat positiu); b) i c), signes diferents (resultat negatiu).", r"a) y d) tienen signos iguales (resultado positivo); b) y c), signos distintos (resultado negativo).", r"a) and d) have the same signs (positive result); b) and c) have different signs (negative result)."),
       r'\[\text{a)}\ +27\qquad \text{b)}\ -48\qquad \text{c)}\ -4\qquad \text{d)}\ +6\]'),
  prob(L(r"Calcula: \(\ (-8)\cdot4\cdot(-6)\)", r"Calcula: \(\ (-8)\cdot4\cdot(-6)\)", r"Work out: \(\ (-8)\cdot4\cdot(-6)\)"),
       P(r"Hi ha dos factors negatius (parell): el resultat serà positiu. \(8\cdot4\cdot6=192\).", r"Hay dos factores negativos (par): el resultado será positivo. \(8\cdot4\cdot6=192\).", r"There are two negative factors (even): the result is positive. \(8\cdot4\cdot6=192\)."),
       r'\[(-8)\cdot4\cdot(-6)=\boxed{+192}\]'))
s6 += level(2, 3,
  prob(L(r"Troba el nombre que falta: \(\ \text{a)}\ (-6)\cdot\square=-18\qquad \text{b)}\ \square\cdot(-5)=+35\qquad \text{c)}\ (-8)\cdot\square=40\)", r"Encuentra el número que falta: \(\ \text{a)}\ (-6)\cdot\square=-18\qquad \text{b)}\ \square\cdot(-5)=+35\qquad \text{c)}\ (-8)\cdot\square=40\)", r"Find the missing number: \(\ \text{a)}\ (-6)\cdot\square=-18\qquad \text{b)}\ \square\cdot(-5)=+35\qquad \text{c)}\ (-8)\cdot\square=40\)"),
       P(r"El valor absolut el trobem dividint; el signe, amb la regla: a) \((-)\cdot\square=(-)\Rightarrow\square\) positiu. b) \(\square\cdot(-)=(+)\Rightarrow\square\) negatiu. c) \((-)\cdot\square=(+)\Rightarrow\square\) negatiu.",
         r"El valor absoluto lo encontramos dividiendo; el signo, con la regla: a) \((-)\cdot\square=(-)\Rightarrow\square\) positivo. b) \(\square\cdot(-)=(+)\Rightarrow\square\) negativo. c) \((-)\cdot\square=(+)\Rightarrow\square\) negativo.",
         r"Find the absolute value by dividing and the sign with the rule: a) \((-)\cdot\square=(-)\Rightarrow\square\) positive. b) \(\square\cdot(-)=(+)\Rightarrow\square\) negative. c) \((-)\cdot\square=(+)\Rightarrow\square\) negative."),
       r'\[\text{a)}\ \boxed{3}\qquad \text{b)}\ \boxed{-7}\qquad \text{c)}\ \boxed{-5}\]'),
  prob(L(r"Calcula: \(\ \text{a)}\ [(+80):(-8)]:(-5)\qquad \text{b)}\ (+50):[(-30):(+6)]\)", r"Calcula: \(\ \text{a)}\ [(+80):(-8)]:(-5)\qquad \text{b)}\ (+50):[(-30):(+6)]\)", r"Work out: \(\ \text{a)}\ [(+80):(-8)]:(-5)\qquad \text{b)}\ (+50):[(-30):(+6)]\)"),
       r'\[\text{a)}\ (-10):(-5)=\boxed{2}\qquad \text{b)}\ (+50):(-5)=\boxed{-10}\]'))
s6 += level(3, 5,
  prob(L(r"Troba dos enters el producte dels quals siga \(-12\) i la suma, \(1\).", r"Encuentra dos enteros cuyo producto sea \(-12\) y su suma, \(1\).", r"Find two integers whose product is \(-12\) and whose sum is \(1\)."),
       P(r"El producte és negatiu: un és positiu i l'altre, negatiu. Parelles amb producte 12: \(1\cdot12,\ 2\cdot6,\ 3\cdot4\). La suma és 1 quan es diferencien en 1 i el positiu és el gran:", r"El producto es negativo: uno es positivo y el otro, negativo. Parejas con producto 12: \(1\cdot12,\ 2\cdot6,\ 3\cdot4\). La suma es 1 cuando se diferencian en 1 y el positivo es el grande:", r"The product is negative: one is positive and the other negative. Pairs with product 12: \(1\cdot12,\ 2\cdot6,\ 3\cdot4\). The sum is 1 when they differ by 1 and the positive one is bigger:"),
       r'\[\boxed{4\ \text{\tri{i}{y}{and}}\ -3}\qquad 4\cdot(-3)=-12\qquad 4+(-3)=1\]'))
s6 += practice([
  ('★', L(r"a) \((+3)\cdot(-5)\cdot(+2)\) &nbsp; b) \((+21):(-7)\) &nbsp; c) \(-2\cdot(-4)\)", r"a) \((+3)\cdot(-5)\cdot(+2)\) &nbsp; b) \((+21):(-7)\) &nbsp; c) \(-2\cdot(-4)\)", r"a) \((+3)\cdot(-5)\cdot(+2)\) &nbsp; b) \((+21):(-7)\) &nbsp; c) \(-2\cdot(-4)\)")),
  ('★★', L(r"d) \(\square\cdot7=-77\) &nbsp; e) \([(-5)\cdot(+12)]:(-3)\) &nbsp; f) \((+100):(+4)\cdot(-2)\)", r"d) \(\square\cdot7=-77\) &nbsp; e) \([(-5)\cdot(+12)]:(-3)\) &nbsp; f) \((+100):(+4)\cdot(-2)\)", r"d) \(\square\cdot7=-77\) &nbsp; e) \([(-5)\cdot(+12)]:(-3)\) &nbsp; f) \((+100):(+4)\cdot(-2)\)")),
  ('★★★', L(r"g) Quin signe té el producte de set factors iguals a \(-1\)? h) Troba dos enters de producte \(-20\) i suma \(-1\).", r"g) ¿Qué signo tiene el producto de siete factores iguales a \(-1\)? h) Encuentra dos enteros de producto \(-20\) y suma \(-1\).", r"g) What is the sign of the product of seven factors equal to \(-1\)? h) Find two integers with product \(-20\) and sum \(-1\)."))],
  r'\[\text{a)}\ -30\qquad \text{b)}\ -3\qquad \text{c)}\ 8\qquad \text{d)}\ -11\qquad \text{e)}\ (-60):(-3)=20\qquad \text{f)}\ 25\cdot(-2)=-50\]'
  + P(r"g) Negatiu (set és senar): el producte val \(-1\). &nbsp; h) \(4\) i \(-5\).", r"g) Negativo (siete es impar): el producto vale \(-1\). &nbsp; h) \(4\) y \(-5\).", r"g) Negative (seven is odd): the product is \(-1\). &nbsp; h) \(4\) and \(-5\)."))
assert ev('(+3)·(-5)·(+2)') == -30 and ev('[(-5)·(+12)]:(-3)') == 20 and ev('(+100):(+4)·(-2)') == -50

# ============================================================ 3.7
s7 = box('def', L('Jerarquia de les operacions', 'Jerarquía de las operaciones', 'Order of operations'),
  P(r"Quan en una expressió hi ha diverses operacions, les fem en aquest ordre (com amb els naturals):", r"Cuando en una expresión hay varias operaciones, las hacemos en este orden (como con los naturales):", r"When an expression has several operations, do them in this order (just as with natural numbers):")
  + '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"<strong>Parèntesis i claudàtors</strong>, començant pels de dins.", r"<strong>Paréntesis y corchetes</strong>, empezando por los de dentro.", r"<strong>Brackets</strong>, starting with the innermost."),
      L(r"<strong>Multiplicacions i divisions</strong>, d'esquerra a dreta.", r"<strong>Multiplicaciones y divisiones</strong>, de izquierda a derecha.", r"<strong>Multiplication and division</strong>, from left to right."),
      L(r"<strong>Sumes i restes</strong>, d'esquerra a dreta (o agrupant positius i negatius).", r"<strong>Sumas y restas</strong>, de izquierda a derecha (o agrupando positivos y negativos).", r"<strong>Addition and subtraction</strong>, from left to right (or grouping positives and negatives).")]) + '</ol>'
  + r'\[\underbrace{(-8)\cdot(+2)}_{-16}+\underbrace{(-5)\cdot(-3)}_{+15}=-16+15=-1\]'
  + r'\[12-\underbrace{[13-(-7)]}_{20}:(-5)=12-\underbrace{20:(-5)}_{-4}=12-(-4)=12+4=16\]'
  + note(r"Errors típics: en \(-3+4\cdot(-2)\) <strong>no</strong> es pot sumar primer: és \(-3+(-8)=-11\). I en \(24:(-2)\cdot(-3)\) cal anar d'esquerra a dreta: \((-12)\cdot(-3)=36\), no \(24:6=4\).",
         r"Errores típicos: en \(-3+4\cdot(-2)\) <strong>no</strong> se puede sumar primero: es \(-3+(-8)=-11\). Y en \(24:(-2)\cdot(-3)\) hay que ir de izquierda a derecha: \((-12)\cdot(-3)=36\), no \(24:6=4\).",
         r"Common mistakes: in \(-3+4\cdot(-2)\) you <strong>can't</strong> add first: it's \(-3+(-8)=-11\). And in \(24:(-2)\cdot(-3)\) go from left to right: \((-12)\cdot(-3)=36\), not \(24:6=4\).", '⚠️')
  + hier(['12-[13-(-7)]:(-5)', '(-8)·(+2)+(-5)·(-3)', '(-2)·(-9)+(-24):(-3)-(-6)·4', '19-(-3)·[5-(+8)]', '(9-6)·(-2)+(13+3):(-4)', '(-20):[(-6)-(-2)]'])
  + drill('comb', 'Entrena: operacions combinades', 'Entrena: operaciones combinadas', 'Train: mixed operations'))
s7 += level(1, 1,
  prob(L(r"Calcula: \(\ (+40):(-8)-(-30):(+6)\)", r"Calcula: \(\ (+40):(-8)-(-30):(+6)\)", r"Work out: \(\ (+40):(-8)-(-30):(+6)\)"),
       P(r"Primer les dues divisions:", r"Primero las dos divisiones:", r"Both divisions first:"),
       r'\[\underbrace{(+40):(-8)}_{-5}-\underbrace{(-30):(+6)}_{-5}=-5-(-5)=-5+5=\boxed{0}\]'),
  prob(L(r"Calcula: \(\ (+4)\cdot[(-5)+(+2)]\)", r"Calcula: \(\ (+4)\cdot[(-5)+(+2)]\)", r"Work out: \(\ (+4)\cdot[(-5)+(+2)]\)"),
       r'\[(+4)\cdot[-5+2]=(+4)\cdot(-3)=\boxed{-12}\]'))
s7 += level(2, 3,
  prob(L(r"Calcula: \(\ (-2)\cdot(-9)+(-24):(-3)-(-6)\cdot4\)", r"Calcula: \(\ (-2)\cdot(-9)+(-24):(-3)-(-6)\cdot4\)", r"Work out: \(\ (-2)\cdot(-9)+(-24):(-3)-(-6)\cdot4\)"),
       P(r"Fem les multiplicacions i divisions:", r"Hacemos las multiplicaciones y divisiones:", r"Do the multiplications and divisions:"),
       r'\[\underbrace{(-2)\cdot(-9)}_{+18}+\underbrace{(-24):(-3)}_{+8}-\underbrace{(-6)\cdot4}_{-24}=18+8-(-24)=18+8+24=\boxed{50}\]'),
  prob(L(r"Calcula: \(\ 19-(-3)\cdot[5-(+8)]\)", r"Calcula: \(\ 19-(-3)\cdot[5-(+8)]\)", r"Work out: \(\ 19-(-3)\cdot[5-(+8)]\)"),
       r'\[19-(-3)\cdot[5-8]=19-(-3)\cdot(-3)=19-(+9)=\boxed{10}\]',
       note(r"No restes \(19-(-3)\) primer: la multiplicació va abans que la resta.", r"No restes \(19-(-3)\) primero: la multiplicación va antes que la resta.", r"Don't subtract \(19-(-3)\) first: multiplication comes before subtraction.", '⚠️')))
s7 += level(3, 5,
  prob(L(r"Calcula: \(\ -2\cdot[3-(-4+6)\cdot(-2)]+15:(-5)\)", r"Calcula: \(\ -2\cdot[3-(-4+6)\cdot(-2)]+15:(-5)\)", r"Work out: \(\ -2\cdot[3-(-4+6)\cdot(-2)]+15:(-5)\)"),
       r'\[-2\cdot[3-\underbrace{(-4+6)}_{2}\cdot(-2)]+15:(-5)=-2\cdot[3-\underbrace{2\cdot(-2)}_{-4}]+15:(-5)\]',
       r'\[=-2\cdot[3+4]+15:(-5)=\underbrace{-2\cdot7}_{-14}+\underbrace{15:(-5)}_{-3}=-14-3=\boxed{-17}\]'),
  prob(L(r"Posa parèntesis perquè la igualtat siga certa: \(\ 6-4\cdot2-5=-6\)", r"Pon paréntesis para que la igualdad sea cierta: \(\ 6-4\cdot2-5=-6\)", r"Add brackets to make it true: \(\ 6-4\cdot2-5=-6\)"),
       P(r"Sense parèntesis dona \(6-8-5=-7\). Provem a agrupar:", r"Sin paréntesis da \(6-8-5=-7\). Probamos a agrupar:", r"Without brackets it gives \(6-8-5=-7\). Let's try grouping:"),
       r'\[\boxed{(6-4)\cdot(2-5)}=2\cdot(-3)=-6\ \ ✓\]'))
assert ev('-2·[3-(-4+6)·(-2)]+15:(-5)') == -17 and ev('(-2)·(-9)+(-24):(-3)-(-6)·4') == 50 and ev('19-(-3)·[5-(+8)]') == 10
PR7 = ['(-3)·[(-2)+(-4)]', '(-20):[(-6)-(-2)]', '12+(-5)·[8+(-9)]', '(+27):(-3)-(+3)·(-5)-(-6)·(-2)', '(-2)·(5-7)-(-3)·(8-6)', '(9-6)·(-2)+(13+3):(-4)']
s7 += practice([
  ('★', L(r"a) \((-3)\cdot[(-2)+(-4)]\) &nbsp; b) \((-20):[(-6)-(-2)]\)", r"a) \((-3)\cdot[(-2)+(-4)]\) &nbsp; b) \((-20):[(-6)-(-2)]\)", r"a) \((-3)\cdot[(-2)+(-4)]\) &nbsp; b) \((-20):[(-6)-(-2)]\)")),
  ('★★', L(r"c) \(12+(-5)\cdot[8+(-9)]\) &nbsp; d) \((+27):(-3)-(+3)\cdot(-5)-(-6)\cdot(-2)\)", r"c) \(12+(-5)\cdot[8+(-9)]\) &nbsp; d) \((+27):(-3)-(+3)\cdot(-5)-(-6)\cdot(-2)\)", r"c) \(12+(-5)\cdot[8+(-9)]\) &nbsp; d) \((+27):(-3)-(+3)\cdot(-5)-(-6)\cdot(-2)\)")),
  ('★★★', L(r"e) \((-2)\cdot(5-7)-(-3)\cdot(8-6)\) &nbsp; f) \((9-6)\cdot(-2)+(13+3):(-4)\)", r"e) \((-2)\cdot(5-7)-(-3)\cdot(8-6)\) &nbsp; f) \((9-6)\cdot(-2)+(13+3):(-4)\)", r"e) \((-2)\cdot(5-7)-(-3)\cdot(8-6)\) &nbsp; f) \((9-6)\cdot(-2)+(13+3):(-4)\)"))],
  r'\[\text{a)}\ (-3)\cdot(-6)=18\qquad \text{b)}\ (-20):(-4)=5\]'
  + r'\[\text{c)}\ 12+(-5)\cdot(-1)=12+5=17\qquad \text{d)}\ -9+15-12=-6\]'
  + r'\[\text{e)}\ (-2)\cdot(-2)-(-3)\cdot2=4+6=10\qquad \text{f)}\ 3\cdot(-2)+16:(-4)=-6-4=-10\]')
assert [ev(e) for e in PR7] == [18, 5, 17, -6, 10, -10]

# ============================================================ 3.8
s8 = box('prop', L('Com resolem un problema amb enters?', '¿Cómo resolvemos un problema con enteros?', 'How do we solve a problem with integers?'),
  '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"Llegim bé l'enunciat i decidim quina és la <strong>referència</strong> (el zero).", r"Leemos bien el enunciado y decidimos cuál es la <strong>referencia</strong> (el cero).", r"Read the problem carefully and decide what the <strong>reference point</strong> (zero) is."),
      L(r"Escrivim cada dada com un enter <strong>amb el seu signe</strong>: <em>puja, guanya, ingressa, sobre zero</em> → \(+\); &nbsp; <em>baixa, perd, gasta, deu, baix zero</em> → \(-\).", r"Escribimos cada dato como un entero <strong>con su signo</strong>: <em>sube, gana, ingresa, sobre cero</em> → \(+\); &nbsp; <em>baja, pierde, gasta, debe, bajo cero</em> → \(-\).", r"Write each piece of data as an integer <strong>with its sign</strong>: <em>goes up, wins, pays in, above zero</em> → \(+\); &nbsp; <em>goes down, loses, spends, owes, below zero</em> → \(-\)."),
      L(r"Plantegem l'operació i la resolem.", r"Planteamos la operación y la resolvemos.", r"Write the calculation and work it out."),
      L(r"Interpretem el resultat amb <strong>paraules</strong>: un \(-5\) en un compte vol dir «dec 5 €».", r"Interpretamos el resultado con <strong>palabras</strong>: un \(-5\) en una cuenta significa «debo 5 €».", r"Explain the result in <strong>words</strong>: \(-5\) in a bank account means “I owe €5”.")]) + '</ol>'
  + P(r"<strong>Diferència entre dos valors:</strong> per a saber quant ha <em>canviat</em> una quantitat, fem <strong>valor final − valor inicial</strong>. Si el resultat és positiu, ha pujat; si és negatiu, ha baixat. La <strong>distància</strong> entre dos valors és el major menys el menor.",
      r"<strong>Diferencia entre dos valores:</strong> para saber cuánto ha <em>cambiado</em> una cantidad, hacemos <strong>valor final − valor inicial</strong>. Si el resultado es positivo, ha subido; si es negativo, ha bajado. La <strong>distancia</strong> entre dos valores es el mayor menos el menor.",
      r"<strong>Difference between two values:</strong> to find how much a quantity has <em>changed</em>, work out <strong>final value − initial value</strong>. A positive result means it went up; a negative one, that it went down. The <strong>distance</strong> between two values is the larger minus the smaller.")
  + r'\[\tri{De }{De }{From }-3\text{ °C}\tri{ a }{ a }{ to }5\text{ °C:}\quad 5-(-3)=5+3=+8\text{ °C}\]'
  + f'''<div class="widget" id="w-elev">
  <div class="wt">🛗 {L("Pujades i baixades", "Subidas y bajadas", "Ups and downs")}</div>
  <div class="wrow">{seg([("floor", L("Ascensor", "Ascensor", "Lift")), ("temp", L("Temperatura", "Temperatura", "Temperature")), ("money", L("Compte", "Cuenta", "Account"))], "floor")}</div>
  <div class="wrow">{nin("s", "Partida", "Salida", "Start", "0")}<label>{L("Canvis", "Cambios", "Changes")} <input class="tin w" type="text" data-k="m" value="+5, −3, +5, −8, +10, +5, −6" autocomplete="off" spellcheck="false" aria-label="canvis"></label></div>
  {quick([("floor|0|+5, −3, +5, −8, +10, +5, −6", L("Ascensor de la Mònica", "Ascensor de Mónica", "Mònica's lift")), ("temp|-14|+10, −5", L("Estació d'esquí", "Estación de esquí", "Ski resort")), ("temp|-3|+9, −10", L("Dia d'hivern", "Día de invierno", "Winter day")), ("money|850|+250, +250, +250, +250, +250, −2300", L("Cartilla d'en Pau", "Cartilla de Pau", "Pau's savings")), ("money|-14|+9", L("Deute amb la germana", "Deuda con la hermana", "Debt to a sister"))])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s8 += level(1, 1,
  prob(L(r"La Mònica ix en l'ascensor des de la planta baixa. Puja 5 plantes, baixa 3, puja 5, baixa 8, puja 10, puja 5 i baixa 6. En quina planta està?", r"Mónica sale en el ascensor desde la planta baja. Sube 5 plantas, baja 3, sube 5, baja 8, sube 10, sube 5 y baja 6. ¿En qué planta está?", r"Mònica gets in the lift on the ground floor. It goes up 5 floors, down 3, up 5, down 8, up 10, up 5 and down 6. Which floor is she on?"),
       P(r"La planta baixa és el 0. Pujar és \(+\) i baixar és \(-\):", r"La planta baja es el 0. Subir es \(+\) y bajar es \(-\):", r"The ground floor is 0. Going up is \(+\) and going down is \(-\):"),
       r'\[0+5-3+5-8+10+5-6=(5+5+10+5)-(3+8+6)=25-17=8\]',
       P(r"Està en la \(\boxed{\text{8a planta}}\).", r"Está en la \(\boxed{\text{8.ª planta}}\).", r"She is on \(\boxed{\text{floor 8}}\).")),
  prob(L(r"En Joan li deu 14 € a la seua germana. Si li'n paga 9, quant li deu?", r"Juan le debe 14 € a su hermana. Si le paga 9, ¿cuánto le debe?", r"Joan owes his sister €14. If he pays her back €9, how much does he owe?"),
       r'\[-14+9=-5\]',
       P(r"Encara li deu \(\boxed{5\text{ €}}\).", r"Aún le debe \(\boxed{5\text{ €}}\).", r"He still owes \(\boxed{€5}\).")))
s8 += level(2, 3,
  prob(L(r"Quina diferència de temperatura suporta una persona que passa de la cambra de les verdures, a 4 °C, a la del peix congelat, a \(-18\) °C? I si fa el camí contrari?", r"¿Qué diferencia de temperatura soporta una persona que pasa de la cámara de las verduras, a 4 °C, a la del pescado congelado, a \(-18\) °C? ¿Y si hace el camino contrario?", r"What temperature change does a person experience going from the vegetable cold room, at 4 °C, to the frozen fish room, at \(-18\) °C? And the other way round?"),
       P(r"Final menys inicial:", r"Final menos inicial:", r"Final minus initial:"),
       r'\[-18-4=\boxed{-22\text{ °C}}\ \ (\tri{baixa 22 graus}{baja 22 grados}{down 22 degrees})\qquad 4-(-18)=4+18=\boxed{+22\text{ °C}}\ \ (\tri{puja 22 graus}{sube 22 grados}{up 22 degrees})\]'),
  prob(L(r"Euclides va viure 60 anys i va morir l'any 265 a. C. En quin any va nàixer?", r"Euclides vivió 60 años y murió en el año 265 a. C. ¿En qué año nació?", r"Euclid lived for 60 years and died in 265 BC. In which year was he born?"),
       P(r"Els anys abans de Crist són negatius. Va nàixer 60 anys <em>abans</em> de morir, és a dir, més a l'esquerra en la recta:", r"Los años antes de Cristo son negativos. Nació 60 años <em>antes</em> de morir, es decir, más a la izquierda en la recta:", r"Years BC are negative. He was born 60 years <em>before</em> he died, that is, further left on the line:"),
       r'\[-265-60=-325\ \ \to\ \ \boxed{325\text{ a. C.}}\]'))
s8 += level(3, 5,
  prob(L(r"El Mulhacén, el pic més alt de la península, fa 3478 m d'altura. El Sistema del Trave, un dels avencs més profunds del món, arriba a 1441 m de profunditat. Quina és la diferència d'altitud entre els dos punts?", r"El Mulhacén, el pico más alto de la península, mide 3478 m de altura. El Sistema del Trave, una de las simas más profundas del mundo, llega a 1441 m de profundidad. ¿Cuál es la diferencia de altitud entre los dos puntos?", r"Mulhacén, the highest peak on the Iberian Peninsula, is 3478 m high. The Trave System, one of the deepest caves in the world, goes down to 1441 m. What is the difference in altitude between the two points?"),
       r'\[3478-(-1441)=3478+1441=\boxed{4919\text{ m}}\]'),
  prob(L(r"En Pau tenia 850 € a la cartilla. Ha ingressat 250 € cada mes durant 5 mesos i després n'ha tret 2300 per a pagar el fuster. Quin saldo li queda?", r"Pau tenía 850 € en la cartilla. Ha ingresado 250 € cada mes durante 5 meses y después ha sacado 2300 para pagar al carpintero. ¿Qué saldo le queda?", r"Pau had €850 in his savings account. He paid in €250 every month for 5 months and then took out €2300 to pay the carpenter. What is his balance?"),
       r'\[850+5\cdot250-2300=850+1250-2300=\boxed{-200\text{ €}}\]',
       P(r"El saldo és negatiu: el compte està en <strong>descobert</strong> i en Pau deu 200 € al banc.", r"El saldo es negativo: la cuenta está en <strong>descubierto</strong> y Pau debe 200 € al banco.", r"The balance is negative: the account is <strong>overdrawn</strong> and Pau owes the bank €200.")))
s8 += practice([
  ('★', L(r"a) A les 8 h el termòmetre marcava \(-14\) °C; al migdia havia pujat 10 graus i a les 19 h havia baixat 5 graus. Quina temperatura feia a les 19 h? b) Si estava bussejant a 2 m de profunditat i ara estic sobre un penya-segat a 8 m d'altura, quina distància hi ha entre els dos llocs?", r"a) A las 8 h el termómetro marcaba \(-14\) °C; al mediodía había subido 10 grados y a las 19 h había bajado 5 grados. ¿Qué temperatura hacía a las 19 h? b) Si estaba buceando a 2 m de profundidad y ahora estoy sobre un acantilado a 8 m de altura, ¿qué distancia hay entre los dos lugares?", r"a) At 8 am the thermometer read \(-14\) °C; by midday it had risen 10 degrees and by 7 pm it had dropped 5 degrees. What was the temperature at 7 pm? b) I was diving 2 m deep and now I'm on top of a cliff 8 m high. How far apart are the two places?")),
  ('★★', L(r"c) Un dia d'hivern, a les 6 h feia \(-3\) °C. Al migdia la temperatura havia pujat 9 graus i a mitjanit el termòmetre marcava \(-1\) °C. Quina diferència de temperatura hi ha hagut entre el migdia i la mitjanit? d) La gasolina baixa 5 cèntims el primer mes, puja 3 el segon, puja 8 el tercer i baixa 2 el quart. Quina és la variació total?", r"c) Un día de invierno, a las 6 h hacía \(-3\) °C. Al mediodía la temperatura había subido 9 grados y a medianoche el termómetro marcaba \(-1\) °C. ¿Qué diferencia de temperatura ha habido entre el mediodía y la medianoche? d) La gasolina baja 5 céntimos el primer mes, sube 3 el segundo, sube 8 el tercero y baja 2 el cuarto. ¿Cuál es la variación total?", r"c) On a winter's day it was \(-3\) °C at 6 am. By midday the temperature had risen 9 degrees and at midnight the thermometer read \(-1\) °C. What was the temperature change between midday and midnight? d) Petrol goes down 5 cents in the first month, up 3 in the second, up 8 in the third and down 2 in the fourth. What is the total change?")),
  ('★★★', L(r"e) Arquimedes va nàixer l'any 287 a. C. i va morir l'any 212 a. C. Quants anys va viure? f) Un submarí està a 120 m de profunditat. Puja 45 m i després baixa el triple del que ha pujat. A quina profunditat està ara?", r"e) Arquímedes nació en el año 287 a. C. y murió en el año 212 a. C. ¿Cuántos años vivió? f) Un submarino está a 120 m de profundidad. Sube 45 m y después baja el triple de lo que ha subido. ¿A qué profundidad está ahora?", r"e) Archimedes was born in 287 BC and died in 212 BC. How many years did he live? f) A submarine is 120 m deep. It rises 45 m and then goes down three times as much as it rose. How deep is it now?"))],
  P(r"a) \(-14+10-5=-9\) °C. &nbsp; b) \(8-(-2)=10\) m.", r"a) \(-14+10-5=-9\) °C. &nbsp; b) \(8-(-2)=10\) m.", r"a) \(-14+10-5=-9\) °C. &nbsp; b) \(8-(-2)=10\) m.")
  + P(r"c) Al migdia, \(-3+9=6\) °C; \(\ -1-6=-7\): ha baixat 7 °C. &nbsp; d) \(-5+3+8-2=+4\): ha pujat 4 cèntims.", r"c) Al mediodía, \(-3+9=6\) °C; \(\ -1-6=-7\): ha bajado 7 °C. &nbsp; d) \(-5+3+8-2=+4\): ha subido 4 céntimos.", r"c) At midday, \(-3+9=6\) °C; \(\ -1-6=-7\): it dropped 7 °C. &nbsp; d) \(-5+3+8-2=+4\): it went up 4 cents.")
  + P(r"e) \(-212-(-287)=75\) anys. &nbsp; f) \(-120+45-3\cdot45=-210\): a 210 m de profunditat.", r"e) \(-212-(-287)=75\) años. &nbsp; f) \(-120+45-3\cdot45=-210\): a 210 m de profundidad.", r"e) \(-212-(-287)=75\) years. &nbsp; f) \(-120+45-3\cdot45=-210\): 210 m deep."))
assert ev('-120+45-3·45') == -210 and ev('-212-(-287)') == 75 and ev('850+5·250-2300') == -200

# ============================================================ muntatge
SECS = [
  (L('Els nombres enters', 'Los números enteros', 'Integers'), s1),
  (L('Recta numèrica, ordre i comparació', 'Recta numérica, orden y comparación', 'Number line, order and comparison'), s2),
  (L('Valor absolut i oposat', 'Valor absoluto y opuesto', 'Absolute value and opposite'), s3),
  (L('Suma i resta d\'enters', 'Suma y resta de enteros', 'Adding and subtracting integers'), s4),
  (L('Parèntesis i claudàtors', 'Paréntesis y corchetes', 'Brackets'), s5),
  (L('Multiplicació i divisió', 'Multiplicación y división', 'Multiplication and division'), s6),
  (L('Operacions combinades', 'Operaciones combinadas', 'Mixed operations'), s7),
  (L('Problemes amb enters', 'Problemas con enteros', 'Problems with integers'), s8),
]
NS = len(SECS)
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Nombres enters · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 3 (Nombres enters) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "±";')
assert 'Nombres enters · FentMates' in head and 'content: "±"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">3.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 3", "Unidad 3", "Unit 3")}</span>
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
    <h1><span class="u">{L("Unitat 3", "Unidad 3", "Unit 3")}</span> · {L("Nombres enters", "Números enteros", "Integers")}</h1>
    <p>{L("Què són els nombres enters i per a què serveixen, la recta numèrica, l'ordre, el valor absolut i l'oposat, les quatre operacions amb la regla dels signes, les operacions combinades i els problemes de la vida real: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Qué son los números enteros y para qué sirven, la recta numérica, el orden, el valor absoluto y el opuesto, las cuatro operaciones con la regla de los signos, las operaciones combinadas y los problemas de la vida real: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "What integers are and what they're for, the number line, ordering, absolute value and opposites, the four operations with the sign rule, mixed operations and real-life problems: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
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
  <p>{L("Apunts de teoria · Unitat 3: Nombres enters · 1r ESO", "Apuntes de teoría · Unidad 3: Números enteros · 1º ESO", "Theory notes · Unit 3: Integers · 1st ESO")}</p>
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
