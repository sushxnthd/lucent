# E002-491 | Calibration human-video image-content screening (execution handoff)

**2026-10-27. E002-371 primary workstream. Evidence tier: implemented and launched, authentic S01 frames not yet measured.**

## Repaired independent instrument verification

The prior E002-490 [hosted run 40551660760](https://github.com/sushxnthd/lucent/actions/runs/40551660760) failed **one of thirteen** tests with `source PTS mismatch` under Ubuntu FFmpeg 6.1.1. FFmpeg provisioning itself succeeded. The difference arose in source presentation timestamps, so the experiment did not justify its prior anticipated hosted success.

Pinned the FFV1 encoder timebase to `1:1000` in both the E002-439 implementation and the independent E002-490 replay, retaining strict 1-ms timestamp assertions and reporting observed values on failure. The [replacement hosted run 40563383285](https://github.com/sushxnthd/lucent/actions/runs/40563383285) **completed successfully** on commit `7763be6321e10a467cf146a4e6f3dce4eaab95e4`: all thirteen adversarial tests, machine-readable hard-abstention assertions and independent FFV1 replay passed. This verifies a **synthetic image-encoded optical-clock instrument**, not an actual sensor shutter or anatomical event.

## New human content experiment

Precommitted [E002_491_FROZEN.md](E002_491_FROZEN.md) before processing S01 images. Unlike prior S24 header-only experiments, this run now attempts actual decoded video image-content screening on the **calibration participant S01** from the public Zenodo archive. Source https://zenodo.org/records/18970793, published 2026-03-12, published MD5 `fb56109542a13aa7879778833fe4cbaa`.

Implemented [e002_491_calibration_motion.py](e002_491_calibration_motion.py) and ten nuisance tests. The screen uses bounded 64x64 grayscale frames, framewise brightness subtraction, central-vs-border change, duplicate-frame rejection and contrast/brightness gates. It reports only aggregate metrics and at most twenty candidate **frame indices**. It never produces anatomical closure labels or frame times.

[Hosted S01 acquisition run 40563647913](https://github.com/sushxnthd/lucent/actions/runs/40563647913) was queued at initial check. The new experiment's synthetic tests and authentic human content results are **not yet hosted-verified** in this report. The older S24 archive was checksum-verified previously, but S24 is held out and is not used for calibration. No raw human imagery is uploaded to GitHub.

## Interpretive limits and decisive next step

Even a successful localized-motion candidate is **not** an eyelid closure. Eye gaze, iris/pupil translation, lighting, glasses, head motion and blur can generate or suppress the proxy. Frame indices are not authenticated milliseconds; 1-fps AVI headers are not camera-clock evidence. If the nuisance-confounded fraction exceeds 20%, reject this screening proxy as unstable. If no candidates appear, preserve the negative result.

After S01 succeeds, create a restricted manual annotation packet for independent eyelid-aperture raters on calibration subjects, obtain source camera timing and exposure calibration, freeze velocity assumptions, and then conduct participant-disjoint S21-S31 falsification. No claim of observed anatomical closure or physical E002-371 validation is warranted.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. **Physical shutter acquisitions:** 0. **New verified anatomical closure labels:** 0.
