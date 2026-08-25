---
title: CMS Jupyter classroom materials
status: unmaintained
last_verified: 2026-08-20
summary: >-
  A full introductory sequence: Python and Jupyter from scratch, then several
  exercises on real CMS data. Translated into five languages.
audience: [high-school, undergrad-intro]
languages: [en, fi, sv, de, es, el]
duration:
  min_minutes: 120
  max_minutes: 480
  notes: A sequence rather than a single activity. Pick the notebooks you need.
setup_burden: cloud-notebook
data:
  formats: [csv, nanoaod]
  datasets: [dimuon-csv-2011]
prerequisites:
  physics: [invariant-mass]
  computing: []
learning_goals:
  - Get comfortable with Python and notebooks with no prior programming
  - Work through several independent CMS data exercises
  - Build up to a resonance measurement in stages
physics_topics: [invariant-mass, standard-model, statistics]
computing_topics: [python-basics, pandas, matplotlib]
tags: [multilingual]
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: Helsinki Institute of Physics and contributors
links:
  - {type: repo, url: "https://github.com/cms-opendata-education/cms-jupyter-materials-english", label: "English"}
  - {type: repo, url: "https://github.com/cms-opendata-education/cms-jupyter-materials-finnish", label: "Finnish"}
  - {type: repo, url: "https://github.com/cms-opendata-education/cms-jupyter-materials-swedish", label: "Swedish"}
  - {type: repo, url: "https://github.com/cms-opendata-education/cms-jupyter-materials-german", label: "German"}
  - {type: repo, url: "https://github.com/cms-opendata-education/cms-jupyter-materials-spanish", label: "Spanish"}
  - {type: repo, url: "https://github.com/cms-opendata-education/cms-jupyter-materials-greek", label: "Greek"}
---

The most complete beginner sequence in the collection, and the reason this
index needed a language facet at all. It assumes no programming background and
teaches Python alongside the physics rather than before it.

Written between 2017 and 2021 and no longer maintained. The physics and the
pedagogy hold up; the library versions in the notebooks may not, and the Greek
translation is incomplete. Expect to fix an import or two.

Listed as one record rather than six, since the translations are the same
sequence. If a translation diverges enough to need its own metadata, split it.
