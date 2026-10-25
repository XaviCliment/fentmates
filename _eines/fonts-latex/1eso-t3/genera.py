# Genera t3-fitxa-exercicis.tex i t3-fitxa-solucions.tex (1r ESO, Unitat 3: Nombres enters)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució).
# Els resultats de les operacions es calculen ací mateix (ev), per a no equivocar-nos.
import os, re
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))

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
REP = [("Un avió sobrevola la ciutat a 432 peus d'altura.", '+432'), ("Aquesta nit el termòmetre ha marcat 6 °C baix zero.", '-6'),
       ("El cotxe el tenim aparcat al tercer soterrani.", '-3'), ("Sòcrates va nàixer l'any 470 abans de Crist.", '-470'),
       ("M'he gastat tots els diners (ni en tinc ni en dec).", '0'), ("València està situada a 15 m sobre el nivell de la mar.", '+15'),
       ("En un examen tipus test, cada resposta incorrecta resta 1 punt.", '-1')]
S.append(("Els nombres enters", [
 (1, r"Representa les situacions següents amb un nombre enter:" + tasks(1, [t + r' \dotfill' for t, _ in REP])
     + recorda(r"Primer busca el \textbf{zero} (la referència): 0\,°C, la planta baixa, el nivell de la mar, no tindre ni deure diners\ldots{} El que està \emph{per damunt} és \textbf{positiu} i el que està \emph{per davall}, \textbf{negatiu}."),
     tasks(4, ['$\\res{%s}$' % v for _, v in REP])),
 (1, r"Descriu tres situacions de la vida real en què s'utilitzen els nombres negatius.",
     r"Per exemple: temperatures baix zero ($-5$\,°C), soterranis d'un edifici ($-2$), deutes o saldos negatius ($-30$\,€), profunditats sota el nivell de la mar ($-200$\,m), anys abans de Crist ($-470$), gols en contra\ldots"),
 (1, r"Escriu una situació que es puga representar amb cada enter:" + tasks(5, [r"$-12$", r"$+8$", r"$-1500$", r"$+2026$", r"$-4$"]),
     r"Hi ha moltes respostes. Per exemple: \ a) un bussejador a 12\,m de profunditat; \ b) la planta 8 d'un edifici; \ c) un submarí a 1500\,m de profunditat; \ d) l'any 2026 d.\,C.; \ e) fa 4\,°C baix zero."),
 (1, r"Classifica aquests enters en \emph{positius}, \emph{negatius} i \emph{ni positius ni negatius}. Quins són també nombres naturals? \[-7\qquad 12\qquad 0\qquad +3\qquad -25\qquad 1\qquad -1\qquad 100\]",
     r"Positius: $12,\ +3,\ 1,\ 100$. \ Negatius: $-7,\ -25,\ -1$. \ Ni positiu ni negatiu: $0$. \ Naturals: $\res{12,\ +3,\ 1,\ 100,\ 0}$."),
 (2, r"Escriu l'enter anterior i el següent de cada nombre:" + tasks(5, [r"$5$", r"$-1$", r"$0$", r"$-10$", r"$-99$"]),
     tasks(5, [r"$4$ i $6$", r"$-2$ i $0$", r"$-1$ i $1$", r"$-11$ i $-9$", r"$-100$ i $-98$"])),
 (2, r"Escriu tots els enters compresos entre:" + tasks(3, [r"$-4$ i $3$", r"$-10$ i $-6$", r"$-2$ i $2$"]),
     tasks(3, [r"$\res{-3,-2,-1,0,1,2}$", r"$\res{-9,-8,-7}$", r"$\res{-1,0,1}$"])),
 (3, r"Quants enters hi ha compresos entre $-50$ i $50$? I entre $-50$ i $0$?",
     r"Del $-49$ al $-1$ n'hi ha 49, el 0 i de l'1 al 49, 49 més: $49+1+49=\res{99}$. \ Entre $-50$ i $0$: del $-49$ al $-1$, $\res{49}$."),
]))

PTS3 = [-2, 0, 4, -1, 8, -3, -7, 1]
PTS4 = [-7, 3, 1, -4, 6, -5, -2, 0]
CMP = [('-6', '6'), ('0', '-1'), ('10', '-1'), ('8', '3'), ('-8', '-9'), ('1', '-2'), ('-15', '-51'), ('-100', '1')]
def cmpsym(a, b): a, b = int(a), int(b); return '<' if a < b else '>' if a > b else '='
S.append(("Recta numèrica, ordre i comparació", [
 (1, r"Representa en la recta numèrica els nombres: \ $-2,\ 0,\ 4,\ -1,\ 8,\ -3,\ -7$ \ i \ $1$.\par\smallskip{\centering\rectabuida{-9}{9}\par}"
     + recorda(r"Els \textbf{positius} van a la \textbf{dreta} del zero i els \textbf{negatius}, a l'\textbf{esquerra}. Com més a la dreta, més gran és el nombre."),
     r"\par\smallskip{\centering\recta{-9}{9}{%s}\par}" % ','.join(map(str, PTS3))),
 (1, r"Representa en la recta numèrica aquests nombres i ordena'ls de menor a major: \[-7\qquad 3\qquad 1\qquad -4\qquad 6\qquad -5\qquad -2\qquad 0\]{\centering\rectabuida{-9}{9}\par}",
     r"\par\smallskip{\centering\recta{-9}{9}{%s}\par}\[\res{%s}\]" % (','.join(map(str, PTS4)), '<'.join(map(str, sorted(PTS4))))),
 (1, r"Ordena els nombres següents de major a menor: \ $-7,\ 0,\ 1,\ -1,\ 8,\ -4,\ -9,\ 3$.",
     r"$\res{%s}$" % '>'.join(map(str, sorted([-7, 0, 1, -1, 8, -4, -9, 3], reverse=True)))),
 (1, r"Compara les parelles de nombres amb el signe $<$, $>$ o $=$:" + tasks(4, [r"$%s\ \square\ %s$" % p for p in CMP]),
     tasks(4, [r"$%s\res{%s}%s$" % (a, cmpsym(a, b), b) for a, b in CMP])),
 (2, r"Escriu un enter comprès entre:" + tasks(4, [r"$-5$ i $-2$", r"$-1$ i $1$", r"$-13$ i $-11$", r"$-100$ i $-98$"]),
     tasks(4, [r"$-4$ o $-3$", r"$\res{0}$", r"$\res{-12}$", r"$\res{-99}$"])),
 (2, r"Quin enter està\ldots" + tasks(2, [r"5 unitats a l'esquerra de $2$?", r"7 unitats a la dreta de $-4$?", r"3 unitats a l'esquerra de $-6$?", r"a 4 unitats del $0$? (n'hi ha dos)"]),
     tasks(4, [r"$\res{-3}$", r"$\res{3}$", r"$\res{-9}$", r"$\res{4}$ i $\res{-4}$"])),
 (3, r"Vertader o fals? Justifica-ho:" + tasks(1, [r"Tot nombre negatiu és menor que zero.", r"$-20>-2$.", r"Entre $-3$ i $3$ hi ha 5 enters.", r"El major dels nombres negatius és $-1$.", r"Si $a<b$, aleshores $-a>-b$."]),
     tasks(1, [r"\res{\text{V}}: els negatius estan a l'esquerra del zero.", r"\res{\text{F}}: $-20$ està més a l'esquerra, $-20<-2$.", r"\res{\text{V}}: $-2,\ -1,\ 0,\ 1,\ 2$.", r"\res{\text{V}}: és el negatiu més pròxim al zero.", r"\res{\text{V}}: canviar el signe és com mirar la recta en un espill: per exemple, $2<5$ i $-2>-5$."])),
]))

ABS = ['-5', '-1', '0', '8', '-23', '7']
OPS = ['-8', '-3', '0', '4', '-100', '15']
CMP2 = [(r'|-3|', 3, '3', 3), (r'\text{op}(-2)', 2, '-1', -1), (r'|-2|', 2, '|-1|', 1), (r'\text{op}(\text{op}(-1))', -1, '0', 0), (r'|-4|', 4, r'\text{op}(2)', -2), ('-8', -8, r'\text{op}(8)', -8)]
def sy(a, b): return '<' if a < b else '>' if a > b else '='
S.append(("Valor absolut i oposat", [
 (1, r"Calcula el valor absolut dels nombres següents:" + tasks(6, [r"$|%s|$" % x for x in ABS])
     + recorda(r"El \textbf{valor absolut} d'un nombre és la \textbf{distància} d'aquest nombre al 0: \ $|-5|=|5|=5$. Mai no és negatiu."),
     tasks(3, [r"$|%s|=\res{%d}$" % (x, abs(int(x))) for x in ABS])),
 (1, r"Calcula l'oposat dels nombres següents:" + tasks(6, [r"$\text{op}(%s)$" % x for x in OPS])
     + recorda(r"L'\textbf{oposat} d'un nombre és el que està a la \textbf{mateixa distància} del zero, però a l'altre costat: canviem el signe. \ $\text{op}(-8)=8$, \ $\text{op}(4)=-4$."),
     tasks(3, [r"$\text{op}(%s)=\res{%d}$" % (x, -int(x)) for x in OPS])),
 (1, r"Dos nombres oposats es troben a una distància de $36$ unitats l'un de l'altre. Quins nombres són?",
     r"Cadascun està a la meitat de la distància del zero: $36:2=18$. \ Són $\res{18}$ i $\res{-18}$."),
 (2, r"Ordena de menor a major els nombres següents, fent abans els càlculs: \[3\qquad \text{op}(4)\qquad |-6|\qquad 1\qquad \text{op}(5)\qquad -2\qquad |7|\qquad |-2|\qquad 0\qquad 5\]",
     r"$\text{op}(4)=-4$, \ $|-6|=6$, \ $\text{op}(5)=-5$, \ $|7|=7$, \ $|-2|=2$: \[\res{\text{op}(5)<\text{op}(4)<-2<0<1<|-2|<3<5<|-6|<|7|}\]"),
 (2, r"Compara les parelles de nombres:" + tasks(3, [r"$%s\ \square\ %s$" % (a, c) for a, _, c, _ in CMP2]),
     tasks(3, [r"$%s\res{%s}%s$" % (a, sy(b, d), c) for a, b, c, d in CMP2]) + r"\par (Valors: $3=3$; \ $2>-1$; \ $2>1$; \ $-1<0$; \ $4>-2$; \ $-8=-8$.)"),
 (3, r"Completa els buits amb el nombre o els nombres que corresponguen:" + tasks(3, [r"$\text{op}(\text{op}(\square))=-7$", r"$|\square|=10$", r"$\text{op}(|\square|)=-2$", r"$|\text{op}(-8)|=\square$", r"$\text{op}(|-4|)=\square$", r"$|\square|=\text{op}(5)$"]),
     tasks(3, [r"$\res{-7}$", r"$\res{10}$ o $\res{-10}$", r"$\res{2}$ o $\res{-2}$", r"$\res{8}$", r"$\res{-4}$", r"Cap: $\text{op}(5)=-5$ i un valor absolut no pot ser negatiu."])),
 (3, r"Quins enters tenen valor absolut menor que $4$? I quins tenen valor absolut menor o igual que $2$?",
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
S.append(("Suma i resta d'enters", [
 (1, r"Calcula:" + tasks(5, [m(e) for e in E13])
     + recorda(r"\textbf{Mateix signe}: se sumen i es posa el signe comú ($-3-5=-8$). \ \textbf{Signes diferents}: se resten (gran menys xicotet) i es posa el signe del que té major valor absolut ($-7+4=-3$)."),
     tasks(5, [rsol(e) for e in E13])),
 (1, r"Calcula:" + tasks(6, [m(e) for e in E15]),
     tasks(3, [grouped(e) for e in E15])),
 (2, r"Calcula:" + tasks(4, [m(e) for e in E16])
     + recorda(r"Pots agrupar: suma tots els positius, suma tots els negatius i resta: \ $5-9+8-2=(5+8)-(9+2)=13-11=2$."),
     tasks(3, [grouped(e) for e in E16])),
 (2, r"Calcula de dues maneres, d'esquerra a dreta i agrupant positius i negatius:" + tasks(2, [m('12-4-6+9-15'), m('-7+3-8+10-2+5')]),
     tasks(1, [r"$12-4-6+9-15=8-6+9-15=2+9-15=11-15=\res{-4}$; \quad $(12+9)-(4+6+15)=21-25=\res{-4}$",
               r"$-7+3-8+10-2+5=-4-8+10-2+5=-12+10-2+5=-2-2+5=-4+5=\res{1}$; \quad $(3+10+5)-(7+8+2)=18-17=\res{1}$"])),
 (3, r"Troba el nombre que falta:" + tasks(3, ['$%s$' % q for q, _ in MISS]),
     tasks(3, [r"$\square=\res{%d}$" % a for _, a in MISS])),
]))
assert ev('12-4-6+9-15') == -4 and ev('-7+3-8+10-2+5') == 1 and ev('-8-(-5)') == -3 and ev('-3-(-4)') == 1

E14 = ['(-6)+(-3)', '(+7)+(-4)', '(-8)+(+1)', '(-3)+(-7)', '(+12)+(+5)', '(+3)+(-5)', '(+3)+(+4)', '(+4)+(-6)', '(+7)+(-8)', '(-5)+(+4)', '(-9)+(+3)', '(+1)+(-1)', '(-7)+(+7)', '(-12)+(-3)', '(+7)+(+5)', '(-4)+(-10)', '(+6)+(-12)', '(-9)+(+15)']
E17 = ['3-(-1)', '-8+(-17)', '-4-(-7)', '-(-5)+3', '8+(-14)', '(-2)-(+3)+(-6)', '-(-5)+(-4)-(-10)', '-15-(-3)+7', '(-8)+(-3)-(-17)+(+1)', '-2-(-3)+7-8', '-(-3)+(-1)-(+3)-(-8)', '-3+(-6)-4+1', '12-25+3-8-(-6)', '-7+4-(-8)+(-3)', '-(+4)+(-8)-(-6)+4-1', '-8+(-3)+4-7-5', '-(-6)+(-1)-7+(-3)', '15-(+3)-6+3-12']
E18 = ['12+(+3-5)', '14+(+12-10)', '6-(9-7)', '15-(2-9)', '11-(-6+3)', '10-(-7-5)', '13+(-8+2)', '17+(-5-9)', '1+(-3+8)', '9-(2-1)', '-6-(2-7)', '11+(-1-3)', '6+(6+3)', '-5-(-2-8)', '3+(-8+7)', '15+(-6-8)']
E19 = ['(7-4)+(9-5)', '(2+6)+(5-8)', '(5-9)+(2-12)', '(7+3)-(5+4)', '(8-12)-(2-5)', '(10-7)-(-2-6)', '-(8+4)+(5-9)', '-(6-2)-(7-9)', '(-8-2)+(-1-5)', '(7-1)-(-5+11)', '(15-8)+(-6-12)', '(-2+3)-(8-4)', '(17-12)-(-7-8)', '(-10+3)-(2-9)', '-(6-4)+(8+1)', '-(-7-1)-(2-10)']
E20 = ['6+[5+(7+2)]', '8+[4-(3+5)]', '10-[6+(2+7)]', '15-[2-(6-10)]', '15-[10-(8+4)]', '12-[7-(2-10)]', '(-6)+[5+(2-12)]', '(-7)-[3-(4-9)]', '(2-10)+[5-(8+2)]', '(12-3)-[1-(2-6)]', '[9-(+5)]+[7+(-10)]', '[10-(-2)]-[5-(+12)]', '[8-(6+4)]-(5-7)', '[1+(6-9)]-(8-12)', '2-[6-(-1-21)]', '-1+[-5-(2-13)]']
S.append(("Parèntesis i claudàtors", [
 (1, r"Calcula, eliminant prèviament els parèntesis:" + tasks(3, [m(e) for e in E14])
     + recorda(r"Regla dels signes per a llevar parèntesis: \ $+(+\ \to\ +$ \qquad $+(-\ \to\ -$ \qquad $-(+\ \to\ -$ \qquad $-(-\ \to\ +$"),
     tasks(3, [fsol(e) for e in E14])),
 (2, r"Calcula, eliminant prèviament els parèntesis:" + tasks(2, [m(e) for e in E17]),
     tasks(1, [fsol(e) for e in E17])),
 (2, r"Calcula, resolent prèviament els parèntesis:" + tasks(4, [m(e) for e in E18])
     + recorda(r"Resol primer l'operació de dins del parèntesi, o bé lleva'l: si davant hi ha un $-$, canvia el signe de \textbf{tots} els termes de dins: \ $6-(9-7)=6-9+7=4$."),
     tasks(2, [chain(e) for e in E18])),
 (2, r"Calcula, resolent prèviament els parèntesis:" + tasks(3, [m(e) for e in E19]),
     tasks(2, [chain(e) for e in E19])),
 (3, r"Calcula, començant pels parèntesis de dins:" + tasks(3, [m(e) for e in E20]),
     tasks(1, [chain(e) for e in E20])),
]))

E22 = ['(-4)·(+7)', '(+2)·(+6)', '(-5)·(-7)', '(+3)·(-8)', '(-9)·(-3)', '(-6)·(+4)', '3·(-2)', '4·(+5)', '8·(-6)', '-5·(+3)', '-2·(-4)', '-6·(+3)', '(+3)·(-5)·(+2)', '(-4)·(-1)·(+6)', '(-2)·(-7)·(-2)', '(+5)·(-4)·(-3)', '(-8)·4·(-6)', '5·3·(-9)·4']
E24 = ['(-8):(+2)', '(+20):(-10)', '(-12):(-4)', '(-4):(+2)', '(+21):(-7)', '(-12):(+6)', '(-15):(-3)', '(+32):(+8)', '(-36):(+9)', '(+42):(-7)', '(-48):(-8)', '(+54):(+6)', '[(+80):(-8)]:(-5)', '[(-70):(-2)]:(-7)', '(+50):[(-30):(+6)]', '(-40):[(+24):(+3)]']
E23 = [(r"(-6)\cdot(\ \square\ )=-18", 3), (r"(\ \square\ )\cdot(-3)=-24", 8), (r"(\ \square\ )\cdot(-5)=+35", -7), (r"(+15)\cdot(\ \square\ )=+60", 4), (r"(-8)\cdot(\ \square\ )=40", -5), (r"(\ \square\ )\cdot7=-77", -11)]
LR = {'24:(-2)·(-3)': '(-12)·(-3)', '(-70)·(-5):(+2)': '350:(+2)', '(+100):(+4)·(-2)': '25·(-2)'}
E25 = ['[(+6)·(-4)]:(-3)', '[(-15)·(-2)]:(+6)', '(-5)·[(+12):(-3)]', '[(-5)·(+12)]:(-3)', '24:(-2)·(-3)', '(-40)·[(-10):(-5)]', '(-70)·(-5):(+2)', '(+100):(+4)·(-2)']
S.append(("Multiplicació i divisió", [
 (1, r"Resol les multiplicacions següents:" + tasks(3, [m(e) for e in E22])
     + recorda(r"Regla dels signes: \ $+\cdot+\ \to\ +$ \qquad $+\cdot-\ \to\ -$ \qquad $-\cdot+\ \to\ -$ \qquad $-\cdot-\ \to\ +$. \ Per a la divisió és igual."),
     tasks(3, [rsol(e) for e in E22])),
 (1, r"Calcula:" + tasks(3, [m(e) for e in E24]),
     tasks(2, [chain(e) for e in E24])),
 (2, r"Troba el nombre que falta:" + tasks(3, ['$%s$' % q for q, _ in E23]),
     tasks(6, [r"$\res{%d}$" % a for _, a in E23])),
 (2, r"Calcula (les multiplicacions i divisions seguides es fan d'esquerra a dreta):" + tasks(4, [m(e) for e in E25]),
     tasks(2, [chain(e) if '[' in e else '$' + tx(e) + '=' + tx(LR[e]) + r'=\res{%d}$' % ev(e) for e in E25])),
 (3, r"Troba dos nombres enters que complisquen, en cada cas:" + tasks(1, [r"El producte és $-12$ i la suma és $1$.", r"El producte és $18$ i la suma és $-9$.", r"El producte és $-20$ i la suma és $-1$."]),
     tasks(3, [r"$\res{4}$ i $\res{-3}$", r"$\res{-3}$ i $\res{-6}$", r"$\res{4}$ i $\res{-5}$"])),
 (3, r"Sense fer els càlculs, digues quin signe tindrà el resultat. Després, comprova-ho:" + tasks(1, [m('(-1)·(-2)·(-3)·(-4)'), m('(-5)·(+2)·(-1)·(-3)·(+4)'), r"El producte de set factors iguals a $-1$."]),
     tasks(1, [r"Quatre factors negatius (parell): \res{+}. \ $%d$" % ev('(-1)·(-2)·(-3)·(-4)'), r"Tres factors negatius (senar): \res{-}. \ $%d$" % ev('(-5)·(+2)·(-1)·(-3)·(+4)'), r"Set factors negatius (senar): \res{-}. \ $-1$"])),
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
S.append(("Operacions combinades", [
 (1, r"Calcula:" + tasks(2, [m(e) for e in E26a])
     + recorda(r"Ordre de les operacions: \ 1) parèntesis i claudàtors (de dins cap a fora); \ 2) multiplicacions i divisions, d'esquerra a dreta; \ 3) sumes i restes."),
     tasks(1, [msol(e) for e in E26a])),
 (2, r"Calcula:" + tasks(2, [m(e) for e in E26b]),
     tasks(1, [msol(e) for e in E26b])),
 (3, r"Calcula:" + tasks(2, [m(e) for e in E27]),
     tasks(1, [msol(e) for e in E27])),
 (3, r"Posa parèntesis on calga perquè les igualtats siguen certes:" + tasks(3, [r"$6-4\cdot2-5=-6$", r"$-3+5\cdot2-4=0$", r"$10-2\cdot3+1=2$"]),
     tasks(3, [r"$\res{(6-4)\cdot(2-5)}=-6$", r"$\res{(-3+5)}\cdot2-4=0$", r"$10-2\cdot\res{(3+1)}=2$"])),
]))
assert ev('(6-4)·(2-5)') == -6 and ev('(-3+5)·2-4') == 0 and ev('10-2·(3+1)') == 2

PROB = [
 (1, r"Quina diferència de temperatura suporta una persona que passa de la cambra de conservació de les verdures, que es troba a $4$\,°C, a la del peix congelat, que està a $-18$\,°C? I si passa de la cambra del peix a la de les verdures?",
     r"$-18-4=\res{-22}$\,°C (baixa 22 graus). \ $4-(-18)=4+18=\res{+22}$\,°C (puja 22 graus)."),
 (1, r"La Mònica ix en l'ascensor des de la planta zero del seu edifici. L'ascensor puja 5 plantes, després baixa 3, puja 5, baixa 8, puja 10, puja 5 i baixa 6. En quina planta està?",
     r"$0+5-3+5-8+10+5-6=25-17=\res{8}$: \ està en la planta 8."),
 (1, r"En Joan li deu 14 euros a la seua germana. Si li paga 9 euros, quant li deu?",
     r"$-14+9=-5$: \ encara li deu $\res{5\text{ €}}$."),
 (1, r"En una estació d'esquí, el termòmetre marcava $14$\,° baix zero a les 8 del matí; al migdia la temperatura havia pujat 10 graus i a les 19.00 havia baixat 5 graus respecte al migdia. Quina temperatura feia a les 19.00?",
     r"$-14+10-5=\res{-9}$\,°C."),
 (1, r"Si estava bussejant a una profunditat de 2 metres i ara estic sobre un penya-segat a 8 m d'altura, quina distància hi ha entre els dos llocs?",
     r"$8-(-2)=8+2=\res{10\text{ m}}$."),
 (1, r"El primer mes de l'any la gasolina va baixar 5 cèntims, el segon va pujar 3 cèntims, el tercer va pujar 8 cèntims i el quart va baixar 2 cèntims. Expressa-ho amb nombres enters i calcula la variació total del preu en aquest temps.",
     r"$-5+3+8-2=11-7=\res{+4}$: \ ha pujat 4 cèntims."),
 (2, r"Un dia d'hivern, la temperatura a les sis del matí era de $3$\,° baix zero. Al migdia havia pujat 9 graus, però a les dotze de la nit el termòmetre marcava $1$\,° baix zero. Quina diferència de temperatura hi ha hagut entre el migdia i la mitjanit?",
     r"Al migdia: $-3+9=6$\,°C. \ Diferència: $-1-6=\res{-7}$\,°C: \ ha baixat 7 graus."),
 (2, r"Euclides va ser un matemàtic que va viure 60 anys i va morir l'any 265 a.\,C. En quin any va nàixer?",
     r"$-265-60=-325$: \ va nàixer l'any $\res{325\text{ a.\,C.}}$"),
 (2, r"El Mulhacén, el pic més alt de la península Ibèrica, fa $3478$ metres d'altura. El Sistema del Trave, un dels avencs més profunds del món, arriba a $1441$ metres de profunditat. Troba la diferència d'altitud entre els dos punts.",
     r"$3478-(-1441)=3478+1441=\res{4919\text{ m}}$."),
 (2, r"En Pau tenia 850 euros a la seua cartilla d'estalvis. Ha ingressat 250 euros cada mes durant els 5 últims mesos i després en va traure 2300 per a pagar el fuster. Quin saldo li queda?",
     r"$850+5\cdot250-2300=850+1250-2300=\res{-200\text{ €}}$: \ el compte està en descobert (deu 200\,€)."),
 (3, r"Arquimedes va nàixer l'any 287 a.\,C. i va morir l'any 212 a.\,C. Quants anys va viure?",
     r"$-212-(-287)=-212+287=\res{75\text{ anys}}$."),
 (3, r"Un submarí es troba a 120 m de profunditat. Puja 45 m i després baixa el triple del que ha pujat. A quina profunditat es troba ara?",
     r"$-120+45-3\cdot45=-120+45-135=\res{-210}$: \ a 210\,m de profunditat."),
 (3, r"En un examen tipus test, cada resposta correcta suma 3 punts, cada resposta incorrecta en resta 2 i cada pregunta en blanc val 0. La Laia n'ha encertat 11, n'ha fallat 6 i n'ha deixat 3 en blanc. Quina puntuació ha obtingut? Quantes n'hauria d'haver encertat, com a mínim, per a no tindre una puntuació negativa si n'haguera fallat 9 i n'haguera deixat 3 en blanc?",
     r"$11\cdot3+6\cdot(-2)+3\cdot0=33-12=\res{21\text{ punts}}$. \ Fallar-ne 9 resta $18$: cal sumar-ne almenys 18, és a dir, $18:3=\res{6}$ encerts (en queden $20-9-3=8$, així que és possible)."),
]
assert ev('0+5-3+5-8+10+5-6') == 8 and ev('-14+10-5') == -9 and ev('-5+3+8-2') == 4 and ev('850+5·250-2300') == -200 and ev('-120+45-3·45') == -210 and ev('11·3+6·(-2)') == 21
PROB[0] = (PROB[0][0], PROB[0][1] + recorda(r"Escriu cada dada com un enter \textbf{amb el seu signe} (\emph{puja, guanya, sobre zero} $\to +$; \ \emph{baixa, perd, deu, baix zero} $\to -$). Per a calcular una \textbf{diferència} o variació: \ \textbf{valor final} $-$ \textbf{valor inicial}."), PROB[0][2])
S.append(("Problemes amb enters", PROB))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0] + '\\newcolumntype{C}[1]{>{\\centering\\arraybackslash}p{#1}}\n'
KW = 'pdfkeywords={nombres enters, recta numèrica, valor absolut, oposat, suma i resta, regla dels signes, operacions combinades, problemes}'
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda m: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques 1r ESO}')
pre += r'''
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
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
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 3: Nombres enters. 1r d'ESO}" % t)
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 3: Nombres enters · 1r d'ESO" % t)
    assert 'Nombres enters · 1r' in p and 'unitat 3: Nombres' in p
    out = [p]
    if sol: out.append('\\newcommand{\\res}[1]{\\boxed{#1}}\n')
    else: out.append('\\newcommand{\\res}[1]{#1}\n')
    out.append(r'''
\input{../comu/fentmates.tex}
\fmcurs{1eso}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques}{1r ESO}{''' + ('Solucions de la fitxa · Unitat 3' if sol else "Fitxa d'exercicis · Unitat 3") + r'''}{Nombres enters}
''')
    if not sol:
        out.append(r'''\vspace{10pt}
Nom i cognoms: \rule{8.4cm}{0.4pt}\hfill Grup: \rule{1.6cm}{0.4pt}\hfill Data: \rule{2.2cm}{0.4pt}
''')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o consulta els apunts interactius de la unitat."
             if sol else r"Exercicis graduats per nivells de dificultat:\quad \estrelles{1}\ bàsic \qquad \estrelles{2}\ mitjà \qquad \estrelles{3}\ avançat.\\[2pt] Resol-los al quadern mostrant tots els passos. Les rectes numèriques es poden completar directament en la fitxa. Fes els càlculs sense calculadora.") + r'''
\end{tcolorbox}
''')
    n = 0
    for i, (title, exs) in enumerate(S, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for st, q, s in exs:
            n += 1
            out.append('\\ex{%d} %s\n\n' % (st, tidy(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Si et costa algun exercici, repassa els apunts interactius de la unitat.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't3-fitxa-solucions.tex' if sol else 't3-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8').write(''.join(out))
    return n

n = build(False); build(True)
print(n, 'exercicis')
