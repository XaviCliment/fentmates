# Versió en castellà de genera.py. Genera t3-fitxa-exercicis-es.tex i t3-fitxa-solucions-es.tex (1r ESO, Unitat 3: Nombres enters)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Els resultats de les operacions es calculen ací mateix (ev), per a no equivocar-nos.
import os, re
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
import sys; sys.path.insert(0, os.path.join(HERE, '..', 'comu'))
from castella import preambul, assignatura

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'

def recorda(t): return '\\recorda{%s}' % t

# ---------- aritmètica: les expressions s'escriuen amb - · : ( ) [ ] ----------
def ev(e):
    s = re.sub(r'(\d+)', r'F(\1)', e.replace('·', '*').replace(':', '/').replace('[', '(').replace(']', ')'))
    v = eval(s, {'F': Fraction})
    assert v.denominator == 1, e
    return int(v)
def tx(e): return e.replace('·', r'\cdot ')
def m(e): return '$' + tx(e) + '$'
def num(v): return str(v)
GRP = re.compile(r'[(\[]((?:[^()\[\]]|\([+-]?\d+\))*)[)\]]')  # un grup sense altres grups dins (però pot tindre enters entre parèntesis)
def chain(e):
    """Resol els parèntesis de dins cap a fora i torna «e = pas = … = \\res{resultat}»."""
    steps, cur = [e], e
    while True:
        g = next((x for x in GRP.finditer(cur) if not re.fullmatch(r'[+-]?\d+', x.group(1))), None)
        if not g: break
        v = ev(g.group(1))
        prev = cur[:g.start()]
        rep = num(v) if v >= 0 or not prev or prev[-1] in '([' else '(%d)' % v
        cur = prev + rep + cur[g.end():]
        cur = re.sub(r'^\+', '', cur)
        steps.append(cur)
    r = ev(e)
    if re.fullmatch(r'-?\d+', steps[-1]): steps.pop()
    return '$' + '='.join(tx(s) for s in steps) + r'=\res{%d}$' % r
def flat(e):
    """Lleva els parèntesis dels termes del tipus ±(±n) amb la regla dels signes."""
    def rep(mt):
        o, i, n = mt.group(1) or '+', mt.group(2) or '+', mt.group(3)
        return ('+' if o == i else '-') + n
    f = re.sub(r'([+-]?)\(([+-]?)(\d+)\)', rep, e)
    return re.sub(r'^\+', '', f)
def fsol(e):
    f = flat(e)
    return '$' + tx(e) + ('=' + tx(f) if f != e else '') + r'=\res{%d}$' % ev(e)
def rsol(e): return '$' + tx(e) + r'=\res{%d}$' % ev(e)

S = []  # [(títol, [(estrelles, enunciat, solució)])]

# =====================================================================
REP = [("Un avión sobrevuela la ciudad a 432 pies de altura.", '+432'), ("Esta noche el termómetro ha marcado 6 °C bajo cero.", '-6'),
       ("El coche lo tenemos aparcado en el tercer sótano.", '-3'), ("Sócrates nació en el año 470 antes de Cristo.", '-470'),
       ("Me he gastado todo el dinero (ni tengo ni debo).", '0'), ("Valencia está situada a 15 m sobre el nivel del mar.", '+15'),
       ("En un examen tipo test, cada respuesta incorrecta resta 1 punto.", '-1')]
S.append(("Los números enteros", [
 (1, r"Representa las situaciones siguientes con un número entero:" + tasks(1, [t + r' \dotfill' for t, _ in REP])
     + recorda(r"Primero busca el \textbf{cero} (la referencia): 0\,°C, la planta baja, el nivel del mar, no tener ni deber dinero\ldots{} Lo que está \emph{por encima} es \textbf{positivo} y lo que está \emph{por debajo}, \textbf{negativo}."),
     tasks(4, ['$\\res{%s}$' % v for _, v in REP])),
 (1, r"Describe tres situaciones de la vida real en las que se utilizan los números negativos.",
     r"Por ejemplo: temperaturas bajo cero ($-5$\,°C), sótanos de un edificio ($-2$), deudas o saldos negativos ($-30$\,€), profundidades bajo el nivel del mar ($-200$\,m), años antes de Cristo ($-470$), goles en contra\ldots"),
 (1, r"Escribe una situación que se pueda representar con cada entero:" + tasks(5, [r"$-12$", r"$+8$", r"$-1500$", r"$+2026$", r"$-4$"]),
     r"Hay muchas respuestas. Por ejemplo: \ a) un buceador a 12\,m de profundidad; \ b) la planta 8 de un edificio; \ c) un submarino a 1500\,m de profundidad; \ d) el año 2026 d.\,C.; \ e) hace 4\,°C bajo cero."),
 (1, r"Clasifica estos enteros en \emph{positivos}, \emph{negativos} y \emph{ni positivos ni negativos}. ¿Cuáles son también números naturales? \[-7\qquad 12\qquad 0\qquad +3\qquad -25\qquad 1\qquad -1\qquad 100\]",
     r"Positivos: $12,\ +3,\ 1,\ 100$. \ Negativos: $-7,\ -25,\ -1$. \ Ni positivo ni negativo: $0$. \ Naturales: $\res{12,\ +3,\ 1,\ 100,\ 0}$."),
 (2, r"Escribe el entero anterior y el siguiente de cada número:" + tasks(5, [r"$5$", r"$-1$", r"$0$", r"$-10$", r"$-99$"]),
     tasks(5, [r"$4$ y $6$", r"$-2$ y $0$", r"$-1$ y $1$", r"$-11$ y $-9$", r"$-100$ y $-98$"])),
 (2, r"Escribe todos los enteros comprendidos entre:" + tasks(3, [r"$-4$ y $3$", r"$-10$ y $-6$", r"$-2$ y $2$"]),
     tasks(3, [r"$\res{-3,-2,-1,0,1,2}$", r"$\res{-9,-8,-7}$", r"$\res{-1,0,1}$"])),
 (3, r"¿Cuántos enteros hay comprendidos entre $-50$ y $50$? ¿Y entre $-50$ y $0$?",
     r"Del $-49$ al $-1$ hay 49, el 0 y del 1 al 49, 49 más: $49+1+49=\res{99}$. \ Entre $-50$ y $0$: del $-49$ al $-1$, $\res{49}$."),
]))

PTS3 = [-2, 0, 4, -1, 8, -3, -7, 1]
PTS4 = [-7, 3, 1, -4, 6, -5, -2, 0]
CMP = [('-6', '6'), ('0', '-1'), ('10', '-1'), ('8', '3'), ('-8', '-9'), ('1', '-2'), ('-15', '-51'), ('-100', '1')]
def cmpsym(a, b): a, b = int(a), int(b); return '<' if a < b else '>' if a > b else '='
S.append(("Recta numérica, orden y comparación", [
 (1, r"Representa en la recta numérica los números: \ $-2,\ 0,\ 4,\ -1,\ 8,\ -3,\ -7$ \ y \ $1$.\par\smallskip{\centering\rectabuida{-9}{9}\par}"
     + recorda(r"Los \textbf{positivos} van a la \textbf{derecha} del cero y los \textbf{negativos}, a la \textbf{izquierda}. Cuanto más a la derecha, mayor es el número."),
     r"\par\smallskip{\centering\recta{-9}{9}{%s}\par}" % ','.join(map(str, PTS3))),
 (1, r"Representa en la recta numérica estos números y ordénalos de menor a mayor: \[-7\qquad 3\qquad 1\qquad -4\qquad 6\qquad -5\qquad -2\qquad 0\]{\centering\rectabuida{-9}{9}\par}",
     r"\par\smallskip{\centering\recta{-9}{9}{%s}\par}\[\res{%s}\]" % (','.join(map(str, PTS4)), '<'.join(map(str, sorted(PTS4))))),
 (1, r"Ordena los números siguientes de mayor a menor: \ $-7,\ 0,\ 1,\ -1,\ 8,\ -4,\ -9,\ 3$.",
     r"$\res{%s}$" % '>'.join(map(str, sorted([-7, 0, 1, -1, 8, -4, -9, 3], reverse=True)))),
 (1, r"Compara las parejas de números con el signo $<$, $>$ o $=$:" + tasks(4, [r"$%s\ \square\ %s$" % p for p in CMP]),
     tasks(4, [r"$%s\res{%s}%s$" % (a, cmpsym(a, b), b) for a, b in CMP])),
 (2, r"Escribe un entero comprendido entre:" + tasks(4, [r"$-5$ y $-2$", r"$-1$ y $1$", r"$-13$ y $-11$", r"$-100$ y $-98$"]),
     tasks(4, [r"$-4$ o $-3$", r"$\res{0}$", r"$\res{-12}$", r"$\res{-99}$"])),
 (2, r"¿Qué entero está\ldots" + tasks(2, [r"5 unidades a la izquierda de $2$?", r"7 unidades a la derecha de $-4$?", r"3 unidades a la izquierda de $-6$?", r"a 4 unidades del $0$? (hay dos)"]),
     tasks(4, [r"$\res{-3}$", r"$\res{3}$", r"$\res{-9}$", r"$\res{4}$ y $\res{-4}$"])),
 (3, r"¿Verdadero o falso? Justifícalo:" + tasks(1, [r"Todo número negativo es menor que cero.", r"$-20>-2$.", r"Entre $-3$ y $3$ hay 5 enteros.", r"El mayor de los números negativos es $-1$.", r"Si $a<b$, entonces $-a>-b$."]),
     tasks(1, [r"\res{\text{V}}: los negativos están a la izquierda del cero.", r"\res{\text{F}}: $-20$ está más a la izquierda, $-20<-2$.", r"\res{\text{V}}: $-2,\ -1,\ 0,\ 1,\ 2$.", r"\res{\text{V}}: es el negativo más próximo al cero.", r"\res{\text{V}}: cambiar el signo es como mirar la recta en un espejo: por ejemplo, $2<5$ y $-2>-5$."])),
]))

ABS = ['-5', '-1', '0', '8', '-23', '7']
OPS = ['-8', '-3', '0', '4', '-100', '15']
CMP2 = [(r'|-3|', 3, '3', 3), (r'\text{op}(-2)', 2, '-1', -1), (r'|-2|', 2, '|-1|', 1), (r'\text{op}(\text{op}(-1))', -1, '0', 0), (r'|-4|', 4, r'\text{op}(2)', -2), ('-8', -8, r'\text{op}(8)', -8)]
def sy(a, b): return '<' if a < b else '>' if a > b else '='
S.append(("Valor absoluto y opuesto", [
 (1, r"Calcula el valor absoluto de los números siguientes:" + tasks(6, [r"$|%s|$" % x for x in ABS])
     + recorda(r"El \textbf{valor absoluto} de un número es la \textbf{distancia} de ese número al 0: \ $|-5|=|5|=5$. Nunca es negativo."),
     tasks(3, [r"$|%s|=\res{%d}$" % (x, abs(int(x))) for x in ABS])),
 (1, r"Calcula el opuesto de los números siguientes:" + tasks(6, [r"$\text{op}(%s)$" % x for x in OPS])
     + recorda(r"El \textbf{opuesto} de un número es el que está a la \textbf{misma distancia} del cero, pero al otro lado: cambiamos el signo. \ $\text{op}(-8)=8$, \ $\text{op}(4)=-4$."),
     tasks(3, [r"$\text{op}(%s)=\res{%d}$" % (x, -int(x)) for x in OPS])),
 (1, r"Dos números opuestos se encuentran a una distancia de $36$ unidades el uno del otro. ¿Qué números son?",
     r"Cada uno está a la mitad de la distancia del cero: $36:2=18$. \ Son $\res{18}$ y $\res{-18}$."),
 (2, r"Ordena de menor a mayor los números siguientes, haciendo antes los cálculos: \[3\qquad \text{op}(4)\qquad |-6|\qquad 1\qquad \text{op}(5)\qquad -2\qquad |7|\qquad |-2|\qquad 0\qquad 5\]",
     r"$\text{op}(4)=-4$, \ $|-6|=6$, \ $\text{op}(5)=-5$, \ $|7|=7$, \ $|-2|=2$: \[\res{\text{op}(5)<\text{op}(4)<-2<0<1<|-2|<3<5<|-6|<|7|}\]"),
 (2, r"Compara las parejas de números:" + tasks(3, [r"$%s\ \square\ %s$" % (a, c) for a, _, c, _ in CMP2]),
     tasks(3, [r"$%s\res{%s}%s$" % (a, sy(b, d), c) for a, b, c, d in CMP2]) + r"\par (Valores: $3=3$; \ $2>-1$; \ $2>1$; \ $-1<0$; \ $4>-2$; \ $-8=-8$.)"),
 (3, r"Completa los huecos con el número o los números que correspondan:" + tasks(3, [r"$\text{op}(\text{op}(\square))=-7$", r"$|\square|=10$", r"$\text{op}(|\square|)=-2$", r"$|\text{op}(-8)|=\square$", r"$\text{op}(|-4|)=\square$", r"$|\square|=\text{op}(5)$"]),
     tasks(3, [r"$\res{-7}$", r"$\res{10}$ o $\res{-10}$", r"$\res{2}$ o $\res{-2}$", r"$\res{8}$", r"$\res{-4}$", r"Ninguno: $\text{op}(5)=-5$ y un valor absoluto nunca es menor que 0."])),
 (3, r"¿Qué enteros tienen valor absoluto menor que $4$? ¿Y cuáles tienen valor absoluto menor o igual que $2$?",
     r"$\res{-3,\ -2,\ -1,\ 0,\ 1,\ 2,\ 3}$. \qquad $\res{-2,\ -1,\ 0,\ 1,\ 2}$."),
]))

E13 = ['5-7', '-8-9', '-3+7', '4-3', '-5+1', '10-14', '-7+5', '9-13', '3+10', '9-4', '-5-5', '-4+4', '-3-2', '8+12', '-5+15']
E15 = ['10-3-5', '15-9-6', '5-8+4', '9-3+5', '-2+2+7', '-10+8+6', '-10-3+8', '-4-3-2', '-1-5-7', '9-2-3', '12-4-6', '3-7+4', '5-9+8', '-13+6+4', '-2+10-15', '-11-4+8', '-5-3-4', '-8+5+6']
E16 = ['5+7-2-4', '2-6+4-9', '9-6-7+2', '-4-5+3+8', '-8+2-7+6', '-1+5+6-7', '4-1-2-11', '-2+6-8-1', '-1+2+17-12', '-24+15+13-8', '-18-10+12+1', '11-15-13-2']
def grouped(e):
    t = re.findall(r'[+-]?\d+', e); p = [int(x) for x in t if int(x) > 0]; n = [-int(x) for x in t if int(x) < 0]
    if not p or not n: return rsol(e)
    return '$' + tx(e) + '=%d-%d' % (sum(p), sum(n)) + r'=\res{%d}$' % ev(e)
MISS = [(r"-3+\square=5", 8), (r"\square-7=-2", 5), (r"4+\square=-6", -10), (r"\square+9=0", -9), (r"-8-\square=-3", -5), (r"\square-(-4)=1", -3)]
S.append(("Suma y resta de enteros", [
 (1, r"Calcula:" + tasks(5, [m(e) for e in E13])
     + recorda(r"\textbf{Mismo signo}: se suman y se pone el signo común ($-3-5=-8$). \ \textbf{Signos diferentes}: se restan (grande menos pequeño) y se pone el signo del que tiene mayor valor absoluto ($-7+4=-3$)."),
     tasks(5, [rsol(e) for e in E13])),
 (1, r"Calcula:" + tasks(6, [m(e) for e in E15]),
     tasks(3, [grouped(e) for e in E15])),
 (2, r"Calcula:" + tasks(4, [m(e) for e in E16])
     + recorda(r"Puedes agrupar: suma todos los positivos, suma todos los negativos y resta: \ $5-9+8-2=(5+8)-(9+2)=13-11=2$."),
     tasks(3, [grouped(e) for e in E16])),
 (2, r"Calcula de dos maneras, de izquierda a derecha y agrupando positivos y negativos:" + tasks(2, [m('12-4-6+9-15'), m('-7+3-8+10-2+5')]),
     tasks(1, [r"$12-4-6+9-15=8-6+9-15=2+9-15=11-15=\res{-4}$; \quad $(12+9)-(4+6+15)=21-25=\res{-4}$",
               r"$-7+3-8+10-2+5=-4-8+10-2+5=-12+10-2+5=-2-2+5=-4+5=\res{1}$; \quad $(3+10+5)-(7+8+2)=18-17=\res{1}$"])),
 (3, r"Halla el número que falta:" + tasks(3, ['$%s$' % q for q, _ in MISS]),
     tasks(3, [r"$\square=\res{%d}$" % a for _, a in MISS])),
]))
assert ev('12-4-6+9-15') == -4 and ev('-7+3-8+10-2+5') == 1 and ev('-8-(-5)') == -3 and ev('-3-(-4)') == 1

E14 = ['(-6)+(-3)', '(+7)+(-4)', '(-8)+(+1)', '(-3)+(-7)', '(+12)+(+5)', '(+3)+(-5)', '(+3)+(+4)', '(+4)+(-6)', '(+7)+(-8)', '(-5)+(+4)', '(-9)+(+3)', '(+1)+(-1)', '(-7)+(+7)', '(-12)+(-3)', '(+7)+(+5)', '(-4)+(-10)', '(+6)+(-12)', '(-9)+(+15)']
E17 = ['3-(-1)', '-8+(-17)', '-4-(-7)', '-(-5)+3', '8+(-14)', '(-2)-(+3)+(-6)', '-(-5)+(-4)-(-10)', '-15-(-3)+7', '(-8)+(-3)-(-17)+(+1)', '-2-(-3)+7-8', '-(-3)+(-1)-(+3)-(-8)', '-3+(-6)-4+1', '12-25+3-8-(-6)', '-7+4-(-8)+(-3)', '-(+4)+(-8)-(-6)+4-1', '-8+(-3)+4-7-5', '-(-6)+(-1)-7+(-3)', '15-(+3)-6+3-12']
E18 = ['12+(+3-5)', '14+(+12-10)', '6-(9-7)', '15-(2-9)', '11-(-6+3)', '10-(-7-5)', '13+(-8+2)', '17+(-5-9)', '1+(-3+8)', '9-(2-1)', '-6-(2-7)', '11+(-1-3)', '6+(6+3)', '-5-(-2-8)', '3+(-8+7)', '15+(-6-8)']
E19 = ['(7-4)+(9-5)', '(2+6)+(5-8)', '(5-9)+(2-12)', '(7+3)-(5+4)', '(8-12)-(2-5)', '(10-7)-(-2-6)', '-(8+4)+(5-9)', '-(6-2)-(7-9)', '(-8-2)+(-1-5)', '(7-1)-(-5+11)', '(15-8)+(-6-12)', '(-2+3)-(8-4)', '(17-12)-(-7-8)', '(-10+3)-(2-9)', '-(6-4)+(8+1)', '-(-7-1)-(2-10)']
E20 = ['6+[5+(7+2)]', '8+[4-(3+5)]', '10-[6+(2+7)]', '15-[2-(6-10)]', '15-[10-(8+4)]', '12-[7-(2-10)]', '(-6)+[5+(2-12)]', '(-7)-[3-(4-9)]', '(2-10)+[5-(8+2)]', '(12-3)-[1-(2-6)]', '[9-(+5)]+[7+(-10)]', '[10-(-2)]-[5-(+12)]', '[8-(6+4)]-(5-7)', '[1+(6-9)]-(8-12)', '2-[6-(-1-21)]', '-1+[-5-(2-13)]']
S.append(("Paréntesis y corchetes", [
 (1, r"Calcula, eliminando previamente los paréntesis:" + tasks(3, [m(e) for e in E14])
     + recorda(r"Regla de los signos para quitar paréntesis: \ $+(+\ \to\ +$ \qquad $+(-\ \to\ -$ \qquad $-(+\ \to\ -$ \qquad $-(-\ \to\ +$"),
     tasks(3, [fsol(e) for e in E14])),
 (2, r"Calcula, eliminando previamente los paréntesis:" + tasks(2, [m(e) for e in E17]),
     tasks(1, [fsol(e) for e in E17])),
 (2, r"Calcula, resolviendo previamente los paréntesis:" + tasks(4, [m(e) for e in E18])
     + recorda(r"Resuelve primero la operación de dentro del paréntesis, o bien quítalo: si delante hay un $-$, cambia el signo de \textbf{todos} los términos de dentro: \ $6-(9-7)=6-9+7=4$."),
     tasks(2, [chain(e) for e in E18])),
 (2, r"Calcula, resolviendo previamente los paréntesis:" + tasks(3, [m(e) for e in E19]),
     tasks(2, [chain(e) for e in E19])),
 (3, r"Calcula, empezando por los paréntesis de dentro:" + tasks(3, [m(e) for e in E20]),
     tasks(1, [chain(e) for e in E20])),
]))

E22 = ['(-4)·(+7)', '(+2)·(+6)', '(-5)·(-7)', '(+3)·(-8)', '(-9)·(-3)', '(-6)·(+4)', '3·(-2)', '4·(+5)', '8·(-6)', '-5·(+3)', '-2·(-4)', '-6·(+3)', '(+3)·(-5)·(+2)', '(-4)·(-1)·(+6)', '(-2)·(-7)·(-2)', '(+5)·(-4)·(-3)', '(-8)·4·(-6)', '5·3·(-9)·4']
E24 = ['(-8):(+2)', '(+20):(-10)', '(-12):(-4)', '(-4):(+2)', '(+21):(-7)', '(-12):(+6)', '(-15):(-3)', '(+32):(+8)', '(-36):(+9)', '(+42):(-7)', '(-48):(-8)', '(+54):(+6)', '[(+80):(-8)]:(-5)', '[(-70):(-2)]:(-7)', '(+50):[(-30):(+6)]', '(-40):[(+24):(+3)]']
E23 = [(r"(-6)\cdot(\ \square\ )=-18", 3), (r"(\ \square\ )\cdot(-3)=-24", 8), (r"(\ \square\ )\cdot(-5)=+35", -7), (r"(+15)\cdot(\ \square\ )=+60", 4), (r"(-8)\cdot(\ \square\ )=40", -5), (r"(\ \square\ )\cdot7=-77", -11)]
LR = {'24:(-2)·(-3)': '(-12)·(-3)', '(-70)·(-5):(+2)': '350:(+2)', '(+100):(+4)·(-2)': '25·(-2)'}
E25 = ['[(+6)·(-4)]:(-3)', '[(-15)·(-2)]:(+6)', '(-5)·[(+12):(-3)]', '[(-5)·(+12)]:(-3)', '24:(-2)·(-3)', '(-40)·[(-10):(-5)]', '(-70)·(-5):(+2)', '(+100):(+4)·(-2)']
S.append(("Multiplicación y división", [
 (1, r"Resuelve las multiplicaciones siguientes:" + tasks(3, [m(e) for e in E22])
     + recorda(r"Regla de los signos: \ $+\cdot+\ \to\ +$ \qquad $+\cdot-\ \to\ -$ \qquad $-\cdot+\ \to\ -$ \qquad $-\cdot-\ \to\ +$. \ Para la división es igual."),
     tasks(3, [rsol(e) for e in E22])),
 (1, r"Calcula:" + tasks(3, [m(e) for e in E24]),
     tasks(2, [chain(e) for e in E24])),
 (2, r"Halla el número que falta:" + tasks(3, ['$%s$' % q for q, _ in E23]),
     tasks(6, [r"$\res{%d}$" % a for _, a in E23])),
 (2, r"Calcula (las multiplicaciones y divisiones seguidas se hacen de izquierda a derecha):" + tasks(4, [m(e) for e in E25]),
     tasks(2, [chain(e) if '[' in e else '$' + tx(e) + '=' + tx(LR[e]) + r'=\res{%d}$' % ev(e) for e in E25])),
 (3, r"Halla dos números enteros que cumplan, en cada caso:" + tasks(1, [r"El producto es $-12$ y la suma es $1$.", r"El producto es $18$ y la suma es $-9$.", r"El producto es $-20$ y la suma es $-1$."]),
     tasks(3, [r"$\res{4}$ y $\res{-3}$", r"$\res{-3}$ y $\res{-6}$", r"$\res{4}$ y $\res{-5}$"])),
 (3, r"Sin hacer los cálculos, di qué signo tendrá el resultado. Después, compruébalo:" + tasks(1, [m('(-1)·(-2)·(-3)·(-4)'), m('(-5)·(+2)·(-1)·(-3)·(+4)'), r"El producto de siete factores iguales a $-1$."]),
     tasks(1, [r"Cuatro factores negativos (par): \res{+}. \ $%d$" % ev('(-1)·(-2)·(-3)·(-4)'), r"Tres factores negativos (impar): \res{-}. \ $%d$" % ev('(-5)·(+2)·(-1)·(-3)·(+4)'), r"Siete factores negativos (impar): \res{-}. \ $-1$"])),
]))

E26a = ['(-8)·(+2)+(-5)·(-3)', '(+40):(-8)-(-30):(+6)', '(-2)·(-9)+(-24):(-3)-(-6)·4', '(+27):(-3)-(+3)·(-5)-(-6)·(-2)', '(-3)·[(-2)+(-4)]', '(+4)·[(-5)+(+2)]', '(+6):[(+5)-(+7)]', '(-20):[(-6)-(-2)]']
E26b = ['[(-8)+(+7)]·(-3)', '[(-9)+(-3)]:(+6)', '19-(-3)·[5-(+8)]', '12+(-5)·[8+(-9)]', '12-[13-(-7)]:(-5)', '10-(+20):[7+(-3)]', '(-2)·(5-7)-(-3)·(8-6)', '(9-6)·(-2)+(13+3):(-4)']
E27 = ['-2·[3-(-4+6)·(-2)]+15:(-5)', '[(-3)·4-(-2)·5]:(-2)', '18:[-7-(-4)]-(-2)·[5-3·(-1)]', '(-4)·[6-2·(3-7)]-[-10:(-5)]']
# per als combinats, escrivim a mà el pas intermedi principal i comprovem el resultat
MID = {'(-8)·(+2)+(-5)·(-3)': '-16+15', '(+40):(-8)-(-30):(+6)': '-5-(-5)', '(-2)·(-9)+(-24):(-3)-(-6)·4': '18+8-(-24)', '(+27):(-3)-(+3)·(-5)-(-6)·(-2)': '-9-(-15)-12',
       '(-3)·[(-2)+(-4)]': '(-3)·(-6)', '(+4)·[(-5)+(+2)]': '(+4)·(-3)', '(+6):[(+5)-(+7)]': '(+6):(-2)', '(-20):[(-6)-(-2)]': '(-20):(-4)',
       '[(-8)+(+7)]·(-3)': '(-1)·(-3)', '[(-9)+(-3)]:(+6)': '(-12):(+6)', '19-(-3)·[5-(+8)]': '19-(-3)·(-3)=19-9', '12+(-5)·[8+(-9)]': '12+(-5)·(-1)=12+5',
       '12-[13-(-7)]:(-5)': '12-20:(-5)=12-(-4)', '10-(+20):[7+(-3)]': '10-20:4=10-5', '(-2)·(5-7)-(-3)·(8-6)': '(-2)·(-2)-(-3)·2=4+6', '(9-6)·(-2)+(13+3):(-4)': '3·(-2)+16:(-4)=-6-4',
       '-2·[3-(-4+6)·(-2)]+15:(-5)': '-2·[3-2·(-2)]+15:(-5)=-2·7+(-3)=-14-3', '[(-3)·4-(-2)·5]:(-2)': '[-12+10]:(-2)=(-2):(-2)',
       '18:[-7-(-4)]-(-2)·[5-3·(-1)]': '18:(-3)-(-2)·8=-6+16', '(-4)·[6-2·(3-7)]-[-10:(-5)]': '(-4)·[6+8]-2=-56-2'}
for k, v in MID.items():
    for part in v.split('='): assert ev(part) == ev(k), (k, part)
def msol(e): return '$' + tx(e) + '=' + tx(MID[e]) + r'=\res{%d}$' % ev(e)
S.append(("Operaciones combinadas", [
 (1, r"Calcula:" + tasks(2, [m(e) for e in E26a])
     + recorda(r"Orden de las operaciones: \ 1) paréntesis y corchetes (de dentro hacia fuera); \ 2) multiplicaciones y divisiones, de izquierda a derecha; \ 3) sumas y restas."),
     tasks(1, [msol(e) for e in E26a])),
 (2, r"Calcula:" + tasks(2, [m(e) for e in E26b]),
     tasks(1, [msol(e) for e in E26b])),
 (3, r"Calcula:" + tasks(2, [m(e) for e in E27]),
     tasks(1, [msol(e) for e in E27])),
 (3, r"Pon paréntesis donde haga falta para que las igualdades sean ciertas:" + tasks(3, [r"$6-4\cdot2-5=-6$", r"$-3+5\cdot2-4=0$", r"$10-2\cdot3+1=2$"]),
     tasks(3, [r"$\res{(6-4)\cdot(2-5)}=-6$", r"$\res{(-3+5)}\cdot2-4=0$", r"$10-2\cdot\res{(3+1)}=2$"])),
]))
assert ev('(6-4)·(2-5)') == -6 and ev('(-3+5)·2-4') == 0 and ev('10-2·(3+1)') == 2

PROB = [
 (1, r"¿Qué diferencia de temperatura soporta una persona que pasa de la cámara de conservación de las verduras, que se encuentra a $4$\,°C, a la del pescado congelado, que está a $-18$\,°C? ¿Y si pasa de la cámara del pescado a la de las verduras?",
     r"$-18-4=\res{-22}$\,°C (baja 22 grados). \ $4-(-18)=4+18=\res{+22}$\,°C (sube 22 grados)."),
 (1, r"Mónica sale en el ascensor desde la planta cero de su edificio. El ascensor sube 5 plantas, después baja 3, sube 5, baja 8, sube 10, sube 5 y baja 6. ¿En qué planta está?",
     r"$0+5-3+5-8+10+5-6=25-17=\res{8}$: \ está en la planta 8."),
 (1, r"Juan le debe 14 euros a su hermana. Si le paga 9 euros, ¿cuánto le debe?",
     r"$-14+9=-5$: \ todavía le debe $\res{5\text{ €}}$."),
 (1, r"En una estación de esquí, el termómetro marcaba $14$\,° bajo cero a las 8 de la mañana; al mediodía la temperatura había subido 10 grados y a las 19.00 había bajado 5 grados respecto al mediodía. ¿Qué temperatura hacía a las 19.00?",
     r"$-14+10-5=\res{-9}$\,°C."),
 (1, r"Si estaba buceando a una profundidad de 2 metros y ahora estoy sobre un acantilado a 8 m de altura, ¿qué distancia hay entre los dos lugares?",
     r"$8-(-2)=8+2=\res{10\text{ m}}$."),
 (1, r"El primer mes del año la gasolina bajó 5 céntimos, el segundo subió 3 céntimos, el tercero subió 8 céntimos y el cuarto bajó 2 céntimos. Exprésalo con números enteros y calcula la variación total del precio en este tiempo.",
     r"$-5+3+8-2=11-7=\res{+4}$: \ ha subido 4 céntimos."),
 (2, r"Un día de invierno, la temperatura a las seis de la mañana era de $3$\,° bajo cero. Al mediodía había subido 9 grados, pero a las doce de la noche el termómetro marcaba $1$\,° bajo cero. ¿Qué diferencia de temperatura ha habido entre el mediodía y la medianoche?",
     r"Al mediodía: $-3+9=6$\,°C. \ Diferencia: $-1-6=\res{-7}$\,°C: \ ha bajado 7 grados."),
 (2, r"Euclides fue un matemático que vivió 60 años y murió en el año 265 a.\,C. ¿En qué año nació?",
     r"$-265-60=-325$: \ nació en el año $\res{325\text{ a.\,C.}}$"),
 (2, r"El Mulhacén, el pico más alto de la península ibérica, mide $3478$ metros de altura. El Sistema del Trave, una de las simas más profundas del mundo, llega a $1441$ metros de profundidad. Halla la diferencia de altitud entre los dos puntos.",
     r"$3478-(-1441)=3478+1441=\res{4919\text{ m}}$."),
 (2, r"Pablo tenía 850 euros en su cartilla de ahorros. Ha ingresado 250 euros cada mes durante los 5 últimos meses y después sacó 2300 para pagar al carpintero. ¿Qué saldo le queda?",
     r"$850+5\cdot250-2300=850+1250-2300=\res{-200\text{ €}}$: \ la cuenta está en descubierto (debe 200\,€)."),
 (3, r"Arquímedes nació en el año 287 a.\,C. y murió en el año 212 a.\,C. ¿Cuántos años vivió?",
     r"$-212-(-287)=-212+287=\res{75\text{ años}}$."),
 (3, r"Un submarino se encuentra a 120 m de profundidad. Sube 45 m y después baja el triple de lo que ha subido. ¿A qué profundidad se encuentra ahora?",
     r"$-120+45-3\cdot45=-120+45-135=\res{-210}$: \ a 210\,m de profundidad."),
 (3, r"En un examen tipo test, cada respuesta correcta suma 3 puntos, cada respuesta incorrecta resta 2 y cada pregunta en blanco vale 0. Lucía ha acertado 11, ha fallado 6 y ha dejado 3 en blanco. ¿Qué puntuación ha obtenido? ¿Cuántas debería haber acertado, como mínimo, para no tener una puntuación negativa si hubiera fallado 9 y hubiera dejado 3 en blanco?",
     r"$11\cdot3+6\cdot(-2)+3\cdot0=33-12=\res{21\text{ puntos}}$. \ Fallar 9 resta $18$: hay que sumar al menos 18, es decir, $18:3=\res{6}$ aciertos (quedan $20-9-3=8$, así que es posible)."),
]
assert ev('0+5-3+5-8+10+5-6') == 8 and ev('-14+10-5') == -9 and ev('-5+3+8-2') == 4 and ev('850+5·250-2300') == -200 and ev('-120+45-3·45') == -210 and ev('11·3+6·(-2)') == 21
PROB[0] = (PROB[0][0], PROB[0][1] + recorda(r"Escribe cada dato como un entero \textbf{con su signo} (\emph{sube, gana, sobre cero} $\to +$; \ \emph{baja, pierde, debe, bajo cero} $\to -$). Para calcular una \textbf{diferencia} o variación: \ \textbf{valor final} $-$ \textbf{valor inicial}."), PROB[0][2])
S.append(("Problemas con enteros", PROB))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recuerda:}\ #1\end{tcolorbox}}
% recta numèrica entera: \rectabuida{min}{max} i \recta{min}{max}{punts}
\newcommand{\rectabase}[2]{\draw[latex-latex,muted] (#1-0.8,0)--(#2+0.8,0);
  \foreach \i in {#1,...,#2}{\draw[muted] (\i,0.12)--(\i,-0.12) node[below=-1pt,font=\scriptsize,text=muted]{$\i$};}}
\newcommand{\rectabuida}[2]{\begin{tikzpicture}[x=0.78cm,baseline=0]\rectabase{#1}{#2}\end{tikzpicture}}
\newcommand{\recta}[3]{\begin{tikzpicture}[x=0.78cm,baseline=0]\rectabase{#1}{#2}
  \foreach \p in {#3}{\fill[accent] (\p,0) circle (0.11) node[above=1pt,font=\small\bfseries,text=navy]{$\p$};}\end{tikzpicture}}
'''

def tidy(t):
    """Valor absolut amb \lvert…\rvert i signe menys unari després d'un espai o d'una coma (−1 i no − 1)."""
    t = re.sub(r'\|([^|$]+)\|', r'\\lvert \1\\rvert ', t)
    return re.sub(r'(\\ |\\qquad |\\quad |,)-(\d+)', r'\1{-\2}', t)

def build(sol):
    t = 'Soluciones de la ficha' if sol else 'Ficha de ejercicios'
    p = preambul(pre, pdftitle='%s de la unidad 3: Números enteros' % t, capcalera='%s · Unidad 3: Números enteros' % t,
                 pdfkeywords='números enteros, recta numérica, valor absoluto, opuesto, suma y resta, regla de los signos, operaciones combinadas, problemas',
                 curs='1eso')
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

''' + assignatura('1eso') + '{' + ('Soluciones de la ficha · Unidad 3' if sol else 'Ficha de ejercicios · Unidad 3') + '}{Números enteros}\n')
    if not sol:
        out.append(r'''\vspace{10pt}
Nombre y apellidos: \rule{6.6cm}{0.4pt}\hfill Grupo: \rule{1.6cm}{0.4pt}\hfill Fecha: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resolver cada ejercicio antes de mirar su solución. Si no te sale el mismo resultado, repasa los pasos o consulta los apuntes interactivos de la unidad."
             if sol else r"Ejercicios graduados por niveles de dificultad:\quad \estrelles{1}\ básico \qquad \estrelles{2}\ medio \qquad \estrelles{3}\ avanzado.\\[2pt] Resuélvelos en el cuaderno mostrando todos los pasos. Las rectas numéricas se pueden completar directamente en la ficha. Haz los cálculos sin calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, tidy(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ ¡Ánimo! Si te cuesta algún ejercicio, repasa los apuntes interactivos de la unidad.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-solucions-es.tex' if sol else 't3-fitxa-exercicis-es.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'ejercicios')
