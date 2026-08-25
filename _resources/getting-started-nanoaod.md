---
title: Getting started with CMS NanoAOD
status: active
last_verified: 2026-08-20
summary: >-
  The Portal's own walkthrough for Run 2 NanoAOD. The right starting point
  for a student project that needs more than CSV files but should not need
  a container.
audience: [undergrad-advanced, graduate, researcher]
languages: [en]
duration:
  min_minutes: 60
  max_minutes: 240
  notes: Reading and first working example. Budget longer for a real project.
setup_burden: local-python
data:
  formats: [nanoaod]
  datasets: [nanoaod-2015]
prerequisites:
  physics: [detectors]
  computing: [python-basics, uproot, root]
learning_goals:
  - Locate and stream a NanoAOD dataset from the Portal
  - Understand what NanoAOD does and does not contain
  - Run a first selection without installing CMSSW
physics_topics: [detectors, standard-model]
computing_topics: [uproot, root, python-basics]
tags: [research-pathway, reference]
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: CERN Open Data Portal
links:
  - {type: portal, url: "https://opendata.cern.ch/docs/cms-getting-started-nanoaod", label: "Getting started with NanoAOD"}
  - {type: reference, url: "https://cms-opendata-guide.web.cern.ch/", label: "CMS Open Data Guide"}
---

We do not host this. It lives on the CERN Open Data Portal and is maintained
there. It is indexed here because it is genuinely hard to find unless you
already know it exists, and because it is the correct answer to the single
most common question from someone starting an undergraduate research project.

Start here if your students have outgrown CSV files but you do not want to
take on a container. NanoAOD is flat ROOT, readable with uproot, and covers
most of what an undergraduate project needs.

Go to MiniAOD instead only when you have identified a specific variable that
NanoAOD does not carry.
