#!/usr/bin/env python3
"""Genera el logo definitiu de FentMates, [∫·Σ]ᵀ, en SVG, PDF i PNG.

Ús:  python3 _eines/logo/genera.py

La marca: una integral suau i una sigma majúscula dins d'una matriu (claudàtors
grocs), amb un punt de producte entre totes dues i la T de matriu transposada.
El nom «FentMates» és Sora Bold convertida en traços (no depén de cap lletra
instal·lada); per extraure'ls fa servir opentype.js dins de Chrome headless, de
manera que cal Chrome i connexió a internet.

Ix a svg/, pdf/ (per a LaTeX) i png/ (fons transparent):
  marca-<color>           només el símbol
  horitzontal-<color>     símbol + nom
  vertical-<color>        símbol damunt del nom
  web-<color>             símbol + nom + fentmates.org
Colors: clar (blau i groc), fosc (per a fons blau), coral i turquesa (els
accents de les fitxes), blau (una sola tinta) i blanc.
A més, marca-<curs> i vertical-<curs> amb l'accent del color de cada curs, el
mateix de la pàgina inicial (LEVELS a assets/js/materials.js), per a les fitxes.
"""
import json
import shutil
import pathlib
import subprocess
import tempfile
import urllib.request

DIR = pathlib.Path(__file__).resolve().parent
WEB = DIR.parent.parent / "assets" / "img" / "logo"     # els que fa servir la web
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OPENTYPE = "https://cdnjs.cloudflare.com/ajax/libs/opentype.js/1.3.4/opentype.min.js"

# tinta, accent i color secundari (per a fentmates.org)
COLORS = {
    "clar":     ("#1b2748", "#e9a919", "#5d6685"),
    "fosc":     ("#e8ecf7", "#ffc94d", "#a1abc8"),
    "coral":    ("#1b2748", "#e8603a", "#5d6685"),
    "turquesa": ("#1b2748", "#1f9e90", "#5d6685"),
    "blau":     ("#1b2748", "#1b2748", "#1b2748"),
    "blanc":    ("#ffffff", "#ffffff", "#ffffff"),
}

# color de cada curs, igual que a assets/js/materials.js
COURSES = {
    "1eso": "#e6b84a", "2eso": "#3b82f6", "3eso": "#ff7a50", "4eso-a": "#a78bfa", "4eso-b": "#6d28d9",
    "1batx-mi": "#9b1c1c", "1batx-ccss": "#ef6b6b", "2batx-mii": "#1e6b47", "2batx-ccss": "#2bb3a3",
}

# ---------- la marca (unitats SVG; claudàtors de y = 12 a 88) ----------
MARK_VB = (10, 4, 148, 88)
INTEGRAL = "M29 78C31 86 38 87 41 77L50 23C53 13 60 13 62 21"
SIGMA = "M116 27V18H76L98 50L76 82H116V73"            # amb remats a les puntes
BRACKETS = "M23 12H14V88H23M123 12H132V88H123"
TRANSPOSE = "M142 7H155M148.5 7V21"
DOT = (65.5, 50, 5.5)


def mark(ink, acc):
    return (f'<g fill="none" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="{INTEGRAL}" stroke="{ink}" stroke-width="8.5"/>'
            f'<path d="{SIGMA}" stroke="{ink}" stroke-width="8.5"/>'
            f'<path d="{BRACKETS}" stroke="{acc}" stroke-width="5"/>'
            f'<path d="{TRANSPOSE}" stroke="{acc}" stroke-width="3.6"/></g>'
            f'<circle cx="{DOT[0]}" cy="{DOT[1]}" r="{DOT[2]}" fill="{acc}"/>')


def svg(inner, vb):
    x, y, w, h = vb
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:g} {y:g} {w:g} {h:g}" '
            f'width="{w:g}" height="{h:g}">{inner}</svg>\n')


# ---------- el nom, en traços ----------
def chrome(*args):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                           "--virtual-time-budget=10000", *args],
                          check=True, capture_output=True, text=True).stdout


def ttf_url(weight):
    css = urllib.request.urlopen(f"https://fonts.googleapis.com/css2?family=Sora:wght@{weight}").read().decode()
    return css.split("url(")[1].split(")")[0]


def glyphs():
    """Traços de «Fent», «Mates» (amb l'interlletratge t–M) i «fentmates.org» a cos 100, línia base 0."""
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp, "g.html")
        page.write_text(f'''<script src="{OPENTYPE}"></script><pre id="o"></pre><script>
const load = u => new Promise((ok, ko) => opentype.load(u, (e, f) => e ? ko(e) : ok(f)));
Promise.all([load("{ttf_url(700)}"), load("{ttf_url(600)}")]).then(([b, s]) => {{
  const S = 100, k = b.getKerningValue(b.charToGlyph("t"), b.charToGlyph("M")) * S / b.unitsPerEm;
  const fent = b.getPath("Fent", 0, 0, S), xm = b.getAdvanceWidth("Fent", S) + k;
  const mates = b.getPath("Mates", xm, 0, S), web = s.getPath("fentmates.org", 0, 0, S);
  const box = p => p.getBoundingBox();
  document.getElementById("o").textContent = JSON.stringify({{
    cap: b.tables.os2.sCapHeight / b.unitsPerEm * S,
    fent: fent.toPathData(2), mates: mates.toPathData(2), word: [box(fent).x1, box(mates).x2],
    web: web.toPathData(2), webbox: [box(web).x1, box(web).x2], webx: s.tables.os2.sxHeight / s.unitsPerEm * S }});
}}).catch(e => document.getElementById("o").textContent = "ERR " + e);
</script>''')
        out = chrome("--dump-dom", page.as_uri())
    data = out.split('<pre id="o">')[1].split("</pre>")[0]
    assert not data.startswith("ERR") and data, f"No s'han pogut llegir les lletres: {data}"
    return json.loads(data)


def word(g, x, baseline, size, ink, acc):
    """«FentMates» amb el costat esquerre de la F a x i la línia base a baseline."""
    k = size / 100
    t = f'transform="translate({x - g["word"][0] * k:.2f} {baseline:g}) scale({k:.4f})"'
    return f'<g {t}><path d="{g["fent"]}" fill="{ink}"/><path d="{g["mates"]}" fill="{acc}"/></g>'


def word_width(g, size):
    return (g["word"][1] - g["word"][0]) * size / 100


def lockups(g, ink, acc, muted):
    mx, my, mw, mh = MARK_VB
    out = {}
    # horitzontal: alçada de majúscula = 36, centrada amb els claudàtors (y = 50)
    size = 36 / g["cap"] * 100
    x0 = mx + mw + 24
    out["horitzontal"] = svg(mark(ink, acc) + word(g, x0, 50 + 18, size, ink, acc),
                             (mx, my, x0 + word_width(g, size) + 2 - mx, mh))
    # web: el nom una mica més amunt i fentmates.org davall
    k = 17 / 100
    web = (f'<g transform="translate({x0 - g["webbox"][0] * k + 1:.2f} 86) scale({k})">'
           f'<path d="{g["web"]}" fill="{muted}"/></g>')
    out["web"] = svg(mark(ink, acc) + word(g, x0, 50 + 8, size, ink, acc) + web,
                     (mx, my, x0 + word_width(g, size) + 2 - mx, mh))
    # vertical: el nom 1,6 vegades més ample que la marca, centrat davall
    size = 1.6 * mw / (g["word"][1] - g["word"][0]) * 100
    cx, cap = mx + mw / 2, g["cap"] * size / 100
    w = word_width(g, size)
    out["vertical"] = svg(mark(ink, acc) + word(g, cx - w / 2, my + mh + 14 + cap, size, ink, acc),
                          (cx - w / 2 - 2, my, w + 4, mh + 14 + cap + 12))
    return out


# ---------- PDF i PNG ----------
def render(name, text, scale):
    w, h = (float(v) for v in text.split('viewBox="')[1].split('"')[0].split()[2:])
    body = text.replace(f'width="{w:g}" height="{h:g}"', 'width="100%" height="100%"', 1)
    css = "html,body{margin:0;height:100%;background:transparent}svg{display:block}"
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp, "p.html")
        page.write_text(f"<!doctype html><style>@page{{size:{w:g}pt {h:g}pt;margin:0}}{css}</style>{body}")
        chrome("--no-pdf-header-footer", f"--print-to-pdf={DIR / 'pdf' / (name + '.pdf')}", page.as_uri())
        page.write_text(f"<!doctype html><style>{css}</style>{body}")
        chrome("--default-background-color=00000000", f"--window-size={round(w * scale)},{round(h * scale)}",
               f"--screenshot={DIR / 'png' / (name + '.png')}", page.as_uri())


def main():
    for d in ("svg", "pdf", "png"):
        (DIR / d).mkdir(exist_ok=True)
    g = glyphs()
    files = {}
    for color, (ink, acc, muted) in COLORS.items():
        files.update({f"marca-{color}": svg(mark(ink, acc), MARK_VB),
                      **{f"{k}-{color}": v for k, v in lockups(g, ink, acc, muted).items()}})
    for course, acc in COURSES.items():
        files.update({f"marca-{course}": svg(mark("#1b2748", acc), MARK_VB),
                      f"vertical-{course}": lockups(g, "#1b2748", acc, "#5d6685")["vertical"]})
    for name, text in files.items():
        (DIR / "svg" / f"{name}.svg").write_text(text)
        render(name, text, 1200 / float(text.split('width="')[1].split('"')[0]))
        print("✓", name)
    WEB.mkdir(exist_ok=True)
    for name in ("horitzontal-fosc", "marca-blanc"):
        shutil.copy(DIR / "svg" / f"{name}.svg", WEB)


if __name__ == "__main__":
    main()
