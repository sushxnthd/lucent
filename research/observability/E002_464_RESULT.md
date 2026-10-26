# E002-464 — dynamic encoder transfer can fabricate an apparent dark-gap crossing

**Date:** 2026-10-26. **Evidence tier:** constructed delayed/signed sensor counterexamples plus executable fail-closed repair; no physical encoder measurements or new human labels. [Frozen before implementation](E002_464_FROZEN.md), commit `48c05af8d3ff8b006897fe3d722a2c4cc5f4070a`. This is a measurement-model falsification and product/reference-label consequence, **not** a new theorem.

## Falsification: the reference is not automatically instantaneous

E002-463 requires a string `bandwidth_calibration_id` but does not require a numerical bound on temporal memory or a nonnegative normalized impulse response. A valid-looking record with nominal timestamp t=1.00 ms and reported aperture 1.95±0.01 mm therefore produces `WITNESSED_CROSSING` in its ordinary-camera dark gap (0.15,2.35) ms.

**Counterexample 1 (delay):** Let the true aperture dip below the 2.00-mm threshold at t=-0.40 ms, then return to 2.30 mm before the first shutter exposure. The physical aperture remains above threshold throughout the entire dark gap. A causal reference sensor with pure 1.40-ms delay reports the earlier 1.95-mm crossing at t=1.00 ms. E002-463's timestamp-only logic falsely locates the crossing in the gap, creating an apparent falsification of the ordinary-camera exclusion despite no actual dark-gap crossing. The constructed trajectory is deliberately not physiologically constrained.

**Counterexample 2 (signed temporal response):** A linear filter with coefficients (2,-1) reports 2×2.20−2.45 = **1.95 mm**, even though both input apertures are above 2.00 mm. A negative-valued kernel destroys the implication that a below-threshold filtered output proves any below-threshold physical aperture.

These counterexamples attack **reference-witness validity**, not E002-371's conditional mathematical bound. They show why even a nominally independent encoder can corrupt the reference label when its dynamic transfer is unspecified.

## Repaired research-only instrument gate

The new [E002-464 adapter](e002_464_dynamic_reference.py) refuses positive dark-gap reference witnesses unless the input declares numerical maximum past memory L, future lead F, centered acquisition support E, bounded clock error delta, position error, and a **nonnegative unit-mass temporal response**. It requires calibration identifiers but **does not independently authenticate them**.

For reported time t, the true physical influence support is conservatively contained in

`[t − delta − E/2 − L, t + delta + E/2 + F]`.

Both edges must lie **strictly** inside the ordinary-camera dark gap. For a nonnegative unit-mass kernel and bounded additive position error epsilon, a reported mean y satisfying `y+epsilon<=c` implies **existence** of a true threshold crossing somewhere within this support, not at the nominal timestamp. The gate forwards that expanded support to E002-463/E002-456 and never promotes noncrossing samples into negative OPEN truth.

The frozen delay example (L=1.40 ms) is refused because the effective support begins at -0.42 ms, before the 0.15-ms dark-gap boundary. The synthetic positive control (L=0.10 ms) retains support [0.88,1.02] ms and is admitted. An undeclared or signed kernel abstains. The independent arithmetic checker enumerates the preregistered 201×201 past-memory/future-lead grid, with predicted **11,039/40,401** strictly interior cases. These are **frozen predictions** until hosted execution is verified, not physical rates.

## Verification and implementation

- [18 adversarial Python tests](test_e002_464_dynamic_reference.py) exercise the delayed/signed counterexamples, strict boundary equality, missing calibrations, nonfinite values, acquisition support, clock error, open-world nonlabels, nuisance abstention, and the 40,401-case sweep.
- [Independent Node.js arithmetic reproduction](e002_464_independent_replay.cjs) does not import the Python evaluator.
- [Dedicated GitHub Actions workflow](../../.github/workflows/e002_464_dynamic_reference.yml) runs both implementations and asserts that no physical release is authorized.
- **At report creation the E002-464 hosted workflow result has not been verified. Do not claim its tests or sweep passed until GitHub Actions completion is inspected.** The predecessor [E002-463 run 40322384434](https://github.com/sushxnthd/lucent/actions/runs/40322384434) **did pass**, including its 18 earlier tests; that earlier success does not resolve this newly found transfer gap.

## Physical acquisition handoff: what would actually validate the reference

1. Measure encoder *input-to-output* dynamic response using an independently timestamped position standard (optical interferometer, traceable displacement sensor, or independently calibrated fast motion stage). Step and bidirectional swept-frequency/chirp inputs must include near-threshold, unseen high-speed motions. An instrument's declared bandwidth alone does **not** bound delay, phase, ringing, or tail.
2. Bound actual input influence support and sign/normalization of the effective impulse response **with uncertainty**. An analog/IIR response with unbounded tails cannot claim finite exact support merely from a measured -3 dB bandwidth. Unless a rigorous tail-mass/amplitude argument is separately proved and independently reviewed, the deterministic dark-gap witness must **abstain**.
3. Independently capture shutter optical exposure support (photodiode + timing trace), rolling-row timing, reference and ordinary-camera clocks, aperture geometry/scale, missing samples, gain, blur and saturation. Independently escrow frozen predictions before revealing the position trace.
4. Blind the test to unseen waveforms and exposure phases. Include true inside-gap crossings, before-gap delayed crossings, outside-gap filtered ringing, always-open controls, and uncertainty-straddling boundaries. Report coverage and false witness count **per nuisance stratum**, not only pooled.
5. Only after physical bench transfer passes should the [E002-456 participant-disjoint anatomical protocol](E002_456_RESULT.md) be attempted. High-speed video positives are not automatically complete negatives. No deterministic human speed limit follows from a sample maximum.

## Product and release consequence

**E002-463's timestamp-only encoder adapter is historical synthetic evidence, not a physically admissible anatomical reference-label pipeline.** Any prospective validation or physical product using a filtered encoder must use a transfer-aware, independently calibrated reference model. Unknown response support, signed/ringing kernels, or unauthenticated provenance => abstain. The new E002-464 gate itself is still research-only and cannot authorize release.

E002-371 **NOT PHYSICALLY VALIDATED**. No new human anatomical trajectories, authenticated shutter or hard physiological velocity caps. Hidden closure, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. S21/S22 remain sealed; Hush branch/PR #45 untouched. Draft PR #26 stays unmerged.
