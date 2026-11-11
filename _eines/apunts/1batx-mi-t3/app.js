(function () {
  "use strict";
  var root = document.documentElement;
  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca-ES-valencia", es: "es", en: "en" };
  var UNIT_KEY = "fm-1batx-mi-u3-done";

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

  /* ---------- gràfiques cartesianes ---------- */
  function gview(o) {
    var W = o.W || 360, H = o.H || 260, pl = o.pl || 30, pr = 10, pt = 10, pb = 22;
    function X(x) { return pl + (x - o.x0) / (o.x1 - o.x0) * (W - pl - pr); }
    function Y(y) { return H - pb - (y - o.y0) / (o.y1 - o.y0) * (H - pt - pb); }
    var g = "", v;
    (o.xt || []).forEach(function (t) { g += '<line class="g" x1="' + f1(X(t[0])) + '" x2="' + f1(X(t[0])) + '" y1="' + Y(o.y0) + '" y2="' + Y(o.y1) + '"/>'; });
    for (v = Math.ceil(o.y0 / o.sy) * o.sy; v <= o.y1 + 1e-9; v += o.sy) g += '<line class="g" x1="' + X(o.x0) + '" x2="' + X(o.x1) + '" y1="' + f1(Y(v)) + '" y2="' + f1(Y(v)) + '"/>';
    var ay = Math.max(o.y0, Math.min(o.y1, 0)), ax = Math.max(o.x0, Math.min(o.x1, 0));
    g += '<line class="ax" x1="' + X(o.x0) + '" x2="' + X(o.x1) + '" y1="' + f1(Y(ay)) + '" y2="' + f1(Y(ay)) + '"/><line class="ax" x1="' + f1(X(ax)) + '" x2="' + f1(X(ax)) + '" y1="' + Y(o.y0) + '" y2="' + Y(o.y1) + '"/>';
    (o.xt || []).forEach(function (t) { if (t[1]) g += '<text x="' + f1(X(t[0])) + '" y="' + f1(Math.min(H - 4, Y(ay) + 13)) + '" text-anchor="middle">' + t[1] + "</text>"; });
    for (v = Math.ceil(o.y0 / o.sy) * o.sy; v <= o.y1 + 1e-9; v += o.sy) if (Math.abs(v) > 1e-9) g += '<text x="' + f1(X(ax) - 4) + '" y="' + f1(Y(v) + 3.5) + '" text-anchor="end">' + String(+v.toFixed(3)).replace("-", "−").replace(".", lang === "en" ? "." : ",") + "</text>";
    var id = "cl" + Math.random().toString(36).slice(2, 8);
    var clip = '<defs><clipPath id="' + id + '"><rect x="' + X(o.x0) + '" y="' + Y(o.y1) + '" width="' + (X(o.x1) - X(o.x0)) + '" height="' + (Y(o.y0) - Y(o.y1)) + '"/></clipPath></defs>';
    return { g: g + clip, X: X, Y: Y, o: o, open: '<g clip-path="url(#' + id + ')">', close: "</g>" };
  }
  // corba de f; es talla on la funció salta (asímptotes)
  function curve(G, f, color, opts) {
    opts = opts || {};
    var o = G.o, a = opts.a == null ? o.x0 : opts.a, b = opts.b == null ? o.x1 : opts.b, N = opts.n || 600, d = "", pen = false, M = (o.y1 - o.y0), py = null;
    for (var i = 0; i <= N; i++) {
      var x = a + (b - a) * i / N, y = f(x);
      if (!isFinite(y) || Math.abs(y) > 1e6) { pen = false; py = null; continue; }
      if (py != null && Math.abs(y - py) > M * 1.5) pen = false;
      py = y; y = Math.max(o.y0 - M, Math.min(o.y1 + M, y));
      d += (pen ? "L" : "M") + G.X(x).toFixed(1) + " " + G.Y(y).toFixed(1); pen = true;
    }
    return '<path class="cv" d="' + d + '" style="stroke:' + color + (opts.w ? ";stroke-width:" + opts.w : "") + '"' + (opts.dash ? ' stroke-dasharray="' + opts.dash + '"' : "") + "/>";
  }
  function gdot(G, x, y, col, r) { return '<circle class="pt" cx="' + f1(G.X(x)) + '" cy="' + f1(G.Y(y)) + '" r="' + (r || 5) + '" style="fill:' + col + '"/>'; }
  function piTicks(x0, x1, step) { // marques en múltiples de π·step
    var out = [], k;
    for (k = Math.ceil(x0 / (Math.PI * step) - 1e-9); k * Math.PI * step <= x1 + 1e-9; k++) {
      var f = Fr(k * Math.round(step * 4), 4), s = f.n === 0 ? "" : (f.n < 0 ? "−" : "") + (Math.abs(f.n) === 1 ? "" : Math.abs(f.n)) + "π" + (f.d > 1 ? "/" + f.d : "");
      out.push([k * Math.PI * step, s]);
    }
    return out;
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

  /* ---------- 3.1 radians ---------- */
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

  /* ---------- 3.2 triangle rectangle ---------- */
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

  /* ---------- 3.3 circumferència goniomètrica ---------- */
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
        [t3("Recíproques", "Recíprocas", "Reciprocals"), tex("\\sec\\alpha=" + (c ? val(ex && ex.sec, 1 / c) : "\\nexists") + ",\\ \\ \\text{cosec}\\,\\alpha=" + (s ? val(ex && ex.csc, 1 / s) : "\\nexists") + ",\\ \\ \\text{cotg}\\,\\alpha=" + (s ? val(ex && ex.cot, c / s) : "\\nexists"))],
        [t3("Signes", "Signos", "Signs"), q ? tex("\\sin" + (s > 0 ? "+" : "-") + ",\\ \\cos" + (c > 0 ? "+" : "-") + ",\\ \\tan" + (s * c > 0 ? "+" : "-")) : "—"]
      ];
      info.innerHTML = kv(rows);
    }
    snap.addEventListener("change", draw); onLang(draw);
  }

  /* ---------- 3.3 raons a partir d'una ---------- */
  function wFind() {
    var w = byId("w-find"); if (!w) return;
    var info = w.querySelector(".info"), R = $(w, "r"), V = $(w, "v"), QS = $(w, "q");
    var PRE = [["sin", "0.62", 2], ["cos", "-0.83", 3], ["tan", "-0.92", 4], ["cos", "sqrt5/3", 1], ["sec", "4", 4], ["cot", "-1/2", 2], ["sin", "3/5", 2]];
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
      var rec = [];
      if (r !== "sec") rec.push("\\sec\\alpha=" + (Math.abs(cv) < 1e-12 ? "\\nexists" : T(O.inv(c))));
      if (r !== "csc") rec.push("\\text{cosec}\\,\\alpha=" + (Math.abs(sv) < 1e-12 ? "\\nexists" : T(O.inv(s))));
      if (r !== "cot") rec.push("\\text{cotg}\\,\\alpha=" + (Math.abs(sv) < 1e-12 ? "\\nexists" : T(O.div(c, s))));
      steps.push(tex(rec.join(",\\quad ")));
      var ang = deg(Math.atan2(sv, cv)); if (ang < 0) ang += 360;
      steps.push(t3("Amb la calculadora: ", "Con la calculadora: ", "With a calculator: ") + tex("\\alpha" + (Math.abs(ang - Math.round(ang)) < 1e-6 ? "=" + Math.round(ang) + "^\\circ" : "\\approx " + dmsT(ang))));
      info.innerHTML = "<ol>" + steps.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ol>";
    }
    [R, QS].forEach(function (el) { el.addEventListener("change", draw); }); V.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 3.4 reducció al primer quadrant ---------- */
  function wRed() {
    var w = byId("w-red"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), B = $(w, "b");
    var C = UC(svg, { W: 320, R: 105 });
    var PRE = ["150", "225", "300", "1680", "-330", "3825", "-1710", "117"];
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

  /* ---------- 3.5 triangles rectangles ---------- */
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

  /* ---------- 3.6 laboratori del triangle ---------- */
  function wLab() {
    var w = byId("w-lab"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), r = 8, Sz = 360, pad = 16, k = (Sz - 2 * pad) / (2 * r);
    var pts = { A: [-5, -3], B: [5, -3], C: [1, 4] }, drag = null;
    function X(x) { return pad + (x + r) * k; }
    function Y(y) { return pad + (r - y) * k; }
    var base = "", i;
    for (i = -r; i <= r; i++) base += '<line class="g" x1="' + X(i) + '" y1="' + Y(-r) + '" x2="' + X(i) + '" y2="' + Y(r) + '"/><line class="g" x1="' + X(-r) + '" y1="' + Y(i) + '" x2="' + X(r) + '" y2="' + Y(i) + '"/>';
    base += '<line class="ax" x1="' + X(-r) + '" y1="' + Y(0) + '" x2="' + X(r) + '" y2="' + Y(0) + '"/><line class="ax" x1="' + X(0) + '" y1="' + Y(-r) + '" x2="' + X(0) + '" y2="' + Y(r) + '"/>';
    function d2(p, q) { return (p[0] - q[0]) * (p[0] - q[0]) + (p[1] - q[1]) * (p[1] - q[1]); }
    function ang(P, Q, R) { var u = [Q[0] - P[0], Q[1] - P[1]], v = [R[0] - P[0], R[1] - P[1]]; return deg(Math.acos((u[0] * v[0] + u[1] * v[1]) / Math.sqrt((u[0] * u[0] + u[1] * u[1]) * (v[0] * v[0] + v[1] * v[1])))); }
    function draw() {
      var A = pts.A, B = pts.B, C = pts.C, det = (B[0] - A[0]) * (C[1] - A[1]) - (B[1] - A[1]) * (C[0] - A[0]), h = "";
      if (det) {
        // circumcentre
        var D = 2 * (A[0] * (B[1] - C[1]) + B[0] * (C[1] - A[1]) + C[0] * (A[1] - B[1]));
        var ux = ((A[0] * A[0] + A[1] * A[1]) * (B[1] - C[1]) + (B[0] * B[0] + B[1] * B[1]) * (C[1] - A[1]) + (C[0] * C[0] + C[1] * C[1]) * (A[1] - B[1])) / D;
        var uy = ((A[0] * A[0] + A[1] * A[1]) * (C[0] - B[0]) + (B[0] * B[0] + B[1] * B[1]) * (A[0] - C[0]) + (C[0] * C[0] + C[1] * C[1]) * (B[0] - A[0])) / D;
        var R = Math.sqrt(d2([ux, uy], A));
        h += '<circle cx="' + f1(X(ux)) + '" cy="' + f1(Y(uy)) + '" r="' + f1(R * k) + '" class="arc" style="stroke:' + COL.ang + ';stroke-dasharray:3 4"/>';
        h += '<circle class="pt" cx="' + f1(X(ux)) + '" cy="' + f1(Y(uy)) + '" r="3.5" style="fill:' + COL.ang + '"/>';
      }
      h += '<path class="tri" d="M' + X(A[0]) + " " + Y(A[1]) + "L" + X(B[0]) + " " + Y(B[1]) + "L" + X(C[0]) + " " + Y(C[1]) + 'Z"/>';
      var g = [(A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3];
      [["a", B, C], ["b", A, C], ["c", A, B]].forEach(function (s) { var m = [(s[1][0] + s[2][0]) / 2, (s[1][1] + s[2][1]) / 2], dx = m[0] - g[0], dy = m[1] - g[1], dd = Math.hypot(dx, dy) || 1; h += '<text class="lb it" x="' + f1(X(m[0]) + dx / dd * 13) + '" y="' + f1(Y(m[1]) - dy / dd * 13 + 5) + '" text-anchor="middle" style="fill:var(--muted)">' + s[0] + "</text>"; });
      ["A", "B", "C"].forEach(function (key) { var p = pts[key], dx = p[0] - g[0], dy = p[1] - g[1], dd = Math.hypot(dx, dy) || 1;
        h += '<circle class="halo" data-id="' + key + '" cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="17"/><circle class="pt drag" data-id="' + key + '" cx="' + X(p[0]) + '" cy="' + Y(p[1]) + '" r="6.5" style="fill:' + COL.r + '"/>';
        h += '<text class="lb it" x="' + f1(X(p[0]) + dx / dd * 18) + '" y="' + f1(Y(p[1]) - dy / dd * 18 + 5) + '" text-anchor="middle">' + key + "</text>"; });
      svg.innerHTML = base + h;
      if (!det) { info.innerHTML = t3("Els tres punts estan alineats: no hi ha triangle.", "Los tres puntos están alineados: no hay triángulo.", "The three points are collinear: there is no triangle."); return; }
      var a = Math.sqrt(d2(B, C)), b = Math.sqrt(d2(A, C)), c = Math.sqrt(d2(A, B)), aA = ang(A, B, C), aB = ang(B, A, C), aC = 180 - aA - aB;
      function q(s, x, An, y) { return tex("{\\dfrac{" + s + "}{\\sin\\hat " + An + "}=\\dfrac{" + dT(x, 2) + "}{\\sin " + dmsT(y) + "}\\approx " + dT(x / Math.sin(rad(y)), 3) + "}"); }
      var big = Math.max(a, b, c), other = a * a + b * b + c * c - big * big, typ = Math.abs(big * big - other) < 1e-9 ? t3("rectangle", "rectángulo", "right-angled") : big * big > other ? t3("obtusangle", "obtusángulo", "obtuse") : t3("acutangle", "acutángulo", "acute");
      info.innerHTML = kv([
        [t3("Costats", "Lados", "Sides"), tex("a\\approx " + dT(a, 2) + ",\\ b\\approx " + dT(b, 2) + ",\\ c\\approx " + dT(c, 2))],
        [t3("Angles", "Ángulos", "Angles"), tex("\\hat A\\approx " + dmsT(aA) + ",\\ \\hat B\\approx " + dmsT(aB) + ",\\ \\hat C\\approx " + dmsT(aC)) + small(t3("Triangle ", "Triángulo ", "") + typ + (lang === "en" ? " triangle" : ""))],
        [t3("Teorema del sinus", "Teorema del seno", "Sine rule"), q("a", a, "A", aA) + " &nbsp; " + q("b", b, "B", aB) + " &nbsp; " + q("c", c, "C", aC)],
        [cdot(COL.ang) + t3("Circumferència circumscrita", "Circunferencia circunscrita", "Circumcircle"), tex("2R\\approx " + dT(a / Math.sin(rad(aA)), 3))],
        [t3("Teorema del cosinus", "Teorema del coseno", "Cosine rule"), tex("b^2+c^2-2bc\\cos\\hat A\\approx " + dT(b * b + c * c - 2 * b * c * Math.cos(rad(aA)), 2) + "=a^2")],
        [t3("Àrea", "Área", "Area"), tex("S=\\tfrac12\\,bc\\sin\\hat A\\approx " + dT(0.5 * b * c * Math.sin(rad(aA)), 2) + "\\ \\text{u}^2")]
      ]);
    }
    svg.addEventListener("pointerdown", function (e) { var t = e.target.closest ? e.target.closest("[data-id]") : null; if (!t) return; drag = t.getAttribute("data-id"); svg.classList.add("dragging"); try { svg.setPointerCapture(e.pointerId); } catch (_) {} e.preventDefault(); });
    svg.addEventListener("pointermove", function (e) {
      if (!drag) return; var q = svgPt(svg, e); if (!q) return;
      var p = [Math.max(-r, Math.min(r, Math.round((q.x - pad) / k - r))), Math.max(-r, Math.min(r, Math.round(r - (q.y - pad) / k)))], c = pts[drag];
      if (c[0] === p[0] && c[1] === p[1]) return;
      if (Object.keys(pts).some(function (j) { return j !== drag && pts[j][0] === p[0] && pts[j][1] === p[1]; })) return;
      pts[drag] = p; draw();
    });
    function up() { drag = null; svg.classList.remove("dragging"); }
    svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
    onLang(draw);
  }

  /* ---------- 3.7 resolució de triangles ---------- */
  function wTri() {
    var w = byId("w-tri"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), ins = $(w, "ins"), mode = 0, res = null, st;
    var MODES = [
      { k: ["a", "b", "c"], v: ["10", "14", "8"], lab: function () { return t3("Tres costats", "Tres lados", "Three sides"); } },
      { k: ["b", "c", "A"], v: ["6", "9", "39 12"], lab: function () { return t3("Dos costats i l'angle comprés", "Dos lados y el ángulo comprendido", "Two sides and the included angle"); } },
      { k: ["a", "B", "C"], v: ["7", "38 49", "66 40"], lab: function () { return t3("Un costat i dos angles", "Un lado y dos ángulos", "One side and two angles"); } },
      { k: ["a", "b", "A"], v: ["8", "10", "36 38"], lab: function () { return t3("Dos costats i un angle oposat", "Dos lados y un ángulo opuesto", "Two sides and an opposite angle"); } }
    ];
    var vals = MODES.map(function (m) { return m.v.slice(); });
    function build() {
      var m = MODES[mode];
      ins.innerHTML = m.k.map(function (k, i) { var isA = k === k.toUpperCase(); return '<label>' + tex(isA ? "\\hat " + k + "=" : k + "=") + ' <input class="tin s" data-k="' + i + '" value="' + vals[mode][i] + '" autocomplete="off">' + (isA ? "°" : "") + "</label>"; }).join("");
      ins.querySelectorAll("input").forEach(function (el) { el.addEventListener("input", function () { vals[mode][+el.getAttribute("data-k")] = el.value; solve(); }); });
      solve();
    }
    presetBtns($(w, "mode"), function () { return MODES.map(function (m) { return m.lab(); }); }, function (i) { mode = i; build(); }, 0);
    function S2(x) { return dT(x, 2); }
    function solve() {
      var m = MODES[mode], v = [], bad = false;
      ins.querySelectorAll("input").forEach(function (el, i) { var isA = m.k[i] === m.k[i].toUpperCase(), x = isA ? parseAng(el.value) : parseNum(el.value), ok = x != null && x > 0 && (!isA || x < 180); el.classList.toggle("bad", !ok); if (!ok) bad = true; v.push(x); });
      var steps = [], sols = [];
      if (bad) { res = { steps: [t3("Revisa les dades: costats positius i angles entre 0° i 180°.", "Revisa los datos: lados positivos y ángulos entre 0° y 180°.", "Check the data: positive sides and angles between 0° and 180°.")], sols: [] }; st.reset(1); return; }
      var a, b, c, A, B, C, s1;
      if (mode === 0) {
        a = v[0]; b = v[1]; c = v[2];
        var mx = Math.max(a, b, c);
        if (mx >= a + b + c - mx) steps.push(t3("No hi ha triangle: el costat més llarg (", "No hay triángulo: el lado más largo (", "No triangle: the longest side (") + tex(S2(mx)) + t3(") no és menor que la suma dels altres dos.", ") no es menor que la suma de los otros dos.", ") is not less than the sum of the other two."));
        else {
          A = deg(Math.acos((b * b + c * c - a * a) / (2 * b * c))); B = deg(Math.acos((a * a + c * c - b * b) / (2 * a * c))); C = 180 - A - B;
          steps.push(t3("Teorema del cosinus per a ", "Teorema del coseno para ", "Cosine rule for ") + tex("\\hat A") + ": " + tex("\\cos\\hat A=\\dfrac{b^2+c^2-a^2}{2bc}=\\dfrac{" + S2(b) + "^2+" + S2(c) + "^2-" + S2(a) + "^2}{2\\cdot" + S2(b) + "\\cdot" + S2(c) + "}\\approx " + dT(Math.cos(rad(A)), 4) + "\\Rightarrow\\hat A\\approx " + dmsT(A)));
          steps.push(t3("Igual per a ", "Igual para ", "Likewise for ") + tex("\\hat B") + ": " + tex("\\cos\\hat B=\\dfrac{a^2+c^2-b^2}{2ac}\\approx " + dT(Math.cos(rad(B)), 4) + "\\Rightarrow\\hat B\\approx " + dmsT(B)));
          steps.push(tex("\\hat C=180^\\circ-\\hat A-\\hat B\\approx " + dmsT(C)));
          sols.push({ a: a, b: b, c: c, A: A, B: B, C: C });
        }
      } else if (mode === 1) {
        b = v[0]; c = v[1]; A = v[2];
        a = Math.sqrt(b * b + c * c - 2 * b * c * Math.cos(rad(A)));
        steps.push(t3("Teorema del cosinus: ", "Teorema del coseno: ", "Cosine rule: ") + tex("a^2=b^2+c^2-2bc\\cos\\hat A=" + S2(b) + "^2+" + S2(c) + "^2-2\\cdot" + S2(b) + "\\cdot" + S2(c) + "\\cdot\\cos " + dmsT(A) + "\\Rightarrow a\\approx " + S2(a)));
        B = deg(Math.acos((a * a + c * c - b * b) / (2 * a * c))); C = 180 - A - B;
        steps.push(t3("Un altre angle, amb el cosinus (així no hi ha ambigüitat): ", "Otro ángulo, con el coseno (así no hay ambigüedad): ", "Another angle, with the cosine (no ambiguity this way): ") + tex("\\cos\\hat B=\\dfrac{a^2+c^2-b^2}{2ac}\\approx " + dT(Math.cos(rad(B)), 4) + "\\Rightarrow\\hat B\\approx " + dmsT(B)));
        steps.push(tex("\\hat C=180^\\circ-\\hat A-\\hat B\\approx " + dmsT(C)));
        sols.push({ a: a, b: b, c: c, A: A, B: B, C: C });
      } else if (mode === 2) {
        a = v[0]; B = v[1]; C = v[2]; A = 180 - B - C;
        if (A <= 1e-9) steps.push(t3("No hi ha triangle: ", "No hay triángulo: ", "No triangle: ") + tex("\\hat B+\\hat C\\ge180^\\circ"));
        else {
          steps.push(tex("\\hat A=180^\\circ-\\hat B-\\hat C=" + dmsT(A)));
          b = a * Math.sin(rad(B)) / Math.sin(rad(A)); c = a * Math.sin(rad(C)) / Math.sin(rad(A));
          steps.push(t3("Teorema del sinus: ", "Teorema del seno: ", "Sine rule: ") + tex("\\dfrac{b}{\\sin\\hat B}=\\dfrac{a}{\\sin\\hat A}\\Rightarrow b=\\dfrac{" + S2(a) + "\\cdot\\sin " + dmsT(B) + "}{\\sin " + dmsT(A) + "}\\approx " + S2(b)));
          steps.push(tex("c=\\dfrac{a\\cdot\\sin\\hat C}{\\sin\\hat A}=\\dfrac{" + S2(a) + "\\cdot\\sin " + dmsT(C) + "}{\\sin " + dmsT(A) + "}\\approx " + S2(c)));
          sols.push({ a: a, b: b, c: c, A: A, B: B, C: C });
        }
      } else {
        a = v[0]; b = v[1]; A = v[2];
        var sB = b * Math.sin(rad(A)) / a;
        steps.push(t3("Teorema del sinus: ", "Teorema del seno: ", "Sine rule: ") + tex("\\dfrac{a}{\\sin\\hat A}=\\dfrac{b}{\\sin\\hat B}\\Rightarrow\\sin\\hat B=\\dfrac{" + S2(b) + "\\cdot\\sin " + dmsT(A) + "}{" + S2(a) + "}\\approx " + dT(sB, 4)));
        if (sB > 1 + 1e-12) steps.push(t3("Un sinus no pot ser major que 1: <strong>no hi ha cap triangle</strong>.", "Un seno no puede ser mayor que 1: <strong>no hay ningún triángulo</strong>.", "A sine cannot exceed 1: <strong>there is no triangle</strong>."));
        else {
          var B1 = deg(Math.asin(Math.min(1, sB))), B2 = 180 - B1, cand = Math.abs(B1 - 90) < 1e-9 ? [B1] : [B1, B2];
          steps.push(cand.length === 1 ? tex("\\hat B=90^\\circ") : t3("Dos angles possibles: ", "Dos ángulos posibles: ", "Two possible angles: ") + tex("\\hat B_1\\approx " + dmsT(B1) + ",\\ \\ \\hat B_2=180^\\circ-\\hat B_1\\approx " + dmsT(B2)));
          var okc = cand.filter(function (x) { return A + x < 180 - 1e-9; });
          if (cand.length === 2) steps.push(okc.length === 2 ? t3("Tots dos valen, perquè ", "Los dos valen, porque ", "Both are valid, since ") + tex("\\hat A+\\hat B_2\\approx " + dmsT(A + B2) + "\\lt180^\\circ") + t3(": hi ha <strong>dos triangles</strong>.", ": hay <strong>dos triángulos</strong>.", ": there are <strong>two triangles</strong>.")
            : okc.length === 1 ? t3("El segon no val, perquè ", "El segundo no vale, porque ", "The second is not valid, since ") + tex("\\hat A+\\hat B_2\\approx " + dmsT(A + B2) + "\\ge180^\\circ") + t3(": hi ha un sol triangle.", ": hay un solo triángulo.", ": there is a single triangle.") : t3("Cap no val: no hi ha triangle.", "Ninguno vale: no hay triángulo.", "Neither is valid: there is no triangle."));
          okc.forEach(function (Bx, i) {
            var Cx = 180 - A - Bx, cx = a * Math.sin(rad(Cx)) / Math.sin(rad(A)), sub = okc.length > 1 ? "_" + (i + 1) : "";
            steps.push(tex("\\hat C" + sub + "=180^\\circ-\\hat A-\\hat B" + sub + "\\approx " + dmsT(Cx) + ",\\quad c" + sub + "=\\dfrac{a\\cdot\\sin\\hat C" + sub + "}{\\sin\\hat A}\\approx " + S2(cx)));
            sols.push({ a: a, b: b, c: cx, A: A, B: Bx, C: Cx });
          });
        }
      }
      sols.forEach(function (s, i) {
        steps.push("<strong>" + (sols.length > 1 ? t3("Solució ", "Solución ", "Solution ") + (i + 1) : t3("Solució", "Solución", "Solution")) + ":</strong> " + tex("a\\approx " + S2(s.a) + ",\\ b\\approx " + S2(s.b) + ",\\ c\\approx " + S2(s.c) + ";\\ \\ \\hat A\\approx " + dmsT(s.A) + ",\\ \\hat B\\approx " + dmsT(s.B) + ",\\ \\hat C\\approx " + dmsT(s.C)) + small(t3("Àrea: ", "Área: ", "Area: ") + tex("S=\\tfrac12\\,bc\\sin\\hat A\\approx " + S2(0.5 * s.b * s.c * Math.sin(rad(s.A))))));
      });
      res = { steps: steps, sols: sols }; st.reset(1);
    }
    function show(k) {
      if (!res) return;
      info.innerHTML = "<ol>" + res.steps.slice(0, k).map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ol>";
      if (!res.sols.length) { svg.innerHTML = ""; return; }
      var T = res.sols.map(function (s) { return triFrom(s.a, s.b, s.c, s.A); });
      if (T.length > 1) { T[1].A = T[0].A; T[1].C = T[0].C; }
      triSvg(svg, T, 360, 260);
    }
    st = stepper(w, function () { return res ? res.steps.length : 0; }, show);
    build();
  }

  /* ---------- 3.8 fórmules de la suma ---------- */
  function wSum() {
    var w = byId("w-sum"); if (!w) return;
    var info = w.querySelector(".info"), SA = $(w, "a"), SB = $(w, "b"), OP = $(w, "op");
    var ANG = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330];
    [SA, SB].forEach(function (s) { s.innerHTML = ANG.map(function (a) { return '<option value="' + a + '">' + a + "°</option>"; }).join(""); });
    SA.value = "45"; SB.value = "30";
    var PRE = [[45, 1, 30], [45, -1, 30], [60, 1, 45], [135, 1, 30], [225, 1, 30], [60, -1, 45], [30, 1, 30]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { return tex((p[0] + p[1] * p[2]) + "^\\circ=" + p[0] + "^\\circ" + (p[1] > 0 ? "+" : "-") + p[2] + "^\\circ"); }); },
      function (i) { SA.value = PRE[i][0]; OP.value = PRE[i][1]; SB.value = PRE[i][2]; draw(); }, 0);
    function P(x) { var s = qT(x); return /[+-]/.test(s.replace(/^-/, "")) || s.charAt(0) === "-" ? "\\left(" + s + "\\right)" : s; }
    function draw() {
      var a = +SA.value, b = +SB.value, sg = +OP.value, g = a + sg * b, ka = a / 15, kb = b / 15;
      var sa = qSinK(ka), ca = qCosK(ka), sb = qSinK(kb), cb = qCosK(kb), pm = sg > 0 ? "+" : "-", mp = sg > 0 ? "-" : "+";
      var S_ = sg > 0 ? qAdd(qMul(sa, cb), qMul(ca, sb)) : qSub(qMul(sa, cb), qMul(ca, sb));
      var C_ = sg > 0 ? qSub(qMul(ca, cb), qMul(sa, sb)) : qAdd(qMul(ca, cb), qMul(sa, sb));
      var A = a + "^\\circ", B = b + "^\\circ", G = "(" + A + pm + B + ")", rows = [];
      rows.push([tex("\\sin" + G), tex("=\\sin " + A + "\\cos " + B + pm + "\\cos " + A + "\\sin " + B + "=" + P(sa) + "\\cdot" + P(cb) + pm + P(ca) + "\\cdot" + P(sb) + "=" + qT(S_))]);
      rows.push([tex("\\cos" + G), tex("=\\cos " + A + "\\cos " + B + mp + "\\sin " + A + "\\sin " + B + "=" + P(ca) + "\\cdot" + P(cb) + mp + P(sa) + "\\cdot" + P(sb) + "=" + qT(C_))]);
      var ta = qTanK(ka), tb = qTanK(kb), tr;
      if (ta && tb) {
        var den = sg > 0 ? qSub(Q(1), qMul(ta, tb)) : qAdd(Q(1), qMul(ta, tb)), num = sg > 0 ? qAdd(ta, tb) : qSub(ta, tb);
        tr = tex("=\\dfrac{\\tan " + A + pm + "\\tan " + B + "}{1" + mp + "\\tan " + A + "\\tan " + B + "}=\\dfrac{" + qT(ta) + pm + P(tb) + "}{1" + mp + P(ta) + "\\cdot" + P(tb) + "}=" + (qZero(den) ? "\\nexists" : qT(qDiv(num, den))));
      } else tr = t3("Una de les tangents no existeix: ho calculem com a ", "Una de las tangentes no existe: lo calculamos como ", "One of the tangents does not exist: we use ") + tex("\\dfrac{\\sin}{\\cos}=" + (qZero(C_) ? "\\nexists" : qT(qDiv(S_, C_))));
      rows.push([tex("\\tan" + G), tr]);
      rows.push([t3("Comprovació", "Comprobación", "Check"), tex(A + pm + B + "=" + g + "^\\circ") + small(tex("\\sin " + g + "^\\circ\\approx " + dT(Math.sin(rad(g)), 4) + ",\\ \\ " + qT(S_) + "\\approx " + dT(qVal(S_), 4)))]);
      info.innerHTML = kv(rows);
    }
    [SA, SB, OP].forEach(function (s) { s.addEventListener("change", draw); }); onLang(draw);
  }

  /* ---------- 3.9 identitats: analitzador d'expressions ---------- */
  function parseExpr(src) {
    var s = src.toLowerCase().replace(/\s+/g, "").replace(/·|×/g, "*").replace(/π/g, "pi").replace(/√/g, "sqrt").replace(/,/g, "."), i = 0;
    var FN = { sin: Math.sin, sen: Math.sin, cos: Math.cos, tan: Math.tan, tg: Math.tan, sec: function (x) { return 1 / Math.cos(x); }, cosec: function (x) { return 1 / Math.sin(x); }, csc: function (x) { return 1 / Math.sin(x); },
      cotg: function (x) { return Math.cos(x) / Math.sin(x); }, cot: function (x) { return Math.cos(x) / Math.sin(x); }, ctg: function (x) { return Math.cos(x) / Math.sin(x); }, sqrt: Math.sqrt };
    var NAMES = Object.keys(FN).sort(function (a, b) { return b.length - a.length; });
    function peek() { return s.charAt(i); }
    function fail() { throw new Error("parse"); }
    function expr() { var f = term(); while (peek() === "+" || peek() === "-") { var o = s.charAt(i++), g = term(), h = f; f = o === "+" ? (function (h, g) { return function (x) { return h(x) + g(x); }; })(h, g) : (function (h, g) { return function (x) { return h(x) - g(x); }; })(h, g); } return f; }
    function startsFactor() { var c = peek(); return c && (/[0-9.(x]/.test(c) || /[a-z]/.test(c)); }
    function term() {
      var f = unary();
      for (;;) {
        var c = peek();
        if (c === "*" || c === "/") { i++; var g = unary(), h = f; f = c === "*" ? (function (h, g) { return function (x) { return h(x) * g(x); }; })(h, g) : (function (h, g) { return function (x) { return h(x) / g(x); }; })(h, g); }
        else if (startsFactor()) { var g2 = power(), h2 = f; f = (function (h, g) { return function (x) { return h(x) * g(x); }; })(h2, g2); }
        else return f;
      }
    }
    function unary() { if (peek() === "-") { i++; var f = unary(); return function (x) { return -f(x); }; } if (peek() === "+") { i++; return unary(); } return power(); }
    function power() { var b = atom(); if (peek() === "^") { i++; var e = unary(); return function (x) { return Math.pow(b(x), e(x)); }; } return b; }
    function atom() {
      var c = peek(), m;
      if (c === "(") { i++; var f = expr(); if (peek() !== ")") fail(); i++; return f; }
      if ((m = s.slice(i).match(/^(\d+\.?\d*|\.\d+)/))) { i += m[0].length; var v = +m[0]; return function () { return v; }; }
      if (s.slice(i, i + 2) === "pi") { i += 2; return function () { return Math.PI; }; }
      if (c === "x") { i++; return function (x) { return x; }; }
      for (var k = 0; k < NAMES.length; k++) if (s.slice(i, i + NAMES[k].length) === NAMES[k]) {
        var fn = FN[NAMES[k]]; i += NAMES[k].length;
        var ex = null; if (peek() === "^") { i++; ex = atom(); }
        var arg = peek() === "(" ? atom() : power();
        return ex ? function (x) { return Math.pow(fn(arg(x)), ex(x)); } : function (x) { return fn(arg(x)); };
      }
      fail();
    }
    var f = expr(); if (i !== s.length) fail();
    return f;
  }
  function wId() {
    var w = byId("w-id"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), IL = $(w, "l"), IR = $(w, "r");
    var PRE = [["sin(2x)/(1+cos(2x))", "tan(x)"], ["(sin(x)-cos(x))/(tan(x)-1)", "cos(x)"], ["tan(x)^2-sin(x)^2", "tan(x)^2*sin(x)^2"], ["cos(3x)", "4cos(x)^3-3cos(x)"], ["tan(x)+cotg(x)", "sec(x)*cosec(x)"], ["sin(2x)", "2sin(x)"], ["(1+sin(2x))/(1+cos(2x))", "(1+tan(x))^2/2"]];
    presetBtns($(w, "pre"), function () { return PRE.map(function (p, i) { return t3("Exemple ", "Ejemplo ", "Example ") + (i + 1); }); }, function (i) { IL.value = PRE[i][0]; IR.value = PRE[i][1]; draw(); }, 0);
    function draw() {
      var fl = null, fr = null;
      try { fl = parseExpr(IL.value); } catch (e) {} try { fr = parseExpr(IR.value); } catch (e) {}
      IL.classList.toggle("bad", !fl); IR.classList.toggle("bad", !fr);
      var G = gview({ x0: -2 * Math.PI, x1: 2 * Math.PI, y0: -4, y1: 4, sy: 1, W: 360, H: 260, xt: piTicks(-2 * Math.PI, 2 * Math.PI, 0.5).map(function (t) { return [t[0], Math.round(Math.abs(t[0] / Math.PI * 2)) % 2 === 0 ? t[1] : ""]; }) });
      var h = G.g + G.open;
      if (fl) h += curve(G, fl, COL.cos, { w: 5 });
      if (fr) h += curve(G, fr, COL.sin, { dash: "7 5" });
      svg.innerHTML = h + G.close;
      if (!fl || !fr) { info.innerHTML = t3("No entenc alguna de les expressions. Exemple: <code>2sin(x)cos(x)</code>, <code>tan(x)^2</code>, <code>1/cos(x)</code>.", "No entiendo alguna de las expresiones. Ejemplo: <code>2sin(x)cos(x)</code>, <code>tan(x)^2</code>, <code>1/cos(x)</code>.", "I can't read one of the expressions. Example: <code>2sin(x)cos(x)</code>, <code>tan(x)^2</code>, <code>1/cos(x)</code>."); return; }
      var worst = null, n = 0;
      for (var k = 0; k < 400; k++) {
        var x = -6.2 + 12.4 * (k + 0.37) / 400, l = fl(x), r = fr(x);
        if (!isFinite(l) || !isFinite(r) || Math.abs(l) > 1e6 || Math.abs(r) > 1e6) continue;
        n++; var d = Math.abs(l - r) / Math.max(1, Math.abs(l));
        if (d > 1e-7 && (!worst || d > worst.d)) worst = { d: d, x: x, l: l, r: r };
      }
      var leg = cdot(COL.cos) + t3("primer membre", "primer miembro", "left side") + " &nbsp; " + cdot(COL.sin) + t3("segon membre", "segundo miembro", "right side");
      if (!n) info.innerHTML = leg + "<p>" + t3("No s'ha pogut avaluar.", "No se ha podido evaluar.", "Could not evaluate.") + "</p>";
      else if (!worst) info.innerHTML = leg + '<p><span class="msg-ok">✓</span> ' + t3("Les dues gràfiques coincideixen: <strong>sembla una identitat</strong>. Ara cal demostrar-la!", "Las dos gráficas coinciden: <strong>parece una identidad</strong>. ¡Ahora hay que demostrarla!", "The two graphs coincide: <strong>it looks like an identity</strong>. Now prove it!") + "</p>";
      else info.innerHTML = leg + '<p><span class="msg-bad">✗</span> ' + t3("<strong>No és una identitat</strong>. Per exemple, per a ", "<strong>No es una identidad</strong>. Por ejemplo, para ", "<strong>Not an identity</strong>. For example, at ") + tex("x\\approx " + dT(worst.x, 3)) + ": " + tex(dT(worst.l, 3) + "\\neq " + dT(worst.r, 3)) + ".</p>";
    }
    IL.addEventListener("input", draw); IR.addEventListener("input", draw); onLang(draw);
  }

  /* ---------- 3.11 equacions elementals ---------- */
  function wEq() {
    var w = byId("w-eq"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), Fs = $(w, "f"), Ks = $(w, "k"), Bi = $(w, "b"), Ci = $(w, "c");
    var PRE = [["sin", "1", "0", "1/2"], ["cos", "1", "0", "-1/2"], ["tan", "1", "0", "1"], ["sin", "4", "0", "-sqrt3/2"], ["cos", "2", "0", "sqrt2/2"], ["tan", "3", "0", "-1"], ["sin", "1/2", "0", "sqrt2/2"], ["cos", "1", "30", "0.4"]];
    var FN = { sin: "\\sin", cos: "\\cos", tan: "\\tan" };
    function kT(k) { return k === "1" ? "x" : k === "1/2" ? "\\frac x2" : k === "1/3" ? "\\frac x3" : k + "x"; }
    function argT(k, b) { return kT(k) + (b ? (b > 0 ? "+" : "-") + Math.abs(b) + "^\\circ" : ""); }
    presetBtns($(w, "pre"), function () { return PRE.map(function (p) { var pv = parseVal(p[3]); return tex(FN[p[0]] + (p[1] === "1" && p[2] === "0" ? " x" : "\\left(" + argT(p[1], +p[2]) + "\\right)") + "=" + (pv.ex ? sT(pv.ex) : dT(pv.v, 2))); }); },
      function (i) { Fs.value = PRE[i][0]; Ks.value = PRE[i][1]; Bi.value = PRE[i][2]; Ci.value = PRE[i][3]; draw(); }, 0);
    function draw() {
      var f = Fs.value, kq = Ks.value.split("/"), k = kq.length > 1 ? +kq[0] / +kq[1] : +kq[0], b = parseNum(Bi.value), pv = parseVal(Ci.value);
      Bi.classList.toggle("bad", b == null); Ci.classList.toggle("bad", !pv);
      if (b == null || !pv) { info.innerHTML = ""; svg.innerHTML = ""; return; }
      var c = pv.v, cT = pv.ex ? sT(pv.ex) : dT(c, 4), U = "u", steps = [], sol = [];
      var arg = argT(Ks.value, b), eqT = FN[f] + "\\left(" + arg + "\\right)=" + cT;
      var simple = Ks.value === "1" && !b;
      if (!simple) steps.push(t3("Fem ", "Hacemos ", "Let ") + tex("u=" + arg) + ": " + tex(FN[f] + " u=" + cT));
      var V = simple ? "x" : "u", fam = [];
      if (f !== "tan" && Math.abs(c) > 1 + 1e-12) steps.push(tex("|" + cT + "|\\gt1") + ": " + t3("<strong>l'equació no té solució</strong>.", "<strong>la ecuación no tiene solución</strong>.", "<strong>the equation has no solution</strong>."));
      else {
        var al = f === "sin" ? deg(Math.asin(Math.max(-1, Math.min(1, c)))) : f === "cos" ? deg(Math.acos(Math.max(-1, Math.min(1, c)))) : deg(Math.atan(c));
        steps.push(t3("Angle de la calculadora: ", "Ángulo de la calculadora: ", "Calculator angle: ") + tex("\\alpha=" + FN[f] + "^{-1}\\left(" + cT + "\\right)" + (Math.abs(al - Math.round(al)) < 1e-9 ? "=" + Math.round(al) + "^\\circ" : "\\approx " + dmsT(al))));
        if (f === "sin") fam = [al, 180 - al]; else if (f === "cos") fam = [al, -al]; else fam = [al];
        fam = fam.map(norm360).filter(function (x, i, A) { return A.findIndex(function (y) { return Math.abs(y - x) < 1e-9; }) === i; });
        var per = f === "tan" ? 180 : 360;
        steps.push(t3("Solució general per a ", "Solución general para ", "General solution for ") + tex(V) + ": " + tex(fam.map(function (x) { return V + "=" + angT(x) + "+" + per + "^\\circ k"; }).join(",\\quad ")) + (f === "sin" && fam.length === 2 ? small(t3("Els dos angles: ", "Los dos ángulos: ", "The two angles: ") + tex("\\alpha") + t3(" i ", " y ", " and ") + tex("180^\\circ-\\alpha")) : f === "cos" && fam.length === 2 ? small(tex("\\alpha") + t3(" i ", " y ", " and ") + tex("-\\alpha\\equiv360^\\circ-\\alpha")) : ""));
        if (!simple) {
          var kf = Ks.value, P2 = per / k;
          steps.push(t3("Aïllem ", "Despejamos ", "Solve for ") + tex("x") + ": " + tex(fam.map(function (x) { return "x=" + angT((x - b) / k) + "+" + angT(P2).replace("\\approx ", "") + "\\,k"; }).join(",\\quad ")));
        }
        fam.forEach(function (x0) {
          var P = per / k, st = (x0 - b) / k;
          for (var n = -20; n <= 20; n++) { var x = st + P * n; if (x > -1e-9 && x < 360 - 1e-9) sol.push(Math.abs(x) < 1e-9 ? 0 : x); }
        });
        sol.sort(function (p, q) { return p - q; });
        steps.push("<strong>" + t3("Solucions en ", "Soluciones en ", "Solutions in ") + tex("[0^\\circ,360^\\circ)") + ":</strong> " + (sol.length ? '<span class="sol-list">' + sol.map(function (x) { return "<span>" + tex(angT(x)) + "</span>"; }).join("") + "</span>" : t3("cap", "ninguna", "none")));
      }
      info.innerHTML = "<p>" + tex(eqT) + "</p><ol>" + steps.map(function (x) { return "<li>" + x + "</li>"; }).join("") + "</ol>";
      var fn = { sin: Math.sin, cos: Math.cos, tan: Math.tan }[f], ym = f === "tan" ? 3 : 1.5;
      var G = gview({ x0: 0, x1: 360, y0: -ym, y1: ym, sy: f === "tan" ? 1 : 0.5, W: 360, H: 240, pl: 30, xt: [[90, "90°"], [180, "180°"], [270, "270°"], [360, "360°"]] });
      var h = G.g + G.open + curve(G, function (x) { return fn(rad(k * x + b)); }, COL.cos, { n: 900 });
      h += '<line x1="' + G.X(0) + '" x2="' + G.X(360) + '" y1="' + f1(G.Y(c)) + '" y2="' + f1(G.Y(c)) + '" stroke="' + COL.sin + '" stroke-width="2" stroke-dasharray="6 4"/>';
      sol.forEach(function (x) { h += gdot(G, x, c, COL.r) + '<line x1="' + f1(G.X(x)) + '" x2="' + f1(G.X(x)) + '" y1="' + f1(G.Y(c)) + '" y2="' + f1(G.Y(0)) + '" class="gd"/>'; });
      svg.innerHTML = h + G.close;
    }
    [Fs, Ks].forEach(function (s) { s.addEventListener("change", draw); }); [Bi, Ci].forEach(function (s) { s.addEventListener("input", draw); }); onLang(draw);
  }

  /* ---------- 3.13 de la circumferència a la gràfica ---------- */
  function wWave() {
    var w = byId("w-wave"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), sl = $(w, "x"), pb = $(w, "play"), fn = 0, timer = null;
    var R = 70, cx = 95, cy = 120, gx0 = 200, gx1 = 625, FN = ["sin", "cos", "tan"];
    presetBtns($(w, "fn"), function () { return [tex("y=\\sin x"), tex("y=\\cos x"), tex("y=\\tan x")]; }, function (i) { fn = i; draw(); }, 0);
    function GX(d) { return gx0 + (gx1 - gx0) * d / 360; }
    function GY(y) { return cy - y * R; }
    function draw() {
      var d = +sl.value, e = rad(d), c = Math.cos(e), s = Math.sin(e), col = [COL.sin, COL.cos, COL.tan][fn];
      $(w, "xv").innerHTML = tex("x=" + d + "^\\circ=" + piT(Fr(d, 180)) + apx(e, 3).replace("=", "\\ \\ "));
      var h = '<line class="ax" x1="' + (cx - R - 14) + '" y1="' + cy + '" x2="' + (cx + R + 14) + '" y2="' + cy + '"/><line class="ax" x1="' + cx + '" y1="' + (cy - R - 14) + '" x2="' + cx + '" y2="' + (cy + R + 14) + '"/><circle class="cir" cx="' + cx + '" cy="' + cy + '" r="' + R + '"/>';
      h += '<line class="ax" x1="' + gx0 + '" y1="' + cy + '" x2="' + (gx1 + 8) + '" y2="' + cy + '"/><line class="ax" x1="' + gx0 + '" y1="' + (cy - 105) + '" x2="' + gx0 + '" y2="' + (cy + 105) + '"/>';
      [1, -1].forEach(function (v) { h += '<line class="g" x1="' + gx0 + '" x2="' + gx1 + '" y1="' + GY(v) + '" y2="' + GY(v) + '"/><text x="' + (gx0 - 4) + '" y="' + (GY(v) + 4) + '" text-anchor="end">' + (v > 0 ? "1" : "−1") + "</text>"; });
      [[90, "π/2"], [180, "π"], [270, "3π/2"], [360, "2π"]].forEach(function (t) { h += '<line class="g" x1="' + GX(t[0]) + '" x2="' + GX(t[0]) + '" y1="' + (cy - 105) + '" y2="' + (cy + 105) + '"/><text x="' + GX(t[0]) + '" y="' + (cy + 14) + '" text-anchor="middle">' + t[1] + "</text>"; });
      var Px = cx + R * c, Py = cy - R * s;
      h += '<path class="sect" style="fill:' + COL.ang + '" d="M' + cx + " " + cy + "L" + (cx + R) + " " + cy + "A" + R + " " + R + " 0 " + (d > 180 ? 1 : 0) + " 0 " + f1(Px) + " " + f1(Py) + 'Z"/>';
      // corba fins a x
      var path = "", pen = false;
      for (var t = 0; t <= d; t += 1) {
        var y = fn === 0 ? Math.sin(rad(t)) : fn === 1 ? Math.cos(rad(t)) : Math.tan(rad(t));
        if (fn === 2 && (Math.abs(y) > 1.5)) { pen = false; continue; }
        path += (pen ? "L" : "M") + f1(GX(t)) + " " + f1(GY(y)); pen = true;
      }
      var full = "";
      pen = false;
      for (t = 0; t <= 360; t += 1) { var yy = fn === 0 ? Math.sin(rad(t)) : fn === 1 ? Math.cos(rad(t)) : Math.tan(rad(t)); if (fn === 2 && Math.abs(yy) > 1.5) { pen = false; continue; } full += (pen ? "L" : "M") + f1(GX(t)) + " " + f1(GY(yy)); pen = true; }
      h += '<path class="cv" d="' + full + '" style="stroke:var(--border)"/><path class="cv" d="' + path + '" style="stroke:' + col + '"/>';
      var val, vy;
      if (fn === 0) { val = s; vy = s; h += '<line class="sg" x1="' + f1(Px) + '" y1="' + cy + '" x2="' + f1(Px) + '" y2="' + f1(Py) + '" style="stroke:' + col + '"/>'; }
      else if (fn === 1) { val = c; vy = c; h += '<line class="sg" x1="' + cx + '" y1="' + cy + '" x2="' + f1(Px) + '" y2="' + cy + '" style="stroke:' + col + '"/><line class="gd" x1="' + f1(Px) + '" y1="' + cy + '" x2="' + f1(Px) + '" y2="' + f1(Py) + '"/>'; }
      else {
        val = Math.abs(c) < 1e-12 ? null : s / c; vy = val;
        h += '<line class="gd" x1="' + (cx + R) + '" y1="' + (cy - 105) + '" x2="' + (cx + R) + '" y2="' + (cy + 105) + '"/>';
        if (val != null && Math.abs(val) <= 1.5) h += '<line class="gd" x1="' + cx + '" y1="' + cy + '" x2="' + (cx + R) + '" y2="' + f1(GY(val)) + '"/><line class="sg" x1="' + (cx + R) + '" y1="' + cy + '" x2="' + (cx + R) + '" y2="' + f1(GY(val)) + '" style="stroke:' + col + '"/>';
      }
      h += '<line class="ln" x1="' + cx + '" y1="' + cy + '" x2="' + f1(Px) + '" y2="' + f1(Py) + '" style="stroke:var(--text)"/><circle class="pt" cx="' + f1(Px) + '" cy="' + f1(Py) + '" r="5" style="fill:' + COL.r + '"/>';
      if (vy != null && Math.abs(vy) <= 1.5) {
        var sx = fn === 2 ? cx + R : fn === 1 ? Px : Px;
        h += '<line class="gd" x1="' + f1(sx) + '" y1="' + f1(GY(vy)) + '" x2="' + f1(GX(d)) + '" y2="' + f1(GY(vy)) + '" style="stroke:' + col + '"/><circle class="pt" cx="' + f1(GX(d)) + '" cy="' + f1(GY(vy)) + '" r="5.5" style="fill:' + col + '"/>';
      }
      svg.innerHTML = h;
      var nm = ["\\sin", "\\cos", "\\tan"][fn], ex = exact(d), qx = ex ? [ex.s, ex.c, ex.t][fn] : null;
      info.innerHTML = tex("y=" + nm + "\\left(" + piT(Fr(d, 180)) + "\\right)=" + (val == null ? "\\nexists" : qx ? qT(qx) + (Math.abs(qVal(qx) - Math.round(qVal(qx))) > 1e-9 ? "\\approx " + dT(val, 3) : "") : (Math.abs(val - +val.toFixed(3)) > 1e-10 ? "\\approx " : "") + dT(val, 3))) +
        (fn === 1 ? small(t3("Per a la gràfica del cosinus, l'abscissa de P (segment blau) es posa en vertical.", "Para la gráfica del coseno, la abscisa de P (segmento azul) se pone en vertical.", "For the cosine graph, the x-coordinate of P (blue segment) is plotted vertically.")) : fn === 2 ? small(t3("La tangent no existeix en π/2 i 3π/2: la gràfica té asímptotes verticals.", "La tangente no existe en π/2 y 3π/2: la gráfica tiene asíntotas verticales.", "The tangent does not exist at π/2 and 3π/2: the graph has vertical asymptotes.")) : "");
    }
    function stop() { if (timer) { cancelAnimationFrame(timer); timer = null; } pb.textContent = "▶"; }
    pb.addEventListener("click", function () {
      if (timer) { stop(); return; }
      pb.textContent = "❚❚"; if (+sl.value >= 360) sl.value = 0;
      var last = null;
      function step(ts) { if (last == null) last = ts; var v = +sl.value + (ts - last) * 0.09; last = ts; if (v >= 360) { sl.value = 360; draw(); stop(); return; } sl.value = v; draw(); timer = requestAnimationFrame(step); }
      timer = requestAnimationFrame(step);
    });
    sl.addEventListener("input", function () { stop(); draw(); }); onLang(draw);
  }

  /* ---------- 3.13 y = A·f(Bx + C) + D ---------- */
  function wFun() {
    var w = byId("w-fun"); if (!w) return;
    var svg = w.querySelector("svg"), info = w.querySelector(".info"), fn = 0, S = {};
    ["A", "B", "C", "D"].forEach(function (k) { S[k] = $(w, k); S[k].addEventListener("input", draw); });
    var BV = [Fr(1, 4), Fr(1, 3), Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(3), Fr(4)];
    presetBtns($(w, "fn"), function () { return [tex("\\sin"), tex("\\cos"), tex("\\tan")]; }, function (i) { fn = i; draw(); }, 0);
    function nT(x) { var f = Fr(Math.round(x * 2), 2); return fT(f).replace("{,}", ","); }
    function draw() {
      var A = +S.A.value, Bf = BV[+S.B.value], B = fVal(Bf), Ck = +S.C.value, Cf = Fr(Ck, 4), C = Ck * Math.PI / 4, D = +S.D.value;
      $(w, "Av").innerHTML = tex(nT(A)); $(w, "Bv").innerHTML = tex(fT(Bf)); $(w, "Cv").innerHTML = tex(piT(Cf)); $(w, "Dv").innerHTML = tex(nT(D));
      var F0 = [Math.sin, Math.cos, Math.tan][fn], nm = ["\\sin", "\\cos", "\\tan"][fn];
      var G = gview({ x0: -2 * Math.PI, x1: 2 * Math.PI, y0: -5, y1: 5, sy: 1, W: 360, H: 260, xt: piTicks(-2 * Math.PI, 2 * Math.PI, 0.5).map(function (t) { return [t[0], Math.round(Math.abs(t[0] / Math.PI * 2)) % 2 === 0 ? t[1] : ""]; }) });
      var h = G.g + G.open + curve(G, F0, "var(--muted)", { dash: "5 5", w: 1.8 }) + curve(G, function (x) { return A * F0(B * x + C) + D; }, COL.cos, { n: 1200 });
      if (fn < 2 && A) [D + Math.abs(A), D - Math.abs(A)].forEach(function (y) { h += '<line class="gd" x1="' + G.X(-2 * Math.PI) + '" x2="' + G.X(2 * Math.PI) + '" y1="' + f1(G.Y(y)) + '" y2="' + f1(G.Y(y)) + '"/>'; });
      svg.innerHTML = h + G.close;
      var inner = (B === 1 ? "" : fT(Bf).replace(/^\\frac\{1\}\{(\d+)\}$/, "\\tfrac{1}{$1}")) + "x" + (Ck ? (Ck > 0 ? "+" : "-") + piT(Fr(Math.abs(Ck), 4)) : "");
      var eq = "y=" + (A === 1 ? "" : A === -1 ? "-" : nT(A)) + nm + "\\left(" + inner + "\\right)" + (D ? (D > 0 ? "+" : "-") + nT(Math.abs(D)) : "");
      var per = fn === 2 ? fDiv(1, Bf) : fDiv(2, Bf), shift = fDiv(fMul(Cf, -1), Bf);
      var rows = [[t3("Funció", "Función", "Function"), tex(A ? eq : "y=" + nT(D))]];
      if (!A) rows.push(["", t3("Amb A = 0 la funció és constant.", "Con A = 0 la función es constante.", "With A = 0 the function is constant.")]);
      else {
        rows.push([fn < 2 ? t3("Amplitud", "Amplitud", "Amplitude") : t3("Factor vertical", "Factor vertical", "Vertical factor"), tex("|A|=" + nT(Math.abs(A))) + (A < 0 ? small(t3("A < 0: la gràfica es reflecteix respecte de l'eix X.", "A < 0: la gráfica se refleja respecto del eje X.", "A < 0: the graph is reflected in the x-axis.")) : "")]);
        rows.push([t3("Període", "Periodo", "Period"), tex("T=\\dfrac{" + (fn === 2 ? "\\pi" : "2\\pi") + "}{" + fT(Bf) + "}=" + piT(per))]);
        rows.push([t3("Desplaçament horitzontal", "Desplazamiento horizontal", "Horizontal shift"), Ck ? tex("-\\dfrac CB=" + piT(shift)) + small(fVal(shift) < 0 ? t3("cap a l'esquerra", "hacia la izquierda", "to the left") : t3("cap a la dreta", "hacia la derecha", "to the right")) : tex("0")]);
        rows.push([t3("Recorregut", "Recorrido", "Range"), fn < 2 ? tex("[" + nT(D - Math.abs(A)) + ",\\ " + nT(D + Math.abs(A)) + "]") : tex("\\mathbb R")]);
      }
      info.innerHTML = kv(rows);
    }
    onLang(draw);
  }

  /* ---------- qüestionari ---------- */
  function q3(va, es, en) { return { va: va, es: es === undefined ? va : es, en: en === undefined ? va : en }; }
  var QUIZ = [
    { q: q3("L'angle de $135^\\circ$ en radians és…", "El ángulo de $135^\\circ$ en radianes es…", "$135^\\circ$ in radians is…"),
      o: [q3("$\\frac{3\\pi}{4}$"), q3("$\\frac{4\\pi}{3}$"), q3("$\\frac{2\\pi}{3}$")], a: 0, e: q3("$135\\cdot\\frac{\\pi}{180}=\\frac{3\\pi}{4}$.") },
    { q: q3("Un radian és aproximadament…", "Un radián es aproximadamente…", "One radian is about…"),
      o: [q3("$1^\\circ$"), q3("$57^\\circ$"), q3("$90^\\circ$")], a: 1, e: q3("$\\frac{180^\\circ}{\\pi}\\approx57^\\circ17'45''$.") },
    { q: q3("Si $\\alpha$ és agut i $\\sin\\alpha=\\frac45$, aleshores $\\cos\\alpha$ val…", "Si $\\alpha$ es agudo y $\\sin\\alpha=\\frac45$, entonces $\\cos\\alpha$ vale…", "If $\\alpha$ is acute and $\\sin\\alpha=\\frac45$, then $\\cos\\alpha$ is…"),
      o: [q3("$\\frac15$"), q3("$\\frac35$"), q3("$\\frac54$")], a: 1, e: q3("$\\sqrt{1-\\frac{16}{25}}=\\frac35$.") },
    { q: q3("En quin quadrant és $\\sin\\alpha\\lt0$ i $\\tan\\alpha\\gt0$?", "¿En qué cuadrante es $\\sin\\alpha\\lt0$ y $\\tan\\alpha\\gt0$?", "In which quadrant is $\\sin\\alpha\\lt0$ and $\\tan\\alpha\\gt0$?"),
      o: [q3("II"), q3("III"), q3("IV")], a: 1, e: q3("Si la tangent és positiva i el sinus negatiu, el cosinus també és negatiu: tercer quadrant.", "Si la tangente es positiva y el seno negativo, el coseno también es negativo: tercer cuadrante.", "If the tangent is positive and the sine negative, the cosine is negative too: third quadrant.") },
    { q: q3("$\\cos 240^\\circ$ val…", "$\\cos 240^\\circ$ vale…", "$\\cos 240^\\circ$ equals…"),
      o: [q3("$-\\frac12$"), q3("$\\frac12$"), q3("$-\\frac{\\sqrt3}{2}$")], a: 0, e: q3("$240^\\circ=180^\\circ+60^\\circ$: $\\cos240^\\circ=-\\cos60^\\circ=-\\frac12$.") },
    { q: q3("$\\sin 1110^\\circ$ val…", "$\\sin 1110^\\circ$ vale…", "$\\sin 1110^\\circ$ equals…"),
      o: [q3("$\\frac{\\sqrt3}{2}$"), q3("$-\\frac12$"), q3("$\\frac12$")], a: 2, e: q3("$1110^\\circ=3\\cdot360^\\circ+30^\\circ$: $\\sin30^\\circ=\\frac12$.") },
    { q: q3("$\\sin(180^\\circ-\\alpha)$ és igual a…", "$\\sin(180^\\circ-\\alpha)$ es igual a…", "$\\sin(180^\\circ-\\alpha)$ equals…"),
      o: [q3("$\\sin\\alpha$"), q3("$-\\sin\\alpha$"), q3("$\\cos\\alpha$")], a: 0, e: q3("Els angles suplementaris tenen el mateix sinus (simetria respecte de l'eix $OY$).", "Los ángulos suplementarios tienen el mismo seno (simetría respecto del eje $OY$).", "Supplementary angles have the same sine (symmetry in the $y$-axis).") },
    { q: q3("En un triangle rectangle en $C$, $c=10$ i $\\hat A=30^\\circ$. El catet $a$ mesura…", "En un triángulo rectángulo en $C$, $c=10$ y $\\hat A=30^\\circ$. El cateto $a$ mide…", "In a triangle right-angled at $C$, $c=10$ and $\\hat A=30^\\circ$. The leg $a$ is…"),
      o: [q3("$5$"), q3("$5\\sqrt3$"), q3("$20$")], a: 0, e: q3("$a=c\\sin\\hat A=10\\cdot\\frac12=5$.") },
    { q: q3("Coneixem $a$, $b$ i $\\hat C$ (l'angle comprés). Quin teorema fem servir primer?", "Conocemos $a$, $b$ y $\\hat C$ (el ángulo comprendido). ¿Qué teorema usamos primero?", "We know $a$, $b$ and the included angle $\\hat C$. Which rule do we use first?"),
      o: [q3("El del sinus", "El del seno", "The sine rule"), q3("El del cosinus", "El del coseno", "The cosine rule"), q3("Pitàgores", "Pitágoras", "Pythagoras")], a: 1, e: q3("$c^2=a^2+b^2-2ab\\cos\\hat C$ dona el tercer costat.", "$c^2=a^2+b^2-2ab\\cos\\hat C$ da el tercer lado.", "$c^2=a^2+b^2-2ab\\cos\\hat C$ gives the third side.") },
    { q: q3("Un triangle de costats 7, 8 i 12 és…", "Un triángulo de lados 7, 8 y 12 es…", "A triangle with sides 7, 8 and 12 is…"),
      o: [q3("acutangle", "acutángulo", "acute"), q3("rectangle", "rectángulo", "right-angled"), q3("obtusangle", "obtusángulo", "obtuse")], a: 2, e: q3("$12^2=144\\gt7^2+8^2=113$: l'angle oposat al costat major és obtús.", "$12^2=144\\gt7^2+8^2=113$: el ángulo opuesto al lado mayor es obtuso.", "$12^2=144\\gt7^2+8^2=113$: the angle opposite the longest side is obtuse.") },
    { q: q3("$\\sin75^\\circ$ val…", "$\\sin75^\\circ$ vale…", "$\\sin75^\\circ$ equals…"),
      o: [q3("$\\frac{\\sqrt6-\\sqrt2}{4}$"), q3("$\\frac{\\sqrt6+\\sqrt2}{4}$"), q3("$\\frac{\\sqrt3+1}{2}$")], a: 1, e: q3("$\\sin(45^\\circ+30^\\circ)=\\frac{\\sqrt2}{2}\\cdot\\frac{\\sqrt3}{2}+\\frac{\\sqrt2}{2}\\cdot\\frac12$.") },
    { q: q3("$\\cos^2\\alpha-\\sin^2\\alpha$ és igual a…", "$\\cos^2\\alpha-\\sin^2\\alpha$ es igual a…", "$\\cos^2\\alpha-\\sin^2\\alpha$ equals…"),
      o: [q3("$1$"), q3("$\\sin2\\alpha$"), q3("$\\cos2\\alpha$")], a: 2, e: q3("És la fórmula del cosinus de l'angle doble.", "Es la fórmula del coseno del ángulo doble.", "It is the double-angle formula for the cosine.") },
    { q: q3("Quantes solucions té $\\sin2x=\\frac12$ en $[0^\\circ,360^\\circ)$?", "¿Cuántas soluciones tiene $\\sin2x=\\frac12$ en $[0^\\circ,360^\\circ)$?", "How many solutions does $\\sin2x=\\frac12$ have in $[0^\\circ,360^\\circ)$?"),
      o: [q3("2"), q3("4"), q3("1")], a: 1, e: q3("$x=15^\\circ,75^\\circ,195^\\circ,255^\\circ$: l'argument $2x$ fa dues voltes.", "$x=15^\\circ,75^\\circ,195^\\circ,255^\\circ$: el argumento $2x$ da dos vueltas.", "$x=15^\\circ,75^\\circ,195^\\circ,255^\\circ$: the argument $2x$ goes round twice.") },
    { q: q3("El període de $y=3\\sin(4x)$ és…", "El periodo de $y=3\\sin(4x)$ es…", "The period of $y=3\\sin(4x)$ is…"),
      o: [q3("$\\frac{\\pi}{2}$"), q3("$8\\pi$"), q3("$\\frac{2\\pi}{3}$")], a: 0, e: q3("$T=\\frac{2\\pi}{4}=\\frac{\\pi}{2}$; el 3 és l'amplitud.", "$T=\\frac{2\\pi}{4}=\\frac{\\pi}{2}$; el 3 es la amplitud.", "$T=\\frac{2\\pi}{4}=\\frac{\\pi}{2}$; the 3 is the amplitude.") }
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
    var all = [wChrome, wSteps, wNav, wRad, wRt, wCirc, wFind, wRed, wRect, wLab, wTri, wSum, wId, wEq, wWave, wFun, wQuiz];
    all.forEach(function (fn) { try { fn(); } catch (e) { if (window.console) console.error(fn.name, e); } });
    window.FM3 = { Q: Q, qT: qT, qDiv: qDiv, exact: exact, parseVal: parseVal, parseExpr: parseExpr, sT: sT };
  }
  if (document.readyState === "complete") init(); else window.addEventListener("load", init);
})();
