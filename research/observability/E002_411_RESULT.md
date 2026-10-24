# E002-411 — sparse LED phase sweeps cannot certify an arbitrary shutter moment

**Date:** 2026-10-24. **Evidence tier:** preregistered analytic + seeded **synthetic optical-instrument** falsification, independent numerical quadrature and source-level release-gate regression. **Not** physical camera calibration, real human aperture validation or a new general theorem.

## Frozen experiment and independently verified result

The [frozen protocol](E002_411_FROZEN.md) was committed first at `1726e08`. The analytic experiment is `e002_411_phase_identifiability.py`; the independently coded midpoint-quadrature oracle is `e002_411_independent_check.py`; regression tests are `test_e002_411_phase_identifiability.py`. The initial [GitHub Actions run 40069693532](https://github.com/sushxnthd/lucent/actions/runs/40069693532) completed successfully, including all preregistered analytic/randomized predictions, independent numerical integration and source-level fail-closed tests. Subsequent explicitly labeled exploratory positive-signal controls were added in separate commits; their CI must be checked separately before describing them as independently verified.

**Preregistered witness:** 10-ms exposure, 0.2-ms independently timed rectangular LED pulses starting at phases 0,1,...,9 ms. Two nonnegative normalized shutter kernels, uniform on [5.5,5.7] and [9.5,9.7] ms, yield **identical ten pulse measurements (all zero)** and identical constant-light response (one). Yet their first absolute moments about the 5-ms exposure center are **0.6 ms versus 4.6 ms**, a **7.6667×** difference. Both remain invisible when each scanned pulse is conservatively expanded by +/-0.05 ms to cover phase jitter. A denser 0.1-ms scan distinguishes these two witnesses but is not a uniqueness proof for unrestricted continuous kernels.

**Randomized frozen falsification:** all **1,000/1,000** seeded shutter pairs were indistinguishable on the sparse pulse scan. Their first-moment separations ranged from **3.802099 to 4.197954 ms**, satisfying the frozen >=3.5-ms threshold. The independent 100,000-bin midpoint oracle returned **0.600000 and 4.600000 ms**, within the preregistered 0.005-ms tolerance. The sparse scan left **7.05 of 10 ms** of exposure support unilluminated even with +/-0.05-ms jitter expansion.

**Exploratory post-freeze positive-signal control:** Mix each witness at 50% with the same uniform shutter response. All ten measured pulse responses become the same **strictly positive 0.01**, with the same DC response of one, yet the shutter moments remain different: **1.55 versus 3.55 ms** (difference **2.0 ms**). This rules out the trivial interpretation that the ambiguity occurs only because the instrument reads zero everywhere. This supplementary control was not preregistered and is not included in the original P1–P6 claim.

## Scientific meaning

The shutter measurement is an inverse problem. With a nonnegative normalized kernel `w(s)`, each pulse observation is `y_j = integral w(s) 1_{[phase_j,phase_j+p]}(s) ds`. If part of the possible shutter support is never illuminated, shutter mass can be moved within that blind region without changing any measured `y_j`. The first absolute moment `M = integral |s-t_center| w(s) ds` can nevertheless change substantially. DC normalization does not resolve the ambiguity. Thus **nominal exposure duration, DC normalization and a sparse pulse scan cannot uniquely establish `M`** without additional independently justified response constraints. This is an elementary partial-identification construction, not novel general mathematics.

E002-403 already demonstrated that underestimating `M` can generate a false E002-371 no-hidden-closure certificate. E002-411 identifies a concrete **calibration-instrument failure mechanism** that could supply such an underestimated `M`. The witness is deliberately adversarial and does not establish that real cameras exhibit these shutter kernels.

## Literature and priority boundary

Temporal camera calibration and LED-based rolling-shutter measurement are established. Relevant primary sources include Kurosawa et al. (2024), *Development of a device to measure the temporal imaging characteristics of CMOS/CCD cameras*, DOI [10.3408/jafst.875](https://doi.org/10.3408/jafst.875), which experimentally validates a multi-LED timing device; Huai et al. (2023), *Automated rolling shutter calibration with an LED panel*, DOI [10.1364/OL.474375](https://doi.org/10.1364/OL.474375); and Dong et al. (2022), *Parametric modeling and experimental measurement of rolling shutter characteristics for optical camera communication*, DOI [10.1364/AO.468009](https://doi.org/10.1364/AO.468009). This targeted priority check **does not establish global novelty** for phase-sweep nullspaces or moment partial identification. Lucent may claim only its application-specific falsification and gate, subject to deeper literature review.

## Enforced research/product consequence

`shutter_release_gate` rejects incomplete pulse-phase coverage, missing independently measured pulse shape/photodiode, missing hardware clock, missing rolling-shutter row response, and missing physical first-moment bound. Even when these **necessary** checks pass, the output remains `product=ABSTAIN_UNCALIBRATED`; a dense scan alone does not authenticate a continuous shutter kernel or human physiology. This gate is a **research qualification function**, not a completed production hardware attestation. The existing human annotation bridge still relies on externally audited provenance and must not be treated as independent authentication.

**World-class completion gate remains open:** real optical shutter-response measurements with independent timebase and row calibration, two blinded human aperture-rater sheets, independently justified physical eyelid velocity, held-out participant/device shutter-gap predictions, adversarial nuisance tests and external replication. No hidden-closure guarantee, blink duration, PERCLOS or fatigue product claim is authorized. [Vector figure](E002_411_IDENTIFIABILITY.svg).

## Reproduce

```bash
python research/observability/e002_411_phase_identifiability.py
python research/observability/e002_411_independent_check.py
python -m unittest discover -s research/observability -p 'test_e002_411_phase_identifiability.py' -v
```

No proprietary datasets, eye images, API costs or participant records are needed. Negative results and the unmerged draft PR are preserved.
