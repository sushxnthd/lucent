# E002-515 | Real-instrument data path is executable; no physical observations yet

Date: 2026-10-29. Frozen protocol: [E002_515_FROZEN.md](E002_515_FROZEN.md). Executable: [e002_515_physical_replay.py](e002_515_physical_replay.py). Regression tests: [test_e002_515_physical_replay.py](test_e002_515_physical_replay.py). Hosted workflow: [e002_515_physical_replay.yml](../../.github/workflows/e002_515_physical_replay.yml).

## New evidence and scope

E002-514 established feasibility only under synthetic eight-channel LED integration and an idealized camera response. E002-515 implements the **real measured-input validation boundary**: independent photodiode/logic-analyzer waveform intervals, eight camera region intensities, and a separately obtained camera exposure-timing reference. The inverse solver never reads the exposure reference until its candidate sets are computed. No nominal FPS or affine camera clock enters the inverse. It searches all waveform-boundary windows with 8–12 ms exposure duration and retains all eight-channel residual-compatible candidates. A reference exposure outside every compatible candidate or an unsafe gap underbound is reported as failure, not silently repaired.

The physical measurement contract was frozen **before any real optical data were obtained**. This is a new executable instrument-validation artifact, **not** a new physiological result, new theorem, high-speed human experiment or independently authenticated camera timing. It does not replace the E002-507 independent human reviewers or establish a continuous-time human eyelid-speed maximum.

## Software verification

Twelve local Python tests passed. These cover an artificial optical consistency fixture, independently shifted exposure reference causing a predeclared coverage failure, empty candidate sets, duplicate frame IDs, missing photodiode time, nonfinite values, missing references, out-of-range truth, timing-envelope monotonicity, reference uncertainty, invalid residual bounds and no FPS dependency. A GitHub Actions workflow additionally exercises the actual three-CSV CLI intake with a deliberately artificial fixture and checks hard-blocked product status. **Hosted verification passed**: [GitHub Actions run 40791695887](https://github.com/sushxnthd/lucent/actions/runs/40791695887) completed successfully on commit cd2c4160, running the 12 adversarial Python controls and end-to-end three-CSV artificial-fixture CLI. This confirms reproducible software behavior, **not** instrument or human evidence.

## E002-515b: reference-uncertainty falsification and correction

During audit of the new evaluator, a substantive inference bug was found **before physical deployment**: the first implementation accepted an exposure candidate whenever its boundary lay *within* the reference timing uncertainty (an **existential** match). This can pass even though another exposure boundary allowed by the independent hardware reference lies outside the candidate's optical timing envelope. Such a result is insufficient for a worst-case observability guarantee.

The correction now demands a conservative **universal** coverage witness: for each independently measured start/end midpoint `a,b`, uncertainty `u`, and candidate `s,e`, require both `|s-a|+u <= timing_envelope_ms` and `|e-b|+u <= timing_envelope_ms`. If no single candidate covers both full reference uncertainty intervals, report `FAIL_REFERENCE_COVERAGE`. This is a sufficient, intentionally conservative criterion; a more general union-of-candidates coverage analysis could admit additional cases, but cannot be silently substituted after observing outcomes.

The frozen artificial fixture with `u=0` remains a software consistency check. A separate adversarial test with `u=0.5 ms`, exact nominal candidate boundaries, and a zero timing envelope must now fail coverage. All 12 tests passed locally after the correction. The **earlier hosted CI success at 40791695887 predates this correction** and must not be cited as verification of the final universal-coverage rule; postpatch CI must be checked separately. This directly changes which future physical measurements can be considered supported, and prevents an unjustified conditional clearance.



**Postpatch verification closure (2026-10-29):** [GitHub Actions run 40791909652](https://github.com/sushxnthd/lucent/actions/runs/40791909652) completed with `conclusion: success` on commit `d0151b734797b837fca79553c3ddc0c6264dc3f5`. This hosted result verifies the corrected reference-uncertainty software tests, not a physical measurement, authenticated clock, or eyelid-speed bound. The earlier warning is preserved as a historical record of the verification state at initial report creation.

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


## E002-518 addendum: native sequence is an additional measurement input

The original E002-515 three-CSV intake did **not** identify which exported rows were consecutive native camera frames, although it labeled every successive camera-row pair as an `evaluated_adjacent_gaps` test. [E002-518](E002_518_RESULT.md) freezes and corrects this sampling-provenance error. Without an independently auditable native-frame index ledger, the updated evaluator reports `INSUFFICIENT_NATIVE_SEQUENCE_PROVENANCE`, evaluates **zero** claimed native-adjacent gaps and retains per-exposure reference coverage diagnostics only. A separate optional `--sequence` CSV with `frame_id,native_index` enables conditional consecutive-index diagnostics but cannot authenticate its own capture provenance. Such a replay is `REPLAY_CONSISTENT_SEQUENCE_UNATTESTED`, never a physical certificate. The old workflow's successful three-CSV result is historical software evidence and is **not** sufficient under this stronger gate.

No physical data, human labels or hard eyelid-velocity ceiling were added. Product and release remain blocked.
