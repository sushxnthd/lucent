# E002-487 Amendment A | AVI timestamp fallback after synthetic fixture failure

2026-10-27. The frozen protocol [E002_487_FROZEN.md](E002_487_FROZEN.md) was committed at `a09d17c2f69b00ebbc38dafe1ae5243da00c4641` before implementation. A locally generated 150-fps MJPEG AVI revealed that FFprobe **packet timestamps can be unavailable even for a decodable video**; the initial parser also exposed an FFprobe argument-order bug. Neither issue was found in human data. Both failed local checks are preserved here instead of retroactively rewriting the frozen protocol.

**Amended operational rule:** If container packet PTS are unavailable or unusable, inspect FFprobe `frame.best_effort_timestamp_time` as a lower-tier, decoder-derived fallback. Record `timing_source` explicitly. Monotonic container or decoder timestamps can pass only the **archive/video metadata acquisition feasibility** gate; they never authenticate camera capture clock, physical shutter/exposure, or anatomical nonclosure. Missing/unusable timestamps from both sources still require abstention. A 150-vs-500-fps rate conflict must be reported, not corrected.

Local 150-fps synthetic MJPEG AVI with 30 frames now passes container packet-PTS cadence (median delta ~6.667 ms). A separate synthetic 500-fps control is correctly marked as a source-rate conflict. This is software-fixture evidence only. The no-cost GitHub runner's real S24 archive download has **not yet run** as of this amendment.

No human anatomical sequences annotated; no physical shutter acquisitions. `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
