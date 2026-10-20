# Lucent E002-328 — projected EAR observability and frozen human gate

Status: exact feature-level geometric interval; independent checker PASS; no human recordings evaluated, no novelty claim.

The active question is whether ordinary-RGB eye-aspect ratio, normalized by a participant's open-eye baseline, can predict independently adjudicated NIR/EEG-assisted blink events under participant, lighting, gaze and glasses holdout.

This branch is research-only, not a fatigue app. Read THEOREM.md, PROTOCOL.md, PRIOR_ART.md, FAILED_GATES.md, checker_results.json. Reproduce with Python 3 standard library: python independent_checker.py.

Product: allow only conditional projected-2D EAR interval and abstention. Reject uncalibrated anatomical closure, millisecond blink timing, pupil waveform, and five-second fatigue certification.

Next: obtain lawful synchronized human RGB/reference data and an independently measured landmark error bound, then test a frozen unseen participant/device regime. mEBAL2 alone cannot provide independent device holdout or subframe reference truth.
