# E002-517 | Exact eight-channel shutter-code collision: held-out synthetic falsification

Date: 2026-10-29. [Frozen protocol](E002_517_FROZEN.md) committed at `9ae46ed7` **before executing the five fresh seeds**. [Executable](e002_517_exact_collision.py), [seven controls](test_e002_517_exact_collision.py), [hosted CI](../../.github/workflows/e002_517_exact_collision.yml). Evidence tier: **exact synthetic instrument-identifiability falsification**, not a human or physical camera measurement.

## Scientific question

E002-514 reported unique timing for 199 of 200 selected held-out synthetic frames. Could eight independent binary LED channels *guarantee* unique local exposure timing across all possible starts and durations? The frozen E002-517 test exhaustively checks all 1-ms start positions and same-duration 8–12-ms exposure windows over 1600 ms, using exact rational eight-channel exposure means. No noise, optical mixing, unknown phase, camera blur, missingness or clock error is needed for the counterexample.

**Result: the global uniqueness claim is false under the original ideal model.** The five new, preregistered seeds produced **27 exact same-duration collision pairs** separated by at least 50 ms, versus the frozen prediction of at least one.

| Frozen seed | Exact distant collision pairs | 10-ms-only pairs |
|---|---:|---:|
| 211 | 5 | 2 |
| 223 | 3 | 0 |
| 227 | 6 | 0 |
| 229 | 9 | 2 |
| 233 | 4 | 0 |
| **Total** | **27** | **4** |

The longest same-duration collision separation was **1094 ms** (seed 233, 9-ms duration). Three seeds had no 10-ms collisions; these negative controls are retained rather than hidden.

## Exact two-world timing witness

The predeclared first eligible 10-ms collision occurs at seed 211. A single externally known eight-channel code and the *same* two camera observation vectors are consistent with both worlds:

| | World A | World B |
|---|---|---|
| Left exposure | [924,934] ms | [924,934] ms |
| Right exposure | [954,964] ms | [1233,1243] ms |
| Right optical vector | (7/10,1/2,2/5,2/5,3/5,3/5,2/5,3/5) | Identical, exactly |
| Actual blind gap | **20 ms** | **299 ms** |
| Hypothetical 50-ms timing budget | Within | Exceeds |

No radiometric noise, rolling shutter or unknown clock is required. Both worlds have identical measured optical input code and identical camera outputs. A point-timing estimator that selects the earlier right exposure would underestimate the blind gap by **279 ms** in world B.

Crucially, the existing E002-514 **set-valued inverse behaves correctly**: it retains both right intervals (two feasible right candidates) and returns a conservative 299-ms gap upper bound. This is not a falsification of that solver's conditional soundness; it is a falsification of any stronger *universal uniqueness* interpretation. The 50-ms timing budget is illustrative and is **not** a physiological blink threshold or a product certificate.

## Controls and reproducibility

- The code uses exact `Fraction` signatures. The two-world vector is independently reproduced by direct integer sums over the raw binary code, rather than relying only on the prefix-sum collision search.
- Same exposure duration, non-overlapping intervals and at least 50-ms separation are required. A 0.001 perturbation of one channel breaks the exact equality.
- All five seed outcomes, including absent 10-ms collisions, are reported. No threshold or seed tuning followed the freeze.
- The existing exhaustive inverse is tested at zero envelope; its conservative gap bound covers both truths.
- No nominal FPS, inferred camera metadata or human video enters the experiment. The result is deterministic **synthetic codebook analysis**.
- Seven adversarial software tests and a hosted workflow are committed. Hosted verification must be checked before claiming a CI pass.

## Sharp codebook-separation criterion (elementary, not a novelty claim)

For a finite set of candidate shutter intervals `I`, let `f(I)` be the exact eight-channel exposure-mean vector, and assume independently calibrated additive observation error bounded by `epsilon` in maximum norm. Define `delta = min_{I != J} ||f(I)-f(J)||_infinity`. **Every admissible observation has at most one feasible interval if and only if `delta > 2*epsilon`**. Sufficiency follows from the triangle inequality; necessity follows by choosing the midpoint of two vectors whose distance is at most `2*epsilon`. For positive error, the dimensionless separation ratio `delta/(2*epsilon)` must exceed one. This is the familiar disjoint-noise-ball condition from coding/identification theory, not a newly discovered theorem.

E002-517's exact same-duration collisions establish `delta = 0` for each of the five tested full-record codebooks, so **no nonnegative error tolerance can make these particular codebooks universally injective**. With unknown gains, crosstalk, blur, line delay or clock phase, replace the point vectors by the *sets of observations reachable under every allowed nuisance*. A unique certificate is permitted only when the relevant reachable sets are disjoint. A small fitted residual alone is not evidence of disjointness.

**Hosted verification:** [GitHub Actions run 40802272798](https://github.com/sushxnthd/lucent/actions/runs/40802272798) completed successfully on the executable/test commit, verifying all seven frozen software controls and the deterministic aggregate. This is independent hosted execution, not independent physical verification.

## Product and scientific consequence

A known eight-channel random LED pattern is **not automatically an injective timestamp code** over a long acquisition window. E002-514's 199/200 selected-frame uniqueness remains a valid synthetic observation but cannot justify a claim of unique per-frame timing for all exposures. For a future instrument, require either (a) a codebook with a **prevalidated minimum signature-separation margin** over every admissible start/duration under independently calibrated noise and radiometry, or (b) full set-valued timing with worst-case blind gaps and explicit abstention. A single plausible optical fit is not enough. Unknown gain, mixing, ambient light, line delay and clock error can only expand the set of possible worlds unless separately bounded.

The result does **not** establish that actual shutter timing is unidentifiable for a particular physical instrument, nor does it validate E002-371 in humans. It changes the **instrument design claim** and strengthens the physical calibration release gate. Stop further synthetic code-seed archaeology. Next decisive work: independent photodiode/exposure-sync measurements with E002-515, two real blinded S01 anatomical reviewers, and participant-disjoint held-out physical predictions.

**Human anatomical ratings: 0. Authenticated physical shutter measurements: 0. Certified continuous-time human eyelid-speed bounds: 0. Participant-disjoint physical predictions: 0.**

**Lucent product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. Hush PR #45 unchanged.
