---
title: Dimuon invariant mass from NanoAOD
status: active
last_verified: 2026-08-20
summary: >-
  A short notebook that opens a NanoAOD file with uproot, makes a couple of
  cuts, and plots the dimuon mass spectrum. Good as a first taste of the
  modern Python analysis stack.
audience: [high-school, undergrad-intro, undergrad-advanced]
languages: [en]
duration:
  min_minutes: 20
  max_minutes: 30
setup_burden: cloud-notebook
data:
  formats: [nanoaod]
  datasets: [nanoaod-2015]
prerequisites:
  physics: [invariant-mass]
  computing: [python-basics, awkward, matplotlib]
learning_goals:
  - Load a NanoAOD file with uproot and awkward
  - Apply simple event selections
  - Compute and plot invariant mass
physics_topics: [invariant-mass, standard-model]
computing_topics: [uproot, awkward, matplotlib, python-basics]
tags: []
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: CMS Open Data Workshop contributors
links:
  - {type: repo, url: "https://github.com/cms-opendata-workshop/workshop2026-lesson-dimuon-from-nanoaod", label: "Repository"}
  - {type: colab, url: "https://colab.research.google.com/github/cms-opendata-workshop/workshop2026-lesson-dimuon-from-nanoaod/blob/main/dimuon-nanoaod.ipynb", label: "Open in Colab"}
  - {type: binder, url: "https://mybinder.org/v2/gh/cms-opendata-workshop/workshop2026-lesson-dimuon-from-nanoaod/HEAD", label: "Open in Binder"}
---

The natural next step after a CSV-based activity: same physics, but now the
students are reading the same file format a CMS analyst would use, with the
same tools.

Short enough to run inside a single class period as a demonstration, or to
hand out as a twenty-minute exercise. The Binder link needs no account at all,
which makes it the better choice if your students do not have Google accounts.
