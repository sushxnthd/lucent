# E002-676 | Instrument-ready shutter-gap challenge (2026-11-06 UTC)

**Evidence tier:** executed exact-rational synthetic fixture, NOT human or physical validation. This is a testable engineering stimulus, not a new theorem or a physiological speed bound.

## Frozen matrix and outcome
Endpoints are normalized aperture 1; closure threshold 0.30. A symmetric maximum-speed triangular occlusion has a midpoint aperture max(0,1−VΔ/2). The gap exclusion criterion is V(Δ+2ε)<1.4, where ε bounds timestamp uncertainty at each end. Freeze gaps 20/30/40/50 ms, V=20/30/40 aperture units/s, and ε=0/1/3 ms. The standard-library exact-rational executable generates all 36 rows and checks that no valid exclusion coexists with the constructed hidden closure.

**Executed local result:** 36 cases; 26 conditional exclusions; 9 constructed hidden-closure cases; zero contradictory cases. These are deterministic constructed trajectories, not an empirical sensitivity estimate. The 1 remaining case is neither a strict exclusion nor a closure witness.

**Adversarial falsifier:** At Δ=40 ms, falsely claiming V=20 certifies no closure, whereas a physically possible trajectory at V=40 reaches aperture 0.20. Therefore any unverified hard speed ceiling invalidates absence claims, regardless of how many synthetic assertions pass.

## Reproduce
`python research/observability/e002_676_fixture.py --out fixture.csv`
Expected stdout: `cases 36 certified 26 hidden 9`, followed by the wrong-speed falsifier. CSV is generated, not committed; source code is the durable reproducible artifact.

## Physical test that could disconfirm the instrument pipeline
Use a motorized or electronically driven calibrated aperture/occluder and a separately timestamped photodiode, not an ordinary phone alone. Independently verify the occluder's maximum speed, optical aperture mapping, shutter exposure kernel, synchronization offsets, frame loss and rolling shutter. Capture the 36 frozen conditions with ordinary camera plus independent high-speed reference. Do not fit thresholds to the test captures. Compare positive reference closures to exclusion decisions; any verified false exclusion blocks the calibration claim. Repeat under altered geometry, illumination, blur, gaze-like occluder offset, lens/eyewear analog, missing frames and clock drift. Preserve raw timestamp traces and negative cases.

## Human transfer prohibition
A motor fixture does not establish any deterministic bound on human eyelid velocity, anatomical aperture geometry, or sleepiness. The E002-671 blinded, participant-held-out human protocol is still required. No human footage or physical device was acquired or analyzed in this run. Product: `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
