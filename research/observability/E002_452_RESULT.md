# E002-452 — Independent human gaze evidence changes the physical-claim gate

**Date:** 2026-10-26. **Frozen before code:** [E002_452_FROZEN.md](E002_452_FROZEN.md), commit `e32371e69b54e1292013c465e679fe20b4b991fb`. **Evidence tier:** independently published *human* group observations plus a new conditional simulator and 12 locally replayed synthetic/adversarial tests. **No new Lucent human aperture labels or authenticated shutter/velocity calibration.** This is not a new theorem or an original human experiment.

## Decisive newly incorporated human evidence

**Culemann et al. (2026),** *Behavior Research Methods* 58, article 89, [DOI 10.3758/s13428-026-02984-4](https://doi.org/10.3758/s13428-026-02984-4), report **2,306 voluntary blinks from 17 people** across +5°, -5°, and -15° vertical eye-in-head orientation. Comparing +5° with -15°, the paper reports a **+21 mm/s group difference in peak closing velocity**, **-22 mm/s in peak opening velocity**, **+28 ms (~8%) eyelid-based duration**, and **+73 ms (~32%) pupil-based duration**. The 2026 paper explicitly contrasts its closing-velocity direction with an earlier search-coil study, so a universal gaze trend is not justified. Its raw video is unavailable under privacy restrictions; anonymized aggregated analysis data and scripts are identified at [OSF tud8a](https://osf.io/tud8a). **These are reported group effects, not measured worst-case speed caps, and the paper's participants were instructed to blink voluntarily.** The publication is independent evidence that gaze is a non-negligible nuisance, not independent validation of E002-371.

**Kim et al. (2025),** *PNAS* 122:e2508058122, [DOI 10.1073/pnas.2508058122](https://doi.org/10.1073/pnas.2508058122), show that eyelid kinematics differ across behaviors and are not reducible to one universal open-close scalar. The [FaceBase release dated 2026-09-01](https://staging.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/) describes 400-fps hardware-synchronized 3-D eyelid-margin motion capture from **eight adults**, with five blink/closure behaviors, [dataset DOI 10.25550/88-28BJ](https://doi.org/10.25550/88-28BJ). **Restricted access (GRU/NPU): not downloaded, accessed, or reanalyzed.** This is the strongest identified direct external anatomical velocity validation target, but its licensing and subject/behavior coverage prevent assuming a deployable universal cap.

## Frozen conditional falsification: gaze-stratum choice reverses the decision

Under an **illustrative, hypothetical** instantaneous 3.0-mm aperture at each endpoint, 2.0-mm closure threshold and 9.5-ms unsampled gap, the sharp assumed-Lipschitz lower envelope is `(a0+a1-V*T)/2`. The dimensionless ratio is `V*T/(a0+a1-2*c)`. These are mathematical conditional calculations, not measured anatomy.

| Hypothetical cap | Ratio | Minimum possible aperture | Conditional outcome |
|---|---:|---:|---|
| 200 mm/s (illustrative upward) | 0.95 | 2.05000 mm | hidden threshold crossing excluded under assumptions |
| 221 mm/s (illustrative downward) | 1.04975 | 1.95025 mm | hidden threshold crossing feasible under assumptions |

The difference **21 mm/s** was deliberately chosen to echo the published *group contrast* and expose decision sensitivity; **200 and 221 mm/s are NOT independently measured physiological maxima**. A clock uncertainty of ±0.3 ms per endpoint reverses the first conditional exclusion when conservatively propagated. The program rejects shutter-averaged endpoints, unmeasured gaze or behavior, invalid units, inconsistent endpoints, and attempts to relabel hypothetical evidence as human-certified.

[Conditional simulator](e002_452_gaze_boundary.py) · [12 adversarial tests](test_e002_452_gaze_boundary.py) · [dedicated hosted workflow](../../.github/workflows/e002_452_gaze_boundary.yml). **Local 12/12 passed on a byte-matched development copy; hosted repository replay is pending unless a completed run is separately verified.** The simulator cannot emit a physical product authorization even if callers supply fabricated evidence booleans.

## Concrete claim consequence

The prior idea of selecting a pooled single literature velocity number for ordinary-camera physical closure certification is **rejected**. A published *mean peak* velocity, empirical sample maximum, or percentile is **not a validated hard upper bound**. A valid deterministic claim requires an independently justified bound that covers the full specified population/behavior/gaze range, camera shutter integration, exposure and clock error, geometry, and realistic nuisance variation. A physical speed bound may remain unattainable without narrowly restricted assumptions.

**Allowed now:** transparent synthetic conditional interval analysis; offline image-space annotation research with clear uncertainty and refusal. **Not allowed:** no-hidden-closure guarantee on actual webcam recordings, blink duration, PERCLOS, fatigue, or medical claims. The code's physical gate always returns `ABSTAIN_UNCALIBRATED` until an externally reviewed evidence verifier exists; a user-supplied boolean cannot bypass it.

## Next decisive human protocol (no data collected in this run)

1. **First priority: request authorized access** to FaceBase 88-28BJ (non-profit human data terms) and separately seek author permission for calibrated gaze-stratified 2026 recordings. Do not bypass restrictions. The OSF release is suitable for checking published *group statistics*, **not** deriving sample-by-sample anatomical hard velocity bounds from raw high-speed trajectories.
2. For new measurements, freeze camera hardware synchronization and shutter impulse-response calibration **before** human recordings. Use high-speed anatomical landmarks (target >=400 fps), independently calibrated mm scale, and simultaneous 30/60-fps ordinary-camera streams. Measure clock uncertainty and rolling shutter, rather than trusting AVI fps tags. Obtain ethics/consent.
3. Include upward/neutral/downward gaze, spontaneous/voluntary/reflexive behavior where ethical and feasible, glasses/occlusion, blur, illumination, head motion, and participant diversity. Annotate margin geometry with two independent raters; report their disagreements and missingness, never impute missing closed states as open.
4. Freeze the full conditional classifier, velocity bound construction, and nuisance exclusions on calibration participants. Keep **participant-disjoint holdouts** sealed. On holdouts, test the decisive statement: **every interval labelled `EXCLUDED` must contain no hidden threshold crossing in independently observed high-speed anatomy**. One well-authenticated crossing in an excluded interval falsifies that cap/claim. Report abstention rate and failure counts by gaze/behavior/camera. Zero failures does **not** prove a universal deterministic bound; any statistical risk statement needs subject-cluster-aware uncertainty.
5. If only bounded empirical risk is defensible, change product claims to calibrated risk estimates with explicit domain, uncertainty, and abstention. Do not market them as deterministic physical impossibility.

**S19:** 0 human anatomical rater exports; sync event clock not authenticated as sensor exposures. **S21/S22:** untouched prospective holdouts. **Hush:** separate branch/PR #45 untouched. Keep Lucent PR #26 draft and unmerged.

## Reproduction

```bash
cd research/observability
python -m unittest -v test_e002_452_gaze_boundary.py
python e002_452_gaze_boundary.py --conditional-fixture
```

This run adds a source-grounded *human nuisance finding and release-policy consequence*, **not physical validation**. E002-371 remains `NOT_ESTABLISHED`.
