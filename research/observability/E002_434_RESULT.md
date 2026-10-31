# E002-434 — real encoded-media timing falsification and fail-closed instrument correction

**Date:** 2026-10-25. **Parent kernel:** E002-371 shutter-gap/eyelid-velocity observability. **Evidence tier:** executable **FFmpeg/FFprobe codec/instrument experiment on synthetic frames**, not human eyelid evidence, physical camera timing or a new mathematical theorem. The protocol was frozen first at commit `aa80586b`.

## Decisive result

An encoded variable-frame-rate (VFR) video can carry **25 fps** in its reported average-rate metadata while its decoded frame presentation timestamps contain 200-ms and 120-ms gaps. Replacing actual encoded presentation times by `frame_index / 25` gives a **maximum 240-ms timestamp error** on this 13-frame FFV1/Matroska fixture. The constant-frame-rate control, encoded using the same codec, has **zero nominal-timestamp error**.

This is a **real encoder/decoder instrument test** with deliberately authored synthetic image frames. It is not a claim that a physical camera dropped frames: a long presentation interval can arise from acquisition, encoding, editing, timestamp synthesis or transcoding. The experiment establishes that the frame-rate shortcut is insufficient for even *container-time* provenance.

| Frozen metric | VFR intervention | CFR negative control |
| --- | ---: | ---: |
| Encoded frames | 13 | 13 |
| Reported average frame rate | 25 fps | 25 fps |
| Maximum presentation interval | **200 ms** | 40 ms |
| Additional long interval | **120 ms** | None |
| Maximum error of `index / fps` vs encoded PTS | **240 ms** | **0 ms** |
| Maximum encoded PTS vs authored schedule error | < 10^-12 s | < 10^-12 s |
| Human/physical sensor validation | **None** | **None** |

Both the preregistered >50-ms VFR discrepancy and <=10-ms CFR control passed. Authored durations were `[.04,.04,.04,.20,.04,.04,.12,.04,.04,.04,.04,.04]` seconds; a final duplicated image ensures the final duration is represented. The independent frame-level FFprobe parser uses `best_effort_timestamp_time` and rejects nonmonotone, duplicate, absent, nonfinite and negative timestamps. Source code and machine-readable [aggregate](E002_434_INSTRUMENT_AGGREGATE.json) preserve the exact intervention and results.

## Actual Lucent instrument consequence

The existing `instrument/analyze_capture.py` previously exposed `timeS = frame_index / reported_fps` without identifying that this was a **nominal decoder-rate estimate**, not a sensor timestamp. The quality-only pipeline now marks that provenance explicitly and adds an **opt-in** `--container-pts` mode that reads validated frame-level container presentation times from the new FFprobe instrument. The code rejects disagreement between decoded frame count and probed timestamp count. A 3-frame-stride integration test preserves original frame indices rather than compressing gaps.

**Neither mode authenticates physical exposure-start/end timestamps.** The output explicitly marks `hardwareExposureTimestampsAuthenticated: false`, `physicalCertificateAuthorized: false`, and `product: ABSTAIN_UNCALIBRATED`. Existing nominal-time users retain backward compatibility with explicit warnings; physical measurement clients must not treat either `timeS` mode as sensor time. This change supports **capture-quality diagnostics**, not eyelid-closure, blink-duration, PERCLOS or fatigue measurements.

## Reproducibility and adversarial verification

Run from the repository root with free FFmpeg/FFprobe, Python 3.11, and (for integration) `numpy` plus `opencv-python-headless`:

```sh
python instrument/verify_frame_timing.py --experiment --output /tmp/e002_434.json
PYTHONPATH=instrument python -m unittest -v research/observability/test_e002_434_container_pts.py
PYTHONPATH=instrument python -m unittest -v research/observability/test_e002_434_instrument_integration.py
python instrument/analyze_capture.py input.mkv input.json --container-pts --output quality.json
```

Six parser/codec test groups **passed locally** on FFmpeg/FFprobe 7.1.5; they include malformed-input rejection, strict PTS ordering, VFR/CFR controls and unconditional abstention. Two additional integration test groups exercise the real OpenCV quality pipeline on the generated VFR video. The dedicated GitHub Actions workflow runs both groups; report its hosted status independently rather than assuming success from the commit.

## Interpretation, priority and falsifiability

This is an established media-timebase failure mode demonstrated for Lucent, **not a new theory of temporal sampling or physical camera metrology**. E002-432 had shown a synthetic missingness alias; E002-434 adds a real encoded-media intervention and a directly tested instrument behavior. Container PTS itself is **not independently authenticated**: remuxing or transcoding can change it, and it does not reveal shutter integration, rolling rows, clock synchronization or sensor frame loss.

An independent acquisition system could falsify a proposed physical-time interpretation by recording hardware exposure pulses and sensor timestamps simultaneously with the encoded stream. Freeze the raw capture hash, physical timing and shutter calibration, then test held-out capture conditions; do not infer them from `ffprobe`. The [E002-433 human-study handoff](E002_433_HUMAN_HANDOFF.md) remains the prospective protocol for participant-disjoint, two-rater, physically registered eyelid validation.

**E002-371 remains physically unvalidated.** No new human sequence, anatomical measurement, physiological hard velocity bound or independently authenticated camera exposure trace was obtained. Product no-hidden-closure certification, blink duration, PERCLOS and fatigue must remain `ABSTAIN_UNCALIBRATED`.
