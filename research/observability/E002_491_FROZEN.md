# E002-491 | Frozen calibration-subject image-content experiment

Frozen 2026-10-27 before opening S01 eye-video frames. This experiment is **not** a validation of E002-371, anatomical blink labels, shutter duration, or acquisition timing. It is a deliberately limited first empirical human-video content test after the S24 metadata-only acquisition.

## Precommitted input and independence
- Public Guttmann-Flury et al. motor-imagery rehost, https://zenodo.org/records/18970793, S01.zip (calibration participant, never S21-S31 held-out).
- Archive MD5: `fb56109542a13aa7879778833fe4cbaa`. Reject any checksum, path, codec or decoder failure.
- Select lexicographically first `*_phantom.avi`; decode at most the first **12,000 native frames**, in original frame order, via FFmpeg to 64x64 grayscale using area downsampling. Do not interpret AVI 1-fps declarations or paper 150-fps statement as authenticated time. Do not fabricate frame timestamps.
- Do not upload or commit raw frames, video, crops, facial images or per-frame pixel arrays. Hosted artifact may contain only aggregate metrics and a maximum of 20 frame indices for independent local review.

## Frozen proxy and nuisance rejection
- For each pair, subtract the whole-frame mean brightness change before absolute pixel differencing.
- Central ROI: x,y in [16,48); outer border: x<8 or x>=56 or y<8 or y>=56.
- Let C and B be mean absolute brightness-corrected differences over central and border pixels, divided by 255.
- A **localized motion candidate**, not a blink, requires C >= 0.035, C/(B+0.01) >= 1.7, absolute whole-frame mean change <= 15 grayscale units, and ratio of frame contrast standard deviations within [1/1.2,1.2]. Exact duplicate frames and low-contrast frames (<10 grayscale standard deviation) are non-eligible.
- Preserve candidate count, number of pairs, duplicate count, confounded pair count, C/B quantiles, and up to 20 highest-scoring candidate indices separated by >=5 native frames. No timing or physical speed conversion.

## Predicted outcomes and kill criteria
1. If authentic S01 video decodes and contains localized image changes, the precommitted proxy should yield at least one candidate. This is a weak motion-screening prediction only.
2. If there are no candidates, report a negative result rather than tuning thresholds.
3. If more than 20% of nonduplicate frame pairs are confounded by photometric/contrast gates, classify this screening proxy as nuisance-unstable. No blink claims under either outcome.
4. Independently test constant frames, global brightness shift, localized moving patch, border-only change, duplicate frames, low contrast, and a gaze-like central translation. The gaze control **must not** be interpreted as an anatomical closure.
5. The strongest possible result here is **authentic human image-content variation with nuisance-qualified candidate indices**. A candidate is neither a measured eyelid aperture nor a closure. Human reference validation still requires anatomical annotations, exposure calibration and independent clock provenance.

## Product enforcement
For every result: `physical_hidden_closure_certified=false`, `anatomical_closure_labels=0`, `independent_hardware_clock_authenticated=false`, `product=ABSTAIN_UNCALIBRATED`, `release=BLOCKED`. This exploratory screening is not part of the released product.
