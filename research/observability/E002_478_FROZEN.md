# E002-478 FROZEN — two-period optical response repeatability falsification

Date: 2026-10-27. Kernel E002-371. **Post-hoc hypothesis after inspecting E002-477 source and synthetic fixture; frozen before implementing the new periodicity test. This is not a blinded preregistration.**

## Question and predicted result
E002-477's intake validates file completeness, timing fields and checksums but does not test whether a stationary camera's optical pulse response repeats after one authenticated frame period. For a time-invariant shutter response under fixed illumination, gain and row, phase-folded pulse response should recur. A synthetic one-shot shutter that responds in the first period but not the second can therefore pass intake while violating the physical repeating-shutter model.

**Prediction A:** The existing E002-477 synthetic fixture passes `PASS_INTAKE_ONLY` but fails a separately frozen periodic-response necessary condition for at least one sensor row. This is a model falsification, not a real camera failure.

**Prediction B:** An independently constructed two-period periodic rectangular-shutter fixture passes the condition. **Prediction C:** Injecting an above-budget second-period brightness/response change fails or abstains. **Prediction D:** An all-dark/no-response trace is indeterminate rather than evidence of a closed shutter. **Prediction E:** Missing externally justified slope/noise/drift/timing budgets must abstain.

## Frozen necessary inequality
Let C_r(t) be dark-subtracted response in row r to the same independently timed pulse, with fixed pulse energy and sensor gain. If stationary periodic shutter response is L-Lipschitz in pulse phase, each measured contrast error is bounded by b, period-to-period drift by d, and independently measured pulse-phase errors by u on each pulse, then for two observations at phases t_i and t_j approximately one frame period T apart:

`|C_r(t_i)-C_r(t_j)| <= L*(abs((t_j-t_i)-T)+2*u)+2*b+d`.

Use medians across the 20 repeats for each row/phase; under a deterministic per-record error bound b, their medians obey the same bound. Pair each first-period phase with the nearest sampled second-period phase, allowing noninteger T/phase-step. Reject on any strict inequality violation. If fewer than two periods, no matched phases, missing independent budgets, no authenticated T, or no measurable response above a prespecified minimum, return `INDETERMINATE`. A pass means **only** this necessary condition survived the supplied budgets. It never certifies shutter support, clock independence, physiological velocity or product release.

Synthetic test budgets (explicit simulator truths, not hardware specifications): L=1 response unit/ms, b=0.0005 response units, d=0.001 response units, u=0.001 ms, minimum peak contrast=0.02 response units. Independently authenticated T is supplied as 1000/240 ms only for synthetic tests. A periodic positive control uses the same 1-ms rectangular support in every frame period; a one-shot negative uses the E002-477 fixture unchanged.

## Reproduction and evidence
Implement standard-library executable and adversarial tests, preserve E002-477 original fixture and result unmodified, run independent arithmetic and local tests, commit code, aggregate and a report to the same branch and draft PR. Do not claim physical calibration, human validation, a new theorem, or production release. Do not replace physical acquisition with repeated synthetic work after this falsification.
