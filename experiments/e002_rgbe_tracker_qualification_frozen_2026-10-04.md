# RGBE-Gaze tracker qualification preregistration — E002

Status: FROZEN BEFORE RGB↔PUPIL OUTCOME INSPECTION
Experiment: RGB-REFERENCE-OBSERVABILITY-002
Class: CAPABILITY-BUILDING / DISCRIMINATION
Date: 2026-10-04

## Purpose
Qualify RGBE-Gaze's released Gazepoint stream as a temporal pupil reference before any RGB pupil waveform score is computed. This document does not authorize an observability claim.

## Prior evidence
The official RGBE-Gaze release documents 66 participants, six sessions per participant, RGB frames, Gazepoint references, and CPU/system synchronization sidecars. Acquisition code requests pupil-related Gazepoint channels. Source audit also identified a risk: raw TCP recv() chunks were persisted and a later positional/headerless conversion was used. Therefore released row integrity is an empirical prerequisite.

## Frozen qualification sequence
For exactly one released session selected without inspecting pupil/RGB agreement:
1. Parse gazepoint.csv without repairing rows.
2. Record row-width histogram. Primary-valid rows must match the intact 48-field schema reconstructed from the upstream converter example.
3. Report fractions width<48, width=48, width>48 and widths near multiples of 48.
4. On exactly-48 rows only, verify TIME/TIME_TICK numeric validity, monotonicity, duplicate rate, cadence distribution, and discontinuities.
5. Verify the preidentified pupil fields (LPD/RPD, LPUPILD/RPUPILD, LPMM/RPMM and validity fields) for finite rate, validity rate, physical range, clipping/constant runs, and left-right consistency. Do not choose among pupil channels based on later RGB agreement.
6. Audit time_win.txt/time_cpu.txt and RGB timestamp/event_cpu sidecars. Quantify whether a deterministic cross-clock mapping can be constructed and report residuals without inspecting RGB pupil estimates.
7. Preserve malformed rows as a negative integrity result. No primary-analysis repair or post-hoc schema shifting.

## Qualification outcomes
PASS-TO-E002: stable 48-field records dominate, a monotonic tracker timebase exists, at least one preidentified pupil channel has nondegenerate valid variation, and RGB/tracker synchronization can be specified without outcome-driven alignment.
FAIL-REFERENCE: released stream cannot support a defensible short-waveform reference.
CONDITIONAL: usable only in explicitly bounded sessions/segments; boundary must be defined from integrity variables, never RGB↔pupil agreement.

No numeric threshold will be invented after observing RGB↔pupil outcomes. Descriptive integrity statistics may define a later amendment only before outcome scoring and must be labeled exploratory.

## Frozen E002 mechanistic prediction
If apparent scale is a principal failure mode behind RGB-SCALE-OBSERVABILITY-001, a dimensionless pupil/reference geometry observable should suppress apparent-scale variation more strongly than raw pupil pixels or raw PupilSense millimetres while preserving tracker-correlated temporal variation. A positive result must survive participant/session held-out evaluation, temporal-shift controls, photometric nuisance controls, and uncertainty stratification.

## Claim boundaries
A PASS qualifies RGBE-Gaze only as a visible-RGB + tracker measurement testbed. Its FLIR camera does not establish phone/webcam validity. No fatigue, sleepiness, alertness, APST-5, or five-second state-validity claim follows from this qualification.

## Discovery Protocol V2 state
KNOWN: RGBE-Gaze documents synchronized RGB and Gazepoint references and its acquisition requests pupil channels.
BELIEVED: released gazepoint.csv retains usable pupil samples.
CONFLICTING: published gaze use suggests substantial usable tracker data; acquisition/conversion source creates record-framing risk.
FALSIFIED: raw PupilSense absolute millimetres are an acceptable geometry-invariant Lucent measurement path.
ANOMALOUS: positional/headerless conversion plus TCP chunk persistence can create malformed or silently selected records.
UNTESTED: released row integrity, pupil-channel validity, cadence, and RGB↔tracker synchronization residual.

Cheapest next discriminating experiment: metadata-only qualification of one released RGBE-Gaze session under the sequence above.
