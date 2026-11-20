# E002-489 | Authentic S24 acquisition exposes a 1-fps container clock, not an anatomical clock

**2026-10-27. Primary E002-371 track. Evidence: authentic checksum-verified archive header, not decoded anatomy.**

## Authenticated empirical observation

GitHub Actions [40532997441](https://github.com/sushxnthd/lucent/actions/runs/40532997441) completed successfully at 2026-10-27 15:41 UTC. The hosted runner downloaded the public S24 archive and verified MD5 `3e8eb615d4a3415115f61dad5265ef12` (345,600,876 bytes). The selected `Sess01/MI241_phantom.avi` is 210,434,510 uncompressed bytes. The report is retained as [aggregate artifact 12747976179](https://github.com/sushxnthd/lucent/actions/runs/40532997441/artifacts/12747976179); no raw human imagery was uploaded.

The **actual AVI header** declares 50,932 frames, 320x288 pixels, `FMP4` compression, `avih.dwMicroSecPerFrame=1000000`, and first video `strh.dwScale=1, dwRate=1`. Thus **both container header rates equal 1.0 fps**. This is neither the original paper's 150-fps acquisition description nor the rehost's approximately 500-fps description. Agreement between two AVI header fields does **not** authenticate the hardware camera clock.

The header-implied duration is 50,932 s (14 h 8 min 52 s); hypothetical 150-fps and 500-fps durations for the same count are 339.5467 s and 101.864 s. None is a verified recording duration. This is a concrete **temporal provenance failure**: reading the file at its declared frame rate, or silently substituting 150/500 fps, would assign unverified times to eyelid events.

## Frozen next prediction and decision

Before further human-anatomy processing, freeze a provenance guard: if only a checksum-verified AVI header is available, all shutter-gap, eyelid-velocity, hidden-closure, blink-duration, PERCLOS, fatigue and medical certificates **must abstain**, regardless of nominal header agreement or an operator-supplied preferred fps. Do not reclassify 1 fps as measured acquisition cadence.

Demonstrate sensitivity using a **strictly illustrative**, zero-exposure point-sampling scenario: b=0.3 mm, closure threshold c=0.1 mm, assumed V=40 mm/s. Then R=V/[2(b-c)f]=100/f, giving R=100 at 1 fps, 0.666667 at 150 fps and 0.2 at 500 fps. The kinematic possibility classification flips across unsupported timing assumptions. These parameters are **not human calibrations** and do not establish real exclusion, closure, or instrument performance.

Acceptance controls: reject malformed/nonfinite rate, inconsistent headers, invalid frame count; preserve abstention even if metadata falsely claims independent timing; independently test the exact arithmetic. The only permitted product behavior is a clock-provenance error and `ABSTAIN_UNCALIBRATED`.

## Next physical/human experiment

Acquire a **calibration** participant (not held-out S24) with independently sourced camera acquisition timestamps or camera trigger/clock provenance. If unavailable, explicitly classify the data as a *container-timebase* dataset and do not claim an anatomical reference clock. Obtain measured exposure and jitter, independently annotated eyelid aperture and geometry, and velocity bounds under blur, gaze, brightness, glasses and missingness. Then preregister participant-disjoint gap predictions before testing the held-out sequences.

**No anatomical human frames decoded or annotated here; no physical shutter calibration. E002-371 is not physically validated. Release BLOCKED.** This report updates the previous E002-488 pending status; it does not assert the AVI 1-fps declaration is the camera's actual sampling rate.
