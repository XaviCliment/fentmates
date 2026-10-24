#!/usr/bin/env python3
"""Genera el logo de FentMates («Cinta FM!») en SVG, PDF i PNG.

Ús:  python3 _eines/logo/genera.py

Tota la geometria surt de la paràbola y = x²/4 dibuixada sobre una quadrícula
d'unitat U = 4 (unitats SVG), amb l'origen al vèrtex V = (64, 52):
  · la V de la M és l'arc de paràbola entre P0(-6, 9) i P2(6, 9)
    (Bézier quadràtica amb punt de control C(0, -9));
  · el braç groc de la F passa pel focus F(0, 1) de la paràbola;
  · la M acaba en «!»: M! (factorial).
Els PDF (per a LaTeX) i els PNG es fan amb Chrome headless, que incrusta la
lletra Outfit; els SVG amb text la demanen a Google Fonts i, si no la troben,
fan servir una lletra semblant.
"""
import json
import pathlib
import subprocess
import tempfile

DIR = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = "https://fonts.googleapis.com/css2?family=Outfit:wght@800&display=swap"

NAVY, WHITE, GOLD = "#1b2748", "#ffffff", "#e9a919"
CORAL, PINK, LILAC, YELLOW, TEAL = "#ff7a50", "#ff8fb1", "#8b7cf6", "#ffc94d", "#2bb3a3"

U, VX, VY = 4, 64, 52                      # unitat de quadrícula i vèrtex


def P(x, y):
    """Punt en coordenades matemàtiques (origen al vèrtex, y cap amunt) → SVG."""
    return VX + U * x, VY - U * y


def fmt(*pts):
    return " ".join(f"{a:g} {b:g}" for a, b in pts)


STROKE = 3 * U
R = 3 * U                                   # radi del cantó de la F
STEM_X, TOP_Y, BASE_Y = -11, 9, -8
P0, C, P2 = P(-6, 9), P(0, -9), P(6, 9)
FOCUS = P(0, 1)
RIBBON = (f"M{fmt(P(STEM_X, BASE_Y))}V{P(0, TOP_Y - 3)[1]:g}"
          f"A{R} {R} 0 0 1 {fmt(P(STEM_X + 3, TOP_Y))}H{P0[0]:g}"
          f"Q{fmt(C, P2)}V{P(0, -3)[1]:g}")
ARM = f"M{fmt(P(STEM_X, 1))}H{P(-6, 0)[0]:g}"
DOT = (*P(6, BASE_Y), 1.5 * U)
VIEWBOX = (6, 2, 96, 96)

assert P0 == (40, 16) and P2 == (88, 16) and FOCUS == (64, 48)
# la Bézier quadràtica passa pel vèrtex: punt mitjà = (P0 + 2C + P2) / 4
assert ((P0[1] + 2 * C[1] + P2[1]) / 4, (P0[0] + 2 * C[0] + P2[0]) / 4) == (VY, VX)

GRAD = (f'<linearGradient id="fm-cinta" gradientUnits="userSpaceOnUse" '
        f'x1="{P(STEM_X, BASE_Y)[0]:g}" y1="{P(0, BASE_Y)[1]:g}" x2="{P2[0]:g}" y2="{P2[1]:g}">'
        f'<stop offset="0" stop-color="{CORAL}"/><stop offset=".55" stop-color="{PINK}"/>'
        f'<stop offset="1" stop-color="{LILAC}"/></linearGradient>')


def mark(mono=None, focus=False):
    """Marca sola (sense <svg>). mono: color únic, o None per a la versió en color."""
    ribbon, arm, dot = ("url(#fm-cinta)", YELLOW, TEAL) if mono is None else (mono,) * 3
    s = "" if mono else f"<defs>{GRAD}</defs>"
    s += (f'<g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="{STROKE}">'
          f'<path d="{ARM}" stroke="{arm}"/><path d="{RIBBON}" stroke="{ribbon}"/></g>'
          f'<circle cx="{DOT[0]:g}" cy="{DOT[1]:g}" r="{DOT[2]:g}" fill="{dot}"/>')
    if focus:
        s += f'<circle cx="{FOCUS[0]:g}" cy="{FOCUS[1]:g}" r="3.4" fill="{mono or TEAL}"/>'
    return s


def svg(inner, vb, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{fmt(vb[:2], vb[2:])}" '
            f'width="{vb[2]:g}" height="{vb[3]:g}">{extra}{inner}</svg>\n')


def tile():
    """Marca sobre una tessel·la blava arrodonida (favicon, avatar)."""
    x, y, w, h = VIEWBOX
    pad = 14
    return svg(f'<rect x="{x - pad}" y="{y - pad}" width="{w + 2 * pad}" height="{h + 2 * pad}" '
               f'rx="{(w + 2 * pad) * .24:g}" fill="{NAVY}"/>' + mark(),
               (x - pad, y - pad, w + 2 * pad, h + 2 * pad))


# ---------- paraula «FentMates» ----------
WORD_SIZE = 50
WORD_STYLE = (f'<style>@import url("{FONTS.replace("&", "&amp;")}");'
              '.fm-word{font-family:Outfit,"Avenir Next","Helvetica Neue",Arial,sans-serif;'
              f'font-weight:800;font-size:{WORD_SIZE}px;letter-spacing:-.5px}}</style>')


def chrome(*args):
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--virtual-time-budget=6000", *args],
                   check=True, capture_output=True, text=True)


def measure_word():
    """Amplada i caixa de la paraula amb Outfit, mesurades a Chrome."""
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp, "mesura.html")
        page.write_text(
            f'<link href="{FONTS}" rel="stylesheet"><body>'
            f'<svg width="600" height="200">{WORD_STYLE}<text id="t" class="fm-word" x="0" y="100">'
            'Fent<tspan>Mates</tspan></text></svg><pre id="o"></pre><script>'
            'document.fonts.load("800 50px Outfit").then(()=>{const b=document.getElementById("t").getBBox();'
            'const ok=document.fonts.check("800 50px Outfit");'
            'document.getElementById("o").textContent=JSON.stringify({x:b.x,y:b.y,w:b.width,h:b.height,ok})})'
            '</script>')
        out = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=6000",
                              "--dump-dom", page.as_uri()], check=True, capture_output=True, text=True).stdout
    data = json.loads(out.split('<pre id="o">')[1].split("</pre>")[0])
    assert data["ok"], "No s'ha pogut carregar Outfit"
    return data


def word(x, baseline, fent, mates, length, anchor="start", size=WORD_SIZE):
    # textLength: si no hi ha Outfit, la lletra de recanvi s'ajusta a la mateixa amplada
    return (f'<text class="fm-word" x="{x:g}" y="{baseline:g}" text-anchor="{anchor}" fill="{fent}" '
            f'textLength="{length:.1f}" lengthAdjust="spacingAndGlyphs" '
            f'font-size="{size:g}" style="font-size:{size:g}px">'
            f'Fent<tspan fill="{mates}">Mates</tspan></text>')


def lockups(m):
    """Horitzontal i vertical, per a fons clar, fosc i en un sol color."""
    vx, vy, vw, vh = VIEWBOX
    asc, desc = 100 - m["y"], m["y"] + m["h"] - 100     # mesurats sobre la línia base
    gap = 16
    out = {}
    themes = {"": (NAVY, GOLD, None), "-fosc": ("#e8ecf7", YELLOW, None), "-negre": (NAVY, NAVY, NAVY)}
    for suf, (fent, mates, mono) in themes.items():
        # horitzontal: la paraula centrada verticalment amb la marca (altura de majúscula ≈ 0,7 em)
        base = vy + vh / 2 + 0.7 * WORD_SIZE / 2
        tx = vx + vw + gap
        out[f"horitzontal{suf}"] = svg(mark(mono) + word(tx, base, fent, mates, m["w"]),
                                       (vx, vy, vw + gap + m["w"] + 4, vh), WORD_STYLE)
        # vertical: marca damunt, paraula a sota centrada i 1,5 vegades més ampla que la marca
        k = 1.5 * vw / m["w"]
        w = 1.5 * vw + 8
        cx = vx + vw / 2
        base = vy + vh + 8 + k * asc
        out[f"vertical{suf}"] = svg(mark(mono) + word(cx, base, fent, mates, k * m["w"], "middle", k * WORD_SIZE),
                                    (cx - w / 2, vy, w, vh + 8 + k * (asc + desc) + 4), WORD_STYLE)
    return out


def render(name, svgtext, scale):
    """Escriu PDF (mida en punts = viewBox) i PNG transparent (viewBox × scale)."""
    vb = [float(v) for v in svgtext.split('viewBox="')[1].split('"')[0].split()]
    w, h = vb[2], vb[3]
    with tempfile.TemporaryDirectory() as tmp:
        page = pathlib.Path(tmp, "p.html")
        body = svgtext.replace(f'width="{w:g}" height="{h:g}"', 'width="100%" height="100%"', 1)
        css = "html,body{margin:0;height:100%;background:transparent}svg{display:block}"
        html = f'<!doctype html><link href="{FONTS}" rel="stylesheet"><style>%s{css}</style>{body}'
        page.write_text(html.replace("%s", f"@page{{size:{w:g}pt {h:g}pt;margin:0}}", 1))
        chrome("--no-pdf-header-footer", f"--print-to-pdf={DIR / 'pdf' / (name + '.pdf')}", page.as_uri())
        page.write_text(html.replace("%s", "", 1))
        chrome("--default-background-color=00000000",
               f"--window-size={round(w * scale)},{round(h * scale)}",
               f"--screenshot={DIR / 'png' / (name + '.png')}", page.as_uri())


def main():
    for d in ("svg", "pdf", "png"):
        (DIR / d).mkdir(exist_ok=True)
    files = {
        "logo": svg(mark(), VIEWBOX),
        "logo-focus": svg(mark(focus=True), VIEWBOX),
        "logo-negre": svg(mark(NAVY), VIEWBOX),
        "logo-blanc": svg(mark(WHITE), VIEWBOX),
        "logo-tessela": tile(),
        **lockups(measure_word()),
    }
    for name, text in files.items():
        (DIR / "svg" / f"{name}.svg").write_text(text)
        render(name, text, 1024 / 96 if name.startswith("logo") else 6)
        print("✓", name)


if __name__ == "__main__":
    main()
