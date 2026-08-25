---
title: MiniParT, a transformer for CMS jet classification
status: active
last_verified: 2026-08-20
summary: >-
  Build a small transformer from scratch in PyTorch and train it to tell
  H to bb, H to cc, and QCD jets apart. Trains in minutes on free Colab.
audience: [undergrad-advanced, graduate]
languages: [en]
duration:
  min_minutes: 120
  max_minutes: 180
setup_burden: cloud-notebook
data:
  formats: [nanoaod, simulation]
  datasets: [nanoaod-2015]
prerequisites:
  physics: [jets, higgs]
  computing: [python-basics, machine-learning]
learning_goals:
  - Understand what a jet is and how H to bb or cc appears in CMS data
  - Build embeddings, self-attention, and multi-head attention from scratch
  - Train an end-to-end classifier in PyTorch
  - Evaluate with ROC curves and AUC, and see where the physics makes it hard
physics_topics: [jets, higgs, detectors]
computing_topics: [machine-learning, python-basics]
tags: []
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: CMS Open Data Workshop contributors
links:
  - {type: lesson, url: "https://cms-opendata-workshop.github.io/workshop2026-lesson-minipart/index.html", label: "Lesson page"}
  - {type: slides, url: "https://docs.google.com/presentation/d/1VpzyGB5RC7H1AIULSVKxc82TsBFVA6G-iJT_djkx3nY", label: "Slides"}
---

A scaled-down version of the Particle Transformer used in real CMS analyses,
small enough to train in minutes on a free Colab session but built on the
same architecture.

No prior neural network experience is assumed, but the pace is brisk. Advanced
high school students with Python and some linear algebra can follow it; it is
scoped for undergraduates.

The most valuable part pedagogically may be the end, where the model plateaus
and students have to reason about why charm tagging is physically harder than
bottom tagging rather than reaching for a bigger network.
