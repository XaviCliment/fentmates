# Exercicis de la fitxa de 2n ESO, Unitat 1: Nombres naturals i enters.
# Una sola llista per a les dues llengües: genera.py (valencià) i genera-es.py (castellà) criden seccions('va'|'es').
# Cada exercici és (estrelles, enunciat, solució). Els resultats es calculen o es comproven ací mateix.
import re
from math import gcd, isqrt
from fractions import Fraction

# ---------- utilitats ----------
def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

def ev(e):
    """Avalua una expressió escrita amb - · : ^ √ ( ) [ ] i comprova que el resultat és enter."""
    s = e.replace('·', '*').replace(':', '/').replace('[', '(').replace(']', ')').replace('^', '**')
    s = re.sub(r'√(\d+)', r'R(\1)', s).replace('√(', 'R(')
    s = re.sub(r'(?<![\w.])(\d+)', r'F(\1)', s)
    def R(x):
        r = isqrt(int(x)); assert r * r == x, e; return F(r)
    F = Fraction
    v = eval(s, {'F': F, 'R': R})
    assert v.denominator == 1, e
    return int(v)
def tx(e):
    e = re.sub(r'√\(([^()]*)\)', r'\\sqrt{\1}', e)
    e = re.sub(r'√(\d+)', r'\\sqrt{\1}', e)
    e = re.sub(r'\^(\d+)', r'^{\1}', e)
    return e.replace('·', r'\cdot ').replace('[', r'\left[').replace(']', r'\right]')
def m(e): return '$' + tx(e) + '$'
def rsol(e): return '$' + tx(e) + r'=\res{%d}$' % ev(e)
def steps(e, *mid):
    """e = pas1 = pas2 = … = \\res{resultat}; comprova que cada pas val el mateix que e."""
    v = ev(e)
    for p in mid: assert ev(p) == v, (e, p, ev(p), v)
    return '$' + '='.join(tx(x) for x in (e,) + mid) + r'=\res{%d}$' % v
def lcm(*a):
    r = 1
    for x in a: r = r * x // gcd(r, x)
    return r
def mcd(*a):
    r = 0
    for x in a: r = gcd(r, x)
    return r
def fac(n):
    f, p = [], 2
    while p * p <= n:
        e = 0
        while n % p == 0: n //= p; e += 1
        if e: f.append((p, e))
        p += 1
    if n > 1: f.append((n, 1))
    return f
def ftex(n): return r'\cdot '.join(str(p) if e == 1 else '%d^{%d}' % (p, e) for p, e in fac(n))
def divs(n): return [d for d in range(1, n + 1) if n % d == 0]

def seccions(lang):
    def t(va, es): return va if lang == 'va' else es
    S = []

    # =====================================================================
    S.append((t('Els nombres naturals', 'Los números naturales'), [
     (1, t(r"Calcula el quocient i el residu de cada divisió i fes la prova ($D=d\cdot q+r$):", r"Calcula el cociente y el resto de cada división y haz la prueba ($D=d\cdot q+r$):")
         + tasks(4, [m('247:12'), m('1000:37'), m('505:5'), m('89:90')]),
         tasks(2, [r'$247=12\cdot\res{20}+\res{7}$', r'$1000=37\cdot\res{27}+\res{1}$', r'$505=5\cdot\res{101}+\res{0}$ ' + t('(exacta)', '(exacta)'), r'$89=90\cdot\res{0}+\res{89}$'])),
     (1, t(r"Indica si el resultat és un nombre natural. Si no ho és, explica per què:", r"Indica si el resultado es un número natural. Si no lo es, explica por qué:")
         + tasks(5, [m('7-12'), m('15·4'), m('20:6'), m('6:3+1'), m('3-3')]),
         tasks(1, [t(r'$7-12=-5$: \res{no} és natural (és negatiu).', r'$7-12=-5$: \res{no} es natural (es negativo).'), r'$15\cdot4=\res{60}$: ' + t('sí.', 'sí.'),
                   t(r'$20:6$ \res{no} és exacta ($20=6\cdot3+2$).', r'$20:6$ \res{no} es exacta ($20=6\cdot3+2$).'), r'$6:3+1=\res{3}$: ' + t('sí.', 'sí.'), r'$3-3=\res{0}$: ' + t('sí (el 0 és natural).', 'sí (el 0 es natural).')])),
     (2, t(r"En una divisió el divisor és 15, el quocient 23 i el residu 9. Quin és el dividend? Podria ser 17 el residu d'aquesta divisió?", r"En una división el divisor es 15, el cociente 23 y el resto 9. ¿Cuál es el dividendo? ¿Podría ser 17 el resto de esta división?"),
         r'$D=15\cdot23+9=\res{354}$. ' + t(r'El residu \res{no} pot ser 17, perquè ha de ser menor que el divisor (15).', r'El resto \res{no} puede ser 17, porque tiene que ser menor que el divisor (15).')),
     (2, t(r"Calcula de cap aplicant la propietat distributiva:", r"Calcula mentalmente aplicando la propiedad distributiva:")
         + tasks(4, [m('7·99'), m('12·15+12·5'), m('35·102'), m('8·(10+5)')]),
         tasks(2, [steps('7·99', '7·100-7'), steps('12·15+12·5', '12·20'), steps('35·102', '35·100+35·2'), steps('8·(10+5)', '80+40')])),
    ]))
    assert 12 * 20 + 7 == 247 and 37 * 27 + 1 == 1000 and 15 * 23 + 9 == 354

    # =====================================================================
    D = [24, 36, 45, 60, 17]
    S.append((t('Múltiples i divisors', 'Múltiplos y divisores'), [
     (1, t(r"Escriu els cinc primers múltiples no nuls de:", r"Escribe los cinco primeros múltiplos no nulos de:") + tasks(3, ['$7$', '$12$', '$15$']),
         tasks(3, ['$' + ',\\ '.join(str(k * i) for i in range(1, 6)) + '$' for k in (7, 12, 15)])),
     (1, t(r"Escriu tots els divisors de:", r"Escribe todos los divisores de:") + tasks(5, ['$%d$' % n for n in D]),
         tasks(1, [r'$\text{Div}(%d)=\{\res{%s}\}$' % (n, ',\\ '.join(map(str, divs(n)))) for n in D])),
     (2, t(r"Digues si són vertaderes o falses i justifica-ho:", r"Di si son verdaderas o falsas y justifícalo:")
         + tasks(1, [t('48 és múltiple de 6.', '48 es múltiplo de 6.'), t('7 és divisor de 77.', '7 es divisor de 77.'), t('5 és múltiple de 15.', '5 es múltiplo de 15.'),
                     t('1 és divisor de qualsevol nombre.', '1 es divisor de cualquier número.'), t('0 és múltiple de 9.', '0 es múltiplo de 9.')]),
         tasks(1, [r'\res{V}: $48=6\cdot8$.', r'\res{V}: $77=7\cdot11$.', t(r'\res{F}: 5 és \emph{divisor} de 15.', r'\res{F}: 5 es \emph{divisor} de 15.'),
                   r'\res{V}: $n=1\cdot n$.', r'\res{V}: $0=9\cdot0$.'])),
    ]))

    # =====================================================================
    NUMS = [1320, 4455, 7125, 2002]
    def dv(n): return ', '.join(str(k) for k in (2, 3, 5, 9, 10, 11) if n % k == 0)
    PR = [31, 51, 57, 61, 87, 91, 97, 1]
    def cls(n):
        if n == 1: return t('ni primer ni compost', 'ni primo ni compuesto')
        f = fac(n)
        return t('primer', 'primo') if f == [(n, 1)] else t('compost', 'compuesto') + r': $%d=%s$' % (n, ftex(n))
    S.append((t('Criteris de divisibilitat. Nombres primers', 'Criterios de divisibilidad. Números primos'), [
     (2, t(r"Sense fer la divisió, indica per quins d'aquests nombres és divisible cadascun: 2, 3, 5, 9, 10 i 11.", r"Sin hacer la división, indica por cuáles de estos números es divisible cada uno: 2, 3, 5, 9, 10 y 11.")
         + tasks(4, ['$%d$' % n for n in NUMS])
         + recorda(t(r"Per l'11: resta la suma de les xifres de lloc senar i la de les de lloc parell; ha de donar 0 o un múltiple d'11.", r"Por el 11: resta la suma de las cifras de lugar impar y la de las de lugar par; tiene que dar 0 o un múltiplo de 11.")),
         tasks(2, [r'$%d$: \res{%s}' % (n, dv(n)) for n in NUMS])),
     (2, t(r"Quines xifres poden anar en el lloc de $\square$?", r"¿Qué cifras pueden ir en el lugar de $\square$?")
         + tasks(1, [t(r'$4\square7$ ha de ser múltiple de 3.', r'$4\square7$ tiene que ser múltiplo de 3.'), t(r'$23\square$ ha de ser múltiple de 2 i de 5.', r'$23\square$ tiene que ser múltiplo de 2 y de 5.'),
                     t(r'$5\square2$ ha de ser múltiple de 9.', r'$5\square2$ tiene que ser múltiplo de 9.')]),
         tasks(1, [r'$4+\square+7=11+\square\in\{12,15,18\}\Rightarrow\square=\res{1,\ 4,\ 7}$', t(r'Ha d\'acabar en 0: $\square=\res{0}$ (230).', r'Tiene que acabar en 0: $\square=\res{0}$ (230).'),
                   r'$5+\square+2=9\Rightarrow\square=\res{2}$ (522)'])),
     (1, t(r"Classifica en primers i compostos. Dels compostos, escriu-ne la descomposició:", r"Clasifica en primos y compuestos. De los compuestos, escribe su descomposición:")
         + tasks(8, ['$%d$' % n for n in PR]),
         tasks(2, [r'$%d$: \res{%s}' % (n, cls(n)) for n in PR])),
    ]))
    assert [x for x in range(4, 8)] and all((400 + 10 * d + 7) % 3 == 0 for d in (1, 4, 7)) and 522 % 9 == 0

    # =====================================================================
    FN = [60, 84, 126, 360, 1000, 1176]
    S.append((t('Descomposició en factors primers', 'Descomposición en factores primos'), [
     (1, t(r"Descompon en factors primers:", r"Descompón en factores primos:") + tasks(6, ['$%d$' % n for n in FN]),
         tasks(3, [r'$%d=\res{%s}$' % (n, ftex(n)) for n in FN])),
     (2, t(r"Quin nombre té cada descomposició?", r"¿Qué número tiene cada descomposición?") + tasks(3, [r'$2^3\cdot3\cdot5^2$', r'$2^2\cdot3^3$', r'$3\cdot5\cdot7\cdot11$']),
         tasks(3, [r'$\res{%d}$' % (2**3 * 3 * 25), r'$\res{%d}$' % (4 * 27), r'$\res{%d}$' % (3 * 5 * 7 * 11)])),
     (3, t(r"Per quin nombre, el més xicotet possible, cal multiplicar 72 perquè el resultat siga un quadrat perfecte? De quin nombre és el quadrat?", r"¿Por qué número, el más pequeño posible, hay que multiplicar 72 para que el resultado sea un cuadrado perfecto? ¿De qué número es el cuadrado?"),
         t(r'$72=2^3\cdot3^2$. Perquè tots els exponents siguen parells falta un 2: $72\cdot\res{2}=144=2^4\cdot3^2=\res{12}^2$.', r'$72=2^3\cdot3^2$. Para que todos los exponentes sean pares falta un 2: $72\cdot\res{2}=144=2^4\cdot3^2=\res{12}^2$.')),
    ]))
    assert ftex(72) == r'2^{3}\cdot 3^{2}' and isqrt(144) == 12

    # =====================================================================
    PAR = [(72, 60), (84, 126), (45, 60, 75), (140, 300), (16, 27)]
    def mm(a): return (r'$%s$: \quad ' % ',\\ '.join('%d=%s' % (x, ftex(x)) for x in a)
                       + r'$\text{mcm}=\res{%d}$,\ \ $\text{MCD}=\res{%d}$' % (lcm(*a), mcd(*a)))
    S.append((t('Mínim comú múltiple i màxim comú divisor', 'Mínimo común múltiplo y máximo común divisor'), [
     (1, t(r"Calcula llistant múltiples i divisors:", r"Calcula listando múltiplos y divisores:") + tasks(4, [r'$\text{mcm}(12,18)$', r'$\text{MCD}(12,18)$', r'$\text{mcm}(8,20)$', r'$\text{MCD}(8,20)$']),
         tasks(4, [r'$\res{%d}$' % lcm(12, 18), r'$\res{%d}$' % mcd(12, 18), r'$\res{%d}$' % lcm(8, 20), r'$\res{%d}$' % mcd(8, 20)])),
     (2, t(r"Calcula el mcm i el MCD descomponent en factors primers:", r"Calcula el mcm y el MCD descomponiendo en factores primos:")
         + tasks(3, [', '.join('$%d$' % x for x in a) for a in PAR])
         + recorda(t(r"\textbf{mcm}: factors comuns i no comuns amb el major exponent. \textbf{MCD}: només els comuns, amb el menor exponent.", r"\textbf{mcm}: factores comunes y no comunes con el mayor exponente. \textbf{MCD}: solo los comunes, con el menor exponente.")),
         tasks(1, [mm(a) for a in PAR])),
     (2, t(r"Comprova amb 72 i 60 que el producte del MCD pel mcm és igual al producte dels dos nombres.", r"Comprueba con 72 y 60 que el producto del MCD por el mcm es igual al producto de los dos números."),
         r'$\text{MCD}\cdot\text{mcm}=12\cdot360=\res{%d}$ \quad $72\cdot60=\res{%d}$ \ \checkmark' % (12 * 360, 72 * 60)),
     (3, t(r"El MCD de dos nombres és 6 i el mcm, 90. Si un dels nombres és 18, quin és l'altre?", r"El MCD de dos números es 6 y el mcm, 90. Si uno de los números es 18, ¿cuál es el otro?"),
         r'$18\cdot b=6\cdot90=540\Rightarrow b=540:18=\res{30}$. ' + t(r'Comprovació: $\text{MCD}(18,30)=6$ i $\text{mcm}(18,30)=90$.', r'Comprobación: $\text{MCD}(18,30)=6$ y $\text{mcm}(18,30)=90$.')),
     (2, t(r"Són primers entre si aquestes parelles de nombres?", r"¿Son primos entre sí estas parejas de números?") + tasks(3, ['$15$ i $28$'.replace(' i ', t(' i ', ' y ')), '$21$ i $35$'.replace(' i ', t(' i ', ' y ')), '$9$ i $16$'.replace(' i ', t(' i ', ' y '))]),
         tasks(3, [r'\res{%s} (MCD $=%d$)' % (t('Sí', 'Sí') if mcd(15, 28) == 1 else 'No', mcd(15, 28)), r'\res{No} (MCD $=%d$)' % mcd(21, 35), r'\res{%s} (MCD $=%d$)' % (t('Sí', 'Sí'), mcd(9, 16))])),
    ]))
    assert lcm(*PAR[0]) == 360 and mcd(18, 30) == 6 and lcm(18, 30) == 90 and mcd(21, 35) == 7

    # =====================================================================
    S.append((t('Problemes de mcm i MCD', 'Problemas de mcm y MCD'), [
     (2, t(r"Dues línies d'autobús ixen de la mateixa parada a les 7:00. La línia A hi passa cada 15 minuts i la B, cada 20 minuts. A quina hora tornaran a coincidir?", r"Dos líneas de autobús salen de la misma parada a las 7:00. La línea A pasa cada 15 minutos y la B, cada 20 minutos. ¿A qué hora volverán a coincidir?"),
         r'$\text{mcm}(15,20)=%d$ min $\Rightarrow$ \res{8:00}' % lcm(15, 20)),
     (2, t(r"Una floristeria té 60 roses i 84 clavells. Vol fer el major nombre possible de rams iguals sense que sobre cap flor. Quants rams farà? Quantes roses i quants clavells durà cada ram?", r"Una floristería tiene 60 rosas y 84 claveles. Quiere hacer el mayor número posible de ramos iguales sin que sobre ninguna flor. ¿Cuántos ramos hará? ¿Cuántas rosas y cuántos claveles llevará cada ramo?"),
         r'$\text{MCD}(60,84)=\res{%d}$ ' % mcd(60, 84) + t('rams', 'ramos') + r'; $60:12=\res{5}$ ' + t('roses i', 'rosas y') + r' $84:12=\res{7}$ ' + t('clavells cada ram.', 'claveles cada ramo.')),
     (2, t(r"Volem enrajolar el terra d'una habitació rectangular de 4,80 m × 3,60 m amb rajoles quadrades, les més grans possible i sense tallar-ne cap. Quant ha de mesurar el costat de cada rajola? Quantes rajoles calen?", r"Queremos embaldosar el suelo de una habitación rectangular de 4,80 m × 3,60 m con baldosas cuadradas, las mayores posibles y sin cortar ninguna. ¿Cuánto debe medir el lado de cada baldosa? ¿Cuántas baldosas hacen falta?"),
         r'$\text{MCD}(480,360)=\res{%d\text{ cm}}$; \quad $4\cdot3=\res{12}$ ' % mcd(480, 360) + t('rajoles.', 'baldosas.')),
     (2, t(r"Tres fars s'encenen cada 8, 12 i 18 segons, respectivament. Si ara s'acaben d'encendre alhora, quants segons passaran fins que tornen a encendre's junts?", r"Tres faros se encienden cada 8, 12 y 18 segundos, respectivamente. Si ahora se acaban de encender a la vez, ¿cuántos segundos pasarán hasta que vuelvan a encenderse juntos?"),
         r'$\text{mcm}(8,12,18)=2^3\cdot3^2=\res{%d\text{ s}}$' % lcm(8, 12, 18)),
     (2, t(r"Un magatzem té 150 llibres de matemàtiques i 210 de ciències. Es volen fer paquets iguals, amb el màxim nombre de llibres i amb un sol tipus de llibre en cada paquet. Quants llibres durà cada paquet? Quants paquets es faran?", r"Un almacén tiene 150 libros de matemáticas y 210 de ciencias. Se quieren hacer paquetes iguales, con el máximo número de libros y con un solo tipo de libro en cada paquete. ¿Cuántos libros llevará cada paquete? ¿Cuántos paquetes se harán?"),
         r'$\text{MCD}(150,210)=\res{%d}$ ' % mcd(150, 210) + t('llibres', 'libros') + r'; $5+7=\res{12}$ ' + t('paquets.', 'paquetes.')),
     (3, t(r"Si agrupem els caramels d'una bossa de 6 en 6, de 8 en 8 o de 10 en 10, sempre en sobren 3. Quants caramels hi ha, com a mínim, a la bossa (més de 3)?", r"Si agrupamos los caramelos de una bolsa de 6 en 6, de 8 en 8 o de 10 en 10, siempre sobran 3. ¿Cuántos caramelos hay, como mínimo, en la bolsa (más de 3)?"),
         r'$\text{mcm}(6,8,10)=%d$; \quad $120+3=\res{123}$ ' % lcm(6, 8, 10) + t('caramels.', 'caramelos.')),
     (3, t(r"Dues rodes dentades engranades tenen 24 i 36 dents. Quantes voltes ha de fer cadascuna perquè tornen a estar en la posició inicial?", r"Dos ruedas dentadas engranadas tienen 24 y 36 dientes. ¿Cuántas vueltas tiene que dar cada una para que vuelvan a estar en la posición inicial?"),
         r'$\text{mcm}(24,36)=%d$ ' % lcm(24, 36) + t('dents', 'dientes') + r': $72:24=\res{3}$ ' + t('voltes la primera i', 'vueltas la primera y') + r' $72:36=\res{2}$ ' + t('la segona.', 'la segunda.')),
    ]))
    assert mcd(480, 360) == 120 and 480 // 120 * (360 // 120) == 12 and mcd(150, 210) == 30 and lcm(6, 8, 10) == 120 and lcm(24, 36) == 72

    # =====================================================================
    REP = [(t('3 graus baix zero', '3 grados bajo cero'), '-3'), (t('el segon soterrani', 'el segundo sótano'), '-2'), (t('un deute de 50 €', 'una deuda de 50 €'), '-50'),
           (t("1200 m d'altitud", '1200 m de altitud'), '+1200'), (t("l'any 44 a. C.", 'el año 44 a. C.'), '-44'), (t('guanyar 15 €', 'ganar 15 €'), '+15')]
    ORD = [-3, 5, -8, 0, 2, -1, -12, 7]
    S.append((t('Els nombres enters', 'Los números enteros'), [
     (1, t(r"Expressa amb un nombre enter:", r"Expresa con un número entero:") + tasks(3, [x for x, _ in REP]),
         tasks(6, ['$\\res{%s}$' % v for _, v in REP])),
     (1, t(r"Escriu el valor absolut i l'oposat de:", r"Escribe el valor absoluto y el opuesto de:") + tasks(4, ['$-7$', '$12$', '$0$', '$-25$']),
         tasks(2, [r'$|-7|=\res{7}$, \ $\text{op}(-7)=\res{7}$', r'$|12|=\res{12}$, \ $\text{op}(12)=\res{-12}$', r'$|0|=\res{0}$, \ $\text{op}(0)=\res{0}$', r'$|-25|=\res{25}$, \ $\text{op}(-25)=\res{25}$'])),
     (1, t(r"Representa en la recta numèrica i ordena de menor a major:", r"Representa en la recta numérica y ordena de menor a mayor:") + r'\[' + ',\\quad '.join(map(str, ORD)) + r'\]',
         '$\\res{' + '<'.join(map(str, sorted(ORD))) + '}$'),
     (2, t(r"Escriu tots els nombres enters $x$ que compleixen:", r"Escribe todos los números enteros $x$ que cumplen:") + tasks(4, [r'$-4<x\le2$', r'$|x|<3$', r'$|x|=5$', r'$-2\le x<-1$']),
         tasks(2, [r'$\res{-3,-2,-1,0,1,2}$', r'$\res{-2,-1,0,1,2}$', r'$\res{-5,\ 5}$', r'$\res{-2}$'])),
     (2, t(r"Les temperatures mínimes d'una setmana han sigut: dilluns $-3$\,°C, dimarts $-5$\,°C, dimecres $1$\,°C, dijous $0$\,°C, divendres $-2$\,°C, dissabte $4$\,°C i diumenge $-1$\,°C. Quin dia va fer més fred? Ordena-les de menor a major. Quina diferència hi ha entre la més alta i la més baixa?",
           r"Las temperaturas mínimas de una semana han sido: lunes $-3$\,°C, martes $-5$\,°C, miércoles $1$\,°C, jueves $0$\,°C, viernes $-2$\,°C, sábado $4$\,°C y domingo $-1$\,°C. ¿Qué día hizo más frío? Ordénalas de menor a mayor. ¿Qué diferencia hay entre la más alta y la más baja?"),
         t(r'El \res{dimarts}.', r'El \res{martes}.') + r' $-5<-3<-2<-1<0<1<4$. \quad ' + steps('4-(-5)', '4+5') + r'\,°C'),
    ]))

    # =====================================================================
    SR = ['(-7)+(-5)', '(-9)+4', '12+(-15)', '(-6)-(-10)', '8-(+13)', '(-3)-5', '0-(-7)', '(-11)+11']
    SN = ['5-8+3-7+2', '-4-6+10-3', '12-15-9+20', '-1+2-3+4-5+6']
    PA = [('7-(3-5+2)', ['7-3+5-2']), ('-(4-9)+(-2+6)', ['5+4']), ('10-[3-(5-8)]', ['10-[3-(-3)]', '10-6']), ('-[-(2-7)-(-3+1)]', ['-[5-(-2)]', '-7'])]
    MD = ['(-6)·(-4)', '7·(-8)', '(-45):9', '(-56):(-7)', '0:(-5)', '(-2)·(-3)·(-5)', '(-1)·(-1)·(-1)·(-1)', '72:(-8)']
    MI = [(r'(-4)\cdot\square=28', -7, '(-4)·(-7)'), (r'\square:(-6)=5', -30, '(-30):(-6)'), (r'\square\cdot(-9)=-81', 9, '9·(-9)'),
          (r'(-48):\square=-12', 4, '(-48):4'), (r'(-5)+\square=-12', -7, '(-5)+(-7)'), (r'\square-8=-3', 5, '5-8')]
    MIV = [28, 5, -81, -12, -12, -3]
    for (_, _, e), v in zip(MI, MIV): assert ev(e) == v, e
    S.append((t('Operacions amb enters', 'Operaciones con enteros'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(4, [m(e) for e in SR]), tasks(4, [rsol(e) for e in SR])),
     (1, t(r"Calcula agrupant els positius i els negatius:", r"Calcula agrupando los positivos y los negativos:") + tasks(2, [m(e) for e in SN]),
         tasks(2, [steps('5-8+3-7+2', '(5+3+2)-(8+7)', '10-15'), steps('-4-6+10-3', '10-(4+6+3)', '10-13'), steps('12-15-9+20', '(12+20)-(15+9)', '32-24'), steps('-1+2-3+4-5+6', '(2+4+6)-(1+3+5)', '12-9')])),
     (2, t(r"Lleva els parèntesis i els claudàtors i calcula:", r"Quita los paréntesis y los corchetes y calcula:") + tasks(2, [m(e) for e, _ in PA])
         + recorda(t(r"Un parèntesi precedit d'un signe $-$ es lleva canviant el signe de tots els termes de dins.", r"Un paréntesis precedido de un signo $-$ se quita cambiando el signo de todos los términos de dentro.")),
         tasks(1, [steps(e, *p) for e, p in PA])),
     (1, t(r"Calcula aplicant la regla dels signes:", r"Calcula aplicando la regla de los signos:") + tasks(4, [m(e) for e in MD]), tasks(2, [rsol(e) for e in MD])),
     (2, t(r"Quin nombre falta en cada cas?", r"¿Qué número falta en cada caso?") + tasks(3, ['$' + q + '$' for q, _, _ in MI]),
         tasks(3, [r'$\square=\res{%d}$' % v for _, v, _ in MI])),
     (2, t(r"Un submarí està a 120 m de profunditat. Puja 45 m i després baixa 80 m. A quina profunditat es troba?", r"Un submarino está a 120 m de profundidad. Sube 45 m y después baja 80 m. ¿A qué profundidad se encuentra?"),
         steps('-120+45-80') + t(r': a \res{155 m} de profunditat.', r': a \res{155 m} de profundidad.')),
     (2, t(r"Pitàgores va nàixer l'any 570 a. C. i va morir l'any 495 a. C. Quants anys va viure?", r"Pitágoras nació en el año 570 a. C. y murió en el año 495 a. C. ¿Cuántos años vivió?"),
         steps('-495-(-570)', '-495+570') + t(r' anys.', r' años.')),
     (3, t(r"Un compte bancari té un saldo de 230 €. Es paguen tres rebuts de 85 € cadascun i, després, s'hi ingressen 120 €. Quin és el saldo final? Ha estat el compte en negatiu en algun moment?", r"Una cuenta bancaria tiene un saldo de 230 €. Se pagan tres recibos de 85 € cada uno y, después, se ingresan 120 €. ¿Cuál es el saldo final? ¿Ha estado la cuenta en negativo en algún momento?"),
         steps('230-3·85+120', '230-255+120') + r'\,€. ' + t(r'Sí: després dels rebuts, $230-255=\res{-25}$\,€.', r'Sí: después de los recibos, $230-255=\res{-25}$\,€.')),
    ]))

    # =====================================================================
    C1 = [('5-3·4', ['5-12']), ('(5-3)·4', ['2·4']), ('18:(-3)+2·(-5)', ['-6-10']), ('-20:4·(-2)', ['-5·(-2)']), ('3·(-2)-4·(-3)', ['-6+12'])]
    C2 = [('4-2·[3-(6-10)]', ['4-2·[3+4]', '4-14']), ('(-3)·(2-7)+15:(-5)', ['(-3)·(-5)-3', '15-3']), ('[(-8)+5]·[6-(-2)]', ['(-3)·8']),
          ('-6-[4-3·(2-5)]', ['-6-[4+9]', '-6-13']), ('25:(-5)-(-3)·(4-6):2', ['-5-(-3)·(-2):2', '-5-6:2', '-5-3'])]
    S.append((t('Operacions combinades', 'Operaciones combinadas'), [
     (1, t(r"Calcula respectant la jerarquia de les operacions:", r"Calcula respetando la jerarquía de las operaciones:") + tasks(3, [m(e) for e, _ in C1])
         + recorda(t(r"Primer, parèntesis; després, potències i arrels; després, multiplicacions i divisions (d'esquerra a dreta) i, al final, sumes i restes.", r"Primero, paréntesis; después, potencias y raíces; después, multiplicaciones y divisiones (de izquierda a derecha) y, al final, sumas y restas.")),
         tasks(2, [steps(e, *p) for e, p in C1])),
     (2, t(r"Calcula:", r"Calcula:") + tasks(2, [m(e) for e, _ in C2]), tasks(1, [steps(e, *p) for e, p in C2])),
     (3, t(r"Un alumne ha fet aquesta operació: \ $12-4:2\cdot(-3)=8:2\cdot(-3)=4\cdot(-3)=-12$. \ Explica quin error ha comés i calcula-la bé.", r"Un alumno ha hecho esta operación: \ $12-4:2\cdot(-3)=8:2\cdot(-3)=4\cdot(-3)=-12$. \ Explica qué error ha cometido y calcúlala bien."),
         t(r"Ha restat abans de dividir i multiplicar. ", r"Ha restado antes de dividir y multiplicar. ") + steps('12-4:2·(-3)', '12-2·(-3)', '12+6')),
     (3, t(r"Posa parèntesis perquè les igualtats siguen certes:", r"Pon paréntesis para que las igualdades sean ciertas:") + tasks(3, [r'$6-4\cdot3+2=10$', r'$6-4\cdot3+2=-14$', r'$-8:2-6=2$']),
         tasks(3, [steps('(6-4)·(3+2)'), steps('6-4·(3+2)'), steps('-8:(2-6)')])),
    ]))
    assert ev('(6-4)·(3+2)') == 10 and ev('6-4·(3+2)') == -14 and ev('-8:(2-6)') == 2 and ev('12-4:2·(-3)') == 18

    # =====================================================================
    PW = ['(-3)^4', '-3^4', '(-2)^5', '(-1)^100', '(-1)^25', '(-10)^3', '0^7', '(-7)^0']
    ON = [(r'(-2)^3\cdot(-2)^5', r'(-2)^{8}'), (r'(-5)^9:(-5)^6', r'(-5)^{3}'), (r'\left[(-3)^2\right]^4', r'(-3)^{8}'),
          (r'2^5\cdot(-3)^5', r'(-6)^{5}'), (r'(-12)^4:3^4', r'(-4)^{4}'), (r'7^3\cdot7^4:7^5', r'7^{2}')]
    PP = [(r'(-2)^7:(-2)^4', r'(-2)^3', -8), (r'\left[(-1)^3\right]^5\cdot(-1)^2', r'(-1)^{17}', -1), (r'5^4\cdot2^4', r'10^4', 10000), (r'(-6)^3:(-3)^3', r'2^3', 8)]
    assert (-2) ** 3 == -8 and (-1) ** 17 == -1 and 10 ** 4 == 10000 and (-6) ** 3 // (-3) ** 3 == 8
    C3 = [('(-2)^3+3^2', ['-8+9']), ('-2^4+(-2)^4', ['-16+16']), ('5-2·√36+(-1)^7', ['5-2·6-1', '5-12-1']), ('(-3)^2·2-√49:(-7)', ['9·2-7:(-7)', '18-(-1)']),
          ('[(-2)^2-3^2]^2:(-5)', ['[4-9]^2:(-5)', '25:(-5)']), ('√(25-9)-(-3)^3:9', ['√16-(-27):9', '4-(-3)'])]
    C4 = [('[(-2)^3-(-3)^2]:(-17)+√64·(-1)^5', ['-17:(-17)+8·(-1)', '1-8']),
          ('-3^2-[(-4)^2:(-2)^3-√81]·(-2)', ['-9-[16:(-8)-9]·(-2)', '-9-[-2-9]·(-2)', '-9-(-11)·(-2)', '-9-22']),
          ('√(5^2-3^2)·(-2)^3-[(-6)^2:(-3)^2-2^4]^2:(-9)', ['√16·(-8)-[36:9-16]^2:(-9)', '4·(-8)-(-12)^2:(-9)', '-32-144:(-9)', '-32+16']),
          ('[2^5:((-2)^2-12)-(-1)^20]·√49', ['[32:(4-12)-1]·7', '[32:(-8)-1]·7', '[-4-1]·7', '-5·7']),
          ('(-10)^3:(-5)^2+4·[√100-(-3)^3:(-9)]^2', ['-1000:25+4·[10-(-27):(-9)]^2', '-40+4·[10-3]^2', '-40+4·49', '-40+196'])]
    RE = [(50, 7, 1),(90, 9, 9), (130, 11, 9), (200, 14, 4)]
    for n, s, r in RE: assert isqrt(n) == s and n - s * s == r
    SG = [(r'(-7)^{12}', '+'), (r'(-3)^{15}', '-'), (r'-5^{4}', '-'), (r'-(-2)^{6}', '-'), (r'(-1)^{2026}', '+')]
    S.append((t('Potències i arrels amb enters', 'Potencias y raíces con enteros'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(4, [m(e) for e in PW])
         + recorda(t(r"Base negativa: exponent parell $\to$ resultat positiu; exponent senar $\to$ resultat negatiu. Compte: $-3^4=-(3^4)$, però $(-3)^4=(-3)\cdot(-3)\cdot(-3)\cdot(-3)$.", r"Base negativa: exponente par $\to$ resultado positivo; exponente impar $\to$ resultado negativo. Cuidado: $-3^4=-(3^4)$, pero $(-3)^4=(-3)\cdot(-3)\cdot(-3)\cdot(-3)$.")),
         tasks(4, [rsol(e) for e in PW])),
     (2, t(r"Sense fer el càlcul, digues quin signe té el resultat:", r"Sin hacer el cálculo, di qué signo tiene el resultado:") + tasks(5, ['$' + e + '$' for e, _ in SG]),
         tasks(5, [r'$\res{%s}$' % s for _, s in SG])),
     (2, t(r"Expressa com una sola potència:", r"Expresa como una sola potencia:") + tasks(3, ['$' + a + '$' for a, _ in ON]),
         tasks(3, ['$' + a + r'=\res{' + b + '}$' for a, b in ON])),
     (2, t(r"Calcula aplicant les propietats de les potències:", r"Calcula aplicando las propiedades de las potencias:") + tasks(4, ['$' + a + '$' for a, _, _ in PP]),
         tasks(2, ['$' + a + '=' + b + r'=\res{%d}$' % v for a, b, v in PP])),
     (1, t(r"Calcula les arrels quadrades (si existeixen):", r"Calcula las raíces cuadradas (si existen):") + tasks(6, [r'$\sqrt{81}$', r'$\sqrt{144}$', r'$\sqrt{-25}$', r'$\sqrt{0}$', r'$\sqrt{400}$', r'$\sqrt{-1}$']),
         tasks(3, [r'$\res{\pm9}$', r'$\res{\pm12}$', t(r'\res{No existeix}', r'\res{No existe}'), r'$\res{0}$', r'$\res{\pm20}$', t(r'\res{No existeix}', r'\res{No existe}')])),
     (2, t(r"Calcula l'arrel entera i el residu i fes la comprovació:", r"Calcula la raíz entera y el resto y haz la comprobación:") + tasks(4, [r'$\sqrt{%d}$' % n for n, _, _ in RE]),
         tasks(2, [r'$\sqrt{%d}\approx\res{%d}$, %s $\res{%d}$: \ $%d=%d^2+%d$' % (n, s, t('residu', 'resto'), r, n, s, r) for n, s, r in RE])),
     (2, t(r"Calcula:", r"Calcula:") + tasks(2, [m(e) for e, _ in C3]), tasks(2, [steps(e, *p) for e, p in C3])),
     (3, t(r"Calcula pas a pas, respectant la jerarquia de les operacions:", r"Calcula paso a paso, respetando la jerarquía de las operaciones:") + tasks(1, [m(e) for e, _ in C4])
         + recorda(t(r"Resol primer els parèntesis i claudàtors de dins cap a fora. Dins de cada un, primer les potències i les arrels, després les multiplicacions i divisions i, al final, les sumes i restes.", r"Resuelve primero los paréntesis y corchetes de dentro hacia fuera. Dentro de cada uno, primero las potencias y las raíces, después las multiplicaciones y divisiones y, al final, las sumas y restas.")),
         tasks(1, [steps(e, *p) for e, p in C4])),
     (3, t(r"Una parcel·la quadrada té una superfície de 1225\,m². Quant mesura el costat? Quants metres de tanca calen per a envoltar-la?", r"Una parcela cuadrada tiene una superficie de 1225\,m². ¿Cuánto mide el lado? ¿Cuántos metros de valla hacen falta para rodearla?"),
         r'$1225=5^2\cdot7^2\Rightarrow\sqrt{1225}=5\cdot7=\res{35\text{ m}}$; \quad $4\cdot35=\res{140\text{ m}}$ ' + t('de tanca.', 'de valla.')),
    ]))
    assert isqrt(1225) == 35
    return S
