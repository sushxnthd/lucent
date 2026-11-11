# E002-466 — detection floors falsify naive optical shutter-phase brackets

**Date:** 2026-10-26. **Evidence tier:** frozen synthetic instrument falsification; local Node adversarial replay and independent exact-rational Python check. **Physical acquisitions: 0. New human anatomical trajectories: 0.** This is an incremental instrument-metrology correction to E002-465, not a new general theorem or physiology.

## Question and frozen result

E002-465 uses the first and last nonzero camera responses to an independently timed optical pulse to bracket exposure support. Its ideal result explicitly assumes noiseless, zero-floor detection. Can an ordinary positive detection threshold be mistaken for exact zero?

The [protocol](E002_466_FROZEN.md) was committed first (`06685efffaacee96f64e8011942884ef6604f4cb`), before implementation. The frozen shutter is [0,0.4] ms; pulse width 0.1 ms; phase step 0.05 ms; integrated-intensity detection threshold 0.15. True overlap response is overlap/0.4, but the observer receives only detected/not-detected flags.

**Naively treating non-detection as zero overlap gives false shutter endpoint brackets** (all ms):
- Start inferred [0.05,0.10], although the true start is **0.00**.
- End inferred [0.30,0.35], although the true end is **0.40**.

Both errors occur in a perfectly linear, noiseless synthetic camera: the only nuisance is a known finite detection floor. This invalidates applying E002-465's ideal zero/nonzero transition formula to thresholded imaging responses without adjustment.

## Restricted conservative correction

For a known linear uniform shutter with width w <= w_max, gain g >= g_min > 0, finite known pulse width p, fixed authenticated threshold tau and exact/noiseless phase timing, non-detection implies optical overlap <= delta = tau*w_max/g_min. Because the rectangular-pulse overlap is unimodal as phase increases, the first detected phase f and immediately preceding nondetected phase z give a conservative start interval [z+p-delta, f+p]. Similarly, last detected phase l and next nondetected phase z' give an end interval [l,z'+delta]. Numerical code adds 1e-10 ms outward arithmetic slack, which is **not** a physical uncertainty estimate.

The dimensionless detector dead-zone ratio is **eta = delta / h = tau*w_max/(g_min*h)** for phase step h. When eta is non-negligible, the phase grid resolution h alone does not determine shutter-edge uncertainty.

Frozen case: delta=0.06 ms, eta=1.2, corrected start approximately [-0.01,0.10] ms and end [0.30,0.41] ms. Both true endpoints are enclosed. This deliberately widens, rather than overclaims, the admissible exposure supports.

## Reproducible falsification and adversarial controls

- [Executable threshold-aware simulator and inference](e002_466_thresholded_phase_scan.mjs).
- [17 Node adversarial tests](test_e002_466_thresholded_phase_scan.mjs).
- [Independent exact-rational Python reproduction](e002_466_independent_rational.py).
- [Dedicated GitHub Actions workflow](../../.github/workflows/e002_466_thresholded_phase_scan.yml).

Local Node 22 execution: **17/17 tests passed**. A seeded, held-out synthetic parameter sweep of **10,000** shutter offsets, widths, gains, detection thresholds and phase offsets yielded **9,471 conditionally bounded synthetic cases**, **529 abstentions**, and **0 bracket-containment failures** among the accepted cases. These are simulator checks, not camera/human performance estimates. Independent Python `fractions.Fraction` arithmetic reproduced the frozen false naive brackets and corrected conservative bounds exactly.

The evaluator refuses certification when the threshold, gain lower bound, exposure width upper bound, phase clock, optical pulse support, zero-noise assumption, linearity, non-clipping, sensor-memory bound or row identity is unverified. Missing/nonuniform phases, disconnected detections and unbracketed transitions abstain. There is no physical-release output path.

## Product and acquisition consequence

The phase-scan physical protocol must characterize **the minimum detectable optical overlap**, not merely detect the first nonzero-looking pixel. Record dark/flat controls, unsaturated RAW response, per-row gain floor, measured emitted pulse energy, independent pulse clock, noise and temporal tails. In a real camera, zero noise and exact finite support are not credible assumptions; this executable estimator is therefore **not field-ready**. Replace it with a separately validated noise/uncertainty set-membership estimator, or abstain. Do not convert a nondetected pulse into a hard shutter edge.

A prospective physical acceptance test should preregister a held-out phase/intensity/row matrix; independently measure pulse timing and energy; fit threshold/gain/clock/tail uncertainty on calibration runs; seal predictions before evaluating held-out optical traces; and report shutter-support coverage, failures and abstentions by nuisance stratum. Preserve raw camera and photodiode data with checksums. Then test a calibrated moving-aperture instrument and only afterward participant-disjoint anatomical eyelid trajectories.

**E002-371 is NOT PHYSICALLY VALIDATED.** Physical hidden-closure, blink duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. S21/S22 remain sealed. No product release, PR merge, or physical/human evidence is claimed.
