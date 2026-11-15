# Genera t6-fitxa-exercicis.tex i t6-fitxa-solucions.tex (2n ESO, Unitat 6: Proporcionalitat i percentatges)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Les 8 seccions segueixen els apartats dels apunts (6.1-6.8).
# Text bilingüe: T(valencià, castellà). Aquest mateix fitxer genera la versió en castellà quan l'executa genera-es.py
# (variable d'entorn FM_LANG=es).
# Tots els resultats escrits a mà es comproven amb ck() (fraccions i decimals exactes).
# Ús: python3 genera.py && pdflatex t6-fitxa-exercicis.tex (dues vegades) && pdflatex t6-fitxa-solucions.tex (dues vegades)
#     python3 genera-es.py (i el mateix amb els -es.tex)
import os, re
from decimal import Decimal as Dm
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
ES = os.environ.get('FM_LANG') == 'es'
def T(va, es): return es if ES else va

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def ck(a, b):
    """a == b, amb a i b enters, Fraction, Decimal o text decimal"""
    f = lambda v: Fr(str(v)) if isinstance(v, (str, Dm)) else Fr(v)
    assert f(a) == f(b), (a, b)
def D(s): return Dm(s)
def r3(a, ma, b, mb, c, mc, x='x'):
    return r'$\begin{array}{rcl}%s\ \text{%s}&\longrightarrow&%s\ \text{%s}\\ %s\ \text{%s}&\longrightarrow&%s\end{array}$' % (a, ma, b, mb, c, mc, x)
def comp(heads, r1, r2):
    return (r'$\begin{array}{' + 'c' * len(heads) + '}' + ' & '.join(r'\text{%s}' % h for h in heads) + r'\\ \hline ' + ' & '.join(r1) + r'\\ ' + ' & '.join(r2) + r'\end{array}$')
def ptab(r1, r2, h1, h2):
    n = len(r1)
    return (r'\begin{tabular}{l|' + 'c' * n + '}' + h1 + ' & ' + ' & '.join(r1) + r'\\ \hline ' + h2 + ' & ' + ' & '.join(r2) + r'\end{tabular}')

S_ = []
# =====================================================================
# 1. Raons i proporcions
S_.append((T("Raons i proporcions", "Razones y proporciones"), [
 (1, T(r"En un institut hi ha 360 alumnes i 24 professors. Calcula la raó entre alumnes i professors, simplifica-la i explica què significa.", r"En un instituto hay 360 alumnos y 24 profesores. Calcula la razón entre alumnos y profesores, simplifícala y explica qué significa.")
     + recorda(T(r"La raó entre $a$ i $b$ és el quocient $\frac{a}{b}$. Una proporció és una igualtat de dues raons: $\frac{a}{b}=\frac{c}{d}\iff a\cdot d=b\cdot c$.", r"La razón entre $a$ y $b$ es el cociente $\frac{a}{b}$. Una proporción es una igualdad de dos razones: $\frac{a}{b}=\frac{c}{d}\iff a\cdot d=b\cdot c$.")),
     T(r"$\frac{360}{24}=\res{15}$: hi ha 15 alumnes per cada professor.", r"$\frac{360}{24}=\res{15}$: hay 15 alumnos por cada profesor.")),
 (1, T(r"Comprova si formen proporció:", r"Comprueba si forman proporción:") + tasks(4, [r'$\frac{3}{4}$ i $\frac{15}{20}$' if not ES else r'$\frac{3}{4}$ y $\frac{15}{20}$', r'$\frac{5}{6}$ i $\frac{12}{15}$' if not ES else r'$\frac{5}{6}$ y $\frac{12}{15}$', r'$\frac{2{,}5}{2}$ i $\frac{10}{8}$' if not ES else r'$\frac{2{,}5}{2}$ y $\frac{10}{8}$', r'$\frac{7}{9}$ i $\frac{21}{28}$' if not ES else r'$\frac{7}{9}$ y $\frac{21}{28}$']),
     tasks(2, [T(r'$3\cdot20=60=4\cdot15$: \rest{sí}', r'$3\cdot20=60=4\cdot15$: \rest{sí}'), r'$5\cdot15=75\neq6\cdot12=72$: \rest{no}', T(r'$2{,}5\cdot8=20=2\cdot10$: \rest{sí}', r'$2{,}5\cdot8=20=2\cdot10$: \rest{sí}'), r'$7\cdot28=196\neq9\cdot21=189$: \rest{no}'])),
 (2, T(r"Calcula el terme desconegut:", r"Calcula el término desconocido:") + tasks(4, [r'$\frac{x}{12}=\frac{15}{20}$', r'$\frac{8}{x}=\frac{6}{9}$', r'$\frac{4{,}5}{6}=\frac{x}{8}$', r'$\frac{14}{35}=\frac{6}{x}$']),
     tasks(4, [r'$x=\frac{12\cdot15}{20}=\res{9}$', r'$x=\frac{8\cdot9}{6}=\res{12}$', r'$x=\frac{4{,}5\cdot8}{6}=\res{6}$', r'$x=\frac{35\cdot6}{14}=\res{15}$'])),
 (2, T(r"En un concurs de dibuix es presenten 84 treballs, dels quals 35 són de xics. Quina és la raó entre treballs de xics i de xiques? I entre els de xiques i el total?", r"En un concurso de dibujo se presentan 84 trabajos, de los cuales 35 son de chicos. ¿Cuál es la razón entre trabajos de chicos y de chicas? ¿Y entre los de chicas y el total?"),
     T(r"Xiques: $84-35=49$. Xics/xiques: $\frac{35}{49}=\res{\frac{5}{7}}$; xiques/total: $\frac{49}{84}=\res{\frac{7}{12}}$.", r"Chicas: $84-35=49$. Chicos/chicas: $\frac{35}{49}=\res{\frac{5}{7}}$; chicas/total: $\frac{49}{84}=\res{\frac{7}{12}}$.")),
 (3, T(r"Un batut es fa mesclant llet i maduixes en la raó $\frac{5}{2}$. Si hi posem 750 mL de llet, quantes maduixes (en mL) hi hem de posar? Quina quantitat de batut tindrem?", r"Un batido se hace mezclando leche y fresas en la razón $\frac{5}{2}$. Si ponemos 750 mL de leche, ¿cuántas fresas (en mL) tenemos que poner? ¿Qué cantidad de batido tendremos?"),
     T(r"$\frac{5}{2}=\frac{750}{x}\Rightarrow x=\frac{2\cdot750}{5}=\res{300\ \text{mL}}$ de maduixes; en total, $\res{1050\ \text{mL}}$ de batut.", r"$\frac{5}{2}=\frac{750}{x}\Rightarrow x=\frac{2\cdot750}{5}=\res{300\ \text{mL}}$ de fresas; en total, $\res{1050\ \text{mL}}$ de batido.")),
 (3, T(r"Les edats de dues germanes estan en la raó $\frac{3}{4}$ i entre les dues sumen 28 anys. Quants anys té cadascuna?", r"Las edades de dos hermanas están en la razón $\frac{3}{4}$ y entre las dos suman 28 años. ¿Cuántos años tiene cada una?"),
     T(r"Per cada 3 anys de la menuda, la gran en té 4: $3+4=7$ parts; cada part són $28:7=4$ anys. \rest{12 i 16 anys} (i $\frac{12}{16}=\frac{3}{4}$ \ding{51}).", r"Por cada 3 años de la pequeña, la mayor tiene 4: $3+4=7$ partes; cada parte son $28:7=4$ años. \rest{12 y 16 años} (y $\frac{12}{16}=\frac{3}{4}$ \ding{51}).")),
]))
ck(Fr(360, 24), 15); ck(Fr(3, 4), Fr(15, 20)); assert Fr(5, 6) != Fr(12, 15); ck(D('2.5') * 8, 20); assert Fr(7, 9) != Fr(21, 28)
ck(Fr(12 * 15, 20), 9); ck(Fr(72, 6), 12); ck(D('4.5') * 8 / 6, 6); ck(Fr(35 * 6, 14), 15); ck(Fr(35, 49), Fr(5, 7)); ck(Fr(49, 84), Fr(7, 12))
ck(Fr(1500, 5), 300); ck(Fr(12, 16), Fr(3, 4))

# =====================================================================
# 2. Proporcionalitat directa
S_.append((T("Magnituds directament proporcionals", "Magnitudes directamente proporcionales"), [
 (1, T(r"Indica quines parelles de magnituds són directament proporcionals:", r"Indica qué parejas de magnitudes son directamente proporcionales:")
     + tasks(2, [T(r"El nombre de kg de pomes i el preu.", r"El número de kg de manzanas y el precio."), T(r"L'edat d'una persona i la seua altura.", r"La edad de una persona y su altura."),
                 T(r"El costat d'un quadrat i el seu perímetre.", r"El lado de un cuadrado y su perímetro."), T(r"Els minuts que parlem per un mòbil amb quota fixa mensual i el preu de la factura.", r"Los minutos que hablamos por un móvil con cuota fija mensual y el precio de la factura.")])
     + recorda(T(r"Són directament proporcionals si el doble d'una correspon al doble de l'altra, la meitat a la meitat… El quocient entre les quantitats corresponents és constant.", r"Son directamente proporcionales si el doble de una corresponde al doble de la otra, la mitad a la mitad… El cociente entre las cantidades correspondientes es constante.")),
     tasks(2, [T(r"\rest{Sí} (preu = preu/kg · kg).", r"\rest{Sí} (precio = precio/kg · kg)."), r"\rest{No}.", T(r"\rest{Sí} ($P=4\cdot c$).", r"\rest{Sí} ($P=4\cdot c$)."), T(r"\rest{No} (amb 0 minuts ja paguem la quota).", r"\rest{No} (con 0 minutos ya pagamos la cuota).")])),
 (1, T(r"Completa la taula de proporcionalitat directa i calcula'n la constant:", r"Completa la tabla de proporcionalidad directa y calcula su constante:") + '\\\\[4pt]' + ptab(['2', '5', '8', '', '20'], ['7', '', '', '42', ''], T('Hores', 'Horas'), 'Km'),
     ptab(['2', '5', '8', r'\rest{12}', '20'], ['7', r'\rest{17{,}5}', r'\rest{28}', '42', r'\rest{70}'], T('Hores', 'Horas'), 'Km') + T(r'\quad Constant: $k=\frac{7}{2}=\res{3{,}5}$ km/h.', r'\quad Constante: $k=\frac{7}{2}=\res{3{,}5}$ km/h.')),
 (1, T(r"Si 4 entrades de cine costen 30 €, quant costen 7 entrades? Resol-ho per reducció a la unitat.", r"Si 4 entradas de cine cuestan 30 €, ¿cuánto cuestan 7 entradas? Resuélvelo por reducción a la unidad."),
     T(r"Una entrada: $30:4=7{,}50$ €. Set: $7{,}50\cdot7=\res{52{,}50\ \text{€}}$.", r"Una entrada: $30:4=7{,}50$ €. Siete: $7{,}50\cdot7=\res{52{,}50\ \text{€}}$.")),
 (2, T(r"Un cotxe gasta 6,4 L de gasoil cada 100 km. Resol per regla de tres:", r"Un coche gasta 6,4 L de gasóleo cada 100 km. Resuelve por regla de tres:") + tasks(2, [T(r"Quants litres gasta en 450 km?", r"¿Cuántos litros gasta en 450 km?"), T(r"Quants km pot fer amb 40 L?", r"¿Cuántos km puede hacer con 40 L?")]),
     tasks(2, [r3('100', 'km', '6{,}4', 'L', '450', 'km') + r'\quad $x=\frac{6{,}4\cdot450}{100}=\res{28{,}8\ \text{L}}$', r3('6{,}4', 'L', '100', 'km', '40', 'L') + r'\quad $x=\frac{100\cdot40}{6{,}4}=\res{625\ \text{km}}$'])),
 (2, T(r"Una màquina embotella 1500 botelles en 2 hores i mitja. Quantes en farà en una jornada de 8 hores? Quant tardarà a embotellar-ne 2100?", r"Una máquina embotella 1500 botellas en 2 horas y media. ¿Cuántas hará en una jornada de 8 horas? ¿Cuánto tardará en embotellar 2100?"),
     T(r"En 1 h: $1500:2{,}5=600$ botelles. En 8 h: $600\cdot8=\res{4800}$. Per a 2100: $2100:600=\res{3{,}5\ \text{h}}$ (3 h 30 min).", r"En 1 h: $1500:2{,}5=600$ botellas. En 8 h: $600\cdot8=\res{4800}$. Para 2100: $2100:600=\res{3{,}5\ \text{h}}$ (3 h 30 min).")),
 (2, T(r"Per a fer una paella per a 4 persones fan falta 320 g d'arròs i 1,2 L de brou. Quant en farà falta per a 10 persones?", r"Para hacer una paella para 4 personas hacen falta 320 g de arroz y 1,2 L de caldo. ¿Cuánto hará falta para 10 personas?"),
     T(r"Per persona: 80 g d'arròs i 0,3 L de brou. Per a 10: \rest{800 g d'arròs i 3 L de brou}.", r"Por persona: 80 g de arroz y 0,3 L de caldo. Para 10: \rest{800 g de arroz y 3 L de caldo}.")),
 (3, T(r"En un plànol a escala 1:250, una habitació fa 1,6 cm per 1,4 cm. Quines dimensions reals té? Quina superfície té, en m²?", r"En un plano a escala 1:250, una habitación mide 1,6 cm por 1,4 cm. ¿Qué dimensiones reales tiene? ¿Qué superficie tiene, en m²?"),
     T(r"$1{,}6\cdot250=400$ cm $=4$ m; $\ 1{,}4\cdot250=350$ cm $=3{,}5$ m. Superfície: $4\cdot3{,}5=\res{14\ \text{m}^2}$.", r"$1{,}6\cdot250=400$ cm $=4$ m; $\ 1{,}4\cdot250=350$ cm $=3{,}5$ m. Superficie: $4\cdot3{,}5=\res{14\ \text{m}^2}$.")),
 (3, T(r"Una empresa de lloguer de bicicletes cobra 4 € per hora. Una altra cobra 5 € fixos més 3 € per hora. a) Fes una taula per a 1, 2, 3 i 6 hores per a cada empresa. b) En quin cas el preu és directament proporcional al temps? c) A partir de quantes hores és més barata la segona?", r"Una empresa de alquiler de bicicletas cobra 4 € por hora. Otra cobra 5 € fijos más 3 € por hora. a) Haz una tabla para 1, 2, 3 y 6 horas para cada empresa. b) ¿En qué caso el precio es directamente proporcional al tiempo? c) ¿A partir de cuántas horas es más barata la segunda?"),
     T(r"a) 1a: 4, 8, 12, 24 €; \ 2a: 8, 11, 14, 23 €. b) \rest{Només en la primera} (quocient constant 4); en la segona $\frac{8}{1}\neq\frac{11}{2}$. c) Igualen a les 5 h (20 €); \rest{a partir de 6 hores} és més barata la segona.", r"a) 1.ª: 4, 8, 12, 24 €; \ 2.ª: 8, 11, 14, 23 €. b) \rest{Solo en la primera} (cociente constante 4); en la segunda $\frac{8}{1}\neq\frac{11}{2}$. c) Igualan a las 5 h (20 €); \rest{a partir de 6 horas} es más barata la segunda.")),
]))
for h, k in [(5, '17.5'), (8, 28), (20, 70)]: ck(D('3.5') * h, k)
ck(D(42) / D('3.5'), 12); ck(D(30) / 4 * 7, '52.5'); ck(D('6.4') * 450 / 100, '28.8'); ck(D(4000) / D('6.4'), 625); ck(D(1500) / D('2.5'), 600); ck(D(2100) / 600, '3.5')
ck(Fr(320, 4) * 10, 800); ck(D('1.2') / 4 * 10, 3); ck(D('1.6') * 250, 400); ck(D('1.4') * 250, 350); ck(4 * D('3.5'), 14)
assert [4 * h for h in (1, 2, 3, 6)] == [4, 8, 12, 24] and [5 + 3 * h for h in (1, 2, 3, 6)] == [8, 11, 14, 23] and 4 * 5 == 5 + 3 * 5 and 4 * 6 > 5 + 3 * 6

# =====================================================================
# 3. Proporcionalitat inversa
S_.append((T("Magnituds inversament proporcionals", "Magnitudes inversamente proporcionales"), [
 (1, T(r"Indica si són directament proporcionals, inversament proporcionals o cap de les dues:", r"Indica si son directamente proporcionales, inversamente proporcionales o ninguna de las dos:")
     + tasks(2, [T(r"El nombre de pintors i els dies que tarden a pintar una casa.", r"El número de pintores y los días que tardan en pintar una casa."), T(r"Els litres d'aigua d'un dipòsit i el que pesa.", r"Los litros de agua de un depósito y lo que pesa."),
                 T(r"La velocitat d'un cotxe i el temps que tarda en un trajecte.", r"La velocidad de un coche y el tiempo que tarda en un trayecto."), T(r"El nombre de persones d'una família i la seua despesa en menjar.", r"El número de personas de una familia y su gasto en comida.")])
     + recorda(T(r"Són inversament proporcionals si el doble d'una correspon a la meitat de l'altra. El producte de les quantitats corresponents és constant.", r"Son inversamente proporcionales si el doble de una corresponde a la mitad de la otra. El producto de las cantidades correspondientes es constante.")),
     tasks(2, [r"\rest{Inversa}", r"\rest{Directa}", r"\rest{Inversa}", T(r"\rest{Cap de les dues} (augmenten juntes, però no exactament en la mateixa proporció)", r"\rest{Ninguna} (aumentan juntas, pero no exactamente en la misma proporción)")])),
 (1, T(r"Completa la taula de proporcionalitat inversa i calcula'n la constant:", r"Completa la tabla de proporcionalidad inversa y calcula su constante:") + '\\\\[4pt]' + ptab(['2', '3', '4', '', '12'], ['18', '', '', '6', ''], T('Aixetes', 'Grifos'), T('Hores', 'Horas')),
     ptab(['2', '3', '4', r'\rest{6}', '12'], ['18', r'\rest{12}', r'\rest{9}', '6', r'\rest{3}'], T('Aixetes', 'Grifos'), T('Hores', 'Horas')) + T(r'\quad Constant: $k=2\cdot18=\res{36}$.', r'\quad Constante: $k=2\cdot18=\res{36}$.')),
 (1, T(r"Tres màquines iguals fan una faena en 12 hores. Quant tardarien 4 màquines? Resol-ho per reducció a la unitat.", r"Tres máquinas iguales hacen un trabajo en 12 horas. ¿Cuánto tardarían 4 máquinas? Resuélvelo por reducción a la unidad."),
     T(r"Una sola màquina: $12\cdot3=36$ h. Quatre: $36:4=\res{9\ \text{h}}$.", r"Una sola máquina: $12\cdot3=36$ h. Cuatro: $36:4=\res{9\ \text{h}}$.")),
 (2, T(r"Un tren a 120 km/h tarda 3 h 30 min a fer un trajecte. Quant tardaria a 140 km/h?", r"Un tren a 120 km/h tarda 3 h 30 min en hacer un trayecto. ¿Cuánto tardaría a 140 km/h?"),
     r3('120', 'km/h', '3{,}5', 'h', '140', 'km/h') + T(r'\quad Inversa: $x=\frac{120\cdot3{,}5}{140}=\res{3\ \text{h}}$.', r'\quad Inversa: $x=\frac{120\cdot3{,}5}{140}=\res{3\ \text{h}}$.')),
 (2, T(r"Un ramader té pinso per a alimentar 40 vaques durant 30 dies. Si ven 10 vaques, quants dies li durarà el pinso? I si en compra 8 més (en lloc de vendre'n)?", r"Un ganadero tiene pienso para alimentar 40 vacas durante 30 días. Si vende 10 vacas, ¿cuántos días le durará el pienso? ¿Y si compra 8 más (en lugar de vender)?"),
     T(r"Constant: $40\cdot30=1200$. Amb 30 vaques: $1200:30=\res{40\ \text{dies}}$. Amb 48: $1200:48=\res{25\ \text{dies}}$.", r"Constante: $40\cdot30=1200$. Con 30 vacas: $1200:30=\res{40\ \text{días}}$. Con 48: $1200:48=\res{25\ \text{días}}$.")),
 (2, T(r"Per a omplir un dipòsit fan falta 45 cubs de 12 L. Quants cubs de 18 L farien falta? De quina capacitat haurien de ser els cubs per a omplir-lo amb 60 cubs?", r"Para llenar un depósito hacen falta 45 cubos de 12 L. ¿Cuántos cubos de 18 L harían falta? ¿De qué capacidad tendrían que ser los cubos para llenarlo con 60 cubos?"),
     T(r"El dipòsit té $45\cdot12=540$ L. $540:18=\res{30\ \text{cubs}}$; $\ 540:60=\res{9\ \text{L}}$.", r"El depósito tiene $45\cdot12=540$ L. $540:18=\res{30\ \text{cubos}}$; $\ 540:60=\res{9\ \text{L}}$.")),
 (3, T(r"Unes obres s'han de fer en 18 dies i hi treballen 10 obrers. Al cap de 6 dies, se'n van 2 obrers. Quants dies tardaran els que queden a acabar l'obra?", r"Unas obras se tienen que hacer en 18 días y trabajan 10 obreros. Al cabo de 6 días, se van 2 obreros. ¿Cuántos días tardarán los que quedan en acabar la obra?"),
     T(r"Falten 12 dies de faena per a 10 obrers. Amb 8 obrers (inversa): $x=\frac{10\cdot12}{8}=15$ dies més. En total: $6+15=\res{21\ \text{dies}}$.", r"Faltan 12 días de trabajo para 10 obreros. Con 8 obreros (inversa): $x=\frac{10\cdot12}{8}=15$ días más. En total: $6+15=\res{21\ \text{días}}$.")),
 (3, T(r"Decideix si cada problema és de proporcionalitat directa o inversa i resol-lo:", r"Decide si cada problema es de proporcionalidad directa o inversa y resuélvelo:")
     + tasks(1, [T(r"Amb rajoles de 30 cm de costat necessitem 24 files per a cobrir una paret. Quantes files farien falta amb rajoles de 20 cm?", r"Con azulejos de 30 cm de lado necesitamos 24 filas para cubrir una pared. ¿Cuántas filas harían falta con azulejos de 20 cm?"),
                 T(r"En 5 caixes caben 120 llibres. Quantes caixes iguals fan falta per a 312 llibres?", r"En 5 cajas caben 120 libros. ¿Cuántas cajas iguales hacen falta para 312 libros?"),
                 T(r"Un grup d'amics lloga una casa i, si són 6, cadascun paga 85 €. Quant pagaria cadascun si foren 10?", r"Un grupo de amigos alquila una casa y, si son 6, cada uno paga 85 €. ¿Cuánto pagaría cada uno si fueran 10?")]),
     tasks(1, [T(r"Inversa: $\frac{30\cdot24}{20}=\res{36\ \text{files}}$.", r"Inversa: $\frac{30\cdot24}{20}=\res{36\ \text{filas}}$."), T(r"Directa: $\frac{5\cdot312}{120}=\res{13\ \text{caixes}}$.", r"Directa: $\frac{5\cdot312}{120}=\res{13\ \text{cajas}}$."), T(r"Inversa: $\frac{6\cdot85}{10}=\res{51\ \text{€}}$.", r"Inversa: $\frac{6\cdot85}{10}=\res{51\ \text{€}}$.")])),
]))
for a, b in [(3, 12), (4, 9), (6, 6), (12, 3)]: ck(a * b, 36)
ck(36 // 4, 9); ck(D(120) * D('3.5') / 140, 3); ck(Fr(1200, 30), 40); ck(Fr(1200, 48), 25); ck(Fr(540, 18), 30); ck(Fr(540, 60), 9); ck(Fr(120, 8), 15)
ck(Fr(30 * 24, 20), 36); ck(Fr(5 * 312, 120), 13); ck(Fr(6 * 85, 10), 51)

# =====================================================================
# 4. Proporcionalitat composta
S_.append((T("Proporcionalitat composta", "Proporcionalidad compuesta"), [
 (1, T(r"Per a alimentar 6 gossos durant 10 dies calen 24 kg de pinso. Quants quilos calen per a 9 gossos durant 15 dies?", r"Para alimentar 6 perros durante 10 días hacen falta 24 kg de pienso. ¿Cuántos kilos hacen falta para 9 perros durante 15 días?")
     + recorda(T(r"Compara cada magnitud amb la incògnita, suposant que les altres no canvien. Si és directa, multiplica per $\frac{\text{nou}}{\text{antic}}$; si és inversa, per $\frac{\text{antic}}{\text{nou}}$.", r"Compara cada magnitud con la incógnita, suponiendo que las demás no cambian. Si es directa, multiplica por $\frac{\text{nuevo}}{\text{antiguo}}$; si es inversa, por $\frac{\text{antiguo}}{\text{nuevo}}$.")),
     T(r"D i D: $x=24\cdot\frac{9}{6}\cdot\frac{15}{10}=\res{54\ \text{kg}}$. (Un gos menja $24:6:10=0{,}4$ kg al dia.)", r"D y D: $x=24\cdot\frac{9}{6}\cdot\frac{15}{10}=\res{54\ \text{kg}}$. (Un perro come $24:6:10=0{,}4$ kg al día.)")),
 (1, T(r"4 aixetes iguals, obertes 5 hores, aboquen 6000 L. Quants litres abocaran 6 aixetes obertes 3 hores?", r"4 grifos iguales, abiertos 5 horas, vierten 6000 L. ¿Cuántos litros verterán 6 grifos abiertos 3 horas?"),
     T(r"Una aixeta en una hora: $6000:4:5=300$ L. Llavors: $300\cdot6\cdot3=\res{5400\ \text{L}}$.", r"Un grifo en una hora: $6000:4:5=300$ L. Entonces: $300\cdot6\cdot3=\res{5400\ \text{L}}$.")),
 (2, T(r"12 obrers, treballant 8 hores diàries, fan una obra en 20 dies. Quants dies tardaran 15 obrers treballant 8 hores diàries? I 16 obrers treballant 6 hores diàries?", r"12 obreros, trabajando 8 horas diarias, hacen una obra en 20 días. ¿Cuántos días tardarán 15 obreros trabajando 8 horas diarias? ¿Y 16 obreros trabajando 6 horas diarias?"),
     comp([T('Obrers', 'Obreros'), T('Hores/dia', 'Horas/día'), T('Dies', 'Días')], ['12', '8', '20'], ['16', '6', 'x']) + r'\\[3pt]'
     + T(r"Si només canvien els obrers: $20\cdot\frac{12}{15}=\res{16\ \text{dies}}$. Amb 16 obrers i 6 h (I i I): $20\cdot\frac{12}{16}\cdot\frac{8}{6}=\res{20\ \text{dies}}$.", r"Si solo cambian los obreros: $20\cdot\frac{12}{15}=\res{16\ \text{días}}$. Con 16 obreros y 6 h (I e I): $20\cdot\frac{12}{16}\cdot\frac{8}{6}=\res{20\ \text{días}}$.")),
 (2, T(r"Una família de 4 persones gasta 540 € en menjar en 30 dies. Quant gastarà una família de 6 persones en 20 dies?", r"Una familia de 4 personas gasta 540 € en comida en 30 días. ¿Cuánto gastará una familia de 6 personas en 20 días?"),
     T(r"D i D: $540\cdot\frac{6}{4}\cdot\frac{20}{30}=\res{540\ \text{€}}$. (Casualment, el mateix!)", r"D y D: $540\cdot\frac{6}{4}\cdot\frac{20}{30}=\res{540\ \text{€}}$. (¡Casualmente, lo mismo!)")),
 (2, T(r"Per a transportar 360 tones de terra, 5 camions fan 8 viatges cadascun. Quants viatges haurà de fer cada camió si en són 6 i han de transportar 540 tones?", r"Para transportar 360 toneladas de tierra, 5 camiones hacen 8 viajes cada uno. ¿Cuántos viajes tendrá que hacer cada camión si son 6 y tienen que transportar 540 toneladas?"),
     T(r"Més tones → més viatges (D); més camions → menys viatges cadascun (I): $8\cdot\frac{540}{360}\cdot\frac{5}{6}=\res{10\ \text{viatges}}$.", r"Más toneladas → más viajes (D); más camiones → menos viajes cada uno (I): $8\cdot\frac{540}{360}\cdot\frac{5}{6}=\res{10\ \text{viajes}}$.")),
 (3, T(r"En una fàbrica, 8 màquines treballant 9 hores diàries fan 3600 peces en 5 dies. Quants dies necessitaran 6 màquines treballant 10 hores diàries per a fer 4800 peces?", r"En una fábrica, 8 máquinas trabajando 9 horas diarias hacen 3600 piezas en 5 días. ¿Cuántos días necesitarán 6 máquinas trabajando 10 horas diarias para hacer 4800 piezas?"),
     comp([T('Màquines', 'Máquinas'), T('Hores/dia', 'Horas/día'), T('Peces', 'Piezas'), T('Dies', 'Días')], ['8', '9', '3600', '5'], ['6', '10', '4800', 'x']) + r'\\[3pt]'
     + T(r"I, I i D: $x=5\cdot\frac{8}{6}\cdot\frac{9}{10}\cdot\frac{4800}{3600}=\res{8\ \text{dies}}$. (Una màquina fa $3600:8:9:5=10$ peces per hora.)", r"I, I y D: $x=5\cdot\frac{8}{6}\cdot\frac{9}{10}\cdot\frac{4800}{3600}=\res{8\ \text{días}}$. (Una máquina hace $3600:8:9:5=10$ piezas por hora.)")),
 (3, T(r"Per a llaurar un camp de 18 ha, 3 tractors treballen 6 dies. Quants tractors calen per a llaurar un camp de 30 ha en 5 dies?", r"Para arar un campo de 18 ha, 3 tractores trabajan 6 días. ¿Cuántos tractores hacen falta para arar un campo de 30 ha en 5 días?"),
     T(r"Més hectàrees → més tractors (D); menys dies → més tractors (I): $3\cdot\frac{30}{18}\cdot\frac{6}{5}=\res{6\ \text{tractors}}$.", r"Más hectáreas → más tractores (D); menos días → más tractores (I): $3\cdot\frac{30}{18}\cdot\frac{6}{5}=\res{6\ \text{tractores}}$.")),
]))
ck(24 * Fr(9, 6) * Fr(15, 10), 54); ck(D(24) / 60, '0.4'); ck(Fr(6000, 20) * 18, 5400); ck(20 * Fr(12, 15), 16); ck(20 * Fr(12, 16) * Fr(8, 6), 20)
ck(540 * Fr(6, 4) * Fr(20, 30), 540); ck(8 * Fr(540, 360) * Fr(5, 6), 10); ck(5 * Fr(8, 6) * Fr(9, 10) * Fr(4800, 3600), 8); ck(Fr(3600, 8 * 9 * 5), 10); ck(3 * Fr(30, 18) * Fr(6, 5), 6)

# =====================================================================
# 5. Repartiments
S_.append((T("Repartiments proporcionals", "Repartos proporcionales"), [
 (1, T(r"Reparteix en parts directament proporcionals:", r"Reparte en partes directamente proporcionales:") + tasks(2, [T(r"840 a 3 i 4", r"840 a 3 y 4"), T(r"1200 a 2, 3 i 5", r"1200 a 2, 3 y 5")])
     + recorda(T(r"Directe: $k=\dfrac{N}{a+b+c}$ i cada part és $a\cdot k$, $b\cdot k$… Invers: es reparteix directament als inversos $\frac{1}{a},\frac{1}{b}\ldots$ (amb el m.c.m., als numeradors).", r"Directo: $k=\dfrac{N}{a+b+c}$ y cada parte es $a\cdot k$, $b\cdot k$… Inverso: se reparte directamente a los inversos $\frac{1}{a},\frac{1}{b}\ldots$ (con el m.c.m., a los numeradores).")),
     tasks(2, [T(r"$k=120$: \rest{360 i 480}", r"$k=120$: \rest{360 y 480}"), T(r"$k=120$: \rest{240, 360 i 600}", r"$k=120$: \rest{240, 360 y 600}")])),
 (1, T(r"Dos amics compren un dècim de loteria de 45 €: un hi posa 20 € i l'altre 25 €. Els toca un premi de 135 €. Com se l'han de repartir?", r"Dos amigos compran un décimo de lotería de 45 €: uno pone 20 € y el otro 25 €. Les toca un premio de 135 €. ¿Cómo se lo tienen que repartir?"),
     T(r"$k=\frac{135}{45}=3$: \rest{60 € i 75 €}.", r"$k=\frac{135}{45}=3$: \rest{60 € y 75 €}.")),
 (2, T(r"Tres socis han invertit 6000 €, 9000 € i 15 000 € en una empresa i han obtingut uns beneficis de 7500 €. Quant rep cadascun?", r"Tres socios han invertido 6000 €, 9000 € y 15 000 € en una empresa y han obtenido unos beneficios de 7500 €. ¿Cuánto recibe cada uno?"),
     T(r"Simplifiquem: 2, 3 i 5. $k=\frac{7500}{10}=750$: \rest{1500 €, 2250 € i 3750 €}.", r"Simplificamos: 2, 3 y 5. $k=\frac{7500}{10}=750$: \rest{1500 €, 2250 € y 3750 €}.")),
 (2, T(r"Reparteix en parts inversament proporcionals:", r"Reparte en partes inversamente proporcionales:") + tasks(2, [T(r"500 a 2 i 3", r"500 a 2 y 3"), T(r"1300 a 2, 3 i 4", r"1300 a 2, 3 y 4")]),
     tasks(2, [T(r"$\frac{1}{2},\frac{1}{3}\to3,2$; $k=100$: \rest{300 i 200}", r"$\frac{1}{2},\frac{1}{3}\to3,2$; $k=100$: \rest{300 y 200}"), T(r"$\frac{1}{2},\frac{1}{3},\frac{1}{4}\to6,4,3$; $k=100$: \rest{600, 400 i 300}", r"$\frac{1}{2},\frac{1}{3},\frac{1}{4}\to6,4,3$; $k=100$: \rest{600, 400 y 300}")])),
 (2, T(r"Una àvia reparteix 1170 € entre els seus tres néts de manera directament proporcional a les seues edats: 6, 9 i 11 anys. Quant rep cadascun? I si el repartiment fóra inversament proporcional a 2, 3 i 6?", r"Una abuela reparte 1170 € entre sus tres nietos de forma directamente proporcional a sus edades: 6, 9 y 11 años. ¿Cuánto recibe cada uno? ¿Y si el reparto fuera inversamente proporcional a 2, 3 y 6?"),
     T(r"$k=\frac{1170}{26}=45$: \rest{270 €, 405 € i 495 €}. Invers: $\frac{1}{2},\frac{1}{3},\frac{1}{6}\to3,2,1$; $k=195$: \rest{585 €, 390 € i 195 €}.", r"$k=\frac{1170}{26}=45$: \rest{270 €, 405 € y 495 €}. Inverso: $\frac{1}{2},\frac{1}{3},\frac{1}{6}\to3,2,1$; $k=195$: \rest{585 €, 390 € y 195 €}.")),
 (3, T(r"Un premi de 2800 € es reparteix entre tres atletes de manera inversament proporcional al lloc en què han arribat (1r, 2n i 3r). Quant rep cadascun?", r"Un premio de 2800 € se reparte entre tres atletas de forma inversamente proporcional al puesto en que han llegado (1.º, 2.º y 3.º). ¿Cuánto recibe cada uno?"),
     T(r"$\frac{1}{1},\frac{1}{2},\frac{1}{3}\to6,3,2$; $k=\frac{2800}{11}$: \rest{1527,27 €, 763,64 € i 509,09 €} (arrodonit).", r"$\frac{1}{1},\frac{1}{2},\frac{1}{3}\to6,3,2$; $k=\frac{2800}{11}$: \rest{1527,27 €, 763,64 € y 509,09 €} (redondeado).")),
 (3, T(r"Tres germans es reparteixen una quantitat de manera directament proporcional a 3, 5 i 7. Al segon li toquen 60 € més que al primer. Quina quantitat s'han repartit? Quant rep cadascun?", r"Tres hermanos se reparten una cantidad de forma directamente proporcional a 3, 5 y 7. Al segundo le tocan 60 € más que al primero. ¿Qué cantidad se han repartido? ¿Cuánto recibe cada uno?"),
     T(r"Entre el primer i el segon hi ha $5-3=2$ parts, que són 60 €: cada part val 30 €. Reben \rest{90 €, 150 € i 210 €}; en total, \rest{450 €}.", r"Entre el primero y el segundo hay $5-3=2$ partes, que son 60 €: cada parte vale 30 €. Reciben \rest{90 €, 150 € y 210 €}; en total, \rest{450 €}.")),
]))
ck(Fr(840, 7), 120); ck(Fr(1200, 10), 120); ck(Fr(135, 45), 3); ck(Fr(7500, 10), 750); ck(Fr(500, 5), 100); ck(Fr(1300, 13), 100)
ck(Fr(1170, 26), 45); ck(45 * 11, 495); ck(Fr(1170, 6), 195)
for w, v in [(6, '1527.27'), (3, '763.64'), (2, '509.09')]: ck(round(Fr(2800 * w, 11), 2), v)
ck(Fr(60, 2), 30); ck(15 * 30, 450)

# =====================================================================
# 6. Percentatges
S_.append((T("Percentatges: concepte i càlcul", "Porcentajes: concepto y cálculo"), [
 (1, T(r"Completa la taula:", r"Completa la tabla:") + '\\\\[4pt]' + r'\begin{tabular}{l|cccccc}' + T('Percentatge', 'Porcentaje') + r' & 30\,\% & & & 2\,\% & & 150\,\% \\ \hline ' + T('Fracció irreductible', 'Fracción irreducible') + r' & & $\frac{3}{4}$ & & & $\frac{1}{8}$ & \\ ' + 'Decimal' + r' & & & 0,05 & & & \end{tabular}',
     r'\begin{tabular}{l|cccccc}' + T('Percentatge', 'Porcentaje') + r' & 30\,\% & \rest{75\,\%} & \rest{5\,\%} & 2\,\% & \rest{12{,}5\,\%} & 150\,\% \\ \hline ' + T('Fracció', 'Fracción') + r' & $\res{\frac{3}{10}}$ & $\frac{3}{4}$ & $\res{\frac{1}{20}}$ & $\res{\frac{1}{50}}$ & $\frac{1}{8}$ & $\res{\frac{3}{2}}$ \\ Decimal & \rest{0,3} & \rest{0,75} & 0,05 & \rest{0,02} & \rest{0,125} & \rest{1,5} \end{tabular}'),
 (1, T(r"Calcula mentalment:", r"Calcula mentalmente:") + tasks(4, [r'10\,\% de 480', r'50\,\% de 76', r'25\,\% de 360', r'5\,\% de 240', r'20\,\% de 45', r'1\,\% de 3500', r'15\,\% de 60', r'75\,\% de 80'])
     + recorda(T(r"El 10 \% és dividir entre 10; el 5 \%, la meitat del 10 \%; el 50 \%, la meitat; el 25 \%, la quarta part; el 20 \%, la cinquena part.", r"El 10 \% es dividir entre 10; el 5 \%, la mitad del 10 \%; el 50 \%, la mitad; el 25 \%, la cuarta parte; el 20 \%, la quinta parte.")),
     tasks(4, [r'\res{48}', r'\res{38}', r'\res{90}', r'\res{12}', r'\res{9}', r'\res{35}', r'\res{9}', r'\res{60}'])),
 (1, T(r"Calcula:", r"Calcula:") + tasks(3, [r'12\,\% de 350', r'35\,\% de 84', r'4\,\% de 1250', r'7{,}5\,\% de 240', r'0{,}5\,\% de 6000', r'120\,\% de 65']),
     tasks(3, [r'$350\cdot0{,}12=\res{42}$', r'$84\cdot0{,}35=\res{29{,}4}$', r'$1250\cdot0{,}04=\res{50}$', r'$240\cdot0{,}075=\res{18}$', r'$6000\cdot0{,}005=\res{30}$', r'$65\cdot1{,}2=\res{78}$'])),
 (2, T(r"En un institut de 850 alumnes, el 46 \% són xics, el 18 \% va a l'escola de música i el 6 \% és d'altres països. Quants alumnes hi ha en cada cas?", r"En un instituto de 850 alumnos, el 46 \% son chicos, el 18 \% va a la escuela de música y el 6 \% es de otros países. ¿Cuántos alumnos hay en cada caso?"),
     T(r"$850\cdot0{,}46=\res{391}$ xics; $\ 850\cdot0{,}18=\res{153}$; $\ 850\cdot0{,}06=\res{51}$.", r"$850\cdot0{,}46=\res{391}$ chicos; $\ 850\cdot0{,}18=\res{153}$; $\ 850\cdot0{,}06=\res{51}$.")),
 (2, T(r"El cos humà és aproximadament un 65 \% aigua. Quants quilos d'aigua té una persona de 58 kg? I una de 72 kg?", r"El cuerpo humano es aproximadamente un 65 \% agua. ¿Cuántos kilos de agua tiene una persona de 58 kg? ¿Y una de 72 kg?"),
     r"$58\cdot0{,}65=\res{37{,}7\ \text{kg}}$; $\ 72\cdot0{,}65=\res{46{,}8\ \text{kg}}$."),
 (3, T(r"D'un dipòsit de 2000 L, el dilluns se'n gasta el 30 \% i el dimarts, el 25 \% del que quedava. Quants litres queden? Quin percentatge del dipòsit s'ha gastat?", r"De un depósito de 2000 L, el lunes se gasta el 30 \% y el martes, el 25 \% de lo que quedaba. ¿Cuántos litros quedan? ¿Qué porcentaje del depósito se ha gastado?"),
     T(r"Dilluns: $2000\cdot0{,}3=600$; queden 1400. Dimarts: $1400\cdot0{,}25=350$; queden \rest{1050 L}. S'ha gastat $\frac{950}{2000}=\res{47{,}5\,\%}$ (no el 55 \%!).", r"Lunes: $2000\cdot0{,}3=600$; quedan 1400. Martes: $1400\cdot0{,}25=350$; quedan \rest{1050 L}. Se ha gastado $\frac{950}{2000}=\res{47{,}5\,\%}$ (¡no el 55 \%!).")),
]))
for p, f, d in [(30, Fr(3, 10), '0.3'), (75, Fr(3, 4), '0.75'), (5, Fr(1, 20), '0.05'), (2, Fr(1, 50), '0.02'), (D('12.5'), Fr(1, 8), '0.125'), (150, Fr(3, 2), '1.5')]: ck(Fr(str(p)) / 100, f); ck(f, d)
for p, n, r in [(10, 480, 48), (50, 76, 38), (25, 360, 90), (5, 240, 12), (20, 45, 9), (1, 3500, 35), (15, 60, 9), (75, 80, 60), (12, 350, 42), (35, 84, '29.4'), (4, 1250, 50), ('7.5', 240, 18), ('0.5', 6000, 30), (120, 65, 78), (46, 850, 391), (18, 850, 153), (6, 850, 51), (65, 58, '37.7'), (65, 72, '46.8')]:
    ck(D(str(p)) * n / 100, r)
ck(D(950) / 2000, '0.475')

# =====================================================================
# 7. Quin percentatge representa? Càlcul del total
S_.append((T("Quin percentatge representa? Càlcul del total", "¿Qué porcentaje representa? Cálculo del total"), [
 (1, T(r"Quin percentatge representa…", r"¿Qué porcentaje representa…") + tasks(2, [T(r"12 de 50?", r"12 de 50?"), T(r"27 de 36?", r"27 de 36?"), T(r"45 de 300?", r"45 de 300?"), T(r"90 de 72?", r"90 de 72?")])
     + recorda(T(r"$p\,\%=\frac{\text{part}}{\text{total}}\cdot100$. \quad Total $=$ part $:\ \frac{p}{100}$.", r"$p\,\%=\frac{\text{parte}}{\text{total}}\cdot100$. \quad Total $=$ parte $:\ \frac{p}{100}$.")),
     tasks(4, [r'$\frac{12}{50}=\res{24\,\%}$', r'$\frac{27}{36}=\res{75\,\%}$', r'$\frac{45}{300}=\res{15\,\%}$', r'$\frac{90}{72}=\res{125\,\%}$'])),
 (1, T(r"Calcula la quantitat total si:", r"Calcula la cantidad total si:") + tasks(2, [T(r"el 20 \% és 36", r"el 20 \% es 36"), T(r"el 15 \% és 63", r"el 15 \% es 63"), T(r"el 75 \% és 240", r"el 75 \% es 240"), T(r"el 4 \% és 18", r"el 4 \% es 18")]),
     tasks(4, [r'$36:0{,}2=\res{180}$', r'$63:0{,}15=\res{420}$', r'$240:0{,}75=\res{320}$', r'$18:0{,}04=\res{450}$'])),
 (2, T(r"En una classe de 28 alumnes n'han aprovat 21. Quin percentatge ha aprovat? I quin ha suspés?", r"En una clase de 28 alumnos han aprobado 21. ¿Qué porcentaje ha aprobado? ¿Y cuál ha suspendido?"),
     T(r"$\frac{21}{28}=0{,}75$: \rest{75 \% aprovats} i \rest{25 \% suspesos}.", r"$\frac{21}{28}=0{,}75$: \rest{75 \% aprobados} y \rest{25 \% suspensos}.")),
 (2, T(r"En una votació, una proposta ha obtingut 182 vots, que són el 35 \% dels vots emesos. Quantes persones han votat?", r"En una votación, una propuesta ha obtenido 182 votos, que son el 35 \% de los votos emitidos. ¿Cuántas personas han votado?"),
     T(r"$182:0{,}35=\res{520\ \text{persones}}$.", r"$182:0{,}35=\res{520\ \text{personas}}$.")),
 (2, T(r"Una jugadora de bàsquet ha fet 15 tirs de 3 punts i n'ha encertat 6. Un company n'ha fet 20 i n'ha encertat 7. Qui té millor percentatge d'encert?", r"Una jugadora de baloncesto ha hecho 15 tiros de 3 puntos y ha acertado 6. Un compañero ha hecho 20 y ha acertado 7. ¿Quién tiene mejor porcentaje de acierto?"),
     T(r"Ella: $\frac{6}{15}=40\,\%$; ell: $\frac{7}{20}=35\,\%$. \rest{Ella}, tot i que ha encertat menys tirs.", r"Ella: $\frac{6}{15}=40\,\%$; él: $\frac{7}{20}=35\,\%$. \rest{Ella}, aunque ha acertado menos tiros.")),
 (3, T(r"D'una pizza n'hem menjat el 62,5 \% i en queden 3 porcions iguals. En quantes porcions estava tallada? Quin percentatge representa cada porció?", r"De una pizza nos hemos comido el 62,5 \% y quedan 3 porciones iguales. ¿En cuántas porciones estaba cortada? ¿Qué porcentaje representa cada porción?"),
     T(r"Les 3 porcions són el $100-62{,}5=37{,}5\,\%$: total $=3:0{,}375=\res{8\ \text{porcions}}$. Cada porció: $\frac{1}{8}=\res{12{,}5\,\%}$.", r"Las 3 porciones son el $100-62{,}5=37{,}5\,\%$: total $=3:0{,}375=\res{8\ \text{porciones}}$. Cada porción: $\frac{1}{8}=\res{12{,}5\,\%}$.")),
 (3, T(r"Una botiga ha venut aquest mes 252 bicicletes, que són el 120 \% de les que va vendre el mes passat. Quantes en va vendre el mes passat? Quantes més n'ha venut aquest mes?", r"Una tienda ha vendido este mes 252 bicicletas, que son el 120 \% de las que vendió el mes pasado. ¿Cuántas vendió el mes pasado? ¿Cuántas más ha vendido este mes?"),
     T(r"$252:1{,}2=\res{210}$ bicicletes; aquest mes n'ha venut \rest{42 més}.", r"$252:1{,}2=\res{210}$ bicicletas; este mes ha vendido \rest{42 más}.")),
]))
ck(Fr(12, 50), Fr(24, 100)); ck(Fr(27, 36), Fr(75, 100)); ck(Fr(45, 300), Fr(15, 100)); ck(Fr(90, 72), Fr(125, 100))
ck(D(36) / D('0.2'), 180); ck(D(63) / D('0.15'), 420); ck(D(240) / D('0.75'), 320); ck(D(18) / D('0.04'), 450); ck(Fr(21, 28), Fr(3, 4)); ck(D(182) / D('0.35'), 520)
ck(Fr(6, 15), Fr(40, 100)); ck(Fr(7, 20), Fr(35, 100)); ck(D(3) / D('0.375'), 8); ck(D(252) / D('1.2'), 210)

# =====================================================================
# 8. Augments i disminucions percentuals
S_.append((T("Augments i disminucions percentuals", "Aumentos y disminuciones porcentuales"), [
 (1, T(r"Escriu l'índex de variació de cada cas:", r"Escribe el índice de variación de cada caso:") + tasks(3, [T(r"augment del 25 \%", r"aumento del 25 \%"), T(r"disminució del 10 \%", r"disminución del 10 \%"), T(r"augment del 4 \%", r"aumento del 4 \%"), T(r"rebaixa del 35 \%", r"rebaja del 35 \%"), T(r"IVA del 21 \%", r"IVA del 21 \%"), T(r"augment del 100 \%", r"aumento del 100 \%")])
     + recorda(T(r"Augment del $p\,\%$: índex $1+\frac{p}{100}$. Disminució del $p\,\%$: índex $1-\frac{p}{100}$. \ Final $=$ inicial $\cdot$ índex; \ inicial $=$ final $:$ índex.", r"Aumento del $p\,\%$: índice $1+\frac{p}{100}$. Disminución del $p\,\%$: índice $1-\frac{p}{100}$. \ Final $=$ inicial $\cdot$ índice; \ inicial $=$ final $:$ índice.")),
     tasks(6, [r'\rest{1,25}', r'\rest{0,9}', r'\rest{1,04}', r'\rest{0,65}', r'\rest{1,21}', r'\rest{2}'])),
 (1, T(r"Calcula el preu final:", r"Calcula el precio final:") + tasks(2, [T(r"Una jaqueta de 90 € rebaixada un 30 \%.", r"Una chaqueta de 90 € rebajada un 30 \%."), T(r"Un llibre de 22 € amb un 4 \% d'IVA.", r"Un libro de 22 € con un 4 \% de IVA."), T(r"Un sou de 1450 € que puja un 3 \%.", r"Un sueldo de 1450 € que sube un 3 \%."), T(r"Una tauleta de 340 € amb un 15 \% de descompte.", r"Una tableta de 340 € con un 15 \% de descuento.")]),
     tasks(2, [r'$90\cdot0{,}7=\res{63\ \text{€}}$', r'$22\cdot1{,}04=\res{22{,}88\ \text{€}}$', r'$1450\cdot1{,}03=\res{1493{,}50\ \text{€}}$', r'$340\cdot0{,}85=\res{289\ \text{€}}$'])),
 (2, T(r"Un cotxe valia 18 500 € i ha baixat un 12 \%. Quant val ara? Quants euros ha baixat?", r"Un coche valía 18 500 € y ha bajado un 12 \%. ¿Cuánto vale ahora? ¿Cuántos euros ha bajado?"),
     T(r"$18\,500\cdot0{,}88=\res{16\,280\ \text{€}}$; ha baixat \rest{2220 €}.", r"$18\,500\cdot0{,}88=\res{16\,280\ \text{€}}$; ha bajado \rest{2220 €}.")),
 (2, T(r"Calcula la quantitat inicial:", r"Calcula la cantidad inicial:") + tasks(1, [T(r"Després d'una rebaixa del 20 \%, unes botes costen 68 €.", r"Después de una rebaja del 20 \%, unas botas cuestan 68 €."), T(r"Amb l'IVA del 21 \%, una factura és de 157,30 €.", r"Con el IVA del 21 \%, una factura es de 157,30 €."), T(r"Després d'augmentar un 6 \%, un poble té 3180 habitants.", r"Después de aumentar un 6 \%, un pueblo tiene 3180 habitantes.")]),
     tasks(3, [r'$68:0{,}8=\res{85\ \text{€}}$', r'$157{,}30:1{,}21=\res{130\ \text{€}}$', r'$3180:1{,}06=\res{3000}$'])),
 (2, T(r"Calcula el percentatge de variació:", r"Calcula el porcentaje de variación:") + tasks(1, [T(r"Una samarreta passa de 25 € a 20 €.", r"Una camiseta pasa de 25 € a 20 €."), T(r"Una ciutat passa de 40 000 a 43 000 habitants.", r"Una ciudad pasa de 40 000 a 43 000 habitantes."), T(r"El preu de l'oli passa de 6,40 € a 8 € el litre.", r"El precio del aceite pasa de 6,40 € a 8 € el litro.")]),
     tasks(3, [r'$\frac{20}{25}=0{,}8$: \rest{$-20\,\%$}', r'$\frac{43\,000}{40\,000}=1{,}075$: \rest{$+7{,}5\,\%$}', r'$\frac{8}{6{,}4}=1{,}25$: \rest{$+25\,\%$}'])),
 (3, T(r"El preu d'una consola de 400 € puja un 10 \% i, després, baixa un 10 \%. Quant val al final? Quina és la variació percentual total?", r"El precio de una consola de 400 € sube un 10 \% y, después, baja un 10 \%. ¿Cuánto vale al final? ¿Cuál es la variación porcentual total?"),
     T(r"$400\cdot1{,}1\cdot0{,}9=400\cdot0{,}99=\res{396\ \text{€}}$. Índex total $0{,}99$: ha baixat \rest{un 1 \%}.", r"$400\cdot1{,}1\cdot0{,}9=400\cdot0{,}99=\res{396\ \text{€}}$. Índice total $0{,}99$: ha bajado \rest{un 1 \%}.")),
 (3, T(r"En unes rebaixes fan un 40 \% de descompte i, a l'hora de pagar, un 10 \% més sobre el preu rebaixat. a) És el mateix que un 50 \% de descompte? b) Si hem pagat 37,80 €, quant costava abans?", r"En unas rebajas hacen un 40 \% de descuento y, a la hora de pagar, un 10 \% más sobre el precio rebajado. a) ¿Es lo mismo que un 50 \% de descuento? b) Si hemos pagado 37,80 €, ¿cuánto costaba antes?"),
     T(r"a) No: $0{,}6\cdot0{,}9=0{,}54$, és un descompte del \rest{46 \%}. b) $37{,}80:0{,}54=\res{70\ \text{€}}$.", r"a) No: $0{,}6\cdot0{,}9=0{,}54$, es un descuento del \rest{46 \%}. b) $37{,}80:0{,}54=\res{70\ \text{€}}$.")),
 (3, T(r"Un comerciant compra una bicicleta per 250 €, la posa a la venda guanyant-hi un 40 \% i, com que no la ven, després la rebaixa un 20 \%. a) A quin preu la ven finalment? b) Quin percentatge guanya respecte del preu de compra?", r"Un comerciante compra una bicicleta por 250 €, la pone a la venta ganando un 40 \% y, como no la vende, después la rebaja un 20 \%. a) ¿A qué precio la vende finalmente? b) ¿Qué porcentaje gana respecto del precio de compra?"),
     T(r"a) $250\cdot1{,}4\cdot0{,}8=250\cdot1{,}12=\res{280\ \text{€}}$. b) Índex $1{,}12$: guanya \rest{un 12 \%}.", r"a) $250\cdot1{,}4\cdot0{,}8=250\cdot1{,}12=\res{280\ \text{€}}$. b) Índice $1{,}12$: gana \rest{un 12 \%}.")),
]))
ck(90 * D('0.7'), 63); ck(22 * D('1.04'), '22.88'); ck(1450 * D('1.03'), '1493.5'); ck(340 * D('0.85'), 289); ck(18500 * D('0.88'), 16280); ck(18500 - 16280, 2220)
ck(D(68) / D('0.8'), 85); ck(D('157.30') / D('1.21'), 130); ck(D(3180) / D('1.06'), 3000); ck(D(20) / 25, '0.8'); ck(D(43000) / 40000, '1.075'); ck(D(8) / D('6.4'), '1.25')
ck(400 * D('1.1') * D('0.9'), 396); ck(D('0.6') * D('0.9'), '0.54'); ck(D('37.80') / D('0.54'), 70); ck(250 * D('1.4') * D('0.8'), 280)

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = T("raons, proporcions, proporcionalitat directa, proporcionalitat inversa, regla de tres, proporcionalitat composta, repartiments proporcionals, percentatges, augments i disminucions percentuals",
       'razones, proporciones, proporcionalidad directa, proporcionalidad inversa, regla de tres, proporcionalidad compuesta, repartos proporcionales, porcentajes, aumentos y disminuciones porcentuales')
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: 'pdfkeywords={%s}' % KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 2n ESO}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre += r'''\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}
\usepackage{pifont}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''
if ES: pre = pre.replace(r'\textbf{Recorda:}', r'\textbf{Recuerda:}')
TIT = T('Proporcionalitat i percentatges', 'Proporcionalidad y porcentajes')

def build(sol_):
    if ES:
        import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
        from castella import preambul, assignatura
        t = 'Soluciones de la ficha' if sol_ else 'Ficha de ejercicios'
        p = preambul(pre, pdftitle='%s de la unidad 6: %s' % (t, TIT), capcalera='%s · Unidad 6: %s' % (t, TIT), pdfkeywords=KW, curs='2eso')
        cap = assignatura('2eso') + '{' + ('Soluciones de la ficha · Unidad 6' if sol_ else 'Ficha de ejercicios · Unidad 6') + '}{' + TIT + '}'
    else:
        t = 'Solucions de la fitxa' if sol_ else "Fitxa d'exercicis"
        p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}", "pdftitle={%s de la unitat 6: %s. 2n d'ESO}" % (t, TIT))
        p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 6: %s · 2n d'ESO" % (t, TIT))
        assert "2n d'ESO" in p and 'Unitat 6' in p and 'unitat 6' in p
        cap = r'\capcalera{Matemàtiques}{2n ESO}{' + ('Solucions de la fitxa · Unitat 6' if sol_ else "Fitxa d'exercicis · Unitat 6") + '}{' + TIT + '}'
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol_ else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append('\n\\def\\fmneed{14}\n\\input{../comu/fentmates.tex}\n\\fmcurs{2eso}\n\n\\begin{document}\n\\thispagestyle{primera}\n\n' + cap + '\n')
    if not sol_:
        out.append(T('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n',
                     '\\vspace{10pt}\nNombre y apellidos: \\rule{6.6cm}{0.4pt}\\hfill Grupo: \\rule{1.6cm}{0.4pt}\\hfill Fecha: \\rule{2.2cm}{0.4pt}\n'))
    intro = (T(r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat: hi trobaràs calculadores de regla de tres, proporcionalitat composta, repartiments i percentatges que ho resolen pas a pas.",
               r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad: encontrarás calculadoras de regla de tres, proporcionalidad compuesta, repartos y porcentajes que lo resuelven paso a paso.") if sol_ else
             T(r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Abans de calcular, decideix si la relació és directa o inversa, i comprova al final que el resultat té sentit. Les seccions segueixen l'ordre dels apunts de la unitat (6.1--6.8).",
               r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Antes de calcular, decide si la relación es directa o inversa, y comprueba al final que el resultado tiene sentido. Las secciones siguen el orden de los apuntes de la unidad (6.1--6.8)."))
    out.append('\\vspace{8pt}\n\n\\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]\n\\small ' + intro + '\n\\end{tcolorbox}\n')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            out.append('\\ex{%d} %s\n\n' % (st, s if sol_ else q))
    if not sol_:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ' + T("Ànim! Comprova els teus resultats amb les eines interactives dels apunts de la unitat.", "¡Ánimo! Comprueba tus resultados con las herramientas interactivas de los apuntes de la unidad.") + '\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't6-fitxa-%s%s.tex' % ('solucions' if sol_ else 'exercicis', '-es' if ES else '')
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(x[1]) for x in S_), T('exercicis', 'ejercicios'))
