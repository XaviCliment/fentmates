/* ==========================================================
   Lògica comuna: idioma, tema, menú, nivells, PAU i reptes.
   Normalment no cal tocar res d'ací.
   ========================================================== */
(function () {
  "use strict";

  var LANGS = ["va", "es", "en"];
  var HTML_LANG = { va: "ca", es: "es", en: "en" };
  var DATE_LOCALE = { va: "ca-ES", es: "es-ES", en: "en-GB" };
  var SITE = window.SITE || {};
  var LEVELS = window.LEVELS || {};

  var ICONS = {
    notes: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/></svg>',
    exercises: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>',
    video: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="5" width="15" height="14" rx="2"/><path d="m17 10 5-3v10l-5-3z"/></svg>',
    resource: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m16.2 7.8-2.1 6.3-6.3 2.1 2.1-6.3z"/></svg>',
    calc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2"/><rect x="8" y="5" width="8" height="4" rx="1"/><path d="M8 13h.01M12 13h.01M16 13h.01M8 17h.01M12 17h.01M16 17h.01"/></svg>',
    exam: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg>',
    download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>',
    chev: '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m6 9 6 6 6-6"/></svg>',
    menu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>',
    mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
    linkedin: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56zM22.22 0H1.77C.79 0 0 .77 0 1.73v20.54C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.73C24 .77 23.2 0 22.22 0z"/></svg>',
    x: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.9 2H22l-6.8 7.8L23 22h-6.3l-4.9-6.4L6.2 22H3l7.3-8.4L1 2h6.4l4.4 5.9zm-1.1 18h1.7L6.3 3.9H4.5z"/></svg>'
  };

  /* ---------- utilitats ---------- */
  function store(key, val) {
    try {
      if (val === undefined) return localStorage.getItem(key);
      localStorage.setItem(key, val);
    } catch (e) { return null; }
  }

  var params = new URLSearchParams(location.search);
  var lang = params.get("lang");
  if (LANGS.indexOf(lang) < 0) lang = store("lang");
  if (LANGS.indexOf(lang) < 0) lang = "va";

  function t(key) {
    var d = window.I18N[lang] || {};
    return d[key] != null ? d[key] : (window.I18N.va[key] || key);
  }
  function tx(v) {
    if (v == null) return "";
    return typeof v === "string" ? v : (v[lang] || v.va || "");
  }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function parseDay(s) { var p = String(s).split("-"); return new Date(+p[0], +p[1] - 1, +p[2]); }
  function today() { var d = new Date(); return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function fmtDate(s) {
    return parseDay(s).toLocaleDateString(DATE_LOCALE[lang], { day: "numeric", month: "long", year: "numeric" });
  }
  function el(id) { return document.getElementById(id); }
  // materials visibles (els que porten hidden: true no es mostren)
  function visible(items) { return (items || []).filter(function (i) { return !i.hidden; }); }
  function levelKeys(stage) {
    return Object.keys(LEVELS).filter(function (k) { return !stage || (LEVELS[k].stage || "eso") === stage; });
  }

  /* Fórmules LaTeX amb KaTeX */
  function typeset(root) {
    if (!window.renderMathInElement || !root) return;
    window.renderMathInElement(root, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    });
  }

  /* ---------- tema ---------- */
  function currentTheme() {
    var th = document.documentElement.getAttribute("data-theme");
    if (th) return th;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  var savedTheme = store("theme");
  if (savedTheme) document.documentElement.setAttribute("data-theme", savedTheme);

  /* ---------- capçalera i peu ---------- */
  var page = document.body.getAttribute("data-page") || "home";
  var levelKey = document.body.getAttribute("data-level");

  function navLink(href, label, current) {
    return '<li><a href="' + href + '"' + (current ? ' aria-current="page"' : "") + ">" + esc(label) + "</a></li>";
  }

  function renderHeader() {
    var h = el("site-header");
    if (!h) return;
    var links = navLink("index.html", t("nav.home"), page === "home");
    var sub = ["eso", "batx"].map(function (st) {
      var ks = levelKeys(st);
      if (!ks.length) return "";
      return '<li class="sub-group"><span class="sub-head">' + esc(t("stage." + st)) + "</span><ul>" +
        ks.map(function (k) { return navLink(k + ".html", tx(LEVELS[k].name), k === levelKey).replace("<a ", '<a style="--c:' + LEVELS[k].color + '" '); }).join("") + "</ul></li>";
    }).join("");
    links += '<li class="has-sub' + (levelKey ? " current" : "") + '"><button type="button" class="sub-toggle" aria-expanded="false">' +
      esc(t("nav.courses")) + ICONS.chev + '</button><ul class="sub-menu">' + sub + "</ul></li>";
    links += navLink("pau.html", t("nav.pau"), page === "pau");
    links += navLink("reptes.html", t("nav.challenges"), page === "reptes");

    var langs = LANGS.map(function (l) {
      return '<button type="button" data-lang="' + l + '" aria-pressed="' + (l === lang) + '">' + l.toUpperCase() + "</button>";
    }).join("");
    h.innerHTML =
      '<div class="container">' +
        '<a class="brand" href="index.html"><span class="brand-logo" aria-hidden="true">π</span><span class="brand-text">Fent<b>Mates</b></span></a>' +
        '<nav class="main-nav" id="main-nav" aria-label="Principal"><ul>' + links + "</ul></nav>" +
        '<div class="header-tools">' +
          '<div class="lang-switch" role="group" aria-label="Idioma / Language">' + langs + "</div>" +
          '<button class="icon-btn theme-toggle" type="button" aria-label="' + esc(t("nav.theme")) + '">' + (currentTheme() === "dark" ? ICONS.sun : ICONS.moon) + "</button>" +
          '<button class="icon-btn menu-toggle" type="button" aria-controls="main-nav" aria-expanded="false" aria-label="' + esc(t("nav.menu")) + '">' + ICONS.menu + "</button>" +
        "</div>" +
      "</div>";

    h.querySelectorAll("[data-lang]").forEach(function (b) {
      b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
    });
    h.querySelector(".theme-toggle").addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      store("theme", next);
      this.innerHTML = next === "dark" ? ICONS.sun : ICONS.moon;
    });
    var nav = h.querySelector(".main-nav");
    var mt = h.querySelector(".menu-toggle");
    mt.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      mt.setAttribute("aria-expanded", open);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { nav.classList.remove("open"); mt.setAttribute("aria-expanded", "false"); }
    });
    var hs = h.querySelector(".has-sub"), st = h.querySelector(".sub-toggle");
    st.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = hs.classList.toggle("open");
      st.setAttribute("aria-expanded", open);
    });
    document.addEventListener("click", function (e) {
      if (!hs.contains(e.target)) { hs.classList.remove("open"); st.setAttribute("aria-expanded", "false"); }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { hs.classList.remove("open"); st.setAttribute("aria-expanded", "false"); }
    });
  }

  function contactLinks(cls, menuUp) {
    var links = [];
    if (SITE.x) links.push(["https://x.com/" + SITE.x, "x", "X"]);
    if (SITE.linkedin) links.push([SITE.linkedin, "linkedin", "LinkedIn"]);
    var out = "";
    // Correu: menú amb Gmail, aplicació de correu o copiar l'adreça
    // (el mailto sol no funciona si l'ordinador no té cap aplicació de correu configurada)
    if (SITE.email) {
      var gmail = "https://mail.google.com/mail/?view=cm&fs=1&to=" + encodeURIComponent(SITE.email);
      out += '<span class="mail-wrap"><button type="button" class="' + cls + ' mail-btn" aria-haspopup="true" aria-expanded="false" aria-label="' + esc(t("contact.mail")) + '" title="' + esc(t("contact.mail")) + '">' + ICONS.mail + "</button>" +
        '<span class="mail-menu' + (menuUp ? " up" : "") + '" role="menu">' +
          '<a role="menuitem" href="' + esc(gmail) + '" target="_blank" rel="noopener">' + esc(t("contact.gmail")) + "</a>" +
          '<a role="menuitem" href="mailto:' + esc(SITE.email) + '">' + esc(t("contact.app")) + "</a>" +
          '<button role="menuitem" type="button" class="mail-copy">' + esc(t("contact.copy")) + "</button>" +
        "</span></span>";
    }
    return out + links.map(function (l) {
      return '<a class="' + cls + '" href="' + esc(l[0]) + '" aria-label="' + esc(l[2]) + '" title="' + esc(l[2]) + '" target="_blank" rel="noopener">' + ICONS[l[1]] + "</a>";
    }).join("");
  }

  function closeMailMenus(except) {
    document.querySelectorAll(".mail-wrap.open").forEach(function (w) {
      if (w === except) return;
      w.classList.remove("open");
      w.querySelector(".mail-btn").setAttribute("aria-expanded", "false");
    });
  }

  function setupMailMenu() {
    document.addEventListener("click", function (e) {
      var btn = e.target.closest && e.target.closest(".mail-btn");
      if (btn) {
        var w = btn.parentNode;
        closeMailMenus(w);
        var open = w.classList.toggle("open");
        btn.setAttribute("aria-expanded", open);
        return;
      }
      var copy = e.target.closest && e.target.closest(".mail-copy");
      if (copy) {
        var done = function () { copy.textContent = t("contact.copied"); setTimeout(function () { copy.textContent = t("contact.copy"); }, 2000); };
        if (navigator.clipboard) navigator.clipboard.writeText(SITE.email).then(done, function () { prompt("", SITE.email); });
        else prompt("", SITE.email);
        return;
      }
      if (!(e.target.closest && e.target.closest(".mail-menu"))) closeMailMenus();
      else setTimeout(closeMailMenus, 100);
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeMailMenus(); });
  }

  /* Comptador de visites (hits.sh): compta cada pàgina vista del web publicat.
     Estadístiques: https://hits.sh/fentmates.org/  ·  En local no compta. */
  function visitCounter() {
    var h = location.hostname;
    if (!h || h === "localhost" || h === "127.0.0.1" || /\.local$/.test(h)) {
      return '<span class="visits" title="El comptador només funciona al web publicat">' + esc(t("footer.visits")) + ': —</span>';
    }
    return '<span class="visits"><img src="https://hits.sh/fentmates.org.svg?style=flat-square&amp;label=' +
      encodeURIComponent(t("footer.visits")) + '&amp;color=5d6685&amp;labelColor=8a93ad" alt="' + esc(t("footer.visits")) +
      '" width="80" height="20" loading="lazy" referrerpolicy="no-referrer"></span>';
  }

  function renderFooter() {
    var f = el("site-footer");
    if (!f) return;
    f.innerHTML =
      '<div class="container">' +
        "<span>© " + new Date().getFullYear() + " · FentMates · " + esc(t("footer.made")) + "</span>" +
        visitCounter() +
        '<span class="footer-links">' + contactLinks("social-btn small", true) + '<a href="#top">' + esc(t("footer.top")) + "</a></span>" +
      "</div>";
  }

  function renderContact() {
    var c = el("contact-buttons");
    if (c) c.innerHTML = contactLinks("social-btn");
  }

  /* ---------- textos estàtics ---------- */
  function applyI18n() {
    document.documentElement.lang = HTML_LANG[lang];
    document.querySelectorAll("[data-i18n]").forEach(function (n) { n.textContent = t(n.getAttribute("data-i18n")); });
    document.querySelectorAll("[data-i18n-html]").forEach(function (n) { n.innerHTML = t(n.getAttribute("data-i18n-html")); });
    document.querySelectorAll("[data-i18n-attr]").forEach(function (n) {
      n.getAttribute("data-i18n-attr").split(";").forEach(function (pair) {
        var p = pair.split(":");
        n.setAttribute(p[0].trim(), t(p[1].trim()));
      });
    });
    var lvl = levelKey && LEVELS[levelKey];
    var titleKey = document.body.getAttribute("data-title-key");
    document.title = lvl ? tx(lvl.name) + " · FentMates" : titleKey ? t(titleKey) + " · FentMates" : "FentMates";
  }

  function setLang(l) {
    if (LANGS.indexOf(l) < 0) return;
    lang = l;
    store("lang", l);
    var u = new URL(location.href);
    u.searchParams.delete("lang");
    history.replaceState(null, "", u);
    renderAll();
  }

  /* ---------- inici: targetes de nivell ---------- */
  function levelCard(k) {
    var L = LEVELS[k];
    var n = 0;
    L.units.forEach(function (u) { n += visible(u.items).length; });
    var soon = !L.units.length;
    var tag = soon
      ? '<span class="tag">' + esc(t("level.comingsoon")) + "</span>"
      : '<span class="tag">' + L.units.filter(function (u) { return !u.num; }).length + " " + esc(t("level.units")) + " · " + n + " " + esc(t("level.items")) + "</span>";
    return '<a class="level-card' + (soon ? " soon" : "") + '" href="' + k + '.html" style="--c:' + L.color + '">' +
      '<span class="symbol" aria-hidden="true">' + esc(L.symbol || "") + "</span>" +
      '<span class="tags">' + tag + "</span>" +
      "<h3>" + esc(tx(L.name)) + "</h3>" +
      "<p>" + esc(tx(L.desc)) + "</p>" +
      '<span class="go">' + esc(t("levels.go")) + "</span></a>";
  }

  function renderLevelCards() {
    var box = el("level-cards");
    if (!box) return;
    box.innerHTML = ["eso", "batx"].map(function (st) {
      var ks = levelKeys(st);
      if (!ks.length) return "";
      return '<div class="level-group"><h3 class="group-title">' + esc(t("stage." + st)) + '</h3><div class="levels">' +
        ks.map(levelCard).join("") + "</div></div>";
    }).join("");
  }

  /* ---------- pàgina de nivell ---------- */
  var state = { q: "", type: "all" };
  var KINDS = ["notes", "exercises", "video", "resource", "exam", "calc"];

  function renderLevelPage() {
    var L = levelKey && LEVELS[levelKey];
    if (!L) return;
    document.documentElement.style.setProperty("--c", L.color);
    document.querySelectorAll("[data-level-name]").forEach(function (n) { n.textContent = tx(L.name); });
    var d = el("level-desc"); if (d) d.textContent = tx(L.desc);

    var soon = !L.units.length;
    var tb = document.querySelector(".toolbar");
    if (tb) tb.hidden = soon;

    var cta = el("level-cta");
    if (cta) cta.innerHTML = L.pau ? '<a class="pau-cta" href="pau.html">🎯 ' + esc(t("level.pau.cta")) + "</a>" : "";

    var f = el("filters");
    if (f) {
      var present = KINDS.filter(function (k) {
        return L.units.some(function (u) { return visible(u.items).some(function (i) { return i.type === k; }); });
      });
      f.innerHTML = ["all"].concat(present).map(function (k) {
        return '<button type="button" class="filter" data-type="' + k + '" aria-pressed="' + (state.type === k) + '">' +
          esc(k === "all" ? t("level.all") : t("kind." + k)) + "</button>";
      }).join("");
      f.querySelectorAll(".filter").forEach(function (b) {
        b.addEventListener("click", function () { state.type = b.getAttribute("data-type"); renderLevelPage(); });
      });
    }
    var s = el("search");
    if (s && !s.dataset.bound) {
      s.dataset.bound = "1";
      s.addEventListener("input", function () { state.q = s.value.trim().toLowerCase(); renderUnits(L); });
    }
    renderUnits(L);
  }

  function ytId(url) {
    var m = String(url || "").match(/(?:youtube\.com\/(?:watch\?v=|embed\/|shorts\/)|youtu\.be\/)([\w-]{11})/);
    return m ? m[1] : null;
  }

  function renderUnits(L) {
    var box = el("units");
    if (!box) return;
    var html = "";
    var openIds = {};
    box.querySelectorAll("details[open]").forEach(function (dd) { openIds[dd.dataset.i] = true; });
    var first = !box.dataset.rendered;

    var unitN = 0;
    L.units.forEach(function (u, ui) {
      var utitle = tx(u.title);
      var num = u.num || String(++unitN);
      var items = visible(u.items).filter(function (it) {
        if (state.type !== "all" && it.type !== state.type) return false;
        if (!state.q) return true;
        return (utitle + " " + tx(it.title) + " " + tx(it.desc)).toLowerCase().indexOf(state.q) >= 0;
      });
      if (!items.length) return;
      var open = state.q || state.type !== "all" || openIds[ui];
      html += '<details class="unit" data-i="' + ui + '"' + (open ? " open" : "") + ">" +
        '<summary><span class="num">' + esc(num) + '</span><span class="u-title">' + esc(utitle) + "</span>" +
        '<span class="count">' + items.length + " " + esc(t("level.items")) + "</span>" + ICONS.chev + "</summary><ul>" +
        items.map(function (it) {
          var inner = '<span class="ico">' + (ICONS[it.type] || ICONS.resource) + "</span>" +
            '<span class="meta"><span class="t">' + esc(tx(it.title)) + "</span>" +
            (it.url ? (it.desc ? '<span class="d">' + esc(tx(it.desc)) + "</span>" : "") : '<span class="d">' + esc(t("level.soon")) + "</span>") +
            '</span><span class="kind">' + esc(t("kind." + it.type)) + "</span>";
          if (!it.url) return '<li><div class="item soon">' + inner + "</div></li>";
          var id = ytId(it.url);
          var attrs = id ? ' data-yt="' + id + '"' : ' target="_blank" rel="noopener"';
          var link = '<a class="item" href="' + esc(it.url) + '"' + attrs + ">" + inner + "</a>";
          if (it.download) return '<li class="has-dl">' + link + '<a class="dl" href="' + esc(it.url) + '" download title="' + esc(t("item.download")) + '" aria-label="' + esc(t("item.download")) + '">' + ICONS.download + "</a></li>";
          return "<li>" + link + "</li>";
        }).join("") + "</ul></details>";
    });
    if (!L.units.length) html = '<div class="coming-soon"><span class="cs-ico" aria-hidden="true">🚧</span><h2>' + esc(t("level.comingsoon")) +
      "</h2><p>" + esc(t("level.comingsoon.text")) + "</p></div>";
    box.innerHTML = html || '<p class="empty">' + esc(t("level.empty")) + "</p>";
    box.dataset.rendered = "1";
    typeset(box);
  }

  /* ---------- Racó PAU ---------- */
  var countdownTimer;
  function renderPau() {
    var P = window.PAU;
    if (!P) return;
    var cd = el("countdown");
    if (cd) {
      var target = new Date(P.date);
      var tick = function () {
        var ms = target - new Date();
        if (ms <= 0) { cd.innerHTML = '<p class="cd-done">' + esc(t("pau.done")) + "</p>"; clearInterval(countdownTimer); return; }
        var d = Math.floor(ms / 864e5), h = Math.floor(ms / 36e5) % 24, m = Math.floor(ms / 6e4) % 60, s = Math.floor(ms / 1e3) % 60;
        cd.innerHTML = [[d, "pau.days"], [h, "pau.hours"], [m, "pau.minutes"], [s, "pau.seconds"]].map(function (p) {
          return '<div class="cd-box"><span class="cd-n">' + p[0] + '</span><span class="cd-l">' + esc(t(p[1])) + "</span></div>";
        }).join("");
      };
      clearInterval(countdownTimer);
      tick();
      countdownTimer = setInterval(tick, 1000);
      var dl = el("pau-date");
      if (dl) dl.textContent = target.toLocaleDateString(DATE_LOCALE[lang], { weekday: "long", day: "numeric", month: "long", year: "numeric" }) +
        (P.confirmed ? "" : " · " + t("pau.date.note"));
    }

    var ex = el("pau-exams");
    if (ex) {
      var years = {};
      P.exams.forEach(function (e) { (years[e.year] = years[e.year] || []).push(e); });
      var link = function (url, key, icon) {
        return url
          ? '<a class="pill" href="' + esc(url) + '" target="_blank" rel="noopener">' + ICONS[icon] + esc(t(key)) + "</a>"
          : '<span class="pill soon" title="' + esc(t("level.soon")) + '">' + ICONS[icon] + esc(t(key)) + "</span>";
      };
      ex.innerHTML = Object.keys(years).sort(function (a, b) { return b - a; }).map(function (y) {
        return '<div class="year-card"><h3>' + y + "</h3>" + years[y].map(function (e) {
          return '<div class="conv"><span class="conv-name">' + esc(t("pau." + e.conv)) + "</span>" +
            '<span class="conv-links">' + link(e.exam, "pau.exam", "notes") + link(e.criteria, "pau.criteria", "exam") + "</span></div>";
        }).join("") + "</div>";
      }).join("");
    }
  }

  /* ---------- Reptes i curiositats ---------- */
  function publishedChallenges() {
    return (window.CHALLENGES || []).filter(function (c) { return parseDay(c.date) <= today(); })
      .sort(function (a, b) { return parseDay(b.date) - parseDay(a.date); });
  }

  function challengeHTML(c, big) {
    return '<article class="challenge' + (big ? " big" : "") + '">' +
      '<div class="ch-meta"><span class="tag">' + esc(tx(c.level)) + "</span>" +
      '<span class="ch-date">' + esc(t("ch.week")) + " " + esc(fmtDate(c.date)) + "</span></div>" +
      "<h3>" + esc(tx(c.title)) + "</h3>" +
      '<p class="ch-statement">' + esc(tx(c.statement)) + "</p>" +
      // reptes amb hideSolution: true no mostren la solució
      (c.hideSolution ? "" :
      '<details class="solution"><summary><span class="show">' + esc(t("ch.show")) + '</span><span class="hide">' + esc(t("ch.hide")) + "</span></summary>" +
      "<p>" + esc(tx(c.solution)) + "</p></details>") + "</article>";
  }

  function curiosityHTML(c) {
    return '<article class="curiosity"><span class="cu-ico" aria-hidden="true">💡</span><h3>' + esc(tx(c.title)) + "</h3><p>" + esc(tx(c.text)) + "</p></article>";
  }

  function renderChallenges() {
    var list = publishedChallenges();
    var cus = window.CURIOSITIES || [];

    var home = el("challenge-home");
    if (home) home.innerHTML = list.slice(0, 2).map(function (c, i) { return challengeHTML(c, i === 0); }).join("");
    var cuHome = el("curiosity-home");
    if (cuHome && cus.length) {
      // dues curiositats que van canviant cada setmana
      var week = Math.floor(today() / (7 * 864e5));
      var picks = [cus[week % cus.length]];
      if (cus.length > 1) picks.push(cus[(week + 1) % cus.length]);
      cuHome.innerHTML = picks.map(curiosityHTML).join("");
    }

    var cur = el("challenge-current");
    if (cur) cur.innerHTML = list.length ? challengeHTML(list[0], true) : "";
    var arch = el("challenge-archive");
    if (arch) arch.innerHTML = list.slice(1).map(function (c) { return challengeHTML(c, false); }).join("");
    var archWrap = el("archive-wrap");
    if (archWrap) archWrap.hidden = list.length < 2;
    var cuList = el("curiosities-list");
    if (cuList) cuList.innerHTML = cus.map(curiosityHTML).join("");
  }

  /* ---------- modal de vídeo ---------- */
  function setupVideoModal() {
    var dlg = el("video-modal");
    if (!dlg) return;
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest("a[data-yt]");
      if (!a || !dlg.showModal) return;
      e.preventDefault();
      dlg.querySelector(".frame").innerHTML =
        '<iframe src="https://www.youtube-nocookie.com/embed/' + a.getAttribute("data-yt") + '?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen title="Vídeo"></iframe>';
      dlg.showModal();
    });
    dlg.querySelector(".close").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener("close", function () { dlg.querySelector(".frame").innerHTML = ""; });
  }

  /* ---------- animació d'entrada ---------- */
  function setupReveal() {
    var els = document.querySelectorAll(".reveal:not(.in)");
    if (!("IntersectionObserver" in window)) { els.forEach(function (e) { e.classList.add("in"); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.1 });
    els.forEach(function (e) { io.observe(e); });
    // per seguretat: si alguna cosa no s'ha mostrat en 2 s, es mostra igualment
    setTimeout(function () { els.forEach(function (e) { e.classList.add("in"); }); }, 2000);
  }

  function renderAll() {
    renderHeader();
    renderFooter();
    renderContact();
    renderLevelCards();
    renderLevelPage();
    renderPau();
    renderChallenges();
    applyI18n();
    typeset(document.querySelector("main"));
  }

  renderAll();
  setupVideoModal();
  setupMailMenu();
  setupReveal();
})();
