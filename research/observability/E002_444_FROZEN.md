# E002-444 — frozen human-frame optical activity versus sparse-event gaps (2026-10-25)

Parent E002-371, E002-441–443. Frozen before decoding S19 video beyond the two-frame probe or examining any S19 optical-motion sequence. S19 only; S21/S22 remain untouched.

## Question and independently fixed analysis
The S19 AVI declares 56,911 320x288 MPEG-4 frames, but a 1-fps container timebase; 56,911 sparse RelTime event rows span 409.941 s with a 7-ms median interval. Does the *image content* provide independent evidence of nonduplicate temporal sampling, and is the proposed one-to-one frame/event ordering plausible at large candidate event gaps? No camera-exposure provenance or anatomical scale is inferred.

Decode **the first 12,000 frames** (or all if fewer) to grayscale via FFmpeg, in native file order, with no image export. Pair frame i with sparse event i only as an **unverified hypothesis**. For every adjacent pair, compute:
- exact byte equality;
- mean absolute 8-bit pixel difference /255 (full 320x288 image);
- fraction of pixels with absolute change >=16/255;
- change quantiles p01,p50,p90,p99, and largest change;
- event-gap bins <=10 ms, 10–100 ms, >100 ms; per-bin counts and median/p90 optical change;
- fraction of large-gap transitions exceeding the **median** <=10-ms change; this is descriptive, not a statistical proof of alignment.
- a deterministic shift-control: compare gaps to optical changes shifted cyclically by 137 frames and report both gap-bin medians. A shift control can detect some spurious association but is not a valid alignment oracle.

The image region is fixed to the **entire frame**, avoiding post-hoc ROI selection. All thresholds fixed before data access. Do not assert that pixel difference is anatomical aperture, eyelid velocity, blink or calibrated time. Even a high association cannot authenticate sensor exposures. Explicitly report missing/extra decoded frames, decode errors, and lack of a verified row/frame map. If candidate event count differs from video frame count, refuse paired analysis. Never read S21/S22.

## Falsification and decisions
If >5% adjacent decoded frames are exactly identical, flag possible redundancy for investigation, not proof of acquisition duplicates. If median pixel change is zero, reject the assumption that every index is an independently informative optical observation. If >100-ms gaps show no stronger optical change than <=10-ms gaps, record lack of positive evidence for the one-to-one event-gap interpretation, without claiming a formal falsification (scene motion need not scale with time). If there are too few long gaps in the fixed first 12,000 frames, report INSUFFICIENT_LONG_GAPS rather than extend the window after seeing results.

## Required controls
Synthetic codec fixture: changing frames, identical frames, deliberately injected >100-ms gap, and cyclic-shift control. Fail closed on malformed frames, invalid gaps, mismatched frame/event counts, missing FFmpeg, checksum failure, and nonfinite results. Use SHA-verified S19 archive, no raw human imagery in outputs, and retain participant-level privacy.

## Evidence and release boundary
Only real-human *video optical-change aggregates* can be claimed. No physical aperture, independent clock/shutter/geometry calibration, human reference closure labels, or hard physiological velocity bound. E002-371 physical validation remains NOT ESTABLISHED. Product must remain ABSTAIN_UNCALIBRATED for no-hidden-closure, blink duration, PERCLOS and fatigue. Do not merge PR #26.
