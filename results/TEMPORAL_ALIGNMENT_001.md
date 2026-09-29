# TEMPORAL-ALIGNMENT-001: Target Timescale Determines Useful Ocular History

**Status:** preregistered public-human-data result with two independent boundary datasets.

## Result in one sentence

Within the same 28-subject eyelid/PVT dataset, experimentally broadening the behavioral target from one immediate reaction to a 60-second performance summary reversed the relative value of short versus long ocular history: the 2-second window was strongest for the immediate target, while the 60-second window was strongest for the 60-second target.

## Preregistered direct test

MTS-TARGET-SMOOTHING-001 held the participants, raw ocular signal, feature map, Ridge model, LOSO protocol, and event intersection fixed. Only the temporal support of the target was changed.

| Target support | 2 s sensor | 5 s | 15 s | 30 s | 60 s |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 s | **0.2700** | 0.1975 | 0.1199 | 0.0968 | 0.0744 |
| 15 s | **0.1868** | 0.1608 | 0.1339 | 0.1339 | 0.1209 |
| 30 s | **0.1678** | 0.1522 | 0.1547 | 0.1561 | 0.1592 |
| 60 s | 0.1559 | 0.1607 | 0.1712 | 0.1953 | **0.2042** |

Define the long-versus-short sensing advantage at target horizon H as:

    D(H) = r(60 s sensor, H) - r(2 s sensor, H)

The preregistered interaction was:

    Delta = D(60 s) - D(0 s)

Observed:

- D(0 s) = **-0.1956**
- D(60 s) = **+0.0483**
- Delta = **+0.2439**
- paired subject-bootstrap 95% CI = **[+0.1647, +0.3191]**
- paired subjects = **28**

The entire interval is positive, satisfying the preregistered criterion.

## Why this matters

This result rejects a simplistic rule such as 'shorter ocular windows are always better.' Instead, the useful sensing horizon depends on the timescale of the functional target.

For an imminent PVT response, old ocular history behaves like stale state and dilutes predictive information. When the target itself is broadened to summarize performance over the next minute, longer ocular history becomes relatively more informative and ultimately overtakes the shortest window.

That converts Temporal Alignment from a post-hoc interpretation of different datasets into a directly manipulated, preregistered within-dataset result.

## Independent boundary evidence

### ADHD-REALDATA-001

On an independent EyeLink working-memory dataset with 50 participants and 5,973 common trials, the preregistered 2-second versus 5-second hypothesis reversed:

- 2 s macro-r = 0.0350
- 5 s macro-r = **0.0749**
- difference = **-0.0400**
- 95% CI = **[-0.0717, -0.0061]**

This falsified the idea that 2 seconds is a universal optimum.

### COGBEACON-REALDATA-001

On an independent WCST-like cognitive-fatigue dataset with 20 people, 77 sessions, and 1,892 eligible rounds:

- 2 s macro-r = 0.1197
- 5 s macro-r = **0.1665**
- 2 s - 5 s = -0.0468, 95% CI [-0.1046, +0.0101]
- 3 s - 5 s = **-0.0796**, 95% CI **[-0.1375, -0.0210]**

Again, a universal ultra-short optimum was not supported.

## Temporal Alignment Principle

Lucent should not optimize scan duration independently of the target.

A more precise design objective is:

    choose sensing duration and active probe jointly to maximize
    target-specific information density minus time/comfort cost.

In practical terms:

1. define the functional target first;
2. estimate the target's temporal support;
3. condition on personal history to remove stable nuisance;
4. concentrate active sensing inside the target-relevant horizon;
5. stop when additional history contributes less target information than its interaction cost.

## What is actually established

The strongest defensible claim is:

> In a preregistered public-human-data experiment, changing only the temporal support of the behavioral target significantly changed the relative value of short versus long ocular sensing history.

This is an empirical measurement-design result.

## What is not established

This does not yet show that:

- APST-5 active probing works in humans;
- a smartphone can recover the needed pupil/gaze dynamics;
- any fixed 2-, 3-, or 5-second window is universally optimal;
- Lucent diagnoses fatigue or any medical condition;
- the mechanism is specifically neural state dilution rather than another temporal statistical effect.

Those remain separate falsification targets.

## Reproduction

    python experiments/mts_target_smoothing.py

See also:

- results/MTS_TARGET_SMOOTHING_001.md
- results/MTS_REALDATA_001.md
- results/ADHD_REALDATA_001.md
- results/COGBEACON_REALDATA_001.md
- docs/TEMPORAL_ALIGNMENT.md