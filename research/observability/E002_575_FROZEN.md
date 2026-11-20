# E002-575 | Source-bound native-geometry LPW reviewer packets: prospective instrument freeze

Frozen 2026-11-01 **before** source-bound extraction code is persisted. This is an execution artifact for the already-frozen E002-573 participant-disjoint pilot and E002-574 window selection. It neither changes the E002-371 scientific kernel nor alters E002-567 physical-camera requirements. No LPW source frames have been acquired or viewed.

## Question and falsifiers

Can the exact native frame positions selected by E002-574 be reproducibly extracted from locally authorized human video, retaining the native decoded image dimensions, with cryptographic source binding, blinded reviewer payloads, and no public transfer? If the source-bound extraction fails, the proposed held-out human experiment is not executable without a new preregistration.

**Predictions locked before implementation:**

1. On a generated 95-Hz, 57-frame FFV1 video, two nonoverlapping 19-frame windows selected at native indices 0–18 and 38–56 yield 38 decoded PNG images for each reviewer, with identical frame bytes between reviewer A/B, exact native 96x64 geometry, no source identifiers in reviewer filenames or JSON, and an owner-only index/digest audit.
2. A changed source hash, false declared native frame count, repeated/overlapping window, nonmonotonic presentation timestamps, variable frame geometry, unsafe/symlinked path, prefilled anatomical labels, missing reviewer clip, existing output destination or wrong manifest must fail closed without a publishable packet.
3. Native-frame selection is based on decoder frame index, not estimated FPS or wall-clock time. Do not resample, interpolate, crop, resize, or infer physiological labels. A lossless PNG of decoded video pixels is **not** raw sensor evidence; decoding can include color conversion and codec artifacts.
4. The only successful output is an owner-private source audit and two separate owner-controlled reviewer folders. Reviewer folders contain 19 decoded frames per clip, a blank anatomical rating template and a nonidentifying manifest. Source paths, native indices and participant identities remain owner-only.
5. All claims remain `SOURCE_BOUND_NATIVE_FRAME_PACKET_ONLY`, `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Successful extraction does not certify acquisition FPS, exposure, shutter, camera clock, eyelid velocity, anatomical closure or independent human annotation.

## Threat and nuisance model

The attack surface is manifest substitution, stale/wrong source video, accidental frame omission or duplication, native-geometry changes, prefilled labels, source-index disclosure to reviewers, unsafe filesystem outputs, and accidental redistribution. Verify SHA-256 of source video before and after extraction, compare all decoded frame counts to independently declared inventory counts, require strictly increasing container presentation timestamps, reject changing decoded dimensions, enforce exact reviewer template shape, use private file permissions and create output only after complete success. Decode only locally through ffprobe/ffmpeg; never download or upload eye-region images in public CI. Container PTS monotonicity is an **integrity check**, not independent optical clock calibration.

Not addressed: a compromised source custodian, fabricated video with matching manifest hash, physical shutter/rolling-sensor exposure, sensor nonlinearity, identity of a real participant, a malicious local OS, or reviewers sharing their answers. Native source acquisition and two genuinely independent human reviewers remain separate steps. The source license is noncommercial scientific research; all imagery remains private.

## Go/no-go

Run synthetic adversarial tests locally and on public CI **only using generated nonhuman test patterns**. Use the instrument on the authentic 2.4-GB LPW archive only once in an authorized private environment after the source inventory and frozen E002-574 mapping are verified. If it fails, report the failure and preserve evidence without modifying held-out selection. If it succeeds, hand separate private packets to two qualified, blinded human reviewers, then use E002-573's frozen positive-only native-frame alias test. Even a successful human alias witness is not E002-371 physical validation. E002-567's synchronized camera/photodiode study is still the decisive physical gate.
