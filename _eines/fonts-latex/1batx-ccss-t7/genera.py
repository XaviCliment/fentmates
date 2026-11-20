# Genera t7-fitxa-exercicis.tex i t7-fitxa-solucions.tex (1r Batxillerat CCSS, Unitat 7: Derivades i aplicacions)
# a partir d'una sola llista d'exercicis: cada exercici és (estrelles, enunciat, solució); a Batxillerat no es mostren les estrelles.
# Parteix de la fitxa de la unitat 9 de 1r Batx MI (_eines/fonts-latex/1batx-mi-t9), sense funcions trigonomètriques
# (no formen part del currículum de CCSS). La fitxa segueix els apartats dels apunts (7.1-7.9). Els problemes d'optimització
# són de dos tipus: funció donada (cal estudiar-ne també el creixement i el decreixement) o funció de benefici, ingressos
# o cost que cal construir (contextos empresarials i socials).
# Comprovacions (comprova.py): sympy verifica cada derivada (DER), valor (VAL), punts crítics (CRIT), signes de f' (SIGN) i TVM.
# Ús: python3 genera.py && pdflatex t7-fitxa-exercicis.tex (dues vegades) && pdflatex t7-fitxa-solucions.tex (dues vegades)
import os, re, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from comprova import DER, VAL, EQL, CRIT, SIGN, TVM, LIM, NCHK

def tasks(n, items):
    return '\\begin{tasks}(%d)\n' % n + ''.join('  \\task %s\n' % i for i in items) + '\\end{tasks}'
def recorda(t): return '\\recorda{%s}' % t
def m(s): return '$' + s + '$'
def dm(s): return r'\[' + s + r'\]'
def R(s): return r'$\res{' + s + '}$'

# ---------- gràfiques (TikZ) ----------
def tzg(x0, x1, y0, y1, body, sc=0.45):
    g = r'\draw[muted!30,very thin] (%s,%s) grid (%s,%s);' % (x0, y0, x1, y1)
    g += r'\draw[-latex,thick] (%s,0)--(%s,0);\draw[-latex,thick] (0,%s)--(0,%s);' % (x0, x1 + 0.4, y0, y1 + 0.4)
    return r'\begin{tikzpicture}[scale=%s,baseline=(current bounding box.center)]\begin{scope}%s\clip (%s,%s) rectangle (%s,%s);%s\end{scope}\end{tikzpicture}' % (sc, g, x0, y0, x1, y1, body)
CV = r'\draw[accent,line width=1.5pt,smooth,samples=120,domain=%s] plot (\x,{%s});'
def dot(x, y): return r'\fill[accent] (%s,%s) circle (0.15);' % (x, y)
def lab(x, y, t, pos='above'): return r'\node[%s,font=\scriptsize] at (%s,%s) {$%s$};' % (pos, x, y, t)
def dl(x0, y0, x1, y1): return r'\draw[teal,dashed,thick] (%s,%s)--(%s,%s);' % (x0, y0, x1, y1)
def G(g): return r'\par\smallskip{\centering ' + g + r'\par}'

S_ = []

# =====================================================================
# 1. Taxa de variació mitjana
f1 = 'x**2-8*x+12'
TVM(f1, 1, 2, -5); TVM(f1, 1, 5, -2); TVM(f1, 1, 8, 1); EQL('((1+h)**2-8*(1+h)+12-5)/h', 'h-6')
s1 = '20*x-5*x**2'
TVM(s1, 0, 1, 15); TVM(s1, 1, 2, 5); TVM(s1, 2, 4, -10)
TVM('sqrt(x)', 1, 4, '1/3'); TVM('2**x', 0, 3, '7/3'); TVM('1/x', 1, 2, '-1/2')
S_.append(("Taxa de variació mitjana", [
 (1, r"Troba la TVM de la funció $y=x^2-8x+12$ en els intervals $[1,2]$, $[1,5]$ i $[1,8]$. Després, troba-la en l'interval variable $[1,1+h]$ i comprova que, donant a $h$ els valors 1, 4 i 7, obtens els resultats anteriors."
     + recorda(r"$\text{TVM}[a,b]=\dfrac{f(b)-f(a)}{b-a}$ \ és el pendent del segment que uneix els punts $(a,f(a))$ i $(b,f(b))$. Si la TVM és positiva, la funció ha crescut de mitjana en l'interval."),
     r"$f(1)=5$, $f(2)=0$, $f(5)=-3$, $f(8)=12$. \ $\text{TVM}[1,2]=\frac{0-5}{1}=\res{-5}$; \ $\text{TVM}[1,5]=\frac{-3-5}{4}=\res{-2}$; \ $\text{TVM}[1,8]=\frac{12-5}{7}=\res{1}$. \\ $f(1+h)=h^2-6h+5$: \ $\text{TVM}[1,1+h]=\frac{h^2-6h+5-5}{h}=\res{h-6}$. \ Amb $h=1,4,7$: $-5$, $-2$ i $1$."),
 (1, r"Llancem una pilota cap amunt i la seua altura (en metres) després de $t$ segons és $s(t)=20t-5t^2$. Calcula la velocitat mitjana en els intervals $[0,1]$, $[1,2]$ i $[2,4]$. Què indica el signe del darrer resultat?",
     r"$\text{TVM}[0,1]=\frac{15-0}{1}=\res{15\text{ m/s}}$; \ $\text{TVM}[1,2]=\frac{20-15}{1}=\res{5\text{ m/s}}$; \ $\text{TVM}[2,4]=\frac{0-20}{2}=\res{-10\text{ m/s}}$: és negativa perquè la pilota \rest{baixa}."),
 (1, r"Calcula la TVM de cada funció en l'interval indicat:" + tasks(3, [r'$f(x)=\sqrt x$ \ en $[1,4]$', r'$g(x)=2^x$ \ en $[0,3]$', r'$h(x)=\dfrac1x$ \ en $[1,2]$']),
     tasks(3, [r'$\frac{2-1}{3}=\res{\frac13}$', r'$\frac{8-1}{3}=\res{\frac73}$', r'$\frac{\frac12-1}{1}=\res{-\frac12}$'])),
]))

# =====================================================================
# 2. Derivada en un punt. Funció derivada
DER('1/x', '-1/x**2'); VAL('-1/x**2', -2, '-1/4'); DER('-2*x+4', '-2'); DER('3*x**2-5*x+1', '6*x-5')
VAL('6*x-5', -2, -17); VAL('6*x-5', 1, 1); VAL('6*x-5', 0, -5)
EQL('((x+h)**2+3*(x+h)-x**2-3*x)/h', '2*x+h+3'); DER('x**2+3*x', '2*x+3')
EQL('(2/(x+h+1)-2/(x+1))/h', '-2/((x+h+1)*(x+1))'); DER('2/(x+1)', '-2/(x+1)**2')
EQL('(x+h+1-(x+1))/(h*(sqrt(x+h+1)+sqrt(x+1)))', '1/(sqrt(x+h+1)+sqrt(x+1))'); DER('sqrt(x+1)', '1/(2*sqrt(x+1))')
EQL('((3+h)**2-9)/h', '6+h'); VAL('x**2', 3, 9)
S_.append(("Derivada en un punt i funció derivada", [
 (1, r"Calcula, aplicant la definició, les derivades següents:" + tasks(1, [r"La derivada de $y=\dfrac1x$ en el punt $x=-2$.", r"La derivada de $y=-2x+4$ en els punts d'abscisses $-3$, $0$, $4$ i $7$. Per què ix sempre el mateix?", r"La derivada de $y=3x^2-5x+1$ en els punts d'abscisses $-2$, $1$ i $0$."])
     + recorda(r"$f'(a)=\displaystyle\lim_{h\to0}\frac{f(a+h)-f(a)}{h}$: és el pendent de la recta tangent a la gràfica en el punt $(a,f(a))$."),
     tasks(1, [r"$\dfrac{f(-2+h)-f(-2)}{h}=\dfrac{\frac{1}{-2+h}+\frac12}{h}=\dfrac{1}{2(-2+h)}\to\res{f'(-2)=-\frac14}$",
               r"$\dfrac{-2(a+h)+4-(-2a+4)}{h}=\dfrac{-2h}{h}=-2$: \ $\res{f'(a)=-2}$ en tots els punts, perquè la gràfica és una recta de pendent $-2$.",
               r"$\dfrac{f(a+h)-f(a)}{h}=6a-5+3h\to6a-5$: \ $f'(-2)=\res{-17}$, \ $f'(1)=\res{1}$, \ $f'(0)=\res{-5}$"])),
 (2, r"Troba la funció derivada aplicant la definició $f'(x)=\displaystyle\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$:" + tasks(3, [r'$f(x)=x^2+3x$', r'$f(x)=\dfrac{2}{x+1}$', r'$f(x)=\sqrt{x+1}$']),
     tasks(1, [r"$\dfrac{(x+h)^2+3(x+h)-x^2-3x}{h}=\dfrac{2xh+h^2+3h}{h}=2x+h+3\to\res{2x+3}$",
               r"$\dfrac{\frac{2}{x+h+1}-\frac{2}{x+1}}{h}=\dfrac{-2h}{h(x+h+1)(x+1)}\to\res{\dfrac{-2}{(x+1)^2}}$",
               r"Pel conjugat: $\dfrac{\sqrt{x+h+1}-\sqrt{x+1}}{h}=\dfrac{1}{\sqrt{x+h+1}+\sqrt{x+1}}\to\res{\dfrac{1}{2\sqrt{x+1}}}$"])),
 (1, r"Calcula per definició el pendent de la recta tangent a $y=x^2$ en $x=3$ i escriu-ne l'equació.",
     r"$\dfrac{(3+h)^2-9}{h}=6+h\to f'(3)=6$. \ Tangent per $(3,9)$: $y=9+6(x-3)\Rightarrow\res{y=6x-9}$"),
]))
EQL('9+6*(x-3)', '6*x-9')

# =====================================================================
# 3. Regles de derivació
D3 = [('2*x**3-5*x**2+3*x-2', '6*x**2-10*x+3', r'2x^3-5x^2+3x-2', r"6x^2-10x+3"),
      ('sqrt(2*x)+(5*x**2)**Rational(1,3)', '1/sqrt(2*x)+2*5**Rational(1,3)/(3*x**Rational(1,3))', r'\sqrt{2x}+\sqrt[3]{5x^2}', r"\dfrac{1}{\sqrt{2x}}+\dfrac{2\sqrt[3]{5}}{3\sqrt[3]{x}}"),
      ('1/(x*sqrt(x))', '-3/(2*x**2*sqrt(x))', r'\dfrac{1}{x\sqrt x}', r"-\dfrac{3}{2x^2\sqrt x}"),
      ('x**3/(x**2+1)', '(x**4+3*x**2)/(x**2+1)**2', r'\dfrac{x^3}{x^2+1}', r"\dfrac{x^4+3x^2}{(x^2+1)^2}"),
      ('x**2*log(x)', '2*x*log(x)+x', r'x^2\cdot\ln x', r"2x\ln x+x"),
      ('sqrt(3*x**3)*exp(x)', 'sqrt(3)*exp(x)*sqrt(x)*(2*x+3)/2', r'\sqrt{3x^3}\cdot e^x', r"\dfrac{\sqrt3}{2}\,e^x\sqrt x\,(2x+3)")]
D3b = [('x**4-3/x**2+5', '4*x**3+6/x**3', r'x^4-\dfrac{3}{x^2}+5', r"4x^3+\dfrac{6}{x^3}"),
       ('(x+1)/(x-1)', '-2/(x-1)**2', r'\dfrac{x+1}{x-1}', r"\dfrac{-2}{(x-1)^2}"),
       ('x**2/(x+2)', '(x**2+4*x)/(x+2)**2', r'\dfrac{x^2}{x+2}', r"\dfrac{x^2+4x}{(x+2)^2}"),
       ('exp(x)/x', 'exp(x)*(x-1)/x**2', r'\dfrac{e^x}{x}', r"\dfrac{e^x(x-1)}{x^2}"),
       ('log(x)/log(2)+3**x', '1/(x*log(2))+3**x*log(3)', r'\log_2x+3^x', r"\dfrac{1}{x\ln2}+3^x\ln3"),
       ('(2*x-1)*exp(x)', 'exp(x)*(2*x+1)', r'(2x-1)\,e^x', r"e^x(2x+1)"),
       ('(x**2+1)*exp(x)', 'exp(x)*(x+1)**2', r'(x^2+1)\,e^x', r"e^x(x+1)^2"),
       ('log(x)/x', '(1-log(x))/x**2', r'\dfrac{\ln x}{x}', r"\dfrac{1-\ln x}{x^2}"),
       ('x/log(x)', '(log(x)-1)/log(x)**2', r'\dfrac{x}{\ln x}', r"\dfrac{\ln x-1}{(\ln x)^2}")]
for f, d, _, _ in D3 + D3b: DER(f, d)
S_.append(("Regles de derivació", [
 (1, r"Calcula la funció derivada d'aquestes funcions simples:" + tasks(2, ['$f(x)=%s$' % a for _, _, a, _ in D3])
     + recorda(r"$(x^n)'=nx^{n-1}$ (també amb exponents fraccionaris: escriu les arrels com a potències). \ $(f\cdot g)'=f'g+fg'$; \ $\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}$."),
     tasks(2, ["$f'(x)=\\res{%s}$" % b for _, _, _, b in D3])),
 (1, r"Deriva i simplifica:" + tasks(3, ['$f(x)=%s$' % a for _, _, a, _ in D3b])
     + recorda(r"$(e^x)'=e^x$, \ $(a^x)'=a^x\ln a$, \ $(\ln x)'=\frac1x$, \ $(\log_ax)'=\frac{1}{x\ln a}$."),
     tasks(3, ["$\\res{%s}$" % b for _, _, _, b in D3b])),
]))

# =====================================================================
# 4. Regla de la cadena
D4 = [('sqrt(x**2+1)', 'x/sqrt(x**2+1)', r'\sqrt{x^2+1}', r"\dfrac{x}{\sqrt{x^2+1}}"),
      ('x*exp(x**2)', 'exp(x**2)*(1+2*x**2)', r'x\,e^{x^2}', r"e^{x^2}(1+2x^2)"),
      ('2*x/(x**2+1)**2', '(2-6*x**2)/(x**2+1)**3', r'\dfrac{2x}{(x^2+1)^2}', r"\dfrac{2-6x^2}{(x^2+1)^3}"),
      ('log(x**3-1)', '3*x**2/(x**3-1)', r'\ln(x^3-1)', r"\dfrac{3x^2}{x^3-1}"),
      ('x/sqrt(x**2+1)', '1/(x**2+1)**Rational(3,2)', r'\dfrac{x}{\sqrt{x^2+1}}', r"\dfrac{1}{(x^2+1)\sqrt{x^2+1}}"),
      ('(2*x+1)**4', '8*(2*x+1)**3', r'(2x+1)^4', r"8(2x+1)^3")]
D4b = [('exp(3*x**2-x)', 'exp(3*x**2-x)*(6*x-1)', r'e^{3x^2-x}', r"(6x-1)\,e^{3x^2-x}"),
       ('(x**2-3*x)**5', '5*(x**2-3*x)**4*(2*x-3)', r'(x^2-3x)^5', r"5(x^2-3x)^4(2x-3)"),
       ('exp(sqrt(x))', 'exp(sqrt(x))/(2*sqrt(x))', r'e^{\sqrt x}', r"\dfrac{e^{\sqrt x}}{2\sqrt x}"),
       ('log(exp(x)+1)', 'exp(x)/(exp(x)+1)', r'\ln(e^x+1)', r"\dfrac{e^x}{e^x+1}"),
       ('1/(3*x-2)**2', '-6/(3*x-2)**3', r'\dfrac{1}{(3x-2)^2}', r"\dfrac{-6}{(3x-2)^3}"),
       ('sqrt(log(x))', '1/(2*x*sqrt(log(x)))', r'\sqrt{\ln x}', r"\dfrac{1}{2x\sqrt{\ln x}}"),
       ('log((x-1)/(x+1))', '2/(x**2-1)', r'\ln\dfrac{x-1}{x+1}', r"\dfrac{2}{x^2-1}"),
       ('log(x**2+1)/log(10)', '2*x/((x**2+1)*log(10))', r'\log(x^2+1)', r"\dfrac{2x}{(x^2+1)\ln10}"),
       ('2**(x**2+1)', '2*x*2**(x**2+1)*log(2)', r'2^{x^2+1}', r"2x\cdot2^{x^2+1}\ln2")]
for f, d, _, _ in D4 + D4b: DER(f, d)
DER('x**2*exp(-x)', 'exp(-x)*(2*x-x**2)'); VAL('exp(-x)*(2*x-x**2)', 1, 'exp(-1)'); DER('log(x**2+3)', '2*x/(x**2+3)'); VAL('2*x/(x**2+3)', 1, '1/2')
S_.append(("Regla de la cadena", [
 (1, r"Calcula la funció derivada d'aquestes funcions compostes:" + tasks(2, ['$f(x)=%s$' % a for _, _, a, _ in D4])
     + recorda(r"Regla de la cadena: $\left[f(g(x))\right]'=f'(g(x))\cdot g'(x)$. Derivem la funció «de fora» deixant igual la «de dins» i ho multipliquem per la derivada de la de dins."),
     tasks(2, ["$f'(x)=\\res{%s}$" % b for _, _, _, b in D4])),
 (2, r"Deriva:" + tasks(3, ['$f(x)=%s$' % a for _, _, a, _ in D4b]),
     tasks(3, ["$\\res{%s}$" % b for _, _, _, b in D4b])),
 (2, r"Calcula $f'(1)$ si $f(x)=x^2e^{-x}$, i $g'(1)$ si $g(x)=\ln(x^2+3)$.",
     r"$f'(x)=2xe^{-x}-x^2e^{-x}=e^{-x}(2x-x^2)$: \ $f'(1)=\res{\frac1e}$. \ \ $g'(x)=\frac{2x}{x^2+3}$: \ $g'(1)=\res{\frac12}$."),
]))

# =====================================================================
# 5. Recta tangent i normal
VAL('x**2+2*x-1', 1, 2); DER('x**2+2*x-1', '2*x+2'); EQL('2+4*(x-1)', '4*x-2'); EQL('2-(x-1)/4', '-x/4+Rational(9,4)')
VAL('2*x**2-3*x', -1, 5); DER('2*x**2-3*x', '4*x-3'); VAL('4*x-3', -1, -7); EQL('5-7*(x+1)', '-7*x-2'); EQL('5+(x+1)/7', 'x/7+Rational(36,7)')
VAL('(x+1)/(x-1)', 2, 3); VAL('-2/(x-1)**2', 2, -2); EQL('3-2*(x-2)', '-2*x+7'); EQL('3+(x-2)/2', 'x/2+2')
VAL('log(x)', 1, 0); VAL('1/x', 1, 1); VAL('exp(2*x)', 0, 1); DER('exp(2*x)', '2*exp(2*x)')
CRIT('x**3-3*x**2+1', [0, 2]); VAL('x**3-3*x**2+1', 0, 1); VAL('x**3-3*x**2+1', 2, -3)
VAL('3*x**2-6*x', 3, 9); VAL('3*x**2-6*x', -1, 9); VAL('x**3-3*x**2+1', 3, 1); VAL('x**3-3*x**2+1', -1, -3); EQL('1+9*(x-3)', '9*x-26'); EQL('-3+9*(x+1)', '9*x+6')
S_.append(("Recta tangent i recta normal", [
 (1, r"Calcula l'equació de la recta tangent i de la recta normal a les funcions següents en el punt indicat:" + tasks(1, [r'$f(x)=x^2+2x-1$ \ en el punt d\'abscissa $x=1$', r'$f(x)=2x^2-3x$ \ en el punt d\'abscissa $x=-1$', r'$f(x)=\dfrac{x+1}{x-1}$ \ en el punt d\'abscissa $x=2$'])
     + recorda(r"Tangent: $y=f(a)+f'(a)(x-a)$. \ Normal (perpendicular a la tangent): $y=f(a)-\dfrac{1}{f'(a)}(x-a)$."),
     tasks(1, [r"$f(1)=2$, $f'(x)=2x+2$, $f'(1)=4$. \ Tangent: $\res{y=4x-2}$; \ normal: $y=2-\frac14(x-1)\Rightarrow\res{y=-\frac14x+\frac94}$",
               r"$f(-1)=5$, $f'(x)=4x-3$, $f'(-1)=-7$. \ Tangent: $\res{y=-7x-2}$; \ normal: $y=5+\frac17(x+1)\Rightarrow\res{y=\frac17x+\frac{36}{7}}$",
               r"$f(2)=3$, $f'(x)=\frac{-2}{(x-1)^2}$, $f'(2)=-2$. \ Tangent: $\res{y=-2x+7}$; \ normal: $y=3+\frac12(x-2)\Rightarrow\res{y=\frac12x+2}$"])),
 (1, r"Troba la recta tangent a $f(x)=\ln x$ en $x=1$ i la recta tangent a $g(x)=e^{2x}$ en $x=0$.",
     r"$f(1)=0$, $f'(1)=1$: \ $\res{y=x-1}$. \ \ $g(0)=1$, $g'(x)=2e^{2x}$, $g'(0)=2$: \ $\res{y=2x+1}$."),
 (2, r"Donada $f(x)=x^3-3x^2+1$:" + tasks(1, [r"En quins punts la recta tangent és horitzontal?", r"En quins punts la recta tangent és paral·lela a la recta $y=9x$? Escriu l'equació d'aquestes tangents."]),
     tasks(1, [r"$f'(x)=3x^2-6x=0\Rightarrow x=0,\ x=2$: \ $\res{(0,1)}$ i $\res{(2,-3)}$.",
               r"$3x^2-6x=9\Rightarrow x^2-2x-3=0\Rightarrow x=3,\ x=-1$. \ En $(3,1)$: $\res{y=9x-26}$; \ en $(-1,-3)$: $\res{y=9x+6}$."])),
 (2, r"Troba $a$ perquè la recta tangent a $f(x)=x^2+ax$ en $x=1$ tinga pendent 5. Escriu l'equació d'aquesta tangent.",
     r"$f'(x)=2x+a$, \ $f'(1)=2+a=5\Rightarrow\res{a=3}$. \ $f(1)=4$: \ $y=4+5(x-1)\Rightarrow\res{y=5x-1}$."),
]))
DER('x**2+3*x', '2*x+3'); VAL('x**2+3*x', 1, 4); EQL('4+5*(x-1)', '5*x-1')

# =====================================================================
# 6. Monotonia i extrems
CRIT('-x**2+5*x-1', ['5/2']); VAL('-x**2+5*x-1', '5/2', '21/4'); SIGN('-x**2+5*x-1', [(0, '+'), (3, '-')])
CRIT('2*x**3-3*x**2-12*x+5', [-1, 2]); VAL('2*x**3-3*x**2-12*x+5', -1, 12); VAL('2*x**3-3*x**2-12*x+5', 2, -15); SIGN('2*x**3-3*x**2-12*x+5', [(-2, '+'), (0, '-'), (3, '+')])
CRIT('x**2/(x-1)', [0, 2]); VAL('x**2/(x-1)', 2, 4); SIGN('x**2/(x-1)', [(-1, '+'), ('1/2', '-'), ('3/2', '-'), (3, '+')]); DER('x**2/(x-1)', '(x**2-2*x)/(x-1)**2')
CRIT('x*exp(x)', [-1]); VAL('x*exp(x)', -1, '-exp(-1)'); SIGN('x*exp(x)', [(-2, '-'), (0, '+')])
CRIT('log(x**2+1)', [0]); SIGN('log(x**2+1)', [(-1, '-'), (1, '+')])
CRIT('x**4-8*x**2+3', [-2, 0, 2]); VAL('12*x**2-16', 0, -16); VAL('12*x**2-16', 2, 32); VAL('x**4-8*x**2+3', 2, -13); VAL('x**4-8*x**2+3', 0, 3)
CRIT('x**3-3*x+2', [-1, 1]); VAL('x**3-3*x+2', -2, 0); VAL('x**3-3*x+2', -1, 4); VAL('x**3-3*x+2', 1, 0); VAL('x**3-3*x+2', 3, 20)
VAL('3*x**2+2*(-3)*x', 2, 0); VAL('x**3-3*x**2+1', 2, -3); VAL('6*x-6', 2, 6)
S_.append(("Monotonia i extrems", [
 (1, r"Estudia la monotonia (intervals de creixement i de decreixement) i els extrems relatius de les funcions:" + tasks(2, [r'$f(x)=-x^2+5x-1$', r'$f(x)=2x^3-3x^2-12x+5$'])
     + recorda(r"Calculem $f'(x)$, resolem $f'(x)=0$ i estudiem el signe de $f'$ en els intervals que determinen aquests punts i els que no són del domini: on $f'>0$ la funció creix i on $f'<0$ decreix. Si passa de créixer a decréixer hi ha un màxim relatiu; si passa de decréixer a créixer, un mínim."),
     tasks(1, [r"$f'(x)=-2x+5=0\Rightarrow x=\frac52$. \ Creixent en $\res{\left(-\infty,\frac52\right)}$ i decreixent en $\res{\left(\frac52,+\infty\right)}$. Màxim relatiu (i absolut) en $\res{\left(\frac52,\frac{21}{4}\right)}$.",
               r"$f'(x)=6x^2-6x-12=6(x+1)(x-2)$. \ Creixent en $\res{(-\infty,-1)\cup(2,+\infty)}$, decreixent en $\res{(-1,2)}$. Màxim relatiu $\res{(-1,12)}$, mínim relatiu $\res{(2,-15)}$."])),
 (2, r"\label{ex:racional}Estudia la monotonia i els extrems relatius de:" + tasks(3, [r'$f(x)=\dfrac{x^2}{x-1}$', r'$g(x)=x\,e^x$', r'$h(x)=\ln(x^2+1)$']),
     tasks(1, [r"$D=\mathbb R-\{1\}$, \ $f'(x)=\frac{x^2-2x}{(x-1)^2}=0\Rightarrow x=0,\ x=2$. \ Creixent en $\res{(-\infty,0)\cup(2,+\infty)}$, decreixent en $\res{(0,1)\cup(1,2)}$. Màxim $\res{(0,0)}$, mínim $\res{(2,4)}$.",
               r"$g'(x)=e^x(x+1)=0\Rightarrow x=-1$. \ Decreixent en $\res{(-\infty,-1)}$, creixent en $\res{(-1,+\infty)}$. Mínim $\res{\left(-1,-\frac1e\right)}$.",
               r"$h'(x)=\frac{2x}{x^2+1}=0\Rightarrow x=0$. \ Decreixent en $\res{(-\infty,0)}$, creixent en $\res{(0,+\infty)}$. Mínim $\res{(0,0)}$."])),
 (2, r"Troba els extrems relatius de $f(x)=x^4-8x^2+3$ amb el criteri de la segona derivada.",
     r"$f'(x)=4x^3-16x=4x(x^2-4)=0\Rightarrow x=0,\ x=\pm2$. \ $f''(x)=12x^2-16$: \ $f''(0)=-16<0$: màxim $\res{(0,3)}$; \ $f''(\pm2)=32>0$: mínims $\res{(-2,-13)}$ i $\res{(2,-13)}$."),
 (2, r"Calcula el màxim i el mínim absoluts de $f(x)=x^3-3x+2$ en l'interval $[-2,3]$."
     + recorda(r"Els extrems absoluts d'una funció contínua en $[a,b]$ són en els punts singulars de dins de l'interval o en els extrems $a$ i $b$: n'hi ha prou de comparar-ne els valors."),
     r"$f'(x)=3x^2-3=0\Rightarrow x=\pm1$ (tots dos dins). \ $f(-2)=0$, $f(-1)=4$, $f(1)=0$, $f(3)=20$. \ Màxim absolut $\res{(3,20)}$; mínim absolut $\res{0}$, en $x=-2$ i en $x=1$."),
 (3, r"Troba $a$ i $b$ perquè $f(x)=x^3+ax^2+b$ tinga un extrem relatiu en el punt $(2,-3)$. És un màxim o un mínim?",
     r"$f'(2)=12+4a=0\Rightarrow\res{a=-3}$. \ $f(2)=8-12+b=-3\Rightarrow\res{b=1}$. \ $f''(x)=6x-6$, $f''(2)=6>0$: \rest{mínim relatiu}."),
]))

# =====================================================================
# 7. Representació gràfica
G1 = tzg(-3, 3, -3, 3, CV % ('-2.2:2.2', '\\x*\\x*\\x-3*\\x') + dot(-1, 2) + dot(1, -2) + dot(0, 0) + dot(-1.732, 0) + dot(1.732, 0) + lab(-1, 2, '(-1,2)') + lab(1, -2, '(1,-2)', 'below'))
CRIT('x**3-3*x', [-1, 1]); VAL('x**3-3*x', -1, 2); VAL('x**3-3*x', 1, -2)
G2 = tzg(-5, 7, -6, 10, CV % ('-5:0.8', '\\x*\\x/(\\x-1)') + CV % ('1.15:7', '\\x*\\x/(\\x-1)') + dl(1, -6, 1, 10) + dl(-5, -4, 7, 8) + dot(0, 0) + dot(2, 4) + lab(2, 4, '(2,4)', 'below right'), sc=0.36)
EQL('x**2', '(x-1)*(x+1)+1')
G3 = tzg(-5, 5, -3, 3, CV % ('-5:5', '4*\\x/(\\x*\\x+1)') + dot(-1, -2) + dot(1, 2) + lab(1, 2, '(1,2)') + lab(-1, -2, '(-1,-2)', 'below'))
CRIT('4*x/(x**2+1)', [-1, 1]); VAL('4*x/(x**2+1)', 1, 2); DER('4*x/(x**2+1)', '4*(1-x**2)/(x**2+1)**2')
G4 = tzg(-3, 3, -2, 3, CV % ('-1.85:1.85', '\\x*\\x*\\x*\\x-2*\\x*\\x') + dot(-1, -1) + dot(1, -1) + dot(0, 0) + dot(-1.414, 0) + dot(1.414, 0))
CRIT('x**4-2*x**2', [-1, 0, 1]); VAL('x**4-2*x**2', 1, -1)
# exercicis nous de representació (polinomi i quatre racionals)
G5 = tzg(-1, 5, -2, 5, CV % ('-0.45:4.45', '\\x*\\x*\\x-6*\\x*\\x+9*\\x') + dot(0, 0) + dot(1, 4) + dot(3, 0) + lab(1, 4, '(1,4)') + lab(3, 0, '(3,0)', 'below'))
EQL('x**3-6*x**2+9*x', 'x*(x-3)**2'); DER('x**3-6*x**2+9*x', '3*(x-1)*(x-3)'); CRIT('x**3-6*x**2+9*x', [1, 3]); VAL('x**3-6*x**2+9*x', 1, 4); VAL('x**3-6*x**2+9*x', 3, 0)
SIGN('x**3-6*x**2+9*x', [(0, '+'), (2, '-'), (4, '+')])
G6 = tzg(-6, 6, -8, 8, CV % ('-6:-0.45', '(\\x*\\x+4)/\\x') + CV % ('0.45:6', '(\\x*\\x+4)/\\x') + dl(-6, -6, 6, 6) + dot(-2, -4) + dot(2, 4) + lab(2, 4, '(2,4)', 'below right') + lab(-2, -4, '(-2,-4)'), sc=0.3)
f6 = '(x**2+4)/x'
EQL(f6, 'x+4/x'); DER(f6, '(x**2-4)/x**2'); CRIT(f6, [-2, 2]); VAL(f6, -2, -4); VAL(f6, 2, 4); LIM(f6, 0, '-', '-oo'); LIM(f6, 0, '+', 'oo')
SIGN(f6, [(-3, '+'), (-1, '-'), (1, '-'), (3, '+')])
G7 = tzg(-6, 6, -4, 5, CV % ('-6:-2.08', '\\x*\\x/(\\x*\\x-4)') + CV % ('-1.92:1.92', '\\x*\\x/(\\x*\\x-4)') + CV % ('2.08:6', '\\x*\\x/(\\x*\\x-4)') + dl(-2, -4, -2, 5) + dl(2, -4, 2, 5) + dl(-6, 1, 6, 1) + dot(0, 0), sc=0.36)
f7 = 'x**2/(x**2-4)'
DER(f7, '-8*x/(x**2-4)**2'); CRIT(f7, [0]); VAL(f7, 0, 0); LIM(f7, 2, '-', '-oo'); LIM(f7, 2, '+', 'oo'); LIM(f7, -2, '-', 'oo'); LIM(f7, -2, '+', '-oo'); LIM(f7, 'oo', '', 1)
SIGN(f7, [(-3, '+'), (-1, '+'), (1, '-'), (3, '-')])
G8 = tzg(-7, 6, -14, 6, CV % ('-7:-1.25', '(\\x-1)*(\\x-1)/(\\x+1)') + CV % ('-0.7:6', '(\\x-1)*(\\x-1)/(\\x+1)') + dl(-1, -14, -1, 6) + dl(-7, -10, 6, 3) + dot(-3, -8) + dot(1, 0) + dot(0, 1) + lab(-3, -8, '(-3,-8)') + lab(1, 0, '(1,0)', 'below right'), sc=0.3)
f8 = '(x-1)**2/(x+1)'
EQL('x**2-2*x+1', '(x+1)*(x-3)+4'); DER(f8, '(x-1)*(x+3)/(x+1)**2'); CRIT(f8, [-3, 1]); VAL(f8, -3, -8); VAL(f8, 1, 0); VAL(f8, 0, 1); LIM(f8, -1, '-', '-oo'); LIM(f8, -1, '+', 'oo')
LIM(f8 + '-(x-3)', 'oo', '', 0); SIGN(f8, [(-4, '+'), (-2, '-'), (0, '-'), (2, '+')])
G9 = tzg(-6, 6, -4, 4, CV % ('-6:-2.06', '\\x/(\\x*\\x-4)') + CV % ('-1.94:1.94', '\\x/(\\x*\\x-4)') + CV % ('2.06:6', '\\x/(\\x*\\x-4)') + dl(-2, -4, -2, 4) + dl(2, -4, 2, 4) + dot(0, 0), sc=0.36)
f9 = 'x/(x**2-4)'
DER(f9, '-(x**2+4)/(x**2-4)**2'); CRIT(f9, []); LIM(f9, -2, '-', '-oo'); LIM(f9, -2, '+', 'oo'); LIM(f9, 2, '-', '-oo'); LIM(f9, 2, '+', 'oo'); LIM(f9, 'oo', '', 0)
SIGN(f9, [(-3, '-'), (-1, '-'), (1, '-'), (3, '-')]); VAL(f9, -1, '1/3'); VAL(f9, 1, '-1/3'); VAL(f9, 3, '3/5'); VAL(f9, -3, '-3/5')
S_.append(("Representació gràfica de funcions", [
 (2, r"Estudia i representa la funció $f(x)=x^3-3x$: domini, punts de tall, simetria, asímptotes, monotonia i extrems."
     + recorda(r"Passos: domini, punts de tall, simetria, asímptotes, monotonia i punts singulars, signe de la funció, taula de valors i representació gràfica."),
     r"$D=\mathbb R$; talls: $(0,0)$, $(\pm\sqrt3,0)$; \rest{senar} (simètrica respecte de l'origen); sense asímptotes (polinomi). \ $f'(x)=3x^2-3$: creix en $(-\infty,-1)\cup(1,+\infty)$ i decreix en $(-1,1)$; màxim $\res{(-1,2)}$ i mínim $\res{(1,-2)}$." + G(G1)),
 (2, r"Representa la funció $f(x)=\dfrac{x^2}{x-1}$ de l'exercici \ref{ex:racional}. Estudia'n abans les asímptotes.",
     r"$D=\mathbb R-\{1\}$; tall $(0,0)$; sense simetria. \ AV $x=1$: $\lim_{x\to1^-}f=-\infty$, $\lim_{x\to1^+}f=+\infty$. \ $x^2=(x-1)(x+1)+1$: AO $\res{y=x+1}$. \ Màxim $(0,0)$ i mínim $(2,4)$ (exercici \ref{ex:racional})." + G(G2)),
 (2, r"Estudia i representa $f(x)=\dfrac{4x}{x^2+1}$.",
     r"$D=\mathbb R$; tall $(0,0)$; \rest{senar}. \ Sense AV; AH $\res{y=0}$ ($\lim_{x\to\pm\infty}f=0$). \ $f'(x)=\frac{4(1-x^2)}{(x^2+1)^2}$: decreix en $(-\infty,-1)\cup(1,+\infty)$ i creix en $(-1,1)$; mínim $\res{(-1,-2)}$ i màxim $\res{(1,2)}$. Positiva si $x>0$." + G(G3)),
 (2, r"Estudia i representa $f(x)=x^4-2x^2$.",
     r"$D=\mathbb R$; talls $(0,0)$ i $(\pm\sqrt2,0)$; \rest{parella}; sense asímptotes. \ $f'(x)=4x^3-4x=4x(x-1)(x+1)$: decreix en $(-\infty,-1)\cup(0,1)$ i creix en $(-1,0)\cup(1,+\infty)$; mínims $\res{(\pm1,-1)}$ i màxim $\res{(0,0)}$." + G(G4)),
 (2, r"Estudia i representa $f(x)=x^3-6x^2+9x$.",
     r"$D=\mathbb R$; $f(x)=x(x-3)^2$: talls $(0,0)$ i $(3,0)$; sense simetria ni asímptotes. \ $f'(x)=3x^2-12x+9=3(x-1)(x-3)$: creix en $(-\infty,1)\cup(3,+\infty)$ i decreix en $(1,3)$; màxim $\res{(1,4)}$ i mínim $\res{(3,0)}$. Negativa si $x<0$." + G(G5)),
 (2, r"Estudia i representa $f(x)=\dfrac{x^2+4}{x}$.",
     r"$D=\mathbb R-\{0\}$; no talla els eixos; \rest{senar}. \ AV $x=0$: $\lim_{x\to0^-}f=-\infty$, $\lim_{x\to0^+}f=+\infty$. \ $f(x)=x+\frac4x$: AO $\res{y=x}$. \ $f'(x)=\frac{x^2-4}{x^2}$: creix en $(-\infty,-2)\cup(2,+\infty)$ i decreix en $(-2,0)\cup(0,2)$; màxim $\res{(-2,-4)}$ i mínim $\res{(2,4)}$. Negativa si $x<0$ i positiva si $x>0$." + G(G6)),
 (2, r"Estudia i representa $f(x)=\dfrac{x^2}{x^2-4}$.",
     r"$D=\mathbb R-\{-2,2\}$; tall $(0,0)$; \rest{parella}. \ AV $x=2$: $\lim_{x\to2^-}f=-\infty$, $\lim_{x\to2^+}f=+\infty$; AV $x=-2$: $\lim_{x\to-2^-}f=+\infty$, $\lim_{x\to-2^+}f=-\infty$. \ AH $\res{y=1}$. \ $f'(x)=\frac{-8x}{(x^2-4)^2}$: creix en $(-\infty,-2)\cup(-2,0)$ i decreix en $(0,2)\cup(2,+\infty)$; màxim relatiu $\res{(0,0)}$. Positiva en $(-\infty,-2)\cup(2,+\infty)$ i negativa en $(-2,0)\cup(0,2)$." + G(G7)),
 (3, r"Estudia i representa $f(x)=\dfrac{(x-1)^2}{x+1}$, amb les asímptotes verticals i obliqües.",
     r"$D=\mathbb R-\{-1\}$; talls $(1,0)$ i $(0,1)$; sense simetria. \ AV $x=-1$: $\lim_{x\to-1^-}f=-\infty$, $\lim_{x\to-1^+}f=+\infty$. \ $x^2-2x+1=(x+1)(x-3)+4$: AO $\res{y=x-3}$. \ $f'(x)=\frac{(x-1)(x+3)}{(x+1)^2}$: creix en $(-\infty,-3)\cup(1,+\infty)$ i decreix en $(-3,-1)\cup(-1,1)$; màxim $\res{(-3,-8)}$ i mínim $\res{(1,0)}$. Negativa si $x<-1$." + G(G8)),
 (3, r"Estudia i representa $f(x)=\dfrac{x}{x^2-4}$. Té extrems relatius?",
     r"$D=\mathbb R-\{-2,2\}$; tall $(0,0)$; \rest{senar}. \ AV $x=-2$: $\lim_{x\to-2^-}f=-\infty$, $\lim_{x\to-2^+}f=+\infty$; AV $x=2$: $\lim_{x\to2^-}f=-\infty$, $\lim_{x\to2^+}f=+\infty$. \ AH $\res{y=0}$. \ $f'(x)=\frac{-(x^2+4)}{(x^2-4)^2}<0$: \rest{decreixent} en tot el domini i \rest{sense extrems}. Positiva en $(-2,0)\cup(2,+\infty)$ i negativa en $(-\infty,-2)\cup(0,2)$." + G(G9)),
]))

# =====================================================================
# 8. Optimització (CCSS: funcions donades, amb estudi de la monotonia, i funcions de benefici o ingressos que cal construir)
CRIT('-x**2+40*x-300', [20]); VAL('-x**2+40*x-300', 20, 100); EQL('-x**2+40*x-300', '-(x-10)*(x-30)'); SIGN('-x**2+40*x-300', [(5, '+'), (25, '-')])
CRIT('x+100+3600/x', [-60, 60]); VAL('x+100+3600/x', 60, 220); SIGN('x+100+3600/x', [(30, '-'), (90, '+')])
CRIT('-2*x**3+21*x**2-36*x+40', [1, 6]); VAL('-2*x**3+21*x**2-36*x+40', 0, 40); VAL('-2*x**3+21*x**2-36*x+40', 1, 23); VAL('-2*x**3+21*x**2-36*x+40', 6, 148); VAL('-2*x**3+21*x**2-36*x+40', 7, 131)
SIGN('-2*x**3+21*x**2-36*x+40', [('1/2', '-'), (3, '+'), ('13/2', '-')])
CRIT('40*x/(x**2+16)', [-4, 4]); VAL('40*x/(x**2+16)', 4, 5); DER('40*x/(x**2+16)', '40*(16-x**2)/(x**2+16)**2'); SIGN('40*x/(x**2+16)', [(1, '+'), (5, '-')])
CRIT('10*x*exp(-x/5)', [5]); VAL('10*x*exp(-x/5)', 5, '50/e'); DER('10*x*exp(-x/5)', '(10-2*x)*exp(-x/5)'); SIGN('10*x*exp(-x/5)', [(1, '+'), (6, '-')])
assert abs(50 / math.e - 18.39) < 0.005
EQL('120*x-(2*x**2+40*x+300)', '-2*x**2+80*x-300'); CRIT('-2*x**2+80*x-300', [20]); VAL('-2*x**2+80*x-300', 20, 500)
EQL('(80-x)*(40+x)', '3200+40*x-x**2'); CRIT('(80-x)*(40+x)', [20]); VAL('(80-x)*(40+x)', 20, 3600)
EQL('(20-x)*(800+50*x)', '16000+200*x-50*x**2'); CRIT('(20-x)*(800+50*x)', [2]); VAL('(20-x)*(800+50*x)', 2, 16200)
EQL('(x-6)*(600-20*x)-1000', '-20*x**2+720*x-4600'); CRIT('(x-6)*(600-20*x)-1000', [18]); VAL('(x-6)*(600-20*x)-1000', 18, 1880); VAL('600-20*x', 18, 240)
CRIT('(10000-10*x**2)*(2+x/20)', ['(-40+sqrt(4600))/3', '(-40-sqrt(4600))/3']); VAL('(10000-10*x**2)*(2+x/20)', 9, '45031/2'); VAL('(10000-10*x**2)*(2+x/20)', 10, 22500); VAL('(10000-10*x**2)*(2+x/20)', 0, 20000); VAL('(10000-10*x**2)*(2+x/20)', 20, 18000)
assert abs((-40 + math.sqrt(4600)) / 3 - 9.27) < 0.01
S_.append(("Problemes d'optimització", [
 (1, r"El benefici mensual d'una empresa, en milers d'euros, quan ven $x$ centenars d'unitats és $B(x)=-x^2+40x-300$. Estudia el creixement i el decreixement de $B$. Quantes unitats ha de vendre per obtindre el benefici màxim? Quin és aquest benefici? Per a quines vendes té pèrdues?"
     + recorda(r"Si coneixem la funció: estudiem el signe de la derivada (on creix i on decreix), trobem els punts on $f'(x)=0$, justifiquem si són màxims o mínims i comprovem que la solució té sentit en el context (unitats positives, hores dins de l'interval\ldots)."),
     r"$B'(x)=-2x+40=0\Rightarrow x=20$. \ Creixent en $\res{(0,20)}$ i decreixent en $\res{(20,+\infty)}$: màxim en $x=20$. \ Ha de vendre $\res{2\,000\text{ unitats}}$ i el benefici màxim és $B(20)=\res{100\,000\text{ €}}$. \ $B(x)=-(x-10)(x-30)<0$ si $x<10$ o $x>30$: pèrdues amb \rest{menys de 1\,000 o més de 3\,000 unitats}."),
 (2, r"El cost total de produir $x$ unitats d'un article és $C(x)=x^2+100x+3\,600$ euros. Troba la funció de cost mitjà per unitat, $M(x)=\frac{C(x)}{x}$, estudia'n el creixement i el decreixement i calcula quantes unitats cal produir perquè siga mínim. Quin és aquest cost mitjà?",
     r"$M(x)=x+100+\frac{3\,600}{x}$, $x>0$. \ $M'(x)=1-\frac{3\,600}{x^2}=0\Rightarrow x=60$. \ Decreixent en $\res{(0,60)}$ i creixent en $\res{(60,+\infty)}$: mínim. \ $\res{60\text{ unitats}}$, amb un cost mitjà de $M(60)=\res{220\text{ €}}$."),
 (2, r"El nombre de persones connectades a una plataforma de vídeo (en milers) entre les 17 h i les 24 h és $N(t)=-2t^3+21t^2-36t+40$, on $t\in[0,7]$ són les hores que han passat des de les 17 h. Estudia quan augmenta i quan disminueix el nombre de connexions. A quina hora hi ha més persones connectades? I menys?",
     r"$N'(t)=-6t^2+42t-36=-6(t-1)(t-6)=0\Rightarrow t=1,\ t=6$. \ Decreix en $\res{(0,1)\cup(6,7)}$ i creix en $\res{(1,6)}$. \ $N(0)=40$, $N(1)=23$, $N(6)=148$, $N(7)=131$. \ Màxim a les $\res{23\text{ h}}$ (148\,000 persones) i mínim a les $\res{18\text{ h}}$ (23\,000 persones)."),
 (2, r"Les vendes d'un mòbil nou, en milers d'unitats al mes, $t$ mesos després de llançar-lo són $V(t)=\dfrac{40t}{t^2+16}$, $t\geq0$. Estudia el creixement i el decreixement de les vendes. En quin moment són màximes i quantes se'n venen? Què passa a llarg termini?",
     r"$V'(t)=\frac{40(t^2+16)-40t\cdot2t}{(t^2+16)^2}=\frac{40(16-t^2)}{(t^2+16)^2}=0\Rightarrow t=4$ ($t=-4$ no té sentit). \ Creixent en $\res{(0,4)}$ i decreixent en $\res{(4,+\infty)}$. \ Màxim al $\res{\text{quart mes}}$: $V(4)=\frac{160}{32}=\res{5\,000\text{ unitats}}$. \ $\lim_{t\to+\infty}V(t)=0$: les vendes \rest{tendeixen a desaparéixer}."),
 (3, r"Una empresa estima que el benefici d'una campanya, en milers d'euros, si inverteix $x$ milers d'euros en publicitat, és $B(x)=10x\,e^{-0{,}2x}$, $x\geq0$. Estudia el creixement i el decreixement de $B$. Quant ha d'invertir per obtindre el benefici màxim? Quin és?",
     r"$B'(x)=10e^{-0{,}2x}+10x\cdot(-0{,}2)e^{-0{,}2x}=(10-2x)\,e^{-0{,}2x}=0\Rightarrow x=5$ (l'exponencial no s'anul·la mai). \ Creixent en $\res{(0,5)}$ i decreixent en $\res{(5,+\infty)}$. \ Ha d'invertir $\res{5\,000\text{ €}}$ i el benefici màxim és $B(5)=\frac{50}{e}\approx\res{18\,394\text{ €}}$."),
 (2, r"Una empresa ven cada unitat que fabrica a 120~€, i el cost de fabricar-ne $x$ al dia és $C(x)=2x^2+40x+300$ euros. Escriu la funció de benefici diari i calcula quantes unitats ha de fabricar per maximitzar-lo. Quin és el benefici màxim?"
     + recorda(r"Si hem de construir la funció: \ ingressos = preu $\cdot$ quantitat venuda; \ benefici = ingressos $-$ costos. Tria bé la variable, escriu el preu i la quantitat en funció d'ella i indica quins valors pot prendre."),
     r"$B(x)=120x-(2x^2+40x+300)=-2x^2+80x-300$. \ $B'(x)=-4x+80=0\Rightarrow x=20$; $B''=-4<0$: màxim. \ $\res{20\text{ unitats}}$ al dia, amb un benefici de $B(20)=\res{500\text{ €}}$."),
 (2, r"Un hotel té 80 habitacions i, a 50~€ la nit, les té totes ocupades. Per cada euro que puja el preu, queda una habitació buida. Cada habitació ocupada li costa 10~€ de neteja i manteniment. Quin preu fa màxim el benefici? Quantes habitacions s'ocupen i quin és el benefici?",
     r"$x$ = euros que puja el preu: s'ocupen $80-x$ habitacions i cadascuna deixa $50+x-10=40+x$ euros. \ $B(x)=(80-x)(40+x)=3\,200+40x-x^2$, \ $0\leq x\leq80$. \ $B'(x)=40-2x=0\Rightarrow x=20$; $B''=-2<0$: màxim. \ Preu $\res{70\text{ €}}$, $\res{60\text{ habitacions}}$ ocupades i un benefici de $60\cdot60=\res{3\,600\text{ €}}$ per nit."),
 (2, r"Un concert benèfic té 800 espectadors si l'entrada costa 20~€. Per cada euro que es rebaixa l'entrada, hi van 50 persones més. Quin preu fa màxima la recaptació? Quantes persones hi van i quant es recapta?",
     r"$x$ = euros de rebaixa: preu $20-x$, espectadors $800+50x$. \ $R(x)=(20-x)(800+50x)=16\,000+200x-50x^2$. \ $R'(x)=200-100x=0\Rightarrow x=2$; $R''=-100<0$: màxim. \ Preu $\res{18\text{ €}}$, $\res{900\text{ persones}}$ i una recaptació de $\res{16\,200\text{ €}}$."),
 (3, r"La demanda setmanal d'un producte és $q=600-20p$ unitats quan el preu és $p$ euros. Fabricar cada unitat costa 6~€ i, a més, l'empresa té uns costos fixos de 1\,000~€ setmanals. Escriu el benefici en funció del preu i troba el preu que el fa màxim. Quantes unitats es venen i quin és el benefici?",
     r"$B(p)=\underbrace{p\,(600-20p)}_{\text{ingressos}}-\underbrace{\big(6(600-20p)+1\,000\big)}_{\text{costos}}=(p-6)(600-20p)-1\,000=-20p^2+720p-4\,600$, \ $6\leq p\leq30$. \ $B'(p)=-40p+720=0\Rightarrow p=18$; $B''<0$: màxim. \ Preu $\res{18\text{ €}}$, $q=\res{240\text{ unitats}}$ i benefici $B(18)=\res{1\,880\text{ €}}$."),
 (3, r"Una comerciant té 10\,000 kg de raïm que podria vendre hui a 2~€ el kg. El preu augmentarà 5 cèntims cada dia, però cada dia se'n fan malbé 10 kg per cada quadrat dels dies que transcorren ($10t^2$ kg). Si pot esperar com a molt 20 dies, quin dia li convé vendre?",
     r"Ingressos = quilos $\cdot$ preu: \ $I(t)=(10\,000-10t^2)(2+0{,}05t)$, $t\in[0,20]$. \ $I'(t)=-1{,}5t^2-40t+500=0\Rightarrow t\approx9{,}27$. \ Amb dies enters: $I(9)=22\,515{,}5$, $I(10)=22\,500$; \ $I(0)=20\,000$, $I(20)=18\,000$. \ Li convé vendre el \rest{9é dia}: $\res{22\,515{,}50\text{ €}}$."),
]))

# =====================================================================
pre = open(os.path.join(HERE, 'preamble.tex'), encoding='utf-8').read()
pre = pre.split('% ---------- recta real ----------')[0]
KW = "pdfkeywords={taxa de variació mitjana, derivada, funció derivada, regles de derivació, regla de la cadena, recta tangent, recta normal, monotonia, màxims i mínims, representació gràfica, optimització}"
pre = re.sub(r'pdfkeywords=\{[^}]*\}', lambda mm: KW, pre)
pre = pre.replace('pdfsubject={Matemàtiques 3r ESO}', 'pdfsubject={Matemàtiques Aplicades a les CCSS I}')
pre = pre.replace('after-item-skip=2pt', 'after-item-skip=5pt')
pre = pre.replace(r'{\color{navy}\bfseries\theexer.}\ \ {\small\estrelles{#1}}\ \ }', r'{\color{navy}\bfseries\theexer.}\ \ }')
assert 'estrelles{#1}}' not in pre
pre = pre.replace(r'\stepcounter{exer}', r'\refstepcounter{exer}')
pre += r'\newcommand{\exf}[1]{\par\medskip\refstepcounter{exer}\noindent{\color{navy}\bfseries\theexer.}\ \ }' + '\n'
pre = pre.replace(r'\needspace{10\baselineskip}\bigskip', r'\needspace{16\baselineskip}\bigskip')
pre += r'''\providecommand{\gt}{>}\providecommand{\lt}{<}
% quadre de recordatori (només a la fitxa d'exercicis)
\newcommand{\recorda}[1]{\par\smallskip\begin{tcolorbox}[colback=accent!7,colframe=accent!55,arc=2mm,boxrule=0.5pt,left=2.5mm,right=2.5mm,top=1mm,bottom=1mm]\small{\color{accent}\faLightbulb[regular]}\ \textbf{Recorda:}\ #1\end{tcolorbox}}
'''

def fix(t):
    """Fora dels dibuixos: l'espai després de la coma en coordenades com (2,-1), que amb icomma quedaria enganxat."""
    parts = re.split(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', t, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'(?<!\\),-(?=[0-9\\])', r',\\,-', parts[i].replace("\\'", "'"))
    return ''.join(parts)

TIT = "Derivades i aplicacions"
def build(sol):
    t = 'Solucions de la fitxa' if sol else "Fitxa d'exercicis"
    p = pre.replace("pdftitle={Fitxa d'exercicis de la unitat 3: Proporcionalitat i percentatges. 3r d'ESO}",
                    "pdftitle={%s de la unitat 7: %s. 1r de Batxillerat CCSS}" % (t, TIT))
    p = p.replace("Fitxa d'exercicis · Unitat 3: Proporcionalitat i percentatges · 3r d'ESO", "%s · Unitat 7: %s · 1r Batxillerat CCSS" % (t, TIT))
    assert 'aplicacions · 1r' in p and 'unitat 7: Derivades' in p
    out = [p, '\\newcommand{\\res}[1]{\\boxed{#1}}\\newcommand{\\rest}[1]{\\fbox{#1}}\n' if sol else '\\newcommand{\\res}[1]{#1}\\newcommand{\\rest}[1]{#1}\n']
    out.append(r'''
\def\fmneed{11}% que el títol d'una secció no quede sol al final del full
\input{../comu/fentmates.tex}
\fmcurs{1batx-ccss}

\begin{document}
\thispagestyle{primera}

\capcalera{Matemàtiques CCSS}{1r Batx}{''' + ('Solucions de la fitxa · Unitat 7' if sol else "Fitxa d'exercicis · Unitat 7") + r'''}{\raggedright ''' + TIT + r'''}
''')
    if not sol:
        out.append('\\vspace{10pt}\nNom i cognoms: \\rule{8.4cm}{0.4pt}\\hfill Grup: \\rule{1.6cm}{0.4pt}\\hfill Data: \\rule{2.2cm}{0.4pt}\n')
    out.append(r'''\vspace{8pt}

\begin{tcolorbox}[colback=soft,colframe=soft,arc=2mm,left=3mm,right=3mm,top=1.5mm,bottom=1.5mm]
\small ''' + (r"Intenta resoldre cada exercici abans de mirar-ne la solució. Si no t'ix el mateix resultat, repassa els passos o comprova'l amb la calculadora de derivades i les eines dels apunts interactius de la unitat."
             if sol else r"Resol els exercicis al quadern mostrant tots els passos i simplifica sempre les derivades. Les seccions segueixen l'ordre dels apunts. Pots comprovar les derivades amb la calculadora de derivades dels apunts interactius.") + r'''
\end{tcolorbox}
''')
    for i, (title, exs) in enumerate(S_, 1):
        out.append('\n%% =====================================================\n\\seccio{%d}{%s}\n\n' % (i, title))
        for j, (st_, q, s) in enumerate(exs):
            if sol:
                lab = re.search(r'\\label\{[^}]*\}', q)
                s = (lab.group(0) if lab else '') + s
            out.append('\\%s{%d} %s\n\n' % ('exf' if j == 0 else 'ex', st_, fix(s if sol else q)))
    if not sol:
        out.append('\\vfill\n\\begin{center}\\color{muted}\\small\\faCheckCircle[regular]\\ \\ Ànim! Comprova les teues derivades amb la calculadora dels apunts interactius.\\end{center}\n')
    out.append('\n\\end{document}\n')
    name = 't7-fitxa-solucions.tex' if sol else 't7-fitxa-exercicis.tex'
    open(os.path.join(HERE, name), 'w', encoding='utf-8', newline='\n').write(''.join(out))

build(False); build(True)
print(sum(len(s_[1]) for s_ in S_), 'exercicis;', NCHK[0], 'comprovacions')
