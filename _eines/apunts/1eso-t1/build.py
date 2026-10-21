import os, re, sys

# Genera materials/1eso/t1-nombres-naturals.html. Ús: python3 _eines/apunts/1eso-t1/build.py
# Agafa la capçalera i l'estil de materials/3eso/t3-proporcionalitat-percentatges.html; el JavaScript és a app.js i l'estil propi, a extra.css.
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SRC = os.path.join(SITE, "materials/3eso/t3-proporcionalitat-percentatges.html")
OUT = os.path.join(SITE, "materials/1eso/t1-nombres-naturals.html")

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
    return (f'\n<!-- ======================= 1.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">1.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')
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
def hier(presets):
    keys = ''.join(f'<button type="button" data-ins="{k}">{k}</button>' for k in ['·', ':', '^', '√', '(', ')', '[', ']'])
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

# ============================================================ 1.1
s1 = box('def', L('Definició: nombres naturals', 'Definición: números naturales', 'Definition: natural numbers'),
  P(r"Els <strong>nombres naturals</strong> són els que fem servir per a <strong>comptar</strong>: 0, 1, 2, 3, 4… El conjunt de tots ells es representa amb la lletra \(\mathbb{N}\):",
    r"Los <strong>números naturales</strong> son los que usamos para <strong>contar</strong>: 0, 1, 2, 3, 4… El conjunto de todos ellos se representa con la letra \(\mathbb{N}\):",
    r"<strong>Natural numbers</strong> are the numbers we use for <strong>counting</strong>: 0, 1, 2, 3, 4… The set of all of them is written with the letter \(\mathbb{N}\):")
  + r'\[\mathbb{N}=\{0,\ 1,\ 2,\ 3,\ 4,\ 5,\ 6,\ \ldots\}\]'
  + ul(L(r"<strong>No s'acaben mai:</strong> sempre podem sumar 1 i obtindre'n un altre. El conjunt és <strong>infinit</strong>.",
         r"<strong>No se acaban nunca:</strong> siempre podemos sumar 1 y obtener otro. El conjunto es <strong>infinito</strong>.",
         r"<strong>They never end:</strong> we can always add 1 and get another one. The set is <strong>infinite</strong>."),
       L(r"Cada natural té un <strong>següent</strong> (el següent de 99 és 100) i, tots menys el 0, tenen un <strong>anterior</strong> (l'anterior de 100 és 99).",
         r"Cada natural tiene un <strong>siguiente</strong> (el siguiente de 99 es 100) y, todos menos el 0, tienen un <strong>anterior</strong> (el anterior de 100 es 99).",
         r"Every natural number has a <strong>next</strong> one (after 99 comes 100) and, all except 0, have a <strong>previous</strong> one (before 100 comes 99)."),
       L(r"Estan <strong>ordenats</strong>: de dos naturals sempre sabem quin és el més gran. Ho escrivim amb \(<\) (menor que) i \(>\) (major que): \(\ 15<51\), \(\ 300>299\).",
         r"Están <strong>ordenados</strong>: de dos naturales siempre sabemos cuál es el mayor. Lo escribimos con \(<\) (menor que) y \(>\) (mayor que): \(\ 15<51\), \(\ 300>299\).",
         r"They are <strong>ordered</strong>: of two natural numbers we always know which is bigger. We write \(<\) (less than) and \(>\) (greater than): \(\ 15<51\), \(\ 300>299\)."))
  + '<div class="nline"><svg viewBox="0 0 620 70" role="img" aria-label="recta"><line class="sv-ax" x1="20" y1="34" x2="600" y2="34"/><path class="sv-ax" d="M592 28 L602 34 L592 40" fill="none"/>'
  + ''.join(f'<line class="sv-ax" x1="{40+i*52}" y1="27" x2="{40+i*52}" y2="41"/><circle class="sv-dot" cx="{40+i*52}" cy="34" r="4.5"/><text class="sv-t" x="{40+i*52}" y="62" text-anchor="middle">{i}</text>' for i in range(11))
  + '<text class="sv-tb" x="602" y="62" text-anchor="end">…</text></svg></div>'
  + P(r"Els podem situar en la <strong>recta numèrica</strong>, separats sempre per la mateixa distància: com més a la dreta, més gran és el nombre.",
      r"Los podemos situar en la <strong>recta numérica</strong>, separados siempre por la misma distancia: cuanto más a la derecha, mayor es el número.",
      r"We can place them on the <strong>number line</strong>, always the same distance apart: the further right, the bigger the number.")
  + note(r"Alguns llibres comencen els naturals per l'1. En aquests apunts hi incloem el 0.",
         r"Algunos libros empiezan los naturales por el 1. En estos apuntes incluimos el 0.",
         r"Some books start the natural numbers at 1. In these notes we include 0."))
s1 += box('prop', L('Per a què servixen?', '¿Para qué sirven?', 'What are they for?'),
  ul(L(r"<strong>Comptar</strong> (quants n'hi ha): «a la classe hi ha 24 alumnes».", r"<strong>Contar</strong> (cuántos hay): «en la clase hay 24 alumnos».", r"<strong>Counting</strong> (how many): “there are 24 students in the class”."),
     L(r"<strong>Ordenar</strong> (quin lloc ocupa): «he arribat el 3r a la meta».", r"<strong>Ordenar</strong> (qué lugar ocupa): «he llegado el 3.º a la meta».", r"<strong>Ordering</strong> (which position): “I finished 3rd in the race”."),
     L(r"<strong>Identificar</strong> (com un codi): el codi postal 46001, un número de telèfon o el dorsal d'un jugador.", r"<strong>Identificar</strong> (como un código): el código postal 46001, un número de teléfono o el dorsal de un jugador.", r"<strong>Identifying</strong> (like a code): the postcode 46001, a phone number or a player's shirt number.")))
s1 += sub("El sistema de numeració decimal", "El sistema de numeración decimal", "The decimal number system")
s1 += box('def', L('Sistema de numeració decimal', 'Sistema de numeración decimal', 'The decimal system'),
  P(r"Escrivim tots els nombres amb només <strong>deu xifres</strong>: 0, 1, 2, 3, 4, 5, 6, 7, 8 i 9. El nostre sistema és:",
    r"Escribimos todos los números con solo <strong>diez cifras</strong>: 0, 1, 2, 3, 4, 5, 6, 7, 8 y 9. Nuestro sistema es:",
    r"We write every number using only <strong>ten digits</strong>: 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9. Our system is:")
  + ul(L(r"<strong>Decimal:</strong> 10 unitats d'un ordre formen 1 unitat de l'ordre següent.", r"<strong>Decimal:</strong> 10 unidades de un orden forman 1 unidad del orden siguiente.", r"<strong>Decimal (base 10):</strong> 10 units of one place make 1 unit of the next place."),
       L(r"<strong>Posicional:</strong> el valor d'una xifra depén del lloc que ocupa.", r"<strong>Posicional:</strong> el valor de una cifra depende del lugar que ocupa.", r"<strong>Positional:</strong> what a digit is worth depends on its place."))
  + r'\[1\ \text{D}=10\ \text{U}\qquad 1\ \text{C}=10\ \text{D}=100\ \text{U}\qquad 1\ \text{UM}=10\ \text{C}=1000\ \text{U}\qquad\ldots\]'
  + '<div class="tbl-wrap"><table class="data"><thead><tr>'
  + ''.join(f'<th>{t}</th>' for t in ['CMi', 'DMi', 'UMi', 'CM', 'DM', 'UM', 'C', 'D', 'U'])
  + '</tr></thead><tbody><tr>'
  + ''.join(f'<td class="l" style="font-size:.75rem">{t}</td>' for t in [
      L('centenes de milió', 'centenas de millón', 'hundred millions'), L('desenes de milió', 'decenas de millón', 'ten millions'), L('unitats de milió', 'unidades de millón', 'millions'),
      L('centenes de miler', 'centenas de millar', 'hundred thousands'), L('desenes de miler', 'decenas de millar', 'ten thousands'), L('unitats de miler', 'unidades de millar', 'thousands'),
      L('centenes', 'centenas', 'hundreds'), L('desenes', 'decenas', 'tens'), L('unitats', 'unidades', 'units')])
  + '</tr><tr>' + ''.join(f'<td><strong>{d}</strong></td>' for d in '025308146') + '</tr></tbody></table></div>'
  + P(r"El nombre \(25\,308\,146\) es llig «vint-i-cinc milions tres-cents huit mil cent quaranta-sis». Per a llegir-lo millor, separem les xifres de tres en tres començant per la dreta.",
      r"El número \(25\,308\,146\) se lee «veinticinco millones trescientos ocho mil ciento cuarenta y seis». Para leerlo mejor, separamos las cifras de tres en tres empezando por la derecha.",
      r"The number \(25\,308\,146\) is read “twenty-five million three hundred and eight thousand one hundred and forty-six”. To read it more easily, we split the digits into groups of three starting from the right.")
  + note(r"En valencià i en castellà, els nombres de quatre xifres s'escriuen junts (\(4738\)) i, a partir de cinc xifres, se separen amb un espai (\(44\,863\)). <strong>Mai amb punt ni coma.</strong>",
         r"En castellano, los números de cuatro cifras se escriben juntos (\(4738\)) y, a partir de cinco cifras, se separan con un espacio (\(44\,863\)). <strong>Nunca con punto ni coma.</strong>",
         r"In these notes, four-digit numbers are written together (\(4738\)) and from five digits on we use a space (\(44\,863\)), as is done in Spain. In English you'll often see a comma: 44,863.", '✏️'))
s1 += box('prop', L("Valor d'una xifra segons la seua posició", 'Valor de una cifra según su posición', "A digit's value depends on its place"),
  P(r"En el nombre \(5353\) hi ha dos cincs, però no valen el mateix: el primer val \(5000\) (5 unitats de miler) i el segon val \(50\) (5 desenes).",
    r"En el número \(5353\) hay dos cincos, pero no valen lo mismo: el primero vale \(5000\) (5 unidades de millar) y el segundo vale \(50\) (5 decenas).",
    r"In the number \(5353\) there are two fives, but they're not worth the same: the first is worth \(5000\) (5 thousands) and the second \(50\) (5 tens).")
  + r'\[5353=5\,\text{UM}+3\,\text{C}+5\,\text{D}+3\,\text{U}=5000+300+50+3\]'
  + f'''<div class="widget" id="w-place">
  <div class="wt">🔢 {L("Taula de valor posicional", "Tabla de valor posicional", "Place value table")}</div>
  <div class="wrow"><label>{L("Nombre", "Número", "Number")} <input class="tin w" type="text" inputmode="numeric" value="25308146" autocomplete="off" aria-label="nombre"></label></div>
  {quick([("5353", "5353"), ("7405", "7405"), ("35060", "35 060"), ("600006", "600 006"), ("1000001", "1 000 001"), ("230450978", "230 450 978")])}
  <div class="tbl-wrap pv"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s1 += level(1, 1,
  prob(L("Escriu amb xifres: «dos milions tres-cents mil cinquanta».", "Escribe con cifras: «dos millones trescientos mil cincuenta».", "Write in figures: “two million three hundred thousand and fifty”."),
       P(r"Hi ha 2 milions, 300 milers i 50 unitats. Ho posem en la taula i omplim amb zeros els llocs buits:", r"Hay 2 millones, 300 millares y 50 unidades. Lo ponemos en la tabla y rellenamos con ceros los lugares vacíos:", r"There are 2 millions, 300 thousands and 50 units. We put them in the table and fill the empty places with zeros:")
       + r'\[\underbrace{2}_{\text{UMi}}\ \underbrace{300}_{\text{CM DM UM}}\ \underbrace{050}_{\text{C D U}}\]',
       r'\[\boxed{2\,300\,050}\]'),
  prob(L("Quant val la xifra 6 en cadascun d'aquests nombres? \(\ 4682,\ \ 61\,007,\ \ 306\)", "¿Cuánto vale la cifra 6 en cada uno de estos números? \(\ 4682,\ \ 61\,007,\ \ 306\)", "What is the digit 6 worth in each of these numbers? \(\ 4682,\ \ 61\,007,\ \ 306\)"),
       P(r"En \(4682\) està en les centenes: val \(\boxed{600}\).", r"En \(4682\) está en las centenas: vale \(\boxed{600}\).", r"In \(4682\) it's in the hundreds: it's worth \(\boxed{600}\)."),
       P(r"En \(61\,007\) està en les desenes de miler: val \(\boxed{60\,000}\).", r"En \(61\,007\) está en las decenas de millar: vale \(\boxed{60\,000}\).", r"In \(61\,007\) it's in the ten thousands: it's worth \(\boxed{60\,000}\)."),
       P(r"En \(306\) està en les unitats: val \(\boxed{6}\).", r"En \(306\) está en las unidades: vale \(\boxed{6}\).", r"In \(306\) it's in the units: it's worth \(\boxed{6}\).")))
s1 += level(2, 3,
  prob(L(r"Ordena de menor a major: \(\ 30\,909,\ \ 30\,099,\ \ 3999,\ \ 39\,090,\ \ 30\,990\).", r"Ordena de menor a mayor: \(\ 30\,909,\ \ 30\,099,\ \ 3999,\ \ 39\,090,\ \ 30\,990\).", r"Order from smallest to largest: \(\ 30\,909,\ \ 30\,099,\ \ 3999,\ \ 39\,090,\ \ 30\,990\)."),
       P(r"Primer mirem quantes xifres té cada un: \(3999\) en té 4 i és el més xicotet. La resta en tenen 5.", r"Primero miramos cuántas cifras tiene cada uno: \(3999\) tiene 4 y es el menor. Los demás tienen 5.", r"First look at how many digits each has: \(3999\) has 4, so it's the smallest. The others have 5."),
       P(r"Amb les mateixes xifres, comparem d'esquerra a dreta: tots comencen per 3; en la segona xifra, \(39\,090\) té un 9 i és el més gran. Després comparem la tercera xifra dels altres (0, 9, 9) i, si cal, la quarta.", r"Con las mismas cifras, comparamos de izquierda a derecha: todos empiezan por 3; en la segunda cifra, \(39\,090\) tiene un 9 y es el mayor. Después comparamos la tercera cifra de los demás (0, 9, 9) y, si hace falta, la cuarta.", r"With the same number of digits, compare from left to right: all start with 3; in the second digit, \(39\,090\) has a 9, so it's the biggest. Then compare the third digit of the rest (0, 9, 9) and, if needed, the fourth."),
       r'\[\boxed{3999<30\,099<30\,909<30\,990<39\,090}\]'),
  prob(L(r"Escriu l'anterior i el següent de \(10\,000\) i de \(2\,099\,999\).", r"Escribe el anterior y el siguiente de \(10\,000\) y de \(2\,099\,999\).", r"Write the number before and after \(10\,000\) and \(2\,099\,999\)."),
       r'\[9999\ \longleftarrow\ 10\,000\ \longrightarrow\ 10\,001\]',
       P(r"Si sumem 1 a \(2\,099\,999\), tots els 9 es converteixen en 0 i «portem» una unitat fins a les centenes de miler:", r"Si sumamos 1 a \(2\,099\,999\), todos los 9 se convierten en 0 y «nos llevamos» una unidad hasta las centenas de millar:", r"If we add 1 to \(2\,099\,999\), all the 9s turn into 0 and we “carry” one all the way to the hundred thousands:")
       + r'\[2\,099\,998\ \longleftarrow\ 2\,099\,999\ \longrightarrow\ \boxed{2\,100\,000}\]'))
s1 += level(3, 5,
  prob(L(r"Amb les xifres 3, 0, 7 i 5, sense repetir-ne cap, escriu el nombre de quatre xifres més gran i el més xicotet possible. Quina és la diferència entre ells?", r"Con las cifras 3, 0, 7 y 5, sin repetir ninguna, escribe el número de cuatro cifras mayor y el menor posible. ¿Cuál es la diferencia entre ellos?", r"Using the digits 3, 0, 7 and 5 once each, write the largest and the smallest possible four-digit number. What is the difference between them?"),
       P(r"<strong>El més gran:</strong> posem les xifres de major a menor: \(7530\).", r"<strong>El mayor:</strong> ponemos las cifras de mayor a menor: \(7530\).", r"<strong>The largest:</strong> put the digits from biggest to smallest: \(7530\)."),
       P(r"<strong>El més xicotet:</strong> de menor a major seria 0357, però un nombre de quatre xifres no pot començar per 0. Comencem per la xifra més xicoteta que no siga 0 (el 3) i després posem la resta de menor a major: \(3057\).", r"<strong>El menor:</strong> de menor a mayor sería 0357, pero un número de cuatro cifras no puede empezar por 0. Empezamos por la cifra más pequeña que no sea 0 (el 3) y después ponemos el resto de menor a mayor: \(3057\).", r"<strong>The smallest:</strong> smallest to largest would be 0357, but a four-digit number can't start with 0. Start with the smallest non-zero digit (3) and then put the rest from smallest to largest: \(3057\)."),
       r'\[7530-3057=\boxed{4473}\]'))
s1 += practice([
  ('★', L(r"a) Escriu amb lletres \(40\,518\). b) Escriu amb xifres «set milions huit-cents mil».", r"a) Escribe con letras \(40\,518\). b) Escribe con cifras «siete millones ochocientos mil».", r"a) Write \(40\,518\) in words. b) Write in figures “seven million eight hundred thousand”.")),
  ('★★', L(r"c) Quantes desenes té en total el nombre \(4580\)? d) I quantes centenes té \(25\,000\)?", r"c) ¿Cuántas decenas tiene en total el número \(4580\)? d) ¿Y cuántas centenas tiene \(25\,000\)?", r"c) How many tens are there altogether in \(4580\)? d) And how many hundreds in \(25\,000\)?")),
  ('★★★', L(r"e) Escriu el nombre més gran i el més xicotet de cinc xifres, totes diferents. f) Quants nombres de tres xifres hi ha?", r"e) Escribe el número mayor y el menor de cinco cifras, todas distintas. f) ¿Cuántos números de tres cifras hay?", r"e) Write the largest and the smallest five-digit numbers with all digits different. f) How many three-digit numbers are there?"))],
  P(r"a) quaranta mil cinc-cents dihuit. &nbsp; b) \(7\,800\,000\).", r"a) cuarenta mil quinientos dieciocho. &nbsp; b) \(7\,800\,000\).", r"a) forty thousand five hundred and eighteen. &nbsp; b) \(7\,800\,000\).")
  + P(r"c) \(458\) desenes (\(4580=458\cdot10\)). &nbsp; d) \(250\) centenes.", r"c) \(458\) decenas (\(4580=458\cdot10\)). &nbsp; d) \(250\) centenas.", r"c) \(458\) tens (\(4580=458\cdot10\)). &nbsp; d) \(250\) hundreds.")
  + P(r"e) \(98\,765\) i \(10\,234\). &nbsp; f) Del 100 al 999: \(999-99=900\) nombres.", r"e) \(98\,765\) y \(10\,234\). &nbsp; f) Del 100 al 999: \(999-99=900\) números.", r"e) \(98\,765\) and \(10\,234\). &nbsp; f) From 100 to 999: \(999-99=900\) numbers."))

# ============================================================ 1.2
s2 = box('def', L('Aproximar un nombre', 'Aproximar un número', 'Approximating a number'),
  P(r"<strong>Aproximar</strong> és canviar un nombre per un altre de pròxim, més fàcil de llegir, recordar o calcular. Si a un concert hi ha 44 863 persones, el diari dirà que n'hi havia «unes 45 000». Hi ha dues maneres de fer-ho: el <strong>truncament</strong> i l'<strong>arrodoniment</strong>.",
    r"<strong>Aproximar</strong> es cambiar un número por otro próximo, más fácil de leer, recordar o calcular. Si en un concierto hay 44 863 personas, el periódico dirá que había «unas 45 000». Hay dos formas de hacerlo: el <strong>truncamiento</strong> y el <strong>redondeo</strong>.",
    r"<strong>Approximating</strong> means replacing a number with a nearby one that is easier to read, remember or work with. If 44,863 people go to a concert, the newspaper will say “about 45,000”. There are two ways to do it: <strong>truncating</strong> and <strong>rounding</strong>."))
s2 += box('def', L('Truncament', 'Truncamiento', 'Truncating'),
  P(r"<strong>Truncar</strong> un nombre a un ordre (desenes, centenes, milers…) és <strong>canviar per zeros totes les xifres que hi ha a la dreta</strong> d'aquest ordre. És com «tallar» el nombre.",
    r"<strong>Truncar</strong> un número a un orden (decenas, centenas, millares…) es <strong>cambiar por ceros todas las cifras que hay a la derecha</strong> de ese orden. Es como «cortar» el número.",
    r"To <strong>truncate</strong> a number to a place (tens, hundreds, thousands…) means <strong>replacing every digit to its right with a zero</strong>. It's like “chopping” the number.")
  + r'\[44\,8\underline{63}\ \xrightarrow{\ \tri{truncament a les centenes}{truncamiento a las centenas}{truncate to the hundreds}\ }\ 44\,800\]')
s2 += box('def', L('Arrodoniment', 'Redondeo', 'Rounding'),
  P(r"Per a <strong>arrodonir</strong> a un ordre, mirem la <strong>xifra següent</strong> (la que hi ha just a la dreta):",
    r"Para <strong>redondear</strong> a un orden, miramos la <strong>cifra siguiente</strong> (la que hay justo a la derecha):",
    r"To <strong>round</strong> to a place, look at the <strong>next digit</strong> (the one just to its right):")
  + ul(L(r"Si és <strong>0, 1, 2, 3 o 4</strong> → la xifra de l'ordre es queda igual.", r"Si es <strong>0, 1, 2, 3 o 4</strong> → la cifra del orden se queda igual.", r"If it's <strong>0, 1, 2, 3 or 4</strong> → the digit in that place stays the same."),
       L(r"Si és <strong>5, 6, 7, 8 o 9</strong> → sumem 1 a la xifra de l'ordre.", r"Si es <strong>5, 6, 7, 8 o 9</strong> → sumamos 1 a la cifra del orden.", r"If it's <strong>5, 6, 7, 8 or 9</strong> → add 1 to the digit in that place."),
       L(r"Després, canviem per zeros totes les xifres de la dreta.", r"Después, cambiamos por ceros todas las cifras de la derecha.", r"Then replace all the digits to the right with zeros."))
  + r'\[44\,8\fbox{6}3\ \xrightarrow{\ 6\,\ge\,5\ }\ 44\,900\qquad\qquad 44\,8\fbox{2}3\ \xrightarrow{\ 2\,<\,5\ }\ 44\,800\]')
s2 += box('prop', L("Quina aproximació és millor?", "¿Qué aproximación es mejor?", "Which approximation is better?"),
  P(r"L'<strong>error</strong> d'una aproximació és la diferència entre el valor exacte i l'aproximat. <strong>L'arrodoniment sempre dona el nombre més pròxim</strong>, és a dir, el de menys error.",
    r"El <strong>error</strong> de una aproximación es la diferencia entre el valor exacto y el aproximado. <strong>El redondeo siempre da el número más próximo</strong>, es decir, el de menor error.",
    r"The <strong>error</strong> of an approximation is the difference between the exact value and the approximate one. <strong>Rounding always gives the closest number</strong>, that is, the one with the smallest error.")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>44 863</th><th>' + L('Truncament', 'Truncamiento', 'Truncated') + '</th><th>' + L('Error', 'Error', 'Error') + '</th><th>' + L('Arrodoniment', 'Redondeo', 'Rounded') + '</th><th>' + L('Error', 'Error', 'Error') + '</th></tr></thead><tbody>'
  + '<tr><th>' + L('a les desenes', 'a las decenas', 'to the tens') + r'</th><td>\(44\,860\)</td><td>3</td><td>\(44\,860\)</td><td>3</td></tr>'
  + '<tr><th>' + L('a les centenes', 'a las centenas', 'to the hundreds') + r'</th><td>\(44\,800\)</td><td>63</td><td>\(44\,900\)</td><td>37</td></tr>'
  + '<tr><th>' + L('als milers', 'a los millares', 'to the thousands') + r'</th><td>\(44\,000\)</td><td>863</td><td>\(45\,000\)</td><td>137</td></tr>'
  + '</tbody></table></div>'
  + f'''<div class="widget" id="w-round">
  <div class="wt">🎯 {L("Aproximador: truncament i arrodoniment", "Aproximador: truncamiento y redondeo", "Approximator: truncating and rounding")}</div>
  <div class="wrow"><label>{L("Nombre", "Número", "Number")} <input class="tin w" type="text" inputmode="numeric" value="44863" autocomplete="off" aria-label="nombre"></label>
  <div class="seg" role="group">''' + ''.join(f'<button type="button" data-k="{k}" aria-pressed="{"true" if k == 2 else "false"}">{t}</button>' for k, t in [
      (1, L('Desenes', 'Decenas', 'Tens')), (2, L('Centenes', 'Centenas', 'Hundreds')), (3, L('U. de miler', 'U. de millar', 'Thousands')),
      (4, L('D. de miler', 'D. de millar', 'Ten thous.')), (5, L('C. de miler', 'C. de millar', 'Hundred thous.')), (6, L('U. de milió', 'U. de millón', 'Millions'))]) + f'''</div></div>
  {quick([("7386", "7386"), ("52349", "52 349"), ("2996", "2996"), ("39970", "39 970"), ("18750", "18 750"), ("825948", "825 948")])}
  <div class="dgw"></div>
  <div class="cards"><div class="card"><h4>✂ {L("Truncament", "Truncamiento", "Truncated")}</h4><div data-o="t"></div></div><div class="card"><h4>⚖ {L("Arrodoniment", "Redondeo", "Rounded")}</h4><div data-o="r"></div></div></div>
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('round', 'Entrena: aproxima', 'Entrena: aproxima', 'Train: approximate'))
s2 += level(1, 1,
  prob(L(r"Trunca i arrodoneix \(7386\) a les centenes.", r"Trunca y redondea \(7386\) a las centenas.", r"Truncate and round \(7386\) to the hundreds."),
       P(r"<strong>Truncament:</strong> posem zeros a la dreta de les centenes:", r"<strong>Truncamiento:</strong> ponemos ceros a la derecha de las centenas:", r"<strong>Truncating:</strong> put zeros to the right of the hundreds:") + r'\[73\underline{86}\ \to\ \boxed{7300}\]',
       P(r"<strong>Arrodoniment:</strong> la xifra següent (desenes) és un 8, que és 5 o més. Sumem 1 a les centenes:", r"<strong>Redondeo:</strong> la cifra siguiente (decenas) es un 8, que es 5 o más. Sumamos 1 a las centenas:", r"<strong>Rounding:</strong> the next digit (tens) is 8, which is 5 or more. Add 1 to the hundreds:") + r'\[73\fbox{8}6\ \to\ \boxed{7400}\]'),
  prob(L(r"Arrodoneix \(52\,349\) a les desenes, a les centenes i a les unitats de miler.", r"Redondea \(52\,349\) a las decenas, a las centenas y a las unidades de millar.", r"Round \(52\,349\) to the tens, the hundreds and the thousands."),
       P(r"<strong>Desenes:</strong> mirem les unitats (9 ≥ 5) → \(\boxed{52\,350}\)", r"<strong>Decenas:</strong> miramos las unidades (9 ≥ 5) → \(\boxed{52\,350}\)", r"<strong>Tens:</strong> look at the units (9 ≥ 5) → \(\boxed{52\,350}\)"),
       P(r"<strong>Centenes:</strong> mirem les desenes (4 < 5) → \(\boxed{52\,300}\)", r"<strong>Centenas:</strong> miramos las decenas (4 < 5) → \(\boxed{52\,300}\)", r"<strong>Hundreds:</strong> look at the tens (4 < 5) → \(\boxed{52\,300}\)"),
       P(r"<strong>Milers:</strong> mirem les centenes (3 < 5) → \(\boxed{52\,000}\)", r"<strong>Millares:</strong> miramos las centenas (3 < 5) → \(\boxed{52\,000}\)", r"<strong>Thousands:</strong> look at the hundreds (3 < 5) → \(\boxed{52\,000}\)")))
s2 += level(2, 3,
  prob(L(r"Una moto costa 18 750 €. Trunca i arrodoneix el preu a les unitats de miler. Quina aproximació té menys error?", r"Una moto cuesta 18 750 €. Trunca y redondea el precio a las unidades de millar. ¿Qué aproximación tiene menos error?", r"A motorbike costs €18,750. Truncate and round the price to the thousands. Which approximation has the smaller error?"),
       r'\[\tri{Truncament}{Truncamiento}{Truncated}:\ 18\,000\ €\qquad \tri{error}{error}{error}=18\,750-18\,000=750\ €\]',
       r'\[\tri{Arrodoniment}{Redondeo}{Rounded}:\ 19\,000\ €\qquad \tri{error}{error}{error}=19\,000-18\,750=250\ €\]',
       P(r"<strong>L'arrodoniment s'acosta més</strong> al preu real (250 € d'error en lloc de 750 €).", r"<strong>El redondeo se acerca más</strong> al precio real (250 € de error en lugar de 750 €).", r"<strong>Rounding gets closer</strong> to the real price (€250 error instead of €750).")),
  prob(L(r"Arrodoneix \(2996\) a les desenes i \(39\,970\) a les centenes.", r"Redondea \(2996\) a las decenas y \(39\,970\) a las centenas.", r"Round \(2996\) to the tens and \(39\,970\) to the hundreds."),
       P(r"\(299\fbox{6}\): com que 6 ≥ 5, sumem 1 a les desenes: 9 + 1 = 10. Es converteix en 0 i «en portem una» a les centenes, que també valen 9… i així fins als milers:", r"\(299\fbox{6}\): como 6 ≥ 5, sumamos 1 a las decenas: 9 + 1 = 10. Se convierte en 0 y «nos llevamos una» a las centenas, que también valen 9… y así hasta los millares:", r"\(299\fbox{6}\): since 6 ≥ 5, add 1 to the tens: 9 + 1 = 10. It becomes 0 and we “carry one” to the hundreds, which are also 9… and so on up to the thousands:") + r'\[2996\ \to\ \boxed{3000}\]',
       P(r"\(39\,9\fbox{7}0\): 7 ≥ 5, sumem 1 a les centenes (9) i ens en portem una fins a les desenes de miler:", r"\(39\,9\fbox{7}0\): 7 ≥ 5, sumamos 1 a las centenas (9) y nos llevamos una hasta las decenas de millar:", r"\(39\,9\fbox{7}0\): 7 ≥ 5, add 1 to the hundreds (9) and carry all the way to the ten thousands:") + r'\[39\,970\ \to\ \boxed{40\,000}\]'))
s2 += level(3, 5,
  prob(L(r"En arrodonir un nombre a les centenes hem obtingut \(3500\). Quin és el nombre més xicotet que podia ser? I el més gran?", r"Al redondear un número a las centenas hemos obtenido \(3500\). ¿Cuál es el número más pequeño que podía ser? ¿Y el mayor?", r"Rounding a number to the hundreds gave \(3500\). What is the smallest number it could have been? And the largest?"),
       P(r"Podia ser un nombre «de 34 centenes i escaig» que puja (desenes ≥ 5): el més xicotet és \(3450\).", r"Podía ser un número «de 34 centenas y pico» que sube (decenas ≥ 5): el menor es \(3450\).", r"It could be a number “34 hundred and something” that rounds up (tens ≥ 5): the smallest is \(3450\)."),
       P(r"O un nombre de 35 centenes que es queda igual (desenes < 5): el més gran és \(3549\).", r"O un número de 35 centenas que se queda igual (decenas < 5): el mayor es \(3549\).", r"Or a number with 35 hundreds that stays the same (tens < 5): the largest is \(3549\).")
       + r'\[\boxed{3450\ \le\ n\ \le\ 3549}\]'))
s2 += practice([
  ('★', L(r"a) Trunca a les desenes: \(4587\) i \(9999\). b) Arrodoneix a les centenes: \(6249\) i \(6250\).", r"a) Trunca a las decenas: \(4587\) y \(9999\). b) Redondea a las centenas: \(6249\) y \(6250\).", r"a) Truncate to the tens: \(4587\) and \(9999\). b) Round to the hundreds: \(6249\) and \(6250\).")),
  ('★★', L(r"c) Una ciutat té 825 948 habitants. Arrodoneix-ho a les desenes de miler i a les centenes de miler. d) Trunca i arrodoneix \(1495\) a les centenes.", r"c) Una ciudad tiene 825 948 habitantes. Redondéalo a las decenas de millar y a las centenas de millar. d) Trunca y redondea \(1495\) a las centenas.", r"c) A city has 825,948 inhabitants. Round it to the ten thousands and to the hundred thousands. d) Truncate and round \(1495\) to the hundreds.")),
  ('★★★', L(r"e) Escriu tres nombres que, arrodonits a les desenes de miler, donen \(60\,000\). f) Quan coincideixen el truncament i l'arrodoniment a les centenes?", r"e) Escribe tres números que, redondeados a las decenas de millar, den \(60\,000\). f) ¿Cuándo coinciden el truncamiento y el redondeo a las centenas?", r"e) Write three numbers that round to \(60\,000\) to the nearest ten thousand. f) When do truncating and rounding to the hundreds give the same result?"))],
  r'\[\text{a)}\ 4580,\ \ 9990\qquad \text{b)}\ 6200,\ \ 6300\]'
  + r'\[\text{c)}\ 830\,000,\ \ 800\,000\qquad \text{d)}\ 1400\ \ (\tri{truncament}{truncamiento}{truncated}),\ \ 1500\ \ (\tri{arrodoniment}{redondeo}{rounded})\]'
  + P(r"e) Qualsevol entre \(55\,000\) i \(64\,999\), per exemple \(57\,300\), \(60\,000\) i \(64\,120\). &nbsp; f) Quan la xifra de les desenes és 0, 1, 2, 3 o 4.", r"e) Cualquiera entre \(55\,000\) y \(64\,999\), por ejemplo \(57\,300\), \(60\,000\) y \(64\,120\). &nbsp; f) Cuando la cifra de las decenas es 0, 1, 2, 3 o 4.", r"e) Any number from \(55\,000\) to \(64\,999\), e.g. \(57\,300\), \(60\,000\) and \(64\,120\). &nbsp; f) When the tens digit is 0, 1, 2, 3 or 4."))

# ============================================================ 1.3
s3 = sub("Suma i resta", "Suma y resta", "Addition and subtraction")
s3 += box('def', L('Suma', 'Suma', 'Addition'),
  P(r"<strong>Sumar</strong> és ajuntar quantitats. Els nombres que sumem s'anomenen <strong>sumands</strong> i el resultat, <strong>suma</strong>.", r"<strong>Sumar</strong> es juntar cantidades. Los números que sumamos se llaman <strong>sumandos</strong> y el resultado, <strong>suma</strong>.", r"<strong>Adding</strong> means putting amounts together. The numbers we add are the <strong>addends</strong> and the result is the <strong>sum</strong>.")
  + r'\[\underbrace{347}_{\tri{sumand}{sumando}{addend}}+\underbrace{85}_{\tri{sumand}{sumando}{addend}}=\underbrace{432}_{\tri{suma}{suma}{sum}}\]')
s3 += box('prop', L('Propietats de la suma', 'Propiedades de la suma', 'Properties of addition'),
  ul(L(r"<strong>Commutativa:</strong> l'ordre dels sumands no canvia la suma. \(\ a+b=b+a\qquad 7+5=5+7=12\)", r"<strong>Conmutativa:</strong> el orden de los sumandos no altera la suma. \(\ a+b=b+a\qquad 7+5=5+7=12\)", r"<strong>Commutative:</strong> the order of the addends doesn't change the sum. \(\ a+b=b+a\qquad 7+5=5+7=12\)"),
       L(r"<strong>Associativa:</strong> podem agrupar els sumands com vulguem. \(\ (a+b)+c=a+(b+c)\)", r"<strong>Asociativa:</strong> podemos agrupar los sumandos como queramos. \(\ (a+b)+c=a+(b+c)\)", r"<strong>Associative:</strong> we can group the addends however we like. \(\ (a+b)+c=a+(b+c)\)"),
       L(r"<strong>Element neutre:</strong> sumar 0 no canvia res. \(\ a+0=a\)", r"<strong>Elemento neutro:</strong> sumar 0 no cambia nada. \(\ a+0=a\)", r"<strong>Identity:</strong> adding 0 changes nothing. \(\ a+0=a\)"))
  + note(r"Aquestes propietats ajuden a calcular de cap: \(\ 27+45+73=(27+73)+45=100+45=145\).", r"Estas propiedades ayudan a calcular mentalmente: \(\ 27+45+73=(27+73)+45=100+45=145\).", r"These properties help with mental maths: \(\ 27+45+73=(27+73)+45=100+45=145\).", '🧠'))
s3 += box('def', L('Resta', 'Resta', 'Subtraction'),
  P(r"<strong>Restar</strong> és llevar una quantitat d'una altra o calcular quant es diferencien dues quantitats.", r"<strong>Restar</strong> es quitar una cantidad de otra o calcular cuánto se diferencian dos cantidades.", r"<strong>Subtracting</strong> means taking one amount away from another or finding how much two amounts differ.")
  + r'\[\underbrace{532}_{\tri{minuend}{minuendo}{minuend}}-\underbrace{178}_{\tri{subtrahend}{sustraendo}{subtrahend}}=\underbrace{354}_{\tri{diferència}{diferencia}{difference}}\qquad \tri{Prova}{Prueba}{Check}:\ 354+178=532\ ✓\]'
  + ul(L(r"<strong>Prova de la resta:</strong> diferència + subtrahend = minuend.", r"<strong>Prueba de la resta:</strong> diferencia + sustraendo = minuendo.", r"<strong>Checking a subtraction:</strong> difference + subtrahend = minuend."),
       L(r"Amb nombres naturals, només podem restar si el minuend és <strong>major o igual</strong> que el subtrahend: \(5-8\) no dona un nombre natural.", r"Con números naturales, solo podemos restar si el minuendo es <strong>mayor o igual</strong> que el sustraendo: \(5-8\) no da un número natural.", r"With natural numbers, we can only subtract if the minuend is <strong>greater than or equal to</strong> the subtrahend: \(5-8\) isn't a natural number."),
       L(r"La resta <strong>no</strong> és commutativa: \(10-4\neq4-10\).", r"La resta <strong>no</strong> es conmutativa: \(10-4\neq4-10\).", r"Subtraction is <strong>not</strong> commutative: \(10-4\neq4-10\).")))
s3 += sub("Multiplicació", "Multiplicación", "Multiplication")
s3 += box('def', L('Multiplicació', 'Multiplicación', 'Multiplication'),
  P(r"<strong>Multiplicar</strong> és sumar un mateix nombre diverses vegades. Els nombres que multipliquem són els <strong>factors</strong> i el resultat, el <strong>producte</strong>. Escrivim el signe \(\cdot\) o \(\times\).", r"<strong>Multiplicar</strong> es sumar un mismo número varias veces. Los números que multiplicamos son los <strong>factores</strong> y el resultado, el <strong>producto</strong>. Escribimos el signo \(\cdot\) o \(\times\).", r"<strong>Multiplying</strong> means adding the same number several times. The numbers we multiply are the <strong>factors</strong> and the result is the <strong>product</strong>. We write \(\cdot\) or \(\times\).")
  + r'\[\underbrace{4}_{\tri{factor}{factor}{factor}}\cdot\underbrace{6}_{\tri{factor}{factor}{factor}}=6+6+6+6=\underbrace{24}_{\tri{producte}{producto}{product}}\]')
s3 += box('prop', L('Propietats de la multiplicació', 'Propiedades de la multiplicación', 'Properties of multiplication'),
  ul(L(r"<strong>Commutativa:</strong> \(\ a\cdot b=b\cdot a\qquad 3\cdot8=8\cdot3=24\)", r"<strong>Conmutativa:</strong> \(\ a\cdot b=b\cdot a\qquad 3\cdot8=8\cdot3=24\)", r"<strong>Commutative:</strong> \(\ a\cdot b=b\cdot a\qquad 3\cdot8=8\cdot3=24\)"),
       L(r"<strong>Associativa:</strong> \(\ (a\cdot b)\cdot c=a\cdot(b\cdot c)\qquad 25\cdot7\cdot4=(25\cdot4)\cdot7=700\)", r"<strong>Asociativa:</strong> \(\ (a\cdot b)\cdot c=a\cdot(b\cdot c)\qquad 25\cdot7\cdot4=(25\cdot4)\cdot7=700\)", r"<strong>Associative:</strong> \(\ (a\cdot b)\cdot c=a\cdot(b\cdot c)\qquad 25\cdot7\cdot4=(25\cdot4)\cdot7=700\)"),
       L(r"<strong>Element neutre:</strong> \(\ a\cdot1=a\). I qualsevol nombre per 0 dona 0: \(\ a\cdot0=0\).", r"<strong>Elemento neutro:</strong> \(\ a\cdot1=a\). Y cualquier número por 0 da 0: \(\ a\cdot0=0\).", r"<strong>Identity:</strong> \(\ a\cdot1=a\). And any number times 0 is 0: \(\ a\cdot0=0\)."),
       L(r"<strong>Distributiva:</strong> per a multiplicar un nombre per una suma (o una resta), el multipliquem per cada terme i després sumem (o restem):", r"<strong>Distributiva:</strong> para multiplicar un número por una suma (o una resta), lo multiplicamos por cada término y después sumamos (o restamos):", r"<strong>Distributive:</strong> to multiply a number by a sum (or a difference), multiply it by each term and then add (or subtract):")
       + r'\[a\cdot(b+c)=a\cdot b+a\cdot c\qquad 5\cdot(10+3)=50+15=65\]'
       + L(r"Llegida al revés, és <strong>traure factor comú</strong>: \(\ 7\cdot12+7\cdot8=7\cdot(12+8)=7\cdot20=140\).", r"Leída al revés, es <strong>sacar factor común</strong>: \(\ 7\cdot12+7\cdot8=7\cdot(12+8)=7\cdot20=140\).", r"Read backwards, it's <strong>taking out a common factor</strong>: \(\ 7\cdot12+7\cdot8=7\cdot(12+8)=7\cdot20=140\)."))
  + note(r"Per a multiplicar per 10, 100, 1000… afegim 1, 2, 3… zeros: \(\ 37\cdot100=3700\qquad 45\cdot1000=45\,000\).", r"Para multiplicar por 10, 100, 1000… añadimos 1, 2, 3… ceros: \(\ 37\cdot100=3700\qquad 45\cdot1000=45\,000\).", r"To multiply by 10, 100, 1000… add 1, 2, 3… zeros: \(\ 37\cdot100=3700\qquad 45\cdot1000=45\,000\).", '🧠'))
s3 += sub("Divisió", "División", "Division")
s3 += box('def', L('Divisió', 'División', 'Division'),
  P(r"<strong>Dividir</strong> és repartir una quantitat en parts iguals o veure quantes vegades cap un nombre dins d'un altre. Els termes són el <strong>dividend</strong> \(D\), el <strong>divisor</strong> \(d\), el <strong>quocient</strong> \(q\) i el <strong>residu</strong> \(r\), i sempre es compleix:",
    r"<strong>Dividir</strong> es repartir una cantidad en partes iguales o ver cuántas veces cabe un número dentro de otro. Los términos son el <strong>dividendo</strong> \(D\), el <strong>divisor</strong> \(d\), el <strong>cociente</strong> \(q\) y el <strong>resto</strong> \(r\), y siempre se cumple:",
    r"<strong>Dividing</strong> means sharing an amount into equal parts or finding how many times one number fits into another. Its terms are the <strong>dividend</strong> \(D\), the <strong>divisor</strong> \(d\), the <strong>quotient</strong> \(q\) and the <strong>remainder</strong> \(r\), and it's always true that:")
  + r'\[\boxed{\ D=d\cdot q+r\ }\qquad \tri{amb}{con}{with}\ \ r\lt d\]'
  + ul(L(r"Si \(r=0\), la divisió és <strong>exacta</strong>: \(\ 42:7=6\) perquè \(7\cdot6=42\).", r"Si \(r=0\), la división es <strong>exacta</strong>: \(\ 42:7=6\) porque \(7\cdot6=42\).", r"If \(r=0\), the division is <strong>exact</strong>: \(\ 42:7=6\) because \(7\cdot6=42\)."),
       L(r"Si \(r\neq0\), la divisió és <strong>entera</strong>: \(\ 38:5\) dona \(q=7\) i \(r=3\), perquè \(5\cdot7+3=38\).", r"Si \(r\neq0\), la división es <strong>entera</strong>: \(\ 38:5\) da \(q=7\) y \(r=3\), porque \(5\cdot7+3=38\).", r"If \(r\neq0\), there is a <strong>remainder</strong>: \(\ 38:5\) gives \(q=7\) and \(r=3\), because \(5\cdot7+3=38\)."),
       L(r"<strong>Mai</strong> es pot dividir entre 0.", r"<strong>Nunca</strong> se puede dividir entre 0.", r"You can <strong>never</strong> divide by 0."))
  + f'''<div class="widget" id="w-div">
  <div class="wt">➗ {L("Divisió: dividend, divisor, quocient i residu", "División: dividendo, divisor, cociente y resto", "Division: dividend, divisor, quotient and remainder")}</div>
  <div class="wrow"><label>{L("Dividend", "Dividendo", "Dividend")} <input class="tin s" type="text" inputmode="numeric" data-k="D" value="38" autocomplete="off" aria-label="D"></label><span class="op">:</span><label>{L("Divisor", "Divisor", "Divisor")} <input class="tin s" type="text" inputmode="numeric" data-k="d" value="5" autocomplete="off" aria-label="d"></label></div>
  {quick([("38:5", "38 : 5"), ("42:7", "42 : 7"), ("50:8", "50 : 8"), ("7:9", "7 : 9"), ("1375:12", "1375 : 12"), ("9876:32", "9876 : 32")])}
  <div class="cards"><div class="card"><h4>{L("Quocient", "Cociente", "Quotient")} q</h4><div data-o="q"></div></div><div class="card"><h4>{L("Residu", "Resto", "Remainder")} r</h4><div data-o="r"></div></div><div class="card"><h4>{L("Tipus", "Tipo", "Type")}</h4><div data-o="t"></div></div></div>
  <div class="dots"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s3 += sub("Operacions combinades", "Operaciones combinadas", "Combined operations")
s3 += box('prop', L("Jerarquia de les operacions", "Jerarquía de las operaciones", "Order of operations"),
  P(r"Quan en una expressió hi ha diverses operacions, les fem sempre en aquest <strong>ordre</strong>:", r"Cuando en una expresión hay varias operaciones, las hacemos siempre en este <strong>orden</strong>:", r"When an expression has several operations, we always do them in this <strong>order</strong>:")
  + '<ol>' + ''.join(f'<li>{x}</li>' for x in [
      L(r"<strong>Parèntesis</strong> \(\ (\ )\) i <strong>claudàtors</strong> \(\ [\ ]\), començant pels de dins.", r"<strong>Paréntesis</strong> \(\ (\ )\) y <strong>corchetes</strong> \(\ [\ ]\), empezando por los de dentro.", r"<strong>Brackets</strong> \(\ (\ )\) and \(\ [\ ]\), starting with the innermost."),
      L(r"<strong>Potències i arrels</strong> (les veurem en els apartats 1.5 i 1.8).", r"<strong>Potencias y raíces</strong> (las veremos en los apartados 1.5 y 1.8).", r"<strong>Powers and roots</strong> (see sections 1.5 and 1.8)."),
      L(r"<strong>Multiplicacions i divisions</strong>, d'esquerra a dreta.", r"<strong>Multiplicaciones y divisiones</strong>, de izquierda a derecha.", r"<strong>Multiplication and division</strong>, from left to right."),
      L(r"<strong>Sumes i restes</strong>, d'esquerra a dreta.", r"<strong>Sumas y restas</strong>, de izquierda a derecha.", r"<strong>Addition and subtraction</strong>, from left to right.")]) + '</ol>'
  + r'\[3+4\cdot5=3+20=23\qquad\qquad (3+4)\cdot5=7\cdot5=35\]'
  + note(r"Una ajuda per a recordar-ho: <strong>Pa-Po-MuDi-SuRe</strong> (Parèntesis, Potències, Multiplicacions i Divisions, Sumes i Restes).", r"Una ayuda para recordarlo: <strong>Pa-Po-MuDi-SuRe</strong> (Paréntesis, Potencias, Multiplicaciones y Divisiones, Sumas y Restas).", r"A memory aid: <strong>BIDMAS</strong> (Brackets, Indices, Division and Multiplication, Addition and Subtraction).", '🧠')
  + note(r"<strong>Compte!</strong> Les multiplicacions i divisions tenen la mateixa importància: es fan en l'ordre en què apareixen. \(\ 12:3\cdot2=4\cdot2=8\) (i no \(12:6=2\)).", r"<strong>¡Cuidado!</strong> Las multiplicaciones y divisiones tienen la misma importancia: se hacen en el orden en que aparecen. \(\ 12:3\cdot2=4\cdot2=8\) (y no \(12:6=2\)).", r"<strong>Careful!</strong> Multiplication and division have the same priority: do them in the order they appear. \(\ 12:3\cdot2=4\cdot2=8\) (not \(12:6=2\)).", '⚠️')
  + hier(["18-12:3+2·4", "3+4·5", "(3+4)·5", "12:3·2", "6·(9-4)-20:5", "50-[3·(12-7)+5]·2", "2·[15-(3+2)·2]+9:3"])
  + drill('comb', 'Entrena: operacions combinades', 'Entrena: operaciones combinadas', 'Train: combined operations'))
s3 += level(1, 1,
  prob(L(r"Calcula \(5307-2849\) i fes la prova.", r"Calcula \(5307-2849\) y haz la prueba.", r"Work out \(5307-2849\) and check it."),
       r'\[5307-2849=\boxed{2458}\]',
       r'\[\tri{Prova}{Prueba}{Check}:\ 2458+2849=5307\ ✓\]'),
  prob(L(r"Fes la divisió \(1375:12\) i comprova-la.", r"Haz la división \(1375:12\) y compruébala.", r"Work out \(1375:12\) and check it."),
       P(r"12 cap 114 vegades en 1375 i en sobren 7:", r"12 cabe 114 veces en 1375 y sobran 7:", r"12 goes into 1375 114 times with 7 left over:") + r'\[q=114,\qquad r=7\]',
       r'\[\tri{Prova}{Prueba}{Check}:\ 12\cdot114+7=1368+7=1375\ ✓\qquad (7<12\ ✓)\]'),
  prob(L(r"Calcula \(25\cdot(4+8)\) de dues maneres.", r"Calcula \(25\cdot(4+8)\) de dos maneras.", r"Work out \(25\cdot(4+8)\) in two ways."),
       r'\[\tri{Primer el parèntesi}{Primero el paréntesis}{Brackets first}:\ 25\cdot12=300\]',
       r'\[\tri{Propietat distributiva}{Propiedad distributiva}{Distributive property}:\ 25\cdot4+25\cdot8=100+200=\boxed{300}\]'))
s3 += level(2, 4,
  prob(r"\(18-12:3+2\cdot4\)",
       P(r"Primer les multiplicacions i divisions, d'esquerra a dreta:", r"Primero las multiplicaciones y divisiones, de izquierda a derecha:", r"First multiplication and division, from left to right:") + r'\[18-\underbrace{12:3}_{4}+\underbrace{2\cdot4}_{8}=18-4+8\]',
       P(r"Després les sumes i restes, d'esquerra a dreta:", r"Después las sumas y restas, de izquierda a derecha:", r"Then addition and subtraction, from left to right:") + r'\[\underbrace{18-4}_{14}+8=\boxed{22}\]'),
  prob(r"\(6\cdot(9-4)-20:5\)",
       r'\[6\cdot\underbrace{(9-4)}_{5}-20:5=\underbrace{6\cdot5}_{30}-\underbrace{20:5}_{4}\]',
       r'\[30-4=\boxed{26}\]'))
s3 += level(3, 6,
  prob(r"\(50-\left[3\cdot(12-7)+5\right]\cdot2\)",
       P(r"Comencem pel parèntesi de dins:", r"Empezamos por el paréntesis de dentro:", r"Start with the inner brackets:") + r'\[50-\left[3\cdot\underbrace{(12-7)}_{5}+5\right]\cdot2=50-\left[3\cdot5+5\right]\cdot2\]',
       P(r"Ara el claudàtor (dins: primer la multiplicació):", r"Ahora el corchete (dentro: primero la multiplicación):", r"Now the square brackets (inside: multiplication first):") + r'\[50-\left[\underbrace{15+5}_{20}\right]\cdot2=50-20\cdot2\]',
       r'\[50-\underbrace{20\cdot2}_{40}=\boxed{10}\]'),
  prob(L(r"Posa parèntesis perquè les igualtats siguen certes: a) \(3+4\cdot5-2=33\qquad\) b) \(3+4\cdot5-2=15\)", r"Pon paréntesis para que las igualdades sean ciertas: a) \(3+4\cdot5-2=33\qquad\) b) \(3+4\cdot5-2=15\)", r"Add brackets so that the equalities are true: a) \(3+4\cdot5-2=33\qquad\) b) \(3+4\cdot5-2=15\)"),
       P(r"a) Per a arribar a 33 necessitem multiplicar \(7\cdot5=35\) i restar 2:", r"a) Para llegar a 33 necesitamos multiplicar \(7\cdot5=35\) y restar 2:", r"a) To reach 33 we need \(7\cdot5=35\) and then subtract 2:") + r'\[\boxed{(3+4)\cdot5-2}=7\cdot5-2=35-2=33\ ✓\]',
       P(r"b) 15 és \(3+12\), i \(12=4\cdot3\):", r"b) 15 es \(3+12\), y \(12=4\cdot3\):", r"b) 15 is \(3+12\), and \(12=4\cdot3\):") + r'\[\boxed{3+4\cdot(5-2)}=3+4\cdot3=3+12=15\ ✓\]'))
s3 += practice([
  ('★', L(r"a) \(456+1289+74\qquad\) b) \(3000-1456\qquad\) c) \(236\cdot45\qquad\) d) \(9876:32\) (amb la prova)", r"a) \(456+1289+74\qquad\) b) \(3000-1456\qquad\) c) \(236\cdot45\qquad\) d) \(9876:32\) (con la prueba)", r"a) \(456+1289+74\qquad\) b) \(3000-1456\qquad\) c) \(236\cdot45\qquad\) d) \(9876:32\) (and check it)")),
  ('★★', r"e) \(7+3\cdot8-10:2\qquad\) f) \((7+3)\cdot8-10:2\qquad\) g) \(48:(6+2)\cdot3\)"),
  ('★★★', L(r"h) \(2\cdot\left[15-(3+2)\cdot2\right]+9:3\qquad\) i) En una divisió, el divisor és 15, el quocient 23 i el residu 9. Quin és el dividend? j) Podria ser 15 el residu?", r"h) \(2\cdot\left[15-(3+2)\cdot2\right]+9:3\qquad\) i) En una división, el divisor es 15, el cociente 23 y el resto 9. ¿Cuál es el dividendo? j) ¿Podría ser 15 el resto?", r"h) \(2\cdot\left[15-(3+2)\cdot2\right]+9:3\qquad\) i) In a division the divisor is 15, the quotient 23 and the remainder 9. What is the dividend? j) Could the remainder be 15?"))],
  r'\[\text{a)}\ 1819\qquad \text{b)}\ 1544\qquad \text{c)}\ 10\,620\qquad \text{d)}\ q=308,\ r=20\ \ (32\cdot308+20=9876)\]'
  + r'\[\text{e)}\ 7+24-5=26\qquad \text{f)}\ 80-5=75\qquad \text{g)}\ 48:8\cdot3=6\cdot3=18\]'
  + r'\[\text{h)}\ 2\cdot[15-10]+3=10+3=13\qquad \text{i)}\ D=15\cdot23+9=354\]'
  + P(r"j) No: el residu sempre és menor que el divisor. Si en sobraren 15, encara en cabria un grup més.", r"j) No: el resto siempre es menor que el divisor. Si sobraran 15, todavía cabría un grupo más.", r"j) No: the remainder is always less than the divisor. If 15 were left, one more group would fit."))

# ============================================================ 1.4
s4 = box('prop', L("Com resolem un problema? Quatre passos", "¿Cómo resolvemos un problema? Cuatro pasos", "How do we solve a problem? Four steps"),
  '<ol>' + ''.join(f'<li>{x}</li>' for x in [
    L(r"<strong>Llig i entén.</strong> Què em pregunten? Quines dades tinc? (Subratlla-les.)", r"<strong>Lee y entiende.</strong> ¿Qué me preguntan? ¿Qué datos tengo? (Subráyalos.)", r"<strong>Read and understand.</strong> What is the question? What information do I have? (Underline it.)"),
    L(r"<strong>Pensa un pla.</strong> Quines operacions he de fer i en quin ordre? Un dibuix o un esquema ajuda molt.", r"<strong>Piensa un plan.</strong> ¿Qué operaciones tengo que hacer y en qué orden? Un dibujo o un esquema ayuda mucho.", r"<strong>Make a plan.</strong> Which operations do I need and in what order? A drawing or diagram helps a lot."),
    L(r"<strong>Resol.</strong> Fes els càlculs amb ordre i escriu què calcules en cada pas.", r"<strong>Resuelve.</strong> Haz los cálculos con orden y escribe qué calculas en cada paso.", r"<strong>Solve.</strong> Do the calculations neatly and write what each step works out."),
    L(r"<strong>Comprova i respon.</strong> El resultat té sentit? Escriu la resposta amb una frase i amb les unitats (€, km, alumnes…).", r"<strong>Comprueba y responde.</strong> ¿El resultado tiene sentido? Escribe la respuesta con una frase y con las unidades (€, km, alumnos…).", r"<strong>Check and answer.</strong> Does the result make sense? Write the answer as a sentence with units (€, km, students…).")]) + '</ol>')
s4 += box('prop', L("Quina operació he de fer?", "¿Qué operación tengo que hacer?", "Which operation do I need?"),
  '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Si el problema diu…', 'Si el problema dice…', 'If the problem says…') + '</th><th>' + L('Operació', 'Operación', 'Operation') + '</th></tr></thead><tbody>'
  + '<tr><td class="l">' + L('ajuntar, afegir, en total, entre tots, rep més…', 'juntar, añadir, en total, entre todos, recibe más…', 'altogether, in total, more, plus, combined…') + '</td><td>➕</td></tr>'
  + '<tr><td class="l">' + L('llevar, gastar, quant en queda, quant falta, quants més que…', 'quitar, gastar, cuánto queda, cuánto falta, cuántos más que…', 'take away, spend, how many are left, how many more, how much more than…') + '</td><td>➖</td></tr>'
  + '<tr><td class="l">' + L('cada un… té…, vegades, el doble, el triple…', 'cada uno… tiene…, veces, el doble, el triple…', 'each… has…, times, double, triple…') + '</td><td>✖️</td></tr>'
  + '<tr><td class="l">' + L('repartir a parts iguals, quantes vegades cap, fer grups de…', 'repartir a partes iguales, cuántas veces cabe, hacer grupos de…', 'share equally, how many times does it fit, make groups of…') + '</td><td>➗</td></tr>'
  + '</tbody></table></div>'
  + note(r"En els problemes de dividir, pensa bé què has de fer amb el residu: de vegades cal <strong>afegir un grup més</strong> (autobusos) i de vegades <strong>no es compta</strong> (caixes plenes).", r"En los problemas de dividir, piensa bien qué tienes que hacer con el resto: a veces hay que <strong>añadir un grupo más</strong> (autobuses) y a veces <strong>no se cuenta</strong> (cajas llenas).", r"In division problems, think carefully about the remainder: sometimes you need <strong>one more group</strong> (coaches) and sometimes it <strong>doesn't count</strong> (full boxes).", '⚠️')
  + f'''<div class="widget" id="w-rest">
  <div class="wt">🚌 {L("Què fem amb el residu?", "¿Qué hacemos con el resto?", "What do we do with the remainder?")}</div>
  <div class="seg" role="group"><button type="button" data-k="bus" aria-pressed="true">🚌 {L("Autobusos", "Autobuses", "Coaches")}</button><button type="button" data-k="box" aria-pressed="false">🥚 {L("Caixes plenes", "Cajas llenas", "Full boxes")}</button><button type="button" data-k="share" aria-pressed="false">🍬 {L("Repartir", "Repartir", "Sharing")}</button></div>
  <div class="wrow" style="margin-top:10px"><label><span data-f="N"></span> <input class="tin s" type="text" inputmode="numeric" data-k="N" value="197" autocomplete="off" aria-label="N"></label><span class="op">:</span><label><span data-f="g"></span> <input class="tin s" type="text" inputmode="numeric" data-k="g" value="55" autocomplete="off" aria-label="g"></label></div>
  <div class="bxs"></div>
  <div class="info" aria-live="polite"></div>
</div>''')
s4 += level(1, 1,
  prob(L(r"Una biblioteca té 1245 llibres. Compra'n 380 de nous i en retira 95 de vells. Quants llibres té ara?", r"Una biblioteca tiene 1245 libros. Compra 380 nuevos y retira 95 viejos. ¿Cuántos libros tiene ahora?", r"A library has 1245 books. It buys 380 new ones and removes 95 old ones. How many books does it have now?"),
       r'\[1245+380=1625\ \ \tri{llibres}{libros}{books}\qquad 1625-95=1530\]',
       P(r"<strong>Ara té 1530 llibres.</strong> (En una sola expressió: \(1245+380-95=1530\).)", r"<strong>Ahora tiene 1530 libros.</strong> (En una sola expresión: \(1245+380-95=1530\).)", r"<strong>It now has 1530 books.</strong> (In one expression: \(1245+380-95=1530\).)")),
  prob(L(r"Un cine té 18 files de 24 butaques cada una. Quantes butaques hi ha?", r"Un cine tiene 18 filas de 24 butacas cada una. ¿Cuántas butacas hay?", r"A cinema has 18 rows of 24 seats each. How many seats are there?"),
       r'\[18\cdot24=\boxed{432}\ \tri{butaques}{butacas}{seats}\]'))
s4 += level(2, 3,
  prob(L(r"A una excursió van 185 alumnes i 12 professors. Els autobusos tenen 55 places. Quants autobusos calen?", r"A una excursión van 185 alumnos y 12 profesores. Los autobuses tienen 55 plazas. ¿Cuántos autobuses hacen falta?", r"185 students and 12 teachers are going on a trip. Coaches have 55 seats. How many coaches are needed?"),
       r'\[185+12=197\ \tri{persones}{personas}{people}\]',
       r'\[197:55\ \to\ q=3,\ r=32\qquad (55\cdot3+32=197)\]',
       P(r"Amb 3 autobusos es quedarien 32 persones a terra. <strong>Calen 4 autobusos.</strong>", r"Con 3 autobuses se quedarían 32 personas en tierra. <strong>Hacen falta 4 autobuses.</strong>", r"With 3 coaches, 32 people would be left behind. <strong>4 coaches are needed.</strong>")),
  prob(L(r"Marta compra 3 samarretes de 12 € i uns pantalons de 29 €. Paga amb un bitllet de 100 €. Quant li tornen?", r"Marta compra 3 camisetas de 12 € y unos pantalones de 29 €. Paga con un billete de 100 €. ¿Cuánto le devuelven?", r"Marta buys 3 T-shirts at €12 each and a pair of trousers for €29. She pays with a €100 note. How much change does she get?"),
       r'\[\tri{Gasta}{Gasta}{She spends}:\ 3\cdot12+29=36+29=65\ €\]',
       r'\[100-(3\cdot12+29)=100-65=\boxed{35\ €}\]'))
s4 += level(3, 5,
  prob(L(r"Un granger té 1350 ous. Els posa en caixes de 12 i ven cada caixa plena a 3 €. Quants diners guanya? Quants ous li sobren?", r"Un granjero tiene 1350 huevos. Los pone en cajas de 12 y vende cada caja llena a 3 €. ¿Cuánto dinero gana? ¿Cuántos huevos le sobran?", r"A farmer has 1350 eggs. He packs them in boxes of 12 and sells each full box for €3. How much money does he make? How many eggs are left over?"),
       r'\[1350:12\ \to\ q=112,\ r=6\qquad (12\cdot112+6=1350)\]',
       P(r"Omple 112 caixes (la que tindria 6 ous no està plena i no es ven):", r"Llena 112 cajas (la que tendría 6 huevos no está llena y no se vende):", r"He fills 112 boxes (the one with only 6 eggs isn't full and isn't sold):") + r'\[112\cdot3=336\ €\]',
       P(r"<strong>Guanya 336 € i li sobren 6 ous.</strong>", r"<strong>Gana 336 € y le sobran 6 huevos.</strong>", r"<strong>He makes €336 and has 6 eggs left over.</strong>")),
  prob(L(r"Tres amics compren un ordinador de 450 € i una impressora de 84 €. El primer paga 200 € i els altres dos es reparteixen a parts iguals el que falta. Quant paga cadascun?", r"Tres amigos compran un ordenador de 450 € y una impresora de 84 €. El primero paga 200 € y los otros dos se reparten a partes iguales lo que falta. ¿Cuánto paga cada uno?", r"Three friends buy a computer for €450 and a printer for €84. The first pays €200 and the other two split the rest equally. How much does each one pay?"),
       r'\[\tri{Total}{Total}{Total}:\ 450+84=534\ €\qquad \tri{Falta}{Falta}{Still to pay}:\ 534-200=334\ €\]',
       r'\[334:2=167\ €\]',
       P(r"<strong>El primer paga 200 € i els altres dos, 167 € cadascun.</strong> Comprovació: \(200+167+167=534\) ✓", r"<strong>El primero paga 200 € y los otros dos, 167 € cada uno.</strong> Comprobación: \(200+167+167=534\) ✓", r"<strong>The first pays €200 and the other two €167 each.</strong> Check: \(200+167+167=534\) ✓")))
s4 += practice([
  ('★', L(r"a) Un tren té 8 vagons de 64 seients. Quants seients hi ha? b) Joan té 1250 cromos i en regala 375. Quants li'n queden?", r"a) Un tren tiene 8 vagones de 64 asientos. ¿Cuántos asientos hay? b) Juan tiene 1250 cromos y regala 375. ¿Cuántos le quedan?", r"a) A train has 8 carriages with 64 seats each. How many seats are there? b) Joan has 1250 stickers and gives away 375. How many are left?")),
  ('★★', L(r"c) Una fàbrica fa 1440 llapis al dia i els empaqueta en capses de 24. Quantes capses omple? d) Repartim 250 caramels entre 23 xiquets. Quants en rep cadascun? En sobren?", r"c) Una fábrica hace 1440 lápices al día y los empaqueta en cajas de 24. ¿Cuántas cajas llena? d) Repartimos 250 caramelos entre 23 niños. ¿Cuántos recibe cada uno? ¿Sobran?", r"c) A factory makes 1440 pencils a day and packs them in boxes of 24. How many boxes does it fill? d) We share 250 sweets among 23 children. How many does each get? Are any left?")),
  ('★★★', L(r"e) Una família estalvia 85 € cada mes. Quant estalvia en 3 anys? Si volen una tele de 2750 €, quants mesos hauran d'estalviar? f) Un llibre té 288 pàgines. Llig 12 pàgines cada dia de dilluns a divendres i 20 pàgines cada dia del cap de setmana. En quantes setmanes l'acaba?", r"e) Una familia ahorra 85 € cada mes. ¿Cuánto ahorra en 3 años? Si quieren una tele de 2750 €, ¿cuántos meses tendrán que ahorrar? f) Un libro tiene 288 páginas. Lee 12 páginas cada día de lunes a viernes y 20 páginas cada día del fin de semana. ¿En cuántas semanas lo acaba?", r"e) A family saves €85 every month. How much do they save in 3 years? If they want a €2750 TV, how many months must they save? f) A book has 288 pages. I read 12 pages a day Monday to Friday and 20 pages a day at the weekend. How many weeks does it take me to finish?"))],
  r'\[\text{a)}\ 8\cdot64=512\qquad \text{b)}\ 1250-375=875\qquad \text{c)}\ 1440:24=60\qquad \text{d)}\ 250=23\cdot10+20\]'
  + P(r"d) Cadascun en rep 10 i en sobren 20.", r"d) Cada uno recibe 10 y sobran 20.", r"d) Each gets 10 and 20 are left over.")
  + r'\[\text{e)}\ 85\cdot36=3060\ €\qquad 2750:85\to q=32,\ r=30\]'
  + P(r"e) Amb 32 mesos encara no arriben (falten 30 €): necessiten <strong>33 mesos</strong>.", r"e) Con 32 meses todavía no llegan (faltan 30 €): necesitan <strong>33 meses</strong>.", r"e) 32 months isn't quite enough (€30 short): they need <strong>33 months</strong>.")
  + r'\[\text{f)}\ 5\cdot12+2\cdot20=100\ \tri{pàgines per setmana}{páginas por semana}{pages a week}\qquad 288:100\to q=2,\ r=88\]'
  + P(r"f) En 2 setmanes en llig 200; les 88 que falten les acaba durant la <strong>tercera setmana</strong>.", r"f) En 2 semanas lee 200; las 88 que faltan las acaba durante la <strong>tercera semana</strong>.", r"f) In 2 weeks I read 200; I finish the remaining 88 during the <strong>third week</strong>."))

# ============================================================ 1.5
s5 = box('def', L('Potència', 'Potencia', 'Power'),
  P(r"Una <strong>potència</strong> és una manera curta d'escriure una multiplicació de <strong>factors iguals</strong>:", r"Una <strong>potencia</strong> es una forma corta de escribir una multiplicación de <strong>factores iguales</strong>:", r"A <strong>power</strong> is a short way of writing a multiplication of <strong>equal factors</strong>:")
  + r'\[a^{n}=\underbrace{a\cdot a\cdot a\cdots a}_{n\ \tri{vegades}{veces}{times}}\qquad\qquad 2^{5}=2\cdot2\cdot2\cdot2\cdot2=32\]'
  + ul(L(r"La <strong>base</strong> \(a\) és el factor que es repeteix.", r"La <strong>base</strong> \(a\) es el factor que se repite.", r"The <strong>base</strong> \(a\) is the factor being repeated."),
       L(r"L'<strong>exponent</strong> \(n\) indica quantes vegades es repeteix.", r"El <strong>exponente</strong> \(n\) indica cuántas veces se repite.", r"The <strong>exponent</strong> \(n\) tells us how many times it is repeated."))
  + P(r"\(2^5\) es llig «dos elevat a cinc». Quan l'exponent és 2 diem «<strong>al quadrat</strong>» (\(7^2\): set al quadrat) i quan és 3, «<strong>al cub</strong>» (\(4^3\): quatre al cub).", r"\(2^5\) se lee «dos elevado a cinco». Cuando el exponente es 2 decimos «<strong>al cuadrado</strong>» (\(7^2\): siete al cuadrado) y cuando es 3, «<strong>al cubo</strong>» (\(4^3\): cuatro al cubo).", r"\(2^5\) is read “two to the power of five”. When the exponent is 2 we say “<strong>squared</strong>” (\(7^2\): seven squared) and when it is 3, “<strong>cubed</strong>” (\(4^3\): four cubed)."))
s5 += box('prop', L("Per què «quadrat» i «cub»?", "¿Por qué «cuadrado» y «cubo»?", "Why “squared” and “cubed”?"),
  P(r"Un quadrat de costat 4 està format per \(4\cdot4=4^2=16\) quadradets. Un cub d'aresta 4 està format per \(4\cdot4\cdot4=4^3=64\) cubets.", r"Un cuadrado de lado 4 está formado por \(4\cdot4=4^2=16\) cuadraditos. Un cubo de arista 4 está formado por \(4\cdot4\cdot4=4^3=64\) cubitos.", r"A square with side 4 is made of \(4\cdot4=4^2=16\) little squares. A cube with edge 4 is made of \(4\cdot4\cdot4=4^3=64\) little cubes.")
  + ul(L(r"Exponent 1: \(\ a^1=a\qquad 9^1=9\)", r"Exponente 1: \(\ a^1=a\qquad 9^1=9\)", r"Exponent 1: \(\ a^1=a\qquad 9^1=9\)"),
       L(r"Base 1: \(\ 1^n=1\qquad 1^{50}=1\)", r"Base 1: \(\ 1^n=1\qquad 1^{50}=1\)", r"Base 1: \(\ 1^n=1\qquad 1^{50}=1\)"),
       L(r"Base 0: \(\ 0^n=0\qquad 0^{8}=0\)", r"Base 0: \(\ 0^n=0\qquad 0^{8}=0\)", r"Base 0: \(\ 0^n=0\qquad 0^{8}=0\)"))
  + '<div class="tbl-wrap"><table class="data sq"><thead><tr><th>\\(n\\)</th>' + ''.join(f'<th>{i}</th>' for i in range(1, 13)) + '</tr></thead><tbody>'
  + '<tr><th>\\(n^2\\)</th>' + ''.join(f'<td>{i*i}</td>' for i in range(1, 13)) + '</tr>'
  + '<tr><th>\\(n^3\\)</th>' + ''.join(f'<td>{i**3}</td>' if i <= 10 else '<td>—</td>' for i in range(1, 13)) + '</tr></tbody></table></div>'
  + note(r"<strong>Compte!</strong> \(2^3\neq2\cdot3\). &nbsp; \(2^3=2\cdot2\cdot2=8\), mentre que \(2\cdot3=6\). L'exponent no multiplica la base: diu quantes vegades es repeteix.", r"<strong>¡Cuidado!</strong> \(2^3\neq2\cdot3\). &nbsp; \(2^3=2\cdot2\cdot2=8\), mientras que \(2\cdot3=6\). El exponente no multiplica la base: dice cuántas veces se repite.", r"<strong>Careful!</strong> \(2^3\neq2\cdot3\). &nbsp; \(2^3=2\cdot2\cdot2=8\), whereas \(2\cdot3=6\). The exponent doesn't multiply the base: it says how many times it's repeated.", '⚠️')
  + f'''<div class="widget" id="w-pow">
  <div class="wt">🧱 {L("Construeix una potència", "Construye una potencia", "Build a power")}</div>
  <div class="wrow"><label>{L("Base", "Base", "Base")} <input type="range" min="0" max="12" value="3" data-k="a" aria-label="base"> <output data-v="a">3</output></label><label>{L("Exponent", "Exponente", "Exponent")} <input type="range" min="1" max="8" value="2" data-k="n" aria-label="exponent"> <output data-v="n">2</output></label></div>
  <div class="info" aria-live="polite"></div>
  <div class="pvis"></div>
  <div class="pchain"></div>
</div>
''' + drill('pow', 'Entrena: calcula la potència', 'Entrena: calcula la potencia', 'Train: work out the power'))
s5 += level(1, 1,
  prob(L(r"Escriu en forma de potència i calcula: a) \(3\cdot3\cdot3\cdot3\qquad\) b) \(10\cdot10\cdot10\qquad\) c) \(7\cdot7\)", r"Escribe en forma de potencia y calcula: a) \(3\cdot3\cdot3\cdot3\qquad\) b) \(10\cdot10\cdot10\qquad\) c) \(7\cdot7\)", r"Write as a power and work out: a) \(3\cdot3\cdot3\cdot3\qquad\) b) \(10\cdot10\cdot10\qquad\) c) \(7\cdot7\)"),
       P(r"Comptem quantes vegades es repeteix el factor: aquest és l'exponent.", r"Contamos cuántas veces se repite el factor: ese es el exponente.", r"Count how many times the factor is repeated: that's the exponent."),
       r'\[\text{a)}\ 3^4=81\qquad \text{b)}\ 10^3=1000\qquad \text{c)}\ 7^2=49\]'),
  prob(L(r"Escriu com es lligen i calcula: \(5^3\) i \(2^6\).", r"Escribe cómo se leen y calcula: \(5^3\) y \(2^6\).", r"Write how they are read and work them out: \(5^3\) and \(2^6\)."),
       P(r"\(5^3\): «cinc al cub» \(=5\cdot5\cdot5=\boxed{125}\)", r"\(5^3\): «cinco al cubo» \(=5\cdot5\cdot5=\boxed{125}\)", r"\(5^3\): “five cubed” \(=5\cdot5\cdot5=\boxed{125}\)"),
       P(r"\(2^6\): «dos elevat a sis» \(=2\cdot2\cdot2\cdot2\cdot2\cdot2=\boxed{64}\)", r"\(2^6\): «dos elevado a seis» \(=2\cdot2\cdot2\cdot2\cdot2\cdot2=\boxed{64}\)", r"\(2^6\): “two to the power of six” \(=2\cdot2\cdot2\cdot2\cdot2\cdot2=\boxed{64}\)")))
s5 += level(2, 3,
  prob(L(r"Calcula: \(1^{20},\ \ 0^{7},\ \ 13^{1},\ \ 2^{10}\).", r"Calcula: \(1^{20},\ \ 0^{7},\ \ 13^{1},\ \ 2^{10}\).", r"Work out: \(1^{20},\ \ 0^{7},\ \ 13^{1},\ \ 2^{10}\)."),
       r'\[1^{20}=1\qquad 0^{7}=0\qquad 13^{1}=13\]',
       P(r"Per a \(2^{10}\) anem doblant: 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024.", r"Para \(2^{10}\) vamos doblando: 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024.", r"For \(2^{10}\) keep doubling: 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024.") + r'\[2^{10}=\boxed{1024}\]'),
  prob(L(r"Ordena de menor a major: \(\ 2^5,\ \ 5^2,\ \ 3^3,\ \ 4^2\).", r"Ordena de menor a mayor: \(\ 2^5,\ \ 5^2,\ \ 3^3,\ \ 4^2\).", r"Order from smallest to largest: \(\ 2^5,\ \ 5^2,\ \ 3^3,\ \ 4^2\)."),
       r'\[2^5=32\qquad 5^2=25\qquad 3^3=27\qquad 4^2=16\]',
       r'\[\boxed{4^2<5^2<3^3<2^5}\]'))
s5 += level(3, 5,
  prob(L(r"En un edifici hi ha 4 plantes; en cada planta, 4 pisos; en cada pis, 4 habitacions, i en cada habitació, 4 finestres. Quantes finestres hi ha? Expressa-ho amb una potència.", r"En un edificio hay 4 plantas; en cada planta, 4 pisos; en cada piso, 4 habitaciones, y en cada habitación, 4 ventanas. ¿Cuántas ventanas hay? Exprésalo con una potencia.", r"A building has 4 floors; each floor has 4 flats; each flat has 4 rooms, and each room has 4 windows. How many windows are there? Write it as a power."),
       r'\[\underbrace{4}_{\tri{plantes}{plantas}{floors}}\cdot\underbrace{4}_{\tri{pisos}{pisos}{flats}}\cdot\underbrace{4}_{\tri{habitacions}{habitaciones}{rooms}}\cdot\underbrace{4}_{\tri{finestres}{ventanas}{windows}}=4^4\]',
       r'\[4^4=16\cdot16=\boxed{256}\ \tri{finestres}{ventanas}{windows}\]'))
s5 += practice([
  ('★', r"a) \(6^2\) &nbsp; b) \(2^4\) &nbsp; c) \(10^5\) &nbsp; d) \(4^3\)"),
  ('★★', L(r"e) Escriu com a potència: 8, 27, 125, 1000 i 81. f) Què és més gran, \(2^4\) o \(4^2\)?", r"e) Escribe como potencia: 8, 27, 125, 1000 y 81. f) ¿Qué es mayor, \(2^4\) o \(4^2\)?", r"e) Write as a power: 8, 27, 125, 1000 and 81. f) Which is bigger, \(2^4\) or \(4^2\)?")),
  ('★★★', L(r"g) Escriu 64 com a potència de tres maneres diferents. h) Calcula l'àrea d'un quadrat de 12 cm de costat i el volum d'un cub de 5 cm d'aresta.", r"g) Escribe 64 como potencia de tres maneras diferentes. h) Calcula el área de un cuadrado de 12 cm de lado y el volumen de un cubo de 5 cm de arista.", r"g) Write 64 as a power in three different ways. h) Find the area of a square with 12 cm sides and the volume of a cube with 5 cm edges."))],
  r'\[\text{a)}\ 36\qquad \text{b)}\ 16\qquad \text{c)}\ 100\,000\qquad \text{d)}\ 64\]'
  + r'\[\text{e)}\ 2^3,\ \ 3^3,\ \ 5^3,\ \ 10^3,\ \ 9^2=3^4\qquad \text{f)}\ \tri{Són iguals}{Son iguales}{They are equal}:\ 2^4=4^2=16\]'
  + r'\[\text{g)}\ 8^2=4^3=2^6\qquad \text{h)}\ 12^2=144\ \text{cm}^2,\qquad 5^3=125\ \text{cm}^3\]')

# ============================================================ 1.6
s6 = box('def', L('Potències de 10', 'Potencias de 10', 'Powers of 10'),
  P(r"Les potències de base 10 són les més fàcils de calcular: <strong>\(10^n\) és un 1 seguit de \(n\) zeros</strong>.", r"Las potencias de base 10 son las más fáciles de calcular: <strong>\(10^n\) es un 1 seguido de \(n\) ceros</strong>.", r"Powers of 10 are the easiest to work out: <strong>\(10^n\) is a 1 followed by \(n\) zeros</strong>.")
  + '<div class="tbl-wrap"><table class="data"><thead><tr><th>' + L('Potència', 'Potencia', 'Power') + '</th>' + ''.join(f'<th>\\(10^{{{i}}}\\)</th>' for i in [1, 2, 3, 4, 5, 6, 9]) + '</tr></thead><tbody>'
  + '<tr><th>' + L('Valor', 'Valor', 'Value') + '</th>' + ''.join(f'<td>\\({v}\\)</td>' for v in ['10', '100', '1000', r'10\,000', r'100\,000', r'1\,000\,000', r'1\,000\,000\,000']) + '</tr>'
  + '<tr><th>' + L('Es llig', 'Se lee', 'In words') + '</th>' + ''.join(f'<td style="font-size:.78rem">{t}</td>' for t in [L('deu', 'diez', 'ten'), L('cent', 'cien', 'a hundred'), L('mil', 'mil', 'a thousand'), L('deu mil', 'diez mil', 'ten thousand'), L('cent mil', 'cien mil', 'a hundred thousand'), L('un milió', 'un millón', 'a million'), L('mil milions', 'mil millones', 'a billion')]) + '</tr>'
  + '</tbody></table></div>')
s6 += sub("Expressió abreujada de nombres grans", "Expresión abreviada de números grandes", "Writing large numbers in short form")
s6 += box('def', L('Expressió abreujada', 'Expresión abreviada', 'Short form'),
  P(r"Un nombre acabat en zeros es pot escriure com un nombre <strong>multiplicat per una potència de 10</strong>. Només hem de <strong>comptar els zeros del final</strong>:", r"Un número acabado en ceros se puede escribir como un número <strong>multiplicado por una potencia de 10</strong>. Solo tenemos que <strong>contar los ceros del final</strong>:", r"A number ending in zeros can be written as a number <strong>multiplied by a power of 10</strong>. We just <strong>count the zeros at the end</strong>:")
  + r'\[5\,000\,000=5\cdot10^{6}\qquad 340\,000=34\cdot10^{4}\qquad 3\,060\,000=306\cdot10^{4}\]'
  + P(r"Així és més fàcil escriure nombres molt grans. Per exemple, la distància de la Terra al Sol és d'uns \(150\,000\,000\) km \(=15\cdot10^{7}\) km. I al revés: \(7\cdot10^{5}=700\,000\).", r"Así es más fácil escribir números muy grandes. Por ejemplo, la distancia de la Tierra al Sol es de unos \(150\,000\,000\) km \(=15\cdot10^{7}\) km. Y al revés: \(7\cdot10^{5}=700\,000\).", r"This makes very large numbers easier to write. For example, the Earth is about \(150\,000\,000\) km \(=15\cdot10^{7}\) km from the Sun. And the other way round: \(7\cdot10^{5}=700\,000\)."))
s6 += sub("Descomposició polinòmica d'un nombre", "Descomposición polinómica de un número", "Expanded form with powers of 10")
s6 += box('def', L('Descomposició polinòmica', 'Descomposición polinómica', 'Expanded (polynomial) form'),
  P(r"Com que \(1\ \text{D}=10\), \(1\ \text{C}=10^2\), \(1\ \text{UM}=10^3\)…, podem escriure qualsevol nombre com la <strong>suma de cada xifra multiplicada per la potència de 10 del seu lloc</strong>:", r"Como \(1\ \text{D}=10\), \(1\ \text{C}=10^2\), \(1\ \text{UM}=10^3\)…, podemos escribir cualquier número como la <strong>suma de cada cifra multiplicada por la potencia de 10 de su lugar</strong>:", r"Since \(1\ \text{T}=10\), \(1\ \text{H}=10^2\), \(1\ \text{Th}=10^3\)…, we can write any number as the <strong>sum of each digit times the power of 10 of its place</strong>:")
  + r'\[3705=3\cdot10^{3}+7\cdot10^{2}+0\cdot10+5=3\cdot10^{3}+7\cdot10^{2}+5\]'
  + r'\[48\,503=4\cdot10^{4}+8\cdot10^{3}+5\cdot10^{2}+3\]'
  + note(r"Els termes amb xifra 0 no fa falta escriure'ls, però <strong>no</strong> ens podem descuidar de cap potència quan tornem a escriure el nombre: \(6\cdot10^{5}+4\cdot10^{3}+7\cdot10+2=604\,072\).", r"Los términos con cifra 0 no hace falta escribirlos, pero <strong>no</strong> podemos olvidar ninguna potencia cuando volvemos a escribir el número: \(6\cdot10^{5}+4\cdot10^{3}+7\cdot10+2=604\,072\).", r"Terms with a 0 digit can be left out, but we must <strong>not</strong> forget any place when we write the number back: \(6\cdot10^{5}+4\cdot10^{3}+7\cdot10+2=604\,072\).", '⚠️')
  + f'''<div class="widget" id="w-ten">
  <div class="wt">🔟 {L("Potències de 10 en acció", "Potencias de 10 en acción", "Powers of 10 in action")}</div>
  <div class="wrow"><div class="seg" role="group"><button type="button" data-k="abbr" aria-pressed="true">{L("Expressió abreujada", "Expresión abreviada", "Short form")}</button><button type="button" data-k="poly" aria-pressed="false">{L("Descomposició polinòmica", "Descomposición polinómica", "Expanded form")}</button></div>
  <label>{L("Nombre", "Número", "Number")} <input class="tin w" type="text" inputmode="numeric" value="45000000" autocomplete="off" aria-label="nombre"></label></div>
  <div class="quick"><span class="ql">⚡</span><button type="button" data-m="abbr" data-b="150000000">150 000 000</button><button type="button" data-m="abbr" data-b="340000">340 000</button><button type="button" data-m="abbr" data-b="3060000">3 060 000</button><button type="button" data-m="poly" data-b="3705">3705</button><button type="button" data-m="poly" data-b="48503">48 503</button><button type="button" data-m="poly" data-b="2000900">2 000 900</button></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('ten', 'Entrena: potències de 10', 'Entrena: potencias de 10', 'Train: powers of 10'))
s6 += level(1, 1,
  prob(L(r"Calcula \(10^4\) i \(10^7\).", r"Calcula \(10^4\) y \(10^7\).", r"Work out \(10^4\) and \(10^7\)."),
       r'\[10^4=\boxed{10\,000}\ \ (4\ \tri{zeros}{ceros}{zeros})\qquad 10^7=\boxed{10\,000\,000}\ \ (7\ \tri{zeros}{ceros}{zeros})\]'),
  prob(L(r"Escriu de forma abreujada: \(8\,000\,000\), \(52\,000\) i \(3\,060\,000\).", r"Escribe de forma abreviada: \(8\,000\,000\), \(52\,000\) y \(3\,060\,000\).", r"Write in short form: \(8\,000\,000\), \(52\,000\) and \(3\,060\,000\)."),
       P(r"Comptem els zeros del final (en \(3\,060\,000\), el 0 del mig no compta perquè no està al final):", r"Contamos los ceros del final (en \(3\,060\,000\), el 0 del medio no cuenta porque no está al final):", r"Count the zeros at the end (in \(3\,060\,000\), the middle 0 doesn't count because it's not at the end):")
       + r'\[8\cdot10^{6}\qquad 52\cdot10^{3}\qquad 306\cdot10^{4}\]'))
s6 += level(2, 3,
  prob(L(r"Fes la descomposició polinòmica de \(48\,503\) i de \(2\,000\,900\).", r"Haz la descomposición polinómica de \(48\,503\) y de \(2\,000\,900\).", r"Write \(48\,503\) and \(2\,000\,900\) in expanded form."),
       r'\[48\,503=4\cdot10^{4}+8\cdot10^{3}+5\cdot10^{2}+0\cdot10+3=\boxed{4\cdot10^{4}+8\cdot10^{3}+5\cdot10^{2}+3}\]',
       r'\[2\,000\,900=\boxed{2\cdot10^{6}+9\cdot10^{2}}\]'),
  prob(L(r"Quin nombre és \(6\cdot10^{5}+4\cdot10^{3}+7\cdot10+2\)?", r"¿Qué número es \(6\cdot10^{5}+4\cdot10^{3}+7\cdot10+2\)?", r"Which number is \(6\cdot10^{5}+4\cdot10^{3}+7\cdot10+2\)?"),
       P(r"Posem cada xifra en el seu lloc i omplim amb zeros els llocs que falten (\(10^4\) i \(10^2\)):", r"Ponemos cada cifra en su lugar y rellenamos con ceros los lugares que faltan (\(10^4\) y \(10^2\)):", r"Put each digit in its place and fill the missing places (\(10^4\) and \(10^2\)) with zeros:")
       + r'\[600\,000+4000+70+2=\boxed{604\,072}\]'))
s6 += level(3, 5,
  prob(L(r"El cor d'una persona batega unes \(100\,000\) vegades al dia. Quantes vegades batega en \(1000\) dies? Expressa-ho amb potències de 10.", r"El corazón de una persona late unas \(100\,000\) veces al día. ¿Cuántas veces late en \(1000\) días? Exprésalo con potencias de 10.", r"A person's heart beats about \(100\,000\) times a day. How many times does it beat in \(1000\) days? Use powers of 10."),
       r'\[100\,000\cdot1000=10^{5}\cdot10^{3}\]',
       P(r"Multiplicar per \(10^3\) és afegir 3 zeros més: en total, \(5+3=8\) zeros.", r"Multiplicar por \(10^3\) es añadir 3 ceros más: en total, \(5+3=8\) ceros.", r"Multiplying by \(10^3\) adds 3 more zeros: \(5+3=8\) zeros in total.") + r'\[10^{8}=\boxed{100\,000\,000}\ \tri{batecs}{latidos}{beats}\]'))
s6 += practice([
  ('★', L(r"a) Escriu \(10^5\) i \(10^8\). b) Calcula \(9\cdot10^{4}\) i \(12\cdot10^{6}\).", r"a) Escribe \(10^5\) y \(10^8\). b) Calcula \(9\cdot10^{4}\) y \(12\cdot10^{6}\).", r"a) Write out \(10^5\) and \(10^8\). b) Work out \(9\cdot10^{4}\) and \(12\cdot10^{6}\).")),
  ('★★', L(r"c) Descomposició polinòmica de \(7080\) i de \(90\,315\). d) Quin nombre és \(3\cdot10^{4}+5\cdot10^{2}\)?", r"c) Descomposición polinómica de \(7080\) y de \(90\,315\). d) ¿Qué número es \(3\cdot10^{4}+5\cdot10^{2}\)?", r"c) Expanded form of \(7080\) and \(90\,315\). d) Which number is \(3\cdot10^{4}+5\cdot10^{2}\)?")),
  ('★★★', L(r"e) Una ciutat té uns \(800\,000\) habitants i cadascun gasta uns 100 litres d'aigua al dia. Quants litres gasta la ciutat cada dia? f) Quantes xifres té \(10^{20}\)?", r"e) Una ciudad tiene unos \(800\,000\) habitantes y cada uno gasta unos 100 litros de agua al día. ¿Cuántos litros gasta la ciudad cada día? f) ¿Cuántas cifras tiene \(10^{20}\)?", r"e) A city has about \(800\,000\) inhabitants and each uses about 100 litres of water a day. How many litres does the city use each day? f) How many digits does \(10^{20}\) have?"))],
  r'\[\text{a)}\ 100\,000,\ \ 100\,000\,000\qquad \text{b)}\ 90\,000,\ \ 12\,000\,000\]'
  + r'\[\text{c)}\ 7\cdot10^{3}+8\cdot10\qquad 9\cdot10^{4}+3\cdot10^{2}+1\cdot10+5\qquad \text{d)}\ 30\,500\]'
  + r'\[\text{e)}\ 8\cdot10^{5}\cdot10^{2}=8\cdot10^{7}=80\,000\,000\ \text{L}\qquad \text{f)}\ 21\ \tri{xifres (un 1 i 20 zeros)}{cifras (un 1 y 20 ceros)}{digits (a 1 and 20 zeros)}\]')

# ============================================================ 1.7
def prop_box(t3, rule3, formula, example):
    return box('def', t3, P(*rule3) + formula + example)
s7 = P(r"Les potències tenen unes <strong>propietats</strong> que ens permeten calcular més ràpid, sense fer totes les multiplicacions. Totes es poden entendre escrivint les potències com a multiplicacions.", r"Las potencias tienen unas <strong>propiedades</strong> que nos permiten calcular más rápido, sin hacer todas las multiplicaciones. Todas se pueden entender escribiendo las potencias como multiplicaciones.", r"Powers have some <strong>properties</strong> that let us calculate faster, without doing every multiplication. Each one makes sense if we write the powers out as multiplications.")
s7 += prop_box(L('1. Producte de potències de la mateixa base', '1. Producto de potencias de la misma base', '1. Multiplying powers with the same base'),
  (r"Es deixa la mateixa base i <strong>se sumen els exponents</strong>:", r"Se deja la misma base y <strong>se suman los exponentes</strong>:", r"Keep the base and <strong>add the exponents</strong>:"),
  r'\[\boxed{a^{m}\cdot a^{n}=a^{m+n}}\]', r'\[2^{3}\cdot2^{2}=(2\cdot2\cdot2)\cdot(2\cdot2)=2^{5}\]')
s7 += prop_box(L('2. Quocient de potències de la mateixa base', '2. Cociente de potencias de la misma base', '2. Dividing powers with the same base'),
  (r"Es deixa la mateixa base i <strong>es resten els exponents</strong> (el del dividend menys el del divisor):", r"Se deja la misma base y <strong>se restan los exponentes</strong> (el del dividendo menos el del divisor):", r"Keep the base and <strong>subtract the exponents</strong> (top minus bottom):"),
  r'\[\boxed{a^{m}:a^{n}=a^{m-n}}\]', r'\[5^{6}:5^{4}=\frac{\cancel{5}\cdot\cancel{5}\cdot\cancel{5}\cdot\cancel{5}\cdot5\cdot5}{\cancel{5}\cdot\cancel{5}\cdot\cancel{5}\cdot\cancel{5}}=5^{2}\]')
s7 += prop_box(L("3. Potència d'una potència", '3. Potencia de una potencia', '3. Power of a power'),
  (r"Es deixa la base i <strong>es multipliquen els exponents</strong>:", r"Se deja la base y <strong>se multiplican los exponentes</strong>:", r"Keep the base and <strong>multiply the exponents</strong>:"),
  r'\[\boxed{\left(a^{m}\right)^{n}=a^{m\cdot n}}\]', r'\[\left(3^{2}\right)^{4}=3^{2}\cdot3^{2}\cdot3^{2}\cdot3^{2}=3^{2+2+2+2}=3^{8}\]')
s7 += prop_box(L('4. Producte de potències amb el mateix exponent', '4. Producto de potencias con el mismo exponente', '4. Multiplying powers with the same exponent'),
  (r"Es <strong>multipliquen les bases</strong> i es deixa el mateix exponent:", r"Se <strong>multiplican las bases</strong> y se deja el mismo exponente:", r"<strong>Multiply the bases</strong> and keep the exponent:"),
  r'\[\boxed{a^{n}\cdot b^{n}=(a\cdot b)^{n}}\]', r'\[2^{3}\cdot5^{3}=(2\cdot2\cdot2)\cdot(5\cdot5\cdot5)=(2\cdot5)\cdot(2\cdot5)\cdot(2\cdot5)=10^{3}=1000\]')
s7 += prop_box(L('5. Quocient de potències amb el mateix exponent', '5. Cociente de potencias con el mismo exponente', '5. Dividing powers with the same exponent'),
  (r"Es <strong>divideixen les bases</strong> i es deixa el mateix exponent:", r"Se <strong>dividen las bases</strong> y se deja el mismo exponente:", r"<strong>Divide the bases</strong> and keep the exponent:"),
  r'\[\boxed{a^{n}:b^{n}=(a:b)^{n}}\]', r'\[15^{2}:5^{2}=(15:5)^{2}=3^{2}=9\qquad(225:25=9\ ✓)\]')
s7 += prop_box(L("6. Potència d'exponent zero", '6. Potencia de exponente cero', '6. Exponent zero'),
  (r"<strong>Tota potència d'exponent 0 val 1</strong> (si la base no és 0). Vegem per què: dividim una potència entre ella mateixa.", r"<strong>Toda potencia de exponente 0 vale 1</strong> (si la base no es 0). Veamos por qué: dividimos una potencia entre sí misma.", r"<strong>Any power with exponent 0 equals 1</strong> (if the base isn't 0). Here's why: divide a power by itself."),
  r'\[7^{3}:7^{3}=\begin{cases}7^{3-3}=7^{0}\\[2pt] 343:343=1\end{cases}\qquad\Longrightarrow\qquad\boxed{a^{0}=1}\]',
  P(r"I recorda també que \(a^{1}=a\).", r"Y recuerda también que \(a^{1}=a\).", r"And remember too that \(a^{1}=a\)."))
s7 += box('prop', L('Resum de les propietats', 'Resumen de las propiedades', 'Summary of the properties'),
  '<div class="tbl-wrap"><table class="data"><tbody>'
  + '<tr><td class="l">' + L('Mateixa base, multiplicació', 'Misma base, multiplicación', 'Same base, multiply') + r'</td><td>\(a^{m}\cdot a^{n}=a^{m+n}\)</td><td>' + L('se sumen els exponents', 'se suman los exponentes', 'add the exponents') + '</td></tr>'
  + '<tr><td class="l">' + L('Mateixa base, divisió', 'Misma base, división', 'Same base, divide') + r'</td><td>\(a^{m}:a^{n}=a^{m-n}\)</td><td>' + L('es resten els exponents', 'se restan los exponentes', 'subtract the exponents') + '</td></tr>'
  + '<tr><td class="l">' + L("Potència d'una potència", 'Potencia de una potencia', 'Power of a power') + r'</td><td>\(\left(a^{m}\right)^{n}=a^{m\cdot n}\)</td><td>' + L('es multipliquen els exponents', 'se multiplican los exponentes', 'multiply the exponents') + '</td></tr>'
  + '<tr><td class="l">' + L('Mateix exponent, multiplicació', 'Mismo exponente, multiplicación', 'Same exponent, multiply') + r'</td><td>\(a^{n}\cdot b^{n}=(a\cdot b)^{n}\)</td><td>' + L('es multipliquen les bases', 'se multiplican las bases', 'multiply the bases') + '</td></tr>'
  + '<tr><td class="l">' + L('Mateix exponent, divisió', 'Mismo exponente, división', 'Same exponent, divide') + r'</td><td>\(a^{n}:b^{n}=(a:b)^{n}\)</td><td>' + L('es divideixen les bases', 'se dividen las bases', 'divide the bases') + '</td></tr>'
  + '<tr><td class="l">' + L('Exponent 0 i 1', 'Exponente 0 y 1', 'Exponent 0 and 1') + r'</td><td>\(a^{0}=1\qquad a^{1}=a\)</td><td></td></tr>'
  + '</tbody></table></div>'
  + note(r"<strong>Amb sumes i restes no hi ha cap propietat!</strong> \(\ 2^{3}+2^{2}\neq2^{5}\): \(\ 8+4=12\), però \(2^{5}=32\). Tampoc podem ajuntar \(2^{3}\cdot3^{2}\) (bases i exponents diferents): només el calculem, \(8\cdot9=72\).", r"<strong>¡Con sumas y restas no hay ninguna propiedad!</strong> \(\ 2^{3}+2^{2}\neq2^{5}\): \(\ 8+4=12\), pero \(2^{5}=32\). Tampoco podemos juntar \(2^{3}\cdot3^{2}\) (bases y exponentes distintos): solo lo calculamos, \(8\cdot9=72\).", r"<strong>There are no properties for addition and subtraction!</strong> \(\ 2^{3}+2^{2}\neq2^{5}\): \(\ 8+4=12\), but \(2^{5}=32\). Nor can we combine \(2^{3}\cdot3^{2}\) (different bases and exponents): we just work it out, \(8\cdot9=72\).", '⚠️')
  + f'''<div class="widget" id="w-props">
  <div class="wt">🔍 {L("Mira per què funcionen les propietats", "Mira por qué funcionan las propiedades", "See why the properties work")}</div>
  <div class="seg" role="group"><button type="button" data-k="mul" aria-pressed="true">{L("Producte, mateixa base", "Producto, misma base", "Product, same base")}</button><button type="button" data-k="div" aria-pressed="false">{L("Quocient, mateixa base", "Cociente, misma base", "Quotient, same base")}</button><button type="button" data-k="pow" aria-pressed="false">{L("Potència d'una potència", "Potencia de una potencia", "Power of a power")}</button><button type="button" data-k="same" aria-pressed="false">{L("Producte, mateix exponent", "Producto, mismo exponente", "Product, same exponent")}</button><button type="button" data-k="quo" aria-pressed="false">{L("Quocient, mateix exponent", "Cociente, mismo exponente", "Quotient, same exponent")}</button><button type="button" data-k="zero" aria-pressed="false">{L("Exponent 0", "Exponente 0", "Exponent 0")}</button></div>
  <div class="wrow" style="margin-top:10px"><label data-f="a">a <input class="tin s" type="number" min="0" max="12" value="2" data-k="a" aria-label="a"></label><label data-f="b">b <input class="tin s" type="number" min="1" max="12" value="5" data-k="b" aria-label="b"></label><label data-f="m">m <input class="tin s" type="number" min="1" max="6" value="3" data-k="m" aria-label="m"></label><label data-f="n">n <input class="tin s" type="number" min="1" max="6" value="2" data-k="n" aria-label="n"></label></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('props', 'Entrena: aplica les propietats', 'Entrena: aplica las propiedades', 'Train: use the properties'))
s7 += level(1, 1,
  prob(L(r"Expressa com una sola potència: a) \(3^{4}\cdot3^{5}\qquad\) b) \(7^{8}:7^{3}\qquad\) c) \(\left(2^{3}\right)^{4}\)", r"Expresa como una sola potencia: a) \(3^{4}\cdot3^{5}\qquad\) b) \(7^{8}:7^{3}\qquad\) c) \(\left(2^{3}\right)^{4}\)", r"Write as a single power: a) \(3^{4}\cdot3^{5}\qquad\) b) \(7^{8}:7^{3}\qquad\) c) \(\left(2^{3}\right)^{4}\)"),
       r'\[\text{a)}\ 3^{4+5}=\boxed{3^{9}}\]', r'\[\text{b)}\ 7^{8-3}=\boxed{7^{5}}\]', r'\[\text{c)}\ 2^{3\cdot4}=\boxed{2^{12}}\]'),
  prob(L(r"Calcula: \(5^{0}\) i \(2^{4}\cdot5^{4}\).", r"Calcula: \(5^{0}\) y \(2^{4}\cdot5^{4}\).", r"Work out: \(5^{0}\) and \(2^{4}\cdot5^{4}\)."),
       r'\[5^{0}=\boxed{1}\]',
       P(r"Tenen el mateix exponent: multipliquem les bases.", r"Tienen el mismo exponente: multiplicamos las bases.", r"Same exponent: multiply the bases.") + r'\[2^{4}\cdot5^{4}=(2\cdot5)^{4}=10^{4}=\boxed{10\,000}\]'))
s7 += level(2, 3,
  prob(r"\(2^{3}\cdot2^{5}\cdot2\)",
       P(r"Recorda que \(2=2^{1}\):", r"Recuerda que \(2=2^{1}\):", r"Remember that \(2=2^{1}\):") + r'\[2^{3}\cdot2^{5}\cdot2^{1}=2^{3+5+1}=2^{9}\]',
       r'\[2^{9}=\boxed{512}\]'),
  prob(r"\(\left(5^{3}\cdot5^{4}\right):5^{5}\)",
       r'\[\left(5^{3}\cdot5^{4}\right):5^{5}=5^{7}:5^{5}\]',
       r'\[5^{7-5}=5^{2}=\boxed{25}\]'))
s7 += level(3, 5,
  prob(r"\(\left[\left(3^{2}\right)^{3}\cdot3^{4}\right]:3^{8}\)",
       P(r"Primer la potència de la potència, de dins del claudàtor:", r"Primero la potencia de la potencia, dentro del corchete:", r"First the power of a power, inside the square brackets:") + r'\[\left[3^{6}\cdot3^{4}\right]:3^{8}\]',
       r'\[3^{10}:3^{8}=3^{2}=\boxed{9}\]'),
  prob(L(r"Calcula de la manera més ràpida: a) \(25^{3}\cdot4^{3}\qquad\) b) \(12^{4}:4^{4}\)", r"Calcula de la forma más rápida: a) \(25^{3}\cdot4^{3}\qquad\) b) \(12^{4}:4^{4}\)", r"Work out the quickest way: a) \(25^{3}\cdot4^{3}\qquad\) b) \(12^{4}:4^{4}\)"),
       r'\[\text{a)}\ (25\cdot4)^{3}=100^{3}=\boxed{1\,000\,000}\]',
       r'\[\text{b)}\ (12:4)^{4}=3^{4}=\boxed{81}\]'))
s7 += practice([
  ('★', L(r"Expressa com una sola potència: a) \(4^{2}\cdot4^{6}\qquad\) b) \(9^{7}:9^{2}\qquad\) c) \(\left(5^{2}\right)^{3}\qquad\) d) \(2^{5}\cdot3^{5}\)", r"Expresa como una sola potencia: a) \(4^{2}\cdot4^{6}\qquad\) b) \(9^{7}:9^{2}\qquad\) c) \(\left(5^{2}\right)^{3}\qquad\) d) \(2^{5}\cdot3^{5}\)", r"Write as a single power: a) \(4^{2}\cdot4^{6}\qquad\) b) \(9^{7}:9^{2}\qquad\) c) \(\left(5^{2}\right)^{3}\qquad\) d) \(2^{5}\cdot3^{5}\)")),
  ('★★', r"e) \(10^{3}\cdot10^{2}\cdot10\qquad\) f) \(\left(7^{4}\cdot7^{2}\right):7^{6}\)"),
  ('★★★', L(r"g) \(\left[\left(2^{2}\right)^{4}\cdot2^{3}\right]:\left(2^{5}\right)^{2}\qquad\) h) \(8^{3}:4^{3}\) i \(50^{2}\cdot2^{2}\qquad\) i) Explica per què \(3^{2}+3^{3}\neq3^{5}\).", r"g) \(\left[\left(2^{2}\right)^{4}\cdot2^{3}\right]:\left(2^{5}\right)^{2}\qquad\) h) \(8^{3}:4^{3}\) y \(50^{2}\cdot2^{2}\qquad\) i) Explica por qué \(3^{2}+3^{3}\neq3^{5}\).", r"g) \(\left[\left(2^{2}\right)^{4}\cdot2^{3}\right]:\left(2^{5}\right)^{2}\qquad\) h) \(8^{3}:4^{3}\) and \(50^{2}\cdot2^{2}\qquad\) i) Explain why \(3^{2}+3^{3}\neq3^{5}\)."))],
  r'\[\text{a)}\ 4^{8}\qquad \text{b)}\ 9^{5}\qquad \text{c)}\ 5^{6}\qquad \text{d)}\ 6^{5}\qquad \text{e)}\ 10^{6}\qquad \text{f)}\ 7^{0}=1\]'
  + r'\[\text{g)}\ \left[2^{8}\cdot2^{3}\right]:2^{10}=2^{11}:2^{10}=2\qquad \text{h)}\ 2^{3}=8,\ \ 100^{2}=10\,000\]'
  + P(r"i) Amb sumes no hi ha propietat: \(3^{2}+3^{3}=9+27=36\), però \(3^{5}=243\).", r"i) Con sumas no hay propiedad: \(3^{2}+3^{3}=9+27=36\), pero \(3^{5}=243\).", r"i) There's no rule for sums: \(3^{2}+3^{3}=9+27=36\), but \(3^{5}=243\)."))

# ============================================================ 1.8
s8 = box('def', L('Arrel quadrada', 'Raíz cuadrada', 'Square root'),
  P(r"L'<strong>arrel quadrada</strong> d'un nombre \(a\) és el nombre \(b\) que, elevat al quadrat, dona \(a\):", r"La <strong>raíz cuadrada</strong> de un número \(a\) es el número \(b\) que, elevado al cuadrado, da \(a\):", r"The <strong>square root</strong> of a number \(a\) is the number \(b\) which, squared, gives \(a\):")
  + r'\[\boxed{\ \sqrt{a}=b\quad\Longleftrightarrow\quad b^{2}=a\ }\qquad\qquad \sqrt{49}=7\ \ \tri{perquè}{porque}{because}\ \ 7^{2}=49\]'
  + P(r"El signe \(\sqrt{\ \ }\) s'anomena <strong>radical</strong> i el nombre de dins, <strong>radicand</strong>. Elevar al quadrat i fer l'arrel quadrada són <strong>operacions inverses</strong>: l'una desfà el que fa l'altra.", r"El signo \(\sqrt{\ \ }\) se llama <strong>radical</strong> y el número de dentro, <strong>radicando</strong>. Elevar al cuadrado y hacer la raíz cuadrada son <strong>operaciones inversas</strong>: una deshace lo que hace la otra.", r"The sign \(\sqrt{\ \ }\) is the <strong>radical sign</strong> and the number inside is the <strong>radicand</strong>. Squaring and taking the square root are <strong>inverse operations</strong>: each undoes the other.")
  + note(r"Si un quadrat té 49 cm² d'àrea, el seu costat mesura \(\sqrt{49}=7\) cm.", r"Si un cuadrado tiene 49 cm² de área, su lado mide \(\sqrt{49}=7\) cm.", r"If a square has an area of 49 cm², its side is \(\sqrt{49}=7\) cm.", '📐'))
s8 += box('def', L('Arrel exacta', 'Raíz exacta', 'Exact root'),
  P(r"Si el radicand és un <strong>quadrat perfecte</strong> (el quadrat d'un natural), l'arrel és <strong>exacta</strong>:", r"Si el radicando es un <strong>cuadrado perfecto</strong> (el cuadrado de un natural), la raíz es <strong>exacta</strong>:", r"If the radicand is a <strong>perfect square</strong> (the square of a natural number), the root is <strong>exact</strong>:")
  + '<div class="tbl-wrap"><table class="data sq"><thead><tr><th>' + L('Quadrat perfecte', 'Cuadrado perfecto', 'Perfect square') + '</th>' + ''.join(f'<th>{i*i}</th>' for i in range(1, 16)) + '</tr></thead><tbody><tr><th>' + L('Arrel', 'Raíz', 'Root') + '</th>' + ''.join(f'<td>{i}</td>' for i in range(1, 16)) + '</tr></tbody></table></div>'
  + note(r"Si un nombre acaba en un nombre parell de zeros, la seua arrel en té la meitat: \(\sqrt{400}=20\), \(\ \sqrt{10\,000}=100\), \(\ \sqrt{2500}=50\).", r"Si un número acaba en un número par de ceros, su raíz tiene la mitad: \(\sqrt{400}=20\), \(\ \sqrt{10\,000}=100\), \(\ \sqrt{2500}=50\).", r"If a number ends in an even number of zeros, its root has half as many: \(\sqrt{400}=20\), \(\ \sqrt{10\,000}=100\), \(\ \sqrt{2500}=50\).", '🧠'))
s8 += box('def', L('Arrel entera i residu', 'Raíz entera y resto', 'Whole-number root and remainder'),
  P(r"Si el radicand <strong>no</strong> és un quadrat perfecte, l'arrel no és exacta. L'<strong>arrel entera</strong> és el natural més gran el quadrat del qual <strong>no passa</strong> del radicand, i el <strong>residu</strong> és el que sobra:", r"Si el radicando <strong>no</strong> es un cuadrado perfecto, la raíz no es exacta. La <strong>raíz entera</strong> es el natural más grande cuyo cuadrado <strong>no pasa</strong> del radicando, y el <strong>resto</strong> es lo que sobra:", r"If the radicand is <strong>not</strong> a perfect square, the root isn't exact. The <strong>whole-number root</strong> is the largest natural number whose square <strong>doesn't go over</strong> the radicand, and the <strong>remainder</strong> is what's left:")
  + r'\[\tri{residu}{resto}{remainder}=\tri{radicand}{radicando}{radicand}-(\tri{arrel entera}{raíz entera}{root})^{2}\]'
  + P(r"Per exemple, \(\sqrt{40}\): com que \(6^{2}=36\le40<49=7^{2}\), l'arrel entera és 6 i el residu, \(40-36=4\).", r"Por ejemplo, \(\sqrt{40}\): como \(6^{2}=36\le40<49=7^{2}\), la raíz entera es 6 y el resto, \(40-36=4\).", r"For example, \(\sqrt{40}\): since \(6^{2}=36\le40<49=7^{2}\), the whole-number root is 6 and the remainder is \(40-36=4\).")
  + r'\[40=6^{2}+4\]'
  + f'''<div class="widget" id="w-sqrt">
  <div class="wt">🟩 {L("Fem quadrats amb rajoles", "Hacemos cuadrados con baldosas", "Making squares with tiles")}</div>
  <div class="wrow"><label>{L("Rajoles", "Baldosas", "Tiles")} <input type="range" min="1" max="225" value="40" aria-label="rajoles"> <input class="tin s" type="text" inputmode="numeric" value="40" autocomplete="off" aria-label="N"></label></div>
  {quick([("40", "40"), ("49", "49"), ("30", "30"), ("90", "90"), ("150", "150"), ("200", "200")])}
  <div class="tiles"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('sqrt', 'Entrena: arrels quadrades', 'Entrena: raíces cuadradas', 'Train: square roots'))
s8 += level(1, 1,
  prob(L(r"Calcula: \(\sqrt{81},\ \ \sqrt{121},\ \ \sqrt{400}\).", r"Calcula: \(\sqrt{81},\ \ \sqrt{121},\ \ \sqrt{400}\).", r"Work out: \(\sqrt{81},\ \ \sqrt{121},\ \ \sqrt{400}\)."),
       r'\[\sqrt{81}=9\ \ (9^{2}=81)\qquad \sqrt{121}=11\ \ (11^{2}=121)\qquad \sqrt{400}=20\ \ (20^{2}=400)\]'),
  prob(L(r"Calcula l'arrel entera i el residu de \(\sqrt{30}\).", r"Calcula la raíz entera y el resto de \(\sqrt{30}\).", r"Find the whole-number root and remainder of \(\sqrt{30}\)."),
       P(r"Busquem entre quins quadrats està 30:", r"Buscamos entre qué cuadrados está 30:", r"Find which squares 30 lies between:") + r'\[5^{2}=25\le30<36=6^{2}\]',
       P(r"<strong>Arrel entera 5 i residu \(30-25=5\).</strong> Comprovació: \(5^{2}+5=30\) ✓", r"<strong>Raíz entera 5 y resto \(30-25=5\).</strong> Comprobación: \(5^{2}+5=30\) ✓", r"<strong>Root 5 and remainder \(30-25=5\).</strong> Check: \(5^{2}+5=30\) ✓")))
s8 += level(2, 3,
  prob(L(r"Calcula l'arrel entera i el residu de \(\sqrt{150}\).", r"Calcula la raíz entera y el resto de \(\sqrt{150}\).", r"Find the whole-number root and remainder of \(\sqrt{150}\)."),
       P(r"Provem: \(10^{2}=100\), \(11^{2}=121\), \(12^{2}=144\), \(13^{2}=169\) (ens passem).", r"Probamos: \(10^{2}=100\), \(11^{2}=121\), \(12^{2}=144\), \(13^{2}=169\) (nos pasamos).", r"Try: \(10^{2}=100\), \(11^{2}=121\), \(12^{2}=144\), \(13^{2}=169\) (too big)."),
       r'\[12^{2}=144\le150<169=13^{2}\quad\Rightarrow\quad \tri{arrel entera}{raíz entera}{root}\ 12,\ \ \tri{residu}{resto}{remainder}\ 150-144=6\]'),
  prob(L(r"Entre quins dos nombres naturals consecutius està \(\sqrt{90}\)?", r"¿Entre qué dos números naturales consecutivos está \(\sqrt{90}\)?", r"Between which two consecutive natural numbers does \(\sqrt{90}\) lie?"),
       r'\[81<90<100\quad\Rightarrow\quad\sqrt{81}<\sqrt{90}<\sqrt{100}\quad\Rightarrow\quad\boxed{9<\sqrt{90}<10}\]'))
s8 += level(3, 5,
  prob(L(r"Tenim 200 rajoles quadrades i volem fer el quadrat més gran possible. Quantes rajoles té cada costat? En sobren? Quantes en faltarien per a fer el quadrat següent?", r"Tenemos 200 baldosas cuadradas y queremos hacer el cuadrado más grande posible. ¿Cuántas baldosas tiene cada lado? ¿Sobran? ¿Cuántas faltarían para hacer el cuadrado siguiente?", r"We have 200 square tiles and want to make the biggest possible square. How many tiles are on each side? Are any left over? How many more would we need for the next square?"),
       r'\[14^{2}=196\le200<225=15^{2}\]',
       P(r"<strong>Cada costat té 14 rajoles i en sobren \(200-196=4\).</strong> Per al quadrat de 15 × 15 en faltarien \(225-200=25\).", r"<strong>Cada lado tiene 14 baldosas y sobran \(200-196=4\).</strong> Para el cuadrado de 15 × 15 faltarían \(225-200=25\).", r"<strong>Each side has 14 tiles and \(200-196=4\) are left over.</strong> For a 15 × 15 square we'd need \(225-200=25\) more.")),
  prob(L(r"L'arrel entera d'un nombre és 7 i el residu és 10. Quin és el nombre? Podria ser 15 el residu?", r"La raíz entera de un número es 7 y el resto es 10. ¿Cuál es el número? ¿Podría ser 15 el resto?", r"A number has whole-number root 7 and remainder 10. What is the number? Could the remainder be 15?"),
       r'\[n=7^{2}+10=49+10=\boxed{59}\]',
       P(r"Si el residu fóra 15, el nombre seria \(49+15=64=8^{2}\), i llavors l'arrel seria exacta i valdria 8. <strong>El residu més gran possible amb arrel 7 és 14</strong> (\(63=7^2+14\)).", r"Si el resto fuera 15, el número sería \(49+15=64=8^{2}\), y entonces la raíz sería exacta y valdría 8. <strong>El resto más grande posible con raíz 7 es 14</strong> (\(63=7^2+14\)).", r"If the remainder were 15, the number would be \(49+15=64=8^{2}\), so the root would be exactly 8. <strong>The largest possible remainder with root 7 is 14</strong> (\(63=7^2+14\)).")))
s8 += practice([
  ('★', r"a) \(\sqrt{36}\) &nbsp; b) \(\sqrt{100}\) &nbsp; c) \(\sqrt{169}\) &nbsp; d) \(\sqrt{1}\)"),
  ('★★', L(r"e) Arrel entera i residu de \(\sqrt{20}\), \(\sqrt{55}\) i \(\sqrt{99}\). f) \(\sqrt{10\,000}\)", r"e) Raíz entera y resto de \(\sqrt{20}\), \(\sqrt{55}\) y \(\sqrt{99}\). f) \(\sqrt{10\,000}\)", r"e) Whole-number root and remainder of \(\sqrt{20}\), \(\sqrt{55}\) and \(\sqrt{99}\). f) \(\sqrt{10\,000}\)")),
  ('★★★', L(r"g) Un camp quadrat té 625 m² d'àrea. Quants metres de tanca calen per a envoltar-lo? h) Quin és el nombre més gran que té arrel entera 9?", r"g) Un campo cuadrado tiene 625 m² de área. ¿Cuántos metros de valla hacen falta para rodearlo? h) ¿Cuál es el número más grande que tiene raíz entera 9?", r"g) A square field has an area of 625 m². How many metres of fence are needed to go round it? h) What is the largest number whose whole-number root is 9?"))],
  r'\[\text{a)}\ 6\qquad \text{b)}\ 10\qquad \text{c)}\ 13\qquad \text{d)}\ 1\]'
  + r'\[\text{e)}\ 4\ (r=4)\qquad 7\ (r=6)\qquad 9\ (r=18)\qquad \text{f)}\ 100\]'
  + r'\[\text{g)}\ \sqrt{625}=25\ \text{m}\ \to\ 4\cdot25=100\ \text{m}\qquad \text{h)}\ 9^{2}+18=99\ \ (100=10^{2})\]')

# ============================================================ 1.9
s9 = box('prop', L("Jerarquia amb potències i arrels", "Jerarquía con potencias y raíces", "Order of operations with powers and roots"),
  P(r"Recorda l'ordre: <strong>1)</strong> parèntesis, <strong>2)</strong> potències i arrels, <strong>3)</strong> multiplicacions i divisions, <strong>4)</strong> sumes i restes.", r"Recuerda el orden: <strong>1)</strong> paréntesis, <strong>2)</strong> potencias y raíces, <strong>3)</strong> multiplicaciones y divisiones, <strong>4)</strong> sumas y restas.", r"Remember the order: <strong>1)</strong> brackets, <strong>2)</strong> powers and roots, <strong>3)</strong> multiplication and division, <strong>4)</strong> addition and subtraction.")
  + r'\[2+3\cdot4^{2}=2+3\cdot16=2+48=50\qquad\qquad (2+3)\cdot4^{2}=5\cdot16=80\]'
  + P(r"El signe de l'arrel fa de <strong>parèntesi</strong>: primer calculem el que hi ha dins.", r"El signo de la raíz hace de <strong>paréntesis</strong>: primero calculamos lo que hay dentro.", r"The root sign acts like <strong>brackets</strong>: work out what's inside first.")
  + note(r"<strong>L'arrel d'una suma no és la suma de les arrels:</strong> \(\ \sqrt{9+16}=\sqrt{25}=5\), però \(\sqrt{9}+\sqrt{16}=3+4=7\). I el mateix amb les potències: \((2+3)^{2}=25\), però \(2^{2}+3^{2}=13\).", r"<strong>La raíz de una suma no es la suma de las raíces:</strong> \(\ \sqrt{9+16}=\sqrt{25}=5\), pero \(\sqrt{9}+\sqrt{16}=3+4=7\). Y lo mismo con las potencias: \((2+3)^{2}=25\), pero \(2^{2}+3^{2}=13\).", r"<strong>The root of a sum is not the sum of the roots:</strong> \(\ \sqrt{9+16}=\sqrt{25}=5\), but \(\sqrt{9}+\sqrt{16}=3+4=7\). The same goes for powers: \((2+3)^{2}=25\), but \(2^{2}+3^{2}=13\).", '⚠️')
  + hier(["2^3+3·√49-5^2", "2+3·4^2", "(2+3)·4^2", "√(9+16)", "√9+√16", "(10^2-6^2):2^3+√(5^2-3^2)", "4·3^2-√81:3"]))
s9 += level(1, 1,
  prob(L(r"Calcula: \(3^{2}+4^{2}\) i \(\sqrt{3^{2}+4^{2}}\).", r"Calcula: \(3^{2}+4^{2}\) y \(\sqrt{3^{2}+4^{2}}\).", r"Work out: \(3^{2}+4^{2}\) and \(\sqrt{3^{2}+4^{2}}\)."),
       r'\[3^{2}+4^{2}=9+16=\boxed{25}\]',
       r'\[\sqrt{3^{2}+4^{2}}=\sqrt{25}=\boxed{5}\]'),
  prob(L(r"Una capsa té 6 files de 6 bombons. En un paquet hi ha 6 capses. Quants bombons hi ha en un paquet?", r"Una caja tiene 6 filas de 6 bombones. En un paquete hay 6 cajas. ¿Cuántos bombones hay en un paquete?", r"A box has 6 rows of 6 chocolates. A pack has 6 boxes. How many chocolates are there in a pack?"),
       r'\[6\cdot6\cdot6=6^{3}\]',
       r'\[6^{3}=\boxed{216}\ \tri{bombons}{bombones}{chocolates}\]'))
s9 += level(2, 3,
  prob(r"\(2^{3}+3\cdot\sqrt{49}-5^{2}\)",
       P(r"Primer les potències i l'arrel:", r"Primero las potencias y la raíz:", r"Powers and root first:") + r'\[\underbrace{2^{3}}_{8}+3\cdot\underbrace{\sqrt{49}}_{7}-\underbrace{5^{2}}_{25}=8+3\cdot7-25\]',
       r'\[8+21-25=\boxed{4}\]'),
  prob(L(r"Un jardí quadrat té 81 m² d'àrea. Volem posar-hi una tanca al voltant que costa 7 € el metre. Quant costarà?", r"Un jardín cuadrado tiene 81 m² de área. Queremos ponerle alrededor una valla que cuesta 7 € el metro. ¿Cuánto costará?", r"A square garden has an area of 81 m². We want to put a fence round it that costs €7 per metre. How much will it cost?"),
       r'\[\tri{Costat}{Lado}{Side}:\ \sqrt{81}=9\ \text{m}\]',
       r'\[\tri{Perímetre}{Perímetro}{Perimeter}:\ 4\cdot9=36\ \text{m}\]',
       r'\[36\cdot7=\boxed{252\ €}\]'))
s9 += level(3, 5,
  prob(L(r"El dilluns envies un missatge a 3 amics. El dimarts, cadascun l'envia a 3 amics nous, i així cada dia. Quantes persones noves el reben el diumenge? I en tota la setmana?", r"El lunes envías un mensaje a 3 amigos. El martes, cada uno lo envía a 3 amigos nuevos, y así cada día. ¿Cuántas personas nuevas lo reciben el domingo? ¿Y en toda la semana?", r"On Monday you send a message to 3 friends. On Tuesday, each of them sends it to 3 new friends, and so on every day. How many new people get it on Sunday? And during the whole week?"),
       '<div class="tbl-wrap"><table class="data"><thead><tr><th></th>' + ''.join(f'<th>{d}</th>' for d in [L('Dl', 'L', 'Mon'), L('Dt', 'M', 'Tue'), L('Dc', 'X', 'Wed'), L('Dj', 'J', 'Thu'), L('Dv', 'V', 'Fri'), L('Ds', 'S', 'Sat'), L('Dg', 'D', 'Sun')]) + '</tr></thead><tbody><tr><th>' + L('Reben', 'Reciben', 'Get it') + '</th>' + ''.join(f'<td>\\(3^{{{i}}}={3**i}\\)</td>' for i in range(1, 8)) + '</tr></tbody></table></div>',
       P(r"<strong>El diumenge el reben \(3^{7}=2187\) persones noves.</strong>", r"<strong>El domingo lo reciben \(3^{7}=2187\) personas nuevas.</strong>", r"<strong>On Sunday, \(3^{7}=2187\) new people get it.</strong>"),
       r'\[3+9+27+81+243+729+2187=\boxed{3279}\ \tri{persones en tota la setmana}{personas en toda la semana}{people in the whole week}\]'),
  prob(r"\(\left(10^{2}-6^{2}\right):2^{3}+\sqrt{5^{2}-3^{2}}\cdot10^{0}\)",
       P(r"Dins dels parèntesis i de l'arrel, primer les potències:", r"Dentro de los paréntesis y de la raíz, primero las potencias:", r"Inside the brackets and the root, powers first:") + r'\[\left(100-36\right):2^{3}+\sqrt{25-9}\cdot10^{0}=64:2^{3}+\sqrt{16}\cdot10^{0}\]',
       P(r"Ara les potències i arrels que queden:", r"Ahora las potencias y raíces que quedan:", r"Now the remaining powers and roots:") + r'\[64:8+4\cdot1\]',
       r'\[8+4=\boxed{12}\]'))
s9 += practice([
  ('★', r"a) \(5^{2}-4^{2}\qquad\) b) \(\sqrt{64}+\sqrt{36}\qquad\) c) \(\sqrt{64+36}\)"),
  ('★★', L(r"d) \(4\cdot3^{2}-\sqrt{81}:3\qquad\) e) Un tauler d'escacs té 8 × 8 caselles. Quantes caselles té? Si un tauler quadrat té 225 caselles, quantes en té cada costat?", r"d) \(4\cdot3^{2}-\sqrt{81}:3\qquad\) e) Un tablero de ajedrez tiene 8 × 8 casillas. ¿Cuántas casillas tiene? Si un tablero cuadrado tiene 225 casillas, ¿cuántas tiene cada lado?", r"d) \(4\cdot3^{2}-\sqrt{81}:3\qquad\) e) A chessboard has 8 × 8 squares. How many squares is that? If a square board has 225 squares, how many are along each side?")),
  ('★★★', L(r"f) \(\left(2^{4}+3^{2}\right)\cdot\sqrt{100}:5^{2}\qquad\) g) En una prestatgeria hi ha 5 prestatges; en cada prestatge, 5 capses; en cada capsa, 5 carpetes, i en cada carpeta, 5 fulls. Quants fulls hi ha? h) Un cub està fet de 4 × 4 × 4 cubets. Quants cubets té? Si li llevem la capa de dalt, quants en queden?", r"f) \(\left(2^{4}+3^{2}\right)\cdot\sqrt{100}:5^{2}\qquad\) g) En una estantería hay 5 estantes; en cada estante, 5 cajas; en cada caja, 5 carpetas, y en cada carpeta, 5 hojas. ¿Cuántas hojas hay? h) Un cubo está hecho de 4 × 4 × 4 cubitos. ¿Cuántos cubitos tiene? Si le quitamos la capa de arriba, ¿cuántos quedan?", r"f) \(\left(2^{4}+3^{2}\right)\cdot\sqrt{100}:5^{2}\qquad\) g) A bookcase has 5 shelves; each shelf has 5 boxes; each box has 5 folders and each folder has 5 sheets. How many sheets are there? h) A cube is made of 4 × 4 × 4 little cubes. How many little cubes is that? If we remove the top layer, how many are left?"))],
  r'\[\text{a)}\ 25-16=9\qquad \text{b)}\ 8+6=14\qquad \text{c)}\ \sqrt{100}=10\]'
  + r'\[\text{d)}\ 36-9:3=36-3=33\qquad \text{e)}\ 8^{2}=64;\ \ \sqrt{225}=15\]'
  + r'\[\text{f)}\ 25\cdot10:25=10\qquad \text{g)}\ 5^{4}=625\qquad \text{h)}\ 4^{3}=64;\ \ 64-4^{2}=48\]')

# ============================================================ muntatge
SECS = [
  (L('Els nombres naturals', 'Los números naturales', 'Natural numbers'), s1),
  (L('Aproximació: truncament i arrodoniment', 'Aproximación: truncamiento y redondeo', 'Approximation: truncating and rounding'), s2),
  (L('Operacions amb nombres naturals', 'Operaciones con números naturales', 'Operations with natural numbers'), s3),
  (L('Problemes amb nombres naturals', 'Problemas con números naturales', 'Word problems with natural numbers'), s4),
  (L('Potències', 'Potencias', 'Powers'), s5),
  (L('Potències de base 10', 'Potencias de base 10', 'Powers of 10'), s6),
  (L('Propietats de les potències', 'Propiedades de las potencias', 'Properties of powers'), s7),
  (L('Arrels quadrades', 'Raíces cuadradas', 'Square roots'), s8),
  (L('Problemes amb potències i arrels', 'Problemas con potencias y raíces', 'Problems with powers and roots'), s9),
]
src = open(SRC, encoding='utf-8').read().split('\n')
head = '\n'.join(src[:253])
head = head.replace('<title>Proporcionalitat i percentatges · FentMates</title>', '<title>Nombres naturals · FentMates</title>')
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Apunts interactius de la Unitat 1 (Nombres naturals) de 1r d\'ESO, en valencià, castellà i anglés.">', head)
head = head.replace('.hero::after { content: "%";', '.hero::after { content: "ℕ";')
assert 'Nombres naturals · FentMates' in head and 'content: "ℕ"' in head
wide = '\n'.join(src[344:350])
assert 'FentMates: 80%' in wide
css = open(os.path.join(HERE, 'extra.css'), encoding='utf-8').read()
js = open(os.path.join(HERE, 'app.js'), encoding='utf-8').read()

ntools = sum(b.count('class="widget') for _, b in SECS)
toc = ''.join(f'        <li><a href="#s{i}"><span class="n">1.{i}</span>{t}<span class="ck">✓</span></a></li>\n' for i, (t, _) in enumerate(SECS, 1))
body = f'''<body>
<header class="topbar">
  <div class="in">
    <a class="brand" href="../../index.html"><span class="logo">∑</span>FentMates</a>
    <span class="crumb"><a href="../../1eso.html">{L("1r ESO", "1º ESO", "1st ESO (Year 7)")}</a> / {L("Unitat 1", "Unidad 1", "Unit 1")}</span>
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
    <h1><span class="u">{L("Unitat 1", "Unidad 1", "Unit 1")}</span> · {L("Nombres naturals", "Números naturales", "Natural numbers")}</h1>
    <p>{L("Què són els nombres naturals, com s'aproximen, les quatre operacions i la jerarquia, problemes, potències, potències de 10, propietats de les potències i arrels quadrades: teoria explicada pas a pas, problemes resolts ordenats de més fàcils a més difícils i eines interactives per a practicar.",
          "Qué son los números naturales, cómo se aproximan, las cuatro operaciones y la jerarquía, problemas, potencias, potencias de 10, propiedades de las potencias y raíces cuadradas: teoría explicada paso a paso, problemas resueltos ordenados de más fáciles a más difíciles y herramientas interactivas para practicar.",
          "What natural numbers are, how to approximate them, the four operations and their order, word problems, powers, powers of 10, properties of powers and square roots: theory explained step by step, worked problems from easier to harder and interactive tools to practise.")}</p>
    <div class="chips"><span>{L("9 apartats", "9 apartados", "9 sections")}</span><span>{L(f"{ntools} eines interactives", f"{ntools} herramientas interactivas", f"{ntools} interactive tools")}</span><span>{L("Problemes per nivells ★☆☆ → ★★★", "Problemas por niveles ★☆☆ → ★★★", "Problems by level ★☆☆ → ★★★")}</span><span>{L("Autoavaluació final", "Autoevaluación final", "Final self-check")}</span></div>
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
      <div class="meter-l"><span id="meter-n">0</span>/9 {L("apartats estudiats", "apartados estudiados", "sections studied")}</div>
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
  <p>{L("Apunts de teoria · Unitat 1: Nombres naturals · 1r ESO", "Apuntes de teoría · Unidad 1: Números naturales · 1º ESO", "Theory notes · Unit 1: Natural numbers · 1st ESO")}</p>
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
