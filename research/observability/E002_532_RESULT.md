# E002-532 RESULT | Coded-light shutter calibration is identifiable only under an instrument model

2026-10-30. Primary E002-371 human-validation kernel, existing branch `research/observability-human-boundary`, draft PR #26. [Frozen protocol](E002_532_FROZEN.md) committed at `271de1a82c501a76bf17eec145960dca8a6578f0` before executable construction.

**Evidence tier: deterministic synthetic optical-instrument validation and a real-capture intake interface. NOT a physical camera calibration, new human physiological evidence, new general theorem, or deployment-ready shutter estimate.**

## Decisive engineering experiment

A photodiode-attested LED waveform would permit an exposure integration model to be checked against measured row brightness. This test asks whether *given the model and a prespecified finite grid* the exposure duration, relative clock offset and rolling-shutter row delay are identifiable from coded illumination. It does **not** assume that video FPS equals physical shutter exposure time.

Frozen synthetic instrument: 40 nonperiodic quarter-ms LED pulses, 20 nominal 10-ms-spaced frames, three separated row ROIs per frame, 30 calibration observations and 30 held-out observations. The synthetic truth is clock offset 1 ms, exposure 2 ms, row delay 0.5 ms per ROI-row unit. A 36-candidate grid is fit using exact-rational duty-cycle integration and tolerance 0.02. The held-out half is not used to select candidates.

| Frozen adversary | Result | Decision |
| --- | --- | --- |
| Nonperiodic coded LED, correct model | Exactly **1/36** train-feasible; truth (1,2,0.5); 30/30 held-out residuals zero | `UNVERIFIED_PHYSICAL_INPUT` |
| Steady illumination (phase diversity removed) | **36/36** feasible | `AMBIGUOUS_GRID` |
| Force global shutter (`row_delay=0`) on rolling-shutter truth | **0** feasible | `MODEL_FALSIFIED` |
| Change one held-out normalized brightness to 0.1 | Frozen fit unchanged, held-out mismatch | `FALSIFIED_HELDOUT` |
| Omit one held-out row with explicit missingness | 29 valid held-out; missing count 1 | Still research-only |
| Assert every physical-evidence boolean without supplying authenticated measurements | Still no certification | `SYNTHETIC_GRID_FIT_ONLY` |

All 18 Python adversarial tests and independent Node.js BigInt quarter-ms integration replay passed **locally** before GitHub persistence. The dedicated [hosted workflow](../../.github/workflows/e002_532_optical_calibration.yml) must be checked separately; no hosted success is claimed in this document. The initial independent replay file contained a transcription error in the LED width array; it was corrected in a separate commit `5b867d2` before the hosted workflow was added. No hidden test or data outcome was overwritten.

## Scientific meaning and novelty limitation

The result is a **finite-model identifiability and falsification demonstration**, not a new law of shutter calibration. A known binary waveform can distinguish several shutter parameters under independently calibrated linear photometry, whereas constant illumination cannot. A global-shutter assumption can be contradicted by row-resolved optical data. The exact fit is conditional on the frozen finite candidate grid; values between grid points, temporal drift, unmodelled readout, photodiode uncertainty, rolling shutter geometry, gamma, saturation, gain drift and codec changes remain unbounded.

**Priority audit:** LED-based rolling-shutter timing calibration is established prior art, not a Lucent invention. See Huai et al., *Optics Letters* 48, 847–850 (2023), [DOI 10.1364/OL.474375](https://doi.org/10.1364/OL.474375), which demonstrates rolling-shutter line-delay calibration with a blinking LED panel on real cameras; and Kurosawa et al., *Japanese Journal of Forensic Science and Technology* 29, 135–153 (2024), [DOI 10.3408/jafst.875](https://doi.org/10.3408/jafst.875), which describes dedicated LED-based measurements of exposure, interframe timing and scanning speed. E002-532 is an application-specific reproducible calibration **gate** for the E002-371 human study, not a priority claim over either method.

## Real physical measurement handoff

Run the executable locally, never on private participant video in public CI:

```bash
python research/observability/e002_532_optical_calibration.py --synthetic
python -m unittest discover -s research/observability -p 'test_e002_532_optical_calibration.py' -v
node research/observability/e002_532_independent_replay.cjs
python research/observability/e002_532_optical_calibration.py --input /secure/photodiode_camera_observations.json
```

Private input JSON: `version=E002-532-v1`, `evidence_tier=physical_input_unverified`, `pulses=[{start_ms,end_ms}]`, `frames=[{native_frame_id,t_ms,row,brightness,partition}]`, `grid={delta_ms:[...],exposure_ms:[...],row_delay_ms:[...]}`, `brightness_tolerance`, and `attestations` with explicit photodiode, linear-photometry, native-frame, rolling-geometry and camera-clock fields. Times and brightness may be rational strings; input must be measured, not constructed from the fitted model. Explicit missing rows may set `valid=false` and omit brightness. Keep native images, clock logs, identities and calibration files private. All self-asserted flags remain unauthenticated.

Physical experiment: borrow a hardware LED driver, independent photodiode/clock logger and high-speed + ordinary cameras; record actual LED optical transitions, native row ROI brightness, frame identities, exposure/scanline settings and independent dark/bright controls. Freeze train/held-out pulse phases, candidate grid, uncertainties and nuisances before inspecting held-out brightness. Repeat across camera restart, gaze/geometry, lighting, glasses and motion blur conditions as applicable; use a **separate** anatomical study to validate the closure predicate. An optical LED calibration does not validate eyelid speed, eyelid threshold or same-predicate cross-camera transport.

**Kill criterion:** if held-out optical observations are incompatible with the frozen grid, if phase locking makes multiple models feasible, or if independent timing/photometry is unavailable, do not use this method to support Lucent's hidden-closure exclusion claims. The exact continuous-time shutter uncertainty set requires independently bounded instrumentation and model misspecification, not just a single best grid point.

## Release consequence

The executable returns `ABSTAIN_UNCALIBRATED` and `BLOCKED` in **every** case, including a unique synthetic or self-attested physical fit. It never emits a no-hidden-closure certificate. Real shutter/clock calibration: **0**; independent blinded S01 anatomical reviews: **0**; certified human continuous-time speed ceilings: **0**; participant-disjoint physical predictions: **0**. Further synthetic parameter polishing is lower priority than an actual borrowed-equipment optical capture and two independent human reviewers.

Hush PR #45 untouched. No merge, force-push or deployment.
