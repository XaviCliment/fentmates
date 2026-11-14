#!/usr/bin/env python3
"""
Genera les guies «Amb la calculadora» a partir de guies.py.
Ús (des de la carpeta arrel del web):  python3 _eines/casio/build_casio.py
"""
import html, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)
from guies import GUIDES  # noqa: E402
from guies_es import GUIDES as GUIDES_ES  # noqa: E402

LANG = ["va"]

# nom intern -> (text de la tecla, classe, descripció)
KEYS = {
    "HOME": ("⌂", "fn", "HOME"), "CONFIG": ("☰", "fn", "CONFIG (ajustos)"),
    "CATALOG": ("CATALOG", "fn", "CATALOG"), "TOOLS": ("⋯", "fn", "TOOLS (eines)"),
    "FORMAT": ("FORMAT", "fn", "FORMAT"), "VAR": ("x⇄", "fn", "VARIABLE"),
    "FUNC": ("f(x)", "fn", "FUNCTION"), "OK": ("OK", "ok", "OK"), "EXE": ("EXE", "exe", "EXE (executar)"),
    "AC": ("AC", "ac", "AC"), "BACK": ("↶", "fn", "Tornar enrere"), "DEL": ("DEL", "ac", "Esborrar"),
    "SHIFT": ("⇧", "shift", "SHIFT"), "FRAC": ("▭⁄▭", "num", "Fracció"),
    "SQRT": ("√▭", "num", "Arrel quadrada"), "SQ": ("▭²", "num", "Quadrat"), "POW": ("▭^▭", "num", "Potència"),
    "X": ("x", "num", "Tecla x"), "LOGB": ("log▭▭", "num", "Logaritme en base (amb ⇧: ln)"),
    "EXP": ("×10ˣ", "num", "Potència de 10"), "UP": ("▲", "cur", "Cursor amunt"), "DOWN": ("▼", "cur", "Cursor avall"),
    "LEFT": ("◀", "cur", "Cursor esquerra"), "RIGHT": ("▶", "cur", "Cursor dreta"),
}
KEYS_ES = {
    "CONFIG": "CONFIG (ajustes)", "TOOLS": "TOOLS (herramientas)", "EXE": "EXE (ejecutar)",
    "BACK": "Volver atrás", "DEL": "Borrar", "FRAC": "Fracción", "SQRT": "Raíz cuadrada", "SQ": "Cuadrado",
    "POW": "Potencia", "X": "Tecla x", "LOGB": "Logaritmo en base (con ⇧: ln)", "EXP": "Potencia de 10",
    "UP": "Cursor arriba", "DOWN": "Cursor abajo", "LEFT": "Cursor izquierda", "RIGHT": "Cursor derecha",
}
LABELS = {"va": {"ex": "Exemple", "screen": "Pantalla", "tip": "Consell"},
          "es": {"ex": "Ejemplo", "screen": "Pantalla", "tip": "Consejo"}}
# textos fixos de plantilla.html per a la versió en castellà
TPL_ES = [
    ('<html lang="ca">', '<html lang="es">'),
    ("Com fer amb la Casio ClassWiz fx-991SP CW tot el que s'estudia a la unitat «{{TITLE}}», pas a pas.",
     "Cómo hacer con la Casio ClassWiz fx-991SP CW todo lo que se estudia en la unidad «{{TITLE}}», paso a paso."),
    ("Amb la calculadora · {{UNIT}}", "Con la calculadora · {{UNIT}}"),
    ('aria-label="Apartats"><h3>{{N}} apartats</h3>', 'aria-label="Apartados"><h3>{{N}} apartados</h3>'),
    ("Tecles que apareixen", "Teclas que aparecen"),
    ("<b>Abans de començar</b>", "<b>Antes de empezar</b>"),
    ("Les guies suposen la configuració de fàbrica (entrada i eixida «E Mat/S Mat»). Si la teua calculadora fa coses estranyes:",
     "Las guías suponen la configuración de fábrica (entrada y salida «E Mat/S Mat»). Si tu calculadora hace cosas raras:"),
    ("Els noms dels menús són els de la calculadora en <b>castellà</b>. Si la tens en valencià/català, els trobaràs en el mateix lloc amb un nom molt semblant.",
     "Los nombres de los menús son <b>exactamente</b> los que aparecen en la calculadora configurada en castellano."),
    ("Les tecles amb fons groc <span class=\"k shift\">⇧</span> activen la funció escrita damunt de la tecla següent. El signe negatiu és",
     "Las teclas con fondo amarillo <span class=\"k shift\">⇧</span> activan la función escrita encima de la tecla siguiente. El signo negativo es"),
    ("La calculadora és per <b>comprovar</b> i estalviar càlculs llargs: a l'examen cal escriure el procediment.",
     "La calculadora sirve para <b>comprobar</b> y ahorrar cálculos largos: en el examen hay que escribir el procedimiento."),
]
LEGEND = ["HOME", "CONFIG", "CATALOG", "TOOLS", "FORMAT", "VAR", "FUNC", "SHIFT", "OK", "EXE", "AC",
          "FRAC", "SQRT", "POW", "X", "RIGHT"]


def key(name):
    if name in KEYS:
        t, c, d = KEYS[name]
        if LANG[0] == "es":
            d = KEYS_ES.get(name, d)
        return '<kbd class="k %s" title="%s">%s</kbd>' % (c, d, html.escape(t))
    return '<kbd class="k num">%s</kbd>' % html.escape(name)


def fmt(s):
    # protegeix el LaTeX perquè no es toque
    maths = []
    def keep(m):
        maths.append(m.group(0)); return "\x00%d\x00" % (len(maths) - 1)
    s = re.sub(r"\$[^$]+\$", keep, s)
    s = re.sub(r"\[\[(.+?)\]\]", lambda m: key(m.group(1)), s)
    s = re.sub(r"<<(.+?)>>", lambda m: '<span class="menu">%s</span>' % html.escape(m.group(1)), s)
    s = s.replace(" › ", ' <span class="gt">›</span> ')
    return re.sub(r"\x00(\d+)\x00", lambda m: maths[int(m.group(1))], s)


def screen(s):
    # [[a,b],[c,d]] -> matriu dibuixada
    def mat(m):
        rows = re.findall(r"\[([^\[\]]+)\]", m.group(0))
        return '<span class="mat">' + "".join(
            "<span>" + "".join("<i>%s</i>" % html.escape(c.strip()) for c in r.split(",")) + "</span>" for r in rows) + "</span>"
    s = html.escape(s, quote=False)
    s = re.sub(r"\[\[[^\]]*\](?:,\[[^\]]*\])*\]", mat, s)
    return s.replace(" · ", '<span class="sep">·</span>')


def section(i, sec, L=None):
    L = L or LABELS["va"]
    out = ['<section class="card" id="s%d">' % (i + 1),
           '<h2><span class="n">%d</span>%s</h2>' % (i + 1, fmt(sec["t"]))]
    if sec.get("why"):
        out.append('<p class="why">%s</p>' % fmt(sec["why"]))
    out.append('<ol class="steps">' + "".join("<li>%s</li>" % fmt(st) for st in sec["steps"]) + "</ol>")
    out.append('<div class="example"><div class="ex-h">%s</div><p class="ex-q">%s</p>' % (L["ex"], fmt(sec["ex"])))
    out.append('<div class="ex-keys">%s</div>' % fmt(sec["keys"]))
    out.append('<div class="lcd"><span class="lcd-l">%s</span><span class="lcd-v">%s</span></div></div>' % (L["screen"], screen(sec["screen"])))
    if sec.get("tip"):
        out.append('<p class="tip"><b>💡 %s:</b> %s</p>' % (L["tip"], fmt(sec["tip"])))
    out.append("</section>")
    return "\n".join(out)


def page(g, lang="va"):
    tpl = open(os.path.join(HERE, "plantilla.html"), encoding="utf-8").read()
    keys = KEYS
    if lang == "es":
        for a, b in TPL_ES:
            assert a in tpl, a
            tpl = tpl.replace(a, b)
        keys = dict((k, (v[0], v[1], KEYS_ES.get(k, v[2]))) for k, v in KEYS.items())
    toc = "".join('<li><a href="#s%d">%s</a></li>' % (i + 1, fmt(s["t"])) for i, s in enumerate(g["sections"]))
    legend = "".join('<li>%s<span>%s</span></li>' % (key(k), keys[k][2]) for k in LEGEND)
    body = "\n".join(section(i, s, LABELS[lang]) for i, s in enumerate(g["sections"]))
    rep = {"{{TITLE}}": g["title"], "{{UNIT}}": g["unit"], "{{INTRO}}": fmt(g["intro"]), "{{COLOR}}": g["color"],
           "{{BACK}}": g["back"], "{{BACK_LABEL}}": g["back_label"], "{{TOC}}": toc, "{{LEGEND}}": legend,
           "{{BODY}}": body, "{{N}}": str(len(g["sections"]))}
    for a, b in rep.items():
        tpl = tpl.replace(a, b)
    return tpl



def es_name(f):
    b, e = os.path.splitext(f)
    return b + "-es" + e


# Còpies de guies de CCSS per a 2n Batx MII (mateix contingut, altre enllaç de tornada)
MII = {"materials/2batx-ccss/casio-u1-matrius.html": "materials/2batx-mii/casio-u1-matrius.html",
       "materials/2batx-ccss/casio-u2-sistemes.html": "materials/2batx-mii/casio-u2-sistemes.html"}
MII_LABEL = {"va": "2n Batxillerat MII", "es": "2º Bachillerato MII"}


def pagines(guides, lang):
    for g in guides:
        yield g["file"], g
        if g["file"] in MII:
            yield MII[g["file"]], dict(g, back="../../2batx-mii.html", back_label=MII_LABEL[lang])


# FentMates: el tema comú (logo i colors del bloc) només a les pàgines de calculadora
import runpy as _runpy  # noqa: E402
_tema = _runpy.run_path(os.path.join(ROOT, "_eines", "tema", "aplica.py"))

for lang, guides in (("va", GUIDES), ("es", GUIDES_ES)):
    LANG[0] = lang
    for f, g in pagines(guides, lang):
        if lang == "es":
            f = es_name(f)
        path = os.path.join(ROOT, f)
        open(path, "w", encoding="utf-8").write(page(g, lang))
        _tema["aplica_fitxer"](path)
        print(f, len(g["sections"]), "apartats")
LANG[0] = "va"
