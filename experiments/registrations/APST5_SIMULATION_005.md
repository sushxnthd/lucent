# APST5-SIM-005 Preregistration — Camera-Robust Equal-Exposure Probe Search

**Status: frozen before the held-out result is computed.**

## Question

Under a five-second matched-exposure pupil-response surrogate, which three-pulse timing pattern remains most distinguishable from the fixed contiguous control after realistic camera sampling, timestamp jitter, dropped frames, and measurement noise?

This is an engineering-model test of **observability**, not human validation.

## Fixed stimulus family

- total duration: 5.0 s;
- segment duration: 0.5 s;
- segment 0 is always low;
- exactly three of segments 1..9 are high;
- identical low/high levels for every candidate;
- therefore identical nominal high-display exposure.

There are 84 candidate timing patterns.

The fixed contiguous comparator is (4, 5, 6). The current E002 split sequence is (1, 2, 8).

## Pupil surrogate

Use the same delayed asymmetric pupil-response model and parameter bounds as APST5-SIM-001, but simulate internally at 100 Hz.

The simulator remains a literature-inspired design surrogate rather than a biological digital twin.

## Observation transformation

For each simulated person and condition:

1. convert pupil diameter to fractional change relative to the first 0.4 s median;
2. sample through a camera model;
3. linearly interpolate valid observations onto the same 20 Hz analysis grid used by E002;
4. subtract the first-0.4-second median again.

This removes absolute pupil scale and aligns the test with the planned pupil-to-iris / baseline-centered analysis.

## Frozen camera scenarios

| Scenario | FPS | timestamp jitter SD | frame-drop probability | observation-noise SD |
| --- | ---: | ---: | ---: | ---: |
| high quality | 60 | 1 ms | 0% | 0.005 |
| ordinary | 30 | 4 ms | 2% | 0.010 |
| stressed | 24 | 8 ms | 8% | 0.020 |

Noise values are dimensionless fractional-pupil surrogates and are not empirical estimates of a particular phone.

## Separation statistic

For a candidate probe u and the contiguous control c, define:

- B: RMSE between their noise-free baseline-centered camera-observed traces;
- W: median RMSE between two independent noisy camera observations of the same condition, pooled across candidate and comparator;
- separation ratio S = B/W.

This mirrors the E002 matched-exposure temporal-distinguishability concept.

## Design / test separation

### Design population

- 40 synthetic parameter draws;
- seed 20261001;
- parameter scale 0.60.

For every candidate, compute S across all design people and all three camera scenarios.

The design objective is the **10th percentile** separation ratio, not the mean.

Select the candidate with maximal design P10.

### Held-out population

After selection, evaluate on:

- 500 fresh synthetic parameter draws;
- seed 271828;
- parameter scale 0.80;
- the same three predeclared camera scenarios;
- new camera/noise random seeds.

No candidate selection uses the held-out population.

## Primary comparison

Compare on the held-out population:

1. newly selected robust probe;
2. current E002 split sequence (1,2,8);
3. evenly spaced sequence (2,5,8);

all against the fixed contiguous control (4,5,6).

Report mean S, P10 S, median S, P90 S, and the fraction of person × camera cells with S > 1.25.

## Robust-success criterion

A selected sequence is considered **model-robustly observable** only if on held-out data:

1. P10 separation ratio > 1.25; and
2. at least 90% of person × camera cells have S > 1.25.

This threshold is intentionally tied to E002's frozen engineering separation rule.

## Secondary analyses

After the primary result:

- report performance separately by camera scenario;
- compare the selected sequence with the current E002 sequence;
- report whether the current E002 sequence itself satisfies the robust-success criterion.

## Protocol rule

This experiment does **not** automatically alter E002.

If a different sequence outperforms the frozen E002 sequence, the existing nine-capture E002 protocol remains version 1. A future protocol version may test the newly selected sequence prospectively.

## Claim boundary

Even a strong result establishes only that the timing pattern is distinguishable under the committed surrogate and camera model.

It does not prove real pupils follow the surrogate, the phone pupil extractor achieves the assumed noise levels, active probing predicts vigilance/fatigue, or any selected sequence is safe or optimal in humans.
