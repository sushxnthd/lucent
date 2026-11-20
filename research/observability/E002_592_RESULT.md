# E002-592 | Camera contrast budget falsifies an unqualified ideal-aperture observability transfer

**Date:** 2026-11-01 UTC. **Kernel:** E002-371. **Preregistered:** [E002_592_FROZEN.md](E002_592_FROZEN.md), commit `6ec67382b8d3ca90d6866dd13412727c18c1943e`. **Evidence tier:** exact-rational synthetic camera-transfer experiment with two independently implemented runtimes. **No physical-camera or human validation.**

## Question and result

E002-591 proves a sharp *ideal aperture-mean* separation for sustained closure. The present experiment tests the transfer to **measured pixel brightness**, which depends on independently authenticated aperture-to-pixel contrast and nuisance budgets.

Fix normalized exposure T=1, baseline aperture c=1/2, closure threshold tau=1/10, dwell d=3/5, and speed L=VT=20. Every admissible sustained closure has aperture mean at most 839/2000 (0.4195), whereas the constant-open control has mean 0.5. The exact difference is 161/2000 (0.0805). An explicit closure witness with knots `(0,1/2),(1/50,1/10),(31/50,1/10),(133/200,1),(39/40,1),(1,1/2)` attains that bound, with exactly 60% dwell and speed at most 20.

Use the deliberately simple camera model Y=b+kappa*mean(aperture)+eta. Here kappa is a positive, **independently known** per-trial contrast coefficient, while b and eta are bounded independently by B and E in each candidate history. The constant-open and closure observation envelopes are disjoint exactly when

`kappa*(c-M_d(L)) > 2*(B+E)`.

Equality is a touching boundary and **requires abstention**. This is a two-hypothesis, model-conditional separability criterion, not a general absence-of-blink certificate. If kappa is not independently bounded below, or imaging assumptions are unverified, it abstains.

| Frozen condition | Contrast kappa | B | E | Exact margin | Decision |
|---|---:|---:|---:|---:|---|
| Low contrast | 0.2 | 0.01 | 0.005 | -0.0139 | OVERLAP_ABSTAIN |
| High contrast | 0.6 | 0.01 | 0.005 | +0.0183 | MODEL_SEPARABLE_ONLY |
| Larger illumination uncertainty | 0.6 | 0.02 | 0.005 | -0.0017 | OVERLAP_ABSTAIN |
| Higher speed L=100 | 0.6 | 0.01 | 0.005 | -0.00114 | OVERLAP_ABSTAIN |
| Exact touching contrast 60/161 | 60/161 | 0.01 | 0.005 | 0 | OVERLAP_ABSTAIN |

**Counterexample:** For kappa=0.2, the always-open center is 0.1 and the maximum-mean closure center is 0.0839. Their nuisance intervals overlap: the same measured brightness can be produced by both, despite the ideal-aperture means being provably different. The Python simulator constructs exact allowable illumination/read-error decompositions of the shared measurement. This falsifies the product claim that an ideal aperture separation necessarily transfers to a real camera image.

## Verification and adversarial controls

The [Python implementation](e002_592_sensor_transfer.py) and [independent Node BigInt verifier](e002_592_independent_replay.cjs) each passed five frozen rational cases and 1,000 deterministic synthetic adversarial combinations. Python seed 592 (Mersenne Twister) yielded 274 separable and 726 overlap/abstain conditions; independent Node seed 592 (xorshift32, **a different ensemble**) yielded 279 separable and 721 overlap/abstain conditions. These counts are synthetic model stress tests, **not** human success rates. Both agree on all five exact frozen cases and the 839/2000 witness integral. Python additionally passed 12 fail-closed calibration/nuisance controls and three invalid-input controls. The independently implemented Node code verifies that every emitted separability result has strictly nonoverlapping mathematical envelopes.

The [hosted workflow](../../.github/workflows/e002_592_sensor_transfer.yml) is committed. Its actual conclusion must be checked before reporting hosted success. No camera images, human anatomy, private participant records, or external datasets are included.

## Data acquisition attempts and literature limits

Two targeted public-source searches this run found Kwon et al. (2013, [DOI 10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227)) reporting **600-fps** human eyelid measurements, but did not establish downloadable native videos with authenticated original capture timestamps. OpenEDS ([arXiv 1905.03702](https://arxiv.org/abs/1905.03702)) reports **200-Hz** synchronized eye-facing imagery but access is by request; it does not supply a verified open 400–600-fps raw physical shutter-reference dataset. The [mEBAL2 dataset](https://github.com/BiDAlab/mEBAL2) is approximately **30-Hz** and requires a signed access agreement. The [MPEblink Zenodo dataset](https://zenodo.org/records/7754768) is a large in-the-wild blink benchmark but does not establish independently calibrated high-speed eyelid velocity or shutter metrology. This is an access/measurement limitation, not evidence that no such dataset exists.

The sensor transfer inequality is elementary bounded-error interval separation, not a claim of mathematical priority. Radiometric response calibration and temporal integration are established topics. The new contribution of this experiment is a precisely specified **falsification of an overstrong Lucent product inference**, with an executable abstention boundary. It has not undergone external peer review.

## Decisive human study and release gate

Freeze participant-disjoint calibration/holdout, anatomical closure threshold, minimum dwell, independently justified velocity ceilings, radiometric response and per-exposure nuisance intervals before examining holdout. Simultaneously record eyelids at preferably 400–600 fps and an ordinary 30-fps camera with independently measured shutter/rolling-row/clock support. Obtain two blinded anatomical rater streams, and separate test strata for gaze, glasses, blur, brightness, occlusion and missingness. Measure aperture-to-pixel contrast and nuisance envelopes on calibration participants **without using held-out closure labels**. Test held-out predictions prospectively and report false exclusions and abstention by participant/session cluster. Any real closure inside a supposedly certified exclusion falsifies the claim or its premises.

**Physical captures: 0. Independent anatomical rater pairs: 0. Authenticated shutter calibrations: 0. Hard human velocity ceilings: 0. Held-out physical predictions: 0.**

**Product consequence:** a positive ideal aperture-mean margin is insufficient to emit a real-world no-hidden-closure certificate. Missing contrast/brightness/geometry/blur/gaze/glasses/sampling/clock evidence must abstain. The model-only `MODEL_SEPARABLE_ONLY` state must never be surfaced as clinical, fatigue, PERCLOS, or physiological certification. **Product ABSTAIN_UNCALIBRATED; release BLOCKED.** Keep draft PR #26 unmerged.
