# E002-454 — zero-of-649 is weak evidence for a physical cap

**Date:** 2026-10-26. **Protocol frozen first:** [E002_454_FROZEN.md](E002_454_FROZEN.md), commit `f476f7de05dbd9d4252d76713d8cb556e258daed`. **Input:** [E002-453 checksum-verified external human aggregate](E002_453_HUMAN_AGGREGATE.json), from Culemann et al. (2026), DOI [10.3758/s13428-026-02984-4](https://doi.org/10.3758/s13428-026-02984-4). This is a **new dataset-specific rank diagnostic** of the E002-453 sample-maximum transfer test, not new raw human measurements. The participant-clustering and exact-binomial issue was **already established by Lucent E002-440** (synthetic clustered-study falsification and release ledger). Neither Clopper–Pearson bounds nor pseudoreplication are novel here. E002-454 adds the exact **12/17 no-exceedance null benchmark for the real E002-453 split**, not a new statistical theorem.

## Result: a sample-maximum validation can pass almost by construction

E002-453 observed zero exceedances of its 12-person calibration maximum among 649 blinks from five held-out participants. Under an explicitly **conditional** null of exchangeable, continuous participant-session maxima and a split selected independently of velocities, the event that no holdout blink exceeds the training maximum is exactly the event that the single global maximum belongs to the 12 calibration participants. Hence:

`P(no holdout exceedance of calibration maximum | exchangeable unique participant maxima, 12/5 split) = 12/17 = 70.5882%`.

An independent enumerator over the 17 possible positions of the global maximum reproduces the fraction. The 0/649 result is therefore **unsurprising even when there is no finite physiological upper bound**. This is not a conventional p-value or a proof of unbounded physiology; it is a design-sensitivity benchmark. The identity does not apply to the 99th-percentile or gaze-stratified caps, which require separate analyses.

## Existing E002-440 cluster lesson, quantified for this real-data split

For the binary event **at least one peak estimate exceeds the fixed training cap during a comparable participant session**, zero events in five held-out participants gives a one-sided exact 95% upper binomial confidence limit:

`1 - 0.05^(1/5) = 45.07197%`.

The misleading computation treating all 649 blink events as iid would instead give `1 - 0.05^(1/649) = 0.46053%`, underestimating the upper limit by **97.87x**. The participant-level bound itself assumes independent comparable people and a fixed training-derived cap; it is not a guarantee for different devices, gaze tasks, or populations. The number of blinks per participant and selection effects could further limit transfer.

**Frozen kill criteria triggered:** null probability 70.6% >= 50%; participant upper bound 45.1% >= 10%. Therefore **reject** the claim that E002-453's zero exceedances strongly validate a universal physiological cap. Retain the factual descriptive result that no exceedance occurred in that particular five-person holdout.

## Priority audit and verification\n\n[E002-440](E002_440_RESULT.md) already established the participant-level Clopper–Pearson correction and false reassurance from treating repeated intervals as independent. The present calculation is incremental; do not present the 45.1% bound as a newly discovered statistical result. The **70.6% rank-null calculation** is the incremental dataset-specific diagnostic.\n\n## Verification and reproducibility

- Standard-library analyzer: [e002_454_cluster_inference.py](e002_454_cluster_inference.py), fail-closed on inconsistent source metadata, nonzero/missing events, invalid counts, nonfinite values, or a physical-release flag.
- [11 synthetic/adversarial tests](test_e002_454_cluster_inference.py) passed locally. These include independent combinatorial enumeration and inversion of the exact binomial tail. No human video or raw participant rows were used in this pass.
- A second, independent JavaScript calculation of the **committed E002-453 human aggregate** reproduced the Python numerical results to <1e-12; see [machine-readable result](E002_454_CLUSTER_AGGREGATE.json). This cross-language check verifies arithmetic, not the exchangeability assumptions.
- [Dedicated hosted CI](../../.github/workflows/e002_454_cluster_inference.yml) was added to replay the actual committed aggregate and adversarial tests. **Hosted execution has not yet been verified** at report creation; do not claim a hosted pass.

Reproduce from repository root:
```bash
cd research/observability
python -m unittest -v test_e002_454_cluster_inference.py
python e002_454_cluster_inference.py --aggregate E002_453_HUMAN_AGGREGATE.json
```

## Scientific and product consequence

The 12/5 split and published per-blink estimates are insufficient to establish a physical upper velocity bound. A larger held-out sample alone cannot certify a universal deterministic limit; rare/unseen physiology and calibration error remain. No shutter/exposure authentication, high-speed anatomical trajectory, or prospective hidden-closure prediction was obtained. S21/S22 remain untouched.

**Next decisive work:** collect independently calibrated high-speed anatomical eyelid trajectories with hardware-authenticated exposure timing, blinded landmark reliability, gaze/blur/brightness/glasses/clock controls, and a prespecified participant-disjoint test of the sharp hidden-closure predictions. Prefer real new measurements to further reanalysis of the same 17-person CSV.

**Release:** E002-371 remains physically unvalidated. Hidden closure, blink duration, PERCLOS, fatigue, and medical claims remain `ABSTAIN_UNCALIBRATED`. Keep PR #26 draft and unmerged. Hush branch and PR #45 are separate and untouched.
