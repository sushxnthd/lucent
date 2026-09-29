# MTS-TARGET-SMOOTHING-001: Direct Temporal-Alignment Test

**Status:** completed preregistered public-data experiment.

**Primary prediction:** **SUPPORTED**.

## Manipulation

The ocular data, participants, feature family, Ridge model, and LOSO protocol are held fixed. Only the behavioral target's future temporal support is broadened from the current PVT response to a 60-second mean response-speed target.

## Duration x target-horizon matrix

| Target support | 2 s sensor | 5 s | 15 s | 30 s | 60 s |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 s | 0.2700 | 0.1975 | 0.1199 | 0.0968 | 0.0744 |
| 15 s | 0.1868 | 0.1608 | 0.1339 | 0.1339 | 0.1209 |
| 30 s | 0.1678 | 0.1522 | 0.1547 | 0.1561 | 0.1592 |
| 60 s | 0.1559 | 0.1607 | 0.1712 | 0.1953 | 0.2042 |

## Preregistered interaction

Define D(H) = macro-r(60 s sensor, H) - macro-r(2 s sensor, H).

- D(0 s): **-0.1956**
- D(60 s): **+0.0483**
- Delta = D(60) - D(0): **+0.2439**
- paired subject-bootstrap 95% CI: **[+0.1647, +0.3191]**
- paired subjects: **28**

The preregistered criterion requires a positive interaction with the entire 95% interval above zero.

**Decision: supported.**

## Interpretation

Within the same human dataset, broadening the behavioral target from an immediate PVT response to a 60-second performance summary made the 60-second ocular history significantly more useful relative to the 2-second history. This directly supports a target-dependent sensing horizon under the frozen analysis.

## Claim boundary

This experiment tests temporal alignment in public eyelid/PVT data. It does not validate APST-5 active probing, smartphone pupillometry, or a clinical fatigue diagnostic.

## Reproduction

    pip install -e ".[dev]"
    python experiments/mts_target_smoothing.py
