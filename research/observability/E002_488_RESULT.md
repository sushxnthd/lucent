# E002-488 | Repair the human-data bottleneck without relying on FFmpeg provisioning

**2026-10-27. Primary E002-371 track.** The prior E002-487 hosted replacement run remained in its `apt-get` setup step at inspection, preventing authentic human-video acquisition. Its final outcome was not yet available when this experiment was frozen.

## New reproducible instrument/data work

Implemented a standard-library RIFF/AVI header parser that reads both `avih` and the first video `strh` rate declarations, checks their consistency and distinguishes nominal values from independently authenticated camera timing. ZIP MD5, traversal protection, video size limits and metadata-only handling are retained.

Six dependency-free synthetic regression tests passed locally, including 150/500-fps header controls, invalid rate, checksum mismatch and path traversal. Additionally, the parser was checked locally against FFmpeg-generated synthetic AVI fixtures at both 150 and 500 fps. These are **software tests only**, not human anatomical measurements.

A new one-shot GitHub Actions workflow runs the controls and attempts to download the published 345.6-MB S24 archive without `apt-get`, `pip`, `ffmpeg` or `ffprobe`. The frozen protocol is [E002_488_FROZEN.md](E002_488_FROZEN.md). The workflow emits only a bounded JSON header report. Actual acquisition success, source rate and authentic data evidence are **pending hosted execution**.

## Scientific and product consequence

Even a successful checksum-verified AVI header result cannot establish real acquisition cadence or reference-camera exposure gaps. An independent hardware clock or trusted acquisition timing provenance is required before the E002-371 velocity-bound exclusion can be tested against human anatomy. An AVI header mismatch is an explicit temporal abstention, not an invitation to select a favorable rate.

S24 remains anatomically blinded as a held-out participant. Next decisive experiment: acquire a calibration participant S01–S20, annotate eyelid aperture with independent review and uncertainty, and compare held-out gap predictions under measured timing, blur and gaze controls. No physical shutter acquisitions or anatomical reference trajectories were obtained in this local work. `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
