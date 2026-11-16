# Exercicis de la fitxa de 4t ESO Matemàtiques A, Unitat 1: Nombres naturals, enters i fraccionaris.
# Una sola llista per a les dues llengües: genera.py (valencià) i genera-es.py (castellà) criden seccions('va'|'es').
# Cada exercici és (estrelles, enunciat, solució). Els resultats es calculen o es comproven ací mateix.
#
# Les expressions s'escriuen amb - · : ^ √ ( ) [ ] i les fraccions entre claus: {3/4}, {-2/5}.
# ev() les avalua amb aritmètica exacta (Fraction) i tx() les passa a LaTeX.
import re
from math import isqrt
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
    s = s.replace('·', '*').replace(':', '/').replace('[', '(').replace(']', ')').replace('^', '**')
    s = re.sub(r'√(\d+)', r'R(\1)', s).replace('√(', 'R(')
    s = re.sub(r'(?<![\w.])(\d+)', r'F(\1)', s)
    def R(x):
        r = isqrt(int(x)); assert r * r == x, e; return F(r)
    env = {'F': F, 'R': R}
    env.update({'Q' + 'abcdefghijklmnop'[i]: v for i, v in enumerate(q)})
    return eval(s, env)
def fr(v):
    """Fraction -> LaTeX"""
    v = F(v)
    if v.denominator == 1: return str(v.numerator)
    return ('-' if v < 0 else '') + r'\frac{%d}{%d}' % (abs(v.numerator), v.denominator)
def tx(e):
    e = re.sub(r'√\(([^()]*)\)', r'\\sqrt{\1}', e)
    e = re.sub(r'√(\d+)', r'\\sqrt{\1}', e)
    e = FRAC.sub(lambda m: m.group(1) + r'\frac{%s}{%s}' % (m.group(2), m.group(3)), e)
    e = re.sub(r'\^(\d+)', r'^{\1}', e)
    e = e.replace('(', r'\left(').replace(')', r'\right)').replace('[', r'\left[').replace(']', r'\right]')
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
    P1 = ['2^5', '10^4', '3^4', '√64', '√121', '15^0']
    C1 = ['18-2·5+3', '(18-2)·5+3', '48:8·2', '48:(8·2)']
    C2 = [('3^2+4·√25-2^3', ['9+20-8']), ('50-[18:(3^2-6)]·4', ['50-[18:3]·4', '50-6·4']),
          ('2·(5^2-3·4)+√81', ['2·(25-12)+9', '2·13+9']), ('(√100+2^3):6+7', ['(10+8):6+7', '18:6+7'])]
    S.append((t('Nombres naturals. Operacions combinades', 'Números naturales. Operaciones combinadas'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(6, [m(e) for e in P1]), tasks(3, [rsol(e) for e in P1])),
     (1, t(r"Calcula el quocient i el residu de cada divisió i fes la prova ($D=d\cdot q+r$):", r"Calcula el cociente y el resto de cada división y haz la prueba ($D=d\cdot q+r$):")
         + tasks(2, [m('347:15'), m('1000:24')]),
         tasks(2, [r'$347=15\cdot\res{23}+\res{2}$', r'$1000=24\cdot\res{41}+\res{16}$'])),
     (1, t(r"Calcula respectant la jerarquia de les operacions:", r"Calcula respetando la jerarquía de las operaciones:") + tasks(4, [m(e) for e in C1]),
         tasks(4, [rsol(e) for e in C1])),
     (2, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in C2])
         + recorda(t(r"Primer els parèntesis (de dins cap a fora); després les potències i les arrels; després les multiplicacions i divisions i, al final, les sumes i restes.", r"Primero los paréntesis (de dentro hacia fuera); después las potencias y las raíces; después las multiplicaciones y divisiones y, al final, las sumas y restas.")),
         tasks(1, [steps(e, *p) for e, p in C2])),
     (2, t(r"Comprem 4 entrades de cine a 15\,€ i 3 menús a 8\,€. Paguem amb un bitllet de 100\,€. Escriu l'operació en una sola expressió i calcula el canvi.", r"Compramos 4 entradas de cine a 15\,€ y 3 menús a 8\,€. Pagamos con un billete de 100\,€. Escribe la operación en una sola expresión y calcula el cambio."),
         steps('100-(4·15+3·8)', '100-(60+24)', '100-84') + r'\,€'),
     (3, t(r"Un alumne ha fet $5+3\cdot2^2=8\cdot2^2=8\cdot4=32$. Explica l'error i fes-ho bé.", r"Un alumno ha hecho $5+3\cdot2^2=8\cdot2^2=8\cdot4=32$. Explica el error y hazlo bien."),
         t(r'Ha sumat abans de fer la potència i el producte. ', r'Ha sumado antes de hacer la potencia y el producto. ') + steps('5+3·2^2', '5+3·4', '5+12')),
     (3, t(r"Un terreny quadrat té una superfície de 900\,m². Volem tancar-lo deixant una porta de 4\,m. Quants metres de tanca calen? Quant costarà si el metre val 12\,€?", r"Un terreno cuadrado tiene una superficie de 900\,m². Queremos vallarlo dejando una puerta de 4\,m. ¿Cuántos metros de valla hacen falta? ¿Cuánto costará si el metro vale 12\,€?"),
         t(r'Costat: $\sqrt{900}=30$\,m. Tanca: $4\cdot30-4=\res{116\text{ m}}$. Cost: $116\cdot12=\res{1392\text{ €}}$.', r'Lado: $\sqrt{900}=30$\,m. Valla: $4\cdot30-4=\res{116\text{ m}}$. Coste: $116\cdot12=\res{1392\text{ €}}$.')),
    ]))
    assert 15 * 23 + 2 == 347 and 24 * 41 + 16 == 1000 and ev('4·√900-4') == 116 and 116 * 12 == 1392

    # =====================================================================
    AB = [('|-15|', 15), ('|8|', 8), ('|0|', 0), (r'\text{op}(-6)', 6), (r'\text{op}(|-9|)', -9), ('|-3|+|-5|', 8)]
    S.append((t('Nombres enters. Valor absolut', 'Números enteros. Valor absoluto'), [
     (1, t(r"Expressa cada situació amb un nombre enter:", r"Expresa cada situación con un número entero:")
         + tasks(1, [t('5 graus baix zero.', '5 grados bajo cero.'), t('El tercer soterrani d\'un aparcament.', 'El tercer sótano de un aparcamiento.'), t('Un guany de 200 €.', 'Una ganancia de 200 €.'),
                     t('Un submarí a 400 m de profunditat.', 'Un submarino a 400 m de profundidad.'), t('L\'any 50 abans de Crist.', 'El año 50 antes de Cristo.')]),
         tasks(5, [r'$\res{-5}$', r'$\res{-3}$', r'$\res{+200}$', r'$\res{-400}$', r'$\res{-50}$'])),
     (1, t(r"Representa en la recta i ordena de menor a major: $\ -7,\ 4,\ 0,\ -12,\ 3,\ -1,\ 9$.", r"Representa en la recta y ordena de menor a mayor: $\ -7,\ 4,\ 0,\ -12,\ 3,\ -1,\ 9$."),
         r'$\res{-12<-7<-1<0<3<4<9}$'),
     (1, t(r"Calcula:", r"Calcula:") + tasks(6, ['$' + e + '$' for e, _ in AB]),
         tasks(3, ['$' + e + r'=\res{%d}$' % v for e, v in AB])),
     (2, t(r"Escriu tots els nombres enters $x$ que compleixen:", r"Escribe todos los números enteros $x$ que cumplen:") + tasks(3, [r'$|x|=7$', r'$|x|<4$', r'$-3<x\le2$'])
         + recorda(t(r"$|x|$ és la distància de $x$ al 0: $|x|=7$ vol dir que $x$ està a 7 unitats del 0, a la dreta o a l'esquerra.", r"$|x|$ es la distancia de $x$ al 0: $|x|=7$ quiere decir que $x$ está a 7 unidades del 0, a la derecha o a la izquierda.")),
         tasks(1, [r'$x=\res{-7}$ ' + t('i', 'y') + r' $x=\res{7}$', r'$\res{-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 3}$', r'$\res{-2,\ -1,\ 0,\ 1,\ 2}$'])),
     (2, t(r"A les 6 del matí el termòmetre marcava $-8$\,°C i a les 14\,h, 5\,°C. a) Quants graus ha pujat la temperatura? b) A les 22\,h havia baixat 9 graus respecte de les 14\,h. Quina temperatura feia?", r"A las 6 de la mañana el termómetro marcaba $-8$\,°C y a las 14\,h, 5\,°C. a) ¿Cuántos grados ha subido la temperatura? b) A las 22\,h había bajado 9 grados respecto de las 14\,h. ¿Qué temperatura hacía?"),
         tasks(2, [steps('5-(-8)', '5+8') + r'\,°C', steps('5-9') + r'\,°C'])),
    ]))
    for e, v in AB:
        if '|' in e and 'op' not in e: assert ev(e.replace('|-15|', '15').replace('|8|', '8').replace('|0|', '0').replace('|-3|', '3').replace('|-5|', '5')) == v

    # =====================================================================
    E1 = ['-8+5', '-6-9', '7-(-4)', '-3+(-11)', '(-6)·(-7)', '8·(-9)', '(-56):8', '(-45):(-9)']
    E2 = [('-(+4)+(-8)-(-6)+4-1', ['-4-8+6+4-1', '10-13']), ('12-25+3-8-(-6)', ['12-25+3-8+6', '21-33']), ('-(-3)+(-1)-(+3)-(-8)', ['3-1-3+8', '11-4'])]
    E3 = [('18:(-3)+2·(-5)', ['-6+(-10)']), ('(-3)·(2-7)+15:(-5)', ['(-3)·(-5)+(-3)', '15-3']), ('4-2·[3-(6-10)]', ['4-2·[3+4]', '4-2·7', '4-14']),
          ('-20:4·(-2)', ['-5·(-2)']), ('25:(-5)-(-3)·(4-6):2', ['-5-(-3)·(-2):2', '-5-6:2', '-5-3']), ('-6-[4-3·(2-5)]', ['-6-[4-3·(-3)]', '-6-[4+9]', '-6-13'])]
    E4 = [('(-2)^3+3^2', ['-8+9']), ('-2^4+(-2)^4', ['-16+16']), ('5-2·√36+(-1)^7', ['5-2·6+(-1)', '5-12-1']),
          ('[(-2)^2-3^2]^2:(-5)', ['[4-9]^2:(-5)', '(-5)^2:(-5)', '25:(-5)']), ('√(25-9)-(-3)^3:9', ['√16-(-27):9', '4-(-3)', '4+3']), ('(-3)^2·2-√49:(-7)', ['9·2-7:(-7)', '18-(-1)', '18+1'])]
    S.append((t('Operacions combinades amb enters', 'Operaciones combinadas con enteros'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(4, [m(e) for e in E1])
         + recorda(t(r"Regla dels signes: $(+)\cdot(+)=+$, \ $(-)\cdot(-)=+$, \ $(+)\cdot(-)=-$, \ $(-)\cdot(+)=-$. També per a la divisió.", r"Regla de los signos: $(+)\cdot(+)=+$, \ $(-)\cdot(-)=+$, \ $(+)\cdot(-)=-$, \ $(-)\cdot(+)=-$. También para la división.")),
         tasks(4, [rsol(e) for e in E1])),
     (1, t(r"Lleva els parèntesis i calcula:", r"Quita los paréntesis y calcula:") + tasks(2, [m(e) for e, _ in E2]),
         tasks(1, [steps(e, *p) for e, p in E2])),
     (2, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in E3]), tasks(1, [steps(e, *p) for e, p in E3])),
     (2, t(r"Calcula pas a pas (amb potències i arrels):", r"Calcula paso a paso (con potencias y raíces):") + tasks(2, [m(e) for e, _ in E4])
         + recorda(t(r"$(-2)^4=16$, però $-2^4=-16$: sense parèntesi, el signe no forma part de la base.", r"$(-2)^4=16$, pero $-2^4=-16$: sin paréntesis, el signo no forma parte de la base.")),
         tasks(1, [steps(e, *p) for e, p in E4])),
     (2, t(r"Un compte bancari té un saldo de 350\,€. Es paguen 4 rebuts de 95\,€ i després s'ingressen 210\,€. Quin és el saldo final? Ha arribat a estar en negatiu?", r"Una cuenta bancaria tiene un saldo de 350\,€. Se pagan 4 recibos de 95\,€ y después se ingresan 210\,€. ¿Cuál es el saldo final? ¿Ha llegado a estar en negativo?"),
         steps('350-4·95+210', '350-380+210') + r'\,€. ' + t(r'Sí: després dels rebuts el saldo era $350-380=\res{-30}$\,€.', r'Sí: después de los recibos el saldo era $350-380=\res{-30}$\,€.')),
     (3, t(r"Un submarí és a $-150$\,m. Puja 60\,m, després baixa el triple del que ha pujat i, finalment, puja 45\,m. A quina profunditat està?", r"Un submarino está a $-150$\,m. Sube 60\,m, después baja el triple de lo que ha subido y, finalmente, sube 45\,m. ¿A qué profundidad está?"),
         steps('-150+60-3·60+45', '-150+60-180+45') + r'\,m'),
     (3, t(r"Les temperatures mínimes d'una setmana han sigut $-3$, $2$, $-5$, $0$, $-4$, $1$ i $-5$\,°C. Calcula la temperatura mitjana i la diferència entre la màxima i la mínima.", r"Las temperaturas mínimas de una semana han sido $-3$, $2$, $-5$, $0$, $-4$, $1$ y $-5$\,°C. Calcula la temperatura media y la diferencia entre la máxima y la mínima."),
         t(r'Mitjana: ', r'Media: ') + steps('(-3+2-5+0-4+1-5):7', '(-14):7') + r'\,°C. \quad ' + t('Diferència: ', 'Diferencia: ') + steps('2-(-5)') + r'\,°C.'),
    ]))

    # =====================================================================
    Q1 = [('{3/5}·80', 48), ('{2/7}·63', 18), ('{5/4}·120', 150)]
    SI = [(18, 24), (40, 64), (84, 126), (105, 180), (90, 126), (150, 250)]
    def simp(a, b):
        g = F(a, b)
        from math import gcd
        return r'$\frac{%d}{%d}=\frac{%d:%d}{%d:%d}=\res{%s}$' % (a, b, a, gcd(a, b), b, gcd(a, b), fr(g))
    S.append((t('Fraccions. Fraccions equivalents', 'Fracciones. Fracciones equivalentes'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(3, [t(r'$\frac{3}{5}$ de 80', r'$\frac{3}{5}$ de 80'), t(r'$\frac{2}{7}$ de 63', r'$\frac{2}{7}$ de 63'), t(r'$\frac{5}{4}$ de 120', r'$\frac{5}{4}$ de 120')]),
         tasks(3, [r'$%s=\res{%d}$' % (tx(e), v) for e, v in Q1])),
     (1, t(r"Simplifica fins a obtindre la fracció irreductible:", r"Simplifica hasta obtener la fracción irreducible:") + tasks(6, [r'$\frac{%d}{%d}$' % ab for ab in SI], gap='8pt')
         + recorda(t(r"Per a arribar directament a la fracció irreductible, dividim el numerador i el denominador entre el seu MCD.", r"Para llegar directamente a la fracción irreducible, dividimos el numerador y el denominador entre su MCD.")),
         tasks(2, [simp(a, b) for a, b in SI], gap='6pt')),
     (1, t(r"Amplifica:", r"Amplifica:") + tasks(1, [t(r'Escriu tres fraccions equivalents a $\frac{2}{5}$.', r'Escribe tres fracciones equivalentes a $\frac{2}{5}$.'),
                                                   t(r'Escriu $\frac{3}{4}$ amb denominador 20 i $\frac{5}{6}$ amb denominador 42.', r'Escribe $\frac{3}{4}$ con denominador 20 y $\frac{5}{6}$ con denominador 42.'),
                                                   t(r'Escriu $\frac{7}{9}$ amb numerador 35.', r'Escribe $\frac{7}{9}$ con numerador 35.')]),
         tasks(1, [r'$\frac{2}{5}=\res{\frac{4}{10}}=\res{\frac{6}{15}}=\res{\frac{8}{20}}$ ' + t('(per exemple)', '(por ejemplo)'),
                   r'$\frac{3\cdot5}{4\cdot5}=\res{\frac{15}{20}}$; \quad $\frac{5\cdot7}{6\cdot7}=\res{\frac{35}{42}}$', r'$\frac{7\cdot5}{9\cdot5}=\res{\frac{35}{45}}$'])),
     (2, t(r"Comprova si són equivalents:", r"Comprueba si son equivalentes:") + tasks(3, [r'$\frac{6}{9}$ ' + t('i', 'y') + r' $\frac{10}{15}$', r'$\frac{4}{7}$ ' + t('i', 'y') + r' $\frac{12}{20}$', r'$\frac{15}{25}$ ' + t('i', 'y') + r' $\frac{9}{15}$'], gap='6pt'),
         tasks(1, [r'$6\cdot15=90=9\cdot10$: \res{' + t('sí', 'sí') + '}', r'$4\cdot20=80\neq7\cdot12=84$: \res{no}', r'$15\cdot15=225=25\cdot9$: \res{' + t('sí', 'sí') + '}'])),
     (2, t(r"Troba el valor de $x$ perquè les fraccions siguen equivalents:", r"Halla el valor de $x$ para que las fracciones sean equivalentes:") + tasks(3, [r'$\frac{x}{12}=\frac{15}{36}$', r'$\frac{8}{x}=\frac{2}{5}$', r'$\frac{14}{21}=\frac{6}{x}$'], gap='6pt'),
         tasks(3, [r'$36x=180\Rightarrow x=\res{5}$', r'$2x=40\Rightarrow x=\res{20}$', r'$14x=126\Rightarrow x=\res{9}$'])),
     (2, t(r"Ordena de menor a major: $\ \frac{3}{4},\ \frac{2}{3},\ \frac{5}{6},\ \frac{7}{12}$.", r"Ordena de menor a mayor: $\ \frac{3}{4},\ \frac{2}{3},\ \frac{5}{6},\ \frac{7}{12}$."),
         t(r'Amb denominador comú 12: $\frac{9}{12},\ \frac{8}{12},\ \frac{10}{12},\ \frac{7}{12}$. \quad ', r'Con denominador común 12: $\frac{9}{12},\ \frac{8}{12},\ \frac{10}{12},\ \frac{7}{12}$. \quad ') + r'$\res{\frac{7}{12}<\frac{2}{3}<\frac{3}{4}<\frac{5}{6}}$'),
    ]))
    for e, v in Q1: assert ev(e) == v
    ck(F(5, 12), F(15, 36)); ck(F(8, 20), F(2, 5)); ck(F(14, 21), F(6, 9)); assert 4 * 20 != 7 * 12 and 15 * 15 == 25 * 9
    assert sorted([F(3, 4), F(2, 3), F(5, 6), F(7, 12)]) == [F(7, 12), F(2, 3), F(3, 4), F(5, 6)]

    # =====================================================================
    O1 = ['{3/10}+{2/5}', '{5/6}-{1/4}', '2-{3/5}', '{7/12}+{5/18}']
    O2 = ['{2/3}·{5/7}', '{4/9}·{3/8}', '{3/5}:{9/10}', '6:{3/4}']
    O3 = ['{-3/4}-{1/6}+2', '({-8/15})·({-25/12})', '{7/10}:(-14)', '{1/2}-{2/3}+{1/6}']
    S.append((t('Operacions amb fraccions', 'Operaciones con fracciones'), [
     (1, t(r"Calcula i simplifica el resultat:", r"Calcula y simplifica el resultado:") + tasks(4, [m(e) for e in O1], gap='8pt')
         + recorda(t(r"Per a sumar o restar, primer reduïm a comú denominador (amb el mcm dels denominadors). Mai no sumem els denominadors!", r"Para sumar o restar, primero reducimos a común denominador (con el mcm de los denominadores). ¡Nunca sumamos los denominadores!")),
         tasks(2, [steps('{3/10}+{2/5}', '{3/10}+{4/10}'), steps('{5/6}-{1/4}', '{10/12}-{3/12}'), steps('2-{3/5}', '{10/5}-{3/5}'), steps('{7/12}+{5/18}', '{21/36}+{10/36}')], gap='6pt')),
     (1, t(r"Calcula i simplifica el resultat:", r"Calcula y simplifica el resultado:") + tasks(4, [m(e) for e in O2], gap='8pt')
         + recorda(t(r"$\frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}$ \qquad $\frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}$ \ (productes creuats)", r"$\frac{a}{b}\cdot\frac{c}{d}=\frac{a\cdot c}{b\cdot d}$ \qquad $\frac{a}{b}:\frac{c}{d}=\frac{a\cdot d}{b\cdot c}$ \ (productos cruzados)")),
         tasks(2, [steps('{2/3}·{5/7}'), steps('{4/9}·{3/8}', '{12/72}'), steps('{3/5}:{9/10}', '{30/45}'), steps('6:{3/4}', '{24/3}')], gap='6pt')),
     (2, t(r"Calcula (compte amb els signes):", r"Calcula (cuidado con los signos):") + tasks(2, [m(e) for e in O3], gap='8pt'),
         tasks(2, [steps('{-3/4}-{1/6}+2', '{-9/12}-{2/12}+{24/12}'), steps('({-8/15})·({-25/12})', '{200/180}'), steps('{7/10}:(-14)', '{-7/140}'), steps('{1/2}-{2/3}+{1/6}', '{3/6}-{4/6}+{1/6}')], gap='6pt')),
     (2, t(r"Escriu l'oposada i la inversa de cada nombre:", r"Escribe la opuesta y la inversa de cada número:") + tasks(3, [r'$\frac{2}{5}$', r'$-\frac{7}{4}$', r'$3$']),
         tasks(3, [t('Op.', 'Op.') + r' $\res{-\frac{2}{5}}$, \ inv. $\res{\frac{5}{2}}$', t('Op.', 'Op.') + r' $\res{\frac{7}{4}}$, \ inv. $\res{-\frac{4}{7}}$', t('Op.', 'Op.') + r' $\res{-3}$, \ inv. $\res{\frac{1}{3}}$'])),
    ]))

    # =====================================================================
    K1 = [('{1/2}+{1/3}·{3/4}', ['{1/2}+{1/4}']), ('({1/2}+{1/3})·{3/4}', ['{5/6}·{3/4}']), ('1-{2/3}:{4/9}', ['1-{3/2}']), ('{3/5}+{2/5}·{10/3}', ['{3/5}+{4/3}', '{9/15}+{20/15}'])]
    K2 = [('{2/5}-({1/2}-{3/4})-1', ['{2/5}-({-1/4})-1', '{8/20}+{5/20}-{20/20}']), ('{4/3}·({2/5}+{1/3})', ['{4/3}·{11/15}']),
          ('({3/4}-1)·8+{1/2}', ['({-1/4})·8+{1/2}', '-2+{1/2}']), ('2-[{1/3}+{1/4}]:{5/6}', ['2-{7/12}:{5/6}', '2-{7/10}'])]
    K3 = [('({2/3})^2-{1/3}·(2-{1/2})', ['{4/9}-{1/3}·{3/2}', '{4/9}-{1/2}']), ('{5/6}:({1/2}-{1/3})-2^2', ['{5/6}:{1/6}-4', '5-4']),
          ('({-1/2})^3+{3/4}:(1-{1/3})', ['{-1/8}+{3/4}:{2/3}', '{-1/8}+{9/8}'])]
    K4 = [('[{3/4}-({1/2})^2]^2:({-1/2})^3+{5/3}·{6/5}', ['[{3/4}-{1/4}]^2:({-1/8})+2', '({1/2})^2:({-1/8})+2', '{1/4}:({-1/8})+2', '-2+2']),
          ('({1/4}+{2/3}-{1/12})·3+({3/2}-{5/4}):{1/2}', ['{10/12}·3+{1/4}:{1/2}', '{5/2}+{1/2}'])]
    S.append((t('Operacions combinades amb fraccions', 'Operaciones combinadas con fracciones'), [
     (1, t(r"Calcula i compara els dos primers resultats:", r"Calcula y compara los dos primeros resultados:") + tasks(4, [m(e) for e, _ in K1], gap='8pt'),
         tasks(2, [steps(e, *p) for e, p in K1], gap='6pt')),
     (2, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(2, [m(e) for e, _ in K2], gap='8pt'), tasks(1, [steps(e, *p) for e, p in K2], gap='6pt')),
     (2, t(r"Calcula pas a pas (amb potències):", r"Calcula paso a paso (con potencias):") + tasks(1, [m(e) for e, _ in K3], gap='8pt')
         + recorda(t(r"Per a elevar una fracció, elevem el numerador i el denominador: $\left(\frac{2}{3}\right)^2=\frac{2^2}{3^2}=\frac{4}{9}$.", r"Para elevar una fracción, elevamos el numerador y el denominador: $\left(\frac{2}{3}\right)^2=\frac{2^2}{3^2}=\frac{4}{9}$.")),
         tasks(1, [steps(e, *p) for e, p in K3], gap='6pt')),
     (3, t(r"Calcula pas a pas:", r"Calcula paso a paso:") + tasks(1, [m(e) for e, _ in K4], gap='8pt'), tasks(1, [steps(e, *p) for e, p in K4], gap='6pt')),
    ]))

    # =====================================================================
    S.append((t('Problemes amb fraccions', 'Problemas con fracciones'), [
     (1, t(r"En una classe de 30 alumnes, $\frac{2}{5}$ venen a l'institut amb autobús. Quants hi venen amb autobús? Quants no?", r"En una clase de 30 alumnos, $\frac{2}{5}$ vienen al instituto en autobús. ¿Cuántos vienen en autobús? ¿Cuántos no?"),
         r'$\frac{2}{5}\cdot30=\res{12}$ ' + t('amb autobús', 'en autobús') + r'; \quad $30-12=\res{18}$ ' + t('no.', 'no.')),
     (1, t(r"He llegit 120 pàgines d'un llibre, que són els $\frac{3}{8}$ del total. Quantes pàgines té el llibre?", r"He leído 120 páginas de un libro, que son los $\frac{3}{8}$ del total. ¿Cuántas páginas tiene el libro?"),
         r'$120:\frac{3}{8}=\frac{120\cdot8}{3}=\res{320}$ ' + t('pàgines.', 'páginas.')),
     (2, t(r"La Laia cobra 1500\,€ al mes. Dedica $\frac{1}{3}$ al lloguer, $\frac{1}{5}$ al menjar i $\frac{1}{10}$ al transport. Quant gasta en cada cosa? Quina fracció del sou li queda? Quants euros són?", r"Laia cobra 1500\,€ al mes. Dedica $\frac{1}{3}$ al alquiler, $\frac{1}{5}$ a la comida y $\frac{1}{10}$ al transporte. ¿Cuánto gasta en cada cosa? ¿Qué fracción del sueldo le queda? ¿Cuántos euros son?"),
         t('Lloguer', 'Alquiler') + r' $\res{500}$\,€, ' + t('menjar', 'comida') + r' $\res{300}$\,€, ' + t('transport', 'transporte') + r' $\res{150}$\,€. \ ' + r'$1-\left(\frac{1}{3}+\frac{1}{5}+\frac{1}{10}\right)=1-\frac{19}{30}=\res{\frac{11}{30}}$; \ $\frac{11}{30}\cdot1500=\res{550}$\,€.'),
     (2, t(r"Un dipòsit de 600 litres està ple. El dilluns se'n gasta $\frac{1}{4}$ i el dimarts, $\frac{2}{3}$ del que quedava. Quants litres queden?", r"Un depósito de 600 litros está lleno. El lunes se gasta $\frac{1}{4}$ y el martes, $\frac{2}{3}$ de lo que quedaba. ¿Cuántos litros quedan?"),
         t('Dilluns', 'Lunes') + r': $\frac{1}{4}\cdot600=150$ L, ' + t('queden', 'quedan') + r' 450 L. \ ' + t('Dimarts', 'Martes') + r': $\frac{2}{3}\cdot450=300$ L. \ ' + t('Queden', 'Quedan') + r' $\res{150\text{ L}}$.'),
     (2, t(r"Una recepta de paella per a 6 persones porta $\frac{3}{4}$ kg d'arròs. Quant d'arròs cal per a 10 persones?", r"Una receta de paella para 6 personas lleva $\frac{3}{4}$ kg de arroz. ¿Cuánto arroz hace falta para 10 personas?"),
         t('Per persona', 'Por persona') + r': $\frac{3}{4}:6=\frac{1}{8}$ kg. \ ' + t('Per a 10', 'Para 10') + r': $10\cdot\frac{1}{8}=\res{\frac{5}{4}\text{ kg}}=1{,}25$ kg.'),
     (3, t(r"En Pau gasta $\frac{3}{8}$ dels diners en roba i $\frac{2}{5}$ del que li queda en un concert. Encara li queden 30\,€. Quants diners tenia?", r"Pau gasta $\frac{3}{8}$ del dinero en ropa y $\frac{2}{5}$ de lo que le queda en un concierto. Todavía le quedan 30\,€. ¿Cuánto dinero tenía?"),
         t(r'Després de la roba li queden $\frac{5}{8}$; en el concert gasta $\frac{2}{5}\cdot\frac{5}{8}=\frac{1}{4}$. Ha gastat $\frac{3}{8}+\frac{1}{4}=\frac{5}{8}$ i li queden $\frac{3}{8}$, que són 30\,€: \ ', r'Después de la ropa le quedan $\frac{5}{8}$; en el concierto gasta $\frac{2}{5}\cdot\frac{5}{8}=\frac{1}{4}$. Ha gastado $\frac{3}{8}+\frac{1}{4}=\frac{5}{8}$ y le quedan $\frac{3}{8}$, que son 30\,€: \ ') + r'$30:\frac{3}{8}=\res{80\text{ €}}$.'),
     (3, t(r"Un ciclista fa $\frac{1}{4}$ d'una etapa al matí i $\frac{2}{3}$ del que li queda a la vesprada. Encara li falten 15\,km. Quants quilòmetres té l'etapa?", r"Un ciclista hace $\frac{1}{4}$ de una etapa por la mañana y $\frac{2}{3}$ de lo que le queda por la tarde. Todavía le faltan 15\,km. ¿Cuántos kilómetros tiene la etapa?"),
         t(r'Falta $\frac{1}{3}$ de $\frac{3}{4}$, és a dir, $\frac{1}{3}\cdot\frac{3}{4}=\frac{1}{4}$ de l\'etapa: \ ', r'Falta $\frac{1}{3}$ de $\frac{3}{4}$, es decir, $\frac{1}{3}\cdot\frac{3}{4}=\frac{1}{4}$ de la etapa: \ ') + r'$15:\frac{1}{4}=\res{60\text{ km}}$.'),
     (3, t(r"Una garrafa plena d'oli pesa 1,5\,kg. Quan n'hem gastat $\frac{2}{3}$ de l'oli, pesa 0,7\,kg. Quant pesa la garrafa buida?", r"Una garrafa llena de aceite pesa 1,5\,kg. Cuando hemos gastado $\frac{2}{3}$ del aceite, pesa 0,7\,kg. ¿Cuánto pesa la garrafa vacía?"),
         t(r'Els $\frac{2}{3}$ de l\'oli pesen $1{,}5-0{,}7=0{,}8$ kg; tot l\'oli, $0{,}8:\frac{2}{3}=1{,}2$ kg. Garrafa: $1{,}5-1{,}2=\res{0{,}3\text{ kg}}$.', r'Los $\frac{2}{3}$ del aceite pesan $1{,}5-0{,}7=0{,}8$ kg; todo el aceite, $0{,}8:\frac{2}{3}=1{,}2$ kg. Garrafa: $1{,}5-1{,}2=\res{0{,}3\text{ kg}}$.')),
    ]))
    ck(F(2, 5) * 30, 12); ck(120 / F(3, 8), 320); ck(1 - F(1, 3) - F(1, 5) - F(1, 10), F(11, 30)); ck(F(11, 30) * 1500, 550)
    ck(600 - 150 - F(2, 3) * 450, 150); ck(F(3, 4) / 6 * 10, F(5, 4)); ck(F(2, 5) * F(5, 8), F(1, 4)); ck(30 / (1 - F(3, 8) - F(1, 4)), 80)
    ck(15 / (F(1, 3) * F(3, 4)), 60); ck(F('1.5') - F('0.8') / F(2, 3), F('0.3'))

    # =====================================================================
    W1 = ['(-3)^2', '-3^2', '(-2)^5', '(-1)^14', '(-10)^3', '7^0']
    W2 = ['({2/3})^3', '({-1/2})^4', '({-3/5})^3', '({5/4})^2', '({-4/7})^1', '({9/11})^0']
    SG = [(r'(-5)^{7}', '-'), (r'(-8)^{10}', '+'), (r'-2^{6}', '-'), (r'\left(-\frac{3}{4}\right)^{9}', '-')]
    W3 = [('(-2)^4-2^4+(-2)^3', ['16-16+(-8)']), ('3·(-1)^5-(-2)^2', ['3·(-1)-4', '-3-4']), ('({1/2})^2+({1/2})^3', ['{1/4}+{1/8}', '{2/8}+{1/8}']), ('1-({-2/3})^2', ['1-{4/9}'])]
    S.append((t('Potències amb base entera i racional', 'Potencias con base entera y racional'), [
     (1, t(r"Calcula:", r"Calcula:") + tasks(6, [m(e) for e in W1]), tasks(3, [rsol(e) for e in W1])),
     (1, t(r"Calcula:", r"Calcula:") + tasks(6, [m(e) for e in W2], gap='8pt')
         + recorda(t(r"$\left(\frac{a}{b}\right)^n=\frac{a^n}{b^n}$. Si la base és negativa, el resultat és positiu amb exponent parell i negatiu amb exponent senar.", r"$\left(\frac{a}{b}\right)^n=\frac{a^n}{b^n}$. Si la base es negativa, el resultado es positivo con exponente par y negativo con exponente impar.")),
         tasks(3, [rsol(e) for e in W2], gap='6pt')),
     (2, t(r"Sense fer el càlcul, digues quin signe té el resultat:", r"Sin hacer el cálculo, di qué signo tiene el resultado:") + tasks(4, ['$' + e + '$' for e, _ in SG]),
         tasks(4, [r'$\res{%s}$' % s for _, s in SG])),
     (2, t(r"Calcula:", r"Calcula:") + tasks(2, [m(e) for e, _ in W3], gap='8pt'), tasks(2, [steps(e, *p) for e, p in W3], gap='6pt')),
     (3, t(r"Deixem caure una pilota des de 9\,m d'altura. Cada vegada que bota, puja $\frac{2}{3}$ de l'altura anterior. A quina altura arriba després del tercer bot?", r"Dejamos caer una pelota desde 9\,m de altura. Cada vez que bota, sube $\frac{2}{3}$ de la altura anterior. ¿A qué altura llega después del tercer bote?"),
         steps('9·({2/3})^3', '9·{8/27}') + r'\,m $\approx2{,}67$\,m'),
    ]))

    # =====================================================================
    U1 = [('5^3·5^4', '5^{7}'), ('2^9:2^4', '2^{5}'), ('(3^2)^5', '3^{10}'), ('4^3·5^3', '20^{3}'), ('18^6:6^6', '3^{6}'), ('(-7)^4·(-7)^3', '(-7)^{7}')]
    U2 = [(r'\left(\frac{2}{5}\right)^3\cdot\left(\frac{2}{5}\right)^4', r'\left(\frac{2}{5}\right)^{7}'), (r'\left(\frac{3}{4}\right)^8:\left(\frac{3}{4}\right)^5', r'\left(\frac{3}{4}\right)^{3}'),
          (r'\left[\left(-\frac{1}{2}\right)^3\right]^2', r'\left(-\frac{1}{2}\right)^{6}'), (r'\left(\frac{2}{3}\right)^4\cdot\left(\frac{9}{4}\right)^4', r'\left(\frac{3}{2}\right)^{4}')]
    U3 = [('(-2)^7:(-2)^4', ['(-2)^3']), ('[(-1)^3]^5·(-1)^2', ['(-1)^15·(-1)^2', '(-1)^17']), ('2^5·2^3:2^6', ['2^8:2^6', '2^2']),
          ('({2/3})^5·({2/3})^2:({2/3})^4', ['({2/3})^7:({2/3})^4', '({2/3})^3']), ('({-1/3})^6:({-1/3})^4', ['({-1/3})^2'])]
    VF = [(r'2^3+2^4=2^7', 'F'), (r'3^2\cdot3^3=3^5', 'V'), (r'(2+3)^2=2^2+3^2', 'F'), (r'(-4)^2=4^2', 'V'), (r'5^0=0', 'F')]
    S.append((t('Propietats de les potències', 'Propiedades de las potencias'), [
     (1, t(r"Expressa com una sola potència:", r"Expresa como una sola potencia:") + tasks(3, ['$' + tx(a) + '$' for a, _ in U1])
         + recorda(t(r"Mateixa base: $a^m\cdot a^n=a^{m+n}$, \ $a^m:a^n=a^{m-n}$. \ Potència de potència: $(a^m)^n=a^{m\cdot n}$. \ Mateix exponent: $a^n\cdot b^n=(a\cdot b)^n$, \ $a^n:b^n=(a:b)^n$.", r"Misma base: $a^m\cdot a^n=a^{m+n}$, \ $a^m:a^n=a^{m-n}$. \ Potencia de potencia: $(a^m)^n=a^{m\cdot n}$. \ Mismo exponente: $a^n\cdot b^n=(a\cdot b)^n$, \ $a^n:b^n=(a:b)^n$.")),
         tasks(3, ['$' + tx(a) + r'=\res{' + b + '}$' for a, b in U1])),
     (1, t(r"Expressa com una sola potència:", r"Expresa como una sola potencia:") + tasks(2, ['$' + a + '$' for a, _ in U2], gap='8pt'),
         tasks(2, ['$' + a + r'=\res{' + b + '}$' for a, b in U2], gap='6pt')),
     (2, t(r"Simplifica aplicant les propietats i calcula:", r"Simplifica aplicando las propiedades y calcula:") + tasks(3, [m(e) for e, _ in U3], gap='8pt'),
         tasks(1, [steps(e, *p) for e, p in U3], gap='6pt')),
     (2, t(r"Vertader o fals? Corregeix les falses:", r"¿Verdadero o falso? Corrige las falsas:") + tasks(3, ['$' + e + '$' for e, _ in VF]),
         tasks(1, [r'\res{F}: $2^3+2^4=8+16=24$', r'\res{V}', r'\res{F}: $(2+3)^2=25$, \ $2^2+3^2=13$', r'\res{V}: ' + t('exponent parell', 'exponente par'), r'\res{F}: $5^0=1$'])),
     (3, t(r"Calcula descomponent les bases en factors primers:", r"Calcula descomponiendo las bases en factores primos:") + tasks(2, [r'$\dfrac{10^4\cdot2^3}{5^3\cdot4^5}$', r'$9^3\cdot27:3^7$'], gap='8pt'),
         tasks(1, [r'$\dfrac{2^4\cdot5^4\cdot2^3}{5^3\cdot2^{10}}=\dfrac{2^7\cdot5^4}{2^{10}\cdot5^3}=\dfrac{5}{2^3}=\res{\frac{5}{8}}$', r'$3^6\cdot3^3:3^7=3^9:3^7=3^2=\res{9}$'], gap='6pt')),
     (3, t(r"Calcula de la manera més ràpida: $\ \left(\frac{4}{9}\right)^2\cdot\left(\frac{3}{2}\right)^4$", r"Calcula de la manera más rápida: $\ \left(\frac{4}{9}\right)^2\cdot\left(\frac{3}{2}\right)^4$"),
         r'$\left(\frac{4}{9}\right)^2=\left[\left(\frac{2}{3}\right)^2\right]^2=\left(\frac{2}{3}\right)^4 \ \Rightarrow\ \left(\frac{2}{3}\cdot\frac{3}{2}\right)^4=1^4=\res{1}$'),
    ]))
    assert 5 ** 3 * 5 ** 4 == 5 ** 7 and 2 ** 9 // 2 ** 4 == 2 ** 5 and 4 ** 3 * 5 ** 3 == 20 ** 3 and 18 ** 6 // 6 ** 6 == 3 ** 6
    ck(F(2, 3) ** 4 * F(9, 4) ** 4, F(3, 2) ** 4); ck(F(10 ** 4 * 2 ** 3, 5 ** 3 * 4 ** 5), F(5, 8)); ck(F(9 ** 3 * 27, 3 ** 7), 9); ck(F(4, 9) ** 2 * F(3, 2) ** 4, 1)
    assert 2 ** 3 + 2 ** 4 == 24 and 3 ** 2 * 3 ** 3 == 3 ** 5
    return S
