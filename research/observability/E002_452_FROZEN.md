# E002-452 — frozen external-human gaze challenge and product release consequence (2026-10-26)

**Priority:** physical validation of E002-371. **Evidence tiers:** (A) independent peer-reviewed *human* group results, (B) deterministic conditional simulator, (C) no Lucent-measured human anatomical velocity, no certified physical release. Do not conflate these tiers.

## Newly identified independent human observations (frozen before coding)
1. Culemann et al., *Behavior Research Methods* 58:89 (published 2026-03-20), DOI 10.3758/s13428-026-02984-4, report **2,306 voluntary blinks from 17 participants**. A +5° to -15° vertical gaze change is associated with **+21 mm/s peak closing velocity**, **-22 mm/s peak opening velocity**, **+28 ms (~8%) eyelid-based blink duration**, and **+73 ms (~32%) pupil-based duration**. These are group-level condition differences, **not a certified maximum**. Raw recordings are withheld for privacy; anonymized aggregated analysis data and code are linked at https://osf.io/tud8a.
2. Kim et al., *PNAS* 122:e2508058122 (2025), DOI 10.1073/pnas.2508058122, and the FaceBase 2026 release DOI 10.25550/88-28BJ document 400-fps hardware-synchronized **3D eyelid-margin kinematics** for eight adults across five behaviors. **Restricted human data**; no access claimed. This is a strong target for independent calibrated velocity validation, not a data source available for this run.
3. Published studies disagree on direction of closing-velocity dependence for different protocols (Culemann 2026 discussion of VanderWerf 2003). No universal direction or pooled safety cap can be inferred.

## Frozen conditional falsification
Using **illustrative, NOT human-calibrated** endpoint apertures 3.0 and 3.0 mm, threshold 2.0 mm, a 9.5-ms exposure-free interval, and hypothetical gaze-stratum speed caps 200 and 221 mm/s: the sharp Lipschitz endpoint lower envelope is (a0+a1-V*T)/2. Predict **2.05 mm** for 200 mm/s (no hidden threshold crossing) and **1.95025 mm** for 221 mm/s (crossing feasible). The 21 mm/s difference is selected to match the *published group contrast*, not to claim either cap is physiological. Reject any physical certification from this fixture.

## Frozen release decision
A physical no-hidden-closure claim must not be emitted without (i) authenticated exposure timing/shutter model, (ii) independently validated anatomical aperture scale, (iii) an externally justified **upper** speed bound valid for the subject, gaze and behavior strata (not group mean/percentile), (iv) validated nuisance envelope, and (v) prospective participant-disjoint testing. Missing or mismatched gaze stratum, source class, or evidence tier -> `ABSTAIN_UNCALIBRATED`; no pooled-mean fallback. The code should be a **research-only conditional simulator** and an explicit refusal policy, not a clinical or fatigue product.

## Frozen checks
- Conditional envelope numerical predictions above and boundary at dimensionless ratio 1.
- All uncertified or missing evidence must abstain, including purported self-declared booleans.
- Reject invalid/negative/nonfinite values, infeasible endpoints, unknown gaze/behavior strata, finite-exposure averages passed as instantaneous points, missing clock/geometry/nuisance provenance.
- No subject data, private images, holdout S21/S22 reads, or publication of restricted FaceBase content.
- After implementation, run local tests and, if possible, repository-hosted tests. Report verification tier honestly.

**Novelty discipline:** this is an externally sourced human confound and a concrete release-claim falsification, **not** a new theorem or original human study. It does not validate E002-371.