---
title: Visualising NanoAOD events in a notebook
status: active
last_verified: 2026-08-20
summary: >-
  Draw individual collision events from a NanoAOD file inside a Jupyter
  notebook. Students see the event, not just the histogram.
audience: [high-school, undergrad-intro, undergrad-advanced]
languages: [en]
duration:
  min_minutes: 15
  max_minutes: 25
setup_burden: cloud-notebook
data:
  formats: [nanoaod]
  datasets: [nanoaod-2015]
prerequisites:
  physics: [detectors]
  computing: [python-basics]
learning_goals:
  - Render a single CMS event from real data
  - Connect what a detector records to what a plot summarises
physics_topics: [detectors, standard-model]
computing_topics: [python-basics, uproot]
tags: []
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: Thomas McCauley
    affiliation: University of Notre Dame
links:
  - {type: repo, url: "https://github.com/cms-opendata-workshop/workshop2026-lesson-nanoaod-visualisation", label: "Repository"}
  - {type: colab, url: "https://colab.research.google.com/github/cms-opendata-workshop/workshop2026-lesson-nanoaod-visualisation/blob/master/workshop2026-ispynanoaod.ipynb", label: "Open in Colab"}
  - {type: binder, url: "https://mybinder.org/v2/gh/cms-opendata-workshop/workshop2026-lesson-nanoaod-visualisation/HEAD?urlpath=%2Fdoc%2Ftree%2Fworkshop2026-ispynanoaod.ipynb", label: "Open in Binder"}
---

Fifteen minutes, and it pairs naturally with any activity that produces a mass
spectrum. Students who have only seen histograms often do not connect them back
to individual collisions; this closes that gap.

Works well as a demonstration on a projector if you cannot get everyone onto a
machine.
