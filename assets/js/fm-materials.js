/* ==========================================================
   Tema comú de les pàgines de materials (apunts, calculadora,
   exercicis PAU, exàmens…).
   - Detecta el bloc de la unitat a partir del nom del fitxer.
   - Posa el color del bloc al banner dels apunts i als números
     i títols de les seccions (vegeu fm-materials.css).
   - Canvia el logo de dalt: «Fent» + «Mates» en groc i un
     adhesiu del banner de l'inici amb el color del bloc.
   Les pàgines l'enllacen amb _eines/tema/aplica.py.
   ========================================================== */
(function () {
  "use strict";
  var BLOCKS = {
    ari: { c: "#e6b84a", c2: "#c99a2e", icon: "sum" },
    alg: { c: "#4e81bd", c2: "#3d6aa0", icon: "calc" },
    pl:  { c: "#f79645", c2: "#dc7a29", icon: "pi" },
    geo: { c: "#f79645", c2: "#dc7a29", icon: "compass" },
    an:  { c: "#7fa040", c2: "#6a8a33", icon: "graph" },
    pr:  { c: "#8064a1", c2: "#684e88", icon: "dice" },
    all: { c: "#e3a21a", c2: "#c98a0c", icon: "bulb" }
  };
  var ICON = {
    pi: '<text x="0" y="14" text-anchor="middle" font-family="Georgia,serif" font-style="italic" font-size="44" stroke="none" fill="#fff">π</text>',
    sum: '<text x="0" y="14" text-anchor="middle" font-family="Georgia,serif" font-size="44" stroke="none" fill="#fff">∑</text>',
    bulb: '<path d="M-14 6 A20 20 0 1 1 14 6 Q8 12 8 20 H-8 Q-8 12 -14 6 Z"/><path d="M-7 26 H7 M-5 32 H5"/>',
    compass: '<circle cx="0" cy="-30" r="5"/><path d="M-3 -26 L-20 30 M3 -26 L20 30 M-14 10 L14 10"/>',
    dice: '<rect x="-22" y="-22" width="44" height="44" rx="9"/><path d="M-10 -10h0M10 10h0M0 0h0M10 -10h0M-10 10h0" stroke-width="6"/>',
    calc: '<rect x="-22" y="-32" width="44" height="64" rx="7"/><rect x="-14" y="-24" width="28" height="12" rx="2"/><path d="M-10 -2h0M0 -2h0M10 -2h0M-10 8h0M0 8h0M10 8h0M-10 18h0M0 18h0M10 18h0" stroke-width="5"/>',
    graph: '<path d="M-36 24 H36 M-28 32 V-32"/><path d="M-34 18 C-14 18 -10 -24 6 -24 S24 10 36 -6"/>'
  };

  // bloc de cada pàgina segons la carpeta i el nom del fitxer
  function blockOf(path) {
    var m = path.match(/materials\/([^/]+)\/([^/?#]+)/);
    if (!m) return "all";
    var course = m[1], file = m[2];
    if (/resum-teoric/.test(file)) return "all";
    var n = (file.match(/(?:^t|-u)(\d+)/) || [])[1];
    n = n ? +n : 0;
    if (course === "1eso") return "ari";
    if (course === "3eso") return n >= 4 ? "alg" : "ari";
    if (course === "2batx-ccss") return n === 3 ? "pl" : n >= 4 && n <= 5 ? "an" : "alg";
    if (/^2batx/.test(course)) return "alg";
    return "all";
  }

  var key = blockOf(location.pathname);
  var b = BLOCKS[key] || BLOCKS.all;
  var root = document.documentElement;
  root.setAttribute("data-fm-block", key);
  root.style.setProperty("--fm-c", b.c);
  root.style.setProperty("--fm-c2", b.c2);
  // les pàgines de calculadora i PAU usen --c com a color principal
  if (/\/(casio|pau)-/.test(location.pathname)) root.style.setProperty("--c", b.c);
  if (/resum-teoric/.test(location.pathname)) root.setAttribute("data-fm-resum", "");
  var kind = (location.pathname.match(/\/(casio|pau)-/) || [])[1] || "notes";
  root.setAttribute("data-fm-kind", kind);

  function logo() {
    return '<svg class="fm-logo" viewBox="-62 -62 124 124" aria-hidden="true"><rect x="-62" y="-62" width="124" height="124" rx="30" fill="' + b.c + '"/>' +
      '<g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" transform="scale(1.15)">' + ICON[b.icon] + "</g></svg>";
  }
  function brand() {
    document.querySelectorAll("a.brand").forEach(function (a) {
      if (a.dataset.fm) return;
      a.dataset.fm = "1";
      a.innerHTML = logo() + '<span class="fm-name">Fent<b>Mates</b></span>';
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", brand);
  else brand();
})();
