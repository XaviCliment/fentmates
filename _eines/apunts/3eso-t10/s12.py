# 10.1 Raons i proporcions entre segments · 10.2 El teorema de Tales
from comu import *
from fig10 import *

def segrow(pairs, W=260):
    """segments horitzontals un davall de l'altre: [(longitud, nom, etiqueta)]"""
    it, y = [], 0
    for ln, nm, lb in pairs:
        it += [('seg', (0, y), (ln, y), 'hl'), ('dot', (0, y)), ('dot', (ln, y)), ('txt', (0, y), nm, {'dx': -8, 'a': 'end'}), ('txt', (ln / 2, y), lb, {'dy': -7})]
        y -= 1.3
    return G(it, W=W, pad=30)

# =====================================================================
# 10.1 Raons i proporcions entre segments
# =====================================================================
s1 = box('def', L('Raó de dos segments', 'Razón de dos segmentos', 'Ratio of two segments'),
  P(r"La <strong>raó</strong> de dos segments és el quocient de les seues longituds, mesurades amb la <strong>mateixa unitat</strong>. Si \(\overline{AB}=6\) cm i \(\overline{CD}=4\) cm,",
    r"La <strong>razón</strong> de dos segmentos es el cociente de sus longitudes, medidas con la <strong>misma unidad</strong>. Si \(\overline{AB}=6\) cm y \(\overline{CD}=4\) cm,",
    r"The <strong>ratio</strong> of two segments is the quotient of their lengths, measured in the <strong>same unit</strong>. If \(\overline{AB}=6\) cm and \(\overline{CD}=4\) cm,")
  + D(r"\frac{\overline{AB}}{\overline{CD}}=\frac{6}{4}=\frac32=1{,}5")
  + P(r"Vol dir que \(AB\) és una vegada i mitja \(CD\). La raó no té unitats i no depén de la unitat triada: en mil·límetres, \(\frac{60}{40}=1{,}5\) també.",
      r"Quiere decir que \(AB\) es una vez y media \(CD\). La razón no tiene unidades y no depende de la unidad elegida: en milímetros, \(\frac{60}{40}=1{,}5\) también.",
      r"It means that \(AB\) is one and a half times \(CD\). A ratio has no units and doesn't depend on the unit chosen: in millimetres, \(\frac{60}{40}=1.5\) too.")
  + figs(segrow([(6, 'AB', '6 cm'), (4, 'CD', '4 cm')])))
ck(R(6, 4), 1.5)
s1 += box('def', L('Segments proporcionals', 'Segmentos proporcionales', 'Proportional segments'),
  P(r"Quatre segments \(a,\ b,\ c,\ d\) són <strong>proporcionals</strong> si la raó dels dos primers és igual que la raó dels dos últims. Aquesta igualtat de raons és una <strong>proporció</strong>:",
    r"Cuatro segmentos \(a,\ b,\ c,\ d\) son <strong>proporcionales</strong> si la razón de los dos primeros es igual a la razón de los dos últimos. Esta igualdad de razones es una <strong>proporción</strong>:",
    r"Four segments \(a,\ b,\ c,\ d\) are <strong>proportional</strong> if the ratio of the first two equals the ratio of the last two. This equality of ratios is a <strong>proportion</strong>:")
  + D(r"\frac ab=\frac cd")
  + P(r"<strong>Propietat fonamental:</strong> en tota proporció, el producte dels extrems és igual al producte dels mitjans:",
      r"<strong>Propiedad fundamental:</strong> en toda proporción, el producto de los extremos es igual al producto de los medios:",
      r"<strong>Key property:</strong> in every proportion, the product of the extremes equals the product of the means:")
  + D(r"\frac ab=\frac cd\ \Longleftrightarrow\ a\cdot d=b\cdot c")
  + P(r"Exemple: els segments de 3, 5, 6 i 10 cm són proporcionals, perquè \(\frac35=\frac{6}{10}=0{,}6\) (o bé \(3\cdot10=5\cdot6=30\)). Els de 2, 3, 4 i 5 cm no ho són: \(2\cdot5=10\neq3\cdot4=12\).",
      r"Ejemplo: los segmentos de 3, 5, 6 y 10 cm son proporcionales, porque \(\frac35=\frac{6}{10}=0{,}6\) (o bien \(3\cdot10=5\cdot6=30\)). Los de 2, 3, 4 y 5 cm no lo son: \(2\cdot5=10\neq3\cdot4=12\).",
      r"Example: segments of 3, 5, 6 and 10 cm are proportional, because \(\frac35=\frac{6}{10}=0.6\) (or \(3\cdot10=5\cdot6=30\)). Those of 2, 3, 4 and 5 cm aren't: \(2\cdot5=10\neq3\cdot4=12\)."))
assert 3 * 10 == 5 * 6 and 2 * 5 != 3 * 4
s1 += box('prop', L('El quart proporcional', 'El cuarto proporcional', 'The fourth proportional'),
  P(r"Si coneixem tres segments \(a,\ b,\ c\), el <strong>quart proporcional</strong> és el segment \(x\) que compleix \(\frac ab=\frac cx\). Amb la propietat fonamental l'aïllem:",
    r"Si conocemos tres segmentos \(a,\ b,\ c\), el <strong>cuarto proporcional</strong> es el segmento \(x\) que cumple \(\frac ab=\frac cx\). Con la propiedad fundamental lo despejamos:",
    r"If we know three segments \(a,\ b,\ c\), the <strong>fourth proportional</strong> is the segment \(x\) with \(\frac ab=\frac cx\). The key property lets us solve for it:")
  + D(r"\frac ab=\frac cx\ \Rightarrow\ a\cdot x=b\cdot c\ \Rightarrow\ x=\frac{b\cdot c}{a}")
  + D(r"\frac46=\frac{10}{x}\ \Rightarrow\ x=\frac{6\cdot10}{4}=15")
  + note(r"La incògnita pot estar en qualsevol lloc de la proporció. Fes sempre el mateix: <strong>multiplica en creu</strong> i aïlla la \(x\).",
         r"La incógnita puede estar en cualquier lugar de la proporción. Haz siempre lo mismo: <strong>multiplica en cruz</strong> y despeja la \(x\).",
         r"The unknown can be anywhere in the proportion. Always do the same: <strong>cross-multiply</strong> and solve for \(x\).")
  + widget('w-quart', '🧮', L('Calculadora de proporcions', 'Calculadora de proporciones', 'Proportion calculator'),
           ['<div class="wrow">' + tin('a', 'a =', '4') + tin('b', 'b =', '6') + tin('c', 'c =', '10') + tin('d', 'd =', '') + '</div>',
            '<p class="hint-s">' + L(r"Proporció a/b = c/d. Escriu tres valors i deixa en blanc el que vols calcular.", r"Proporción a/b = c/d. Escribe tres valores y deja en blanco el que quieres calcular.", r"Proportion a/b = c/d. Type three values and leave blank the one you want to find.") + '</p>',
            quick([('4|6|10|', '4/6 = 10/x'), ('3|5||12', '3/5 = x/12'), ('|8|6|16', 'x/8 = 6/16'), ('2,5|4|6|', '2,5/4 = 6/x'), ('3|5|6|10', '3/5 = 6/10 ?')])],
           out='<div class="hsteps"></div><div class="gout"></div>')
  + drill('quart', 'Entrena: calcula el valor que falta', 'Entrena: calcula el valor que falta', 'Train: find the missing value'))
ck(R(6 * 10, 4), 15)
x_ = sp.Symbol('x')
s1 += levels(
 [prob(L(r"Són proporcionals els segments \(a=4\) cm, \(b=10\) cm, \(c=6\) cm i \(d=15\) cm? I els segments de 2, 7, 4 i 15 cm?", r"¿Son proporcionales los segmentos \(a=4\) cm, \(b=10\) cm, \(c=6\) cm y \(d=15\) cm? ¿Y los segmentos de 2, 7, 4 y 15 cm?", r"Are the segments \(a=4\) cm, \(b=10\) cm, \(c=6\) cm and \(d=15\) cm proportional? What about 2, 7, 4 and 15 cm?"),
       D(r"\frac4{10}=0{,}4=\frac6{15}\quad(4\cdot15=10\cdot6=60)\ \Rightarrow\ \boxed{\text{%s}}" % Lt('sí', 'sí', 'yes')),
       D(r"2\cdot15=30\neq7\cdot4=28\ \Rightarrow\ \boxed{\text{%s}}" % Lt('no', 'no', 'no'))),
  prob(L(r"Calcula el quart proporcional dels segments de 5, 8 i 15 cm.", r"Calcula el cuarto proporcional de los segmentos de 5, 8 y 15 cm.", r"Find the fourth proportional of the segments 5, 8 and 15 cm."),
       D(r"\frac58=\frac{15}{x}\ \Rightarrow\ x=\frac{8\cdot15}{5}=\boxed{24\ \text{cm}}"))],
 [prob(L(r"Calcula la raó entre els segments \(\overline{AB}=0{,}6\) m i \(\overline{CD}=40\) cm. Quant mesura \(\overline{GH}\) si \(\frac{\overline{AB}}{\overline{CD}}=\frac{\overline{EF}}{\overline{GH}}\) i \(\overline{EF}=9\) cm?", r"Calcula la razón entre los segmentos \(\overline{AB}=0{,}6\) m y \(\overline{CD}=40\) cm. ¿Cuánto mide \(\overline{GH}\) si \(\frac{\overline{AB}}{\overline{CD}}=\frac{\overline{EF}}{\overline{GH}}\) y \(\overline{EF}=9\) cm?", r"Find the ratio of the segments \(\overline{AB}=0.6\) m and \(\overline{CD}=40\) cm. How long is \(\overline{GH}\) if \(\frac{\overline{AB}}{\overline{CD}}=\frac{\overline{EF}}{\overline{GH}}\) and \(\overline{EF}=9\) cm?"),
       P(r"Primer, la mateixa unitat: \(0{,}6\) m \(=60\) cm.", r"Primero, la misma unidad: \(0{,}6\) m \(=60\) cm.", r"First, the same unit: \(0.6\) m \(=60\) cm."),
       D(r"\frac{60}{40}=\frac32=1{,}5"),
       D(r"\frac{3}{2}=\frac{9}{\overline{GH}}\ \Rightarrow\ \overline{GH}=\frac{2\cdot9}{3}=\boxed{6\ \text{cm}}"))],
 [prob(L(r"El <strong>mitjà proporcional</strong> de dos segments \(a\) i \(b\) és el segment \(x\) que compleix \(\frac ax=\frac xb\). Calcula el mitjà proporcional de 4 cm i 9 cm.", r"El <strong>medio proporcional</strong> de dos segmentos \(a\) y \(b\) es el segmento \(x\) que cumple \(\frac ax=\frac xb\). Calcula el medio proporcional de 4 cm y 9 cm.", r"The <strong>mean proportional</strong> of two segments \(a\) and \(b\) is the segment \(x\) with \(\frac ax=\frac xb\). Find the mean proportional of 4 cm and 9 cm."),
       D(r"\frac4x=\frac x9\ \Rightarrow\ x\cdot x=4\cdot9\ \Rightarrow\ x^2=36\ \Rightarrow\ x=\boxed{6\ \text{cm}}"),
       P(r"(La solució negativa no té sentit per a una longitud.) Comprovació: \(\frac46=\frac69=\frac23\ \checkmark\)", r"(La solución negativa no tiene sentido para una longitud.) Comprobación: \(\frac46=\frac69=\frac23\ \checkmark\)", r"(The negative solution makes no sense for a length.) Check: \(\frac46=\frac69=\frac23\ \checkmark\)"))])
ck(R(8 * 15, 5), 24); ck(R(60, 40), 1.5); ck(R(2 * 9, 3), 6); assert sp.solve(x_ ** 2 - 36, x_) == [-6, 6]
s1 += practice([
  ('★', L(r"a) Calcula la raó entre els segments de 12 cm i 8 cm. b) Calcula \(x\): \(\frac{3}{x}=\frac{9}{12}\).", r"a) Calcula la razón entre los segmentos de 12 cm y 8 cm. b) Calcula \(x\): \(\frac{3}{x}=\frac{9}{12}\).", r"a) Find the ratio of the segments 12 cm and 8 cm. b) Find \(x\): \(\frac{3}{x}=\frac{9}{12}\).")),
  ('★★', L(r"c) Són proporcionals els segments de 1,5, 2, 6 i 8 cm? d) Calcula el quart proporcional de 2,5, 4 i 7,5 cm.", r"c) ¿Son proporcionales los segmentos de 1,5, 2, 6 y 8 cm? d) Calcula el cuarto proporcional de 2,5, 4 y 7,5 cm.", r"c) Are the segments 1.5, 2, 6 and 8 cm proportional? d) Find the fourth proportional of 2.5, 4 and 7.5 cm.")),
  ('★★★', L(r"e) Calcula el mitjà proporcional de 2 cm i 18 cm, i el de 3 cm i 5 cm (arrodoneix a les centèsimes).", r"e) Calcula el medio proporcional de 2 cm y 18 cm, y el de 3 cm y 5 cm (redondea a las centésimas).", r"e) Find the mean proportional of 2 cm and 18 cm, and of 3 cm and 5 cm (round to 2 decimal places)."))],
  P(r"a) \(\frac{12}{8}=1{,}5\). b) \(9x=36\Rightarrow x=4\). c) Sí: \(1{,}5\cdot8=2\cdot6=12\). d) \(x=\frac{4\cdot7{,}5}{2{,}5}=12\) cm. e) \(x^2=36\Rightarrow x=6\) cm; \(x^2=15\Rightarrow x=\sqrt{15}\approx3{,}87\) cm.",
    r"a) \(\frac{12}{8}=1{,}5\). b) \(9x=36\Rightarrow x=4\). c) Sí: \(1{,}5\cdot8=2\cdot6=12\). d) \(x=\frac{4\cdot7{,}5}{2{,}5}=12\) cm. e) \(x^2=36\Rightarrow x=6\) cm; \(x^2=15\Rightarrow x=\sqrt{15}\approx3{,}87\) cm.",
    r"a) \(\frac{12}{8}=1.5\). b) \(9x=36\Rightarrow x=4\). c) Yes: \(1.5\cdot8=2\cdot6=12\). d) \(x=\frac{4\cdot7.5}{2.5}=12\) cm. e) \(x^2=36\Rightarrow x=6\) cm; \(x^2=15\Rightarrow x=\sqrt{15}\approx3.87\) cm."))
ck(R(12, 8), 1.5); ck(R(36, 9), 4); assert R(15, 10) * 8 == 2 * 6; ck(R(4) * R(75, 10) / R(25, 10), 12); ck(S(15), 3.87, 2)

# =====================================================================
# 10.2 El teorema de Tales
# =====================================================================
s2 = box('def', L('El teorema de Tales', 'El teorema de Tales', "Thales' theorem"),
  P(r"Si diverses rectes <strong>paral·leles</strong> tallen dues rectes secants \(a\) i \(b\), els segments que determinen sobre una d'elles són <strong>proporcionals</strong> als segments corresponents de l'altra:",
    r"Si varias rectas <strong>paralelas</strong> cortan dos rectas secantes \(a\) y \(b\), los segmentos que determinan sobre una de ellas son <strong>proporcionales</strong> a los segmentos correspondientes de la otra:",
    r"If several <strong>parallel</strong> lines cut two lines \(a\) and \(b\), the segments they mark on one of them are <strong>proportional</strong> to the corresponding segments on the other:")
  + figs(G(tales(2, 3, labs={'AB': '', 'BC': ''}), W=270, cap=L('Les rectes morades són paral·leles', 'Las rectas moradas son paralelas', 'The purple lines are parallel')))
  + D(r"\frac{\overline{AB}}{\overline{BC}}=\frac{\overline{A'B'}}{\overline{B'C'}}\qquad\text{%s}\qquad\frac{\overline{AB}}{\overline{A'B'}}=\frac{\overline{BC}}{\overline{B'C'}}=\frac{\overline{AC}}{\overline{A'C'}}" % Lt('o bé', 'o bien', 'or'))
  + P(r"Les dues formes són equivalents (són la mateixa proporció amb els mitjans intercanviats). Si les paral·leles estan a la mateixa distància entre elles, els segments de cada secant són iguals.",
      r"Las dos formas son equivalentes (son la misma proporción con los medios intercambiados). Si las paralelas están a la misma distancia entre sí, los segmentos de cada secante son iguales.",
      r"Both forms are equivalent (they are the same proportion with the means swapped). If the parallel lines are equally spaced, the segments on each line are equal.")
  + widget('w-tales', '📏', L('Mou les paral·leles i les secants', 'Mueve las paralelas y las secantes', 'Move the parallels and the transversals'),
           ['<div class="wrow">' + rng('d1', 1, 5, 0.5, 2, 'd1') + rng('d2', 1, 5, 0.5, 3, 'd2') + '</div>',
            '<div class="wrow">' + rng('ga', 40, 140, 2, 60, 'a') + rng('gb', 40, 140, 2, 80, 'b') + '</div>']))
s2 += box('prop', L('Calcular un segment amb el teorema de Tales', 'Calcular un segmento con el teorema de Tales', "Finding a segment with Thales' theorem"),
  P(r"Escrivim la proporció posant <strong>en el mateix ordre</strong> els segments de cada secant i aïllem la incògnita multiplicant en creu. Si \(\overline{AB}=4\), \(\overline{BC}=6\) i \(\overline{A'B'}=5\):",
    r"Escribimos la proporción poniendo <strong>en el mismo orden</strong> los segmentos de cada secante y despejamos la incógnita multiplicando en cruz. Si \(\overline{AB}=4\), \(\overline{BC}=6\) y \(\overline{A'B'}=5\):",
    r"Write the proportion with the segments of each line <strong>in the same order</strong> and solve by cross-multiplying. If \(\overline{AB}=4\), \(\overline{BC}=6\) and \(\overline{A'B'}=5\):")
  + figs(G(tales(2, 3, labs={'AB': '4', 'BC': '6', 'A1B1': '5', 'B1C1': 'x'}, hot='B1C1'), W=270))
  + D(r"\frac{4}{6}=\frac{5}{x}\ \Rightarrow\ 4x=30\ \Rightarrow\ x=\frac{30}{4}=7{,}5")
  + note(r"El teorema parla dels segments que hi ha <strong>sobre les secants</strong>. Els segments que hi ha sobre les paral·leles (entre \(a\) i \(b\)) no compleixen, en general, aquesta proporció.",
         r"El teorema habla de los segmentos que hay <strong>sobre las secantes</strong>. Los segmentos que hay sobre las paralelas (entre \(a\) y \(b\)) no cumplen, en general, esta proporción.",
         r"The theorem is about the segments <strong>on the transversals</strong>. The segments on the parallel lines themselves (between \(a\) and \(b\)) do not, in general, satisfy this proportion.", '⚠️')
  + drill('tales', 'Entrena: calcula x amb el teorema de Tales', 'Entrena: calcula x con el teorema de Tales', "Train: find x with Thales' theorem"))
ck(R(30, 4), 7.5)
s2 += box('prop', L('El recíproc: com saber si unes rectes són paral·leles', 'El recíproco: cómo saber si unas rectas son paralelas', 'The converse: how to tell whether lines are parallel'),
  P(r"El teorema també funciona al revés: si unes rectes determinen sobre dues secants segments proporcionals, aleshores <strong>són paral·leles</strong>. Si la proporció falla, no ho són.",
    r"El teorema también funciona al revés: si unas rectas determinan sobre dos secantes segmentos proporcionales, entonces <strong>son paralelas</strong>. Si la proporción falla, no lo son.",
    r"The theorem also works backwards: if some lines mark proportional segments on two transversals, then they <strong>are parallel</strong>. If the proportion fails, they aren't.")
  + D(r"\overline{AB}=3,\ \overline{BC}=4,\ \overline{A'B'}=4{,}5,\ \overline{B'C'}=6:\quad \frac34=0{,}75=\frac{4{,}5}{6}\ \checkmark"))
s2 = s2.replace("aleshores <strong>són paral·leles</strong>", "aleshores <strong>són paral·leles</strong>").replace("", "")
ck(R(45, 10) / 6, 0.75)
s2 += levels(
 [prob(L(r"Les rectes \(r\), \(s\) i \(t\) són paral·leles. Sobre la secant \(a\) determinen \(\overline{AB}=3\) cm i \(\overline{BC}=5\) cm, i sobre la secant \(b\), \(\overline{A'B'}=4{,}2\) cm. Calcula \(\overline{B'C'}\).", r"Las rectas \(r\), \(s\) y \(t\) son paralelas. Sobre la secante \(a\) determinan \(\overline{AB}=3\) cm y \(\overline{BC}=5\) cm, y sobre la secante \(b\), \(\overline{A'B'}=4{,}2\) cm. Calcula \(\overline{B'C'}\).", r"The lines \(r\), \(s\) and \(t\) are parallel. On line \(a\) they mark \(\overline{AB}=3\) cm and \(\overline{BC}=5\) cm, and on line \(b\), \(\overline{A'B'}=4.2\) cm. Find \(\overline{B'C'}\)."),
       D(r"\frac{3}{5}=\frac{4{,}2}{x}\ \Rightarrow\ 3x=21\ \Rightarrow\ x=\boxed{7\ \text{cm}}"))],
 [prob(L(r"En la figura, les rectes morades són paral·leles. Calcula \(x\) i \(\overline{A'C'}\).", r"En la figura, las rectas moradas son paralelas. Calcula \(x\) y \(\overline{A'C'}\).", r"In the figure the purple lines are parallel. Find \(x\) and \(\overline{A'C'}\).")
       + figs(G(tales(2.5, 3.5, labs={'AB': '5', 'BC': '7', 'A1B1': 'x', 'B1C1': '8,4'}, hot='A1B1'), W=270)),
       D(r"\frac{5}{7}=\frac{x}{8{,}4}\ \Rightarrow\ 7x=42\ \Rightarrow\ x=\boxed{6}"),
       D(r"\overline{A'C'}=6+8{,}4=\boxed{14{,}4}"))],
 [prob(L(r"Tres parcel·les estan entre dos carrers, i les seues partions són paral·leles. Al carrer Major les façanes fan 20 m, 30 m i 40 m. Al carrer Nou, la façana total de les tres parcel·les fa 108 m. Quant fa la façana de cada parcel·la al carrer Nou?", r"Tres parcelas están entre dos calles, y sus lindes son paralelas. En la calle Mayor las fachadas miden 20 m, 30 m y 40 m. En la calle Nueva, la fachada total de las tres parcelas mide 108 m. ¿Cuánto mide la fachada de cada parcela en la calle Nueva?", r"Three plots lie between two streets and their boundaries are parallel. On High Street their fronts are 20 m, 30 m and 40 m. On New Street the three plots have a total front of 108 m. How long is each plot's front on New Street?"),
       P(r"Pel teorema de Tales, la raó entre les façanes dels dos carrers és sempre la mateixa:", r"Por el teorema de Tales, la razón entre las fachadas de las dos calles es siempre la misma:", r"By Thales' theorem, the ratio between the fronts on the two streets is always the same:"),
       D(r"k=\frac{108}{20+30+40}=\frac{108}{90}=1{,}2"),
       D(r"20\cdot1{,}2=\boxed{24\ \text{m}}\qquad30\cdot1{,}2=\boxed{36\ \text{m}}\qquad40\cdot1{,}2=\boxed{48\ \text{m}}"),
       P(r"Comprovació: \(24+36+48=108\ \checkmark\)", r"Comprobación: \(24+36+48=108\ \checkmark\)", r"Check: \(24+36+48=108\ \checkmark\)"))])
ck(R(5 * 42, 30), 7); ck(R(42, 7), 6); ck(R(108, 90), 1.2); assert 24 + 36 + 48 == 108
s2 += practice([
  ('★', L(r"a) Amb rectes paral·leles: \(\overline{AB}=6\), \(\overline{BC}=9\), \(\overline{A'B'}=4\). Calcula \(\overline{B'C'}\).", r"a) Con rectas paralelas: \(\overline{AB}=6\), \(\overline{BC}=9\), \(\overline{A'B'}=4\). Calcula \(\overline{B'C'}\).", r"a) With parallel lines: \(\overline{AB}=6\), \(\overline{BC}=9\), \(\overline{A'B'}=4\). Find \(\overline{B'C'}\).")),
  ('★★', L(r"b) \(\overline{AB}=2{,}5\), \(\overline{A'B'}=3\), \(\overline{B'C'}=4{,}8\). Calcula \(\overline{BC}\). c) \(\overline{AB}=4\), \(\overline{BC}=5\), \(\overline{A'B'}=6\), \(\overline{B'C'}=7\). Són paral·leles les rectes?", r"b) \(\overline{AB}=2{,}5\), \(\overline{A'B'}=3\), \(\overline{B'C'}=4{,}8\). Calcula \(\overline{BC}\). c) \(\overline{AB}=4\), \(\overline{BC}=5\), \(\overline{A'B'}=6\), \(\overline{B'C'}=7\). ¿Son paralelas las rectas?", r"b) \(\overline{AB}=2.5\), \(\overline{A'B'}=3\), \(\overline{B'C'}=4.8\). Find \(\overline{BC}\). c) \(\overline{AB}=4\), \(\overline{BC}=5\), \(\overline{A'B'}=6\), \(\overline{B'C'}=7\). Are the lines parallel?")),
  ('★★★', L(r"d) Amb rectes paral·leles, \(\overline{AB}=x\), \(\overline{BC}=x+3\), \(\overline{A'B'}=4\) i \(\overline{B'C'}=6\). Calcula \(x\).", r"d) Con rectas paralelas, \(\overline{AB}=x\), \(\overline{BC}=x+3\), \(\overline{A'B'}=4\) y \(\overline{B'C'}=6\). Calcula \(x\).", r"d) With parallel lines, \(\overline{AB}=x\), \(\overline{BC}=x+3\), \(\overline{A'B'}=4\) and \(\overline{B'C'}=6\). Find \(x\)."))],
  P(r"a) \(\frac69=\frac4x\Rightarrow x=6\). b) \(\frac{2{,}5}{x}=\frac{3}{4{,}8}\Rightarrow x=4\). c) \(\frac45=0{,}8\neq\frac67\approx0{,}86\): no són paral·leles. d) \(\frac{x}{x+3}=\frac46\Rightarrow6x=4x+12\Rightarrow x=6\).",
    r"a) \(\frac69=\frac4x\Rightarrow x=6\). b) \(\frac{2{,}5}{x}=\frac{3}{4{,}8}\Rightarrow x=4\). c) \(\frac45=0{,}8\neq\frac67\approx0{,}86\): no son paralelas. d) \(\frac{x}{x+3}=\frac46\Rightarrow6x=4x+12\Rightarrow x=6\).",
    r"a) \(\frac69=\frac4x\Rightarrow x=6\). b) \(\frac{2.5}{x}=\frac{3}{4.8}\Rightarrow x=4\). c) \(\frac45=0.8\neq\frac67\approx0.86\): they aren't parallel. d) \(\frac{x}{x+3}=\frac46\Rightarrow6x=4x+12\Rightarrow x=6\)."))
ck(R(9 * 4, 6), 6); ck(R(25, 10) * R(48, 10) / 3, 4); ck(R(6, 7), 0.86, 2); assert sp.solve(6 * x_ - 4 * (x_ + 3), x_) == [6]
