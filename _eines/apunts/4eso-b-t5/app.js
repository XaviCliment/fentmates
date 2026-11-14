(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-4eso-b-u5-done";

  /* ---------- textos de la interfície ---------- */
  var UI = {
    va: { next: "Següent pas", all: "Mostra-ho tot", reset: "Amaga els passos", step: "Pas", of: "de", studied: "Estudiat", mark: "Marca com a estudiat",
      score: "Encerts", right: "Correcte!", wrong: "No és correcte.", theme: "Canvia entre mode clar i fosc", top: "Torna amunt" },
    es: { next: "Siguiente paso", all: "Mostrarlo todo", reset: "Ocultar los pasos", step: "Paso", of: "de", studied: "Estudiado", mark: "Marcar como estudiado",
      score: "Aciertos", right: "¡Correcto!", wrong: "No es correcto.", theme: "Cambiar entre modo claro y oscuro", top: "Volver arriba" },
    en: { next: "Next step", all: "Show all", reset: "Hide the steps", step: "Step", of: "of", studied: "Studied", mark: "Mark as studied",
      score: "Correct", right: "Correct!", wrong: "Not quite.", theme: "Switch between light and dark mode", top: "Back to top" }
  };
  var lang = root.getAttribute("data-lang") || "va";
  function u(k) { return (UI[lang] || UI.va)[k]; }
  function t3(va, es, en) { return lang === "es" ? es : lang === "en" ? en : va; }
  var refreshers = [];
  function onLang(fn) { refreshers.push(fn); fn(); }

  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function tex(s, display) { try { return window.katex.renderToString(s, { throwOnError: false, displayMode: !!display }); } catch (e) { return s; } }
  function $(w, r) { return w.querySelector('[data-role="' + r + '"]'); }
  function byId(id) { return document.getElementById(id); }
  function presetBtns(box, labels, onPick, first) {
    var bs = [];
    labels().forEach(function (_, i) {
      var b = document.createElement("button"); b.type = "button"; b.className = "btn";
      b.addEventListener("click", function () { bs.forEach(function (x) { x.classList.remove("on"); }); b.classList.add("on"); onPick(i); });
      box.appendChild(b); bs.push(b);
    });
    if (first != null && bs[first]) bs[first].classList.add("on");
    onLang(function () { var L = labels(); bs.forEach(function (b, i) { b.innerHTML = L[i]; }); });
    return bs;
  }
  function kv(rows) { return '<div class="kv">' + rows.map(function (r) { return "<span>" + r[0] + "</span><span>" + r[1] + "</span>"; }).join("") + "</div>"; }
  function rt(s) { return s.replace(/\$([^$]+)\$/g, function (_, m) { return tex(m); }); }
  function small(s) { return "<br><small>" + s + "</small>"; }
  var COL = { cos: "#3b82f6", sin: "#f97316", tan: "#16a34a", ang: "#7c3aed", r: "#e11d48" };
  function cdot(c) { return '<i class="tag-c" style="background:' + c + '"></i>'; }

  /* ---------- nombres ---------- */
  function gcd(a, b) { a = Math.abs(a); b = Math.abs(b); while (b) { var t = a % b; a = b; b = t; } return a; }
  function lcm(a, b) { return a / gcd(a, b) * b; }
  function decS(x, k) { var s = String(+x.toFixed(k == null ? 2 : k)); if (s === "-0") s = "0"; return lang === "en" ? s : s.replace(".", ","); }
  function dT(x, k) { return decS(x, k).replace(",", "{,}"); }
  function apx(x, k) { var e = Math.abs(x - +x.toFixed(k == null ? 4 : k)) > 1e-10; return (e ? "\\approx " : "=") + dT(x, k == null ? 4 : k); }
  function Fr(n, d) { if (d === undefined) d = 1; if (d < 0) { n = -n; d = -d; } var g = gcd(n, d) || 1; return { n: n / g, d: d / g }; }
  function F(x) { return typeof x === "number" ? Fr(x) : x; }
  function fAdd(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d + b.n * a.d, a.d * b.d); }
  function fSub(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d - b.n * a.d, a.d * b.d); }
  function fMul(a, b) { a = F(a); b = F(b); return Fr(a.n * b.n, a.d * b.d); }
  function fDiv(a, b) { a = F(a); b = F(b); return Fr(a.n * b.d, a.d * b.n); }
  function fVal(a) { a = F(a); return a.n / a.d; }
  function fT(f) { f = F(f); return f.d === 1 ? String(f.n) : (f.n < 0 ? "-" : "") + "\\frac{" + Math.abs(f.n) + "}{" + f.d + "}"; }
  function surd(n) { var a = 1, b = n, i; for (i = 2; i * i <= b; i++) while (b % (i * i) === 0) { b /= i * i; a *= i; } return { a: a, b: b }; }
  function rad(d) { return d * Math.PI / 180; }
  function deg(r) { return r * 180 / Math.PI; }
  function norm360(a) { a = a % 360; if (a < 0) a += 360; if (Math.abs(a - 360) < 1e-9 || Math.abs(a) < 1e-9) a = 0; return a; }
  function dmsT(x) {
    var sg = x < 0 ? "-" : "", s = Math.round(Math.abs(x) * 3600), d = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), q = s % 60;
    return sg + d + "^\\circ" + (m || q ? m + "'" : "") + (q ? q + "''" : "");
  }
  function angT(x) { return Math.abs(x - Math.round(x)) < 1e-9 ? Math.round(x) + "^\\circ" : (Math.abs(x * 60 - Math.round(x * 60)) < 1e-6 ? "" : "\\approx ") + dmsT(x); }
  // a·π (a fracció) -> \frac{3\pi}{4}
  function piT(f) {
    f = F(f); if (f.n === 0) return "0";
    var top = (Math.abs(f.n) === 1 ? "" : Math.abs(f.n)) + "\\pi";
    return (f.n < 0 ? "-" : "") + (f.d === 1 ? top : "\\frac{" + top + "}{" + f.d + "}");
  }
  function degPi(x) { // graus -> fracció de π si és senzilla
    var n = Math.round(x * 3600); if (Math.abs(n - x * 3600) > 1e-6) return null;
    var f = Fr(n, 180 * 3600); return f.d <= 720 ? f : null;
  }
  function parseNum(s) { s = String(s).trim().replace(",", "."); if (!s || !/^[+-]?(\d+\.?\d*|\.\d+)$/.test(s)) return null; return +s; }
  // "36 38" o "36°38'12''" o "-12.5" -> graus
  function parseAng(s) {
    s = String(s).trim().replace(/,/g, ".").replace(/[°º'’"″′]/g, " ").trim(); if (!s) return null;
    var neg = /^-/.test(s); s = s.replace(/^[+-]/, "").trim();
    var p = s.split(/\s+/); if (p.length > 3 || p.some(function (x) { return !/^\d+\.?\d*$|^\.\d+$/.test(x); })) return null;
    var v = +p[0] + (p[1] ? +p[1] / 60 : 0) + (p[2] ? +p[2] / 3600 : 0);
    return neg ? -v : v;
  }

  /* ---------- nombres de la forma r·√m (r racional) ---------- */
  function S(r, m) { r = F(r); if (r.n === 0) return { r: Fr(0), m: 1 }; var s = surd(m); return { r: fMul(r, s.a), m: s.b }; }
  function sMul(x, y) { return S(fMul(x.r, y.r), x.m * y.m); }
  function sInv(x) { return S(fDiv(1, fMul(x.r, x.m)), x.m); }
  function sDiv(x, y) { return sMul(x, sInv(y)); }
  function sSq(x) { return fMul(fMul(x.r, x.r), x.m); }
  function sSqrt(q) { q = F(q); return S(Fr(1, q.d), q.n * q.d); }
  function sNeg(x) { return S(fMul(x.r, -1), x.m); }
  function sVal(x) { return fVal(x.r) * Math.sqrt(x.m); }
  function sT(x) {
    if (x.m === 1) return fT(x.r);
    var n = Math.abs(x.r.n), d = x.r.d, top = (n === 1 ? "" : n) + "\\sqrt{" + x.m + "}";
    return (x.r.n < 0 ? "-" : "") + (d === 1 ? top : "\\frac{" + top + "}{" + d + "}");
  }
  // "-3/5", "sqrt5/3", "2√3", "0.62" -> { v, ex (r·√m o null) }
  function parseVal(s) {
    s = String(s).trim().replace(/\s+/g, "").replace(/√/g, "sqrt").replace(/,/g, ".");
    if (!s) return null;
    if (/^[+-]?(\d+\.\d*|\.\d+)$/.test(s)) return { v: +s, ex: null };
    var m = s.match(/^([+-]?)(\d*)\*?(?:sqrt\(?(\d+)\)?)?(?:\/(\d+))?$/);
    if (!m || (!m[2] && !m[3])) return null;
    var a = m[2] ? +m[2] : 1, root = m[3] ? +m[3] : 1, d = m[4] ? +m[4] : 1;
    if (!d) return null;
    var ex = S(Fr((m[1] === "-" ? -1 : 1) * a, d), root);
    return { v: sVal(ex), ex: ex };
  }

  /* ---------- nombres de Q(√2,√3): [a, b, c, d] = a + b√2 + c√3 + d√6 ---------- */
  function Q(a, b, c, d) { return [F(a || 0), F(b || 0), F(c || 0), F(d || 0)]; }
  function qAdd(x, y) { return x.map(function (v, i) { return fAdd(v, y[i]); }); }
  function qNeg(x) { return x.map(function (v) { return fMul(v, -1); }); }
  function qSub(x, y) { return qAdd(x, qNeg(y)); }
  function qMul(x, y) {
    var a = x[0], b = x[1], c = x[2], d = x[3], e = y[0], f = y[1], g = y[2], h = y[3];
    function s() { var r = Fr(0); for (var i = 0; i < arguments.length; i += 3) r = fAdd(r, fMul(arguments[i + 2], fMul(arguments[i], arguments[i + 1]))); return r; }
    return [s(a, e, 1, b, f, 2, c, g, 3, d, h, 6), s(a, f, 1, b, e, 1, c, h, 3, d, g, 3), s(a, g, 1, c, e, 1, b, h, 2, d, f, 2), s(a, h, 1, d, e, 1, b, g, 1, c, f, 1)];
  }
  function qZero(x) { return x.every(function (v) { return v.n === 0; }); }
  function qInv(y) {
    var c2 = [y[0], fMul(y[1], -1), y[2], fMul(y[3], -1)], p = qMul(y, c2), c3 = [p[0], p[1], fMul(p[2], -1), fMul(p[3], -1)], q = qMul(p, c3)[0];
    return qMul(qMul(c2, c3), Q(fDiv(1, q)));
  }
  function qDiv(x, y) { return qMul(x, qInv(y)); }
  function qVal(x) { return fVal(x[0]) + fVal(x[1]) * Math.SQRT2 + fVal(x[2]) * Math.sqrt(3) + fVal(x[3]) * Math.sqrt(6); }
  function qT(x) {
    var L = x.reduce(function (m, v) { return lcm(m, v.d); }, 1), nums = x.map(function (v) { return v.n * (L / v.d); });
    var R = ["", "\\sqrt2", "\\sqrt3", "\\sqrt6"], terms = [];
    [0, 3, 2, 1].forEach(function (i) { if (nums[i]) terms.push([nums[i], R[i]]); }); // 1, √6, √3, √2
    if (!terms.length) return "0";
    var neg = L > 1 && terms.every(function (t) { return t[0] < 0; }), str = "";
    if (!neg) terms = terms.filter(function (t) { return t[0] > 0; }).concat(terms.filter(function (t) { return t[0] < 0; }));
    terms.forEach(function (t, i) {
      var c = neg ? -t[0] : t[0], a = Math.abs(c), body = t[1] ? (a === 1 ? "" : a) + t[1] : String(a);
      str += (c < 0 ? "-" : i ? "+" : "") + body;
    });
    return (neg ? "-" : "") + (L === 1 ? str : "\\frac{" + str + "}{" + L + "}");
  }
  // sinus i cosinus exactes dels múltiples de 15°
  var SIN15 = [Q(0), Q(0, Fr(-1, 4), 0, Fr(1, 4)), Q(Fr(1, 2)), Q(0, Fr(1, 2)), Q(0, 0, Fr(1, 2)), Q(0, Fr(1, 4), 0, Fr(1, 4)), Q(1)];
  function k15(d) { var k = Math.round(d / 15); return Math.abs(k * 15 - d) < 1e-9 ? ((k % 24) + 24) % 24 : null; }
  function qSinK(k) { k = ((k % 24) + 24) % 24; return k <= 6 ? SIN15[k] : k <= 12 ? SIN15[12 - k] : k <= 18 ? qNeg(SIN15[k - 12]) : qNeg(SIN15[24 - k]); }
  function qCosK(k) { return qSinK(k + 6); }
  function qTanK(k) { var c = qCosK(k); return qZero(c) ? null : qDiv(qSinK(k), c); }
  function exact(d) { // raons exactes d'un angle en graus (null si no és múltiple de 15°)
    var k = k15(d); if (k == null) return null;
    var s = qSinK(k), c = qCosK(k), t = qTanK(k);
    return { s: s, c: c, t: t, sec: qZero(c) ? null : qInv(c), csc: qZero(s) ? null : qInv(s), cot: qZero(s) ? null : qDiv(c, s) };
  }

  /* ---------- circumferència goniomètrica ---------- */
  function svgPt(svg, e) {
    var m = svg.getScreenCTM(); if (!m) return null;
    var pt = svg.createSVGPoint(); pt.x = e.clientX; pt.y = e.clientY;
    return pt.matrixTransform(m.inverse());
  }
  function f1(x) { return Math.round(x * 10) / 10; }
  function UC(svg, o) {
    o = o || {};
    var W = o.W || 320, H = o.H || W, cx = o.cx || W / 2, cy = o.cy || H / 2, R = o.R || 110;
    var P = { R: R, onDrag: null };
    function X(x) { return cx + x * R; }
    function Y(y) { return cy - y * R; }
    P.X = X; P.Y = Y;
    function L(x1, y1, x2, y2, cls, st) { return '<line x1="' + f1(x1) + '" y1="' + f1(y1) + '" x2="' + f1(x2) + '" y2="' + f1(y2) + '" class="' + cls + '"' + (st ? ' style="' + st + '"' : "") + "/>"; }
    var base = L(cx - R - 22, cy, cx + R + 22, cy, "ax") + L(cx, cy + R + 22, cx, cy - R - 22, "ax") + '<circle class="cir" cx="' + cx + '" cy="' + cy + '" r="' + R + '"/>';
    base += '<text x="' + (X(1) + 4) + '" y="' + (cy + 13) + '">1</text><text x="' + (X(-1) - 14) + '" y="' + (cy + 13) + '">−1</text><text x="' + (cx + 4) + '" y="' + (Y(1) - 4) + '">1</text><text x="' + (cx + 4) + '" y="' + (Y(-1) + 13) + '">−1</text>';
    P.seg = function (x1, y1, x2, y2, col, cls) { return L(X(x1), Y(y1), X(x2), Y(y2), cls || "ln", col ? "stroke:" + col : ""); };
    P.dot = function (x, y, col, drag) {
      var s = drag ? '<circle class="halo" cx="' + f1(X(x)) + '" cy="' + f1(Y(y)) + '" r="18"/>' : "";
      return s + '<circle class="pt' + (drag ? " drag" : "") + '" cx="' + f1(X(x)) + '" cy="' + f1(Y(y)) + '" r="' + (drag ? 7 : 4.5) + '" style="fill:' + col + '"/>';
    };
    P.text = function (x, y, s, dx, dy, col, it) { return '<text class="lb' + (it ? " it" : "") + '" x="' + f1(X(x) + (dx || 0)) + '" y="' + f1(Y(y) + (dy || 0)) + '" text-anchor="middle"' + (col ? ' style="fill:' + col + '"' : "") + ">" + s + "</text>"; };
    // arc de a0 a a1 (graus, pot fer més d'una volta: espiral), radi en píxels
    P.arc = function (a0, a1, r, col, lbl, spiral) {
      var sw = a1 - a0, N = Math.max(2, Math.ceil(Math.abs(sw) / 3)), d = "", i, t, rr;
      if (Math.abs(sw) < 0.5) return "";
      for (i = 0; i <= N; i++) { t = a0 + sw * i / N; rr = r + (spiral ? 9 * Math.abs(t - a0) / 360 : 0); d += (i ? "L" : "M") + f1(cx + rr * Math.cos(rad(t))) + " " + f1(cy - rr * Math.sin(rad(t))); }
      var s = '<path class="arc" style="stroke:' + col + '" d="' + d + '"/>';
      var e = rad(a1), rr2 = r + (spiral ? 9 * Math.abs(sw) / 360 : 0), ux = Math.cos(e), uy = -Math.sin(e), dir = sw > 0 ? 1 : -1, tx = -uy * dir, ty = ux * dir;
      var ex = cx + rr2 * ux, ey = cy + rr2 * uy;
      s += '<path d="M' + f1(ex) + " " + f1(ey) + "L" + f1(ex - tx * 8 + ux * 4) + " " + f1(ey - ty * 8 + uy * 4) + "L" + f1(ex - tx * 8 - ux * 4) + " " + f1(ey - ty * 8 - uy * 4) + 'Z" style="fill:' + col + '"/>';
      if (lbl) { var m = rad(a0 + (Math.abs(sw) > 360 ? sw % 360 : sw) / 2); s += '<text class="lb" x="' + f1(cx + (r + 16) * Math.cos(m)) + '" y="' + f1(cy - (r + 16) * Math.sin(m) + 4) + '" text-anchor="middle" style="fill:' + col + '">' + lbl + "</text>"; }
      return s;
    };
    P.sector = function (a0, a1, col) {
      var sw = Math.max(-359.9, Math.min(359.9, a1 - a0)); if (Math.abs(sw) < 0.5) return "";
      var b = rad(a0 + sw);
      return '<path class="sect" style="fill:' + col + '" d="M' + cx + " " + cy + "L" + f1(X(Math.cos(rad(a0)))) + " " + f1(Y(Math.sin(rad(a0)))) + "A" + R + " " + R + " 0 " + (Math.abs(sw) > 180 ? 1 : 0) + " " + (sw > 0 ? 0 : 1) + " " + f1(X(Math.cos(b))) + " " + f1(Y(Math.sin(b))) + 'Z"/>';
    };
    P.draw = function (h) { svg.innerHTML = base + h; };
    var drag = false;
    function at(e) { var q = svgPt(svg, e); if (!q || !P.onDrag) return; var a = deg(Math.atan2(cy - q.y, q.x - cx)); P.onDrag(a < 0 ? a + 360 : a); }
    svg.addEventListener("pointerdown", function (e) { if (!P.onDrag) return; drag = true; svg.classList.add("dragging"); try { svg.setPointerCapture(e.pointerId); } catch (_) {} at(e); e.preventDefault(); });
    svg.addEventListener("pointermove", function (e) { if (drag) at(e); });
    function up() { drag = false; svg.classList.remove("dragging"); }
    svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
    return P;
  }

  /* ---------- controls de passos per als ginys ---------- */
  function stepper(w, getN, onShow) {
    var shown = 1, nb = $(w, "next"), ab = $(w, "all"), cnt = $(w, "cnt");
    function upd() {
      var n = getN(); if (shown > n) shown = n; if (shown < 0) shown = 0;
      nb.textContent = u("next") + " →"; nb.disabled = shown >= n;
      ab.textContent = shown >= n ? u("reset") : u("all");
      cnt.textContent = n ? u("step") + " " + shown + " " + u("of") + " " + n : "";
      onShow(shown);
    }
    nb.addEventListener("click", function () { shown++; upd(); });
    ab.addEventListener("click", function () { shown = shown >= getN() ? Math.min(1, getN()) : getN(); upd(); });
    onLang(upd);
    return { upd: upd, reset: function (v) { shown = v == null ? 1 : v; upd(); } };
  }

  /* ---------- 5.1 radians ---------- */
  function wRad() {
    var w = byId("w-rad"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), sl = $(w, "a");
    var C = UC(svg, { W: 300, R: 100 });
    C.onDrag = function (d) {
      var cur = +sl.value, k = Math.round((cur - d) / 360), v = Math.round((d + 360 * k) / 5) * 5;
      if (v < 0) v += 360; if (v > 720) v -= 360; sl.value = v; draw();
    };
    function draw() {
      var a = +sl.value, r = rad(a), e = rad(a);
      var h = C.sector(0, Math.min(a, 359.9), COL.ang) + C.arc(0, a, 26, COL.ang, a ? a + "°" : "", a > 360);
      var arcR = '<path class="sg" style="stroke:' + COL.sin + '" d="M' + C.X(1) + " " + C.Y(0);
      for (var i = 1; i <= 60; i++) { var t = rad(Math.min(a, 360) * i / 60); arcR += "L" + f1(C.X(Math.cos(t))) + " " + f1(C.Y(Math.sin(t))); }
      if (a > 0) h += arcR + '"/>';
      h += C.seg(0, 0, 1, 0, "var(--text)") + C.seg(0, 0, Math.cos(e), Math.sin(e), "var(--text)") + C.dot(Math.cos(e), Math.sin(e), COL.ang, true);
      C.draw(h);
      var f = Fr(a, 180);
      info.innerHTML = kv([
        [t3("Graus", "Grados", "Degrees"), tex(a + "^\\circ")],
        [t3("Radians", "Radianes", "Radians"), tex(a + "^\\circ\\cdot\\dfrac{\\pi}{180^\\circ}=" + piT(f) + (a ? "\\ \\text{rad}" + apx(r, 3) : "")) ],
        [t3("Voltes", "Vueltas", "Turns"), tex(fT(Fr(a, 360))) + (a >= 360 ? small(t3("Té el mateix costat que ", "Tiene el mismo lado que ", "Same side as ") + tex(norm360(a) + "^\\circ")) : "")],
        [cdot(COL.sin) + t3("Arc (r = 1)", "Arco (r = 1)", "Arc (r = 1)"), tex("l=\\alpha\\cdot r" + apx(r, 3)) + small(t3("En una circumferència de radi 1, la mesura en radians és la longitud de l'arc.", "En una circunferencia de radio 1, la medida en radianes es la longitud del arco.", "On a circle of radius 1, the radian measure is the arc length."))]
      ]);
    }
    sl.addEventListener("input", draw); onLang(draw);
    var dg = $(w, "dg"), dgo = $(w, "dgo"), rd = $(w, "rd"), rdo = $(w, "rdo");
    function conv() {
      var a = parseAng(dg.value); dg.classList.toggle("bad", a == null);
      if (a == null) dgo.innerHTML = "";
      else { var f = degPi(a); dgo.innerHTML = tex(dmsT(a) + "=" + (f ? piT(f) + "\\ \\text{rad}" + apx(rad(a), 4) : dT(rad(a), 4) + "\\ \\text{rad}")); }
      var s = rd.value.trim().replace(/\s+/g, "").replace(/π/g, "pi").replace(/,/g, "."), m = s.match(/^([+-]?)(\d*\.?\d*)\*?(pi)?(?:\/(\d+\.?\d*))?$/), v = null, ex = null;
      if (m && (m[2] || m[3]) && m[2] !== ".") {
        var c = m[2] ? +m[2] : 1, d = m[4] ? +m[4] : 1, sg = m[1] === "-" ? -1 : 1;
        if (d) { v = sg * c * (m[3] ? Math.PI : 1) / d; if (m[3] && Number.isInteger(c) && Number.isInteger(d)) ex = Fr(sg * c * 180, d); }
      }
      rd.classList.toggle("bad", v == null);
      rdo.innerHTML = v == null ? "" : tex((ex ? "=" + fT(ex) + "^\\circ" + (ex.d > 1 ? apx(fVal(ex), 4) : "") : dT(v, 4) + "\\cdot\\dfrac{180^\\circ}{\\pi}\\approx " + dT(deg(v), 4) + "^\\circ") + (ex && ex.d === 1 ? "" : "\\approx " + dmsT(deg(v))));
    }
    dg.addEventListener("input", conv); rd.addEventListener("input", conv); onLang(conv);
  }

  /* ---------- 5.2 triangle rectangle ---------- */
  function wRt() {
    var w = byId("w-rt"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), sa = $(w, "a"), sc = $(w, "c");
    function draw() {
      var al = +sa.value, c = +sc.value, a = c * Math.sin(rad(al)), b = c * Math.cos(rad(al));
      $(w, "av").textContent = al + "°"; $(w, "cv").textContent = decS(c, 1);
      var k = Math.min(24, 270 / b, 190 / a), Ax = 25, Ay = 220, Cx = Ax + b * k, By = Ay - a * k;
      var h = '<path class="tri" d="M' + Ax + " " + Ay + "L" + f1(Cx) + " " + Ay + "L" + f1(Cx) + " " + f1(By) + 'Z"/>';
      h += '<path d="M' + f1(Cx - 11) + " " + Ay + "V" + (Ay - 11) + "H" + f1(Cx) + '" fill="none" stroke="var(--text)" stroke-width="1.3"/>';
      var r = 30, e = rad(al);
      h += '<path class="arc" style="stroke:' + COL.ang + '" d="M' + (Ax + r) + " " + Ay + "A" + r + " " + r + " 0 0 0 " + f1(Ax + r * Math.cos(e)) + " " + f1(Ay - r * Math.sin(e)) + '"/>';
      h += '<text class="lb it" x="' + f1(Ax + 42 * Math.cos(e / 2)) + '" y="' + f1(Ay - 42 * Math.sin(e / 2) + 5) + '" style="fill:' + COL.ang + '">α</text>';
      h += '<line class="sg" x1="' + f1(Cx) + '" y1="' + Ay + '" x2="' + f1(Cx) + '" y2="' + f1(By) + '" style="stroke:' + COL.sin + '"/>';
      h += '<line class="sg" x1="' + Ax + '" y1="' + Ay + '" x2="' + f1(Cx) + '" y2="' + Ay + '" style="stroke:' + COL.cos + '"/>';
      h += '<text class="lb it" x="' + f1((Ax + Cx) / 2) + '" y="' + (Ay + 16) + '" text-anchor="middle" style="fill:' + COL.cos + '">b</text>';
      h += '<text class="lb it" x="' + f1(Cx + 12) + '" y="' + f1((Ay + By) / 2) + '" style="fill:' + COL.sin + '">a</text>';
      h += '<text class="lb it" x="' + f1((Ax + Cx) / 2 - 12) + '" y="' + f1((Ay + By) / 2 - 6) + '" text-anchor="middle">c</text>';
      h += '<text class="lb it" x="' + (Ax - 12) + '" y="' + (Ay + 5) + '">A</text><text class="lb it" x="' + f1(Cx + 6) + '" y="' + (Ay + 14) + '">C</text><text class="lb it" x="' + f1(Cx + 6) + '" y="' + f1(By + 4) + '">B</text>';
      svg.innerHTML = h;
      var E = { 30: ["\\frac12", "\\frac{\\sqrt3}{2}", "\\frac{\\sqrt3}{3}"], 45: ["\\frac{\\sqrt2}{2}", "\\frac{\\sqrt2}{2}", "1"], 60: ["\\frac{\\sqrt3}{2}", "\\frac12", "\\sqrt3"] }[al];
      function q(n, d, v, i) { return tex("=\\dfrac{" + n + "}{" + d + "}=\\dfrac{" + dT(n === "a" ? a : b, 2) + "}{" + dT(d === "c" ? c : b, 2) + "}" + apx(v, 4) + (E ? "=" + E[i] : "")); }
      info.innerHTML = kv([
        [t3("Costats", "Lados", "Sides"), tex("a" + apx(a, 2) + ",\\ \\ b" + apx(b, 2) + ",\\ \\ c=" + dT(c, 1))],
        [cdot(COL.sin) + tex("\\sin\\alpha"), q("a", "c", Math.sin(e), 0).replace("=\\dfrac{a}", "\\dfrac{a}")],
        [cdot(COL.cos) + tex("\\cos\\alpha"), q("b", "c", Math.cos(e), 1)],
        [tex("\\tan\\alpha"), tex("=\\dfrac{a}{b}=\\dfrac{" + dT(a, 2) + "}{" + dT(b, 2) + "}" + apx(Math.tan(e), 4) + (E ? "=" + E[2] : ""))],
        [t3("Comprovació", "Comprobación", "Check"), tex("\\sin^2\\alpha+\\cos^2\\alpha=1")]
      ]);
    }
    sa.addEventListener("input", draw); sc.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 5.3 circumferència goniomètrica ---------- */
  function quadOf(a) { a = norm360(a); return a % 90 === 0 ? 0 : Math.floor(a / 90) + 1; }
  function quadName(q) { return ["", "I", "II", "III", "IV"][q]; }
  function wCirc() {
    var w = byId("w-circ"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), snap = $(w, "snap"), A = 150;
    var C = UC(svg, { W: 320, R: 105 });
    C.onDrag = function (d) { A = snap.checked ? Math.round(d / 15) * 15 % 360 : Math.round(d) % 360; draw(); };
    function v(x) { return x == null ? "\\nexists" : x; }
    function draw() {
      var e = rad(A), c = Math.cos(e), s = Math.sin(e), ex = exact(A), q = quadOf(A);
      if (Math.abs(c) < 1e-12) c = 0; if (Math.abs(s) < 1e-12) s = 0;
      var tn = c ? s / c : null, h = C.sector(0, A, COL.ang) + C.arc(0, A, 24, COL.ang, A ? A + "°" : "");
      if (tn != null) {
        var lim = 1.45, ty = Math.max(-lim, Math.min(lim, tn));
        h += C.seg(1, -1.45, 1, 1.45, "var(--muted)", "gd") + C.seg(0, 0, 1, ty * (Math.abs(tn) > lim ? 1 : 1), "var(--muted)", "gd");
        h += C.seg(1, 0, 1, ty, COL.tan, "sg") + (Math.abs(tn) <= lim ? C.dot(1, tn, COL.tan) + C.text(1, tn, "T", 12, 4, COL.tan, true) : "");
      }
      h += C.seg(c, 0, c, s, "var(--muted)", "gd") + C.seg(0, s, c, s, "var(--muted)", "gd");
      h += C.seg(0, 0, c, 0, COL.cos, "sg") + C.seg(c, 0, c, s, COL.sin, "sg") + C.seg(0, 0, c, s, "var(--text)");
      h += C.dot(c, s, COL.r, true) + C.text(c, s, "P", c >= 0 ? 14 : -14, s >= 0 ? -8 : 16, null, true);
      C.draw(h);
      function val(qx, num) { return qx ? qT(qx) + (qx.slice(1).some(function (f) { return f.n; }) ? "\\approx " + dT(num, 4) : "") : num == null ? "\\nexists" : dT(num, 4).replace(/^/, Math.abs(num - +num.toFixed(4)) > 1e-10 ? "\\approx " : ""); }
      var f = Fr(A, 180), rows = [
        [t3("Angle", "Ángulo", "Angle"), tex("\\alpha=" + A + "^\\circ=" + piT(f) + "\\ \\text{rad}") + small(q ? t3("Quadrant ", "Cuadrante ", "Quadrant ") + quadName(q) : t3("Sobre un eix", "Sobre un eje", "On an axis"))],
        [t3("Punt", "Punto", "Point"), tex("P=(\\cos\\alpha,\\ \\sin\\alpha)")],
        [cdot(COL.sin) + tex("\\sin\\alpha"), tex(val(ex && ex.s, s))],
        [cdot(COL.cos) + tex("\\cos\\alpha"), tex(val(ex && ex.c, c))],
        [cdot(COL.tan) + tex("\\tan\\alpha"), tex(tn == null ? "\\nexists\\ (\\cos\\alpha=0)" : val(ex && ex.t, tn))],
        [t3("Signes", "Signos", "Signs"), q ? tex("\\sin" + (s > 0 ? "+" : "-") + ",\\ \\cos" + (c > 0 ? "+" : "-") + ",\\ \\tan" + (s * c > 0 ? "+" : "-")) : "—"]
      ];
      info.innerHTML = kv(rows);
    }
    snap.addEventListener("change", draw); onLang(draw);
  }

  /* ---------- 5.3 raons a partir d'una ---------- */
  function wFind() {
    var w = byId("w-find"); if (!w) return;
    var info = w.querySelector(".info"), R = $(w, "r"), V = $(w, "v"), QS = $(w, "q");
    var PRE = [["cos", "0.7", 1], ["tan", "-3", 2], ["sin", "0.62", 2], ["cos", "-0.83", 3], ["tan", "-0.92", 4], ["sin", "-4/5", 4], ["tan", "5/12", 1]];
    var NM = { sin: "\\sin\\alpha", cos: "\\cos\\alpha", tan: "\\tan\\alpha", sec: "\\sec\\alpha", csc: "\\text{cosec}\\,\\alpha", cot: "\\text{cotg}\\,\\alpha" };
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { var pv = parseVal(p[1]); return tex(NM[p[0]] + "=" + (pv.ex ? sT(pv.ex) : dT(pv.v, 4)) + "\\ (" + quadName(p[2]) + ")"); }); },
      function (i) { R.value = PRE[i][0]; V.value = PRE[i][1]; QS.value = PRE[i][2]; draw(); }, 0);
    function draw() {
      var r = R.value, q = +QS.value, pv = parseVal(V.value);
      V.classList.toggle("bad", !pv);
      if (!pv) { info.innerHTML = t3("Escriu un nombre: <code>0.62</code>, <code>-3/5</code>, <code>sqrt5/3</code>…", "Escribe un número: <code>0.62</code>, <code>-3/5</code>, <code>sqrt5/3</code>…", "Type a number: <code>0.62</code>, <code>-3/5</code>, <code>sqrt5/3</code>…"); return; }
      var sgS = q <= 2 ? 1 : -1, sgC = q === 1 || q === 4 ? 1 : -1, sgT = sgS * sgC;
      var E = !!pv.ex, rows = [], steps = [];
      // operacions en mode exacte (r·√m) o decimal
      var O = E ? { T: sT, inv: sInv, mul: sMul, div: sDiv, neg: sNeg, v: sVal, one_sq: function (x) { return sSqrt(fSub(1, sSq(x))); }, inv_sq1: function (t) { return sSqrt(fDiv(1, fAdd(1, sSq(t)))); }, sq: function (x) { return fT(sSq(x)); }, ok1: function (x) { return fVal(fSub(1, sSq(x))) >= 0; } }
        : { T: function (x) { return dT(x, 4); }, inv: function (x) { return 1 / x; }, mul: function (a, b) { return a * b; }, div: function (a, b) { return a / b; }, neg: function (x) { return -x; }, v: function (x) { return x; }, one_sq: function (x) { return Math.sqrt(1 - x * x); }, inv_sq1: function (t) { return 1 / Math.sqrt(1 + t * t); }, sq: function (x) { return dT(x * x, 4); }, ok1: function (x) { return Math.abs(x) <= 1 + 1e-12; } };
      var x = E ? pv.ex : pv.v, xv = pv.v, eq = E ? "=" : "\\approx ";
      function T(y) { return O.T(y); }
      function sgName(sg) { return sg > 0 ? t3("positiu", "positivo", "positive") : t3("negatiu", "negativo", "negative"); }
      // raó base
      var base = r, b = x;
      if (r === "sec" || r === "csc" || r === "cot") {
        if (Math.abs(xv) < 1e-12) { info.innerHTML = t3("Aquesta raó no pot valdre 0.", "Esta razón no puede valer 0.", "This ratio cannot be 0."); return; }
        base = { sec: "cos", csc: "sin", cot: "tan" }[r]; b = O.inv(x);
        steps.push(tex(NM[base] + "=\\dfrac{1}{" + NM[r] + "}=" + T(b)));
      }
      var bv = O.v(b), need = { sin: sgS, cos: sgC, tan: sgT }[base];
      if ((base === "sin" || base === "cos") && !O.ok1(b)) { info.innerHTML = kv([[t3("Impossible", "Imposible", "Impossible"), tex("-1\\le " + NM[base] + "\\le 1")]]); return; }
      if (Math.abs(bv) > 1e-12 && Math.sign(bv) !== need) {
        info.innerHTML = kv([[t3("Impossible", "Imposible", "Impossible"), t3("En el quadrant ", "En el cuadrante ", "In quadrant ") + quadName(q) + t3(" el ", " el ", " ") + tex(NM[base]) + t3(" és ", " es ", " is ") + sgName(need) + "."]]); return;
      }
      var s, c, t;
      if (base === "sin") {
        s = b; c = O.one_sq(b); if (sgC < 0) c = O.neg(c);
        steps.push(tex("\\cos^2\\alpha=1-\\sin^2\\alpha=1-" + O.sq(b) + "\\Rightarrow\\cos\\alpha=" + (sgC < 0 ? "-" : "+") + "\\sqrt{1-" + O.sq(b) + "}" + eq + T(c)) + small(t3("El cosinus és ", "El coseno es ", "The cosine is ") + sgName(sgC) + t3(" en el quadrant ", " en el cuadrante ", " in quadrant ") + quadName(q) + "."));
      } else if (base === "cos") {
        c = b; s = O.one_sq(b); if (sgS < 0) s = O.neg(s);
        steps.push(tex("\\sin^2\\alpha=1-\\cos^2\\alpha=1-" + O.sq(b) + "\\Rightarrow\\sin\\alpha=" + (sgS < 0 ? "-" : "+") + "\\sqrt{1-" + O.sq(b) + "}" + eq + T(s)) + small(t3("El sinus és ", "El seno es ", "The sine is ") + sgName(sgS) + t3(" en el quadrant ", " en el cuadrante ", " in quadrant ") + quadName(q) + "."));
      } else {
        t = b; c = O.inv_sq1(b); if (sgC < 0) c = O.neg(c);
        steps.push(tex("\\dfrac{1}{\\cos^2\\alpha}=1+\\tan^2\\alpha=1+" + O.sq(b) + "\\Rightarrow\\cos\\alpha=" + (sgC < 0 ? "-" : "+") + "\\dfrac{1}{\\sqrt{1+" + O.sq(b) + "}}" + eq + T(c)) + small(t3("El cosinus és ", "El coseno es ", "The cosine is ") + sgName(sgC) + t3(" en el quadrant ", " en el cuadrante ", " in quadrant ") + quadName(q) + "."));
        s = O.mul(t, c); steps.push(tex("\\sin\\alpha=\\tan\\alpha\\cdot\\cos\\alpha" + eq + T(s)));
      }
      var cv = O.v(c), sv = O.v(s);
      if (base !== "tan") { if (Math.abs(cv) < 1e-12) { t = null; steps.push(tex("\\tan\\alpha\\ \\nexists\\ (\\cos\\alpha=0)")); } else { t = O.div(s, c); steps.push(tex("\\tan\\alpha=\\dfrac{\\sin\\alpha}{\\cos\\alpha}" + eq + T(t))); } }
      var ang = deg(Math.atan2(sv, cv)); if (ang < 0) ang += 360;
      steps.push(t3("Amb la calculadora: ", "Con la calculadora: ", "With a calculator: ") + tex("\\alpha" + (Math.abs(ang - Math.round(ang)) < 1e-6 ? "=" + Math.round(ang) + "^\\circ" : "\\approx " + dmsT(ang))));
      info.innerHTML = "<ol>" + steps.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ol>";
    }
    [R, QS].forEach(function (el) { el.addEventListener("change", draw); }); V.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 5.4 reducció al primer quadrant ---------- */
  function wRed() {
    var w = byId("w-red"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), B = $(w, "b");
    var C = UC(svg, { W: 320, R: 105 });
    var PRE = ["155", "240", "390", "1920", "-30", "-185", "835", "1750"];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(p.replace("-", "-") + "^\\circ"); }); }, function (i) { B.value = PRE[i]; draw(); }, 3);
    function draw() {
      var b = parseNum(B.value); B.classList.toggle("bad", b == null);
      if (b == null) { info.innerHTML = ""; C.draw(""); return; }
      var b0 = norm360(b), k = Math.round((b - b0) / 360), q = quadOf(b0), rows = [];
      if (k) rows.push([t3("Primera volta", "Primera vuelta", "First turn"), tex(angT(b) + "=" + (k === 1 ? "" : k === -1 ? "-" : k + "\\cdot") + "360^\\circ+" + angT(b0)) + small(t3("Les raons de ", "Las razones de ", "The ratios of ") + tex(angT(b)) + t3(" i de ", " y de ", " and ") + tex(angT(b0)) + t3(" són les mateixes.", " son las mismas.", " are the same."))]);
      var a, rel, sS, sC, sT;
      if (q === 0) {
        rows.push([t3("Posició", "Posición", "Position"), t3("Sobre un eix", "Sobre un eje", "On an axis")]);
        a = null;
      } else {
        a = q === 1 ? b0 : q === 2 ? 180 - b0 : q === 3 ? b0 - 180 : 360 - b0;
        rel = q === 1 ? "" : q === 2 ? "180^\\circ-" + angT(a) : q === 3 ? "180^\\circ+" + angT(a) : "360^\\circ-" + angT(a);
        sS = q <= 2 ? "" : "-"; sC = q === 1 || q === 4 ? "" : "-"; sT = q === 1 || q === 3 ? "" : "-";
        rows.push([t3("Quadrant", "Cuadrante", "Quadrant"), quadName(q) + (q > 1 ? ": " + tex(angT(b0) + "=" + rel) : "")]);
      }
      var ex = exact(b0), e = rad(b0), sv = Math.sin(e), cv = Math.cos(e);
      function num(x) { return Math.abs(x) < 1e-12 ? "0" : (Math.abs(x - +x.toFixed(4)) > 1e-10 ? "\\approx " : "") + dT(x, 4); }
      function show(qx, x) { return qx ? qT(qx) : x == null ? "\\nexists" : num(x); }
      if (a != null && q > 1) {
        var ea = exact(a), A = angT(a);
        rows.push([tex("\\sin"), tex("\\sin " + angT(b0) + "=" + sS + "\\sin " + A + "=" + show(ex && ex.s, sv))]);
        rows.push([tex("\\cos"), tex("\\cos " + angT(b0) + "=" + sC + "\\cos " + A + "=" + show(ex && ex.c, cv))]);
        rows.push([tex("\\tan"), tex("\\tan " + angT(b0) + "=" + sT + "\\tan " + A + "=" + show(ex && ex.t, sv / cv))]);
      } else {
        rows.push([tex("\\sin"), tex("\\sin " + angT(b0) + "=" + show(ex && ex.s, sv))]);
        rows.push([tex("\\cos"), tex("\\cos " + angT(b0) + "=" + show(ex && ex.c, Math.abs(cv) < 1e-12 ? 0 : cv))]);
        rows.push([tex("\\tan"), tex("\\tan " + angT(b0) + "=" + (Math.abs(cv) < 1e-12 ? "\\nexists" : show(ex && ex.t, sv / cv)))]);
      }
      info.innerHTML = kv(rows);
      var h = C.sector(0, b0, COL.ang) + C.arc(0, b0, 24, COL.ang, "β");
      if (a != null && q > 1) {
        var ar = rad(a);
        h += C.seg(0, 0, Math.cos(ar), Math.sin(ar), COL.cos, "ln") + C.dot(Math.cos(ar), Math.sin(ar), COL.cos) + C.arc(0, a, 44, COL.cos, "α");
        h += C.seg(Math.cos(ar), Math.sin(ar), cv, sv, "var(--muted)", "gd");
        h += C.text(Math.cos(ar), Math.sin(ar), "P₀", 14, -8, COL.cos);
      }
      h += C.seg(0, 0, cv, sv, "var(--text)") + C.dot(cv, sv, COL.ang) + C.text(cv, sv, "P", cv >= 0 ? 14 : -14, sv >= 0 ? -8 : 16, COL.ang, true);
      C.draw(h);
    }
    B.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- dibuix d'un triangle donat pels tres costats ---------- */
  // pts: [{A:[x,y], B:[x,y], C:[x,y]}, …] en unitats; dibuixa ajustant al requadre
  function triSvg(svg, tris, W, H, labels) {
    var xs = [], ys = [];
    tris.forEach(function (t) { ["A", "B", "C"].forEach(function (k) { xs.push(t[k][0]); ys.push(t[k][1]); }); });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var k = Math.min((W - 60) / Math.max(x1 - x0, 1e-9), (H - 50) / Math.max(y1 - y0, 1e-9));
    var ox = (W - (x1 - x0) * k) / 2 - x0 * k, oy = (H + (y1 - y0) * k) / 2 + y0 * k;
    function P(p) { return [f1(ox + p[0] * k), f1(oy - p[1] * k)]; }
    var h = "";
    tris.forEach(function (t, i) {
      var A = P(t.A), B = P(t.B), Cc = P(t.C);
      h += '<path class="tri' + (i ? " b" : "") + '" d="M' + A + "L" + B + "L" + Cc + 'Z"/>';
    });
    tris.forEach(function (t, i) {
      var g = [(t.A[0] + t.B[0] + t.C[0]) / 3, (t.A[1] + t.B[1] + t.C[1]) / 3];
      ["A", "B", "C"].forEach(function (key) {
        if (i && t[key] === tris[0][key]) return;
        var p = t[key], dx = p[0] - g[0], dy = p[1] - g[1], dd = Math.hypot(dx, dy) || 1, q = P(p);
        h += '<text class="lb it" x="' + f1(+q[0] + dx / dd * 14) + '" y="' + f1(+q[1] - dy / dd * 14 + 5) + '" text-anchor="middle"' + (i ? ' style="fill:#7c3aed"' : "") + ">" + key + (i ? "₂" : tris.length > 1 && t[key] !== tris[1][key] ? "₁" : "") + "</text>";
      });
      if (labels !== false) [["a", "B", "C"], ["b", "A", "C"], ["c", "A", "B"]].forEach(function (s) {
        if (i && t[s[1]] === tris[0][s[1]] && t[s[2]] === tris[0][s[2]]) return;
        var m = [(t[s[1]][0] + t[s[2]][0]) / 2, (t[s[1]][1] + t[s[2]][1]) / 2], dx = m[0] - g[0], dy = m[1] - g[1], dd = Math.hypot(dx, dy) || 1, q = P(m);
        h += '<text class="lb it" x="' + f1(+q[0] + dx / dd * 12) + '" y="' + f1(+q[1] - dy / dd * 12 + 5) + '" text-anchor="middle" style="fill:' + (i ? "#7c3aed" : "var(--muted)") + '">' + s[0] + "</text>";
      });
    });
    svg.innerHTML = h;
  }
  function triFrom(a, b, c, A) { // A a l'origen, B sobre l'eix X
    return { A: [0, 0], B: [c, 0], C: [b * Math.cos(rad(A)), b * Math.sin(rad(A))] };
  }

  /* ---------- 5.5 triangles rectangles ---------- */
  function wRect() {
    var w = byId("w-rect"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), K = ["a", "b", "c", "A", "B"], I = {};
    K.forEach(function (k) { I[k] = $(w, k); I[k].addEventListener("input", draw); });
    var PRE = [{ a: "11", c: "20" }, { a: "15", B: "50" }, { c: "32", B: "57" }, { a: "250", b: "308" }, { a: "35", A: "32" }, { b: "1.7", A: "73 36" }];
    function angL(s) { var q = s.split(" "); return q[0] + "^\\circ" + (q[1] ? q[1] + "'" : ""); }
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(Object.keys(p).map(function (k) { return k === k.toUpperCase() ? "\\hat " + k + "=" + angL(p[k]) : k + "=" + dT(+p[k], 2); }).join(",\\ ")); }); },
      function (i) { K.forEach(function (k) { I[k].value = PRE[i][k] || ""; }); draw(); }, 0);
    function draw() {
      var v = {}, bad = false, given = [];
      K.forEach(function (k) {
        var s = I[k].value.trim(), x = s === "" ? null : k === "A" || k === "B" ? parseAng(s) : parseNum(s);
        var okv = s === "" || (x != null && x > 0 && (k === "A" || k === "B" ? x < 90 : true));
        I[k].classList.toggle("bad", !okv); if (!okv) bad = true;
        if (s !== "" && okv) { v[k] = x; given.push(k); }
      });
      function msg(t) { info.innerHTML = t; svg.innerHTML = ""; }
      if (bad) return msg(t3("Revisa les dades: costats positius i angles aguts.", "Revisa los datos: lados positivos y ángulos agudos.", "Check the data: positive sides and acute angles."));
      if (given.length !== 2) return msg(t3("Escriu exactament <strong>dues</strong> dades.", "Escribe exactamente <strong>dos</strong> datos.", "Enter exactly <strong>two</strong> data."));
      var g = given.join("");
      if (g === "AB") return msg(t3("Amb dos angles no n'hi ha prou: cal almenys un costat.", "Con dos ángulos no basta: hace falta al menos un lado.", "Two angles are not enough: at least one side is needed."));
      var a = v.a, b = v.b, c = v.c, A = v.A, Bb = v.B, st = [];
      function sd(x) { return dT(x, 2); }
      function ap2(x) { return apx(x, 2); }
      if ((g === "ac" || g === "bc") && (v.a || v.b) >= v.c) return msg(t3("La hipotenusa ha de ser el costat més llarg.", "La hipotenusa tiene que ser el lado más largo.", "The hypotenuse must be the longest side."));
      if (g === "ab") { c = Math.hypot(a, b); A = deg(Math.atan(a / b)); st.push(t3("Pitàgores: ", "Pitágoras: ", "Pythagoras: ") + tex("c=\\sqrt{" + sd(a) + "^2+" + sd(b) + "^2}" + ap2(c))); st.push(tex("\\tan\\hat A=\\dfrac ab=\\dfrac{" + sd(a) + "}{" + sd(b) + "}\\Rightarrow\\hat A" + "\\approx " + dmsT(A))); }
      else if (g === "ac") { b = Math.sqrt(c * c - a * a); A = deg(Math.asin(a / c)); st.push(t3("Pitàgores: ", "Pitágoras: ", "Pythagoras: ") + tex("b=\\sqrt{" + sd(c) + "^2-" + sd(a) + "^2}" + ap2(b))); st.push(tex("\\sin\\hat A=\\dfrac ac=\\dfrac{" + sd(a) + "}{" + sd(c) + "}\\Rightarrow\\hat A\\approx " + dmsT(A))); }
      else if (g === "bc") { a = Math.sqrt(c * c - b * b); A = deg(Math.acos(b / c)); st.push(t3("Pitàgores: ", "Pitágoras: ", "Pythagoras: ") + tex("a=\\sqrt{" + sd(c) + "^2-" + sd(b) + "^2}" + ap2(a))); st.push(tex("\\cos\\hat A=\\dfrac bc=\\dfrac{" + sd(b) + "}{" + sd(c) + "}\\Rightarrow\\hat A\\approx " + dmsT(A))); }
      else {
        if (Bb != null) A = 90 - Bb;
        var AT = dmsT(A), BT = dmsT(90 - A);
        st.push(tex("\\hat " + (v.A != null ? "B" : "A") + "=90^\\circ-" + (v.A != null ? AT : BT) + "=" + (v.A != null ? BT : AT)));
        if (g === "aA") { c = a / Math.sin(rad(A)); b = a / Math.tan(rad(A)); st.push(tex("\\sin\\hat A=\\dfrac ac\\Rightarrow c=\\dfrac{" + sd(a) + "}{\\sin " + AT + "}" + ap2(c))); st.push(tex("\\tan\\hat A=\\dfrac ab\\Rightarrow b=\\dfrac{" + sd(a) + "}{\\tan " + AT + "}" + ap2(b))); }
        else if (g === "aB") { b = a * Math.tan(rad(90 - A)); c = a / Math.cos(rad(90 - A)); st.push(tex("\\tan\\hat B=\\dfrac ba\\Rightarrow b=" + sd(a) + "\\cdot\\tan " + BT + ap2(b))); st.push(tex("\\cos\\hat B=\\dfrac ac\\Rightarrow c=\\dfrac{" + sd(a) + "}{\\cos " + BT + "}" + ap2(c))); }
        else if (g === "bA") { a = b * Math.tan(rad(A)); c = b / Math.cos(rad(A)); st.push(tex("\\tan\\hat A=\\dfrac ab\\Rightarrow a=" + sd(b) + "\\cdot\\tan " + AT + ap2(a))); st.push(tex("\\cos\\hat A=\\dfrac bc\\Rightarrow c=\\dfrac{" + sd(b) + "}{\\cos " + AT + "}" + ap2(c))); }
        else if (g === "bB") { a = b / Math.tan(rad(90 - A)); c = b / Math.sin(rad(90 - A)); st.push(tex("\\tan\\hat B=\\dfrac ba\\Rightarrow a=\\dfrac{" + sd(b) + "}{\\tan " + BT + "}" + ap2(a))); st.push(tex("\\sin\\hat B=\\dfrac bc\\Rightarrow c=\\dfrac{" + sd(b) + "}{\\sin " + BT + "}" + ap2(c))); }
        else if (g === "cA") { a = c * Math.sin(rad(A)); b = c * Math.cos(rad(A)); st.push(tex("a=c\\cdot\\sin\\hat A=" + sd(c) + "\\cdot\\sin " + AT + ap2(a))); st.push(tex("b=c\\cdot\\cos\\hat A=" + sd(c) + "\\cdot\\cos " + AT + ap2(b))); }
        else if (g === "cB") { a = c * Math.cos(rad(90 - A)); b = c * Math.sin(rad(90 - A)); st.push(tex("a=c\\cdot\\cos\\hat B=" + sd(c) + "\\cdot\\cos " + BT + ap2(a))); st.push(tex("b=c\\cdot\\sin\\hat B=" + sd(c) + "\\cdot\\sin " + BT + ap2(b))); }
      }
      if (g === "ab" || g === "ac" || g === "bc") st.push(tex("\\hat B=90^\\circ-\\hat A\\approx " + dmsT(90 - A)));
      st.push("<strong>" + t3("Solució", "Solución", "Solution") + ":</strong> " + tex("a\\approx " + sd(a) + ",\\ b\\approx " + sd(b) + ",\\ c\\approx " + sd(c) + ",\\ \\hat A\\approx " + dmsT(A) + ",\\ \\hat B\\approx " + dmsT(90 - A) + ",\\ \\hat C=90^\\circ"));
      info.innerHTML = "<ol>" + st.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ol>";
      triSvg(svg, [{ A: [0, 0], C: [b, 0], B: [b, a] }], 320, 240);
      var sq = svg.querySelectorAll("path.tri")[0];
      if (sq) { var d = sq.getAttribute("d").match(/[\d.]+/g).map(Number), cx = d[4], cy = d[5]; svg.insertAdjacentHTML("beforeend", '<path d="M' + (cx - 10) + " " + cy + "V" + (cy - 10) + "H" + cx + '" fill="none" stroke="var(--text)" stroke-width="1.3"/>'); }
    }
    onLang(draw);
  }

  /* ---------- 5.4 existeix un angle amb aquestes dues raons? ---------- */
  // k: "sc" (sin, cos), "st" (sin, tg), "ct" (cos, tg); X, Y: resultats de parseVal
  var PAIR = {
    sc: { n: ["\\sin\\alpha", "\\cos\\alpha"], id: "\\sin^2\\alpha+\\cos^2\\alpha=1" },
    st: { n: ["\\sin\\alpha", "\\tan\\alpha"], id: "1+\\dfrac{1}{\\tan^2\\alpha}=\\dfrac{1}{\\sin^2\\alpha}" },
    ct: { n: ["\\cos\\alpha", "\\tan\\alpha"], id: "1+\\tan^2\\alpha=\\dfrac{1}{\\cos^2\\alpha}" }
  };
  function chkPair(k, X, Y) {
    var E = !!(X.ex && Y.ex), x = X.v, y = Y.v, L, R, Lt, Rt, ok;
    if (k !== "sc" && (Math.abs(x) < 1e-12 || Math.abs(y) < 1e-12)) return { err: "zero" };
    if (Math.abs(x) > 1 + 1e-12) return { err: "range", which: 0 };
    if (k === "sc" && Math.abs(y) > 1 + 1e-12) return { err: "range", which: 1 };
    function ft(f) { return E ? fT(f) : dT(f, 4); }
    if (E) {
      var x2 = sSq(X.ex), y2 = sSq(Y.ex);
      if (k === "sc") { L = fAdd(x2, y2); R = Fr(1); Lt = "\\left(" + sT(X.ex) + "\\right)^2+\\left(" + sT(Y.ex) + "\\right)^2=" + fT(x2) + "+" + fT(y2) + "=" + fT(L); Rt = "1"; }
      else if (k === "ct") { L = fAdd(1, y2); R = fDiv(1, x2); Lt = "1+\\left(" + sT(Y.ex) + "\\right)^2=1+" + fT(y2) + "=" + fT(L); Rt = "\\dfrac{1}{" + fT(x2).replace(/^\\frac/, "\\tfrac") + "}=" + fT(R); }
      else { L = fAdd(1, fDiv(1, y2)); R = fDiv(1, x2); Lt = "1+\\dfrac{1}{" + fT(y2).replace(/^\\frac/, "\\tfrac") + "}=" + fT(L); Rt = "\\dfrac{1}{" + fT(x2).replace(/^\\frac/, "\\tfrac") + "}=" + fT(R); }
      ok = L.n === R.n && L.d === R.d; L = fVal(L); R = fVal(R);
    } else {
      if (k === "sc") { L = x * x + y * y; R = 1; Lt = dT(x, 4) + "^2+" + dT(y, 4) + "^2\\approx " + dT(L, 4); Rt = "1"; }
      else if (k === "ct") { L = 1 + y * y; R = 1 / (x * x); Lt = "1+" + dT(y, 4) + "^2\\approx " + dT(L, 4); Rt = "\\dfrac{1}{" + dT(x, 4) + "^2}\\approx " + dT(R, 4); }
      else { L = 1 + 1 / (y * y); R = 1 / (x * x); Lt = "1+\\dfrac{1}{" + dT(y, 4) + "^2}\\approx " + dT(L, 4); Rt = "\\dfrac{1}{" + dT(x, 4) + "^2}\\approx " + dT(R, 4); }
      ok = Math.abs(L - R) <= 0.002 * Math.max(1, Math.abs(R));
    }
    var s, c;
    if (k === "sc") { s = x; c = y; } else if (k === "ct") { c = x; s = x * y; } else { s = x; c = x / y; }
    var a = deg(Math.atan2(s, c)); if (a < 0) a += 360;
    return { ok: ok, E: E, L: L, R: R, Lt: Lt, Rt: Rt, ang: a, s: s, c: c };
  }
  function wChk() {
    var w = byId("w-chk"); if (!w) return;
    var info = w.querySelector(".info"), K = $(w, "k"), X = $(w, "x"), Y = $(w, "y"), LX = $(w, "lx"), LY = $(w, "ly");
    var PRE = [["sc", "7/25", "11/25"], ["sc", "sqrt5/5", "2sqrt5/5"], ["st", "7/11", "6/11"], ["ct", "sqrt3/2", "sqrt3/3"], ["ct", "0.9397", "0.3640"], ["sc", "0.1485", "0.2588"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { var a = parseVal(p[1]), b = parseVal(p[2]); function sh(q) { return q.ex ? sT(q.ex) : dT(q.v, 4); } return tex(PAIR[p[0]].n[0] + "=" + sh(a) + ",\\ " + PAIR[p[0]].n[1] + "=" + sh(b)); }); },
      function (i) { K.value = PRE[i][0]; X.value = PRE[i][1]; Y.value = PRE[i][2]; draw(); }, 0);
    function draw() {
      var k = K.value, P = PAIR[k];
      LX.innerHTML = tex(P.n[0] + "="); LY.innerHTML = tex(P.n[1] + "=");
      var a = parseVal(X.value), b = parseVal(Y.value);
      X.classList.toggle("bad", !a); Y.classList.toggle("bad", !b);
      if (!a || !b) { info.innerHTML = t3("Escriu dos nombres: <code>0.62</code>, <code>-3/5</code>, <code>sqrt5/3</code>…", "Escribe dos números: <code>0.62</code>, <code>-3/5</code>, <code>sqrt5/3</code>…", "Type two numbers: <code>0.62</code>, <code>-3/5</code>, <code>sqrt5/3</code>…"); return; }
      var r = chkPair(k, a, b);
      if (r.err === "zero") { info.innerHTML = t3("Per a aquesta comprovació les dues raons han de ser diferents de 0.", "Para esta comprobación las dos razones tienen que ser distintas de 0.", "For this check both ratios must be non-zero."); return; }
      if (r.err === "range") { info.innerHTML = kv([[t3("No hi ha cap angle", "No hay ningún ángulo", "No such angle"), tex("-1\\le " + P.n[r.which] + "\\le 1")]]); return; }
      var rows = [
        [t3("Relació", "Relación", "Identity"), tex(P.id)],
        [t3("Primer membre", "Primer miembro", "Left-hand side"), tex(r.Lt)],
        [t3("Segon membre", "Segundo miembro", "Right-hand side"), tex(r.Rt)]
      ];
      if (r.ok) rows.push(['<strong class="sp">✓</strong>', (r.E ? t3("Són iguals: ", "Son iguales: ", "They are equal: ") : t3("Coincideixen (llevat dels arrodoniments): ", "Coinciden (salvo los redondeos): ", "They match (up to rounding): ")) +
        t3("<strong>sí que hi ha</strong> un angle, ", "<strong>sí hay</strong> un ángulo, ", "<strong>there is</strong> such an angle, ") + tex("\\alpha\\approx " + dmsT(Math.round(r.ang * 3600) / 3600)) + small(t3("Quadrant ", "Cuadrante ", "Quadrant ") + quadName(quadOf(r.ang)) + ": " + tex("\\sin\\alpha" + (r.s > 0 ? "\\gt" : "\\lt") + "0,\\ \\cos\\alpha" + (r.c > 0 ? "\\gt" : "\\lt") + "0"))]);
      else rows.push(['<strong class="sm">✗</strong>', t3("Els dos membres no són iguals: <strong>no hi ha cap angle</strong> amb aquestes raons.", "Los dos miembros no son iguales: <strong>no hay ningún ángulo</strong> con estas razones.", "The two sides differ: <strong>no angle</strong> has these ratios.")]);
      info.innerHTML = kv(rows);
    }
    K.addEventListener("change", draw); X.addEventListener("input", draw); Y.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 5.6 doble observació ---------- */
  // mode "s": els dos punts al mateix costat (A, el més pròxim, veu el cim amb α; B, a d metres més lluny, amb β)
  // mode "o": costats oposats (A i B separats d metres, l'objecte entre ells)
  function dob(mode, a, b, d) {
    var ta = Math.tan(rad(a)), tb = Math.tan(rad(b)), x;
    if (mode === "s") { if (a <= b) return null; x = d * tb / (ta - tb); }
    else x = d * tb / (ta + tb);
    var h = x * ta;
    return { x: x, y: mode === "s" ? x + d : d - x, h: h, la: h / Math.sin(rad(a)), lb: h / Math.sin(rad(b)) };
  }
  function wDob() {
    var w = byId("w-dob"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), M = $(w, "m"), IA = $(w, "a"), IB = $(w, "b"), ID = $(w, "d");
    var PRE = [["s", "46", "33", "100"], ["s", "35", "20", "200"], ["s", "50", "40", "5"], ["s", "76", "45", "480"], ["o", "36", "12", "75"], ["o", "60", "45", "20"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex(p[1] + "^\\circ,\\ " + p[2] + "^\\circ,\\ d=" + p[3]) + (p[0] === "o" ? " · " + t3("oposats", "opuestos", "opposite") : ""); }); },
      function (i) { M.value = PRE[i][0]; IA.value = PRE[i][1]; IB.value = PRE[i][2]; ID.value = PRE[i][3]; draw(); }, 0);
    function draw() {
      M.options[0].text = t3("Al mateix costat", "Al mismo lado", "Same side"); M.options[1].text = t3("A costats oposats", "A lados opuestos", "Opposite sides");
      var mode = M.value, a = parseAng(IA.value), b = parseAng(IB.value), d = parseNum(ID.value);
      var okA = a != null && a > 0 && a < 90, okB = b != null && b > 0 && b < 90, okD = d != null && d > 0;
      IA.classList.toggle("bad", !okA); IB.classList.toggle("bad", !okB); ID.classList.toggle("bad", !okD);
      if (!okA || !okB || !okD) { info.innerHTML = t3("Els angles han de ser aguts i la distància, positiva.", "Los ángulos tienen que ser agudos y la distancia, positiva.", "The angles must be acute and the distance positive."); svg.innerHTML = ""; return; }
      var r = dob(mode, a, b, d);
      if (!r) { info.innerHTML = t3("Des del punt més pròxim l'angle d'elevació ha de ser <strong>més gran</strong>: \\(\\alpha\\gt\\beta\\).", "Desde el punto más cercano el ángulo de elevación tiene que ser <strong>mayor</strong>: \\(\\alpha\\gt\\beta\\).", "From the nearer point the angle of elevation must be <strong>larger</strong>: \\(\\alpha\\gt\\beta\\).").replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }); svg.innerHTML = ""; return; }
      var A = angT(a), B = angT(b), D = dT(d, 2), st = [];
      if (mode === "s") {
        st.push(t3("Dos triangles rectangles amb el mateix catet \\(h\\): ", "Dos triángulos rectángulos con el mismo cateto \\(h\\): ", "Two right triangles sharing the leg \\(h\\): ") + tex("\\tan " + A + "=\\dfrac hx,\\qquad \\tan " + B + "=\\dfrac{h}{x+" + D + "}"));
        st.push(t3("Aïllem \\(h\\) en les dues i igualem: ", "Despejamos \\(h\\) en las dos e igualamos: ", "Solve both for \\(h\\) and equate: ") + tex("x\\tan " + A + "=(x+" + D + ")\\tan " + B));
        st.push(tex("x\\,(\\tan " + A + "-\\tan " + B + ")=" + D + "\\tan " + B + "\\ \\Rightarrow\\ x=\\dfrac{" + D + "\\cdot" + dT(Math.tan(rad(b)), 4) + "}{" + dT(Math.tan(rad(a)), 4) + "-" + dT(Math.tan(rad(b)), 4) + "}" + apx(r.x, 2)));
      } else {
        st.push(t3("Dos triangles rectangles amb el mateix catet \\(h\\): ", "Dos triángulos rectángulos con el mismo cateto \\(h\\): ", "Two right triangles sharing the leg \\(h\\): ") + tex("\\tan " + A + "=\\dfrac hx,\\qquad \\tan " + B + "=\\dfrac{h}{" + D + "-x}"));
        st.push(t3("Aïllem \\(h\\) en les dues i igualem: ", "Despejamos \\(h\\) en las dos e igualamos: ", "Solve both for \\(h\\) and equate: ") + tex("x\\tan " + A + "=(" + D + "-x)\\tan " + B));
        st.push(tex("x\\,(\\tan " + A + "+\\tan " + B + ")=" + D + "\\tan " + B + "\\ \\Rightarrow\\ x=\\dfrac{" + D + "\\cdot" + dT(Math.tan(rad(b)), 4) + "}{" + dT(Math.tan(rad(a)), 4) + "+" + dT(Math.tan(rad(b)), 4) + "}" + apx(r.x, 2)));
      }
      st.push(tex("h=x\\tan " + A + apx(r.h, 2)));
      st.push(t3("Distàncies en línia recta fins al punt \\(M\\): ", "Distancias en línea recta hasta el punto \\(M\\): ", "Straight-line distances to the point \\(M\\): ") + tex("\\overline{AM}=\\dfrac{h}{\\sin " + A + "}" + apx(r.la, 2) + ",\\quad \\overline{BM}=\\dfrac{h}{\\sin " + B + "}" + apx(r.lb, 2)));
      info.innerHTML = "<ol>" + st.map(function (x) { return "<li>" + x.replace(/\\\((.*?)\\\)/g, function (_, m) { return tex(m); }) + "</li>"; }).join("") + "</ol>";
      // dibuix (unitats: metres) — peu de l'altura en H
      var W = 420, Hh = 230, xs, pA, pB;
      if (mode === "s") { pA = -r.x; pB = -r.y; xs = [pB, 0]; } else { pA = -r.x; pB = r.y; xs = [pA, pB]; }
      var span = Math.max(xs[1] - xs[0], 1e-9), k = Math.min((W - 70) / span, (Hh - 75) / r.h), ox = (W - span * k) / 2 - xs[0] * k, oy = Hh - 42;
      function X(v) { return f1(ox + v * k); } function Y(v) { return f1(oy - v * k); }
      var g = '<path d="M10 ' + oy + "H" + (W - 10) + '" stroke="var(--muted)" stroke-width="1.5"/>';
      g += '<path d="M' + X(0) + " " + oy + "V" + Y(r.h) + '" stroke="var(--text)" stroke-width="3"/>';
      g += '<path d="M' + X(0) + " " + (oy - 10) + "H" + (mode === "s" ? X(0) - 10 : +X(0) + 10) + "V" + oy + '" fill="none" stroke="var(--text)" stroke-width="1.2"/>';
      g += '<path class="ln" style="stroke:' + COL.cos + '" d="M' + X(pA) + " " + oy + "L" + X(0) + " " + Y(r.h) + '"/><path class="ln" style="stroke:' + COL.r + '" d="M' + X(pB) + " " + oy + "L" + X(0) + " " + Y(r.h) + '"/>';
      function arcAt(px, ang, dir, col, lbl) {
        var R0 = 30, e = rad(ang), x0 = +px + dir * R0, y0 = oy, x1 = +px + dir * R0 * Math.cos(e), y1 = oy - R0 * Math.sin(e);
        return '<path class="arc" style="stroke:' + col + '" d="M' + f1(x0) + " " + y0 + "A" + R0 + " " + R0 + " 0 0 " + (dir > 0 ? 0 : 1) + " " + f1(x1) + " " + f1(y1) + '"/><text class="lb" x="' + f1(+px + dir * (R0 + 16) * Math.cos(e / 2)) + '" y="' + f1(oy - (R0 + 16) * Math.sin(e / 2) + 4) + '" text-anchor="middle" style="fill:' + col + '">' + lbl + "</text>";
      }
      g += arcAt(X(pA), a, pA < 0 ? 1 : -1, COL.cos, "α") + arcAt(X(pB), b, pB < 0 ? 1 : -1, COL.r, "β");
      g += '<text class="lb it" x="' + X(pA) + '" y="' + (oy + 18) + '" text-anchor="middle">A</text><text class="lb it" x="' + X(pB) + '" y="' + (oy + 18) + '" text-anchor="middle">B</text>';
      g += '<text class="lb it" x="' + X(0) + '" y="' + (Y(r.h) - 8) + '" text-anchor="middle">M</text><text class="lb it" x="' + X(0) + '" y="' + (oy + 18) + '" text-anchor="middle">H</text>';
      g += '<text class="lb it" x="' + (mode === "s" ? +X(0) + 12 : X(0) - 12) + '" y="' + f1((oy + +Y(r.h)) / 2) + '" text-anchor="middle">h</text>';
      g += '<text class="lb it" x="' + f1((+X(pA) + +X(0)) / 2) + '" y="' + (oy - 6) + '" text-anchor="middle" style="fill:var(--muted)">x</text>';
      g += '<text class="lb" x="' + f1((+X(pA) + +X(pB)) / 2) + '" y="' + (oy + 32) + '" text-anchor="middle" style="fill:var(--muted)">' + (mode === "s" ? "AB = " : "AB = ") + decS(d, 2) + "</text>";
      svg.innerHTML = g;
    }
    [M].forEach(function (el) { el.addEventListener("change", draw); }); [IA, IB, ID].forEach(function (el) { el.addEventListener("input", draw); }); onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("L'angle de $135^\\circ$ en radians és…", "El ángulo de $135^\\circ$ en radianes es…", "$135^\\circ$ in radians is…"),
      o: [q3("$\\frac{3\\pi}{4}$"), q3("$\\frac{4\\pi}{3}$"), q3("$\\frac{2\\pi}{3}$")], a: 0, e: q3("$135\\cdot\\frac{\\pi}{180}=\\frac{3\\pi}{4}$.") },
    { q: q3("L'angle de $\\frac{5\\pi}{6}$ rad en graus és…", "El ángulo de $\\frac{5\\pi}{6}$ rad en grados es…", "$\\frac{5\\pi}{6}$ rad in degrees is…"),
      o: [q3("$150^\\circ$"), q3("$300^\\circ$"), q3("$120^\\circ$")], a: 0, e: q3("$\\frac{5\\pi}{6}\\cdot\\frac{180^\\circ}{\\pi}=5\\cdot30^\\circ=150^\\circ$.") },
    { q: q3("En un triangle rectangle, el catet oposat a $\\alpha$ mesura 6 i la hipotenusa 10. Aleshores $\\tan\\alpha$ val…", "En un triángulo rectángulo, el cateto opuesto a $\\alpha$ mide 6 y la hipotenusa 10. Entonces $\\tan\\alpha$ vale…", "In a right triangle the leg opposite $\\alpha$ is 6 and the hypotenuse 10. Then $\\tan\\alpha$ is…"),
      o: [q3("$\\frac35$"), q3("$\\frac34$"), q3("$\\frac43$")], a: 1, e: q3("El catet contigu és $\\sqrt{100-36}=8$: $\\tan\\alpha=\\frac68=\\frac34$.", "El cateto contiguo es $\\sqrt{100-36}=8$: $\\tan\\alpha=\\frac68=\\frac34$.", "The adjacent leg is $\\sqrt{100-36}=8$: $\\tan\\alpha=\\frac68=\\frac34$.") },
    { q: q3("$\\cos60^\\circ$ val…", "$\\cos60^\\circ$ vale…", "$\\cos60^\\circ$ equals…"),
      o: [q3("$\\frac{\\sqrt3}{2}$"), q3("$\\frac12$"), q3("$\\sqrt3$")], a: 1, e: q3("És la meitat del costat d'un triangle equilàter dividida pel costat: $\\frac12$.", "Es la mitad del lado de un triángulo equilátero dividida por el lado: $\\frac12$.", "Half the side of an equilateral triangle over the side: $\\frac12$.") },
    { q: q3("Si $\\alpha$ és agut i $\\sin\\alpha=\\frac45$, aleshores $\\cos\\alpha$ val…", "Si $\\alpha$ es agudo y $\\sin\\alpha=\\frac45$, entonces $\\cos\\alpha$ vale…", "If $\\alpha$ is acute and $\\sin\\alpha=\\frac45$, then $\\cos\\alpha$ is…"),
      o: [q3("$\\frac15$"), q3("$\\frac35$"), q3("$\\frac54$")], a: 1, e: q3("$\\sqrt{1-\\frac{16}{25}}=\\frac35$.") },
    { q: q3("Hi ha algun angle amb $\\sin\\alpha=\\frac12$ i $\\cos\\alpha=\\frac12$?", "¿Hay algún ángulo con $\\sin\\alpha=\\frac12$ y $\\cos\\alpha=\\frac12$?", "Is there an angle with $\\sin\\alpha=\\frac12$ and $\\cos\\alpha=\\frac12$?"),
      o: [q3("Sí, $45^\\circ$", "Sí, $45^\\circ$", "Yes, $45^\\circ$"), q3("Sí, $30^\\circ$", "Sí, $30^\\circ$", "Yes, $30^\\circ$"), q3("No", "No", "No")], a: 2, e: q3("$\\frac14+\\frac14=\\frac12\\neq1$: no es compleix la relació fonamental.", "$\\frac14+\\frac14=\\frac12\\neq1$: no se cumple la relación fundamental.", "$\\frac14+\\frac14=\\frac12\\neq1$: the fundamental identity fails.") },
    { q: q3("Si $\\tan\\alpha=1$ i $\\alpha$ és agut, aleshores…", "Si $\\tan\\alpha=1$ y $\\alpha$ es agudo, entonces…", "If $\\tan\\alpha=1$ and $\\alpha$ is acute, then…"),
      o: [q3("$\\alpha=45^\\circ$"), q3("$\\alpha=60^\\circ$"), q3("$\\alpha=90^\\circ$")], a: 0, e: q3("Els dos catets són iguals: és la meitat d'un quadrat.", "Los dos catetos son iguales: es la mitad de un cuadrado.", "Both legs are equal: it is half a square.") },
    { q: q3("En un triangle rectangle en $C$, $c=10$ i $\\hat A=30^\\circ$. El catet $a$ mesura…", "En un triángulo rectángulo en $C$, $c=10$ y $\\hat A=30^\\circ$. El cateto $a$ mide…", "In a triangle right-angled at $C$, $c=10$ and $\\hat A=30^\\circ$. The leg $a$ is…"),
      o: [q3("$5$"), q3("$5\\sqrt3$"), q3("$20$")], a: 0, e: q3("$a=c\\sin\\hat A=10\\cdot\\frac12=5$.") },
    { q: q3("Una torre de 20 m fa una ombra de 20 m. Amb quin angle arriben els raigs del Sol?", "Una torre de 20 m da una sombra de 20 m. ¿Con qué ángulo llegan los rayos del Sol?", "A 20 m tower casts a 20 m shadow. At what angle do the sun's rays arrive?"),
      o: [q3("$30^\\circ$"), q3("$45^\\circ$"), q3("$60^\\circ$")], a: 1, e: q3("$\\tan\\alpha=\\frac{20}{20}=1\\Rightarrow\\alpha=45^\\circ$.") },
    { q: q3("En quin quadrant és $\\sin\\alpha\\lt0$ i $\\cos\\alpha\\gt0$?", "¿En qué cuadrante es $\\sin\\alpha\\lt0$ y $\\cos\\alpha\\gt0$?", "In which quadrant is $\\sin\\alpha\\lt0$ and $\\cos\\alpha\\gt0$?"),
      o: [q3("II"), q3("III"), q3("IV")], a: 2, e: q3("En el quart quadrant el punt $P$ té abscissa positiva i ordenada negativa.", "En el cuarto cuadrante el punto $P$ tiene abscisa positiva y ordenada negativa.", "In the fourth quadrant $P$ has a positive $x$ and a negative $y$.") },
    { q: q3("$\\cos 240^\\circ$ val…", "$\\cos 240^\\circ$ vale…", "$\\cos 240^\\circ$ equals…"),
      o: [q3("$-\\frac12$"), q3("$\\frac12$"), q3("$-\\frac{\\sqrt3}{2}$")], a: 0, e: q3("$240^\\circ=180^\\circ+60^\\circ$: $\\cos240^\\circ=-\\cos60^\\circ=-\\frac12$.") },
    { q: q3("$\\sin 390^\\circ$ val…", "$\\sin 390^\\circ$ vale…", "$\\sin 390^\\circ$ equals…"),
      o: [q3("$\\frac{\\sqrt3}{2}$"), q3("$-\\frac12$"), q3("$\\frac12$")], a: 2, e: q3("$390^\\circ=360^\\circ+30^\\circ$: $\\sin390^\\circ=\\sin30^\\circ=\\frac12$.") },
    { q: q3("$\\sin(180^\\circ-\\alpha)$ és igual a…", "$\\sin(180^\\circ-\\alpha)$ es igual a…", "$\\sin(180^\\circ-\\alpha)$ equals…"),
      o: [q3("$\\sin\\alpha$"), q3("$-\\sin\\alpha$"), q3("$\\cos\\alpha$")], a: 0, e: q3("Els angles suplementaris tenen el mateix sinus (simetria respecte de l'eix $OY$).", "Los ángulos suplementarios tienen el mismo seno (simetría respecto del eje $OY$).", "Supplementary angles have the same sine (symmetry in the $y$-axis).") },
    { q: q3("$\\tan(-30^\\circ)$ val…", "$\\tan(-30^\\circ)$ vale…", "$\\tan(-30^\\circ)$ equals…"),
      o: [q3("$\\frac{\\sqrt3}{3}$"), q3("$-\\frac{\\sqrt3}{3}$"), q3("$-\\sqrt3$")], a: 1, e: q3("Els angles oposats tenen tangents oposades: $-\\tan30^\\circ=-\\frac{\\sqrt3}{3}$.", "Los ángulos opuestos tienen tangentes opuestas: $-\\tan30^\\circ=-\\frac{\\sqrt3}{3}$.", "Opposite angles have opposite tangents: $-\\tan30^\\circ=-\\frac{\\sqrt3}{3}$.") }
  ];
  /*@@GENERIC@@*/
  var TITLES = { va: "Trigonometria · FentMates", es: "Trigonometría · FentMates", en: "Trigonometry · FentMates" };
  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l; root.setAttribute("data-lang", l); root.lang = HTML_LANG[l]; document.title = TITLES[l]; store("lang", l);
    try { var url = new URL(location.href); if (url.searchParams.has("lang")) { url.searchParams.set("lang", l); history.replaceState(null, "", url); } } catch (e) {}
    refreshers.forEach(function (fn) { fn(); });
  }

  function init() {
    document.title = TITLES[lang];
    var Dl = [{ left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }];
    if (window.renderMathInElement) {
      window.renderMathInElement(document.body, { delimiters: Dl, ignoredClasses: ["widget", "lab"], throwOnError: false });
      document.querySelectorAll(".widget .wt, .widget label, .widget .legend, .widget > p").forEach(function (el) { window.renderMathInElement(el, { delimiters: Dl, throwOnError: false }); });
    }
    var all = [wChrome, wSteps, wNav, wRad, wRt, wChk, wRect, wDob, wCirc, wFind, wRed, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM45 = { exact: exact, parseVal: parseVal, sT: sT, chkPair: chkPair, dob: dob };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
