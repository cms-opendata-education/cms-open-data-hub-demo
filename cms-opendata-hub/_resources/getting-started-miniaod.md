---
title: Getting started with CMS MiniAOD
status: active
last_verified: 2026-08-20
summary: >-
  The Portal's walkthrough for Run 2 MiniAOD, including the CMSSW container.
  Use when NanoAOD does not carry the variable you need.
audience: [graduate, researcher]
languages: [en]
duration:
  min_minutes: 240
  notes: Plan on a full day to get a working environment and a first plot.
setup_burden: cmssw
data:
  formats: [miniaod]
  datasets: [miniaod-2015]
prerequisites:
  physics: [detectors, jets]
  computing: [containers, root, python-basics]
learning_goals:
  - Set up the CMSSW container for Run 2 open data
  - Understand the MiniAOD content model
  - Write and run a first EDAnalyzer against open data
physics_topics: [detectors, jets]
computing_topics: [containers, root]
tags: [research-pathway, reference]
instructor_materials: false
license: CC-BY-4.0
authors:
  - name: CERN Open Data Portal
links:
  - {type: portal, url: "https://opendata.cern.ch/docs/cms-getting-started-miniaod", label: "Getting started with MiniAOD"}
  - {type: reference, url: "https://cms-opendata-guide.web.cern.ch/", label: "CMS Open Data Guide"}
---

Maintained on the CERN Open Data Portal, indexed here.

This is a real step up in effort. You need Docker or a virtual machine, you
need to understand validated-run lists and luminosity, and the first plot will
take considerably longer to produce than it would from NanoAOD.

Take this path when you have a concrete reason: a physics object or variable
that NanoAOD does not store. If you are not sure whether you have such a
reason, you probably do not, and NanoAOD is the better use of your time.

For Run 1 data the equivalent format is AOD, with its own container and its
own getting-started page.
