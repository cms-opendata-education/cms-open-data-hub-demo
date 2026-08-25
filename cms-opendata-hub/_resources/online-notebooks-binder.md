---
title: Online notebooks that read the Portal directly
status: unmaintained
last_verified: 2026-08-20
summary: >-
  Notebooks that stream data straight from the CERN Open Data Portal and
  launch in Binder. Nothing downloaded, no account needed.
audience: [high-school, undergrad-intro, general-public]
languages: [en]
duration:
  min_minutes: 20
  max_minutes: 45
setup_burden: cloud-notebook
data:
  formats: [csv, nanoaod]
  datasets: [dimuon-csv-2011]
prerequisites:
  physics: [invariant-mass]
  computing: [python-basics]
learning_goals:
  - Run a real analysis without installing or downloading anything
  - See how data can be streamed rather than copied
physics_topics: [invariant-mass, standard-model]
computing_topics: [python-basics, matplotlib]
tags: []
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: CMS open data education contributors
links:
  - {type: repo, url: "https://github.com/cms-opendata-education/cms-online-notebooks-for-binder", label: "Repository"}
---

The Binder route matters more than it looks: Colab requires a Google account,
and a significant number of school districts block Google sign-in for students
or forbid it outright. These notebooks need no account at all.

The oldest material in the collection, last touched in 2019, and Binder builds
for old environments can be slow or fail. Launch it yourself the day before
rather than in front of a class.
