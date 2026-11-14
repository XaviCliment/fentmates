#!/usr/bin/env python3
"""
Versió en castellà de les pàgines d'exercicis PAU (materials/2batx-*/pau-*.html -> pau-*-es.html).

La pàgina en valencià es genera com sempre (build_pau.py, an/build.py, pr/build.py, mii/...). Aquest
script en llig les dades (var EXERCICIS), en tradueix els textos amb un diccionari valencià -> castellà
i escriu la pàgina en castellà al costat, amb la interfície també traduïda.

Diccionari: _eines/pau/castella/<curs>-<pàgina>.json (p. ex. 2batx-ccss-pau-u1-matrius.json) i, si n'hi ha,
els fitxers <curs>-<pàgina>.*.json (trossos), tots fusionats. Cada clau és un tros de text que va entre
dues etiquetes HTML, amb les fórmules canviades per ⟨1⟩, ⟨2⟩... (la traducció ha de dur els mateixos
marcadors, en l'ordre que calga), o bé el contingut d'un \\text{...} de dins d'una fórmula, o bé un
atribut alt/title/aria-label. Les claus que es repeteixen (frases fetes de les solucions) es tradueixen
una sola vegada.

Ús (des de l'arrel del web):
  python3 _eines/pau/castella/tradueix.py materials/2batx-ccss/pau-u1-matrius.html --falten
        -> escriu <nom>.falten.json amb les claus que encara no tenen traducció (valor "")
  python3 _eines/pau/castella/tradueix.py materials/2batx-ccss/pau-u1-matrius.html
        -> escriu materials/2batx-ccss/pau-u1-matrius-es.html (s'atura si falta alguna traducció)
  python3 _eines/pau/castella/tradueix.py --totes        -> totes les pàgines que tenen diccionari

Si canvies una pàgina en valencià i la tornes a generar, torna a passar aquest script: els textos nous
apareixeran a --falten.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

MATH = re.compile(r"\$\$.+?\$\$|\$[^$]+?\$", re.S)
TAG = re.compile(r"<[^>]*>")
TEXTCMD = re.compile(r"(\\(?:text|mbox|textrm|textbf|textit)\{)((?:[^{}]|\{[^{}]*\})*)(\})")
ATTR = re.compile(r'(\b(?:alt|title|aria-label)=")([^"]*)(")')
LETTERS = re.compile(r"[A-Za-zÀ-ÿ]{2,}|(?<![A-Za-zÀ-ÿ])[ioIO](?![A-Za-zÀ-ÿ])")
PH = re.compile(r"⟨(\d+)⟩")

MONTHS = {"Juny": "Junio", "Juliol": "Julio", "Setembre": "Septiembre", "extra": "extra", "Sense data": "Sin fecha"}


def wanted(t):
    return bool(LETTERS.search(PH.sub("", t)))


def dict_name(page):
    rel = os.path.relpath(os.path.abspath(page), os.path.join(ROOT, "materials"))
    curs, base = rel.split(os.sep)
    return "%s-%s" % (curs, base[:-5])


def load_dict(name):
    d = {}
    files = sorted(glob.glob(os.path.join(HERE, name + ".json")) + glob.glob(os.path.join(HERE, name + ".*.json")))
    for f in files:
        if f.endswith(".falten.json"):
            continue
        for k, v in json.load(open(f, encoding="utf-8")).items():
            if v:
                d[k] = v
    return d


class Tr:
    def __init__(self, d):
        self.d, self.missing, self.order = d, [], {}

    def need(self, k):
        if k not in self.order:
            self.order[k] = len(self.order)
        if k in self.d:
            return self.d[k]
        self.missing.append(k)
        return k

    def ws(self, s, f):
        """conserva els espais del principi i del final"""
        m = re.match(r"^(\s*)(.*?)(\s*)$", s, re.S)
        if not m.group(2) or not wanted(m.group(2)):
            return s
        return m.group(1) + f(m.group(2)) + m.group(3)

    def math(self, m):
        return TEXTCMD.sub(lambda t: t.group(1) + self.ws(t.group(2), self.need) + t.group(3), m)

    def tag(self, t):
        return ATTR.sub(lambda a: a.group(1) + self.ws(a.group(2), self.need) + a.group(3), t)

    def html(self, s):
        if not s:
            return s
        maths = []

        def keep(m):
            maths.append(self.math(m.group(0)))
            return "\x01%d\x02" % (len(maths) - 1)
        s = MATH.sub(keep, s)
        out, pos = [], 0
        for m in TAG.finditer(s):
            out.append(self.run(s[pos:m.start()], maths))
            out.append(self.tag(m.group(0)))
            pos = m.end()
        out.append(self.run(s[pos:], maths))
        return "".join(out)

    def run(self, t, maths):
        ids = [int(i) for i in re.findall(r"\x01(\d+)\x02", t)]
        local = {}
        key = re.sub(r"\x01(\d+)\x02", lambda m: "⟨%d⟩" % local.setdefault(int(m.group(1)), len(local) + 1), t)
        back = {v: k for k, v in local.items()}

        def f(k):
            es = self.need(k)
            got = sorted(int(i) for i in PH.findall(es))
            if got != sorted(local.values()):
                raise SystemExit("Marcadors diferents a la traducció de:\n  %r\n  %r" % (k, es))
            return es
        res = self.ws(key, f)
        return PH.sub(lambda m: maths[back[int(m.group(1))]], res) if ids else res


def conv(c):
    for a, b in MONTHS.items():
        c = c.replace(a, b)
    return c


# interfície de la pàgina (fora de les dades)
UI = [
    ('<html lang="ca">', '<html lang="es">'),
    ("Exercicis de les proves PAU de la Comunitat Valenciana: ", "Ejercicios de las pruebas PAU de la Comunidad Valenciana: "),
    ("(Matemàtiques Aplicades a les CCSS II)", "(Matemáticas Aplicadas a las CCSS II)"),
    ("(Matemàtiques II)", "(Matemáticas II)"),
    ("<span>2n Batxillerat CCSS</span>", "<span>2º Bachillerato CCSS</span>"),
    ("<span>2n Batxillerat MII</span>", "<span>2º Bachillerato MII</span>"),
    ("Exercicis tipus PAU · Unitat ", "Ejercicios tipo PAU · Unidad "),
    (" exercicis de les proves d'accés a la universitat de la Comunitat Valenciana (", " ejercicios de las pruebas de acceso a la universidad de la Comunidad Valenciana ("),
    ("), ordenats per convocatòria, tots amb la resolució pas a pas.", "), ordenados por convocatoria, todos con la resolución paso a paso."),
    ("), ordenats per convocatòria.", "), ordenados por convocatoria."),
    ('placeholder="Cerca una paraula o un any (p. ex. 2019)" aria-label="Cerca exercicis"', 'placeholder="Busca una palabra o un año (p. ej. 2019)" aria-label="Buscar ejercicios"'),
    ('aria-label="Període"', 'aria-label="Periodo"'),
    ("🖨 Imprimeix", "🖨 Imprimir"),
    ("Enunciats de les proves PAU del Sistema Universitari Valencià. Recopilació per a l'alumnat de FentMates.",
     "Enunciados de las pruebas PAU del Sistema Universitario Valenciano. Recopilación para el alumnado de FentMates."),
    ('alt="Sistema Universitari Valencià"', 'alt="Sistema Universitario Valenciano"'),
    ('["tots", "Tots", 0, 9999]', '["tots", "Todos", 0, 9999]'),
    ('"↓ Més recents primer" : "↑ Més antics primer"', '"↓ Más recientes primero" : "↑ Más antiguos primero"'),
    ('"Fets: " + n + " de "', '"Hechos: " + n + " de "'),
    ("✓ Amb solució", "✓ Con solución"),
    ('"> Fet</label>', '"> Hecho</label>'),
    ('<span class="show">Mostra la solució</span><span class="hide">Amaga la solució</span>', '<span class="show">Mostrar la solución</span><span class="hide">Ocultar la solución</span>'),
    ("No hi ha cap exercici amb aquest filtre.", "No hay ningún ejercicio con este filtro."),
]
OPTIONAL = {"), ordenats per convocatòria, tots amb la resolució pas a pas.", "), ordenats per convocatòria.", "(Matemàtiques Aplicades a les CCSS II)", "(Matemàtiques II)", "<span>2n Batxillerat CCSS</span>", "<span>2n Batxillerat MII</span>"}


def translate(page, only_missing=False):
    name = dict_name(page)
    s = open(page, encoding="utf-8").read()
    i = s.index("var EXERCICIS = ") + len("var EXERCICIS = ")
    j = s.index("</script>", i)
    raw = s[i:j].rstrip().rstrip(";")
    data = json.loads(raw)
    tr = Tr(load_dict(name))
    # nom de la unitat (títol, h1 i descripció)
    unit = re.search(r"<h1>(.*?)</h1>", s).group(1)
    unit_es = tr.need(unit)
    for e in data:
        e["conv"] = conv(e["conv"])
        e["h"] = tr.html(e["h"])
        if e.get("s"):
            e["s"] = tr.html(e["s"])
    if only_missing or tr.missing:
        miss = list(dict.fromkeys(tr.missing))
        path = os.path.join(HERE, name + ".falten.json")
        if miss:
            json.dump({k: "" for k in miss}, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
        elif os.path.exists(path):
            os.remove(path)
        print("%s: %d claus, %d sense traduir%s" % (name, len(tr.order), len(miss), " -> " + os.path.relpath(path, ROOT) if miss else ""))
        if not only_missing:
            sys.exit(1)
        return
    head, tail = s[:i], s[j:]
    for a, b in UI:
        if a not in head + tail:
            assert a in OPTIONAL, "No trobe a la pàgina: " + a
        head, tail = head.replace(a, b), tail.replace(a, b)
    head = head.replace("<title>PAU · %s · FentMates</title>" % unit, "<title>PAU · %s · FentMates</title>" % unit_es)
    head = head.replace("Comunidad Valenciana: %s (" % unit, "Comunidad Valenciana: %s (" % unit_es)
    head = head.replace("<h1>%s</h1>" % unit, "<h1>%s</h1>" % unit_es)
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = head + js + ";\n" + tail
    left = [w for w in ("Unitat", "exercicis", "Cerca", "solució", "Tots", "Fets", "Imprimeix", "Batxillerat") if re.search(r"\b%s\b" % w, re.sub(r"/\*.*?\*/", "", head + tail, flags=re.S))]
    assert not left, "Queden textos en valencià a la interfície: %s" % left
    dst = page[:-5] + "-es.html"
    open(dst, "w", encoding="utf-8").write(out)
    print("%s -> %s (%d exercicis, %d claus)" % (os.path.relpath(page, ROOT), os.path.relpath(dst, ROOT), len(data), len(tr.order)))


if __name__ == "__main__":
    args = sys.argv[1:]
    if args == ["--totes"]:
        pages = sorted(p for p in glob.glob(os.path.join(ROOT, "materials", "2batx-*", "pau-*.html")) if not p.endswith("-es.html"))
        for p in pages:
            if os.path.exists(os.path.join(HERE, dict_name(p) + ".json")):
                translate(p)
    else:
        falten = "--falten" in args
        for p in [a for a in args if not a.startswith("--")]:
            translate(os.path.join(ROOT, p) if not os.path.isabs(p) else p, falten)
