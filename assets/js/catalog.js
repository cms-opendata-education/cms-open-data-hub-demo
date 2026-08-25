/* Catalog browse: plain JS, no build step, no search service.
   At a few hundred records this is faster than any index we could ship,
   and there is nothing to break or expire.

   Data source: window.CATALOG if preloaded (offline preview), else
   catalog.json fetched relative to the page. */

(function () {
  "use strict";

  /* Filled from the catalog payload so the ladder can be reordered or
     extended by editing _data/vocab.yml alone. */
  var LADDER = [];
  var LADDER_LABEL = {};

  var AUDIENCE_LABEL = {
    "middle-school": "Middle school",
    "high-school": "High school",
    "undergrad-intro": "Undergrad, intro",
    "undergrad-advanced": "Undergrad, advanced",
    "graduate": "Graduate",
    "researcher": "Researcher",
    "teacher-development": "Teacher PD",
    "general-public": "General public"
  };
  var LANG_LABEL = {
    en: "English", fi: "Finnish", sv: "Swedish", de: "German",
    es: "Spanish", el: "Greek", fr: "French", it: "Italian"
  };
  var DURATION_STOPS = [30, 60, 120, 240, 100000];
  var DURATION_LABEL = ["30 min", "1 hour", "2 hours", "4 hours", "Any"];

  var state = {
    q: "",
    audience: [],
    languages: [],
    status: ["active", "community", "unmaintained"],
    maxSetup: 5,
    maxDuration: 4
  };

  var records = [];
  var root;

  /* ---------- helpers ---------- */

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function setupLevel(r) {
    var i = LADDER.indexOf(r.setup_burden);
    return i < 0 ? LADDER.length - 1 : i;
  }

  function shortestDuration(r) {
    if (!r.duration) return 0;
    return r.duration.min_minutes || 0;
  }

  function durationText(r) {
    if (!r.duration || !r.duration.min_minutes) return "unspecified";
    var lo = r.duration.min_minutes, hi = r.duration.max_minutes;
    function fmt(m) { return m >= 120 ? Math.round(m / 60) + " hr" : m + " min"; }
    if (hi && hi !== lo) return fmt(lo) + "\u2013" + fmt(hi);
    return fmt(lo) + "+";
  }

  function ladderHTML(level) {
    var out = '<span class="ladder" aria-hidden="true">';
    for (var i = 0; i < LADDER.length; i++) {
      var cls = "ladder__rung ladder__rung--n" + i;
      if (i < level) cls += " is-below";
      if (i === level) cls += " is-at";
      out += '<span class="' + cls + '"></span>';
    }
    return out + "</span>";
  }

  /* ---------- filtering ---------- */

  function matches(r) {
    if (state.status.indexOf(r.status) === -1) return false;
    if (setupLevel(r) > state.maxSetup) return false;
    if (shortestDuration(r) > DURATION_STOPS[state.maxDuration]) return false;

    if (state.audience.length) {
      var hit = false;
      for (var i = 0; i < state.audience.length; i++) {
        if ((r.audience || []).indexOf(state.audience[i]) > -1) { hit = true; break; }
      }
      if (!hit) return false;
    }

    if (state.languages.length) {
      var lhit = false;
      for (var j = 0; j < state.languages.length; j++) {
        if ((r.languages || []).indexOf(state.languages[j]) > -1) { lhit = true; break; }
      }
      if (!lhit) return false;
    }

    if (state.q) {
      if (r._haystack.indexOf(state.q.toLowerCase()) === -1) return false;
    }
    return true;
  }

  /* ---------- rendering ---------- */

  function cardHTML(r) {
    var level = setupLevel(r);
    var aud = (r.audience || []).map(function (a) {
      return AUDIENCE_LABEL[a] || a;
    }).join(", ");

    var langs = "";
    if ((r.languages || []).length > 1) {
      langs = '<span><span class="k">languages</span> ' + r.languages.length + "</span>";
    }

    return '' +
      '<article class="card">' +
        '<div class="card__head">' +
          '<h3 class="card__title"><a href="' + esc(r.url) + '" data-id="' + esc(r.id) + '">' +
            esc(r.title) + "</a></h3>" +
          '<span class="chip chip--' + esc(r.status) + '">' + esc(r.status) + "</span>" +
        "</div>" +
        '<p class="card__summary">' + esc(r.summary) + "</p>" +
        '<div class="card__meta">' +
          '<span class="ladder-line">' + ladderHTML(level) +
            esc(LADDER_LABEL[r.setup_burden] || r.setup_burden) + "</span>" +
          '<span><span class="k">for</span> ' + esc(aud) + "</span>" +
          '<span><span class="k">takes</span> ' + esc(durationText(r)) + "</span>" +
          langs +
        "</div>" +
      "</article>";
  }

  function render() {
    var hits = records.filter(matches);
    var list = root.querySelector("#results");
    var bar = root.querySelector("#resultCount");

    bar.innerHTML = "<strong>" + hits.length + "</strong> of " + records.length + " resources";

    if (!hits.length) {
      list.innerHTML =
        '<div class="empty"><h3>Nothing matches those filters</h3>' +
        "<p>Try allowing more setup effort, or clear the filters and start again.</p></div>";
      return;
    }

    hits.sort(function (a, b) {
      var d = setupLevel(a) - setupLevel(b);
      return d !== 0 ? d : a.title.localeCompare(b.title);
    });

    list.innerHTML = hits.map(cardHTML).join("");
  }

  /* ---------- sidebar, built from the catalog payload ----------
     Rendering facets here rather than in Liquid means the deployed site and
     the offline preview run identical code. A template error can no longer
     break one while the other looks fine. */

  function buildFacets(vocab) {
    var panel = root.querySelector(".filters__panel");
    if (!panel) return;

    var top = LADDER.length - 1;
    var html = "";

    html +=
      '<div class="filters__group">' +
        '<span class="filters__legend">Most setup you can tolerate</span>' +
        '<div class="slider-row"><input type="range" id="setupRange" min="0" max="' +
          top + '" step="1" value="' + top + '" aria-label="Maximum setup effort"></div>' +
        '<div class="slider-value" id="setupValue" style="margin-top:4px">' +
          esc(LADDER_LABEL[LADDER[top]]) + "</div></div>";

    html +=
      '<div class="filters__group">' +
        '<span class="filters__legend">Time available</span>' +
        '<div class="slider-row"><input type="range" id="durationRange" min="0" max="4" ' +
          'step="1" value="4" aria-label="Maximum time needed"></div>' +
        '<div class="slider-value" id="durationValue" style="margin-top:4px">Any</div></div>';

    html += '<div class="filters__group"><span class="filters__legend">Audience</span>';
    (vocab.audience || []).forEach(function (a) {
      var n = records.filter(function (r) {
        return (r.audience || []).indexOf(a.id) > -1;
      }).length;
      if (!n) return;
      html += '<label><input type="checkbox" data-facet="audience" value="' + esc(a.id) +
        '"><span>' + esc(a.label) + '</span><span class="count">' + n + "</span></label>";
    });
    html += "</div>";

    var seen = {};
    records.forEach(function (r) {
      (r.languages || []).forEach(function (l) { seen[l] = (seen[l] || 0) + 1; });
    });
    var langs = Object.keys(seen).sort();
    if (langs.length > 1) {
      html += '<div class="filters__group"><span class="filters__legend">Language</span>';
      langs.forEach(function (l) {
        html += '<label><input type="checkbox" data-facet="languages" value="' + esc(l) +
          '"><span>' + esc((LANG_LABEL[l] || l).toString()) +
          '</span><span class="count">' + seen[l] + "</span></label>";
      });
      html += "</div>";
    }

    html += '<div class="filters__group"><span class="filters__legend">Maintenance status</span>';
    (vocab.status || []).forEach(function (s) {
      var on = s.id === "archived" ? "" : " checked";
      html += '<label title="' + esc(s.note) + '"><input type="checkbox" data-facet="status" value="' +
        esc(s.id) + '"' + on + "><span>" + esc(s.label) + "</span></label>";
    });
    html += "</div>";

    panel.innerHTML = html;
  }

  /* ---------- wiring ---------- */

  function readCheckboxes(name) {
    var out = [];
    root.querySelectorAll('input[data-facet="' + name + '"]:checked').forEach(function (el) {
      out.push(el.value);
    });
    return out;
  }

  function bind() {
    var q = root.querySelector("#q");
    if (q) {
      q.addEventListener("input", function () {
        state.q = q.value.trim();
        render();
      });
    }

    root.querySelectorAll('input[data-facet]').forEach(function (el) {
      el.addEventListener("change", function () {
        var f = el.getAttribute("data-facet");
        state[f] = readCheckboxes(f);
        render();
      });
    });

    var setup = root.querySelector("#setupRange");
    if (setup) {
      setup.addEventListener("input", function () {
        state.maxSetup = parseInt(setup.value, 10);
        root.querySelector("#setupValue").textContent = LADDER_LABEL[LADDER[state.maxSetup]];
        render();
      });
    }

    var dur = root.querySelector("#durationRange");
    if (dur) {
      dur.addEventListener("input", function () {
        state.maxDuration = parseInt(dur.value, 10);
        root.querySelector("#durationValue").textContent = DURATION_LABEL[state.maxDuration];
        render();
      });
    }

    var reset = root.querySelector("#reset");
    if (reset) {
      reset.addEventListener("click", function () {
        root.querySelectorAll('input[data-facet]').forEach(function (el) {
          el.checked = el.getAttribute("data-facet") === "status" &&
            el.value !== "archived";
        });
        if (q) q.value = "";
        var top = LADDER.length - 1;
        if (setup) setup.value = String(top);
        if (dur) dur.value = 4;
        state = {
          q: "", audience: [], languages: [],
          status: ["active", "community", "unmaintained"],
          maxSetup: top, maxDuration: 4
        };
        root.querySelector("#setupValue").textContent = LADDER_LABEL[LADDER[top]];
        root.querySelector("#durationValue").textContent = "Any";
        render();
      });
    }

    var toggle = root.querySelector(".filters__toggle");
    if (toggle) {
      toggle.addEventListener("click", function () {
        root.querySelector(".filters__panel").classList.toggle("is-open");
      });
    }
  }

  /* Query params let the front page hand off a preset, e.g.
     browse/?audience=high-school&setup=2 */
  function applyQuery() {
    applyQueryString(window.location.search);
  }

  function applyQueryString(search) {
    var p = new URLSearchParams(search || "");
    if (!p.toString()) return;

    var aud = p.getAll("audience");
    if (aud.length) {
      state.audience = aud;
      root.querySelectorAll('input[data-facet="audience"]').forEach(function (el) {
        el.checked = aud.indexOf(el.value) > -1;
      });
    }
    if (p.has("setup")) {
      state.maxSetup = parseInt(p.get("setup"), 10);
      var s = root.querySelector("#setupRange");
      if (s) { s.value = state.maxSetup; }
      var sv = root.querySelector("#setupValue");
      if (sv) sv.textContent = LADDER_LABEL[LADDER[state.maxSetup]];
    }
    if (p.has("duration")) {
      state.maxDuration = parseInt(p.get("duration"), 10);
      var d = root.querySelector("#durationRange");
      if (d) { d.value = state.maxDuration; }
      var dv = root.querySelector("#durationValue");
      if (dv) dv.textContent = DURATION_LABEL[state.maxDuration];
    }
    if (p.has("q")) {
      state.q = p.get("q");
      var qi = root.querySelector("#q");
      if (qi) qi.value = state.q;
    }
  }

  function prepare(payload) {
    var data = Array.isArray(payload) ? payload : payload.resources;
    var ladder = Array.isArray(payload) ? [] : (payload.ladder || []);

    LADDER = ladder.map(function (s) { return s.id; });
    ladder.forEach(function (s) { LADDER_LABEL[s.id] = s.label; });
    state.maxSetup = Math.max(0, LADDER.length - 1);
    state.status = ((payload.vocab || {}).status || [])
      .filter(function (s) { return s.id !== "archived"; })
      .map(function (s) { return s.id; });

    records = (data || []).map(function (r) {
      var parts = [r.title, r.summary, (r.audience || []).join(" "),
        (r.physics_topics || []).join(" "), (r.computing_topics || []).join(" "),
        (r.tags || []).join(" "), (r.learning_goals || []).join(" "),
        (r.description_text || "")];
      r._haystack = parts.join(" ").toLowerCase();
      return r;
    });
    buildFacets(payload.vocab || {});
    applyQuery();
    bind();
    render();
  }

  function init() {
    root = document.querySelector("[data-catalog]");
    if (!root) return;

    if (window.CATALOG) {
      prepare(window.CATALOG);
      return;
    }
    var src = root.getAttribute("data-catalog") || "catalog.json";
    fetch(src)
      .then(function (res) {
        if (!res.ok) throw new Error(res.status);
        return res.json();
      })
      .then(prepare)
      .catch(function () {
        root.querySelector("#results").innerHTML =
          '<div class="empty"><h3>The catalog did not load</h3>' +
          "<p>Reload the page. If it keeps happening, open an issue in the site repository.</p></div>";
      });
  }

  window.CatalogInit = init;
  window.CatalogApplyQuery = function (search) {
    var saved = window.location.search;
    try {
      Object.defineProperty(window, "__q", { value: search, configurable: true });
    } catch (e) { /* ignore */ }
    applyQueryString(search);
    render();
    return saved;
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
