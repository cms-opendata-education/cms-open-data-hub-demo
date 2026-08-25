# CMS Open Data hub — scaffold

A findability layer over CMS open data educational and research material.
It does not host lessons and it does not rewrite documentation. It is an index
of records pointing at material wherever that material already lives.

Twenty-two records are included with live links: the six activities from the
2026 workshop, the material sitting in the `cms-opendata-education` org, and
six research pathways pointing into the CERN Open Data Portal's own
getting-started pages.

## Run it

**Editing content — no Ruby needed.** Edit a file in `_resources/`, then:

```bash
make preview     # validates, then rebuilds preview.html
```

Open `preview.html`. It is one self-contained file with the CSS, JavaScript,
and whole catalog inlined, so it also works if you email it to someone. All
four pages are there; navigation switches views in place.

**Working on the site itself — Ruby needed.** The preview approximates the
layout but is not the real thing. For anything touching templates, the resource
pages, or navigation:

```bash
bundle install          # once
make serve              # http://localhost:4000/hub/
```

**Before opening a pull request:**

```bash
make check              # schema and vocabulary validation
```

## Deploying to GitHub Pages

Settings, then Pages, then "Deploy from a branch": pick `main` and folder `/`.
GitHub runs Jekyll for you; no Action is required for the build.

One thing will bite you if you skip it. `baseurl` in `_config.yml` must match
the repository name:

| Repository | `baseurl` |
| --- | --- |
| `cms-opendata-education/hub` | `"/hub"` |
| `cms-opendata-education/opendata-hub` | `"/opendata-hub"` |
| `cms-opendata-education/cms-opendata-education.github.io` | `""` |

Get it wrong and every stylesheet, script, and internal link 404s while the
front page still renders as unstyled text, which is a confusing failure to
diagnose. `preview.html` is excluded from the build, so it will not be
deployed.

If you later need a plugin outside the GitHub Pages allow-list, switch to
"GitHub Actions" as the Pages source and build with the standard Jekyll
workflow. Nothing else about the repository has to change.

## How it is put together

```
_resources/*.md      one record per resource — YAML front matter + description
_data/vocab.yml      controlled vocabularies; CI rejects terms not listed here
_data/datasets.yml   datasets, so records can cross-link to the data they need
_data/testimonials.yml  keyed by resource id
catalog.json         Liquid template that emits the whole catalog at build time
assets/js/catalog.js filters client-side; no search service, no index, no keys
bin/validate.py      schema and vocabulary checks
bin/build_preview.py offline preview builder
```

Three decisions worth knowing about, because they are the ones that keep this
maintainable by two or three people.

**A record is not a repository.** One central catalog holds every record
regardless of where the material lives. Some of the best material is not ours —
QuarkNet's Quark Workbench, Bethel's Particle Discovery Lab, the Portal's own
getting-started pages — and could never carry a file we control. Distributing
metadata into per-resource repositories would still need a central registry to
build from, so it buys nothing on day one and costs a network dependency at
build time plus schema drift across thirty repositories. If we want repositories
to own their own metadata later, a scheduled Action can sync them in; the site
never has to know the difference.

**Vocabularies are controlled and enforced.** Free-form tags reliably decay into
`ml` / `machine-learning` / `ML` / `deep-learning`, at which point filters
silently lie to people. Adding a term is a one-line pull request against
`_data/vocab.yml`, and CI blocks any record using a term that is not there.

**Setup burden is an ordered ladder, not a set of checkboxes.** It is the field
teachers filter on hardest, so it gets a slider that means "this or easier" and
a rung indicator on every card. Seven rungs: no computer needed, web page only,
spreadsheet, cloud notebook, local Python, local ROOT, CMSSW.

The first two rungs are separate on purpose. "Nothing to install" collapses two
very different situations: a printed puzzle that works when the lab machines are
broken, and a Colab notebook that needs a Google account many school districts
block. The slider and the rung count are both driven by `_data/vocab.yml`, so
reordering or inserting a rung is a one-file edit.

## Unmaintained is a label, not a reason to hide something

`cms-spreadsheet-materials-multiple-languages` has not been touched since 2017,
has no maintainer, and exists in six languages. It is also the only activity in
the collection that a teacher with no reliable computers can run next week, and
it was effectively invisible. So `status` has four values rather than two, every
record carries a `last_verified` date shown on the page, and only `archived`
drops out of search by default.

A rough activity someone can find beats a perfect one they cannot.

## Contributions

Two paths, deliberately. A GitHub issue form for people who have an account, and
an email address for people who do not; a maintainer converts either into a
record. Testimonials live in their own file per resource so two submissions
landing at once cannot conflict, and so they can carry a much lower review bar
than a resource record.

The monthly CI job runs a link checker and opens an issue listing anything
broken. Given how much of the material lives on Google Drive and Colab, this
turns link rot from a vigilance problem into a triage problem.

## Open questions for DPOA

The schema is deliberately not optimised yet. Worth arguing about:

1. **Scope.** Education plus research pathways in one index, as built here, or
   two separate collections? The front page currently offers two doors that just
   preset filters over one catalog, on the theory that the boundary is blurry —
   a senior thesis student is both.
1. **The spectrum hero.** The front page opens with the dimuon mass spectrum
   because it is the plot most of these activities build toward. It may read as
   intimidating rather than inviting to a teacher who has never taught this.
   Worth testing on someone from the workshop.
2. **Language as a facet.** Six languages already exist in the org. Should
   translations be separate records or a field on one record? Currently a field.
3. **Does `learning_goals` need structure**, or is free text right? Free text is
   easier to write and harder to search.
4. **Granularity.** `cms-jupyter-materials-english` contains many distinct
   exercises. One record or several?
5. **Who holds the keys** once this moves under CERN, and what is the review bar
   for a new record.
