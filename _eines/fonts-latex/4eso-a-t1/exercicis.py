# Exercicis de la fitxa de 4t ESO Matemàtiques A, Unitat 1: Nombres naturals, enters i fraccionaris.
# Una sola llista per a les dues llengües: genera.py (valencià) i genera-es.py (castellà) criden seccions('va'|'es').
# Cada exercici és (estrelles, enunciat, solució). Els resultats es calculen o es comproven ací mateix.
#
# Les expressions s'escriuen amb - · : ^ √ ( ) [ ] i les fraccions entre claus: {3/4}, {-2/5}.
# Exponents negatius: 2^-3. Valor absolut: abs(…). Fracció composta (numerador i denominador amb operacions): ⟦numerador¦denominador⟧.
# ev() les avalua amb aritmètica exacta (Fraction) i tx() les passa a LaTeX.
import re
from math import isqrt, gcd
from fractions import Fraction as F

# ---------- utilitats ----------
def tasks(n, items, gap=None):
    opt = '[after-item-skip=%s]' % gap if gap else ''
    return '\\begin{tasks}%s(%d)\n' % (opt, n) + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t

FRAC = re.compile(r'\{(-?)(\d+)/(\d+)\}')
def ev(e):
    """valor exacte (Fraction) d'una expressió"""
    q = []
    def sub(m):
        q.append(F(int(m.group(2)), int(m.group(3))) * (-1 if m.group(1) else 1))
        return 'Q' + 'abcdefghijklmnop'[len(q) - 1]
    s = FRAC.sub(sub, e)
    s = s.replace('⟦', '((').replace('¦', ')/(').replace('⟧', '))')
    s = s.replace('·', '*').replace(':', '/').replace('[', '(').replace(']', ')').replace('^', '**')
    s = re.sub(r'√(\d+)', r'R(\1)', s).replace('√(', 'R(')
    s = re.sub(r'(?<![\w.])(\d+)', r'F(\1)', s)
    def R(x):
        r = isqrt(int(x)); assert r * r == x, e; return F(r)
    env = {'F': F, 'R': R, 'abs': abs}
    env.update({'Q' + 'abcdefghijklmnop'[i]: v for i, v in enumerate(q)})
    return eval(s, env)
def fr(v):
    """Fraction -> LaTeX"""
    v = F(v)
    if v.denominator == 1: return str(v.numerator)
    return ('-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.numerator), v.denominator)
def _abs(e):
    """abs(…) -> ‹…› (es converteix en \\left\\lvert … \\right\\rvert al final de tx)"""
    while 'abs(' in e:
        i = e.index('abs('); d = 0
        for j in range(i + 3, len(e)):
            d += {'(': 1, ')': -1}.get(e[j], 0)
            if d == 0: break
        e = e[:i] + '‹' + e[i + 4:j] + '›' + e[j + 1:]
    return e
def tx(e):
    e = _abs(e)
    e = re.sub(r'√\(([^()]*)\)', r'\\sqrt{\1}', e)
    e = re.sub(r'√(\d+)', r'\\sqrt{\1}', e)
    e = FRAC.sub(lambda m: m.group(1) + r'\frac{%s}{%s}' % (m.group(2), m.group(3)), e)
    e = re.sub(r'\^(-?\d+)', r'^{\1}', e)
    e = e.replace('(', r'\left(').replace(')', r'\right)').replace('[', r'\left[').replace(']', r'\right]')
    e = e.replace('‹', r'\left\lvert ').replace('›', r'\right\rvert ')
    e = re.sub(r'⟦([^⟦⟧]*)¦([^⟦⟧]*)⟧', r'\\dfrac{\1}{\2}', e)
    return e.replace('·', r'\cdot ')
def m(e): return '$' + tx(e) + '$'
def rsol(e): return '$' + tx(e) + r'=\res{%s}$' % fr(ev(e))
def steps(e, *mid):
    """e = pas1 = pas2 = … = \\res{resultat}; comprova que cada pas val el mateix que e"""
    v = ev(e)
    for p in mid: assert ev(p) == v, (e, p, ev(p), v)
    return '$' + '='.join(tx(x) for x in (e,) + mid) + r'=\res{%s}$' % fr(v)
def ck(a, b): assert F(a) == F(b), (a, b)

def seccions(lang):
    def t(va, es): return va if lang == 'va' else es
    S = []

    # =====================================================================
    P1 = ['3^5', '10^6', '2^3·5^2', '√144', '√225', '17^0']
    C2 = [('25-3·[12-2·(7-4)]', ['25-3·[12-2·3]', '25-3·6', '25-18']),
          ('6+48:[20-4·(9-6)]', ['6+48:[20-4·3]', '6+48:8', '6+6']),
          ('60:[3·(9-5)+2·(7-3)]', ['60:[3·4+2·4]', '60:[12+8]', '60:20']),
          ('2·(40-3·[5+2·(9-6)])+7', ['2·(40-3·[5+2·3])+7', '2·(40-3·11)+7', '2·7+7']),
          ('5·[18-(4+2·3)]-4·[10-(9-2·3)]', ['5·[18-10]-4·[10-3]', '5·8-4·7', '40-28']),
          ('2^3·[15-(√49+2)]+36:3^2', ['8·[15-9]+36:9', '8·6+4', '48+4'])]
    S.append((t('Nombres naturals. Operacions combinades', 'Números naturales. Operaciones combinadas'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(6, [m(e) for e in P1]), tasks(3, [rsol(e) for e in P1])),
     (1, t(r"Calcula el quocient i el residu de cada divisió i fes la prova ($D=d\cdot q+r$):", r"Calcula el cociente y el resto de cada división y haz la prueba ($D=d\cdot q+r$):")
         + tasks(2, [m('1250:37'), m('5000:123')]),
         tasks(2, [r'$1250=37\cdot\res{33}+\res{29}$', r'$5000=123\cdot\res{40}+\res{80}$'])),
     (2, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in C2], gap='6pt')
         + recorda(t(r"Primer els parèntesis i claudàtors (de dins cap a fora); després les potències i les arrels; després les multiplicacions i divisions (d'esquerra a dreta) i, al final, les sumes i restes.", r"Primero los paréntesis y corchetes (de dentro hacia fuera); después las potencias y las raíces; después las multiplicaciones y divisiones (de izquierda a derecha) y, al final, las sumas y restas.")),
         tasks(1, [steps(e, *p) for e, p in C2])),
     (2, t(r"Comprem 3 samarretes a 18\,€ i 2 pantalons a 35\,€, i ens fan un descompte de 15\,€ sobre el total. Paguem amb dos bitllets de 100\,€. Escriu l'operació en una sola expressió i calcula el canvi.", r"Compramos 3 camisetas a 18\,€ y 2 pantalones a 35\,€, y nos hacen un descuento de 15\,€ sobre el total. Pagamos con dos billetes de 100\,€. Escribe la operación en una sola expresión y calcula el cambio."),
         steps('2·100-(3·18+2·35-15)', '200-(54+70-15)', '200-109') + r'\,€'),
     (3, t(r"Un alumne ha fet $36:6\cdot2+4^2=36:12+16=3+16=19$. Explica l'error i fes-ho bé.", r"Un alumno ha hecho $36:6\cdot2+4^2=36:12+16=3+16=19$. Explica el error y hazlo bien."),
         t(r'Ha multiplicat abans de dividir: les multiplicacions i divisions es fan d\'esquerra a dreta. ', r'Ha multiplicado antes de dividir: las multiplicaciones y divisiones se hacen de izquierda a derecha. ') + steps('36:6·2+4^2', '6·2+16', '12+16')),
     (3, t(r"Un hort quadrat té una superfície de 1225\,m². El volem tancar amb 3 voltes de filferro, deixant una porta de 5\,m. El filferro es ven en rotlles de 50\,m a 18\,€ el rotlle. Quants rotlles cal comprar? Quant costaran?", r"Un huerto cuadrado tiene una superficie de 1225\,m². Lo queremos vallar con 3 vueltas de alambre, dejando una puerta de 5\,m. El alambre se vende en rollos de 50\,m a 18\,€ el rollo. ¿Cuántos rollos hay que comprar? ¿Cuánto costarán?"),
         t(r'Costat: $\sqrt{1225}=35$\,m. Una volta: $4\cdot35-5=135$\,m; tres voltes: $3\cdot135=405$\,m. $405:50=8$ i sobren 5\,m, per tant calen $\res{9\text{ rotlles}}$. Cost: $9\cdot18=\res{162\text{ €}}$.',
           r'Lado: $\sqrt{1225}=35$\,m. Una vuelta: $4\cdot35-5=135$\,m; tres vueltas: $3\cdot135=405$\,m. $405:50=8$ y sobran 5\,m, por tanto hacen falta $\res{9\text{ rollos}}$. Coste: $9\cdot18=\res{162\text{ €}}$.')),
    ]))
    assert 37 * 33 + 29 == 1250 and 123 * 40 + 80 == 5000 and 35 ** 2 == 1225 and 3 * (4 * 35 - 5) == 405 and 9 * 18 == 162

    # =====================================================================
    AB = ['abs(-15)+abs(7)', 'abs(-4-9)', 'abs(-4)-abs(9)', '-abs(-12)', 'abs(3-11)·abs(-2)', 'abs(-20):abs(-5)-abs(-3)']
    A3 = [('abs(4-9)-abs(2-3·5)+abs(-6)·(-2)', ['abs(-5)-abs(-13)+6·(-2)', '5-13-12']),
          ('(3-8)·2+abs(6-4·3)·abs(-1-2)', ['(-5)·2+abs(-6)·abs(-3)', '-10+6·3', '-10+18']),
          ('7-abs(-3-abs(2-9))', ['7-abs(-3-7)', '7-abs(-10)', '7-10']),
          ('abs((-2)·(-5)-abs(3-15))-abs(-4)·(1-3)', ['abs(10-12)-4·(-2)', '2+8'])]
    S.append((t('Nombres enters. Valor absolut', 'Números enteros. Valor absoluto'), [
     (1, t(r"Ordena de menor a major: $\ -15,\ 8,\ -3,\ 0,\ -21,\ 5,\ -8,\ 12$.", r"Ordena de menor a mayor: $\ -15,\ 8,\ -3,\ 0,\ -21,\ 5,\ -8,\ 12$."),
         r'$\res{-21<-15<-8<-3<0<5<8<12}$'),
     (1, t(r"Calcula:", r"Calcula:") + tasks(3, [m(e) for e in AB], gap='4pt')
         + recorda(t(r"El valor absolut $|a|$ és la distància de $a$ al 0: sempre és positiu o zero. Si dins hi ha operacions, primer les fem i després traiem el valor absolut.", r"El valor absoluto $|a|$ es la distancia de $a$ al 0: siempre es positivo o cero. Si dentro hay operaciones, primero las hacemos y después quitamos el valor absoluto.")),
         tasks(3, [rsol(e) for e in AB])),
     (2, t(r"Escriu tots els nombres enters $x$ que compleixen:", r"Escribe todos los números enteros $x$ que cumplen:") + tasks(4, [r'$|x|=9$', r'$|x|\le3$', r'$-4\le x<2$', r'$|x-2|=5$']),
         tasks(1, [r'$x=\res{-9}$ ' + t('i', 'y') + r' $x=\res{9}$', r'$\res{-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 3}$', r'$\res{-4,\ -3,\ -2,\ -1,\ 0,\ 1}$',
                   t(r'$x$ està a 5 unitats del 2: \ $x=\res{-3}$ i $x=\res{7}$', r'$x$ está a 5 unidades del 2: \ $x=\res{-3}$ y $x=\res{7}$')])),
     (3, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in A3], gap='6pt'), tasks(1, [steps(e, *p) for e, p in A3])),
     (2, t(r"A les 7 del matí, en una ciutat de Sibèria, el termòmetre marcava $-27$\,°C. A migdia la temperatura havia pujat 19 graus i a mitjanit havia baixat 14 graus respecte de migdia. a) Quina temperatura feia a migdia i a mitjanit? b) Quina diferència hi ha entre la temperatura més alta i la més baixa d'aquestes tres?", r"A las 7 de la mañana, en una ciudad de Siberia, el termómetro marcaba $-27$\,°C. A mediodía la temperatura había subido 19 grados y a medianoche había bajado 14 grados respecto del mediodía. a) ¿Qué temperatura hacía a mediodía y a medianoche? b) ¿Qué diferencia hay entre la temperatura más alta y la más baja de estas tres?"),
         tasks(2, [steps('-27+19') + r'\,°C; \ ' + steps('-8-14') + r'\,°C', steps('-8-(-27)', '-8+27') + r'\,°C'])),
     (2, t(r"Arquimedes va nàixer l'any 287 aC i va morir l'any 212 aC. Quants anys va viure?", r"Arquímedes nació el año 287 a.\,C. y murió el año 212 a.\,C. ¿Cuántos años vivió?"),
         steps('-212-(-287)', '-212+287') + t(' anys.', ' años.')),
    ]))

    # =====================================================================
    E1 = ['-12+7-(-5)', '(-8)·(-6):(-4)', '(-72):(-9)·(-2)', '-15-(-3)·4', '(-2)·(-3)·(-5)', '-36:(-4)-9']
    E3 = [('12-4·[6-3·(5-8)]', ['12-4·[6-3·(-3)]', '12-4·[6+9]', '12-4·15', '12-60']),
          ('-3+24:[-2-2·(1-6)]', ['-3+24:[-2-2·(-5)]', '-3+24:[-2+10]', '-3+24:8', '-3+3']),
          ('5·(-4+9)-[7-(-3)·(2-6)]', ['5·5-[7-(-3)·(-4)]', '25-[7-12]', '25-(-5)']),
          ('(-2)·[8-(3-5)·(-4)]-(-6):(-2)', ['(-2)·[8-(-2)·(-4)]-3', '(-2)·[8-8]-3', '(-2)·0-3']),
          ('40:[-12+4·(7-9)·(-1)]', ['40:[-12+4·(-2)·(-1)]', '40:[-12+8]', '40:(-4)']),
          ('-[6-(2-11)]+3·[-4+(5-1)·2]', ['-[6-(-9)]+3·[-4+4·2]', '-15+3·4', '-15+12'])]
    E4 = [('(-3)^3+(-2)^4-(-1)^9', ['-27+16-(-1)', '-27+16+1']), ('-4^2+(-4)^2-√36·(-2)^3', ['-16+16-6·(-8)', '0+48']),
          ('[(-5)^2-√(100-36)·3]:(-1)^7', ['[25-√64·3]:(-1)', '[25-24]:(-1)', '1:(-1)']), ('2·(-3)^2-[(-2)^3+√81]^2', ['2·9-[-8+9]^2', '18-1^2', '18-1']),
          ('(-2)^5:(-2)^3-3·(-1)^20+√(4^2+3^2)', ['(-32):(-8)-3·1+√25', '4-3+5'])]
    S.append((t('Operacions combinades amb enters', 'Operaciones combinadas con enteros'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(3, [m(e) for e in E1])
         + recorda(t(r"Regla dels signes: $(+)\cdot(+)=+$, \ $(-)\cdot(-)=+$, \ $(+)\cdot(-)=-$, \ $(-)\cdot(+)=-$. També per a la divisió.", r"Regla de los signos: $(+)\cdot(+)=+$, \ $(-)\cdot(-)=+$, \ $(+)\cdot(-)=-$, \ $(-)\cdot(+)=-$. También para la división.")),
         tasks(3, [rsol(e) for e in E1])),
     (2, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in E3], gap='6pt'), tasks(1, [steps(e, *p) for e, p in E3])),
     (2, t(r"Calcula pas a pas (amb potències i arrels):", r"Calcula paso a paso (con potencias y raíces):") + tasks(2, [m(e) for e, _ in E4], gap='6pt')
         + recorda(t(r"$(-4)^2=16$, però $-4^2=-16$: sense parèntesi, el signe no forma part de la base.", r"$(-4)^2=16$, pero $-4^2=-16$: sin paréntesis, el signo no forma parte de la base.")),
         tasks(1, [steps(e, *p) for e, p in E4])),
     (2, t(r"Un compte bancari té un saldo de 420\,€. Es paguen 3 rebuts de 85\,€ i 2 de 120\,€ i, després, s'ingressen dues nòmines de 150\,€. Escriu-ho en una sola expressió i calcula el saldo final. Ha arribat a estar en negatiu?", r"Una cuenta bancaria tiene un saldo de 420\,€. Se pagan 3 recibos de 85\,€ y 2 de 120\,€ y, después, se ingresan dos nóminas de 150\,€. Escríbelo en una sola expresión y calcula el saldo final. ¿Ha llegado a estar en negativo?"),
         steps('420-3·85-2·120+2·150', '420-255-240+300') + r'\,€. ' + t(r'Sí: després dels rebuts el saldo era $420-495=\res{-75}$\,€.', r'Sí: después de los recibos el saldo era $420-495=\res{-75}$\,€.')),
     (3, t(r"Un ascensor és a la planta 3. Baixa 5 plantes, després puja el doble de les que ha baixat i, finalment, baixa 9 plantes. A quina planta està? Si entre planta i planta hi ha 3\,m, quants metres ha recorregut en total?", r"Un ascensor está en la planta 3. Baja 5 plantas, después sube el doble de las que ha bajado y, finalmente, baja 9 plantas. ¿En qué planta está? Si entre planta y planta hay 3\,m, ¿cuántos metros ha recorrido en total?"),
         steps('3-5+2·5-9', '3-5+10-9') + t(' (primer soterrani). \\quad Recorregut: ', ' (primer sótano). \\quad Recorrido: ') + steps('(5+10+9)·3', '24·3') + r'\,m'),
     (3, t(r"Les temperatures mínimes d'una setmana han sigut $-6$, $3$, $-2$, $-8$, $1$, $-4$ i $2$\,°C. Calcula la temperatura mitjana i la diferència entre la màxima i la mínima.", r"Las temperaturas mínimas de una semana han sido $-6$, $3$, $-2$, $-8$, $1$, $-4$ y $2$\,°C. Calcula la temperatura media y la diferencia entre la máxima y la mínima."),
         t(r'Mitjana: ', r'Media: ') + steps('(-6+3-2-8+1-4+2):7', '(-14):7') + r'\,°C. \quad ' + t('Diferència: ', 'Diferencia: ') + steps('3-(-8)') + r'\,°C.'),
     (3, t(r"Troba dos nombres enters que multiplicats donen $-24$ i sumats donen $-2$.", r"Halla dos números enteros que multiplicados den $-24$ y sumados den $-2$."),
         t(r'Han de tindre signes diferents i el negatiu ha de ser el de valor absolut més gran: ', r'Han de tener signos distintos y el negativo debe ser el de valor absoluto mayor: ') + r'$\res{4}$ ' + t('i', 'y') + r' $\res{-6}$ \ ($4\cdot(-6)=-24$, \ $4+(-6)=-2$).'),
    ]))
    assert 4 * -6 == -24 and 4 - 6 == -2

    # =====================================================================
    SI = [(84, 140), (126, 315), (210, 462), (360, 840), (156, 234), (275, 1100)]
    def simp(a, b):
        return r'$\frac{%d}{%d}=\frac{%d:%d}{%d:%d}=\res{%s}$' % (a, b, a, gcd(a, b), b, gcd(a, b), fr(F(a, b)))
    S.append((t('Fraccions. Fraccions equivalents', 'Fracciones. Fracciones equivalentes'), [
     (1, t(r"Simplifica fins a obtindre la fracció irreductible:", r"Simplifica hasta obtener la fracción irreducible:") + tasks(6, [r'$\frac{%d}{%d}$' % ab for ab in SI], gap='8pt')
         + recorda(t(r"Per a arribar directament a la fracció irreductible, dividim el numerador i el denominador entre el seu MCD.", r"Para llegar directamente a la fracción irreducible, dividimos el numerador y el denominador entre su MCD.")),
         tasks(2, [simp(a, b) for a, b in SI], gap='6pt')),
     (1, t(r"Calcula:", r"Calcula:") + tasks(1, [t(r'Els $\frac{2}{3}$ dels $\frac{3}{5}$ de 450\,€.', r'Los $\frac{2}{3}$ de los $\frac{3}{5}$ de 450\,€.'),
                                                t(r'Els $\frac{3}{4}$ de la meitat de 96 alumnes.', r'Los $\frac{3}{4}$ de la mitad de 96 alumnos.'),
                                                t(r'Els $\frac{5}{6}$ d\'un terç de 720 litres.', r'Los $\frac{5}{6}$ de un tercio de 720 litros.')]),
         tasks(1, [r'$\frac{2}{3}\cdot\frac{3}{5}\cdot450=\frac{2}{5}\cdot450=\res{180\text{ €}}$', r'$\frac{3}{4}\cdot\frac{1}{2}\cdot96=\frac{3}{8}\cdot96=\res{36}$',
                   r'$\frac{5}{6}\cdot\frac{1}{3}\cdot720=\frac{5}{18}\cdot720=\res{200\text{ L}}$'])),
     (2, t(r"Comprova si són equivalents:", r"Comprueba si son equivalentes:") + tasks(3, [r'$\frac{21}{35}$ ' + t('i', 'y') + r' $\frac{33}{55}$', r'$\frac{18}{24}$ ' + t('i', 'y') + r' $\frac{27}{32}$', r'$\frac{-14}{49}$ ' + t('i', 'y') + r' $\frac{6}{-21}$'], gap='6pt'),
         tasks(1, [r'$21\cdot55=1155=35\cdot33$: \res{sí}', r'$18\cdot32=576\neq24\cdot27=648$: \res{no}', r'$(-14)\cdot(-21)=294=49\cdot6$: \res{sí}'])),
     (2, t(r"Troba el valor de $x$ perquè les fraccions siguen equivalents:", r"Halla el valor de $x$ para que las fracciones sean equivalentes:") + tasks(3, [r'$\frac{x}{18}=\frac{35}{42}$', r'$\frac{12}{x}=-\frac{4}{7}$', r'$\frac{-15}{25}=\frac{x}{-40}$'], gap='6pt'),
         tasks(3, [r'$42x=630\Rightarrow x=\res{15}$', r'$-4x=84\Rightarrow x=\res{-21}$', r'$25x=600\Rightarrow x=\res{24}$'])),
     (2, t(r"Quina fracció del dia són 16 hores? I 45 minuts? I 2 h 40 min? Dona-les irreductibles.", r"¿Qué fracción del día son 16 horas? ¿Y 45 minutos? ¿Y 2 h 40 min? Dalas irreducibles."),
         r'$\frac{16}{24}=\res{\frac{2}{3}}$; \quad $\frac{45}{1440}=\res{\frac{1}{32}}$; \quad $\frac{160}{1440}=\res{\frac{1}{9}}$'),
     (2, t(r"Ordena de menor a major i situa-les aproximadament en la recta: $\ \frac{5}{6},\ -\frac{3}{4},\ \frac{7}{9},\ -\frac{2}{3},\ \frac{13}{18},\ 0$.", r"Ordena de menor a mayor y sitúalas aproximadamente en la recta: $\ \frac{5}{6},\ -\frac{3}{4},\ \frac{7}{9},\ -\frac{2}{3},\ \frac{13}{18},\ 0$."),
         t(r'Amb denominador comú 36: $\frac{30}{36},\ -\frac{27}{36},\ \frac{28}{36},\ -\frac{24}{36},\ \frac{26}{36}$. \quad ', r'Con denominador común 36: $\frac{30}{36},\ -\frac{27}{36},\ \frac{28}{36},\ -\frac{24}{36},\ \frac{26}{36}$. \quad ')
         + r'$\res{-\frac{3}{4}<-\frac{2}{3}<0<\frac{13}{18}<\frac{7}{9}<\frac{5}{6}}$'),
     (3, t(r"Escriu una fracció compresa entre $\frac{3}{7}$ i $\frac{4}{7}$, i una altra entre $\frac{2}{5}$ i $\frac{1}{2}$. Explica com ho has fet.", r"Escribe una fracción comprendida entre $\frac{3}{7}$ y $\frac{4}{7}$, y otra entre $\frac{2}{5}$ y $\frac{1}{2}$. Explica cómo lo has hecho."),
         t(r'Amplifiquem perquè quede espai entre els numeradors: $\frac{6}{14}<\res{\frac{7}{14}}<\frac{8}{14}$; \ $\frac{8}{20}<\res{\frac{9}{20}}<\frac{10}{20}$ (per exemple).', r'Amplificamos para que quede espacio entre los numeradores: $\frac{6}{14}<\res{\frac{7}{14}}<\frac{8}{14}$; \ $\frac{8}{20}<\res{\frac{9}{20}}<\frac{10}{20}$ (por ejemplo).')),
    ]))
    ck(F(2, 3) * F(3, 5) * 450, 180); ck(F(3, 8) * 96, 36); ck(F(5, 18) * 720, 200)
    ck(F(21, 35), F(33, 55)); assert F(18, 24) != F(27, 32); ck(F(-14, 49), F(6, -21))
    ck(F(15, 18), F(35, 42)); ck(F(12, -21), F(-4, 7)); ck(F(-15, 25), F(24, -40))
    ck(F(16, 24), F(2, 3)); ck(F(45, 1440), F(1, 32)); ck(F(160, 1440), F(1, 9))
    assert sorted([F(5, 6), F(-3, 4), F(7, 9), F(-2, 3), F(13, 18), F(0)]) == [F(-3, 4), F(-2, 3), F(0), F(13, 18), F(7, 9), F(5, 6)]

    # =====================================================================
    O1 = [('{5/12}+{7/18}', ['{15/36}+{14/36}']), ('{11/15}-{7/10}', ['{22/30}-{21/30}']), ('3-{11/4}+{5/6}', ['{36/12}-{33/12}+{10/12}']), ('{-7/20}+{5/8}', ['{-14/40}+{25/40}'])]
    O2 = [('{14/15}·{25/21}', ['{350/315}']), ('{-9/16}·{8/27}', ['{-72/432}']), ('{12/35}:{18/25}', ['{300/630}']), ('({-5/6}):({-10/9})', ['{45/60}'])]
    OF = [('{2/3}·{9/10}', r'\frac{2}{3}', r'\frac{9}{10}'), ('{1/2}·{4/7}', t('la meitat', 'la mitad'), r'\frac{4}{7}'), ('{3/5}·{5/12}', r'\frac{3}{5}', r'\frac{5}{12}'), ('{7/8}·{4/21}', r'\frac{7}{8}', r'\frac{4}{21}')]
    O4 = [('{-5/6}-({-3/4})+{-1/3}', ['{-10/12}+{9/12}-{4/12}']), ('({-2/3})·{9/4}·({-8/15})', ['{144/180}']),
          ('({-4/9}):({-2/3})·(-6)', ['{2/3}·(-6)']), ('-2-({-5/4})+{7/6}', ['{-24/12}+{15/12}+{14/12}'])]
    S.append((t('Operacions amb fraccions', 'Operaciones con fracciones'), [
     (1, t(r"Calcula i simplifica el resultat:", r"Calcula y simplifica el resultado:") + tasks(4, [m(e) for e, _ in O1], gap='8pt')
         + recorda(t(r"Per a sumar o restar, primer reduïm a comú denominador (amb el mcm dels denominadors). Mai no sumem els denominadors!", r"Para sumar o restar, primero reducimos a común denominador (con el mcm de los denominadores). ¡Nunca sumamos los denominadores!")),
         tasks(2, [steps(e, *p) for e, p in O1], gap='6pt')),
     (1, t(r"Calcula i simplifica el resultat:", r"Calcula y simplifica el resultado:") + tasks(4, [m(e) for e, _ in O2], gap='8pt')
         + recorda(t(r"$\frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}$ \qquad $\frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}$. Simplifica abans de multiplicar i els números seran més menuts.", r"$\frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}$ \qquad $\frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}$. Simplifica antes de multiplicar y los números serán más pequeños.")),
         tasks(2, [steps(e, *p) for e, p in O2], gap='6pt')),
     (2, t(r"Troba la fracció resultant:", r"Halla la fracción resultante:") + tasks(4, ['$%s$ %s $%s$' % (a, t('de', 'de'), b) for _, a, b in OF], gap='6pt'),
         tasks(2, [steps(e) for e, _, _ in OF], gap='6pt')),
     (2, t(r"Calcula (compte amb els signes):", r"Calcula (cuidado con los signos):") + tasks(2, [m(e) for e, _ in O4], gap='8pt'),
         tasks(2, [steps(e, *p) for e, p in O4], gap='6pt')),
     (2, t(r"Escriu l'oposat i l'invers de cada nombre:", r"Escribe el opuesto y el inverso de cada número:") + tasks(4, [r'$\frac{3}{8}$', r'$-\frac{5}{2}$', r'$-6$', r'$1+\frac{1}{3}$']),
         tasks(2, [t('Op.', 'Op.') + r' $\res{-\frac{3}{8}}$, \ inv. $\res{\frac{8}{3}}$', t('Op.', 'Op.') + r' $\res{\frac{5}{2}}$, \ inv. $\res{-\frac{2}{5}}$',
                   t('Op.', 'Op.') + r' $\res{6}$, \ inv. $\res{-\frac{1}{6}}$', r'$1+\frac{1}{3}=\frac{4}{3}$: \ ' + t('op.', 'op.') + r' $\res{-\frac{4}{3}}$, \ inv. $\res{\frac{3}{4}}$'])),
    ]))

    # =====================================================================
    K1 = [('{2/3}+{1/2}·{4/9}', ['{2/3}+{2/9}', '{6/9}+{2/9}']), ('({2/3}+{1/2})·{4/9}', ['{7/6}·{4/9}', '{28/54}']),
          ('{3/4}-{1/4}:{3/8}', ['{3/4}-{2/3}', '{9/12}-{8/12}']), ('({3/4}-{1/4}):{3/8}', ['{1/2}:{3/8}', '{8/6}'])]
    K2 = [('{3/4}-[{1/2}-({2/5}-{1/10})]', ['{3/4}-[{1/2}-{3/10}]', '{3/4}-{1/5}', '{15/20}-{4/20}']),
          ('2-[{1/3}+({5/6}-1)]+{1/4}', ['2-[{1/3}+({-1/6})]+{1/4}', '2-{1/6}+{1/4}', '{24/12}-{2/12}+{3/12}']),
          ('1-({2/3}+{1/4}-{1/2}):{5/6}', ['1-{5/12}:{5/6}', '1-{1/2}']),
          ('{4/5}·[{1/2}-({3/4}-{1/8})]', ['{4/5}·[{1/2}-{5/8}]', '{4/5}·({-1/8})']),
          ('[{2/3}·({1/4}+{1/2})]:[(-3)·({1/6}-{1/2})]', ['[{2/3}·{3/4}]:[(-3)·({-1/3})]', '{1/2}:1']),
          ('({5/6}-{2/3}-{1/12}):(1-{3/4})', ['{1/12}:{1/4}'])]
    K3 = [('({3/2})^2-{5/4}·(1-{1/5})', ['{9/4}-{5/4}·{4/5}', '{9/4}-1']), ('({-2/3})^3:{4/9}+{1/2}', ['{-8/27}:{4/9}+{1/2}', '{-2/3}+{1/2}']),
          ('[1-({1/2})^2]^2·{16/3}', ['[1-{1/4}]^2·{16/3}', '({3/4})^2·{16/3}', '{9/16}·{16/3}'])]
    CF = [('⟦{2/3}-{1/4}¦{5/6}+{1/3}⟧', ['⟦{5/12}¦{7/6}⟧']), ('⟦1-{3/5}·{5/6}¦({1/2})^2+{1/3}⟧', ['⟦{1/2}¦{7/12}⟧']),
          ('⟦(-2)·({1/4}-{2/3})¦3·({5/6}-{1/2})⟧', ['⟦(-2)·({-5/12})¦3·{1/3}⟧', '⟦{5/6}¦1⟧']), ('⟦{3/4}:{9/8}-{1/3}¦1-{4/9}⟧', ['⟦{2/3}-{1/3}¦{5/9}⟧', '⟦{1/3}¦{5/9}⟧'])]
    K4 = [('[{3/4}-({1/2})^2]^2:({-1/2})^3+{5/3}·{6/5}', ['[{3/4}-{1/4}]^2:({-1/8})+2', '({1/2})^2:({-1/8})+2', '{1/4}:({-1/8})+2', '-2+2']),
          ('{1/2}-{2/3}·[{3/4}-({1/2}-2)^2:3]', ['{1/2}-{2/3}·[{3/4}-({-3/2})^2:3]', '{1/2}-{2/3}·[{3/4}-{9/4}:3]', '{1/2}-{2/3}·[{3/4}-{3/4}]', '{1/2}-{2/3}·0'])]
    S.append((t('Operacions combinades amb fraccions', 'Operaciones combinadas con fracciones'), [
     (1, t(r"Calcula i compara els resultats de a) i b), i de c) i d):", r"Calcula y compara los resultados de a) y b), y de c) y d):") + tasks(4, [m(e) for e, _ in K1], gap='8pt'),
         tasks(2, [steps(e, *p) for e, p in K1], gap='6pt')),
     (2, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in K2], gap='10pt'), tasks(1, [steps(e, *p) for e, p in K2], gap='6pt')),
     (2, t(r"Calcula pas a pas (amb potències):", r"Calcula paso a paso (con potencias):") + tasks(3, [m(e) for e, _ in K3], gap='8pt')
         + recorda(t(r"Per a elevar una fracció, elevem el numerador i el denominador: $\left(-\frac{2}{3}\right)^3=-\frac{2^3}{3^3}=-\frac{8}{27}$.", r"Para elevar una fracción, elevamos el numerador y el denominador: $\left(-\frac{2}{3}\right)^3=-\frac{2^3}{3^3}=-\frac{8}{27}$.")),
         tasks(1, [steps(e, *p) for e, p in K3], gap='6pt')),
     (3, t(r"Calcula (primer el numerador i el denominador, i després divideix):", r"Calcula (primero el numerador y el denominador, y después divide):") + tasks(4, [m(e) for e, _ in CF], gap='10pt'),
         tasks(2, [steps(e, *p) for e, p in CF], gap='10pt')),
     (3, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(1, [m(e) for e, _ in K4], gap='8pt'), tasks(1, [steps(e, *p) for e, p in K4], gap='6pt')),
    ]))

    # =====================================================================
    S.append((t('Problemes amb fraccions', 'Problemas con fracciones'), [
     (1, t(r"Els $\frac{4}{9}$ dels alumnes d'un institut, que són 352, venen amb autobús. Quants alumnes té l'institut?", r"Los $\frac{4}{9}$ de los alumnos de un instituto, que son 352, vienen en autobús. ¿Cuántos alumnos tiene el instituto?"),
         r'$352:\frac{4}{9}=\frac{352\cdot9}{4}=\res{792}$ ' + t('alumnes.', 'alumnos.')),
     (2, t(r"Un mòbil costa 480\,€. Paguem $\frac{1}{4}$ d'entrada i la resta en 9 quotes iguals. Quant paguem en cada quota? Quina fracció del preu és cada quota?", r"Un móvil cuesta 480\,€. Pagamos $\frac{1}{4}$ de entrada y el resto en 9 cuotas iguales. ¿Cuánto pagamos en cada cuota? ¿Qué fracción del precio es cada cuota?"),
         t(r'Entrada: $\frac{1}{4}\cdot480=120$\,€; resta: 360\,€. Quota: $360:9=\res{40\text{ €}}$, \ que és $\frac{3}{4}:9=\res{\frac{1}{12}}$ del preu.', r'Entrada: $\frac{1}{4}\cdot480=120$\,€; resto: 360\,€. Cuota: $360:9=\res{40\text{ €}}$, \ que es $\frac{3}{4}:9=\res{\frac{1}{12}}$ del precio.')),
     (2, t(r"Es reparteixen 1800\,€ entre tres germans: el primer rep $\frac{2}{5}$ del total, el segon $\frac{3}{4}$ del que queda i el tercer la resta. Quant rep cada un? Quina fracció del total rep el tercer?", r"Se reparten 1800\,€ entre tres hermanos: el primero recibe $\frac{2}{5}$ del total, el segundo $\frac{3}{4}$ de lo que queda y el tercero el resto. ¿Cuánto recibe cada uno? ¿Qué fracción del total recibe el tercero?"),
         t('1r', '1.º') + r': $\frac{2}{5}\cdot1800=\res{720}$\,€; \ ' + t('queden', 'quedan') + r' 1080\,€. \ ' + t('2n', '2.º') + r': $\frac{3}{4}\cdot1080=\res{810}$\,€. \ ' + t('3r', '3.º') + r': $1080-810=\res{270}$\,€, \ $\frac{270}{1800}=\res{\frac{3}{20}}$.'),
     (2, t(r"En un camp de 2400\,m² es planten tomaques en $\frac{3}{8}$ de la superfície i creïlles en $\frac{2}{5}$ de la resta. La resta és per a pebrots. Quants m² ocupa cada cultiu? Quina fracció del camp ocupen els pebrots?", r"En un campo de 2400\,m² se plantan tomates en $\frac{3}{8}$ de la superficie y patatas en $\frac{2}{5}$ del resto. El resto es para pimientos. ¿Cuántos m² ocupa cada cultivo? ¿Qué fracción del campo ocupan los pimientos?"),
         t('Tomaques', 'Tomates') + r': $\frac{3}{8}\cdot2400=\res{900}$\,m²; \ ' + t('resta', 'resto') + r' 1500\,m². \ ' + t('Creïlles', 'Patatas') + r': $\frac{2}{5}\cdot1500=\res{600}$\,m². \ ' + t('Pebrots', 'Pimientos') + r': $\res{900}$\,m², \ $\frac{900}{2400}=\res{\frac{3}{8}}$.'),
     (3, t(r"Una aixeta omple $\frac{1}{6}$ d'un dipòsit cada hora i una altra, $\frac{1}{4}$. Si les obrim totes dues alhora, quina fracció del dipòsit s'omple en una hora? Quant de temps tarden a omplir-lo?", r"Un grifo llena $\frac{1}{6}$ de un depósito cada hora y otro, $\frac{1}{4}$. Si los abrimos los dos a la vez, ¿qué fracción del depósito se llena en una hora? ¿Cuánto tiempo tardan en llenarlo?"),
         r'$\frac{1}{6}+\frac{1}{4}=\frac{2}{12}+\frac{3}{12}=\res{\frac{5}{12}}$. \ ' + t('Temps', 'Tiempo') + r': $1:\frac{5}{12}=\frac{12}{5}=2{,}4$\,h $=\res{2\text{ h }24\text{ min}}$.'),
     (3, t(r"L'Anna gasta $\frac{2}{7}$ del sou en el lloguer i $\frac{1}{3}$ del que li queda en menjar. Encara li queden 600\,€. Quant cobra?", r"Anna gasta $\frac{2}{7}$ del sueldo en el alquiler y $\frac{1}{3}$ de lo que le queda en comida. Todavía le quedan 600\,€. ¿Cuánto cobra?"),
         t(r'Després del lloguer li queden $\frac{5}{7}$; en menjar gasta $\frac{1}{3}\cdot\frac{5}{7}=\frac{5}{21}$. Li queden $\frac{5}{7}-\frac{5}{21}=\frac{10}{21}$, que són 600\,€: \ ', r'Después del alquiler le quedan $\frac{5}{7}$; en comida gasta $\frac{1}{3}\cdot\frac{5}{7}=\frac{5}{21}$. Le quedan $\frac{5}{7}-\frac{5}{21}=\frac{10}{21}$, que son 600\,€: \ ') + r'$600:\frac{10}{21}=\res{1260\text{ €}}$.'),
     (3, t(r"En un viatge, el primer dia fem $\frac{2}{5}$ del recorregut i el segon dia, $\frac{3}{4}$ del que falta. Encara queden 90\,km. Quants quilòmetres té el viatge?", r"En un viaje, el primer día hacemos $\frac{2}{5}$ del recorrido y el segundo día, $\frac{3}{4}$ de lo que falta. Todavía quedan 90\,km. ¿Cuántos kilómetros tiene el viaje?"),
         t(r'Queda $\frac{1}{4}$ de $\frac{3}{5}$, és a dir, $\frac{1}{4}\cdot\frac{3}{5}=\frac{3}{20}$ del viatge: \ ', r'Queda $\frac{1}{4}$ de $\frac{3}{5}$, es decir, $\frac{1}{4}\cdot\frac{3}{5}=\frac{3}{20}$ del viaje: \ ') + r'$90:\frac{3}{20}=\res{600\text{ km}}$.'),
     (3, t(r"Un pot ple de mel pesa 950\,g. Quan n'hem gastat $\frac{3}{5}$ de la mel, pesa 470\,g. Quant pesa el pot buit?", r"Un bote lleno de miel pesa 950\,g. Cuando hemos gastado $\frac{3}{5}$ de la miel, pesa 470\,g. ¿Cuánto pesa el bote vacío?"),
         t(r'Els $\frac{3}{5}$ de la mel pesen $950-470=480$\,g; tota la mel, $480:\frac{3}{5}=800$\,g. Pot: $950-800=\res{150\text{ g}}$.', r'Los $\frac{3}{5}$ de la miel pesan $950-470=480$\,g; toda la miel, $480:\frac{3}{5}=800$\,g. Bote: $950-800=\res{150\text{ g}}$.')),
     (3, t(r"D'un dipòsit ple, el dilluns se'n gasta $\frac{1}{3}$; el dimarts, $\frac{1}{4}$ del que quedava, i el dimecres, $\frac{2}{5}$ del que quedava. Al final queden 360 litres. Quina és la capacitat del dipòsit?", r"De un depósito lleno, el lunes se gasta $\frac{1}{3}$; el martes, $\frac{1}{4}$ de lo que quedaba, y el miércoles, $\frac{2}{5}$ de lo que quedaba. Al final quedan 360 litros. ¿Cuál es la capacidad del depósito?"),
         t(r'Queda la fracció $\frac{2}{3}\cdot\frac{3}{4}\cdot\frac{3}{5}=\frac{18}{60}=\frac{3}{10}$ del dipòsit: \ ', r'Queda la fracción $\frac{2}{3}\cdot\frac{3}{4}\cdot\frac{3}{5}=\frac{18}{60}=\frac{3}{10}$ del depósito: \ ') + r'$360:\frac{3}{10}=\res{1200\text{ L}}$.'),
    ]))
    ck(352 / F(4, 9), 792); ck(F(3, 4) * 480 / 9, 40); ck(F(3, 4) / 9, F(1, 12))
    ck(F(2, 5) * 1800, 720); ck(F(3, 4) * 1080, 810); ck(F(270, 1800), F(3, 20))
    ck(F(3, 8) * 2400, 900); ck(F(2, 5) * 1500, 600); ck(2400 - 900 - 600, 900); ck(F(900, 2400), F(3, 8))
    ck(F(1, 6) + F(1, 4), F(5, 12)); ck(1 / F(5, 12), F(12, 5)); ck(F(12, 5) * 60, 144)
    ck(600 / (F(5, 7) - F(1, 3) * F(5, 7)), 1260); ck(90 / (F(1, 4) * F(3, 5)), 600); ck(950 - 480 / F(3, 5), 150)
    ck(360 / (F(2, 3) * F(3, 4) * F(3, 5)), 1200)

    # =====================================================================
    W1 = ['(-4)^3', '-4^2', '(-1)^23', '-(-2)^4', '(-10)^5', '(-9)^0']
    W2 = ['({3/4})^3', '({-2/3})^4', '({-1/5})^3', '-({3/2})^2', '({-7/8})^0', '({-1/10})^5']
    SG = [(r'(-6)^{9}', '-'), (r'(-11)^{12}', '+'), (r'-3^{8}', '-'), (r'\left(-\frac{2}{5}\right)^{11}', '-'), (r'-(-1)^{100}', '-')]
    W3 = [('(-3)^3-(-3)^2-3^2', ['-27-9-9']), ('(-1)^15-(-1)^16+(-2)^3', ['-1-1+(-8)']), ('({2/3})^2-({1/3})^2', ['{4/9}-{1/9}', '{3/9}']),
          ('({-1/2})^3·8-({3/4})^2:{9/8}', ['{-1/8}·8-{9/16}:{9/8}', '-1-{1/2}'])]
    S.append((t('Potències amb base entera i racional', 'Potencias con base entera y racional'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(6, [m(e) for e in W1]), tasks(3, [rsol(e) for e in W1])),
     (1, t(r"Calcula:", r"Calcula:") + tasks(6, [m(e) for e in W2], gap='8pt')
         + recorda(t(r"$\left(\frac{a}{b}\right)^n=\frac{a^n}{b^n}$. Si la base és negativa, el resultat és positiu amb exponent parell i negatiu amb exponent senar.", r"$\left(\frac{a}{b}\right)^n=\frac{a^n}{b^n}$. Si la base es negativa, el resultado es positivo con exponente par y negativo con exponente impar.")),
         tasks(3, [rsol(e) for e in W2], gap='6pt')),
     (2, t(r"Sense fer el càlcul, digues quin signe té el resultat:", r"Sin hacer el cálculo, di qué signo tiene el resultado:") + tasks(5, ['$' + e + '$' for e, _ in SG]),
         tasks(5, [r'$\res{%s}$' % s for _, s in SG])),
     (2, t(r"Calcula:", r"Calcula:") + tasks(2, [m(e) for e, _ in W3], gap='8pt'), tasks(2, [steps(e, *p) for e, p in W3], gap='6pt')),
     (3, t(r"Deixem caure una pilota des de 16\,m d'altura. Cada vegada que bota, puja $\frac{3}{4}$ de l'altura anterior. a) A quina altura arriba després del quart bot? b) Quants metres ha recorregut en total quan toca terra per tercera vegada?", r"Dejamos caer una pelota desde 16\,m de altura. Cada vez que bota, sube $\frac{3}{4}$ de la altura anterior. a) ¿A qué altura llega después del cuarto bote? b) ¿Cuántos metros ha recorrido en total cuando toca el suelo por tercera vez?"),
         r'a) ' + steps('16·({3/4})^4', '16·{81/256}') + r'\,m $\approx5{,}06$\,m. \quad b) ' + t('Altures dels bots', 'Alturas de los botes') + r': 12\,m i 9\,m; \ ' + steps('16+2·12+2·9', '16+24+18') + r'\,m.'),
    ]))
    ck(16 * F(3, 4), 12); ck(12 * F(3, 4), 9)

    # =====================================================================
    U1 = [('5^3·5^4', '5^{7}'), ('2^9:2^4', '2^{5}'), ('(3^2)^5', '3^{10}'), ('4^3·5^3', '20^{3}'), ('18^6:6^6', '3^{6}'), ('(-7)^4·(-7)^3', '(-7)^{7}')]
    U2 = [(r'\left(\frac{2}{5}\right)^3\cdot\left(\frac{2}{5}\right)^4', r'\left(\frac{2}{5}\right)^{7}'), (r'\left(\frac{3}{4}\right)^8:\left(\frac{3}{4}\right)^5', r'\left(\frac{3}{4}\right)^{3}'),
          (r'\left[\left(-\frac{1}{2}\right)^3\right]^2', r'\left(-\frac{1}{2}\right)^{6}'), (r'\left(\frac{2}{3}\right)^4\cdot\left(\frac{9}{4}\right)^4', r'\left(\frac{3}{2}\right)^{4}')]
    U3 = [('(-2)^7:(-2)^4', ['(-2)^3']), ('[(-1)^3]^5·(-1)^2', ['(-1)^15·(-1)^2', '(-1)^17']), ('2^5·2^3:2^6', ['2^8:2^6', '2^2']),
          ('({2/3})^5·({2/3})^2:({2/3})^4', ['({2/3})^7:({2/3})^4', '({2/3})^3']), ('({-1/3})^6:({-1/3})^4', ['({-1/3})^2'])]
    VF = [(r'2^3+2^4=2^7', 'F'), (r'3^2\cdot3^3=3^5', 'V'), (r'(2+3)^2=2^2+3^2', 'F'), (r'(3^2)^3=3^5', 'F'), (r'5^0=0', 'F'), (r'6^4:3^4=2^4', 'V')]
    S.append((t('Propietats de les potències', 'Propiedades de las potencias'), [
     (1, t(r"Expressa com una sola potència:", r"Expresa como una sola potencia:") + tasks(3, ['$' + tx(a) + '$' for a, _ in U1])
         + recorda(t(r"Mateixa base: $a^m\cdot a^n=a^{m+n}$, \ $a^m:a^n=a^{m-n}$. \ Potència de potència: $(a^m)^n=a^{m\cdot n}$. \ Mateix exponent: $a^n\cdot b^n=(a\cdot b)^n$, \ $a^n:b^n=(a:b)^n$.", r"Misma base: $a^m\cdot a^n=a^{m+n}$, \ $a^m:a^n=a^{m-n}$. \ Potencia de potencia: $(a^m)^n=a^{m\cdot n}$. \ Mismo exponente: $a^n\cdot b^n=(a\cdot b)^n$, \ $a^n:b^n=(a:b)^n$.")),
         tasks(3, ['$' + tx(a) + r'=\res{' + b + '}$' for a, b in U1])),
     (1, t(r"Expressa com una sola potència:", r"Expresa como una sola potencia:") + tasks(2, ['$' + a + '$' for a, _ in U2], gap='8pt'),
         tasks(2, ['$' + a + r'=\res{' + b + '}$' for a, b in U2], gap='6pt')),
     (2, t(r"Simplifica aplicant les propietats i calcula:", r"Simplifica aplicando las propiedades y calcula:") + tasks(3, [m(e) for e, _ in U3], gap='8pt'),
         tasks(1, [steps(e, *p) for e, p in U3], gap='6pt')),
     (2, t(r"Vertader o fals? Corregeix les falses:", r"¿Verdadero o falso? Corrige las falsas:") + tasks(3, ['$' + e + '$' for e, _ in VF]),
         tasks(2, [r'\res{F}: $2^3+2^4=8+16=24$', r'\res{V}', r'\res{F}: $(2+3)^2=25$, \ $2^2+3^2=13$', r'\res{F}: $(3^2)^3=3^6$', r'\res{F}: $5^0=1$', r'\res{V}: $(6:3)^4=2^4$'])),
     (3, t(r"Calcula descomponent les bases en factors primers:", r"Calcula descomponiendo las bases en factores primos:") + tasks(3, [r'$\dfrac{10^4\cdot2^3}{5^3\cdot4^5}$', r'$9^3\cdot27:3^7$', r'$\dfrac{12^3\cdot6^2}{18^2\cdot2^5}$'], gap='8pt'),
         tasks(1, [r'$\dfrac{2^4\cdot5^4\cdot2^3}{5^3\cdot2^{10}}=\dfrac{2^7\cdot5^4}{2^{10}\cdot5^3}=\dfrac{5}{2^3}=\res{\frac{5}{8}}$', r'$3^6\cdot3^3:3^7=3^9:3^7=3^2=\res{9}$',
                   r'$\dfrac{2^6\cdot3^3\cdot2^2\cdot3^2}{2^2\cdot3^4\cdot2^5}=\dfrac{2^8\cdot3^5}{2^7\cdot3^4}=2\cdot3=\res{6}$'], gap='6pt')),
     (3, t(r"Calcula de la manera més ràpida: $\ \left(\frac{4}{9}\right)^2\cdot\left(\frac{3}{2}\right)^4$", r"Calcula de la manera más rápida: $\ \left(\frac{4}{9}\right)^2\cdot\left(\frac{3}{2}\right)^4$"),
         r'$\left(\frac{4}{9}\right)^2=\left[\left(\frac{2}{3}\right)^2\right]^2=\left(\frac{2}{3}\right)^4 \ \Rightarrow\ \left(\frac{2}{3}\cdot\frac{3}{2}\right)^4=1^4=\res{1}$'),
    ]))
    assert 5 ** 3 * 5 ** 4 == 5 ** 7 and 2 ** 9 // 2 ** 4 == 2 ** 5 and 4 ** 3 * 5 ** 3 == 20 ** 3 and 18 ** 6 // 6 ** 6 == 3 ** 6 and 6 ** 4 // 3 ** 4 == 2 ** 4
    ck(F(2, 3) ** 4 * F(9, 4) ** 4, F(3, 2) ** 4); ck(F(10 ** 4 * 2 ** 3, 5 ** 3 * 4 ** 5), F(5, 8)); ck(F(9 ** 3 * 27, 3 ** 7), 9); ck(F(4, 9) ** 2 * F(3, 2) ** 4, 1)
    ck(F(12 ** 3 * 6 ** 2, 18 ** 2 * 2 ** 5), 6)
    assert 2 ** 3 + 2 ** 4 == 24 and 3 ** 2 * 3 ** 3 == 3 ** 5 and (3 ** 2) ** 3 == 3 ** 6

    # =====================================================================
    N1 = ['5^-2', '2^-5', '10^-3', '(-3)^-2', '(-2)^-3', '({1/4})^-2', '({2/5})^-3', '({-3/2})^-1']
    ORD = [r'(-2)^{-1}', r'2^{-2}', r'(-2)^{-3}', r'2^{0}', r'(-2)^{2}', r'2^{-1}']
    B2 = [(r'8^{-2}', r'(2^3)^{-2}=\res{2^{-6}}', F(8) ** -2, F(2) ** -6), (r'\left(\frac{1}{4}\right)^{3}', r'(2^{-2})^{3}=\res{2^{-6}}', F(1, 4) ** 3, F(2) ** -6),
          (r'\left(\frac{1}{16}\right)^{-2}', r'16^{2}=(2^4)^2=\res{2^{8}}', F(1, 16) ** -2, F(2) ** 8),
          (r'\dfrac{4^{-1}\cdot2^{5}}{8^{2}}', r'\dfrac{2^{-2}\cdot2^{5}}{2^{6}}=2^{-2+5-6}=\res{2^{-3}}', F(4) ** -1 * 2 ** 5 / 8 ** 2, F(2) ** -3)]
    NP = [(r'7^{-3}\cdot7^{5}', r'7^{2}'), (r'3^{4}:3^{-2}', r'3^{6}'), (r'(5^{-2})^{3}', r'5^{-6}'), (r'2^{-4}\cdot5^{-4}', r'10^{-4}'),
          (r'\left(\frac{3}{4}\right)^{-2}\cdot\left(\frac{3}{4}\right)^{5}', r'\left(\frac{3}{4}\right)^{3}'), (r'6^{-3}:2^{-3}', r'3^{-3}')]
    NR = [(r'\dfrac{9^{2}\cdot3^{-5}}{27^{-1}}', r'\dfrac{3^{4}\cdot3^{-5}}{3^{-3}}=3^{4-5+3}=\res{3^{2}}', F(9) ** 2 * F(3) ** -5 / F(27) ** -1, 9),
          (r'\dfrac{4^{3}\cdot6^{-2}}{3^{-4}\cdot2^{5}}', r'\dfrac{2^{6}\cdot2^{-2}\cdot3^{-2}}{3^{-4}\cdot2^{5}}=2^{-1}\cdot3^{2}=\res{\frac{9}{2}}', F(4) ** 3 * F(6) ** -2 / (F(3) ** -4 * 2 ** 5), F(9, 2)),
          (r'\dfrac{10^{-2}\cdot25^{2}}{5^{3}\cdot2^{-3}}', r'\dfrac{2^{-2}\cdot5^{-2}\cdot5^{4}}{5^{3}\cdot2^{-3}}=2\cdot5^{-1}=\res{\frac{2}{5}}', F(10) ** -2 * 25 ** 2 / (5 ** 3 * F(2) ** -3), F(2, 5))]
    NC = [('2^-1+2^-2-2^-3', ['{1/2}+{1/4}-{1/8}', '{4/8}+{2/8}-{1/8}']), ('({2/3})^-2-({1/2})^-1·(-3)^-1', ['{9/4}-2·({-1/3})', '{9/4}+{2/3}', '{27/12}+{8/12}']),
          ('[({1/2})^-2-(-3)^0]^-1', ['[4-1]^-1', '3^-1']), ('({3/4}-{1/2})^-2:(2-{4/3})^-1', ['({1/4})^-2:({2/3})^-1', '16:{3/2}'])]
    S.append((t("Potències d'exponent negatiu", 'Potencias de exponente negativo'), [
     (1, t(r"Calcula el valor d'aquestes potències:", r"Calcula el valor de estas potencias:") + tasks(4, [m(e) for e in N1], gap='8pt')
         + recorda(t(r"$a^0=1$, \ $a^{-n}=\dfrac{1}{a^n}$ \ i \ $\left(\dfrac{a}{b}\right)^{-n}=\left(\dfrac{b}{a}\right)^{n}$ \ (si $a\neq0$). L'exponent negatiu no canvia el signe del resultat: \ $2^{-3}=\frac{1}{8}$, no $-8$.", r"$a^0=1$, \ $a^{-n}=\dfrac{1}{a^n}$ \ y \ $\left(\dfrac{a}{b}\right)^{-n}=\left(\dfrac{b}{a}\right)^{n}$ \ (si $a\neq0$). El exponente negativo no cambia el signo del resultado: \ $2^{-3}=\frac{1}{8}$, no $-8$.")),
         tasks(4, [rsol(e) for e in N1], gap='6pt')),
     (2, t(r"Ordena de menor a major:", r"Ordena de menor a mayor:") + r' $\ ' + r',\ '.join(ORD) + '$.',
         r'$-\frac{1}{2},\ \frac{1}{4},\ -\frac{1}{8},\ 1,\ 4,\ \frac{1}{2}$ \ $\Rightarrow$ \ $\res{(-2)^{-1}<(-2)^{-3}<2^{-2}<2^{-1}<2^{0}<(-2)^{2}}$'),
     (2, t(r"Expressa com una potència de base 2:", r"Expresa como una potencia de base 2:") + tasks(4, ['$' + a + '$' for a, _, _, _ in B2], gap='8pt'),
         tasks(2, ['$' + a + '=' + b + '$' for a, b, _, _ in B2], gap='6pt')),
     (2, t(r"Expressa com una sola potència (amb exponents enters):", r"Expresa como una sola potencia (con exponentes enteros):") + tasks(3, ['$' + a + '$' for a, _ in NP], gap='8pt'),
         tasks(3, ['$' + a + r'=\res{' + b + '}$' for a, b in NP], gap='6pt')),
     (3, t(r"Redueix descomponent en factors primers i calcula:", r"Reduce descomponiendo en factores primos y calcula:") + tasks(3, ['$' + a + '$' for a, _, _, _ in NR], gap='8pt'),
         tasks(1, ['$' + a + '=' + b + '$' for a, b, _, _ in NR], gap='6pt')),
     (3, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in NC], gap='10pt'), tasks(1, [steps(e, *p) for e, p in NC], gap='6pt')),
    ]))
    vals = [F(-2) ** -1, F(2) ** -2, F(-2) ** -3, F(2) ** 0, F(-2) ** 2, F(2) ** -1]
    assert [ORD[i] for i in sorted(range(6), key=lambda i: vals[i])] == [r'(-2)^{-1}', r'(-2)^{-3}', r'2^{-2}', r'2^{-1}', r'2^{0}', r'(-2)^{2}']
    for _, _, a, b in B2 + NR: ck(a, b)
    ck(F(7) ** -3 * 7 ** 5, 7 ** 2); ck(F(3) ** 4 / F(3) ** -2, 3 ** 6); ck(F(5) ** -6, (F(5) ** -2) ** 3); ck(F(2) ** -4 * F(5) ** -4, F(10) ** -4)
    ck(F(3, 4) ** -2 * F(3, 4) ** 5, F(3, 4) ** 3); ck(F(6) ** -3 / F(2) ** -3, F(3) ** -3)
    return S
