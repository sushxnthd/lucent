# E002-392A — real human recording falsifies AVI metadata as timing evidence (2026-10-23)

**Evidence tier: actual public human high-speed eye video, instrument/timing audit only; no blink/aperture ground truth.**

## Frozen protocol and source
Frozen at commit `9c068d9` before acquisition. Public CC0 human video from Guttmann-Flury, Sheng and Zhu, *Scientific Data* 12:587 (2025), DOI 10.1038/s41597-025-04861-9, independently mirrored as Zenodo 18978288. Downloaded `S01.zip` and verified MD5 `fef02cb7ebf62e4f3efb6303284fd6cb`. Extracted `Sess01/SSVEP011_phantom.avi` and decoded actual human eye imagery.

## First-run findings and failed prediction
- **Actual AVI metadata:** `r_frame_rate=1/1`, `avg_frame_rate=1/1`, `time_base=1/1`, 53,680 frames, codec MPEG-4, 320×288, apparent container duration **53,680 seconds**.
- **Primary publication:** actual acquisition is reported as **150 fps** with 6.6-ms hardware triggers; the mirror's prose describes `~500 fps`. Neither 150 nor 500 is encoded as AVI fps.
- **Frozen prediction that ffprobe would return approximately 150 fps: FAILED.**
- Direct visual inspection of contact-sheet time overlays shows adjacent frame identifiers and acquisition-clock timestamps differing by approximately **6–7 ms**, qualitatively consistent with 150-fps capture and inconsistent with one second per physical frame. This is not yet a machine-audited clock trace.
- The first-pass ROI-motion CSV and image time labels used the AVI's false 1-fps time base, so their **time labels and 8-second segment claims are invalid**. Do not use them for kinematics or detection rates. The raw eye imagery itself is real, and the source hash is verified.

## Scientific/product consequence
**A human high-speed AVI can encode a nominal 1-fps time base despite being acquired at ~150 fps.** Nominal video container FPS is not sufficient to calibrate actual acquisition intervals. A validator must reconcile camera acquisition clocks, source-paper metadata, sidecar sync and video timing; otherwise it must abstain. The result is a real-data instrument failure, not evidence for or against E002-371's human eyelid observability theorem.

## Repair protocol
Freeze this negative result. Next instrument revision must extract and inspect same-session `*_sync.csv` and `*_phantom.xml`, preserve both metadata and source-paper frame-rate claims, derive *exploratory* frame-index time from the independently published 150-Hz acquisition claim, and never silently promote that claim into a measured exposure time. Recompute three disjoint 8-second **nominal** segments from frame indices; retain `ABSTAIN_UNCALIBRATED`. External camera shutter/clock validation and held-out human recordings are still missing.

## Reproduction
GitHub Actions run: https://github.com/sushxnthd/lucent/actions/runs/39953333788 . Small downloadable CI artifact: `e002-392-human-feasibility` (result JSON, ROI CSV, contact sheet). Raw human video intentionally excluded from the artifact. Source MD5 verified and workflow passed; passing CI does **not** mean the frozen 150-fps metadata prediction passed.
