# Apartats 5.6-5.10 (proporcionalitat i percentatges) dels apunts de la Unitat 5 de 1r ESO.
from comu import *
from dec import gseg

def r3(a1, ma, b1, mb, a2, ma2, x):
    """esquema de regla de tres en TeX"""
    u = lambda t: t if t.startswith('\\') else r'\text{%s}' % t
    return (r'\[\begin{array}{rcl}%s\ %s & \longrightarrow & %s\ %s\\ %s\ %s & \longrightarrow & %s\end{array}\]'
            % (a1, u(ma), b1, u(mb), a2, u(ma2), x))

# ============================================================ 5.6
s6 = box('def', L('Raó entre dos nombres', 'Razón entre dos números', 'Ratio of two numbers'),
  P(r"La <strong>raó</strong> entre dos nombres \(a\) i \(b\) és el quocient \(\dfrac{a}{b}\) (es llig «\(a\) és a \(b\)»). Serveix per a comparar quantitats.",
    r"La <strong>razón</strong> entre dos números \(a\) y \(b\) es el cociente \(\dfrac{a}{b}\) (se lee «\(a\) es a \(b\)»). Sirve para comparar cantidades.",
    r"The <strong>ratio</strong> of two numbers \(a\) and \(b\) is the quotient \(\dfrac{a}{b}\) (read “\(a\) is to \(b\)”, also written \(a:b\)). It's used to compare amounts.")
  + P(r"En una classe hi ha 12 xics i 15 xiques. La raó entre xics i xiques és:", r"En una clase hay 12 chicos y 15 chicas. La razón entre chicos y chicas es:", r"A class has 12 boys and 15 girls. The ratio of boys to girls is:")
  + r'\[\frac{12}{15}=\frac{4}{5}=0\dc8\]'
  + P(r"Vol dir que <strong>per cada 4 xics hi ha 5 xiques</strong>, o que hi ha \(0\dc8\) xics per cada xica.", r"Quiere decir que <strong>por cada 4 chicos hay 5 chicas</strong>, o que hay \(0\dc8\) chicos por cada chica.", r"It means <strong>for every 4 boys there are 5 girls</strong>, or \(0\dc8\) boys per girl.")
  + note(r"Una raó s'assembla a una fracció, però els seus termes poden ser decimals i no parlen de «parts d'una unitat»: comparen dues quantitats diferents.", r"Una razón se parece a una fracción, pero sus términos pueden ser decimales y no hablan de «partes de una unidad»: comparan dos cantidades distintas.", r"A ratio looks like a fraction, but its terms can be decimals and it isn't about “parts of a whole”: it compares two different amounts."))
s6 += box('def', L('Proporció', 'Proporción', 'Proportion'),
  P(r"Una <strong>proporció</strong> és una igualtat entre dues raons. Es llig «\(a\) és a \(b\) com \(c\) és a \(d\)»:", r"Una <strong>proporción</strong> es una igualdad entre dos razones. Se lee «\(a\) es a \(b\) como \(c\) es a \(d\)»:", r"A <strong>proportion</strong> is an equality between two ratios, read “\(a\) is to \(b\) as \(c\) is to \(d\)”:")
  + r'\[\frac{a}{b}=\frac{c}{d}\qquad\text{p. ex.}\quad\frac{3}{5}=\frac{12}{20}\]'
  + P(r"\(a\) i \(d\) són els <strong>extrems</strong>; \(b\) i \(c\), els <strong>mitjans</strong>.", r"\(a\) y \(d\) son los <strong>extremos</strong>; \(b\) y \(c\), los <strong>medios</strong>.", r"\(a\) and \(d\) are the <strong>extremes</strong>; \(b\) and \(c\), the <strong>means</strong>."))
s6 += box('prop', L('Propietat fonamental', 'Propiedad fundamental', 'Key property'),
  P(r"En tota proporció, el producte dels extrems és igual al producte dels mitjans (són els productes creuats de la unitat 4):", r"En toda proporción, el producto de los extremos es igual al producto de los medios (son los productos cruzados de la unidad 4):", r"In every proportion, the product of the extremes equals the product of the means (the cross products from unit 4):")
  + r'\[\frac{a}{b}=\frac{c}{d}\iff a\cdot d=b\cdot c\qquad\qquad \frac{3}{5}=\frac{12}{20}:\ 3\cdot20=60=5\cdot12\]'
  + P(r"Això ens permet calcular un terme desconegut, el <strong>quart proporcional</strong>:", r"Esto nos permite calcular un término desconocido, el <strong>cuarto proporcional</strong>:", r"This lets us find a missing term, the <strong>fourth proportional</strong>:")
  + r'\[\frac{3}{5}=\frac{12}{x}\ \Rightarrow\ 3\cdot x=5\cdot12\ \Rightarrow\ x=\frac{5\cdot12}{3}=\boxed{20}\]'
  + widget('w-prop', '⚖️', L('Calcula el terme desconegut', 'Calcula el término desconocido', 'Find the missing term'),
    '  <div class="wrow"><span class="frin">' + nin('a', '', '', '', '3', 's') .replace('<label>', '').replace('</label>', '') + '<i></i>' + nin('b', '', '', '', '5', 's').replace('<label>', '').replace('</label>', '') + '</span><span class="eqs">=</span><span class="frin">'
    + nin('c', '', '', '', '12', 's').replace('<label>', '').replace('</label>', '') + '<i></i>' + nin('d', '', '', '', 'x', 's', 'text').replace('<label>', '').replace('</label>', '') + '</span></div>\n'
    + '  ' + quick([('3;5;12;x', '3/5 = 12/x'), ('x;8;15;24', 'x/8 = 15/24'), ('4;x;10;25', '4/x = 10/25'), ('2,5;4;x;12', '2,5/4 = x/12'), ('6;9;8;12', '6/9 = 8/12 ?'), ('1,2;0,3;8;x', '1,2/0,3 = 8/x')]) + '\n')
  + drill('prop', 'Entrena: calcula x', 'Entrena: calcula x', 'Train: find x'))
s6 += level(1, 1,
  prob(L(r"En una cistella hi ha 18 pomes i 24 peres. Calcula la raó entre pomes i peres i explica què significa.", r"En una cesta hay 18 manzanas y 24 peras. Calcula la razón entre manzanas y peras y explica qué significa.", r"A basket has 18 apples and 24 pears. Find the ratio of apples to pears and explain what it means."),
       r'\[\frac{18}{24}=\boxed{\frac{3}{4}}=0\dc75\]',
       P(r"Per cada 3 pomes hi ha 4 peres.", r"Por cada 3 manzanas hay 4 peras.", r"For every 3 apples there are 4 pears.")))
s6 += level(2, 2,
  prob(L(r"Comprova si formen proporció: a) \(\frac{6}{9}\) i \(\frac{8}{12}\) &nbsp; b) \(\frac{2\dc5}{4}\) i \(\frac{5}{9}\). Calcula \(x\) en \(\frac{x}{8}=\frac{15}{24}\).", r"Comprueba si forman proporción: a) \(\frac{6}{9}\) y \(\frac{8}{12}\) &nbsp; b) \(\frac{2\dc5}{4}\) y \(\frac{5}{9}\). Calcula \(x\) en \(\frac{x}{8}=\frac{15}{24}\).", r"Check whether they form a proportion: a) \(\frac{6}{9}\) and \(\frac{8}{12}\) &nbsp; b) \(\frac{2\dc5}{4}\) and \(\frac{5}{9}\). Find \(x\) in \(\frac{x}{8}=\frac{15}{24}\)."),
       r'\[\text{a) }6\cdot12=72=9\cdot8\ \Rightarrow\ \tri{Sí}{Sí}{Yes}\qquad\text{b) }2\dc5\cdot9=22\dc5\neq4\cdot5=20\ \Rightarrow\ \text{No}\]',
       r'\[x\cdot24=8\cdot15=120\ \Rightarrow\ x=\frac{120}{24}=\boxed{5}\]'))
ck(Dm('2.5') * 9, '22.5'); ck(Fr(8 * 15, 24), 5)
s6 += level(3, 3,
  prob(L(r"Per a fer una massa de pizza fan falta 300 g de farina per cada 180 mL d'aigua. Si tenim 750 g de farina, quanta aigua necessitem?", r"Para hacer una masa de pizza hacen falta 300 g de harina por cada 180 mL de agua. Si tenemos 750 g de harina, ¿cuánta agua necesitamos?", r"Pizza dough needs 300 g of flour for every 180 mL of water. If we have 750 g of flour, how much water do we need?"),
       P(r"La raó farina/aigua ha de ser la mateixa:", r"La razón harina/agua tiene que ser la misma:", r"The flour/water ratio must stay the same:"),
       r'\[\frac{300}{180}=\frac{750}{x}\ \Rightarrow\ 300\cdot x=180\cdot750=135\,000\ \Rightarrow\ x=\frac{135\,000}{300}=\boxed{450\ \text{mL}}\]'))
ck(Fr(180 * 750, 300), 450)
s6 += practice([
  ('★', L(r"a) En un equip hi ha 8 jugadors i 2 entrenadors. Quina és la raó jugadors/entrenadors? b) Formen proporció \(\frac{4}{10}\) i \(\frac{6}{15}\)?", r"a) En un equipo hay 8 jugadores y 2 entrenadores. ¿Cuál es la razón jugadores/entrenadores? b) ¿Forman proporción \(\frac{4}{10}\) y \(\frac{6}{15}\)?", r"a) A team has 8 players and 2 coaches. What is the players/coaches ratio? b) Do \(\frac{4}{10}\) and \(\frac{6}{15}\) form a proportion?")),
  ('★★', L(r"c) Calcula \(x\): \(\frac{4}{x}=\frac{10}{25}\). d) Calcula \(x\): \(\frac{2\dc5}{4}=\frac{x}{12}\).", r"c) Calcula \(x\): \(\frac{4}{x}=\frac{10}{25}\). d) Calcula \(x\): \(\frac{2\dc5}{4}=\frac{x}{12}\).", r"c) Find \(x\): \(\frac{4}{x}=\frac{10}{25}\). d) Find \(x\): \(\frac{2\dc5}{4}=\frac{x}{12}\).")),
  ('★★★', L(r"e) La raó entre l'edat d'una mare i la de la seua filla és \(\frac{7}{2}\). Si la filla té 12 anys, quants en té la mare?", r"e) La razón entre la edad de una madre y la de su hija es \(\frac{7}{2}\). Si la hija tiene 12 años, ¿cuántos tiene la madre?", r"e) The ratio of a mother's age to her daughter's is \(\frac{7}{2}\). If the daughter is 12, how old is the mother?"))],
  P(r"a) \(\frac{8}{2}=4\): 4 jugadors per entrenador. &nbsp; b) Sí: \(4\cdot15=60=10\cdot6\).", r"a) \(\frac{8}{2}=4\): 4 jugadores por entrenador. &nbsp; b) Sí: \(4\cdot15=60=10\cdot6\).", r"a) \(\frac{8}{2}=4\): 4 players per coach. &nbsp; b) Yes: \(4\cdot15=60=10\cdot6\).")
  + P(r"c) \(x=\frac{4\cdot25}{10}=10\). &nbsp; d) \(x=\frac{2\dc5\cdot12}{4}=7\dc5\). &nbsp; e) \(\frac{x}{12}=\frac{7}{2}\Rightarrow x=42\) anys.", r"c) \(x=\frac{4\cdot25}{10}=10\). &nbsp; d) \(x=\frac{2\dc5\cdot12}{4}=7\dc5\). &nbsp; e) \(\frac{x}{12}=\frac{7}{2}\Rightarrow x=42\) años.", r"c) \(x=\frac{4\cdot25}{10}=10\). &nbsp; d) \(x=\frac{2\dc5\cdot12}{4}=7\dc5\). &nbsp; e) \(\frac{x}{12}=\frac{7}{2}\Rightarrow x=42\) years."))
ck(Fr(100, 10), 10); ck(Dm('2.5') * 12 / 4, '7.5'); ck(Fr(7 * 12, 2), 42)

# ============================================================ 5.7
s7 = box('def', L('Magnituds directament proporcionals', 'Magnitudes directamente proporcionales', 'Directly proportional quantities'),
  P(r"Una <strong>magnitud</strong> és tot allò que es pot mesurar: el pes, el preu, el temps, la distància… Dues magnituds són <strong>directament proporcionals</strong> si, quan multipliquem (o dividim) una per un nombre, l'altra queda multiplicada (o dividida) pel <strong>mateix</strong> nombre.",
    r"Una <strong>magnitud</strong> es todo aquello que se puede medir: el peso, el precio, el tiempo, la distancia… Dos magnitudes son <strong>directamente proporcionales</strong> si, cuando multiplicamos (o dividimos) una por un número, la otra queda multiplicada (o dividida) por el <strong>mismo</strong> número.",
    r"A <strong>quantity</strong> (magnitude) is anything we can measure: weight, price, time, distance… Two quantities are <strong>directly proportional</strong> if, when one is multiplied (or divided) by a number, the other is multiplied (or divided) by the <strong>same</strong> number.")
  + P(r"Exemple: les pomes costen \(1\dc80\) € el quilo.", r"Ejemplo: las manzanas cuestan \(1\dc80\) € el kilo.", r"Example: apples cost \(1\dc80\) € a kilo.")
  + table([L('Pes (kg)', 'Peso (kg)', 'Weight (kg)'), '1', '2', '3', '5', '10'], [[L('Preu (€)', 'Precio (€)', 'Price (€)'), r'\(1\dc80\)', r'\(3\dc60\)', r'\(5\dc40\)', r'\(9\)', r'\(18\)']], 'data ptab')
  + P(r"Si dividim cada preu entre el seu pes, sempre ens dona el mateix: \(\frac{3\dc60}{2}=\frac{5\dc40}{3}=\frac{9}{5}=1\dc80\). Aquest nombre és la <strong>constant de proporcionalitat</strong> (aquí, el preu d'un quilo).",
      r"Si dividimos cada precio entre su peso, siempre da lo mismo: \(\frac{3\dc60}{2}=\frac{5\dc40}{3}=\frac{9}{5}=1\dc80\). Este número es la <strong>constante de proporcionalidad</strong> (aquí, el precio de un kilo).",
      r"Dividing each price by its weight always gives the same number: \(\frac{3\dc60}{2}=\frac{5\dc40}{3}=\frac{9}{5}=1\dc80\). This is the <strong>constant of proportionality</strong> (here, the price of one kilo).")
  + figs((svg_points([(1, 1.8), (2, 3.6), (3, 5.4), (5, 9)], 6, 11, 'kg', '€', line=1.8), L('Els punts estan sobre una recta que passa per l\'origen', 'Los puntos están sobre una recta que pasa por el origen', 'The points lie on a straight line through the origin')))
  + note(r"<strong>Compte!</strong> No n'hi ha prou que «si una augmenta, l'altra també». L'edat i l'altura d'una persona augmenten juntes, però als 20 anys no fem el doble que als 10. I el preu d'un taxi amb baixada de bandera tampoc no és proporcional als quilòmetres.",
         r"<strong>¡Cuidado!</strong> No basta con que «si una aumenta, la otra también». La edad y la altura de una persona aumentan juntas, pero a los 20 años no medimos el doble que a los 10. Y el precio de un taxi con bajada de bandera tampoco es proporcional a los kilómetros.",
         r"<strong>Careful!</strong> It isn't enough that “when one goes up, so does the other”. A person's age and height both increase, but at 20 we aren't twice as tall as at 10. And a taxi fare with a fixed starting charge isn't proportional to the distance either.", '⚠️'))
s7 += box('prop', L('Dos mètodes per a resoldre problemes', 'Dos métodos para resolver problemas', 'Two ways to solve problems'),
  P(r"<strong>Problema:</strong> 3 kg de taronges costen \(5\dc40\) €. Quant costen 7 kg?", r"<strong>Problema:</strong> 3 kg de naranjas cuestan \(5\dc40\) €. ¿Cuánto cuestan 7 kg?", r"<strong>Problem:</strong> 3 kg of oranges cost \(5\dc40\) €. How much do 7 kg cost?")
  + P(r"<strong>1. Reducció a la unitat.</strong> Calculem primer quant val una unitat i després multipliquem:", r"<strong>1. Reducción a la unidad.</strong> Calculamos primero cuánto vale una unidad y después multiplicamos:", r"<strong>1. Unit method.</strong> First find the value of one unit, then multiply:")
  + r'\[1\ \text{kg}:\ 5\dc40:3=1\dc80\ €\qquad 7\ \text{kg}:\ 1\dc80\cdot7=\boxed{12\dc60\ €}\]'
  + P(r"<strong>2. Regla de tres directa.</strong> Escrivim les dades en dues files. Com que són directament proporcionals, els valors formen una proporció:", r"<strong>2. Regla de tres directa.</strong> Escribimos los datos en dos filas. Como son directamente proporcionales, los valores forman una proporción:", r"<strong>2. Direct rule of three.</strong> Write the data in two rows. Since the quantities are directly proportional, the values form a proportion:")
  + r3('3', 'kg', r'5\dc40', '€', '7', 'kg', 'x')
  + r'\[\frac{3}{7}=\frac{5\dc40}{x}\ \Rightarrow\ x=\frac{5\dc40\cdot7}{3}=\frac{37\dc8}{3}=\boxed{12\dc60\ €}\]'
  + note(r"Truc per a recordar-ho: en la regla de tres directa, multipliquem <strong>en creu</strong> i dividim entre el que queda.", r"Truco para recordarlo: en la regla de tres directa, multiplicamos <strong>en cruz</strong> y dividimos entre lo que queda.", r"Memory trick: in the direct rule of three, multiply <strong>across</strong> and divide by the remaining number."))
ck(Dm('5.40') / 3 * 7, '12.6'); ck(Dm('5.40') * 7, '37.8')
s7 += widget('w-r3', '📐', L('Regla de tres', 'Regla de tres', 'Rule of three'),
  f'  <div class="wrow">{gseg("t", [("d", L("Directa", "Directa", "Direct")), ("i", L("Inversa", "Inversa", "Inverse"))], "d")}</div>\n'
  + '  <div class="r3in">'
  + nin('a', '', '', '', '3', 's') + nin('ma', '', '', '', 'kg', 'u', 'text') + '<span class="arr">→</span>' + nin('b', '', '', '', '5,40', 's') + nin('mb', '', '', '', '€', 'u', 'text')
  + nin('c', '', '', '', '7', 's') + '<span class="u0"></span><span class="arr">→</span><span class="xq">x</span><span></span></div>\n'
  + '  ' + quick([('d;3;kg;5,40;€;7', '3 kg → 5,40 €'), ('d;5;L;7,50;€;12', '5 L → 7,50 €'), ('d;2;h;150;km;5', '2 h → 150 km'), ('i;4;' + 'pintors;6;dies;3', '4 pintors → 6 dies'), ('i;60;km/h;4;h;80', '60 km/h → 4 h'), ('i;12;' + 'persones;30;dies;20', '12 pers. → 30 dies')]) + '\n')
s7 += level(1, 1,
  prob(L(r"Completa la taula de proporcionalitat directa i calcula la constant:", r"Completa la tabla de proporcionalidad directa y calcula la constante:", r"Complete the direct proportion table and find the constant:")
       + table([L('Entrades', 'Entradas', 'Tickets'), '1', '2', '4', '?', '10'], [[L('Preu (€)', 'Precio (€)', 'Price (€)'), '?', r'\(13\)', '?', r'\(45\dc50\)', '?']], 'data ptab'),
       P(r"Constant: \(13:2=6\dc50\) € per entrada. Multipliquem o dividim per ella:", r"Constante: \(13:2=6\dc50\) € por entrada. Multiplicamos o dividimos por ella:", r"Constant: \(13:2=6\dc50\) € per ticket. Multiply or divide by it:"),
       table([L('Entrades', 'Entradas', 'Tickets'), '1', '2', '4', r'\(\boxed{7}\)', '10'], [[L('Preu (€)', 'Precio (€)', 'Price (€)'), r'\(\boxed{6\dc50}\)', r'\(13\)', r'\(\boxed{26}\)', r'\(45\dc50\)', r'\(\boxed{65}\)']], 'data ptab')))
ck(Dm(13) / 2, '6.5'); ck(Dm('45.50') / Dm('6.5'), '7')
s7 += level(2, 2,
  prob(L(r"Un cotxe gasta \(6\dc5\) L de gasolina cada 100 km. Quants litres gastarà en un viatge de 340 km?", r"Un coche gasta \(6\dc5\) L de gasolina cada 100 km. ¿Cuántos litros gastará en un viaje de 340 km?", r"A car uses \(6\dc5\) L of petrol every 100 km. How many litres will it use on a 340 km trip?"),
       P(r"Com més quilòmetres, més gasolina, i en la mateixa proporció: és directa.", r"Cuantos más kilómetros, más gasolina, y en la misma proporción: es directa.", r"More kilometres means more petrol, in the same proportion: it's direct."),
       r3('100', 'km', r'6\dc5', 'L', '340', 'km', 'x') + r'\[x=\frac{6\dc5\cdot340}{100}=\frac{2210}{100}=\boxed{22\dc1\ \text{L}}\]'))
ck(Dm('6.5') * 340 / 100, '22.1')
s7 += level(3, 3,
  prob(L(r"En un mapa, 2 cm representen 15 km reals. Quina distància real hi ha entre dues ciutats que en el mapa estan a \(9\dc4\) cm? Quants cm hi haurà en el mapa entre dos pobles que estan a 6 km?", r"En un mapa, 2 cm representan 15 km reales. ¿Qué distancia real hay entre dos ciudades que en el mapa están a \(9\dc4\) cm? ¿Cuántos cm habrá en el mapa entre dos pueblos que están a 6 km?", r"On a map, 2 cm stand for 15 real km. What is the real distance between two cities that are \(9\dc4\) cm apart on the map? How many cm apart on the map are two villages 6 km apart?"),
       P(r"Reduïm a la unitat: 1 cm del mapa són \(15:2=7\dc5\) km reals.", r"Reducimos a la unidad: 1 cm del mapa son \(15:2=7\dc5\) km reales.", r"Unit method: 1 cm on the map is \(15:2=7\dc5\) real km."),
       r'\[9\dc4\cdot7\dc5=\boxed{70\dc5\ \text{km}}\qquad 6:7\dc5=60:75=\boxed{0\dc8\ \text{cm}}\]'))
ck(Dm('9.4') * Dm('7.5'), '70.5'); ck(Dm(6) / Dm('7.5'), '0.8')
s7 += practice([
  ('★', L(r"a) Si 4 bolígrafs costen \(3\dc20\) €, quant costen 9 bolígrafs? b) Són directament proporcionals el costat d'un quadrat i el seu perímetre?", r"a) Si 4 bolígrafos cuestan \(3\dc20\) €, ¿cuánto cuestan 9 bolígrafos? b) ¿Son directamente proporcionales el lado de un cuadrado y su perímetro?", r"a) If 4 pens cost \(3\dc20\) €, how much do 9 pens cost? b) Are a square's side and its perimeter directly proportional?")),
  ('★★', L(r"c) Una aixeta omple 120 L en 8 minuts. Quant tardarà a omplir un dipòsit de 450 L? d) En una recepta per a 4 persones fan falta 300 g d'arròs. Quant en farà falta per a 6 persones?", r"c) Un grifo llena 120 L en 8 minutos. ¿Cuánto tardará en llenar un depósito de 450 L? d) En una receta para 4 personas hacen falta 300 g de arroz. ¿Cuánto hará falta para 6 personas?", r"c) A tap fills 120 L in 8 minutes. How long will it take to fill a 450 L tank? d) A recipe for 4 people needs 300 g of rice. How much is needed for 6 people?")),
  ('★★★', L(r"e) Un taxi cobra 3 € per pujar-hi i \(1\dc20\) € per quilòmetre. Fes una taula per a 1, 2 i 5 km. És una relació de proporcionalitat directa?", r"e) Un taxi cobra 3 € por subir y \(1\dc20\) € por kilómetro. Haz una tabla para 1, 2 y 5 km. ¿Es una relación de proporcionalidad directa?", r"e) A taxi charges 3 € to get in and \(1\dc20\) € per kilometre. Make a table for 1, 2 and 5 km. Is it a direct proportion?"))],
  P(r"a) \(3\dc20:4=0\dc80\); \(0\dc80\cdot9=7\dc20\) €. &nbsp; b) Sí: perímetre \(=4\cdot\) costat (constant 4).", r"a) \(3\dc20:4=0\dc80\); \(0\dc80\cdot9=7\dc20\) €. &nbsp; b) Sí: perímetro \(=4\cdot\) lado (constante 4).", r"a) \(3\dc20:4=0\dc80\); \(0\dc80\cdot9=7\dc20\) €. &nbsp; b) Yes: perimeter \(=4\cdot\) side (constant 4).")
  + P(r"c) \(x=\frac{8\cdot450}{120}=30\) minuts. &nbsp; d) \(x=\frac{300\cdot6}{4}=450\) g.", r"c) \(x=\frac{8\cdot450}{120}=30\) minutos. &nbsp; d) \(x=\frac{300\cdot6}{4}=450\) g.", r"c) \(x=\frac{8\cdot450}{120}=30\) minutes. &nbsp; d) \(x=\frac{300\cdot6}{4}=450\) g.")
  + P(r"e) \(4\dc20\), \(5\dc40\) i \(9\) €. No és proporcional: \(\frac{4\dc20}{1}\neq\frac{5\dc40}{2}\) (el doble de km no costa el doble).", r"e) \(4\dc20\), \(5\dc40\) y \(9\) €. No es proporcional: \(\frac{4\dc20}{1}\neq\frac{5\dc40}{2}\) (el doble de km no cuesta el doble).", r"e) \(4\dc20\), \(5\dc40\) and \(9\) €. Not proportional: \(\frac{4\dc20}{1}\neq\frac{5\dc40}{2}\) (twice the km doesn't cost twice as much)."))
ck(Dm('3.20') / 4 * 9, '7.2'); ck(Fr(8 * 450, 120), 30); ck(Fr(300 * 6, 4), 450); ck(3 + Dm('1.2') * 5, '9')

# ============================================================ 5.8
s8 = box('def', L('Magnituds inversament proporcionals', 'Magnitudes inversamente proporcionales', 'Inversely proportional quantities'),
  P(r"Dues magnituds són <strong>inversament proporcionals</strong> si, quan multipliquem una per un nombre, l'altra queda <strong>dividida</strong> pel mateix nombre (i al revés).",
    r"Dos magnitudes son <strong>inversamente proporcionales</strong> si, cuando multiplicamos una por un número, la otra queda <strong>dividida</strong> por el mismo número (y al revés).",
    r"Two quantities are <strong>inversely proportional</strong> if, when one is multiplied by a number, the other is <strong>divided</strong> by the same number (and vice versa).")
  + P(r"Exemple: per a fer un viatge de 240 km, com més ràpid anem, menys temps tardem.", r"Ejemplo: para hacer un viaje de 240 km, cuanto más rápido vamos, menos tiempo tardamos.", r"Example: on a 240 km trip, the faster we go, the less time it takes.")
  + table([L('Velocitat (km/h)', 'Velocidad (km/h)', 'Speed (km/h)'), '40', '60', '80', '120'], [[L('Temps (h)', 'Tiempo (h)', 'Time (h)'), '6', '4', '3', '2']], 'data ptab')
  + P(r"Ara el que es manté és el <strong>producte</strong>: \(40\cdot6=60\cdot4=80\cdot3=120\cdot2=240\) (la distància). És la <strong>constant de proporcionalitat inversa</strong>.",
      r"Ahora lo que se mantiene es el <strong>producto</strong>: \(40\cdot6=60\cdot4=80\cdot3=120\cdot2=240\) (la distancia). Es la <strong>constante de proporcionalidad inversa</strong>.",
      r"Now what stays the same is the <strong>product</strong>: \(40\cdot6=60\cdot4=80\cdot3=120\cdot2=240\) (the distance). It's the <strong>inverse proportionality constant</strong>.")
  + figs((svg_points([(40, 6), (60, 4), (80, 3), (120, 2)], 130, 7, 'km/h', 'h', line=None, curve=240), L('Els punts estan sobre una corba (una hipèrbola)', 'Los puntos están sobre una curva (una hipérbola)', 'The points lie on a curve (a hyperbola)'))))
s8 += box('prop', L('Resoldre problemes de proporcionalitat inversa', 'Resolver problemas de proporcionalidad inversa', 'Solving inverse proportion problems'),
  P(r"<strong>Problema:</strong> 4 pintors pinten una casa en 6 dies. Quant tardarien 3 pintors?", r"<strong>Problema:</strong> 4 pintores pintan una casa en 6 días. ¿Cuánto tardarían 3 pintores?", r"<strong>Problem:</strong> 4 painters paint a house in 6 days. How long would 3 painters take?")
  + P(r"<strong>1. Reducció a la unitat.</strong> Un sol pintor tardaria 4 vegades més: \(6\cdot4=24\) dies. Tres pintors tardaran la tercera part: \(24:3=\boxed{8\ \text{dies}}\).", r"<strong>1. Reducción a la unidad.</strong> Un solo pintor tardaría 4 veces más: \(6\cdot4=24\) días. Tres pintores tardarán la tercera parte: \(24:3=\boxed{8\ \text{días}}\).", r"<strong>1. Unit method.</strong> One painter alone would take 4 times as long: \(6\cdot4=24\) days. Three painters take a third of that: \(24:3=\boxed{8\ \text{days}}\).")
  + P(r"<strong>2. Regla de tres inversa.</strong> El producte es manté: \(4\cdot6=3\cdot x\).", r"<strong>2. Regla de tres inversa.</strong> El producto se mantiene: \(4\cdot6=3\cdot x\).", r"<strong>2. Inverse rule of three.</strong> The product stays the same: \(4\cdot6=3\cdot x\).")
  + r3('4', r'\tri{pintors}{pintores}{painters}', '6', r'\tri{dies}{días}{days}', '3', r'\tri{pintors}{pintores}{painters}', 'x')
  + r'\[x=\frac{4\cdot6}{3}=\boxed{8\ \tri{dies}{días}{days}}\]'
  + note(r"Abans de calcular, pregunta't: <em>si una magnitud augmenta, l'altra augmenta o disminueix?</em> «Més pintors → menys dies» indica proporcionalitat inversa: multipliquem <strong>en línia</strong> (\(4\cdot6\)) i dividim. Comprova que el resultat té sentit: amb menys pintors, han de ser més dies.",
         r"Antes de calcular, pregúntate: <em>si una magnitud aumenta, ¿la otra aumenta o disminuye?</em> «Más pintores → menos días» indica proporcionalidad inversa: multiplicamos <strong>en línea</strong> (\(4\cdot6\)) y dividimos. Comprueba que el resultado tiene sentido: con menos pintores, tienen que ser más días.",
         r"Before calculating, ask yourself: <em>when one quantity goes up, does the other go up or down?</em> “More painters → fewer days” means inverse proportion: multiply <strong>along the row</strong> (\(4\cdot6\)) and divide. Check the answer makes sense: fewer painters must mean more days."))
s8 += widget('w-kind', '🔎', L('Directa, inversa o cap de les dues?', '¿Directa, inversa o ninguna?', 'Direct, inverse or neither?'),
  '  <div class="ktab"><span class="kl">x</span>' + ''.join(nin(f'x{i}', '', '', '', v, 's') for i, v in enumerate(['1', '2', '3', '6'])) + '<span class="kl">y</span>' + ''.join(nin(f'y{i}', '', '', '', v, 's') for i, v in enumerate(['12', '6', '4', '2'])) + '</div>\n'
  + '  ' + quick([('1;2;3;6;12;6;4;2', 'A'), ('1;2;5;10;1,8;3,6;9;18', 'B'), ('10;12;14;20;140;150;160;190', 'C'), ('2;4;5;8;20;10;8;5', 'D'), ('1;3;4;6;2,5;7,5;10;15', 'E'), ('1;2;3;4;1;4;9;16', 'F')]) + '\n')
s8 += drill('r3', 'Entrena: problemes de regla de tres', 'Entrena: problemas de regla de tres', 'Train: rule-of-three problems')
s8 += level(1, 1,
  prob(L(r"Indica si són directament proporcionals, inversament proporcionals o cap de les dues: a) el nombre d'obrers i el temps que tarden a fer una paret; b) els litres de pintura i els metres quadrats pintats; c) l'edat d'una persona i el seu pes.", r"Indica si son directamente proporcionales, inversamente proporcionales o ninguna de las dos: a) el número de obreros y el tiempo que tardan en hacer una pared; b) los litros de pintura y los metros cuadrados pintados; c) la edad de una persona y su peso.", r"Say whether they're directly proportional, inversely proportional or neither: a) the number of workers and the time they take to build a wall; b) litres of paint and square metres painted; c) a person's age and their weight."),
       ul(L("a) <strong>Inversa</strong>: el doble d'obrers tarden la meitat.", "a) <strong>Inversa</strong>: el doble de obreros tardan la mitad.", "a) <strong>Inverse</strong>: twice as many workers take half the time."),
          L("b) <strong>Directa</strong>: el doble de pintura pinta el doble de superfície.", "b) <strong>Directa</strong>: el doble de pintura pinta el doble de superficie.", "b) <strong>Direct</strong>: twice the paint covers twice the area."),
          L("c) <strong>Cap de les dues</strong>: augmenten juntes al principi, però no en la mateixa proporció.", "c) <strong>Ninguna</strong>: aumentan juntas al principio, pero no en la misma proporción.", "c) <strong>Neither</strong>: they grow together at first, but not in the same proportion."))))
s8 += level(2, 2,
  prob(L(r"Un grup de 12 persones té menjar per a 30 dies. Si se n'hi afegeixen 8 més, per a quants dies tindran menjar?", r"Un grupo de 12 personas tiene comida para 30 días. Si se añaden 8 más, ¿para cuántos días tendrán comida?", r"A group of 12 people has food for 30 days. If 8 more join them, how many days will the food last?"),
       P(r"Ara són \(12+8=20\) persones. Més persones → menys dies: és inversa.", r"Ahora son \(12+8=20\) personas. Más personas → menos días: es inversa.", r"Now there are \(12+8=20\) people. More people → fewer days: it's inverse."),
       r3('12', r'pers.', '30', r'\tri{dies}{días}{days}', '20', 'pers.', 'x') + r'\[x=\frac{12\cdot30}{20}=\frac{360}{20}=\boxed{18\ \tri{dies}{días}{days}}\]'))
ck(Fr(12 * 30, 20), 18)
s8 += level(3, 3,
  prob(L(r"Per a repartir l'aigua d'un dipòsit fan falta 60 garrafes de 5 L. Quantes garrafes de \(1\dc5\) L farien falta? I si només tenim 25 garrafes iguals, de quina capacitat haurien de ser?", r"Para repartir el agua de un depósito hacen falta 60 garrafas de 5 L. ¿Cuántas garrafas de \(1\dc5\) L harían falta? Y si solo tenemos 25 garrafas iguales, ¿de qué capacidad tendrían que ser?", r"Sharing out the water in a tank takes 60 jugs of 5 L. How many \(1\dc5\) L jugs would be needed? And if we only have 25 identical jugs, what capacity should they have?"),
       P(r"La constant (producte) és la capacitat del dipòsit: \(60\cdot5=300\) L.", r"La constante (producto) es la capacidad del depósito: \(60\cdot5=300\) L.", r"The constant (product) is the tank's capacity: \(60\cdot5=300\) L."),
       r'\[300:1\dc5=3000:15=\boxed{200\ \tri{garrafes}{garrafas}{jugs}}\qquad 300:25=\boxed{12\ \text{L}}\]'))
ck(Dm(300) / Dm('1.5'), '200'); ck(Dm(300) / 25, '12')
s8 += practice([
  ('★', L(r"a) Si 3 aixetes omplin una piscina en 10 hores, quant tardaran 5 aixetes iguals? b) Completa la taula inversa: \(\ x:\ 2,\ 4,\ 8\ \); \(\ y:\ 20,\ ?,\ ?\)", r"a) Si 3 grifos llenan una piscina en 10 horas, ¿cuánto tardarán 5 grifos iguales? b) Completa la tabla inversa: \(\ x:\ 2,\ 4,\ 8\ \); \(\ y:\ 20,\ ?,\ ?\)", r"a) If 3 taps fill a pool in 10 hours, how long will 5 identical taps take? b) Complete the inverse table: \(\ x:\ 2,\ 4,\ 8\ \); \(\ y:\ 20,\ ?,\ ?\)")),
  ('★★', L(r"c) Un tren a 90 km/h tarda 2 hores a fer un trajecte. Quant tardaria a 120 km/h? d) Amb 15 € per persona, 8 amics paguen un regal. Quant hauria de pagar cada un si foren 12?", r"c) Un tren a 90 km/h tarda 2 horas en hacer un trayecto. ¿Cuánto tardaría a 120 km/h? d) Con 15 € por persona, 8 amigos pagan un regalo. ¿Cuánto tendría que pagar cada uno si fueran 12?", r"c) A train at 90 km/h takes 2 hours for a journey. How long at 120 km/h? d) At 15 € each, 8 friends pay for a present. How much would each pay if there were 12?")),
  ('★★★', L(r"e) Hem de posar rajoles en una paret. Amb rajoles de 20 cm de costat en fan falta 450 files; quantes files farien falta amb rajoles de 30 cm? f) Decideix si és directa o inversa i resol: 5 màquines fan una faena en 12 h. Quantes màquines calen per a fer-la en 4 h?", r"e) Tenemos que alicatar una pared. Con azulejos de 20 cm de lado hacen falta 450 filas; ¿cuántas filas harían falta con azulejos de 30 cm? f) Decide si es directa o inversa y resuelve: 5 máquinas hacen un trabajo en 12 h. ¿Cuántas máquinas hacen falta para hacerlo en 4 h?", r"e) We're tiling a wall. With 20 cm tiles we need 450 rows; how many rows with 30 cm tiles? f) Decide whether it's direct or inverse and solve: 5 machines do a job in 12 h. How many machines are needed to do it in 4 h?"))],
  P(r"a) \(\frac{3\cdot10}{5}=6\) h. &nbsp; b) Constant 40: \(y=10\) i \(y=5\).", r"a) \(\frac{3\cdot10}{5}=6\) h. &nbsp; b) Constante 40: \(y=10\) e \(y=5\).", r"a) \(\frac{3\cdot10}{5}=6\) h. &nbsp; b) Constant 40: \(y=10\) and \(y=5\).")
  + P(r"c) \(\frac{90\cdot2}{120}=1\dc5\) h (1 h 30 min). &nbsp; d) El regal val 120 €: \(120:12=10\) €.", r"c) \(\frac{90\cdot2}{120}=1\dc5\) h (1 h 30 min). &nbsp; d) El regalo vale 120 €: \(120:12=10\) €.", r"c) \(\frac{90\cdot2}{120}=1\dc5\) h (1 h 30 min). &nbsp; d) The present costs 120 €: \(120:12=10\) €.")
  + P(r"e) \(\frac{20\cdot450}{30}=300\) files. &nbsp; f) Inversa (menys hores → més màquines): \(\frac{5\cdot12}{4}=15\) màquines.", r"e) \(\frac{20\cdot450}{30}=300\) filas. &nbsp; f) Inversa (menos horas → más máquinas): \(\frac{5\cdot12}{4}=15\) máquinas.", r"e) \(\frac{20\cdot450}{30}=300\) rows. &nbsp; f) Inverse (fewer hours → more machines): \(\frac{5\cdot12}{4}=15\) machines."))
ck(Fr(30, 5), 6); ck(Dm(180) / 120, '1.5'); ck(Fr(20 * 450, 30), 300); ck(Fr(60, 4), 15)

# ============================================================ 5.9
PE = [('50', r'\frac{1}{2}', r'0\dc5', 'la meitat', 'la mitad', 'half'), ('25', r'\frac{1}{4}', r'0\dc25', 'la quarta part', 'la cuarta parte', 'a quarter'),
      ('75', r'\frac{3}{4}', r'0\dc75', 'tres quartes parts', 'tres cuartas partes', 'three quarters'), ('20', r'\frac{1}{5}', r'0\dc2', 'la cinquena part', 'la quinta parte', 'a fifth'),
      ('10', r'\frac{1}{10}', r'0\dc1', 'la desena part', 'la décima parte', 'a tenth'), ('1', r'\frac{1}{100}', r'0\dc01', 'la centèsima part', 'la centésima parte', 'a hundredth'),
      ('100', '1', '1', 'el total', 'el total', 'the whole')]
s9 = box('def', L('Què és un percentatge?', '¿Qué es un porcentaje?', 'What is a percentage?'),
  P(r"Un <strong>percentatge</strong> o <strong>tant per cent</strong> és una raó amb denominador 100. El 35 % (es llig «35 per cent») vol dir <strong>35 de cada 100</strong>. Es pot escriure com a fracció o com a decimal:",
    r"Un <strong>porcentaje</strong> o <strong>tanto por ciento</strong> es una razón con denominador 100. El 35 % (se lee «35 por ciento») quiere decir <strong>35 de cada 100</strong>. Se puede escribir como fracción o como decimal:",
    r"A <strong>percentage</strong> is a ratio with denominator 100. 35% (read “35 percent”) means <strong>35 out of every 100</strong>. It can be written as a fraction or as a decimal:")
  + r'\[35\,\%=\frac{35}{100}=\frac{7}{20}=0\dc35\]'
  + figs((pgrid(35), r'\(35\,\%\)'))
  + table([L('Percentatge', 'Porcentaje', 'Percentage'), L('Fracció', 'Fracción', 'Fraction'), L('Decimal', 'Decimal', 'Decimal'), L('Vol dir…', 'Quiere decir…', 'Means…')],
          [[r'\(%s\,\%%\)' % p, r'\(%s\)' % f, r'\(%s\)' % d, L(va, es, en)] for p, f, d, va, es, en in PE]))
ck(Fr(35, 100), Fr(7, 20))
s9 += box('prop', L("Calcular el percentatge d'una quantitat", 'Calcular el porcentaje de una cantidad', 'Finding a percentage of an amount'),
  P(r"Multipliquem la quantitat pel percentatge escrit en forma <strong>decimal</strong> (o multipliquem pel percentatge i dividim entre 100):", r"Multiplicamos la cantidad por el porcentaje escrito en forma <strong>decimal</strong> (o multiplicamos por el porcentaje y dividimos entre 100):", r"Multiply the amount by the percentage written as a <strong>decimal</strong> (or multiply by the percentage and divide by 100):")
  + r'\[35\,\%\ \tri{de}{de}{of}\ 80=80\cdot0\dc35=\boxed{28}\qquad\text{o}\qquad\frac{35\cdot80}{100}=\frac{2800}{100}=28\]'
  + note(r"També és una regla de tres directa: si de 100 en prenem 35, de 80 en prenem \(x\): \(\ x=\frac{80\cdot35}{100}=28\).", r"También es una regla de tres directa: si de 100 tomamos 35, de 80 tomamos \(x\): \(\ x=\frac{80\cdot35}{100}=28\).", r"It's also a direct rule of three: if out of 100 we take 35, out of 80 we take \(x\): \(\ x=\frac{80\cdot35}{100}=28\)."))
ck(80 * Dm('0.35'), '28')
s9 += box('prop', L('Els altres dos problemes', 'Los otros dos problemas', 'The other two problems'),
  P(r"<strong>Quin percentatge representa?</strong> Dividim la part entre el total i multipliquem per 100. En un examen de 40 preguntes n'encertem 34:", r"<strong>¿Qué porcentaje representa?</strong> Dividimos la parte entre el total y multiplicamos por 100. En un examen de 40 preguntas acertamos 34:", r"<strong>What percentage is it?</strong> Divide the part by the whole and multiply by 100. In a 40-question test we get 34 right:")
  + r'\[\frac{34}{40}=0\dc85=\boxed{85\,\%}\]'
  + P(r"<strong>Quin és el total?</strong> Si sabem la part i el percentatge, dividim la part entre el percentatge en forma decimal. Si 18 alumnes són el 30 % de la classe:", r"<strong>¿Cuál es el total?</strong> Si sabemos la parte y el porcentaje, dividimos la parte entre el porcentaje en forma decimal. Si 18 alumnos son el 30 % de la clase:", r"<strong>What is the whole?</strong> If we know the part and the percentage, divide the part by the percentage as a decimal. If 18 students are 30% of the class:")
  + r'\[\text{Total}=18:0\dc3=180:3=\boxed{60\ \tri{alumnes}{alumnos}{students}}\qquad(\tri{comprovació}{comprobación}{check}:\ 60\cdot0\dc3=18\ ✓)\]')
ck(Dm(34) / 40, '0.85'); ck(Dm(18) / Dm('0.3'), '60')
s9 += widget('w-pct', '💯', L('Calculadora de percentatges', 'Calculadora de porcentajes', 'Percentage calculator'),
  f'  <div class="wrow">{gseg("m", [("a", L("Calcula la part", "Calcula la parte", "Find the part")), ("p", L("Calcula el %", "Calcula el %", "Find the %")), ("n", L("Calcula el total", "Calcula el total", "Find the whole"))], "a")}</div>\n'
  + f'  <div class="wrow" style="margin-top:8px">{nin("p", "Percentatge (%)", "Porcentaje (%)", "Percentage (%)", "35", "s")}{nin("n", "Total", "Total", "Whole", "80", "s")}{nin("a", "Part", "Parte", "Part", "28", "s")}</div>\n'
  + '  ' + quick([('a;35;80', '35 % de 80'), ('a;12;250', '12 % de 250'), ('a;7,5;60', '7,5 % de 60'), ('p;;40;34', '34 de 40'), ('p;;25;6', '6 de 25'), ('n;30;;18', '18 → 30 %'), ('n;15;;9', '9 → 15 %')]) + '\n')
s9 += drill('pct', 'Entrena: percentatges', 'Entrena: porcentajes', 'Train: percentages')
s9 += level(1, 1,
  prob(L(r"Escriu com a fracció irreductible i com a decimal: a) \(40\,\%\) &nbsp; b) \(5\,\%\) &nbsp; c) \(120\,\%\). Calcula: d) el \(15\,\%\) de 60 &nbsp; e) el \(8\,\%\) de 350", r"Escribe como fracción irreducible y como decimal: a) \(40\,\%\) &nbsp; b) \(5\,\%\) &nbsp; c) \(120\,\%\). Calcula: d) el \(15\,\%\) de 60 &nbsp; e) el \(8\,\%\) de 350", r"Write as a fraction in simplest form and as a decimal: a) \(40\%\) &nbsp; b) \(5\%\) &nbsp; c) \(120\%\). Work out: d) \(15\%\) of 60 &nbsp; e) \(8\%\) of 350"),
       r'\[\text{a) }\frac{40}{100}=\frac{2}{5}=0\dc4\qquad\text{b) }\frac{5}{100}=\frac{1}{20}=0\dc05\qquad\text{c) }\frac{120}{100}=\frac{6}{5}=1\dc2\]',
       r'\[\text{d) }60\cdot0\dc15=\boxed{9}\qquad\text{e) }350\cdot0\dc08=\boxed{28}\]'))
ck(60 * Dm('0.15'), '9'); ck(350 * Dm('0.08'), '28')
s9 += level(2, 2,
  prob(L(r"En un institut de 650 alumnes, 91 vénen amb bicicleta. Quin percentatge representen?", r"En un instituto de 650 alumnos, 91 vienen en bicicleta. ¿Qué porcentaje representan?", r"In a school of 650 students, 91 come by bike. What percentage is that?"),
       r'\[\frac{91}{650}=0\dc14=\boxed{14\,\%}\]'))
ck(Dm(91) / 650, '0.14')
s9 += level(3, 3,
  prob(L(r"Hem llegit 135 pàgines d'un llibre, que són el \(45\,\%\) del total. Quantes pàgines té el llibre? Quantes ens en falten?", r"Hemos leído 135 páginas de un libro, que son el \(45\,\%\) del total. ¿Cuántas páginas tiene el libro? ¿Cuántas nos faltan?", r"We've read 135 pages of a book, which is \(45\%\) of it. How many pages does the book have? How many are left?"),
       r'\[\text{Total}=135:0\dc45=13\,500:45=\boxed{300\ \tri{pàgines}{páginas}{pages}}\qquad\tri{Falten}{Faltan}{Left}:\ 300-135=\boxed{165}\]',
       P(r"També: falta el \(55\,\%\), i \(300\cdot0\dc55=165\). ✓", r"También: falta el \(55\,\%\), y \(300\cdot0\dc55=165\). ✓", r"Also: \(55\%\) is left, and \(300\cdot0\dc55=165\). ✓")))
ck(Dm(135) / Dm('0.45'), '300'); ck(300 * Dm('0.55'), '165')
s9 += practice([
  ('★', L(r"a) Calcula el \(20\,\%\) de 45 i el \(75\,\%\) de 120. b) Escriu \(0\dc06\) i \(\frac{3}{5}\) com a percentatge.", r"a) Calcula el \(20\,\%\) de 45 y el \(75\,\%\) de 120. b) Escribe \(0\dc06\) y \(\frac{3}{5}\) como porcentaje.", r"a) Work out \(20\%\) of 45 and \(75\%\) of 120. b) Write \(0\dc06\) and \(\frac{3}{5}\) as percentages.")),
  ('★★', L(r"c) En una classe de 25 alumnes, 6 porten ulleres. Quin percentatge en porta? d) El \(2\dc5\,\%\) de 840.", r"c) En una clase de 25 alumnos, 6 llevan gafas. ¿Qué porcentaje lleva? d) El \(2\dc5\,\%\) de 840.", r"c) In a class of 25, 6 wear glasses. What percentage is that? d) \(2\dc5\%\) of 840.")),
  ('★★★', L(r"e) Un 15 % dels habitants d'un poble són menors de 12 anys, i són 63 xiquets. Quants habitants té el poble? f) Què és més, el \(30\,\%\) de 50 o el \(50\,\%\) de 30?", r"e) Un 15 % de los habitantes de un pueblo son menores de 12 años, y son 63 niños. ¿Cuántos habitantes tiene el pueblo? f) ¿Qué es más, el \(30\,\%\) de 50 o el \(50\,\%\) de 30?", r"e) 15% of a village's inhabitants are under 12, and there are 63 children. How many inhabitants does the village have? f) Which is more, \(30\%\) of 50 or \(50\%\) of 30?"))],
  P(r"a) \(9\) i \(90\). &nbsp; b) \(6\,\%\) i \(60\,\%\).", r"a) \(9\) y \(90\). &nbsp; b) \(6\,\%\) y \(60\,\%\).", r"a) \(9\) and \(90\). &nbsp; b) \(6\%\) and \(60\%\).")
  + P(r"c) \(\frac{6}{25}=0\dc24=24\,\%\). &nbsp; d) \(840\cdot0\dc025=21\).", r"c) \(\frac{6}{25}=0\dc24=24\,\%\). &nbsp; d) \(840\cdot0\dc025=21\).", r"c) \(\frac{6}{25}=0\dc24=24\%\). &nbsp; d) \(840\cdot0\dc025=21\).")
  + P(r"e) \(63:0\dc15=420\) habitants. &nbsp; f) Són iguals: \(50\cdot0\dc3=15=30\cdot0\dc5\).", r"e) \(63:0\dc15=420\) habitantes. &nbsp; f) Son iguales: \(50\cdot0\dc3=15=30\cdot0\dc5\).", r"e) \(63:0\dc15=420\) inhabitants. &nbsp; f) They're equal: \(50\cdot0\dc3=15=30\cdot0\dc5\)."))
ck(45 * Dm('0.2'), '9'); ck(120 * Dm('0.75'), '90'); ck(Dm(6) / 25, '0.24'); ck(840 * Dm('0.025'), '21'); ck(Dm(63) / Dm('0.15'), '420')

# ============================================================ 5.10
s10 = box('prop', L('Disminucions percentuals: descomptes i rebaixes', 'Disminuciones porcentuales: descuentos y rebajas', 'Percentage decreases: discounts and sales'),
  P(r"Una jaqueta de 80 € té un descompte del 15 %. Podem calcular-ho de dues maneres:", r"Una chaqueta de 80 € tiene un descuento del 15 %. Podemos calcularlo de dos maneras:", r"An 80 € jacket has a 15% discount. We can work it out in two ways:")
  + ol(L(r"Calculem el descompte i el restem: \(\ 80\cdot0\dc15=12\) €; \(\ 80-12=\boxed{68\ €}\).", r"Calculamos el descuento y lo restamos: \(\ 80\cdot0\dc15=12\) €; \(\ 80-12=\boxed{68\ €}\).", r"Work out the discount and subtract it: \(\ 80\cdot0\dc15=12\) €; \(\ 80-12=\boxed{68\ €}\)."),
       L(r"Si ens descompten el 15 %, paguem el \(100-15=85\,\%\): \(\ 80\cdot0\dc85=\boxed{68\ €}\).", r"Si nos descuentan el 15 %, pagamos el \(100-15=85\,\%\): \(\ 80\cdot0\dc85=\boxed{68\ €}\).", r"If we get 15% off, we pay \(100-15=85\%\): \(\ 80\cdot0\dc85=\boxed{68\ €}\).")))
ck(80 * Dm('0.85'), '68')
s10 += box('prop', L('Augments percentuals: l\'IVA', 'Aumentos porcentuales: el IVA', 'Percentage increases: VAT'),
  P(r"A molts preus se'ls afegeix l'IVA, un impost del 21 %. Si un producte val 50 € sense IVA:", r"A muchos precios se les añade el IVA, un impuesto del 21 %. Si un producto vale 50 € sin IVA:", r"Many prices have VAT (IVA in Spain) added, a 21% tax. If an item costs 50 € before VAT:")
  + ol(L(r"Calculem l'augment i el sumem: \(\ 50\cdot0\dc21=10\dc50\) €; \(\ 50+10\dc50=\boxed{60\dc50\ €}\).", r"Calculamos el aumento y lo sumamos: \(\ 50\cdot0\dc21=10\dc50\) €; \(\ 50+10\dc50=\boxed{60\dc50\ €}\).", r"Work out the increase and add it: \(\ 50\cdot0\dc21=10\dc50\) €; \(\ 50+10\dc50=\boxed{60\dc50\ €}\)."),
       L(r"Paguem el \(100+21=121\,\%\): \(\ 50\cdot1\dc21=\boxed{60\dc50\ €}\).", r"Pagamos el \(100+21=121\,\%\): \(\ 50\cdot1\dc21=\boxed{60\dc50\ €}\).", r"We pay \(100+21=121\%\): \(\ 50\cdot1\dc21=\boxed{60\dc50\ €}\).")))
ck(50 * Dm('1.21'), '60.50')
s10 += box('def', L('Índex de variació', 'Índice de variación', 'Multiplier'),
  P(r"El nombre pel qual multipliquem en el segon mètode s'anomena <strong>índex de variació</strong>:", r"El número por el que multiplicamos en el segundo método se llama <strong>índice de variación</strong>:", r"The number we multiply by in the second method is called the <strong>multiplier</strong>:")
  + table([L('Variació', 'Variación', 'Change'), L('Índex', 'Índice', 'Multiplier'), L('Exemple', 'Ejemplo', 'Example')],
          [[L('Augment del \\(p\\,\\%\\)', 'Aumento del \\(p\\,\\%\\)', '\\(p\\%\\) increase'), r'\(1+\frac{p}{100}\)', r'\(+21\,\%\ \to\ 1\dc21\)'],
           [L('Disminució del \\(p\\,\\%\\)', 'Disminución del \\(p\\,\\%\\)', '\\(p\\%\\) decrease'), r'\(1-\frac{p}{100}\)', r'\(-15\,\%\ \to\ 0\dc85\)']])
  + r'\[\tri{Quantitat final}{Cantidad final}{Final amount}=\tri{Quantitat inicial}{Cantidad inicial}{Starting amount}\cdot\tri{índex de variació}{índice de variación}{multiplier}\]'
  + note(r"Per a trobar la quantitat <strong>inicial</strong>, fem l'operació inversa: dividim. Si després d'una rebaixa del 15 % paguem 68 €, el preu inicial era \(68:0\dc85=80\) €. <strong>No</strong> és \(68+15\,\%\) de 68!",
         r"Para encontrar la cantidad <strong>inicial</strong>, hacemos la operación inversa: dividimos. Si después de una rebaja del 15 % pagamos 68 €, el precio inicial era \(68:0\dc85=80\) €. ¡<strong>No</strong> es \(68+15\,\%\) de 68!",
         r"To find the <strong>starting</strong> amount, do the inverse: divide. If after a 15% discount we pay 68 €, the original price was \(68:0\dc85=80\) €. It is <strong>not</strong> \(68+15\%\) of 68!", '⚠️'))
ck(Dm(68) / Dm('0.85'), '80')
s10 += widget('w-var', '🏷️', L('Augments i disminucions', 'Aumentos y disminuciones', 'Increases and decreases'),
  f'  <div class="wrow">{gseg("t", [("+", L("Augment", "Aumento", "Increase")), ("-", L("Disminució", "Disminución", "Decrease"))], "-")}{gseg("w", [("f", L("Calcula el final", "Calcula el final", "Find the final")), ("i", L("Calcula la inicial", "Calcula la inicial", "Find the starting"))], "f")}</div>\n'
  + f'  <div class="wrow" style="margin-top:8px">{nin("q", "Quantitat", "Cantidad", "Amount", "80", "s")}{nin("p", "Percentatge (%)", "Porcentaje (%)", "Percentage (%)", "15", "s")}</div>\n'
  + '  ' + quick([('-;f;80;15', '80 € −15 %'), ('+;f;50;21', '50 € + IVA 21 %'), ('-;f;24,90;30', '24,90 € −30 %'), ('+;f;1200;4', '1200 +4 %'), ('-;i;68;15', '? −15 % = 68'), ('+;i;60,50;21', '? +21 % = 60,50')]) + '\n')
s10 += drill('var', 'Entrena: augments i disminucions', 'Entrena: aumentos y disminuciones', 'Train: increases and decreases')
s10 += level(1, 1,
  prob(L(r"Escriu l'índex de variació: a) augment del 30 % &nbsp; b) disminució del 8 % &nbsp; c) augment del 4 % &nbsp; d) rebaixa del 50 %", r"Escribe el índice de variación: a) aumento del 30 % &nbsp; b) disminución del 8 % &nbsp; c) aumento del 4 % &nbsp; d) rebaja del 50 %", r"Write the multiplier: a) 30% increase &nbsp; b) 8% decrease &nbsp; c) 4% increase &nbsp; d) 50% off"),
       r'\[\text{a) }1\dc3\qquad\text{b) }0\dc92\qquad\text{c) }1\dc04\qquad\text{d) }0\dc5\]'))
s10 += level(2, 2,
  prob(L(r"Unes sabatilles costen \(64\dc90\) € i en rebaixes tenen un 30 % de descompte. Quant costen ara? Arrodoneix als cèntims.", r"Unas zapatillas cuestan \(64\dc90\) € y en rebajas tienen un 30 % de descuento. ¿Cuánto cuestan ahora? Redondea a los céntimos.", r"Trainers cost \(64\dc90\) € and have 30% off in the sales. How much do they cost now? Round to the cent."),
       r'\[64\dc90\cdot0\dc7=45\dc43\ €\]',
       P(r"Ens estalviem \(64\dc90-45\dc43=19\dc47\) €, que és el 30 % de \(64\dc90\).", r"Nos ahorramos \(64\dc90-45\dc43=19\dc47\) €, que es el 30 % de \(64\dc90\).", r"We save \(64\dc90-45\dc43=19\dc47\) €, which is 30% of \(64\dc90\).")))
ck(Dm('64.90') * Dm('0.7'), '45.43'); ck(Dm('64.90') * Dm('0.3'), '19.47')
s10 += level(3, 3,
  prob(L(r"El preu d'un patinet de 200 € puja un 10 % i, al cap d'un mes, baixa un 10 %. Torna a costar 200 €?", r"El precio de un patinete de 200 € sube un 10 % y, al cabo de un mes, baja un 10 %. ¿Vuelve a costar 200 €?", r"A 200 € scooter goes up 10% and, a month later, comes down 10%. Is it back to 200 €?"),
       r'\[200\cdot1\dc1=220\ €\qquad 220\cdot0\dc9=\boxed{198\ €}\]',
       P(r"No! El 10 % de baixada es calcula sobre 220, que és més que 200: baixa 22 € i només havia pujat 20 €.", r"¡No! El 10 % de bajada se calcula sobre 220, que es más que 200: baja 22 € y solo había subido 20 €.", r"No! The 10% drop is worked out on 220, which is more than 200: it drops 22 € but had only risen 20 €.")))
ck(200 * Dm('1.1') * Dm('0.9'), '198')
s10 += practice([
  ('★', L(r"a) Un ordinador de 650 € té un descompte del 12 %. Quant costa? b) Un llibre val 18 € sense IVA (4 %). Quant val amb IVA?", r"a) Un ordenador de 650 € tiene un descuento del 12 %. ¿Cuánto cuesta? b) Un libro vale 18 € sin IVA (4 %). ¿Cuánto vale con IVA?", r"a) A 650 € computer has a 12% discount. How much does it cost? b) A book costs 18 € before VAT (4%). How much is it with VAT?")),
  ('★★', L(r"c) Un poble tenia 2400 habitants i ara en té un 5 % més. Quants habitants té? d) Una samarreta passa de 25 € a 20 €. Quin percentatge de descompte li han fet?", r"c) Un pueblo tenía 2400 habitantes y ahora tiene un 5 % más. ¿Cuántos habitantes tiene? d) Una camiseta pasa de 25 € a 20 €. ¿Qué porcentaje de descuento le han hecho?", r"c) A village had 2400 inhabitants and now has 5% more. How many does it have? d) A T-shirt goes from 25 € to 20 €. What percentage discount is that?")),
  ('★★★', L(r"e) Després d'aplicar l'IVA del 21 %, una factura és de \(108\dc90\) €. Quant valia sense IVA? f) Un preu baixa un 20 % i després puja un 20 %. Al final, és més car o més barat que al principi? En quin percentatge?", r"e) Después de aplicar el IVA del 21 %, una factura es de \(108\dc90\) €. ¿Cuánto valía sin IVA? f) Un precio baja un 20 % y después sube un 20 %. Al final, ¿es más caro o más barato que al principio? ¿En qué porcentaje?", r"e) After adding 21% VAT, a bill comes to \(108\dc90\) €. What was it before VAT? f) A price falls 20% and then rises 20%. Is it dearer or cheaper than at the start? By what percentage?"))],
  P(r"a) \(650\cdot0\dc88=572\) €. &nbsp; b) \(18\cdot1\dc04=18\dc72\) €.", r"a) \(650\cdot0\dc88=572\) €. &nbsp; b) \(18\cdot1\dc04=18\dc72\) €.", r"a) \(650\cdot0\dc88=572\) €. &nbsp; b) \(18\cdot1\dc04=18\dc72\) €.")
  + P(r"c) \(2400\cdot1\dc05=2520\) habitants. &nbsp; d) Descompte de 5 €: \(\frac{5}{25}=0\dc2=20\,\%\).", r"c) \(2400\cdot1\dc05=2520\) habitantes. &nbsp; d) Descuento de 5 €: \(\frac{5}{25}=0\dc2=20\,\%\).", r"c) \(2400\cdot1\dc05=2520\) inhabitants. &nbsp; d) 5 € off: \(\frac{5}{25}=0\dc2=20\%\).")
  + P(r"e) \(108\dc90:1\dc21=90\) €. &nbsp; f) \(0\dc8\cdot1\dc2=0\dc96\): és un 4 % més barat (per exemple, 100 € → 80 € → 96 €).", r"e) \(108\dc90:1\dc21=90\) €. &nbsp; f) \(0\dc8\cdot1\dc2=0\dc96\): es un 4 % más barato (por ejemplo, 100 € → 80 € → 96 €).", r"e) \(108\dc90:1\dc21=90\) €. &nbsp; f) \(0\dc8\cdot1\dc2=0\dc96\): it's 4% cheaper (e.g. 100 € → 80 € → 96 €)."))
ck(650 * Dm('0.88'), '572'); ck(18 * Dm('1.04'), '18.72'); ck(2400 * Dm('1.05'), '2520'); ck(Dm('108.90') / Dm('1.21'), '90'); ck(Dm('0.8') * Dm('1.2'), '0.96')
