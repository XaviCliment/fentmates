#!/usr/bin/env python3
"""Prova de canvis sobre el logo «FM!» → prova/index.html (comparació pas a pas).

Ús:  python3 _eines/logo/prova/prova.py

Canvis respecte de genera.py:
  1. la paràbola baixa més (mateixa amplada): el vèrtex queda a l'altura de
     l'espai entre el pal dret de la M i el punt;
  2. la F s'aparta de la M (pal més a l'esquerra) i el braç travessa la branca
     esquerra de la paràbola fins a l'eix de simetria (x = vèrtex);
  3. tot en el blau de «Fent», i el braç i el punt en el groc de «Mates».
Quan es decidisca, la versió triada passa a genera.py.
"""
import pathlib
from fractions import Fraction

DIR = pathlib.Path(__file__).resolve().parent
NAVY, GOLD, YELLOW, LIGHT = "#1b2748", "#e9a919", "#ffc94d", "#e8ecf7"
CORAL, PINK, LILAC, TEAL = "#ff7a50", "#ff8fb1", "#8b7cf6", "#2bb3a3"
U, VX, TOP, BASE = 4, 64, 16, 84           # unitat, eix, línia de dalt i base (SVG)
STROKE = 3 * U


def design(depth, stem, arm, arm_over, colors):
    """depth: fondària de la paràbola en unitats; stem: x del pal de la F; arm: (x inicial, x final) del braç.
    Tot en unitats, amb l'origen a l'eix de la paràbola."""
    vy = TOP + U * depth
    sx = VX + U * stem
    cy = 2 * vy - TOP                       # punt de control: el punt mitjà de la Bézier és el vèrtex
    assert (TOP + 2 * cy + TOP) / 4 == vy
    return dict(
        depth=depth, vy=vy, sx=sx, colors=colors, arm_over=arm_over, ax=[VX + U * x for x in arm],
        left=min(sx, VX + U * arm[0]) - 6 - 4,
        f_path=f"M{sx} {BASE}V{TOP + 12}A12 12 0 0 1 {sx + 12} {TOP}H40",
        m_path=f"M40 {TOP}Q{VX} {cy} 88 {TOP}V64",
        arm=f"M{VX + U * arm[0]} 48H{VX + U * arm[1]}",
    )


def mark(d, theme="light"):
    ink, acc, *f_ink = d["colors"][theme]
    s = ""
    if ink == "grad":
        s += (f'<defs><linearGradient id="g{id(d)}" gradientUnits="userSpaceOnUse" x1="{d["sx"]}" y1="{BASE}" '
              f'x2="88" y2="{TOP}"><stop offset="0" stop-color="{CORAL}"/><stop offset=".55" stop-color="{PINK}"/>'
              f'<stop offset="1" stop-color="{LILAC}"/></linearGradient></defs>')
        ink = f"url(#g{id(d)})"
    arm = f'<path d="{d["arm"]}" stroke="{acc[0]}"/>'
    # la F per sota de la M: a la unió P0 mana el traç de la M
    rib = f'<path d="{d["f_path"]}" stroke="{f_ink[0] if f_ink else ink}"/><path d="{d["m_path"]}" stroke="{ink}"/>'
    s += (f'<g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="{STROKE}">'
          + (rib + arm if d["arm_over"] else arm + rib) + "</g>"
          f'<circle cx="88" cy="{BASE}" r="6" fill="{acc[1]}"/>')
    return s


def svg(d, theme="light", attrs=""):
    x = min(d["left"], 2)
    vb = f"{x} 2 {98 - x} 96"
    return f'<svg viewBox="{vb}" {attrs} xmlns="http://www.w3.org/2000/svg">{mark(d, theme)}</svg>'


GRAD = {"light": ("grad", (YELLOW, TEAL)), "dark": ("grad", (YELLOW, TEAL))}
BLUE = {"light": (NAVY, (GOLD, GOLD)), "dark": (LIGHT, (YELLOW, YELLOW))}
GOLD_F = {"light": (NAVY, (GOLD, GOLD), GOLD), "dark": (LIGHT, (YELLOW, YELLOW), YELLOW)}
STEPS = [
    ("Ara", "La versió actual.", design(9, -11, (-11, -6), False, GRAD)),
    ("1 · Paràbola més llarga", "Mateixa amplada; el vèrtex baixa fins a l’espai entre el pal i el punt.",
     design(14, -11, (-11, -6), False, GRAD)),
    ("2 · F separada i braç llarg", "El pal de la F s’aparta 2 unitats i el braç travessa la paràbola fins a l’eix.",
     design(14, -13, (-13, 0), True, GRAD)),
    ("3 · Blau i groc", "Tot en el blau de «Fent»; el braç i el punt en el groc de «Mates».",
     design(14, -13, (-13, 0), True, BLUE)),
    ("4 · Barra curta per darrere", "La barra ja no talla la paràbola: surt per l’esquerra del pal i passa per darrere de la F.",
     design(14, -13, (-15, -8), False, BLUE)),
    ("5 · F groga, vèrtex més amunt", "Tota la F en groc. El vèrtex puja fins a l’altura on acaba el pal dret de la M.",
     design(12, -13, (-15, -8), False, GOLD_F)),
]
NEW = STEPS[-1][2]


def construction(d):
    """Full de construcció de la versió nova, amb l'origen al vèrtex."""
    vy, a = d["vy"], Fraction(d["depth"], 36)
    x0 = min(d["left"], 2)
    h = d["depth"]
    pts = [((40, TOP), f"P₀(−6, {h})", -6, -4), ((88, TOP), f"P₂(6, {h})", -6, -4),
           ((VX, 2 * vy - TOP), f"C(0, −{h})", 3, 2), ((VX, vy), "V(0, 0)", 3, 7)]
    s = (f'<svg viewBox="{x0 - 2} -4 {112 - x0} {2 * vy - TOP + 10}" xmlns="http://www.w3.org/2000/svg">'
         f'<defs><pattern id="q" x="{VX}" y="{vy}" width="4" height="4" patternUnits="userSpaceOnUse">'
         '<path d="M4 0H0V4" fill="none" stroke="#c9d1e6" stroke-width=".25"/></pattern></defs>'
         f'<rect x="{x0}" y="0" width="{108 - x0}" height="{2 * vy - TOP + 4}" fill="url(#q)"/>'
         f'<g opacity=".3">{mark(d)}</g><g fill="none" stroke-linecap="round">'
         f'<path d="M{x0} {vy}H108M{VX} 0V{2 * vy - TOP + 4}" stroke="{NAVY}" stroke-width=".4" opacity=".5"/>'
         f'<path d="M40 {TOP}L{VX} {2 * vy - TOP}L88 {TOP}" stroke="{LILAC}" stroke-width=".55" stroke-dasharray="1.6 1.4"/>'
         f'<path d="M40 {TOP}Q{VX} {2 * vy - TOP} 88 {TOP}" stroke="{CORAL}" stroke-width=".8"/>'
         f'<path d="M{d["ax"][0]} 48H{d["ax"][1]}" stroke="{GOLD}" stroke-width=".8"/></g>')
    for (x, y), label, dx, dy in pts:
        s += (f'<circle cx="{x}" cy="{y}" r="1.3" fill="{NAVY}"/>'
              f'<text x="{x + dx}" y="{y + dy}" font-size="4" font-family="Inter,sans-serif" fill="{NAVY}">{label}</text>')
    for x, label in zip(d["ax"], ("A", "B")):
        s += (f'<circle cx="{x}" cy="48" r="1.3" fill="{GOLD}"/><text x="{x - 6}" y="44" font-size="4" '
              f'font-family="Inter,sans-serif" fill="#b07f0c">{label}({(x - VX) // U:g}, {(vy - 48) // U:g})</text>')
    s += (          f'<text x="{d["sx"] - 4}" y="{vy + 26}" font-size="6" font-weight="700" font-family="Outfit,sans-serif" '
          f'fill="#e0633b">y = {"" if a.numerator == 1 else a.numerator}x²⁄{a.denominator}</text></svg>')
    return s


def page():
    cards = "".join(
        f'<article class="card{" now" if d is NEW else ""}"><div class="panels"><div class="p light">{svg(d)}</div>'
        f'<div class="p dark">{svg(d, "dark")}</div></div><h3>{t}</h3><p>{desc}</p></article>'
        for t, desc, d in STEPS)
    word = '<span class="word">Fent<b>Mates</b></span>'
    sizes = "".join(f'<figure>{svg(NEW, "light", f"height={h}")}<figcaption>{h}</figcaption></figure>'
                    for h in (64, 32, 20, 16))
    return f"""<!doctype html>
<html lang="ca"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Logo FentMates · prova</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@700;800&display=swap" rel="stylesheet">
<style>
  :root {{ --bg:#f6f7fb; --border:#e1e5f0; --text:#1b2340; --muted:#5d6685; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--text); font:16px/1.55 Inter,system-ui,sans-serif; }}
  .wrap {{ max-width:1100px; margin:0 auto; padding:40px 16px 60px; }}
  h1 {{ font:800 32px/1.1 Outfit,sans-serif; margin:0 0 6px; }}
  h2 {{ font:700 22px/1.2 Outfit,sans-serif; margin:44px 0 14px; }}
  h3 {{ font:700 17px/1.2 Outfit,sans-serif; margin:14px 16px 4px; }}
  p {{ margin:0 0 10px; max-width:70ch; }}
  .muted, .card p {{ color:var(--muted); }}
  .card p {{ font-size:14px; margin:0 16px 16px; }}
  .steps {{ display:grid; gap:16px; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); }}
  .card {{ background:#fff; border:1px solid var(--border); border-radius:18px; overflow:hidden; }}
  .card.now {{ outline:3px solid #e9a919; outline-offset:-1px; }}
  .panels {{ display:grid; grid-template-columns:1fr 1fr; }}
  .p {{ aspect-ratio:1; display:grid; place-items:center; padding:16%; }}
  .p svg {{ width:100%; height:100%; }}
  .light {{ background:#fff; }} .dark {{ background:#172036; }}
  .lock {{ display:grid; gap:16px; grid-template-columns:1fr 1fr; }}
  @media (max-width:760px) {{ .lock {{ grid-template-columns:1fr; }} }}
  .lock > div {{ border:1px solid var(--border); border-radius:16px; display:flex; align-items:center; justify-content:center; gap:14px; padding:34px 20px; min-height:190px; }}
  .lock .v {{ flex-direction:column; gap:8px; }}
  .lock .h svg {{ height:76px; width:auto; }} .lock .v svg {{ height:110px; width:auto; }}
  .word {{ font:800 44px/1 Outfit,sans-serif; letter-spacing:-.01em; color:#1b2748; }}
  .word b {{ color:#e9a919; }}
  .dark .word {{ color:#e8ecf7; }} .dark .word b {{ color:#ffc94d; }}
  .v .word {{ font-size:34px; }}
  .build {{ display:grid; grid-template-columns:minmax(0,1.1fr) minmax(0,1fr); gap:28px; align-items:center;
           background:#fff; border:1px solid var(--border); border-radius:18px; padding:22px; }}
  @media (max-width:760px) {{ .build {{ grid-template-columns:1fr; }} }}
  .build svg {{ width:100%; height:auto; }}
  .build ul {{ margin:0; padding-left:20px; display:grid; gap:8px; }}
  .sizes {{ display:flex; align-items:end; gap:24px; background:#fff; border:1px solid var(--border); border-radius:18px; padding:22px; flex-wrap:wrap; }}
  figure {{ margin:0; text-align:center; }} figcaption {{ font-size:12px; color:var(--muted); }}
</style></head><body><div class="wrap">
<h1>Logo FM! · prova de canvis</h1>
<p class="muted">Els canvis aplicats d’un en un, per veure què aporta cadascun. La targeta amb vora groga és el resultat final.</p>
<h2>Pas a pas</h2>
<div class="steps">{cards}</div>
<h2>Amb el nom</h2>
<div class="lock">
  <div class="h light">{svg(NEW)}{word}</div><div class="h dark">{svg(NEW, "dark")}{word}</div>
  <div class="v light">{svg(NEW)}{word}</div><div class="v dark">{svg(NEW, "dark")}{word}</div>
</div>
<h2>Mides petites</h2>
<div class="sizes">{sizes}</div>
<h2>Construcció</h2>
<div class="build">{construction(NEW)}
<ul>
  <li>La paràbola manté els extrems P₀(−6, 12) i P₂(6, 12), és a dir, la mateixa amplada, i baixa 12 unitats. L’equació torna a ser senzilla: <b>y = x²/3</b>.</li>
  <li>El vèrtex V(0, 0) queda exactament a l’altura on acaba el pal dret de la M.</li>
  <li>El pal de la F és a x = −13. La F sencera (pal, cantó, braç de dalt i barra) és groga, i la M blava, com «Fent» i «Mates» però a la inversa. Ja no hi ha un sol traç de dos colors: el groc acaba a P₀, on comença la M.</li>
  <li>La barra va de A(−15, 4) a B(−8, 4): surt 2 unitats per l’esquerra del pal i s’atura abans de la paràbola.</li>
</ul></div>
</div></body></html>
"""


if __name__ == "__main__":
    (DIR / "index.html").write_text(page())
    print("✓", DIR / "index.html")
