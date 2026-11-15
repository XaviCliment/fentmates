# Apartats 2.5-2.8 (fraccions, fraccions i decimals, operacions) dels apunts de la Unitat 2 de 2n ESO.
# Les asserts ck() comproven els resultats escrits a mà (amb Fraction).
from comu import *

# ============================================================ 2.5
s5 = box('def', L('Què és una fracció?', '¿Qué es una fracción?', 'What is a fraction?'),
  P(r"Una <strong>fracció</strong> \(\frac{a}{b}\) és una expressió amb un <strong>numerador</strong> \(a\) i un <strong>denominador</strong> \(b\neq0\). Es pot entendre de tres maneres:",
    r"Una <strong>fracción</strong> \(\frac{a}{b}\) es una expresión con un <strong>numerador</strong> \(a\) y un <strong>denominador</strong> \(b\neq0\). Se puede entender de tres maneras:",
    r"A <strong>fraction</strong> \(\frac{a}{b}\) has a <strong>numerator</strong> \(a\) and a <strong>denominator</strong> \(b\neq0\). It can be understood in three ways:")
  + table([L('Significat', 'Significado', 'Meaning'), L('Exemple amb', 'Ejemplo con', 'Example with') + r' \(\frac{3}{4}\)', ''],
          [[L('<strong>Part de la unitat</strong>', '<strong>Parte de la unidad</strong>', '<strong>Part of a whole</strong>'), L("Dividim la unitat en 4 parts iguals i n'agafem 3.", "Dividimos la unidad en 4 partes iguales y tomamos 3.", "Split the whole into 4 equal parts and take 3."), svg_bar(4, 3, 160, 24)],
           [L('<strong>Quocient</strong>', '<strong>Cociente</strong>', '<strong>Quotient</strong>'), L("És la divisió del numerador entre el denominador.", "Es la división del numerador entre el denominador.", "It's the numerator divided by the denominator."), r'\(3:4=0\dc75\)'],
           [L('<strong>Operador</strong>', '<strong>Operador</strong>', '<strong>Operator</strong>'), L("Actua sobre una quantitat: la dividim entre 4 i multipliquem per 3.", "Actúa sobre una cantidad: la dividimos entre 4 y multiplicamos por 3.", "It acts on an amount: divide by 4 and multiply by 3."), r'\(\frac{3}{4}\ ' + D_ + r'\ 80=\frac{3\cdot80}{4}=60\)']], 'data nw')
  + ul(L(r"Si \(a<b\), la fracció és <strong>pròpia</strong> (menor que 1); si \(a>b\), és <strong>impròpia</strong> (major que 1) i es pot escriure com un enter més una fracció pròpia: \(\frac{11}{4}=2+\frac{3}{4}\).", r"Si \(a<b\), la fracción es <strong>propia</strong> (menor que 1); si \(a>b\), es <strong>impropia</strong> (mayor que 1) y se puede escribir como un entero más una fracción propia: \(\frac{11}{4}=2+\frac{3}{4}\).", r"If \(a<b\), the fraction is <strong>proper</strong> (less than 1); if \(a>b\), it's <strong>improper</strong> (more than 1) and can be written as a whole number plus a proper fraction: \(\frac{11}{4}=2+\frac{3}{4}\)."),
         L(r"Les fraccions també poden ser <strong>negatives</strong>: \(\frac{-2}{3}=\frac{2}{-3}=-\frac{2}{3}\). Normalment deixem el denominador positiu.", r"Las fracciones también pueden ser <strong>negativas</strong>: \(\frac{-2}{3}=\frac{2}{-3}=-\frac{2}{3}\). Normalmente dejamos el denominador positivo.", r"Fractions can also be <strong>negative</strong>: \(\frac{-2}{3}=\frac{2}{-3}=-\frac{2}{3}\). We usually keep the denominator positive.")))
ck(Fr(3, 4) * 80, 60); ck(Fr(11, 4), 2 + Fr(3, 4))
s5 += box('def', L('Fraccions equivalents. Fracció irreductible', 'Fracciones equivalentes. Fracción irreducible', 'Equivalent fractions. Simplest form'),
  P(r"Dues fraccions són <strong>equivalents</strong> si representen el mateix nombre. Ho comprovem amb els <strong>productes creuats</strong>: \(\ \frac{a}{b}=\frac{c}{d}\iff a\cdot d=b\cdot c\). &nbsp; \(\frac{6}{15}=\frac{2}{5}\) perquè \(6\cdot5=15\cdot2=30\).",
    r"Dos fracciones son <strong>equivalentes</strong> si representan el mismo número. Lo comprobamos con los <strong>productos cruzados</strong>: \(\ \frac{a}{b}=\frac{c}{d}\iff a\cdot d=b\cdot c\). &nbsp; \(\frac{6}{15}=\frac{2}{5}\) porque \(6\cdot5=15\cdot2=30\).",
    r"Two fractions are <strong>equivalent</strong> if they stand for the same number. Check with <strong>cross products</strong>: \(\ \frac{a}{b}=\frac{c}{d}\iff a\cdot d=b\cdot c\). &nbsp; \(\frac{6}{15}=\frac{2}{5}\) because \(6\cdot5=15\cdot2=30\).")
  + ul(L(r"<strong>Amplificar</strong>: multipliquem numerador i denominador pel mateix nombre: \(\frac{2}{5}=\frac{4}{10}=\frac{6}{15}=\ldots\)", r"<strong>Amplificar</strong>: multiplicamos numerador y denominador por el mismo número: \(\frac{2}{5}=\frac{4}{10}=\frac{6}{15}=\ldots\)", r"<strong>Scaling up</strong>: multiply top and bottom by the same number: \(\frac{2}{5}=\frac{4}{10}=\frac{6}{15}=\ldots\)"),
         L(r"<strong>Simplificar</strong>: els dividim pel mateix nombre. Si els dividim pel seu \(\text{" + MCD + r"}\), obtenim la <strong>fracció irreductible</strong>, que ja no es pot simplificar: \(\frac{36}{48}=\frac{36:12}{48:12}=\frac{3}{4}\).", r"<strong>Simplificar</strong>: los dividimos por el mismo número. Si los dividimos por su \(\text{" + MCD + r"}\), obtenemos la <strong>fracción irreducible</strong>, que ya no se puede simplificar: \(\frac{36}{48}=\frac{36:12}{48:12}=\frac{3}{4}\).", r"<strong>Simplifying</strong>: divide them by the same number. Dividing by their \(\text{" + MCD + r"}\) gives the <strong>simplest form</strong>, which can't be simplified any more: \(\frac{36}{48}=\frac{36:12}{48:12}=\frac{3}{4}\).")))
ck(Fr(36, 48), Fr(3, 4)); assert 6 * 5 == 15 * 2
s5 += f'''<div class="widget" id="w-eq">
  <div class="wt">🟰 {L("Fàbrica de fraccions equivalents", "Fábrica de fracciones equivalentes", "Equivalent fraction factory")}</div>
  <div class="wrow"><label>{L("Fracció", "Fracción", "Fraction")} {fin("a", "b", "36", "48")}</label>{nin("k", "Amplifica per", "Amplifica por", "Scale by", "1")}</div>
  {quick([("36,48,1", "36/48"), ("2,3,4", "2/3 × 4"), ("75,100,1", "75/100"), ("84,126,1", "84/126"), ("3,5,3", "3/5 × 3"), ("105,180,1", "105/180")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('simp', 'Entrena: fracció irreductible', 'Entrena: fracción irreducible', 'Train: simplest form')
s5 += box('prop', L('Comparar i ordenar fraccions', 'Comparar y ordenar fracciones', 'Comparing and ordering fractions'),
  ul(L(r"Amb el <strong>mateix denominador</strong>, és més gran la que té el numerador més gran: \(\frac{7}{9}>\frac{4}{9}\).", r"Con el <strong>mismo denominador</strong>, es mayor la que tiene el numerador mayor: \(\frac{7}{9}>\frac{4}{9}\).", r"With the <strong>same denominator</strong>, the bigger numerator wins: \(\frac{7}{9}>\frac{4}{9}\)."),
     L(r"Amb el <strong>mateix numerador</strong>, és més gran la que té el denominador més xicotet: \(\frac{3}{4}>\frac{3}{7}\).", r"Con el <strong>mismo numerador</strong>, es mayor la que tiene el denominador más pequeño: \(\frac{3}{4}>\frac{3}{7}\).", r"With the <strong>same numerator</strong>, the smaller denominator wins: \(\frac{3}{4}>\frac{3}{7}\)."),
     L(r"En general, les <strong>reduïm a comú denominador</strong> (amb el \(\text{" + MCM + r"}\) dels denominadors) i comparem els numeradors. També podem passar-les a decimal.", r"En general, las <strong>reducimos a común denominador</strong> (con el \(\text{" + MCM + r"}\) de los denominadores) y comparamos los numeradores. También podemos pasarlas a decimal.", r"In general, give them a <strong>common denominator</strong> (the \(\text{" + MCM + r"}\) of the denominators) and compare numerators. You can also turn them into decimals."),
     L(r"Qualsevol fracció negativa és menor que qualsevol positiva, i entre dues negatives és més gran la que està més a prop del 0: \(-\frac{1}{4}>-\frac{1}{2}\).", r"Cualquier fracción negativa es menor que cualquier positiva, y entre dos negativas es mayor la que está más cerca del 0: \(-\frac{1}{4}>-\frac{1}{2}\).", r"Any negative fraction is less than any positive one, and of two negatives the one closer to 0 is bigger: \(-\frac{1}{4}>-\frac{1}{2}\).")))
s5 += f'''<div class="widget" id="w-cmp">
  <div class="wt">📏 {L("Ordena fraccions en la recta", "Ordena fracciones en la recta", "Order fractions on the number line")}</div>
  <div class="wrow"><label>{L("Fraccions", "Fracciones", "Fractions")} <input class="tin w" type="text" value="2/3, 3/4, 5/8, 7/12" autocomplete="off" spellcheck="false" aria-label="fraccions"></label></div>
  {quick([("2/3, 3/4, 5/8, 7/12", "2/3, 3/4, 5/8, 7/12"), ("3/4, 3/7", "3/4, 3/7"), ("8/9, 11/12", "8/9, 11/12"), ("4/9, 5/6, 2/3", "4/9, 5/6, 2/3"), ("5/2, 2/3, 4/7, 5/4", "5/2, 2/3, 4/7, 5/4")])}
  <div class="fvis"></div>
  <div class="info" aria-live="polite"></div>
</div>
''' + drill('cmp', 'Entrena: compara fraccions', 'Entrena: compara fracciones', 'Train: compare fractions')
s5 += level(1, 1,
  prob(L(r"Simplifica fins a la fracció irreductible: a) \(\frac{84}{126}\) &nbsp; b) \(\frac{105}{180}\)", r"Simplifica hasta la fracción irreducible: a) \(\frac{84}{126}\) &nbsp; b) \(\frac{105}{180}\)", r"Simplify fully: a) \(\frac{84}{126}\) &nbsp; b) \(\frac{105}{180}\)"),
       r'\[\text{a) }84=2^2\cdot3\cdot7,\ 126=2\cdot3^2\cdot7\ \to\ \text{' + MCD + r'}=42:\quad\frac{84}{126}=\boxed{\frac{2}{3}}\]',
       r'\[\text{b) }\text{' + MCD + r'}(105,180)=15:\quad\frac{105}{180}=\boxed{\frac{7}{12}}\]'))
ck(Fr(84, 126), Fr(2, 3)); ck(Fr(105, 180), Fr(7, 12))
s5 += level(2, 2,
  prob(L(r"Ordena de menor a major: \(\ \frac{5}{6};\ -\frac{3}{4};\ \frac{7}{9};\ -\frac{2}{3};\ \frac{3}{4}\)", r"Ordena de menor a mayor: \(\ \frac{5}{6};\ -\frac{3}{4};\ \frac{7}{9};\ -\frac{2}{3};\ \frac{3}{4}\)", r"Order from smallest to largest: \(\ \frac{5}{6};\ -\frac{3}{4};\ \frac{7}{9};\ -\frac{2}{3};\ \frac{3}{4}\)"),
       P(r"\(\text{" + MCM + r"}(6,4,9,3,4)=36\):", r"\(\text{" + MCM + r"}(6,4,9,3,4)=36\):", r"\(\text{" + MCM + r"}(6,4,9,3,4)=36\):") + r'\[\frac{30}{36};\ -\frac{27}{36};\ \frac{28}{36};\ -\frac{24}{36};\ \frac{27}{36}\]',
       r'\[\boxed{-\frac{3}{4}<-\frac{2}{3}<\frac{3}{4}<\frac{7}{9}<\frac{5}{6}}\]'))
assert sorted([Fr(5, 6), Fr(-3, 4), Fr(7, 9), Fr(-2, 3), Fr(3, 4)]) == [Fr(-3, 4), Fr(-2, 3), Fr(3, 4), Fr(7, 9), Fr(5, 6)]
s5 += level(3, 3,
  prob(L(r"Troba \(x\) perquè les fraccions siguen equivalents: a) \(\frac{x}{12}=\frac{15}{36}\) &nbsp; b) \(\frac{8}{x}=\frac{-2}{5}\)", r"Halla \(x\) para que las fracciones sean equivalentes: a) \(\frac{x}{12}=\frac{15}{36}\) &nbsp; b) \(\frac{8}{x}=\frac{-2}{5}\)", r"Find \(x\) so that the fractions are equivalent: a) \(\frac{x}{12}=\frac{15}{36}\) &nbsp; b) \(\frac{8}{x}=\frac{-2}{5}\)"),
       r'\[\text{a) }36x=12\cdot15=180\ \to\ x=\frac{180}{36}=\boxed{5}\]',
       r'\[\text{b) }-2x=8\cdot5=40\ \to\ x=\frac{40}{-2}=\boxed{-20}\]'))
ck(Fr(5, 12), Fr(15, 36)); ck(Fr(8, -20), Fr(-2, 5))
s5 += practice([
  ('★', L(r"a) Calcula \(\frac{2}{7}\) de 63. &nbsp; b) Escriu \(\frac{17}{5}\) com un enter més una fracció pròpia.", r"a) Calcula \(\frac{2}{7}\) de 63. &nbsp; b) Escribe \(\frac{17}{5}\) como un entero más una fracción propia.", r"a) Work out \(\frac{2}{7}\) of 63. &nbsp; b) Write \(\frac{17}{5}\) as a whole number plus a proper fraction.")),
  ('★★', L(r"c) Són equivalents \(\frac{14}{21}\) i \(\frac{22}{33}\)? &nbsp; d) Escriu tres fraccions compreses entre \(\frac{1}{3}\) i \(\frac{1}{2}\).", r"c) ¿Son equivalentes \(\frac{14}{21}\) y \(\frac{22}{33}\)? &nbsp; d) Escribe tres fracciones comprendidas entre \(\frac{1}{3}\) y \(\frac{1}{2}\).", r"c) Are \(\frac{14}{21}\) and \(\frac{22}{33}\) equivalent? &nbsp; d) Write three fractions between \(\frac{1}{3}\) and \(\frac{1}{2}\).")),
  ('★★★', L(r"e) Quina fracció de denominador 20 està just a la meitat entre \(\frac{2}{5}\) i \(\frac{1}{2}\)?", r"e) ¿Qué fracción de denominador 20 está justo en la mitad entre \(\frac{2}{5}\) y \(\frac{1}{2}\)?", r"e) Which fraction with denominator 20 lies exactly halfway between \(\frac{2}{5}\) and \(\frac{1}{2}\)?"))],
  P(r"a) \(18\) &nbsp; b) \(3+\frac{2}{5}\) &nbsp; c) Sí: \(14\cdot33=21\cdot22=462\) (totes dues valen \(\frac{2}{3}\)). &nbsp; d) Amb denominador 24: \(\frac{9}{24},\frac{10}{24},\frac{11}{24}\). &nbsp; e) \(\frac{8}{20}\) i \(\frac{10}{20}\): la del mig és \(\frac{9}{20}\).",
    r"a) \(18\) &nbsp; b) \(3+\frac{2}{5}\) &nbsp; c) Sí: \(14\cdot33=21\cdot22=462\) (las dos valen \(\frac{2}{3}\)). &nbsp; d) Con denominador 24: \(\frac{9}{24},\frac{10}{24},\frac{11}{24}\). &nbsp; e) \(\frac{8}{20}\) y \(\frac{10}{20}\): la del medio es \(\frac{9}{20}\).",
    r"a) \(18\) &nbsp; b) \(3+\frac{2}{5}\) &nbsp; c) Yes: \(14\cdot33=21\cdot22=462\) (both are \(\frac{2}{3}\)). &nbsp; d) With denominator 24: \(\frac{9}{24},\frac{10}{24},\frac{11}{24}\). &nbsp; e) \(\frac{8}{20}\) and \(\frac{10}{20}\): halfway is \(\frac{9}{20}\)."))
ck(Fr(2, 7) * 63, 18); assert 14 * 33 == 21 * 22 == 462; assert Fr(1, 3) < Fr(9, 24) and Fr(11, 24) < Fr(1, 2); ck((Fr(2, 5) + Fr(1, 2)) / 2, Fr(9, 20))

# ============================================================ 2.6
s6 = box('def', L('De fracció a decimal', 'De fracción a decimal', 'From fraction to decimal'),
  P(r"Dividim el numerador entre el denominador. El resultat pot ser un decimal exacte o periòdic, i ho podem saber <strong>abans</strong> de dividir mirant el denominador de la fracció <strong>irreductible</strong>:",
    r"Dividimos el numerador entre el denominador. El resultado puede ser un decimal exacto o periódico, y lo podemos saber <strong>antes</strong> de dividir mirando el denominador de la fracción <strong>irreducible</strong>:",
    r"Divide the numerator by the denominator. The result can be terminating or recurring, and we can tell <strong>before</strong> dividing by looking at the denominator of the fraction in <strong>simplest form</strong>:")
  + table([L('Denominador (descompost en factors primers)', 'Denominador (descompuesto en factores primos)', 'Denominator (prime factors)'), L('Decimal', 'Decimal', 'Decimal'), L('Exemples', 'Ejemplos', 'Examples')],
          [[L('Només té els factors 2 i/o 5', 'Solo tiene los factores 2 y/o 5', 'Only the factors 2 and/or 5'), L('Exacte', 'Exacto', 'Terminating'), r'\(\frac{7}{40}=0\dc175\quad (40=2^3\cdot5)\)'],
           [L('No té cap factor 2 ni 5', 'No tiene ningún factor 2 ni 5', 'No factor 2 or 5 at all'), L('Periòdic pur', 'Periódico puro', 'Purely recurring'), r'\(\frac{4}{11}=0\dc\overline{36}\quad (11)\)'],
           [L('Té factors 2 o 5 i també d’altres', 'Tiene factores 2 o 5 y también otros', 'Has 2 or 5 and other factors too'), L('Periòdic mixt', 'Periódico mixto', 'Mixed recurring'), r'\(\frac{7}{12}=0\dc58\overline{3}\quad (12=2^2\cdot3)\)']], 'data nw'))
ck(Fr(7, 40), Fr('0.175')); assert per(4, 11) == r'0\dc\overline{36}' and per(7, 12) == r'0\dc58\overline{3}'
s6 += widget('w-fd', '🔁', L('Fraccions ⇄ decimals', 'Fracciones ⇄ decimales', 'Fractions ⇄ decimals'),
  f'  <div class="wrow">{gseg("m", [("f", L("Fracció → decimal", "Fracción → decimal", "Fraction → decimal")), ("d", L("Decimal exacte → fracció", "Decimal exacto → fracción", "Terminating decimal → fraction"))], "f")}</div>\n'
  + f'  <div class="wrow" style="margin-top:8px"><span data-p="f">{nin("n", "Numerador", "Numerador", "Numerator", "7", "s", "numeric")}{nin("d", "Denominador", "Denominador", "Denominator", "12", "s", "numeric")}</span><span data-p="d">{nin("x", "Decimal exacte", "Decimal exacto", "Terminating decimal", "0,175", "m")}</span></div>\n'
  + '  ' + quick([('f;7;12', '7/12'), ('f;7;40', '7/40'), ('f;4;11', '4/11'), ('f;5;6', '5/6'), ('f;1;7', '1/7'), ('f;13;20', '13/20'), ('d;0,175', '0,175'), ('d;2,4', '2,4'), ('d;0,125', '0,125')]) + '\n')
s6 += box('def', L('De decimal a fracció: la fracció generatriu', 'De decimal a fracción: la fracción generatriz', 'From decimal to fraction'),
  P(r"La fracció irreductible que dona un nombre decimal és la seua <strong>fracció generatriu</strong>. Sempre en té si el decimal és exacte o periòdic:",
    r"La fracción irreducible que da un número decimal es su <strong>fracción generatriz</strong>. Siempre la tiene si el decimal es exacto o periódico:",
    r"The fraction in simplest form that gives a decimal is its <strong>generating fraction</strong>. Every terminating or recurring decimal has one:")
  + table([L('Tipus', 'Tipo', 'Kind'), L('Regla', 'Regla', 'Rule'), L('Exemple', 'Ejemplo', 'Example')],
          [[L('Exacte', 'Exacto', 'Terminating'), L("Numerador: el nombre sense coma. Denominador: un 1 seguit de tants zeros com xifres decimals.", "Numerador: el número sin coma. Denominador: un 1 seguido de tantos ceros como cifras decimales.", "Numerator: the number without its comma. Denominator: 1 followed by one zero per decimal digit."), r'\(2\dc35=\frac{235}{100}=\frac{47}{20}\)'],
           [L('Periòdic pur', 'Periódico puro', 'Purely recurring'), L("Numerador: el nombre sense coma fins al final del període <strong>menys</strong> la part entera. Denominador: tants <strong>9</strong> com xifres té el període.", "Numerador: el número sin coma hasta el final del periodo <strong>menos</strong> la parte entera. Denominador: tantos <strong>9</strong> como cifras tiene el periodo.", "Numerator: the number without its comma up to the end of the period <strong>minus</strong> the whole part. Denominator: one <strong>9</strong> per digit of the period."), r'\(2\dc\overline{45}=\frac{245-2}{99}=\frac{243}{99}=\frac{27}{11}\)'],
           [L('Periòdic mixt', 'Periódico mixto', 'Mixed recurring'), L("Numerador: el nombre sense coma fins al final del període <strong>menys</strong> la part que no es repeteix. Denominador: tants <strong>9</strong> com xifres té el període i tants <strong>0</strong> com xifres té l'anteperíode.", "Numerador: el número sin coma hasta el final del periodo <strong>menos</strong> la parte que no se repite. Denominador: tantos <strong>9</strong> como cifras tiene el periodo y tantos <strong>0</strong> como cifras tiene el anteperiodo.", "Numerator: the number without its comma up to the end of the period <strong>minus</strong> the non-repeating part. Denominator: one <strong>9</strong> per period digit, then one <strong>0</strong> per non-repeating decimal digit."), r'\(1\dc2\overline{3}=\frac{123-12}{90}=\frac{111}{90}=\frac{37}{30}\)']], 'data nw')
  + P(r"D'on ix la regla? Per a \(x=1\dc2\overline{3}\): multipliquem per 100 i per 10 perquè els dos nombres tinguen els mateixos decimals, i restem:",
      r"¿De dónde sale la regla? Para \(x=1\dc2\overline{3}\): multiplicamos por 100 y por 10 para que los dos números tengan los mismos decimales, y restamos:",
      r"Where does the rule come from? For \(x=1\dc2\overline{3}\): multiply by 100 and by 10 so both numbers have the same decimals, then subtract:")
  + r'\[\begin{aligned}100x&=123\dc333\ldots\\-\ 10x&=\ \ 12\dc333\ldots\\ \hline 90x&=111\end{aligned}\qquad x=\frac{111}{90}=\frac{37}{30}\]')
ck(Fr('2.35'), Fr(47, 20)); ck(gen(2, '', '45'), Fr(27, 11)); ck(gen(1, '2', '3'), Fr(37, 30)); ck(Fr(111, 90), Fr(37, 30))
s6 += widget('w-gen', '🧬', L('Fracció generatriu', 'Fracción generatriz', 'Generating fraction'),
  f'  <div class="wrow">{nin("e", "Part entera", "Parte entera", "Whole part", "1", "s", "numeric")}{nin("a", "Anteperíode", "Anteperiodo", "Non-repeating", "2", "s", "numeric")}{nin("p", "Període", "Periodo", "Period", "3", "s", "numeric")}</div>\n'
  + '  ' + quick([('1;2;3', '1,2(3)'), ('0;;45', '0,(45)'), ('2;;45', '2,(45)'), ('0;8;3', '0,8(3)'), ('3;04;1', '3,04(1)'), ('0;;142', '0,(142)'), ('1;;9', '1,(9)')]) + '\n')
s6 += drill('fd', 'Entrena: fraccions i decimals exactes', 'Entrena: fracciones y decimales exactos', 'Train: fractions and terminating decimals')
s6 += drill('gen', 'Entrena: fracció generatriu', 'Entrena: fracción generatriz', 'Train: generating fractions')
s6 += level(1, 1,
  prob(L(r"Sense dividir, digues quin tipus de decimal dona cada fracció. Després comprova-ho: a) \(\frac{9}{20}\) &nbsp; b) \(\frac{5}{9}\) &nbsp; c) \(\frac{7}{30}\) &nbsp; d) \(\frac{21}{28}\)",
         r"Sin dividir, di qué tipo de decimal da cada fracción. Después compruébalo: a) \(\frac{9}{20}\) &nbsp; b) \(\frac{5}{9}\) &nbsp; c) \(\frac{7}{30}\) &nbsp; d) \(\frac{21}{28}\)",
         r"Without dividing, say what kind of decimal each fraction gives. Then check: a) \(\frac{9}{20}\) &nbsp; b) \(\frac{5}{9}\) &nbsp; c) \(\frac{7}{30}\) &nbsp; d) \(\frac{21}{28}\)"),
       r'\[\text{a) }20=2^2\cdot5:\ \boxed{0\dc45}\qquad\text{b) }9=3^2:\ \boxed{0\dc\overline{5}}\qquad\text{c) }30=2\cdot3\cdot5:\ \boxed{0\dc2\overline{3}}\]',
       P(r"d) Compte! Primer simplifiquem: \(\frac{21}{28}=\frac{3}{4}\), i \(4=2^2\): és exacte, \(\boxed{0\dc75}\).", r"d) ¡Cuidado! Primero simplificamos: \(\frac{21}{28}=\frac{3}{4}\), y \(4=2^2\): es exacto, \(\boxed{0\dc75}\).", r"d) Careful! Simplify first: \(\frac{21}{28}=\frac{3}{4}\), and \(4=2^2\): it terminates, \(\boxed{0\dc75}\).")))
assert per(9, 20) == r'0\dc45' and per(5, 9) == r'0\dc\overline{5}' and per(7, 30) == r'0\dc2\overline{3}' and per(21, 28) == r'0\dc75'
s6 += level(2, 2,
  prob(L(r"Calcula la fracció generatriu: a) \(0\dc\overline{6}\) &nbsp; b) \(3\dc\overline{12}\) &nbsp; c) \(0\dc8\overline{3}\) &nbsp; d) \(2\dc1\overline{45}\)", r"Calcula la fracción generatriz: a) \(0\dc\overline{6}\) &nbsp; b) \(3\dc\overline{12}\) &nbsp; c) \(0\dc8\overline{3}\) &nbsp; d) \(2\dc1\overline{45}\)", r"Find the generating fraction: a) \(0\dc\overline{6}\) &nbsp; b) \(3\dc\overline{12}\) &nbsp; c) \(0\dc8\overline{3}\) &nbsp; d) \(2\dc1\overline{45}\)"),
       r'\[\text{a) }\frac{6}{9}=\boxed{\frac{2}{3}}\qquad\text{b) }\frac{312-3}{99}=\frac{309}{99}=\boxed{\frac{103}{33}}\]',
       r'\[\text{c) }\frac{83-8}{90}=\frac{75}{90}=\boxed{\frac{5}{6}}\qquad\text{d) }\frac{2145-21}{990}=\frac{2124}{990}=\boxed{\frac{118}{55}}\]'))
ck(gen(0, '', '6'), Fr(2, 3)); ck(gen(3, '', '12'), Fr(103, 33)); ck(gen(0, '8', '3'), Fr(5, 6)); ck(gen(2, '1', '45'), Fr(118, 55))
s6 += level(3, 3,
  prob(L(r"Calcula \(0\dc\overline{3}+0\dc\overline{6}\) passant a fracció. Què n'obtens? Fes el mateix amb \(0\dc\overline{9}\).", r"Calcula \(0\dc\overline{3}+0\dc\overline{6}\) pasando a fracción. ¿Qué obtienes? Haz lo mismo con \(0\dc\overline{9}\).", r"Work out \(0\dc\overline{3}+0\dc\overline{6}\) by turning them into fractions. What do you get? Do the same with \(0\dc\overline{9}\)."),
       r'\[0\dc\overline{3}+0\dc\overline{6}=\frac{3}{9}+\frac{6}{9}=\frac{9}{9}=\boxed{1}\qquad 0\dc\overline{9}=\frac{9}{9}=\boxed{1}\]',
       P(r"Encara que semble estrany, \(0\dc999\ldots\) i \(1\) són <strong>el mateix nombre</strong>: entre ells no hi cap cap altre nombre.", r"Aunque parezca extraño, \(0\dc999\ldots\) y \(1\) son <strong>el mismo número</strong>: entre ellos no cabe ningún otro número.", r"Strange as it seems, \(0\dc999\ldots\) and \(1\) are <strong>the same number</strong>: there's no other number between them.")))
ck(gen(0, '', '3') + gen(0, '', '6'), 1); ck(gen(0, '', '9'), 1)
s6 += practice([
  ('★', L(r"a) Escriu com a fracció irreductible: \(0\dc8\), \(\ 0\dc25\), \(\ 1\dc04\). &nbsp; b) Escriu en forma decimal: \(\frac{3}{8}\), \(\frac{2}{3}\).", r"a) Escribe como fracción irreducible: \(0\dc8\), \(\ 0\dc25\), \(\ 1\dc04\). &nbsp; b) Escribe en forma decimal: \(\frac{3}{8}\), \(\frac{2}{3}\).", r"a) Write in simplest form: \(0\dc8\), \(\ 0\dc25\), \(\ 1\dc04\). &nbsp; b) Write as decimals: \(\frac{3}{8}\), \(\frac{2}{3}\).")),
  ('★★', L(r"c) Fracció generatriu de \(5\dc\overline{4}\), \(\ 0\dc\overline{27}\) i \(\ 0\dc1\overline{6}\).", r"c) Fracción generatriz de \(5\dc\overline{4}\), \(\ 0\dc\overline{27}\) y \(\ 0\dc1\overline{6}\).", r"c) Generating fraction of \(5\dc\overline{4}\), \(\ 0\dc\overline{27}\) and \(\ 0\dc1\overline{6}\).")),
  ('★★★', L(r"d) Calcula \(1\dc\overline{3}\cdot0\dc75\) passant-ho tot a fracció.", r"d) Calcula \(1\dc\overline{3}\cdot0\dc75\) pasándolo todo a fracción.", r"d) Work out \(1\dc\overline{3}\cdot0\dc75\) by turning everything into fractions."))],
  P(r"a) \(\frac{4}{5}\), \(\frac{1}{4}\), \(\frac{26}{25}\). &nbsp; b) \(0\dc375\), \(0\dc\overline{6}\). &nbsp; c) \(\frac{49}{9}\), \(\frac{3}{11}\), \(\frac{1}{6}\). &nbsp; d) \(\frac{4}{3}\cdot\frac{3}{4}=1\).",
    r"a) \(\frac{4}{5}\), \(\frac{1}{4}\), \(\frac{26}{25}\). &nbsp; b) \(0\dc375\), \(0\dc\overline{6}\). &nbsp; c) \(\frac{49}{9}\), \(\frac{3}{11}\), \(\frac{1}{6}\). &nbsp; d) \(\frac{4}{3}\cdot\frac{3}{4}=1\).",
    r"a) \(\frac{4}{5}\), \(\frac{1}{4}\), \(\frac{26}{25}\). &nbsp; b) \(0\dc375\), \(0\dc\overline{6}\). &nbsp; c) \(\frac{49}{9}\), \(\frac{3}{11}\), \(\frac{1}{6}\). &nbsp; d) \(\frac{4}{3}\cdot\frac{3}{4}=1\)."))
ck(Fr('1.04'), Fr(26, 25)); ck(gen(5, '', '4'), Fr(49, 9)); ck(gen(0, '', '27'), Fr(3, 11)); ck(gen(0, '1', '6'), Fr(1, 6)); ck(gen(1, '', '3') * Fr('0.75'), 1)

# ============================================================ 2.7
s7 = box('def', L('Suma i resta de fraccions', 'Suma y resta de fracciones', 'Adding and subtracting fractions'),
  ul(L(r"Amb el <strong>mateix denominador</strong>, sumem o restem els numeradors i deixem el denominador: \(\ \frac{4}{7}+\frac{8}{7}=\frac{12}{7}\).", r"Con el <strong>mismo denominador</strong>, sumamos o restamos los numeradores y dejamos el denominador: \(\ \frac{4}{7}+\frac{8}{7}=\frac{12}{7}\).", r"With the <strong>same denominator</strong>, add or subtract the numerators and keep the denominator: \(\ \frac{4}{7}+\frac{8}{7}=\frac{12}{7}\)."),
     L(r"Amb <strong>denominadors diferents</strong>, primer les reduïm a comú denominador amb el \(\text{" + MCM + r"}\):", r"Con <strong>denominadores distintos</strong>, primero las reducimos a común denominador con el \(\text{" + MCM + r"}\):", r"With <strong>different denominators</strong>, first give them a common denominator using the \(\text{" + MCM + r"}\):"))
  + r'\[\frac{5}{6}-\frac{3}{4}+\frac{1}{3}=\frac{10}{12}-\frac{9}{12}+\frac{4}{12}=\frac{10-9+4}{12}=\frac{5}{12}\]'
  + ul(L(r"Un enter és una fracció de denominador 1: \(\ 2-\frac{3}{5}=\frac{10}{5}-\frac{3}{5}=\frac{7}{5}\).", r"Un entero es una fracción de denominador 1: \(\ 2-\frac{3}{5}=\frac{10}{5}-\frac{3}{5}=\frac{7}{5}\).", r"A whole number is a fraction with denominator 1: \(\ 2-\frac{3}{5}=\frac{10}{5}-\frac{3}{5}=\frac{7}{5}\)."),
       L(r"Els signes funcionen com amb els enters: \(\ -\frac{1}{2}-\frac{1}{3}=-\frac{3}{6}-\frac{2}{6}=-\frac{5}{6}\).", r"Los signos funcionan como con los enteros: \(\ -\frac{1}{2}-\frac{1}{3}=-\frac{3}{6}-\frac{2}{6}=-\frac{5}{6}\).", r"Signs work as with integers: \(\ -\frac{1}{2}-\frac{1}{3}=-\frac{3}{6}-\frac{2}{6}=-\frac{5}{6}\)."))
  + note(r"Error típic: \(\frac{2}{3}+\frac{1}{5}\neq\frac{3}{8}\). Mai no sumem els denominadors!", r"Error típico: \(\frac{2}{3}+\frac{1}{5}\neq\frac{3}{8}\). ¡Nunca sumamos los denominadores!", r"Common mistake: \(\frac{2}{3}+\frac{1}{5}\neq\frac{3}{8}\). Never add the denominators!", '⚠️'))
ck(Fr(5, 6) - Fr(3, 4) + Fr(1, 3), Fr(5, 12)); ck(2 - Fr(3, 5), Fr(7, 5)); ck(-Fr(1, 2) - Fr(1, 3), Fr(-5, 6))
s7 += ops([("+", "+"), ("-", "−")], "+", "2", "3", "1", "5", [("2,3,1,5", "2/3 + 1/5"), ("4,7,8,7", "4/7 + 8/7"), ("3,4,5,6", "3/4 − 5/6"), ("5,2,1,8", "5/2 − 1/8"), ("14,15,2,3", "14/15 − 2/3"), ("7,12,5,18", "7/12 + 5/18")],
          L("Suma i resta de dues fraccions", "Suma y resta de dos fracciones", "Adding and subtracting two fractions"))
s7 += drill('sum', 'Entrena: suma i resta', 'Entrena: suma y resta', 'Train: add and subtract')
s7 += level(1, 1,
  prob(L(r"Calcula i simplifica: a) \(\frac{7}{12}+\frac{5}{18}\) &nbsp; b) \(3-\frac{5}{4}\)", r"Calcula y simplifica: a) \(\frac{7}{12}+\frac{5}{18}\) &nbsp; b) \(3-\frac{5}{4}\)", r"Work out and simplify: a) \(\frac{7}{12}+\frac{5}{18}\) &nbsp; b) \(3-\frac{5}{4}\)"),
       r'\[\text{a) }\text{' + MCM + r'}(12,18)=36:\quad\frac{21}{36}+\frac{10}{36}=\boxed{\frac{31}{36}}\qquad\text{b) }\frac{12}{4}-\frac{5}{4}=\boxed{\frac{7}{4}}\]'))
ck(Fr(7, 12) + Fr(5, 18), Fr(31, 36)); ck(3 - Fr(5, 4), Fr(7, 4))
s7 += level(2, 2,
  prob(L(r"Calcula: \(\ \frac{2}{5}-\left(\frac{1}{2}-\frac{3}{4}\right)-1\)", r"Calcula: \(\ \frac{2}{5}-\left(\frac{1}{2}-\frac{3}{4}\right)-1\)", r"Work out: \(\ \frac{2}{5}-\left(\frac{1}{2}-\frac{3}{4}\right)-1\)"),
       P(r"Primer el parèntesi: \(\frac{1}{2}-\frac{3}{4}=\frac{2}{4}-\frac{3}{4}=-\frac{1}{4}\). Restar un negatiu és sumar:", r"Primero el paréntesis: \(\frac{1}{2}-\frac{3}{4}=\frac{2}{4}-\frac{3}{4}=-\frac{1}{4}\). Restar un negativo es sumar:", r"Brackets first: \(\frac{1}{2}-\frac{3}{4}=\frac{2}{4}-\frac{3}{4}=-\frac{1}{4}\). Subtracting a negative means adding:"),
       r'\[\frac{2}{5}+\frac{1}{4}-1=\frac{8}{20}+\frac{5}{20}-\frac{20}{20}=\boxed{-\frac{7}{20}}\]'))
ck(Fr(2, 5) - (Fr(1, 2) - Fr(3, 4)) - 1, Fr(-7, 20))
s7 += level(3, 3,
  prob(L(r"Quina fracció cal sumar a \(\frac{3}{8}\) per a obtindre \(\frac{5}{6}\)? I quina cal restar a \(\frac{1}{4}\) per a obtindre \(-\frac{2}{3}\)?", r"¿Qué fracción hay que sumar a \(\frac{3}{8}\) para obtener \(\frac{5}{6}\)? ¿Y cuál hay que restar a \(\frac{1}{4}\) para obtener \(-\frac{2}{3}\)?", r"What must be added to \(\frac{3}{8}\) to get \(\frac{5}{6}\)? And what must be subtracted from \(\frac{1}{4}\) to get \(-\frac{2}{3}\)?"),
       r'\[\frac{5}{6}-\frac{3}{8}=\frac{20}{24}-\frac{9}{24}=\boxed{\frac{11}{24}}\qquad \frac{1}{4}-\left(-\frac{2}{3}\right)=\frac{3}{12}+\frac{8}{12}=\boxed{\frac{11}{12}}\]'))
ck(Fr(5, 6) - Fr(3, 8), Fr(11, 24)); ck(Fr(1, 4) - Fr(11, 12), Fr(-2, 3))
s7 += practice([
  ('★', L(r"a) \(\frac{3}{10}+\frac{2}{5}\) &nbsp; b) \(\frac{5}{6}-\frac{1}{4}\) &nbsp; c) \(1+\frac{2}{7}\)", r"a) \(\frac{3}{10}+\frac{2}{5}\) &nbsp; b) \(\frac{5}{6}-\frac{1}{4}\) &nbsp; c) \(1+\frac{2}{7}\)", r"a) \(\frac{3}{10}+\frac{2}{5}\) &nbsp; b) \(\frac{5}{6}-\frac{1}{4}\) &nbsp; c) \(1+\frac{2}{7}\)")),
  ('★★', L(r"d) \(\frac{1}{2}-\frac{2}{3}+\frac{1}{6}\) &nbsp; e) \(-\frac{3}{4}-\frac{1}{6}+2\)", r"d) \(\frac{1}{2}-\frac{2}{3}+\frac{1}{6}\) &nbsp; e) \(-\frac{3}{4}-\frac{1}{6}+2\)", r"d) \(\frac{1}{2}-\frac{2}{3}+\frac{1}{6}\) &nbsp; e) \(-\frac{3}{4}-\frac{1}{6}+2\)")),
  ('★★★', L(r"f) \(\frac{2}{3}-\left[\frac{1}{4}-\left(\frac{5}{6}-1\right)\right]\)", r"f) \(\frac{2}{3}-\left[\frac{1}{4}-\left(\frac{5}{6}-1\right)\right]\)", r"f) \(\frac{2}{3}-\left[\frac{1}{4}-\left(\frac{5}{6}-1\right)\right]\)"))],
  P(r"a) \(\frac{7}{10}\) &nbsp; b) \(\frac{7}{12}\) &nbsp; c) \(\frac{9}{7}\) &nbsp; d) \(0\) &nbsp; e) \(\frac{13}{12}\) &nbsp; f) \(\frac{2}{3}-\frac{5}{12}=\frac{1}{4}\)",
    r"a) \(\frac{7}{10}\) &nbsp; b) \(\frac{7}{12}\) &nbsp; c) \(\frac{9}{7}\) &nbsp; d) \(0\) &nbsp; e) \(\frac{13}{12}\) &nbsp; f) \(\frac{2}{3}-\frac{5}{12}=\frac{1}{4}\)",
    r"a) \(\frac{7}{10}\) &nbsp; b) \(\frac{7}{12}\) &nbsp; c) \(\frac{9}{7}\) &nbsp; d) \(0\) &nbsp; e) \(\frac{13}{12}\) &nbsp; f) \(\frac{2}{3}-\frac{5}{12}=\frac{1}{4}\)"))
ck(Fr(3, 10) + Fr(2, 5), Fr(7, 10)); ck(Fr(5, 6) - Fr(1, 4), Fr(7, 12)); ck(Fr(1, 2) - Fr(2, 3) + Fr(1, 6), 0); ck(-Fr(3, 4) - Fr(1, 6) + 2, Fr(13, 12))
ck(Fr(1, 4) - (Fr(5, 6) - 1), Fr(5, 12)); ck(Fr(2, 3) - Fr(5, 12), Fr(1, 4))

# ============================================================ 2.8
s8 = box('def', L('Multiplicació i divisió de fraccions', 'Multiplicación y división de fracciones', 'Multiplying and dividing fractions'),
  ul(L(r"<strong>Multiplicació</strong>: multipliquem els numeradors entre si i els denominadors entre si. \(\ \frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}\qquad \frac{4}{9}\cdot\frac{3}{8}=\frac{12}{72}=\frac{1}{6}\)",
         r"<strong>Multiplicación</strong>: multiplicamos los numeradores entre sí y los denominadores entre sí. \(\ \frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}\qquad \frac{4}{9}\cdot\frac{3}{8}=\frac{12}{72}=\frac{1}{6}\)",
         r"<strong>Multiplying</strong>: multiply numerators together and denominators together. \(\ \frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}\qquad \frac{4}{9}\cdot\frac{3}{8}=\frac{12}{72}=\frac{1}{6}\)"),
     L(r"La <strong>inversa</strong> de \(\frac{a}{b}\) és \(\frac{b}{a}\): el seu producte és 1. La inversa de \(\frac{2}{5}\) és \(\frac{5}{2}\); la de \(-3\), \(-\frac{1}{3}\). El 0 no té inversa.", r"La <strong>inversa</strong> de \(\frac{a}{b}\) es \(\frac{b}{a}\): su producto es 1. La inversa de \(\frac{2}{5}\) es \(\frac{5}{2}\); la de \(-3\), \(-\frac{1}{3}\). El 0 no tiene inversa.", r"The <strong>reciprocal</strong> of \(\frac{a}{b}\) is \(\frac{b}{a}\): their product is 1. The reciprocal of \(\frac{2}{5}\) is \(\frac{5}{2}\); of \(-3\), \(-\frac{1}{3}\). 0 has no reciprocal."),
     L(r"<strong>Divisió</strong>: multipliquem la primera per la <strong>inversa</strong> de la segona (o, el que és el mateix, fem els <strong>productes creuats</strong>). \(\ \frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}\qquad \frac{2}{5}:\frac{4}{15}=\frac{2\cdot15}{5\cdot4}=\frac{30}{20}=\frac{3}{2}\)",
       r"<strong>División</strong>: multiplicamos la primera por la <strong>inversa</strong> de la segunda (o, lo que es lo mismo, hacemos los <strong>productos cruzados</strong>). \(\ \frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}\qquad \frac{2}{5}:\frac{4}{15}=\frac{2\cdot15}{5\cdot4}=\frac{30}{20}=\frac{3}{2}\)",
       r"<strong>Dividing</strong>: multiply the first by the <strong>reciprocal</strong> of the second (that is, use <strong>cross products</strong>). \(\ \frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}\qquad \frac{2}{5}:\frac{4}{15}=\frac{2\cdot15}{5\cdot4}=\frac{30}{20}=\frac{3}{2}\)"),
     L(r"Els signes segueixen la regla dels enters: \(\ \left(-\frac{3}{4}\right)\cdot\frac{2}{9}=-\frac{6}{36}=-\frac{1}{6}\).", r"Los signos siguen la regla de los enteros: \(\ \left(-\frac{3}{4}\right)\cdot\frac{2}{9}=-\frac{6}{36}=-\frac{1}{6}\).", r"Signs follow the integer rule: \(\ \left(-\frac{3}{4}\right)\cdot\frac{2}{9}=-\frac{6}{36}=-\frac{1}{6}\).")))
ck(Fr(4, 9) * Fr(3, 8), Fr(1, 6)); ck(Fr(2, 5) / Fr(4, 15), Fr(3, 2)); ck(Fr(-3, 4) * Fr(2, 9), Fr(-1, 6))
s8 += box('prop', L('Truc: simplifica abans de multiplicar', 'Truco: simplifica antes de multiplicar', 'Tip: simplify before multiplying'),
  P(r"Descompon i ratlla els factors comuns de dalt i de baix. Els números no es fan grans:", r"Descompón y tacha los factores comunes de arriba y de abajo. Los números no se hacen grandes:", r"Break into factors and cancel the common ones top and bottom. The numbers stay small:")
  + r'\[\frac{14}{15}\cdot\frac{25}{21}=\frac{2\cdot\cancel{7}\cdot5\cdot\cancel{5}}{3\cdot\cancel{5}\cdot3\cdot\cancel{7}}=\frac{10}{9}\]')
ck(Fr(14, 15) * Fr(25, 21), Fr(10, 9))
s8 += ops([("·", "·"), (":", ":")], "·", "4", "9", "3", "8", [("4,9,3,8", "4/9 · 3/8"), ("14,15,25,21", "14/15 · 25/21"), ("2,5,4,15", "2/5 : 4/15"), ("5,4,2,1", "5/4 : 2"), ("3,1,1,4", "3 : 1/4"), ("2,3,3,4", "2/3 · 3/4")],
          L("Multiplicació i divisió de dues fraccions", "Multiplicación y división de dos fracciones", "Multiplying and dividing two fractions"))
s8 += drill('mul', 'Entrena: multiplica i divideix', 'Entrena: multiplica y divide', 'Train: multiply and divide')
s8 += level(1, 1,
  prob(L(r"Calcula i simplifica: a) \(\frac{6}{4}\cdot\frac{2}{5}\) &nbsp; b) \(\frac{4}{3}:\frac{5}{6}\) &nbsp; c) \(\frac{3}{7}\cdot14\)", r"Calcula y simplifica: a) \(\frac{6}{4}\cdot\frac{2}{5}\) &nbsp; b) \(\frac{4}{3}:\frac{5}{6}\) &nbsp; c) \(\frac{3}{7}\cdot14\)", r"Work out and simplify: a) \(\frac{6}{4}\cdot\frac{2}{5}\) &nbsp; b) \(\frac{4}{3}:\frac{5}{6}\) &nbsp; c) \(\frac{3}{7}\cdot14\)"),
       r'\[\text{a) }\frac{12}{20}=\boxed{\frac{3}{5}}\qquad\text{b) }\frac{4\cdot6}{3\cdot5}=\frac{24}{15}=\boxed{\frac{8}{5}}\qquad\text{c) }\frac{42}{7}=\boxed{6}\]'))
ck(Fr(6, 4) * Fr(2, 5), Fr(3, 5)); ck(Fr(4, 3) / Fr(5, 6), Fr(8, 5)); ck(Fr(3, 7) * 14, 6)
s8 += level(2, 2,
  prob(L(r"Calcula: a) \(\left(-\frac{5}{6}\right):\frac{10}{9}\) &nbsp; b) \(\frac{2}{3}\ \tri{de}{de}{of}\ \frac{9}{10}\) &nbsp; c) \(\frac{\frac{3}{4}}{\frac{9}{2}}\)", r"Calcula: a) \(\left(-\frac{5}{6}\right):\frac{10}{9}\) &nbsp; b) \(\frac{2}{3}\ \tri{de}{de}{of}\ \frac{9}{10}\) &nbsp; c) \(\frac{\frac{3}{4}}{\frac{9}{2}}\)", r"Work out: a) \(\left(-\frac{5}{6}\right):\frac{10}{9}\) &nbsp; b) \(\frac{2}{3}\ \text{of}\ \frac{9}{10}\) &nbsp; c) \(\frac{\frac{3}{4}}{\frac{9}{2}}\)"),
       r'\[\text{a) }-\frac{5\cdot9}{6\cdot10}=-\frac{45}{60}=\boxed{-\frac{3}{4}}\qquad\text{b) }\frac{2}{3}\cdot\frac{9}{10}=\frac{18}{30}=\boxed{\frac{3}{5}}\]',
       P(r"c) Una fracció de fraccions és una divisió: «extrems per extrems i mitjans per mitjans».", r"c) Una fracción de fracciones es una división: «extremos por extremos y medios por medios».", r"c) A fraction of fractions is a division: “outer times outer over inner times inner”.") + r'\[\frac{3}{4}:\frac{9}{2}=\frac{3\cdot2}{4\cdot9}=\frac{6}{36}=\boxed{\frac{1}{6}}\]'))
ck(Fr(-5, 6) / Fr(10, 9), Fr(-3, 4)); ck(Fr(2, 3) * Fr(9, 10), Fr(3, 5)); ck(Fr(3, 4) / Fr(9, 2), Fr(1, 6))
s8 += level(3, 3,
  prob(L(r"Per quina fracció cal multiplicar \(\frac{4}{9}\) per a obtindre \(\frac{2}{3}\)? Entre quina fracció cal dividir \(\frac{5}{8}\) per a obtindre 5?", r"¿Por qué fracción hay que multiplicar \(\frac{4}{9}\) para obtener \(\frac{2}{3}\)? ¿Entre qué fracción hay que dividir \(\frac{5}{8}\) para obtener 5?", r"What must \(\frac{4}{9}\) be multiplied by to get \(\frac{2}{3}\)? What must \(\frac{5}{8}\) be divided by to get 5?"),
       r'\[\frac{2}{3}:\frac{4}{9}=\frac{18}{12}=\boxed{\frac{3}{2}}\qquad \frac{5}{8}:5=\frac{5}{40}=\boxed{\frac{1}{8}}\]',
       P(r"Comprovació: \(\frac{4}{9}\cdot\frac{3}{2}=\frac{12}{18}=\frac{2}{3}\) &nbsp; i &nbsp; \(\frac{5}{8}:\frac{1}{8}=\frac{40}{8}=5\). ✓", r"Comprobación: \(\frac{4}{9}\cdot\frac{3}{2}=\frac{12}{18}=\frac{2}{3}\) &nbsp; y &nbsp; \(\frac{5}{8}:\frac{1}{8}=\frac{40}{8}=5\). ✓", r"Check: \(\frac{4}{9}\cdot\frac{3}{2}=\frac{12}{18}=\frac{2}{3}\) &nbsp; and &nbsp; \(\frac{5}{8}:\frac{1}{8}=\frac{40}{8}=5\). ✓")))
ck(Fr(4, 9) * Fr(3, 2), Fr(2, 3)); ck(Fr(5, 8) / Fr(1, 8), 5)
s8 += practice([
  ('★', L(r"a) \(\frac{2}{3}\cdot\frac{5}{7}\) &nbsp; b) \(\frac{3}{5}:\frac{9}{10}\) &nbsp; c) Inversa de \(-\frac{7}{4}\)", r"a) \(\frac{2}{3}\cdot\frac{5}{7}\) &nbsp; b) \(\frac{3}{5}:\frac{9}{10}\) &nbsp; c) Inversa de \(-\frac{7}{4}\)", r"a) \(\frac{2}{3}\cdot\frac{5}{7}\) &nbsp; b) \(\frac{3}{5}:\frac{9}{10}\) &nbsp; c) Reciprocal of \(-\frac{7}{4}\)")),
  ('★★', L(r"d) \(\left(-\frac{8}{15}\right)\cdot\left(-\frac{25}{12}\right)\) &nbsp; e) \(6:\frac{3}{4}\) &nbsp; f) \(\frac{7}{10}:(-14)\)", r"d) \(\left(-\frac{8}{15}\right)\cdot\left(-\frac{25}{12}\right)\) &nbsp; e) \(6:\frac{3}{4}\) &nbsp; f) \(\frac{7}{10}:(-14)\)", r"d) \(\left(-\frac{8}{15}\right)\cdot\left(-\frac{25}{12}\right)\) &nbsp; e) \(6:\frac{3}{4}\) &nbsp; f) \(\frac{7}{10}:(-14)\)")),
  ('★★★', L(r"g) \(\frac{3}{4}\cdot\frac{8}{9}:\frac{2}{3}\) &nbsp; h) \(\frac{2}{5}:\left(\frac{4}{5}\cdot\frac{3}{8}\right)\)", r"g) \(\frac{3}{4}\cdot\frac{8}{9}:\frac{2}{3}\) &nbsp; h) \(\frac{2}{5}:\left(\frac{4}{5}\cdot\frac{3}{8}\right)\)", r"g) \(\frac{3}{4}\cdot\frac{8}{9}:\frac{2}{3}\) &nbsp; h) \(\frac{2}{5}:\left(\frac{4}{5}\cdot\frac{3}{8}\right)\)"))],
  P(r"a) \(\frac{10}{21}\) &nbsp; b) \(\frac{2}{3}\) &nbsp; c) \(-\frac{4}{7}\) &nbsp; d) \(\frac{10}{9}\) &nbsp; e) \(8\) &nbsp; f) \(-\frac{1}{20}\) &nbsp; g) \(\frac{2}{3}:\frac{2}{3}=1\) &nbsp; h) \(\frac{2}{5}:\frac{3}{10}=\frac{4}{3}\)",
    r"a) \(\frac{10}{21}\) &nbsp; b) \(\frac{2}{3}\) &nbsp; c) \(-\frac{4}{7}\) &nbsp; d) \(\frac{10}{9}\) &nbsp; e) \(8\) &nbsp; f) \(-\frac{1}{20}\) &nbsp; g) \(\frac{2}{3}:\frac{2}{3}=1\) &nbsp; h) \(\frac{2}{5}:\frac{3}{10}=\frac{4}{3}\)",
    r"a) \(\frac{10}{21}\) &nbsp; b) \(\frac{2}{3}\) &nbsp; c) \(-\frac{4}{7}\) &nbsp; d) \(\frac{10}{9}\) &nbsp; e) \(8\) &nbsp; f) \(-\frac{1}{20}\) &nbsp; g) \(\frac{2}{3}:\frac{2}{3}=1\) &nbsp; h) \(\frac{2}{5}:\frac{3}{10}=\frac{4}{3}\)"))
ck(Fr(2, 3) * Fr(5, 7), Fr(10, 21)); ck(Fr(3, 5) / Fr(9, 10), Fr(2, 3)); ck(Fr(-8, 15) * Fr(-25, 12), Fr(10, 9)); ck(6 / Fr(3, 4), 8); ck(Fr(7, 10) / -14, Fr(-1, 20))
ck(Fr(3, 4) * Fr(8, 9) / Fr(2, 3), 1); ck(Fr(2, 5) / (Fr(4, 5) * Fr(3, 8)), Fr(4, 3))
