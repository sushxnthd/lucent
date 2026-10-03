# RGBE-Gaze E002 dataset qualification audit — 2026-10-04

Status: PRE-OUTCOME DATASET QUALIFICATION
Class: CAPABILITY-BUILDING + DISCRIMINATION
Target: RGB-REFERENCE-OBSERVABILITY-002

## Question
Does the public RGBE-Gaze release retain an independently measured pupil time series with synchronization metadata suitable for a future frozen RGB waveform observability test?

## Source audit
Official upstream: GuangrongZhao/RGBE-Gaze.

The acquisition client explicitly requests Gazepoint streams:
- ENABLE_SEND_TIME and ENABLE_SEND_TIME_TICK;
- ENABLE_SEND_PUPIL_LEFT / ENABLE_SEND_PUPIL_RIGHT;
- ENABLE_SEND_EYE_LEFT / ENABLE_SEND_EYE_RIGHT;
- ENABLE_SEND_PUPILMM;
- ENABLE_SEND_PIX.

The source comments define LPD/RPD as pupil diameter in camera pixels, LPUPILD/RPUPILD as physical pupil diameter in metres, and LPMM/RPMM as pupil diameter in millimetres, with validity flags. The client stores the received Gazepoint records and Windows/CPU timing sidecars.

The upstream README states each released participant/session contains a gazepoint/gazepoint.csv plus time_win.txt and time_cpu.txt, while RGB frames have timestamp_win.txt; Windows timestamps are explicitly intended for synchronization with Gazepoint.

The conversion script extracker-txt2.py converts complete quoted Gazepoint records to CSV rows rather than selecting gaze-only columns. This is positive evidence that requested pupil fields should survive into the release, but it is not proof of the exact columns present in every downloaded session.

## Discovery Protocol V2 state
KNOWN
- Acquisition requested pupil-pixel, physical-pupil, eye-position, validity, high-precision time and pixel/mm scale channels.
- RGB and Gazepoint streams have explicit synchronization sidecars.
- Official dataset organization exposes gazepoint.csv per session.
- Dataset contains 66 participants and six sessions per participant according to the official README.

BELIEVED
- Released gazepoint.csv retains the requested pupil channels because conversion writes all quoted values from qualifying REC records.

CONFLICTING
- RGB is from a FLIR BFS-U3-16S2C research camera, not a commodity phone/webcam. A positive result would establish ordinary visible-RGB observability under this acquisition domain, not smartphone validity.
- The dataset was designed for gaze, not an active pupillary light-response protocol; it qualifies measurement transfer and natural temporal observability, not APST-5 state validity.

FALSIFIED
- None from this qualification audit. RGB-SCALE-OBSERVABILITY-001 remains independently negative for raw PupilSense absolute-mm geometry invariance.

ANOMALOUS
- The conversion script is positional/headerless. Exact schema must be reconstructed from the acquisition field order and validated against values/validity flags before any outcome analysis.

UNTESTED
- Actual downloadable session schema and missingness.
- Timestamp residual after RGB↔Gazepoint alignment.
- Whether natural pupil variation has enough within-window dynamic range for E002 gates.
- Direct pupil/reference RGB segmentation fidelity.
- Scale, lighting, frame-rate and participant-held-out robustness.

## Frozen qualification gates before outcome inspection
A session may enter waveform analysis only if:
1. pupil channel identity is unambiguous from acquisition order/schema;
2. tracker validity flags are present and interpretable;
3. RGB and tracker timestamps admit a documented monotone alignment;
4. no test-participant information is used for calibration or preprocessing selection;
5. raw absolute-mm PupilSense remains comparator-only and cannot rescue the primary method.

## Cheapest next discriminating experiment
Cloud-download one released RGBE-Gaze session only. Inspect filenames, CSV width, candidate pupil columns, validity rates, timestamp monotonicity, RGB frame count and synchronization residual. Do not compute RGB↔pupil performance during this qualification step.

If qualification passes, freeze a dataset-specific E002 addendum before computing waveform outcomes. Primary candidate remains an explicit dimensionless pupil/stable-eye-reference observable; strongest controls include raw pupil pixels, direct uncalibrated ratio, tracker-only quality ceiling, temporal circular shift, cross-eye mismatch and photometric/nuisance predictors.

## Claim boundary
This audit establishes dataset suitability evidence only. It is not an RGB observability PASS, does not validate APST-5, and does not establish fatigue/sleepiness/alertness inference.
