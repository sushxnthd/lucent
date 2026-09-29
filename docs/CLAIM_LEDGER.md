# Lucent Claim Ledger

This file separates what the repository has actually shown from what remains a hypothesis.

A result should move upward only when the evidence layer changes, not because the wording becomes more confident.

| Claim | Evidence | Current status | What would falsify / strengthen it |
| --- | --- | --- | --- |
| Stimulus timing changes parameter identifiability under fixed duration/exposure in the Lucent pupil surrogate. | APST5-SIM-001 | **supported computationally** | alternative physiological models; real pupil measurements |
| A tighter prior over stable nuisance cannot reduce local state Fisher information in the stated model. | Baseline Compression Principle | **mathematical under assumptions** | violation of model assumptions does not falsify the algebra; it limits applicability |
| A 2 s personalized surrogate can exceed a 5 s population surrogate. | APST5-SIM-002 | **supported computationally** | real longitudinal data with measured baseline precision |
| The chosen simple PVT1 personalization transform improves 5 s human-data prediction. | MTS-REALDATA-001 primary test | **not supported** | independent human data with a better-defined nuisance model |
| Very recent passive ocular behavior can be more informative about the immediate next PVT response than longer passive history. | MTS-REALDATA-001 exploratory duration analysis | **supported in one public dataset; replication required** | independent cohort with fixed immediate target |
| Concurrent pupil + pursuit sensing can increase state information density enough to compress 5 s pupil-only sensing to ~3 s in the surrogate. | APST5-SIM-003 | **supported computationally** | joint human measurements |
| The 3 s multimodal result survives substantial channel redundancy. | APST5-SIM-004 | **supported computationally** | explicit joint-covariance modeling and human data |
| Ordinary phone hardware can recover the APST-5 pupil/gaze dynamics with sufficient repeatability. | not yet measured | **open** | E002 phone observability pilot |
| Optimized active 2–5 s probing beats passive sensing in humans. | not yet measured | **open** | preregistered paired active/passive study |
| Lucent can estimate fatigue/cognitive performance robustly on unseen people and devices. | not yet measured | **open** | subject-held-out + device-held-out prospective validation |
| Lucent is a medical diagnostic system. | none | **not claimed** | would require an entirely different clinical validation program |

## Claim discipline

The repository uses four evidence labels:

- **mathematical under assumptions**: follows from a stated model or theorem;
- **supported computationally**: reproduced in simulation / numerical experiments;
- **supported in public human data**: observed in existing participant data under a documented analysis;
- **prospectively validated**: requires a frozen protocol and new human data.

Only the last category can support the strongest real-world performance claims.

## Current center of gravity

Lucent now has three converging clues:

1. **active design:** stimulus timing changes information yield in the surrogate;
2. **temporal locality:** a public human dataset shows the immediate target is better tracked by the most recent tested ocular window than by longer history;
3. **multimodal compression:** concurrent pupil + pursuit sensing remains advantageous across a broad uncertainty envelope in simulation.

The missing bridge is direct smartphone measurement on humans.

That gap is explicit rather than hidden.
