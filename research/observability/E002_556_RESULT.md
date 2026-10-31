# E002-556 RESULT | Instrument-facing complete-support shutter calibration

Date: 2026-10-31. Frozen protocol commit `a2f637a` preceded implementation. Evidence tier: **executable instrument ingestion and seeded synthetic/independent-oracle tests only; no authenticated physical capture or human eyelid measurement.**

## Experimental change, not another shutter theorem
E002-554 demonstrated that central-only flash calibration can conceal edge sensitivity and falsely exclude a real closure. E002-556 replaces the untestable point-estimate shortcut with a **complete temporal partition acquisition interface**: independently clocked, constant-intensity LED/photodiode pulses must span every part of the bounded shutter support. The operator provides raw-linear dark-corrected camera responses and photodiode amplitudes, with error bounds and three replicates per bin. The executable refuses missing edges, gaps, overlap, unbounded photodiode amplitude, incompatible replicates, fewer than eight bins, or fewer than four informative composite holdouts.

For each bin j, response uncertainty produces a nonnegative shutter-mass interval [qlo_j,qhi_j]. The normalized temporal variance is bounded without assuming a boxcar within a bin, by the pairwise identity Var(T)=E[(T-T')^2]/2 and the worst possible separation of two independently sampled points within or across timing-expanded bins. Every held-out composite LED pattern predicts an interval for normalized camera response. A disjoint observed interval **falsifies** the calibrated model. Overlapping intervals mean only *not falsified*, not proof.

## Reproducible synthetic instrument checks
- Eight 1-ms bins; three synthetic replicates per bin; 2-us timing uncertainty; four withheld composite patterns; known nonuniform shutter masses [1,2,3,4,4,3,2,1]/20.
- Exact piecewise-uniform synthetic truth variance: **3,333,333.333 us^2**.
- Conservative calibrated variance interval: **[1,562,081.341, 6,036,839.217] us^2**, containing truth but too wide to support a sharp close-call exclusion.
- All four correctly generated synthetic holdouts overlap their prediction intervals. A corrupted held-out response of 0.99 is detected as `CALIBRATION_FALSIFIED`.
- Local V8 arithmetic checked the valid fixture, truth containment, corrupted holdout and rejection of missing support, inconsistent replicates, unbounded photodiode error and noninformative patterns. The committed Node regression file has **14 checks**; hosted execution must be checked separately.
- Independent Python direct-moment oracle ran **2,000 seeded randomized piecewise-uniform shutters**, with **zero interval-containment violations**; maximum observed relative interval width was **1.688249**. This independently verifies the conservative pairwise envelope against the direct-moment calculation, but does not validate physical camera behavior.

## Files and reproducibility
- [Frozen protocol](E002_556_FROZEN.md)
- [No-dependency Node capture auditor](e002_556_partition_calibration.cjs): `node research/observability/e002_556_partition_calibration.cjs capture.json` or `--self-test`
- [Adversarial Node regression](test_e002_556_partition_calibration.cjs)
- [Independent Python moment oracle](e002_556_independent_oracle.py)
- [CI workflow](../../.github/workflows/e002_556_instrument.yml)

## Acquisition handoff
Collect **real** full-support partition captures with an independently synchronized photodiode, camera raw-linear pixel intensities, matched darks, at least two illumination and exposure settings, and sensor-row-specific timing. Predeclare and withhold four composite waveforms. Preserve source hashes, hardware logs and calibration provenance outside the public repo. Run this auditor without adjusting error bounds after holdout inspection. Confirm LED waveform is constant *within* each bin and independently calibrated. Then test moving-aperture target and two blinded anatomical raters; a high-speed reference-negative is not continuous-time absence.

## Kill and novelty limits
- A finite partition without a certified outer support bound, response linearity, photodiode stability and clock error **cannot** establish shutter variance. Intra-bin response may be arbitrary; intervals are deliberately conservative.
- All outputs are `MODEL_CONSISTENT_UNAUTHENTICATED` or `CALIBRATION_FALSIFIED`, never release permission. Even a model-consistent real instrument would not supply an independently certified continuous-time eyelid speed/acceleration bound or anatomical transfer.
- Underlying variance identity and interval arithmetic are classical; this is a **physical-instrument acquisition and falsification implementation**, not a novel general theorem or measured human result.

Authenticated physical shutter captures **0**; independent blinded anatomical rater pairs **0**; hard physiological motion ceilings **0**; participant-disjoint physical predictions **0**. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Next priority: execute the protocol with actual optical hardware or authorized human video, not another synthetic shutter law.
