# E002-487 | Frozen first-human-video acquisition and timing audit

Frozen 2026-10-27 **before any S24 video bytes were obtained or inspected**. Primary E002-371; existing branch `research/observability-human-boundary`, draft PR #26. This is a **single-subject acquisition feasibility pilot**, NOT the predeclared 20/11 participant-disjoint validation and NOT a new anatomical claim.

## Decisive question
Can a no-cost GitHub-hosted runner retrieve one authentic 2025 Guttmann-Flury human-eye-video archive, verify provenance, and measure its *actual* frame timestamp cadence? Prior local/container download attempts failed due to unavailable DNS. This is a move from synthetic camera models to an authentic video acquisition, not a new theorem.

## Prespecified acquisition
- Source: https://zenodo.org/records/18970793, public CC0 re-host dated 2026-03-12; underlying study https://doi.org/10.1038/s41597-025-04861-9 (2025-04-08).
- Fixed subject S24, `S24.zip` (smallest selected archive), Zenodo-published MD5 `3e8eb615d4a3415115f61dad5265ef12`, advertised compressed size 345.6 MB. Do not substitute another subject or URL post-hoc.
- Download with a hard 600-MB transfer limit and finite timeout; validate MD5 before parsing; reject unsafe ZIP member paths, symlinks, and oversized video extraction. Never commit/upload any raw video, image, XML, face crop, or participant-level annotations.
- Select the lexicographically first `*_phantom.avi` member, explicitly reporting this selection. Require FFprobe stream metadata and enumerate packet PTS where available. Report nominal `r_frame_rate`, `avg_frame_rate`, timebase, frame count, measured positive PTS deltas, monotonicity, large gaps, and fraction of nonpositive steps. Audit first 10,000 packet timestamps at most. Do not infer exposure time from frame rate.
- Paper reports 150 fps while re-host text says ~500 fps. If the actual video is not within 2% of 150 fps, report a **source-rate conflict**; do not silently resample or force 150. If PTS are absent/unusable, mark temporal validation `ABSTAIN_NO_AUTHENTICATED_PTS` even if header declares a rate.
- No automatic pupil/eyelid annotations or closure events are claimed. Metadata-only evidence is a first acquisition milestone, not human E002-371 validation. Positive anatomical witnesses require independently reviewed annotations, calibrated exposure, and a separately fixed threshold.

## Fail / pass criteria
PASS for the **acquisition feasibility pilot** only if archive checksum, safe extraction, video codec read, and positive monotonic PTS succeed. Any failure is preserved as a named negative result, not replaced by synthetic data. A 150-vs-500 discrepancy is a reported scientific result, not a reason to falsify or discard data. Successful acquisition does not authorize any blink-duration, PERCLOS, fatigue, or medical output.

## Reproduction and privacy
Run `python research/observability/e002_487_human_video_intake.py --archive /restricted/S24.zip --output /tmp/e002_487_result.json`. The no-cost CI workflow `.github/workflows/e002-487-human-video.yml` runs once when these exact files are first committed, then only when explicitly updated; upload **aggregate JSON only**. Product state `ABSTAIN_UNCALIBRATED`, release `BLOCKED` regardless of outcome. No change to existing Hush branch/PR.
