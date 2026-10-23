# E002-393A — independent EEG synchronization falsifies naive human-video timing (2026-10-23)

**Source:** verified CC0 SSVEP011 from Guttmann-Flury et al. (2025), same MD5 as E002-392; frozen protocol at commit `5b3743d`. Reproduced in GitHub Actions run 39954570391.

## Actual observations
- 414,720 EEG sync rows at exactly 1-ms nominal increments; 53,680 unique consecutive Phantom frame IDs, matching the 53,680 decoded human eye frames.
- Frame-record interarrival time: 5th percentile 6 ms, median 7 ms, 95th percentile 7 ms. A long interarrival **gap of 872 ms** exists.
- Naively dividing all 53,679 frame steps by the entire elapsed EEG clock span produces **139.3706 fps**, which **fails** the frozen near-150-fps expectation. The AVI itself incorrectly reports 1 fps. The short 6/7-ms steps are consistent with an underlying ~150-Hz cadence quantized to the 1-kHz EEG clock, but *active-run rate has not yet been computed after excluding gaps*.
- The `Blinks` sidecar contains **112 isolated positive samples** among 414,720 rows, each only one 1-ms row long. These are event markers, **not 1-ms physical eyelid closures**.
- First six chronological blink markers occur at EEG times 4.846–12.761 s, **before the first recorded Phantom frame at 18.829 s**. The initial event-alignment implementation incorrectly mapped all six to the first video frame and generated a duplicated contact sheet. **That contact sheet is invalid evidence.**

## Scientific consequences
This actual human recording exposes **three independent ways to produce false confidence**: (1) AVI 1-fps metadata, (2) unsegmented cross-clock rate estimation across recording gaps, and (3) extrapolating EEG event markers outside camera coverage. Neither naive camera cadence nor isolated EEG markers can serve as ground-truth physical aperture.

## Required repair (not a retrospective change to the frozen prediction)
1. Report recording gaps, active inter-frame cadence excluding gaps >20 ms, and both global and active rates.
2. Select blink markers **strictly inside camera coverage**, with nearest-frame temporal error bounded by an independently measured frame interval. Exclude markers falling in camera gaps.
3. Preserve the failed original 150-fps prediction and the invalid initial event sheet; never report them as successes.
4. Still abstain from E002-371 hard human no-hidden-closure claims until physical aperture, exposure integration, optical transfer and independently calibrated velocity bounds exist.

## Artifact
`e002-392-human-feasibility` from run 39954570391 contains the raw numerical summary, repaired nominal video trace, and initial (invalid) blink-window sheet. Raw source footage was not redistributed.
