# E002-487 | First authentic human-video acquisition pipeline, pending hosted execution

**2026-10-27. Primary kernel E002-371. Evidence at commit time: synthetic software controls only; actual S24 video not yet acquired.** Existing branch `research/observability-human-boundary`, draft PR #26. No human anatomical trajectories have been annotated and no physical shutter measurement has been acquired.

## Why this experiment differs from E002-477–486

Previous runs sharpened synthetic observability counterexamples but could not validate them on actual human measurements. E002-487 establishes a concrete, no-cost acquisition route in a GitHub-hosted runner, which has network access independent of the local DNS-restricted container. The prespecified target is the genuine S24 human-eye-video archive, not a newly generated simulator.

The primary [2025 *Scientific Data* paper](https://doi.org/10.1038/s41597-025-04861-9) describes 150-fps Phantom video. The [2026-03-12 Zenodo re-host](https://zenodo.org/records/18970793) describes the same Phantom AVI files as ~500 fps. This disagreement is unresolved. The published S24.zip MD5 is `3e8eb615d4a3415115f61dad5265ef12`, size ~345.6 MB. We must inspect actual AVI stream rates and timestamps rather than pick the favorable figure.

## Executed and verified locally

- Froze [S24-only acquisition and pass/fail criteria](E002_487_FROZEN.md) before inspecting any S24 video.
- Created [metadata-only ZIP and FFprobe intake](e002_487_human_video_intake.py), which checks published checksum, archive safety, selected video stream, timestamp monotonicity, nominal versus empirical container cadence, and source-rate conflict. No human video/image content is exported.
- **10/10 local adversarial tests passed** using locally generated 150- and 500-fps MJPEG AVI fixtures. Tests cover checksum failure, path traversal, symlink, corrupt/missing video, timestamp duplication, 500-fps rate conflict, and oversized video. This is **software evidence**, not a human experiment.
- The initial synthetic AVI timestamp test exposed an FFprobe argument-order bug and an AVI packet-timestamp fallback issue. These failures were recorded in [Amendment A](E002_487_AMENDMENT_A.md) and repaired. A decoder-derived frame timestamp is explicitly lower-tier than packet PTS, and neither authenticates the hardware clock.
- Added a **one-shot** [GitHub Actions acquisition job](../../.github/workflows/e002-487-human-video.yml), triggered only by the workflow file's own push path (or manual dispatch), with 20-minute job limit, 600-MB download cap, fixed S24 checksum, and aggregate JSON artifact only.

## Pending decisive evidence

[Hosted acquisition run 40514211441](https://github.com/sushxnthd/lucent/actions/runs/40514211441) was **queued** when this report was written. No download success, actual camera rate, timestamp statistics, or real anatomical result can be claimed yet. If the run fails, preserve its failure artifact and diagnose that specific obstacle before doing more synthetic science.

Even if it succeeds, **verified S24 AVI metadata is not independently authenticated exposure timing**. It also does not supply eyelid-aperture annotations. The next gate is independent high-rate aperture annotation and reviewer disagreement quantification on a **calibration participant**, not S24. S24 is reserved for metadata-only intake and must not be used for model/threshold selection. If S24 anatomical frames are ever viewed for development, S24 must be removed from the frozen held-out set and a new split declared **before** any held-out outcome analysis; the original 20/11 test would no longer be intact. Physical shutter/moving-aperture controls remain mandatory.

## Product decision

`ABSTAIN_UNCALIBRATED` for hidden closure, blink duration, PERCLOS, fatigue and medical measurements. `BLOCKED` for product release. This work validates a possible acquisition pathway, **not** E002-371's physical law.

No Hush branch/PR changes, merges, force-pushes or deployments.

## Split-integrity correction

The original E002-485 frozen split assigns S24 to the held-out subjects S21–S31. S24 was chosen for this **metadata-only** feasibility pilot because its archive is the smallest. Its anatomy must remain blinded to retain the original 20/11 split. A future annotation pilot must use S01–S20 instead. This correction was made before any S24 video was downloaded or viewed in this run.
