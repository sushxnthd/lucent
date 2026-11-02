# E002-607 | Coded-LED optical shutter identification: instrument-ready, physical evidence absent

Date: 2026-11-02. Parent E002-371. Evidence tier: **SYNTHETIC OPTICAL INSTRUMENT MODEL ONLY**. [Protocol frozen before execution](E002_607_FROZEN.md) in commit `cd8f265`.

## New experimental result
A deterministic externally specified 120-ms binary LED waveform, three sensor rows, five hypothetical frame times, and a 315-element shutter timing candidate space were tested by an exact rational inverse model. The true synthetic timing was (start offset **3 ms**, exposure **4 ms**, selected-row delay **2 ms**). Fitting only the first three frames (nine row measurements) at +/-0.01 normalized linear-light error identified **1/315** candidates, the true tuple; all six untouched held-out row samples agreed. A separately written Node.js enumerator reproduced the unique tuple without importing the Python code.

The negative control is decisive for instrument design: a constant LED yields **315/315** indistinguishable shutter candidates, despite perfect noiseless measurements. Deleting one informative row sample expands the identified set from **1 to 2**. Widening the intensity tolerance to +/-0.10 did not shrink the set (still 1 on this fixture). A declared but unauthenticated radiometric/clock input must never be treated as verified by the script.

| Frozen check | Local outcome |
|---|---:|
| Candidate timing grid | 315 |
| Coded LED, nine training row intensities | 1 surviving |
| Six held-out row intensities | All consistent |
| Constant LED, nine training intensities | 315 surviving |
| One training sample missing | 2 surviving |
| Unknown linear-light response certificate | ABSTAIN |
| Duplicated sample or malformed private input | Reject |
| Independent Node inverse | PASS |

The `--self-test` command was run locally and returned `strict_candidates=1`, `constant_led_candidates=315`, `dropped_sample_candidates=2`, `private_fixture_status=GRID_IDENTIFIED_CONDITIONAL_ONLY`. The independent `node e002_607_independent.cjs` run also passed. [Dedicated hosted workflow](../../.github/workflows/e002_607_optical_identification.yml) committed; **hosted result not yet checked**.

## Why this changes the next physical experiment
An optical timing instrument must use a **time-coded** light source and multiple sensor rows; a static illumination target is incapable of identifying the shutter parameters, even with zero image noise. The tool reports the entire surviving timing set, rather than assuming a single shutter or rolling-row parameter. This is a synthetic identifiability test, not a new theorem, actual camera calibration, or human eyelid result.

### Concrete operator-run physical handoff
1. Use an already available phone/camera with fixed manual exposure, gain, focus, white balance and frame cadence. Obtain a borrowed, independently timed LED driver and photodiode or an equivalent traceable optical timing reference. Record the optical trace and clock-sync witness, not merely requested LED pulses.
2. Image a diffuse LED patch at three widely separated **sensor rows**, not three eye-image columns. Use a calibration sequence of varied pulse widths and coded timing; independently determine black level, sensor response linearization, saturation, readout orientation and uncertainty. Repeat across exposure and lighting conditions. Do not use gamma-compressed JPEG intensities as linear-light values.
3. Retain the *actual measured* pulse trace and raw row-intensity values in encrypted private custody. Construct the local JSON input schema from the `evaluate_private` parser, with 120 measured 1-ms LED bins and 15 row-intensity samples at frame-start labels 0/20/40/60/80 ms. The integer-ms grid is an initial bench **demonstration**, not a claim of sufficient physical resolution; adapt the grid only in a separately frozen physical protocol.
4. Run `python research/observability/e002_607_optical_identification.py --private-input private_calibration.json` offline. Require the fit/held-out split and all attestations. Treat a unique finite-grid result as **conditional**: software flags cannot verify an external clock, optical transfer function or the correctness of the model. Account separately for clock alignment, dropped frames, LED jitter, row selection and uncertainty between grid points.
5. Only after externally reviewed physical shutter calibration, conduct consented human capture under [E002-598's protocol](E002_598_HUMAN_STUDY.md). Two blinded raters must adjudicate high-rate eyelid anatomy. An independent continuous-time velocity ceiling is still needed for a hard E002-371 exclusion; measured sampled maximum speed is not such a ceiling.

## Hard limitations
- **Zero actual camera captures**, zero photodiode traces, zero new human anatomical ratings, zero certified continuous-time physiological velocity bounds, zero held-out physical predictions.
- Binary LED waveform, perfectly known 1-ms clock, exact boxcar exposure, affine rolling row delay, noiseless synthetic response, and a finite timing grid are stipulated, not observed. Saturation, gamma, flicker, blur, sensor nonlinearities and phase drift can defeat the model. No physical or human claim follows.
- This is **instrument preparation**, not independent empirical validation of E002-371. Do not spend another run polishing this synthetic model; acquire physical optical measurements or independent human review next.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. Hush's separate branch and PR #45 were not modified.
