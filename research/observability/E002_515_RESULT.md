# E002-515 | Real-instrument data path is executable; no physical observations yet

Date: 2026-10-29. Frozen protocol: [E002_515_FROZEN.md](E002_515_FROZEN.md). Executable: [e002_515_physical_replay.py](e002_515_physical_replay.py). Regression tests: [test_e002_515_physical_replay.py](test_e002_515_physical_replay.py). Hosted workflow: [e002_515_physical_replay.yml](../../.github/workflows/e002_515_physical_replay.yml).

## New evidence and scope

E002-514 established feasibility only under synthetic eight-channel LED integration and an idealized camera response. E002-515 implements the **real measured-input validation boundary**: independent photodiode/logic-analyzer waveform intervals, eight camera region intensities, and a separately obtained camera exposure-timing reference. The inverse solver never reads the exposure reference until its candidate sets are computed. No nominal FPS or affine camera clock enters the inverse. It searches all waveform-boundary windows with 8–12 ms exposure duration and retains all eight-channel residual-compatible candidates. A reference exposure outside every compatible candidate or an unsafe gap underbound is reported as failure, not silently repaired.

The physical measurement contract was frozen **before any real optical data were obtained**. This is a new executable instrument-validation artifact, **not** a new physiological result, new theorem, high-speed human experiment or independently authenticated camera timing. It does not replace the E002-507 independent human reviewers or establish a continuous-time human eyelid-speed maximum.

## Software verification

Twelve local Python tests passed. These cover an artificial optical consistency fixture, independently shifted exposure reference causing a predeclared coverage failure, empty candidate sets, duplicate frame IDs, missing photodiode time, nonfinite values, missing references, out-of-range truth, timing-envelope monotonicity, reference uncertainty, invalid residual bounds and no FPS dependency. A GitHub Actions workflow additionally exercises the actual three-CSV CLI intake with a deliberately artificial fixture and checks hard-blocked product status. **Hosted success is pending verification**; the tests do not constitute instrument or human evidence.

## How to obtain the decisive physical result

1. Physically drive eight spatially separated LED regions with an external hardware clock and record **measured emitted light** with independent photodiodes/logic analyzer. Record the measured waveform, not merely the commanded LED sequence.
2. Acquire raw linear camera regions with locked gain, exposure, white balance and native-frame continuity. Independently characterize saturation, spatial cross-talk, blur, ambient light, rolling-shutter row delay and clock phase.
3. Measure exposure start/end on a **separate hardware reference channel** (e.g., calibrated exposure-sync output with independently established alignment to actual integration). Do not derive truth from the same camera image intensities being tested.
4. Freeze radiometric residual and timing uncertainty from independent calibration data, then capture **unseen** device/lighting/clock/gaze/occlusion conditions. Export the three private CSVs and run the offline evaluator. On any coverage miss or unsafe gap underbound, falsify the chosen physical envelope. On an apparently consistent replay, request independent instrument review and replication before any physical claim.
5. Separately obtain two genuine blinded S01 anatomical ratings and positive iris-diameter uncertainty for the existing E002-507 fixed 20-window protocol. Only then consider participant-disjoint E002-371 prediction against high-rate physical reference.

**CLI** (run only on an authorized machine with local instrument files):

```bash
python research/observability/e002_515_physical_replay.py \
  --photodiode /secure/photodiode.csv \
  --camera /secure/camera.csv \
  --reference /secure/reference.csv \
  --residual-max PRECALIBRATED_VALUE \
  --timing-envelope-ms PRECALIBRATED_VALUE
```

Do not upload identifiable camera imagery, human annotations, raw reviewer data or owner-only frame mappings to GitHub. The CSV replay itself cannot prove hardware identity, timing independence, model correctness or human anatomy. No instrument truth, human labels, hard velocity ceiling or held-out physical predictions were obtained during this run.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. No claim that Lucent is production-ready. The separate Hush branch/PR is untouched.
