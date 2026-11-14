# Ajuda per a les versions en castellà de les fitxes (genera-es.py de cada unitat).
#
#   from castella import preambul
#   p = preambul(pre, pdftitle="Ficha de ejercicios de la unidad 4: ...", capcalera="Ficha de ejercicios · Unidad 4: ...")
#
# Canvia el babel, la llicència, el títol del PDF i la capçalera de les pàgines del preamble.tex (en valencià).
# El curs s'escriu «3º ESO». Al text, la «o» volada es fa amb \textsuperscript{o}, perquè el caràcter «º»
# de Fira Sans porta un guió baix; a les metadades del PDF (que no es veuen) es deixa el caràcter «º».
# Les metadades del PDF van a \AtBeginDocument: dins de les opcions de hyperref, «º» no compila.
#
# Per a altres cursos, passa curs='1eso', '4eso-b', '1batx-mi', '2batx-ccss' o '2batx-mii' a preambul()
# i fes servir assignatura(curs) en lloc d'ASSIGNATURA (\capcalera{Matemáticas ...}{curs}).
import re

# clau -> (curs al text, curs a les metadades, assignatura)
CURSOS = {
    "1eso": (r"1\textsuperscript{o} ESO", "1º ESO", "Matemáticas"),
    "3eso": (r"3\textsuperscript{o} ESO", "3º ESO", "Matemáticas"),
    "4eso-b": (r"4\textsuperscript{o} ESO", "4º ESO", "Matemáticas B"),
    "1batx-mi": (r"1\textsuperscript{o} Bach.", "1º Bach.", "Matemáticas I"),
    "2batx-ccss": (r"2\textsuperscript{o} Bach.", "2º Bach.", "Matemáticas CCSS"),
    "2batx-mii": (r"2\textsuperscript{o} Bach.", "2º Bach.", "Matemáticas II"),
}
CURS = CURSOS["3eso"][0]
ASSIGNATURA = r"\capcalera{Matemáticas}{%s}" % CURS


# en castellà, el sinus s'escriu «sen» (i l'arcsinus, «arcsen»)
SEN = "\n\\AtBeginDocument{\\renewcommand{\\sin}{\\operatorname{sen}}\\renewcommand{\\arcsin}{\\operatorname{arcsen}}}"


def assignatura(curs="3eso"):
    """\capcalera{<assignatura>}{<curs>} (falten els dos últims arguments: tipus · Unidad N i títol)"""
    t, _, a = CURSOS[curs]
    return r"\capcalera{%s}{%s}" % (a, t)


def preambul(pre, pdftitle, capcalera, pdfkeywords, curs="3eso"):
    ctext, cmeta, assig = CURSOS[curs]
    canvis = [
        (r"\usepackage[catalan]{babel}", r"\usepackage[spanish,es-minimal,es-noshorthands]{babel}" + SEN),
        (r"https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ca}{\ccbyncsa}\ \ Llicència Creative Commons Reconeixement-NoComercial-CompartirIgual",
         r"https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es}{\ccbyncsa}\ \ Licencia Creative Commons Atribución-NoComercial-CompartirIgual"),
    ]
    for a, b in canvis:
        assert a in pre, a
        pre = pre.replace(a, b)
    m = re.search(r"\\usepackage\[hidelinks,.*\]\{hyperref\}\n", pre)
    assert m
    pre = pre.replace(m.group(0), "\\usepackage[hidelinks]{hyperref}\n\\AtBeginDocument{\\hypersetup{pdftitle={%s. %s},"
                      "pdfsubject={%s %s},pdfkeywords={%s}}}\n" % (pdftitle, cmeta, assig, cmeta, pdfkeywords))
    pre, n = re.subn(r"(\\fancyhead\[C\]\{\\small\\color\{muted\})[^\n]*\}\n", lambda m: m.group(1) + capcalera + " · " + ctext + "}\n", pre)
    assert n == 1
    return pre
