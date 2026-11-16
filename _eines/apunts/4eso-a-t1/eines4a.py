# Ajudes dels apunts de la Unitat 1 de 4t ESO A (Nombres naturals, enters i fraccionaris).
# Reaprofita les de ../2eso-t2/comu.py (fraccions) i hi afig els ginys d'enters de ../2eso-t1/build.py.
# Els ginys i entrenadors d'enters porten la classe «wz»: els fa anar la part 2 d'app.js (la de 2eso-t1);
# la resta, la part 1 (la de 2eso-t2).
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '2eso-t2'))
from comu import *            # L, P, box, note, sub, ul, ol, level, prob, practice, drill, quick, nin, seg, widget, table, fin, ops, hier, ck, Fr...
from fractions import Fraction

def sec(i, title, body):
    return (f'\n<!-- ======================= 1.{i} ======================= -->\n<section class="unit" id="s{i}">\n'
            f'  <div class="sec-head"><span class="num">1.{i}</span><h2>{title}</h2></div>\n{body}</section>\n')

def ninz(k, va, es, en, val, cls='s'):
    """camp de text per a enters (sense inputmode decimal, perquè el mòbil mostre el signe menys)"""
    return f'<label>{L(va, es, en)} <input class="tin {cls}" type="text" data-k="{k}" value="{val}" autocomplete="off" aria-label="{k}"></label>'

def drillz(kind, va, es, en):
    """entrenador d'enters (part 2 d'app.js), amb el botó ±"""
    return f'''<div class="widget w-drill wz" data-kind="{kind}">
  <div class="wt">🎯 {L(va, es, en)}</div>
  <div class="dq"></div>
  <div class="wrow"><label>{L("Resultat", "Resultado", "Answer")} <input class="tin m" type="text" autocomplete="off" aria-label="resultat"></label><button class="btn drill-neg" type="button" data-a="neg" aria-label="±">±</button><button class="btn primary" type="button" data-a="check">{L("Comprova", "Comprobar", "Check")}</button><button class="btn" type="button" data-a="new">↻ {L("Un altre", "Otro", "Another")}</button><span class="dscore"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''

def hierz(presets):
    """calculadora pas a pas amb enters, potències i arrels (part 2 d'app.js)"""
    keys = ''.join(f'<button type="button" data-ins="{k}">{k}</button>' for k in ['−', '·', ':', '^', '√', '(', ')', '[', ']'])
    q = ''.join(f'<button type="button" data-e="{e}">{e.replace("-", "−")}</button>' for e in presets)
    return f'''<div class="widget w-hier wz">
  <div class="wt">🧮 {L("Calculadora pas a pas", "Calculadora paso a paso", "Step-by-step calculator")}</div>
  <div class="wrow"><label>{L("Expressió", "Expresión", "Expression")} <input class="tin w" type="text" value="{presets[0].replace("-", "−")}" autocomplete="off" spellcheck="false" aria-label="expressió"></label></div>
  <div class="quick kp"><span class="ql">⌨</span>{keys}</div>
  <div class="quick"><span class="ql">⚡</span>{q}</div>
  <div class="hsteps"></div>
  <div class="steps-ctl"><button class="btn primary" type="button" data-a="next"></button><button class="btn" type="button" data-a="all"></button><span class="step-count"></span></div>
  <div class="info" aria-live="polite"></div>
</div>
'''

# ---------- comprovació d'expressions enteres (amb potències i arrels) ----------
def ev(e):
    """valor exacte d'una expressió escrita amb - · : ^ √ ( ) [ ]"""
    from math import isqrt
    s = e.replace('−', '-').replace('·', '*').replace(':', '/').replace('[', '(').replace(']', ')').replace('^', '**')
    s = re.sub(r'√(\d+)', r'R(\1)', s).replace('√(', 'R(')
    s = re.sub(r'(?<![\w.])(\d+)', r'F(\1)', s)
    def R(x):
        r = isqrt(int(x)); assert r * r == x, e; return Fraction(r)
    return eval(s, {'F': Fraction, 'R': R})

# ---------- recta numèrica estàtica (de 2eso-t1) ----------
def nline(lo, hi, pts=(), h=78):
    X0, X1 = 40, 580
    x = lambda v: X0 + (v - lo) * (X1 - X0) / (hi - lo)
    s = (f'<div class="nline"><svg viewBox="0 0 620 {h}" role="img" aria-label="recta"><line class="sv-ax" x1="16" y1="40" x2="604" y2="40"/>'
         '<path class="sv-ax" d="M596 34 L606 40 L596 46" fill="none"/><path class="sv-ax" d="M24 34 L14 40 L24 46" fill="none"/>')
    for v in range(lo, hi + 1):
        c = 'sv-tb' if v == 0 else 'sv-t'
        s += f'<line class="sv-ax" x1="{x(v):.1f}" y1="33" x2="{x(v):.1f}" y2="47"/><text class="{c}" x="{x(v):.1f}" y="68" text-anchor="middle">{str(v).replace("-", "−")}</text>'
    for v in pts:
        s += f'<circle class="{"sv-neg" if v < 0 else "sv-pos" if v > 0 else "sv-dot"}" cx="{x(v):.1f}" cy="40" r="6"/>'
    return s + '</svg></div>'

# ---------- ginys d'enters (de 2eso-t1/build.py) ----------
SGT = ('<div class="tbl-wrap"><table class="data sgtab"><thead><tr><th class="sop">·</th><th>+</th><th>−</th></tr></thead><tbody>'
       '<tr><th>+</th><td class="pos" data-c="pp">+</td><td class="neg" data-c="pn">−</td></tr>'
       '<tr><th>−</th><td class="neg" data-c="np">−</td><td class="pos" data-c="nn">+</td></tr></tbody></table></div>')

W_ctx = f'''<div class="widget" id="w-ctx">
  <div class="wt">🌡 {L("De la situació al nombre enter", "De la situación al número entero", "From the situation to the integer")}</div>
  <div class="wrow">{seg([("temp", L("Temperatura", "Temperatura", "Temperature")), ("floor", L("Plantes", "Plantas", "Floors")), ("alt", L("Altitud", "Altitud", "Altitude")), ("money", L("Diners", "Dinero", "Money")), ("year", L("Anys", "Años", "Years"))], "temp")}</div>
  <div class="wrow">{ninz("v", "Nombre enter", "Número entero", "Integer", "-6", "m")}</div>
  {quick([("temp|-6", "−6 °C"), ("floor|-3", L("3r soterrani", "3.er sótano", "3rd basement")), ("alt|432", "432 m"), ("alt|-120", "−120 m"), ("money|-25", L("dec 25 €", "debo 25 €", "owe €25")), ("year|-470", "470 a. C."), ("year|0", L("any 0?", "¿año 0?", "year 0?"))])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_line = f'''<div class="widget" id="w-line">
  <div class="wt">📏 {L("Representa i ordena", "Representa y ordena", "Plot and order")}</div>
  <div class="wrow"><label>{L("Nombres", "Números", "Numbers")} <input class="tin w" type="text" data-k="v" value="−2, 0, 4, −1, 8, −3, −7, 1" autocomplete="off" spellcheck="false" aria-label="nombres"></label>{seg([("asc", L("menor → major", "menor → mayor", "smallest → largest")), ("desc", L("major → menor", "mayor → menor", "largest → smallest"))], "asc")}</div>
  {quick([("−7, 3, 1, −4, 6, −5, −2, 0", "−7, 3, 1, −4…"), ("−8, −9", "−8 ? −9"), ("−6, 6", "−6 ? 6"), ("−15, −51", "−15 ? −51"), ("−120, 35, −300, 0, 210", "−120, 35, −300…")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_abs = f'''<div class="widget" id="w-abs">
  <div class="wt">↔ {L("Valor absolut i oposat", "Valor absoluto y opuesto", "Absolute value and opposite")}</div>
  <div class="wrow">{ninz("a", "Nombre enter", "Número entero", "Integer", "-5", "m")}</div>
  {quick([("-5", "−5"), ("8", "8"), ("-23", "−23"), ("0", "0"), ("-100", "−100"), ("18", "18")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_add = f'''<div class="widget" id="w-add">
  <div class="wt">➕ {L("Sumes i restes en la recta", "Sumas y restas en la recta", "Adding and subtracting on the number line")}</div>
  <div class="wrow">{ninz("a", "Partim de", "Partimos de", "Start at", "-2")}{seg([("+", "+"), ("-", "−")], "+")}{ninz("b", "Nombre", "Número", "Number", "6")}</div>
  {quick([("-2|+|6", "−2 + 6"), ("5|-|7", "5 − 7"), ("-8|-|9", "−8 − 9"), ("-3|+|-4", "−3 + (−4)"), ("4|-|-6", "4 − (−6)"), ("-5|+|5", "−5 + 5")])}
  <div class="chart"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_par = f'''<div class="widget" id="w-par">
  <div class="wt">🧹 {L("Lleva els parèntesis", "Quita los paréntesis", "Remove the brackets")}</div>
  <div class="wrow"><label>{L("Expressió", "Expresión", "Expression")} <input class="tin w" type="text" value="−(+4) + (−8) − (−6) + 4 − 1" autocomplete="off" spellcheck="false" aria-label="expressió"></label></div>
  <div class="quick"><span class="ql">⚡</span>{"".join(f'<button type="button" data-e="{e}">{e}</button>' for e in ["(−6) + (−3)", "(+7) + (−4)", "3 − (−1)", "−(−5) + 3", "(−2) − (+3) + (−6)", "−(−3) + (−1) − (+3) − (−8)", "12 − 25 + 3 − 8 − (−6)"])}</div>
  <div class="pchips"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_sign = f'''<div class="widget" id="w-sign">
  <div class="wt">✖ {L("La regla dels signes", "La regla de los signos", "The sign rule")}</div>
  <div class="wrow">{ninz("a", "a", "a", "a", "-6")}{seg([("·", "·"), (":", ":")], "·")}{ninz("b", "b", "b", "b", "4")}</div>
  {quick([("-6|·|4", "(−6)·(+4)"), ("-5|·|-7", "(−5)·(−7)"), ("3|·|-8", "(+3)·(−8)"), ("-36|:|9", "(−36):(+9)"), ("-48|:|-8", "(−48):(−8)"), ("42|:|-7", "(+42):(−7)"), ("-7|:|2", "(−7):(+2)")])}
  {SGT}
  <div class="info" aria-live="polite"></div>
</div>'''

W_powz = f'''<div class="widget" id="w-powz">
  <div class="wt">⚡ {L("Potències amb base entera", "Potencias con base entera", "Powers with an integer base")}</div>
  <div class="wrow">{ninz("b", "Base", "Base", "Base", "-2")}{ninz("n", "Exponent", "Exponente", "Exponent", "5")}</div>
  {quick([("-2|5", "(−2)⁵"), ("-2|4", "(−2)⁴"), ("-3|3", "(−3)³"), ("-1|7", "(−1)⁷"), ("-1|10", "(−1)¹⁰"), ("-10|6", "(−10)⁶"), ("4|3", "4³"), ("-7|0", "(−7)⁰")])}
  <div class="pz"></div>
  <div class="info" aria-live="polite"></div>
</div>'''

W_rootz = f'''<div class="widget" id="w-rootz">
  <div class="wt">√ {L("Arrel quadrada", "Raíz cuadrada", "Square root")}</div>
  <div class="wrow">{ninz("a", "Radicand", "Radicando", "Radicand", "50")}</div>
  {quick([("49", "49"), ("50", "50"), ("144", "144"), ("200", "200"), ("-16", "−16"), ("0", "0"), ("1000", "1000")])}
  <div class="rz"></div>
  <div class="info" aria-live="polite"></div>
</div>'''
