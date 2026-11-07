# E002-488 | Dependency-free authentic AVI header acquisition, frozen before execution

**2026-10-27; primary kernel E002-371; branch `research/observability-human-boundary`; draft PR #26.**

## Motivation and pre-result decision

The E002-487 replacement run 40529185541 remained in the `apt-get` provisioning step at the 2026-10-27 15:35 UTC inspection. Its FFmpeg-dependent path had not reached authentic video or synthetic tests. The next attempt must remove that dependency entirely and acquire the actual published archive.

## Frozen predictions and outcomes

1. Acquire the published `S24.zip` from `https://zenodo.org/records/18970793/files/S24.zip?download=1`, under 600 MB. Authenticate full ZIP MD5 `3e8eb615d4a3415115f61dad5265ef12` before reading metadata. Failure is `FAILED_DOWNLOAD` or `FAILED_INTAKE`, not a human result.
2. Safely select only the lexicographically first `*_phantom.avi` member. Reject traversal/symlinks/oversize; decompress only up to 8 MB of its header. Never decode, view, export or annotate anatomical frames. S24 remains held out.
3. Read AVI `avih.dwMicroSecPerFrame` and video `strh.dwRate/dwScale` independently. If rates disagree by >2%, declare `avi_rate_fields_agree_within_2pct=false`. Compare video stream declared rate against 150 fps (2025 paper) and ~500 fps (2026 rehost) without assuming either is true.
4. Even if the declared rate matches one source, the outcome is only `PASS_AUTHENTIC_ARCHIVE_HEADER_ONLY`. AVI header fields are nominal container declarations, **not independently measured acquisition times, per-frame timestamps, shutter durations or a verified velocity bound**. Physical E002-371 validation and human labels remain zero.
5. Independent local regression controls must include 150/500-fps synthetic AVI headers, checksum rejection, ZIP traversal, invalid RIFF, invalid rate and refusal to infer independent clock calibration.

## Kill criteria

- Download, MD5, ZIP safety or AVI-header parsing failure: do not infer acquisition rate. Preserve exact failure.
- Declared rates conflict: do not silently choose 150 or 500 fps; abstain from temporal reference claims.
- Any pass: advance to independent calibration-participant (S01–S20) human eyelid annotation and actual timing/shutter calibration. Never promote a header-only pass to a validated E002-371 closure claim.

## Release blocker

All hidden-closure, blink-duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`. Product release remains `BLOCKED`. No raw participant video is uploaded to GitHub or artifacts. No merging, deployment or force-push.
