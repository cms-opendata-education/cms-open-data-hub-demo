---
title: Particle Discovery Lab
status: active
last_verified: 2026-08-20
summary: >-
  A full modern-physics lab: reconstruct an unknown particle from dimuon data,
  fit and subtract the background, propagate uncertainties, and identify what
  you found.
audience: [undergrad-intro, undergrad-advanced]
languages: [en]
duration:
  min_minutes: 120
  max_minutes: 360
  notes: Configurable. Three lab periods for the full version as written.
setup_burden: local-python
data:
  formats: [csv]
  datasets: [dimuon-csv-2011]
prerequisites:
  physics: [special-relativity, invariant-mass, conservation-laws]
  computing: [python-basics, matplotlib]
learning_goals:
  - Apply relativistic energy and momentum conservation correctly
  - Handle Poisson-distributed data in histograms
  - Perform and evaluate polynomial background fits
  - Propagate uncertainty through a multi-step analysis
  - Compare a measured mass and width against published values
physics_topics: [invariant-mass, special-relativity, statistics, standard-model]
computing_topics: [python-basics, matplotlib, matlab]
tags: [instructor-guide]
instructor_materials: true
license: CC-BY-4.0
authors:
  - name: Bethel University Physics
links:
  - {type: homepage, url: "https://bethel-physics.github.io/ParticleDiscoveryLab/", label: "Student-facing activity"}
  - {type: portal, url: "https://opendata.cern.ch/record/49", label: "Portal record"}
  - {type: instructor, url: "https://github.com/bethel-physics/ParticleDiscoveryLab/tree/instructors", label: "Instructor branch"}
  - {type: colab, url: "https://colab.research.google.com/drive/1aK6INkWrF_6mlDEYU4RxMYMhYm-8O7MF", label: "Student Colab"}
---

This is the most substantial undergraduate lab in the collection and the one
that most closely resembles a real analysis. Students are not told which
particle they are looking for; they reconstruct it, measure its mass and
width, and identify it themselves.

Student code is provided in both MATLAB and Python, and no CMS-specific
software is required. A Colab version exists if local installation is a
problem, though the lab is written assuming a local environment.

Uncertainty propagation runs through every step rather than being bolted on
at the end, which makes this a good fit for a course where error analysis is
a learning objective in its own right.
