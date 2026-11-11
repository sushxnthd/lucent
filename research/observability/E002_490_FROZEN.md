# E002-490 | Independent optical-clock codec replay and CI dependency repair

Date: 2026-10-27. Primary E002-371 measurement kernel. **Frozen before hosted replay, after an explicitly exploratory local independent implementation.** This is not a new physical acquisition or a preregistered human study.

## Reason to run

At [E002-439 GitHub Actions run 40544611566](https://github.com/sushxnthd/lucent/actions/runs/40544611566), 12 Python tests passed and one FFmpeg-dependent test was skipped, but the full virtual optical-clock experiment failed because the runner had **neither ffmpeg nor ffprobe**. The preceding dependency-check step falsely appeared green because its shell pipeline lacked `pipefail`. This leaves the original E002-439 optical/PTS experiment without hosted verification on the current head.

## Frozen independent replay

Implement a standalone standard-library Python replay with **no imports from E002-439**. Encode 12 synthetic optical frames carrying binary 16-bit ticks `[0,33,67,100,200,233,267,300,400,433,467,500]`, plus independent checkerboard reference cells. Use real FFmpeg FFV1 encode/decode, then re-encode with 2x presentation timestamps. The optical pixels and recovered ticks should be unchanged while final container PTS changes from 500 ms to 1000 ms. This is an instrument **container-clock spoofing control**, not a physical camera timing experiment.

Prespecified hosted acceptance: all 12 optical ticks recovered; all 12 decoded frames byte-identical after retime; last source/retimed PTS 500/1000 ms (±1 ms); independent E002-439 adversarial suite including its real FFmpeg test executes without skips; original experiment returns `ABSTAIN_UNCALIBRATED`. Any dependency installation, codec or numerical failure remains a failed run and must not be reported as a scientific pass.

## Toolchain repair and evidence boundary

Install ffmpeg/ffprobe explicitly on GitHub Actions before the test. Check both binaries with `command -v` under `set -euo pipefail`, not a misleading version-print pipeline. Use the original persistent research branch and draft PR #26. Do not change the optical bound, human study, or production authorization.

The exploratory local independent replay on a Debian FFmpeg 7.1.5 environment produced identical decoded frames and 500/1000-ms PTS; this motivated the frozen hosted verification but is **not** independent physical evidence. No anatomical human reference, calibrated shutter, physiological hard velocity bound, or unseen-condition human test is provided. E002-371 remains unvalidated. Product claims remain `ABSTAIN_UNCALIBRATED`; release blocked.
