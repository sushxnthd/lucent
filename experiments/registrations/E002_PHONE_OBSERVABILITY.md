# E002: APST-5 Phone Observability Pilot — Frozen Protocol

**Purpose:** determine whether ordinary phone hardware can execute the fixed APST-5 luminance sequence and recover repeatable ocular dynamics with sufficient timing fidelity to justify a state-validation study.

This is an instrumentation study. It is not a fatigue experiment.

**Pre-data amendment:** capture order is frozen in [E002_PROTOCOL_AMENDMENT_001.md](E002_PROTOCOL_AMENDMENT_001.md). No stimulus, quality gate, endpoint, or exit criterion is changed.

## Safety boundary

- use ordinary rested / naturalistic states only;
- do not intentionally restrict sleep;
- use a comfortable fixed screen brightness;
- no rapid flashing; stimulus blocks are 0.5 s;
- stop for discomfort, headache, dizziness, visual symptoms, or eye strain;
- never run while driving or performing a safety-critical activity.

## Conditions

Exactly three five-second conditions:

1. passive: constant low display;
2. contiguous: high segments [4,5,6];
3. split: high segments [1,2,8].

Segment duration is 0.5 s. Contiguous and split conditions each contain exactly three high segments and therefore have matched nominal display-content exposure.

RGB content levels are fixed by instrument/protocol.json. They are not treated as calibrated retinal illuminance.

## Repeats

For the first engineering pilot, the nine planned captures follow this exact predeclared order:

1. passive
2. contiguous
3. split
4. passive
5. split
6. contiguous
7. split
8. contiguous
9. passive

This gives three planned captures per condition and includes every directed condition-to-condition transition at least once.

Do not reorder captures or tune thresholds/probe timing after seeing the first condition difference. Technical retries follow the rules in E002_PROTOCOL_AMENDMENT_001.md. Any redesign creates a new protocol version.

## Required capture outputs

Every trial must include:

- raw front-camera video;
- JSON stimulus/camera sidecar from instrument/app.js;
- offline capture-quality JSON;
- offline pupil-dynamics JSON and trace CSV where extraction succeeds.

Raw participant video must never be committed to Git.

## Technical quality gates

A capture is technically usable only if all available checks satisfy:

- actual capture duration in [4.8, 5.3] s;
- maximum stimulus scheduling error <= 35 ms;
- browser frame-cadence median interval <= 45 ms when requestVideoFrameCallback is available;
- browser frame-cadence p95 interval <= 75 ms when available;
- offline face detection rate >= 0.90;
- offline two-eye detection rate >= 0.70;
- pupil extractor valid-frame rate >= 0.60 for analyses that use pupil dynamics.

If a browser does not expose a timing or face API, that missing live check is not automatically an exclusion; the offline video checks become mandatory.

## Primary observability endpoints

### O1 — timing fidelity

At least 8 of 9 planned captures must pass the stimulus-timing gate.

### O2 — ocular observability

At least 8 of 9 planned captures must pass the offline face/eye visibility gate, and at least 6 of 9 must produce a pupil trace with >=60% valid frames.

### O3 — within-condition repeatability

For each active condition, derive:

- baseline-normalized constriction amplitude;
- time to minimum pupil ratio;
- valid pupil-frame rate.

Across repeated technically usable captures, constriction-amplitude coefficient of variation should be <=25% for at least one active condition before progressing to a state study.

### O4 — matched-exposure temporal distinguishability

Interpolate each valid pupil-to-iris trace onto a common 20 Hz grid over 0–5 s and baseline-center it using the pre-first-high interval.

Compute:

- median pairwise RMSE among repeats of the same active condition;
- median pairwise RMSE between contiguous and split active conditions.

Define separation ratio:

    S = median between-condition RMSE / median within-condition RMSE

The timing architecture is considered observably distinct if S > 1.25 and the result is not driven by one failed capture.

## Exit criterion

E002 clears only if O1 and O2 pass and at least one of O3 or O4 passes.

Failure is informative. If timing fails, redesign instrumentation. If eye/pupil observability fails, improve capture hardware/algorithm. If timing and observability pass but O3/O4 fail, the active probe may not create sufficiently stable measurable dynamics on commodity RGB cameras.

## Claim boundary

Clearing E002 would establish only that the phone can execute and observe the experiment. It would not show that the response predicts fatigue, vigilance, or cognitive performance.