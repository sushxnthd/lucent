# E002-095 — Frozen P_54 cross-participant transfer of E002-094 RGB dark-core proxy

Frozen before inspecting **P_54 paired RGB dark-core/Tobii outcomes**. P_54 was previously examined in reference-only and photometric analyses; this is a *method transfer* experiment, **not** a pristine participant-level holdout. P_33 results are known and are not used to tune the method.

## Data and sample lock
Source: Brown Eye of the Typer ETRA2018 public archive, original `P_54/1493129853898_3_-study-dot_test.webm`, `P_54/1493129853898.json`, `P_54/P_54.txt`.
- Exactly 30 target presentation times: 5.25, 5.75, ..., 19.75 s.
- Event-derived video start time; reference uses the original Tobii timestamp field. Nearest valid Tobii reference within **40 ms**, else missing; no lag optimization.
- Use original WebM frame nearest requested presentation time, without exposure-time calibration; document this limitation.
- Use same `FacialFeatures` landmarks and three-row grayscale profile, three-pixel moving average, q15+0.5(q85-q15) threshold, longest central non-boundary-touching dark run, divided by eye-corner width as E002-094. No reference-label-based parameter selection.
- Log all missingness; do not impute missing candidate measurements.

## Frozen hypotheses and gates
H1 (primary): this *non-anatomical* dimensionless dark-core proxy has sufficient bilateral waveform fidelity in P_54. PASS only if **each eye** has >=20/30 valid samples, each eye's Pearson level correlation with matched Tobii mean pupil diameter is >=+0.50, and each eye exceeds whole-frame brightness correlation by >=0.15 in absolute magnitude, with zero-lag correlation greater in absolute value than correlations after +/-1.0-second reference offsets. All conditions conjunctive.

H2 (secondary replication): P_33's exploratory left-eye first-difference association transfers to P_54. PASS only if >=12 consecutive valid transitions, Pearson first-difference r >=+0.50, Spearman >=+0.40, and leave-one-transition-out minimum Pearson r >=+0.35. Treat all as conjunctive. Report circular-shift exceedance score over 29 nonzero shifts descriptively, with no inferential p-value claim. H2 cannot rescue H1.

H3 (negative controls): report on same valid transition mask first-difference correlations for whole-frame brightness, local eye brightness, and eyelid aperture; for H2 to qualify as a *candidate* signal its Pearson r must exceed the maximum absolute negative-control r by >=0.20.

## Mandatory anomaly mining
If any gate fails, inspect missingness runs, eye-specific reversal, time-block sign changes, candidate quantization, per-eye aperture/contrast, apparent eye width, camera brightness, lag sensitivity, and leave-one-out influence. Do not retune the frozen primary.

## Claim boundaries
A dark-core width is not anatomically verified pupil or iris diameter. This passive desktop dot-test does not test active light-response inference, phone geometry, behavioral fatigue, sleepiness, or alertness. Raw PupilSense millimetres remain excluded. P_01, P_02 and P_07 remain untouched RGB/reference holdouts.

## Research roles
Experimentalist: locked implementation. Skeptic: controls and leakage audit. Blinded Analyst: score only after RGB rows extracted. Anomaly Hunter: post-failure probes separately labeled. Prior-Art Auditor: no novelty claim for normalization or visible-light pupillometry. Replicator: independent Python original-data decoding still required. Theorist: update observability model, not state validity.
