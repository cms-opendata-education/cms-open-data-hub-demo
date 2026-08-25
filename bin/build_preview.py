#!/usr/bin/env python3
"""Build a single self-contained preview.html from the resource records.

Jekyll needs Ruby. This does not, so anyone can see the browse experience
after editing a record, and you can email the file to a colleague who will
open it by double-clicking. The CSS, JS, and catalog are all inlined.

    python bin/build_preview.py
"""

import json
import pathlib
import re
import datetime
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOCAB = yaml.safe_load((ROOT / "_data" / "vocab.yml").read_text())
OUT = ROOT / "preview.html"


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    raise TypeError(type(o))


def load_records():
    records = []
    for path in sorted((ROOT / "_resources").glob("*.md")):
        text = path.read_text()
        _, front, body = text.split("---", 2)
        meta = yaml.safe_load(front)
        meta["id"] = path.stem
        meta["url"] = "#" + path.stem
        meta["description_text"] = re.sub(r"\s+", " ", body).strip()
        records.append(meta)
    return records


def facet_block(records):
    """Sidebar HTML, built from the vocabularies exactly as Jekyll does."""
    rows = []

    rows.append(
        '<div class="filters__group">'
        '<span class="filters__legend">Most setup you can tolerate</span>'
        '<div class="slider-row"><input type="range" id="setupRange" min="0" max="5" '
        'step="1" value="5" aria-label="Maximum setup effort"></div>'
        '<div class="slider-value" id="setupValue" style="margin-top:4px">CMSSW</div></div>'
    )
    rows.append(
        '<div class="filters__group">'
        '<span class="filters__legend">Time available</span>'
        '<div class="slider-row"><input type="range" id="durationRange" min="0" max="4" '
        'step="1" value="4" aria-label="Maximum time needed"></div>'
        '<div class="slider-value" id="durationValue" style="margin-top:4px">Any</div></div>'
    )

    aud = ['<div class="filters__group"><span class="filters__legend">Audience</span>']
    for entry in VOCAB["audience"]:
        n = sum(1 for r in records if entry["id"] in (r.get("audience") or []))
        if not n:
            continue
        aud.append(
            f'<label><input type="checkbox" data-facet="audience" value="{entry["id"]}">'
            f'<span>{entry["label"]}</span><span class="count">{n}</span></label>'
        )
    aud.append("</div>")
    rows.append("".join(aud))

    langs = sorted({l for r in records for l in (r.get("languages") or [])})
    lang = ['<div class="filters__group"><span class="filters__legend">Language</span>']
    for l in langs:
        n = sum(1 for r in records if l in (r.get("languages") or []))
        lang.append(
            f'<label><input type="checkbox" data-facet="languages" value="{l}">'
            f'<span>{l.upper()}</span><span class="count">{n}</span></label>'
        )
    lang.append("</div>")
    rows.append("".join(lang))

    st = ['<div class="filters__group"><span class="filters__legend">Maintenance status</span>']
    for entry in VOCAB["status"]:
        checked = "" if entry["id"] == "archived" else " checked"
        st.append(
            f'<label title="{entry["note"]}"><input type="checkbox" data-facet="status" '
            f'value="{entry["id"]}"{checked}><span>{entry["label"]}</span></label>'
        )
    st.append("</div>")
    rows.append("".join(st))

    return "".join(rows)



def strip_liquid(text):
    """Crude Liquid stripper: good enough for the two static pages we mirror."""
    import re
    text = re.sub(r"^---.*?---", "", text, count=1, flags=re.S)
    return text


def home_view():
    spectrum = (ROOT / "_includes" / "spectrum.html").read_text()
    src = (ROOT / "index.html").read_text()
    body = strip_liquid(src)
    body = body.replace("{% include spectrum.html %}", spectrum)

    # Liquid url filters become in-page view switches.
    def to_hash(m):
        return "#browse" + m.group(1)[len("/browse/"):]

    body = re.sub(r"\{\{ '(/browse/[^']*)' \| relative_url \}\}", to_hash, body)
    body = body.replace('href="#browse', 'data-view="browse" href="#browse')
    body = re.sub(r"\{%.*?%\}", "", body, flags=re.S)
    body = re.sub(r"\{\{.*?\}\}", "", body, flags=re.S)
    return body


def data_view():
    datasets = yaml.safe_load((ROOT / "_data" / "datasets.yml").read_text())
    records = load_records()
    out = ['<div class="wrap" style="max-width:820px;padding-top:44px;padding-bottom:64px">',
           "<h1>Which data should I use?</h1>",
           '<p style="font-size:1.1rem;color:var(--ink-2)">Every CMS dataset is documented '
           "on the CERN Open Data Portal, and we do not duplicate that here. What is missing "
           "there is a way to answer the question people actually arrive with: given what I "
           "want to do, where do I start?</p>"]
    for key, d in datasets.items():
        users = [r for r in records if key in ((r.get("data") or {}).get("datasets") or [])]
        pills = "".join(f'<span class="pill">{d[k]}</span>'
                        for k in ("run_period", "energy", "size") if d.get(k))
        used = ""
        if users:
            links = " &middot; ".join(
                f'<a href="#browse" data-view="browse">{u["title"]}</a>' for u in users)
            used = ('<div style="border-top:1px solid var(--rule-soft);padding-top:12px;'
                    'font-family:var(--f-mono);font-size:.76rem">'
                    '<span style="color:var(--ink-3)">used by</span> ' + links + "</div>")
        out.append(
            f'<div id="{key}" style="background:var(--card);border:1px solid var(--rule);'
            f'border-radius:var(--r);padding:22px 24px;margin:18px 0">'
            f'<div style="display:flex;align-items:baseline;gap:12px;flex-wrap:wrap">'
            f'<h2 style="margin:0">{d["title"]}</h2>{pills}</div>'
            f'<p style="color:var(--ink-2);margin:12px 0 14px">{d["blurb"]}</p>'
            f'<p style="margin:0 0 14px"><a href="{d["portal"]}">'
            f'Documentation on the Open Data Portal &rarr;</a></p>{used}</div>')
    out.append('<p class="section-rule">Reference, not tutorial</p>')
    out.append("<p>The <a href='https://cms-opendata-guide.web.cern.ch/'>CMS Open Data Guide"
               "</a> is the authoritative description of formats, objects, and corrections. "
               "Treat it as a dictionary: excellent when you know the word you are looking up, "
               "hard going if you are trying to read it front to back. Come here to find out "
               "which page you need, then go there.</p>")
    out.append("</div>")
    return "".join(out)


def contribute_view():
    src = (ROOT / "contribute.html").read_text()
    body = strip_liquid(src)
    body = body.replace("{{ site.contact_email }}", "cms-dpoa-coordinator@cern.ch")
    body = re.sub(r"\{\{ site\.repo \}\}", "https://github.com/cms-opendata-education/hub", body)
    body = re.sub(r"\{%.*?%\}", "", body, flags=re.S)
    body = re.sub(r"\{\{.*?\}\}", "", body, flags=re.S)
    return body


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CMS Open Data Hub &mdash; offline preview</title>
<style>{css}</style>
</head>
<body>

<header class="masthead">
  <div class="wrap masthead__inner">
    <a class="masthead__title" href="#home" data-view="home">CMS Open Data<span>&nbsp;/</span>&nbsp;Hub</a>
    <nav class="masthead__nav">
      <a href="#home" data-view="home">Home</a>
      <a href="#browse" data-view="browse">Browse</a>
      <a href="#data" data-view="data">Data</a>
      <a href="#contribute" data-view="contribute">Contribute</a>
    </nav>
  </div>
</header>

<div class="view is-active" id="view-home">{home}</div>

<div class="view" id="view-browse">
  <div class="wrap" style="padding-top:34px">
    <h1 style="margin-bottom:6px">Browse the catalog</h1>
    <p style="color:var(--ink-2);max-width:60ch;margin:0">
      {count} records, filtered entirely in the browser. Drag the setup slider
      down to see what a teacher with no reliable computers is left with.
    </p>
  </div>
  <div class="wrap browse" data-catalog>
    <div class="filters">
      <button class="filters__toggle" type="button">Filters</button>
      <div class="filters__panel">{facets}</div>
    </div>
    <div>
      <input class="search-box" type="search" id="q"
             placeholder="Search titles, topics, and goals" aria-label="Search resources">
      <div class="results__bar">
        <span id="resultCount"></span>
        <button class="linkish" id="reset" type="button">Clear filters</button>
      </div>
      <div class="cards" id="results"></div>
    </div>
  </div>
</div>

<div class="view" id="view-data">{data}</div>
<div class="view" id="view-contribute">{contribute}</div>

<footer class="foot">
  <div class="wrap foot__row">
    <span>Offline preview generated by bin/build_preview.py.</span>
    <span>The deployed site has a real page per resource.</span>
  </div>
</footer>

<script>window.CATALOG = {catalog};</script>
<script>{js}</script>
<script>
(function () {{
  function show(name) {{
    document.querySelectorAll(".view").forEach(function (v) {{
      v.classList.toggle("is-active", v.id === "view-" + name);
    }});
    document.querySelectorAll(".masthead__nav a").forEach(function (a) {{
      if (a.dataset.view === name) a.setAttribute("aria-current", "page");
      else a.removeAttribute("aria-current");
    }});
    window.scrollTo(0, 0);
  }}

  document.addEventListener("click", function (e) {{
    var nav = e.target.closest("[data-view]");
    if (nav) {{
      e.preventDefault();
      var href = nav.getAttribute("href") || "";
      var qs = href.indexOf("?") > -1 ? href.slice(href.indexOf("?")) : "";
      show(nav.dataset.view);
      if (qs && window.CatalogApplyQuery) window.CatalogApplyQuery(qs);
      return;
    }}
    var card = e.target.closest(".card__title a");
    if (card) {{
      e.preventDefault();
      var r = window.CATALOG.resources.find(function (x) {{ return x.id === card.dataset.id; }});
      if (!r) return;
      var goals = (r.learning_goals || []).map(function (g) {{
        return "<li>" + g + "</li>"; }}).join("");
      document.getElementById("detail").innerHTML =
        "<h2 style='margin-bottom:4px'>" + r.title + "</h2>" +
        "<p style='color:var(--ink-2)'>" + r.summary + "</p>" +
        "<p>" + r.description_text + "</p>" +
        (goals ? "<p class='section-rule'>What students take away</p><ul>" + goals + "</ul>" : "") +
        "<p style='font-family:var(--f-mono);font-size:.74rem;color:var(--ink-3)'>" +
        "On the deployed site this is a page at /resource/" + r.id + "/</p>" +
        "<button class='btn btn--ghost' id='closeDetail'>Close</button>";
      document.getElementById("overlay").style.display = "flex";
      document.getElementById("closeDetail").addEventListener("click", function () {{
        document.getElementById("overlay").style.display = "none";
      }});
    }}
  }});
}})();
</script>

<div id="overlay" style="display:none;position:fixed;inset:0;background:rgba(22,24,29,.55);
     align-items:flex-start;justify-content:center;padding:6vh 20px;z-index:50;overflow:auto"
     onclick="if(event.target===this)this.style.display='none'">
  <div id="detail" style="background:#fff;max-width:620px;width:100%;padding:30px 32px;
       border-radius:3px"></div>
</div>

</body>
</html>
"""


def main():
    records = load_records()
    css = (ROOT / "assets" / "css" / "main.css").read_text()
    js = (ROOT / "assets" / "js" / "catalog.js").read_text()
    ladder = [{"id": s["id"], "label": s["label"], "note": s["note"]}
              for s in VOCAB["setup_burden"]]
    payload = {"ladder": ladder, "resources": records}
    html = TEMPLATE.format(
        css=css,
        js=js,
        catalog=json.dumps(payload, default=default),
        facets=facet_block(records),
        count=len(records),
        home=home_view(),
        data=data_view(),
        contribute=contribute_view(),
    )
    OUT.write_text(html)
    print(f"Wrote {OUT.relative_to(ROOT)} with {len(records)} records.")


if __name__ == "__main__":
    main()
