---
title: Getting started with CMS AOD
status: active
last_verified: 2026-08-20
summary: >-
  The Portal's walkthrough for Run 1 AOD, the legacy format. Needed for any
  analysis of 2010 through 2012 data.
audience: [graduate, researcher]
languages: [en]
duration:
  min_minutes: 240
  notes: Plan on a full day for a working environment.
setup_burden: cmssw
data:
  formats: [aod]
  datasets: [aod-2011, aod-2010]
prerequisites:
  physics: [detectors, jets]
  computing: [containers, root]
learning_goals:
  - Set up the Run 1 CMSSW container
  - Understand the AOD content model
  - Write a first EDAnalyzer against Run 1 open data
physics_topics: [detectors, jets]
computing_topics: [containers, root]
tags: [research-pathway, reference]
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: CERN Open Data Portal
links:
  - {type: portal, url: "https://opendata.cern.ch/docs/cms-getting-started-aod", label: "Getting started with AOD"}
  - {type: reference, url: "https://cms-opendata-guide.web.cern.ch/", label: "CMS Open Data Guide"}
---

Maintained on the CERN Open Data Portal. Indexed here.

Choose this path only if you specifically need Run 1: a measurement at 7 or
8 TeV, a comparison across run periods, or a reproduction of a published Run 1
result. Run 1 has no NanoAOD equivalent, so there is no lighter option.

The container is older and the tooling around it is less exercised than Run 2.
Budget accordingly.
