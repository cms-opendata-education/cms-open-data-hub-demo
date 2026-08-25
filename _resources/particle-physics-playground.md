---
title: Particle Physics Playground
status: active
last_verified: 2026-08-20
summary: >-
  Students compute the mass of dimuon events from real CMS data, first with
  classical kinematics and then relativistically, and see why only one works.
audience: [high-school, undergrad-intro, undergrad-advanced]
languages: [en]
duration:
  min_minutes: 45
  max_minutes: 120
  notes: Frequently assigned as homework rather than class time.
setup_burden: cloud-notebook
data:
  formats: [csv]
  datasets: [dimuon-csv-2011]
prerequisites:
  physics: [special-relativity, invariant-mass]
  computing: [python-basics, pandas]
learning_goals:
  - Reinforce introductory Python and pandas on data students care about
  - Apply relativistic energy and momentum to a real measurement
  - See a resonance peak emerge from a histogram
physics_topics: [special-relativity, invariant-mass, standard-model]
computing_topics: [python-basics, pandas, matplotlib]
tags: [instructor-guide]
instructor_materials: true
license: CC-BY-4.0
authors:
  - name: Matt Bellis
    affiliation: Siena College
links:
  - {type: homepage, url: "https://sites.google.com/siena.edu/particle-physics-playground/home", label: "Particle Physics Playground"}
  - {type: colab, url: "https://colab.research.google.com/drive/1rzqu-NmFA-Pwc93fnLy5u4sNnvxzKyBS", label: "Student notebook"}
  - {type: instructor, url: "https://colab.research.google.com/drive/1izsL2Ep-BD9PlTrJdWhtuwwMKkw-bVa6", label: "Instructor notebook"}
  - {type: slides, url: "https://docs.google.com/presentation/d/1JKwlRqiKnupkw9iir4d1YCL87ligSZz6STW_GQl73UI", label: "Introduction slides"}
---

Students read in the energy and momentum of muon pairs recorded by CMS and
calculate the mass of the parent particle two ways: once using classical
physics, once using special relativity. The classical calculation produces
noise. The relativistic one produces peaks.

This has been used both with first-year students in an introductory
programming course and with an upper-level particle physics course; the
difference is how much scaffolding you leave in place.

Supplemental material is available for instructors who want to go further,
including a four-vector matching exercise that can be printed and cut into
strips for a no-computer warm-up, and a particle lifetime assignment.
