# Ajuda per a les versions en castellà de les fitxes (genera-es.py de cada unitat).
#
#   from castella import preambul
#   p = preambul(pre, pdftitle="Ficha de ejercicios de la unidad 4: ...", capcalera="Ficha de ejercicios · Unidad 4: ...")
#
# Canvia el babel, la llicència, el títol del PDF i la capçalera de les pàgines del preamble.tex (en valencià).
# El curs s'escriu «3º ESO». Al text, la «o» volada es fa amb \textsuperscript{o}, perquè el caràcter «º»
# de Fira Sans porta un guió baix; a les metadades del PDF (que no es veuen) es deixa el caràcter «º».
# Les metadades del PDF van a \AtBeginDocument: dins de les opcions de hyperref, «º» no compila.
import re

CURS = r"3\textsuperscript{o} ESO"
ASSIGNATURA = r"\capcalera{Matemáticas}{%s}" % CURS


def preambul(pre, pdftitle, capcalera, pdfkeywords):
    canvis = [
        (r"\usepackage[catalan]{babel}", r"\usepackage[spanish,es-minimal,es-noshorthands]{babel}"),
        (r"https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ca}{\ccbyncsa}\ \ Llicència Creative Commons Reconeixement-NoComercial-CompartirIgual",
         r"https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es}{\ccbyncsa}\ \ Licencia Creative Commons Atribución-NoComercial-CompartirIgual"),
    ]
    for a, b in canvis:
        assert a in pre, a
        pre = pre.replace(a, b)
    m = re.search(r"\\usepackage\[hidelinks,.*\]\{hyperref\}\n", pre)
    assert m
    pre = pre.replace(m.group(0), "\\usepackage[hidelinks]{hyperref}\n\\AtBeginDocument{\\hypersetup{pdftitle={%s. 3º ESO},"
                      "pdfsubject={Matemáticas 3º ESO},pdfkeywords={%s}}}\n" % (pdftitle, pdfkeywords))
    pre, n = re.subn(r"(\\fancyhead\[C\]\{\\small\\color\{muted\})[^\n]*\}\n", lambda m: m.group(1) + capcalera + " · " + CURS + "}\n", pre)
    assert n == 1
    return pre
