# E002-490 RESULT — independent real-codec optical-clock replay and CI repair

**Date:** 2026-10-27. **Evidence tier:** local independent FFmpeg FFV1 encoder/decoder with *synthetic* optical frames, plus a committed hosted replay pending completion. No physical camera acquisition or new human anatomical labels.

## New independent instrument result

An independent Python implementation (no imports from E002-439) authored 12 synthetic 64×32 optical frames with a 16-bit binary tick code and 16 reference cells. It used the actual FFmpeg FFV1 encoder and decoder, then re-encoded the same frames with container presentation timestamps doubled. This independently checks the E002-439 principle that an image-borne time code and container PTS are distinct observables.

**Local independent replay on Debian FFmpeg 7.1.5:**

| Prespecified check | Observed |
| --- | --- |
| Authored and recovered optical ticks | 12/12 exact |
| Pixel equality before/after retiming | 12/12 byte-identical |
| Last original container PTS | 500 ms |
| Last retimed container PTS | 1000 ms |
| Maximum PTS displacement | 500 ms |
| Physical shutter acquisitions | 0 |
| Anatomical human reference sequences | 0 |

The independent replay's optical payload is deliberately different from E002-439's Gray/CRC implementation. The result supports a **virtual media-container provenance counterexample**, not camera exposure or human-eyelid timing. The clock ticks themselves were synthetic author-supplied values, not independently measured oscillator time.

## Hosted CI failure diagnosed and repaired in source

At [run 40544611566](https://github.com/sushxnthd/lucent/actions/runs/40544611566), the 13-method E002-439 test suite passed **12 tests with one FFmpeg-dependent skip**. The experiment then failed because both `ffmpeg` and `ffprobe` were unavailable. Its preceding `ffmpeg -version | head` check appeared green because the pipeline lacked `pipefail`. The green dependency step did **not** mean the tools existed.

The repaired [workflow](../../.github/workflows/e002_439_optical_clock.yml) now explicitly provisions both binaries, checks their presence under `set -euo pipefail`, runs the actual E002-439 encoder/decoder tests and machine-readable experiment, and independently replays the E002-490 virtual optical clock. The two programs do not share an optical payload encoder or decoder.

The hosted E002-490 run was **queued at report creation**: [run 40551612138](https://github.com/sushxnthd/lucent/actions/runs/40551612138) (pull request), with a separate push run [40551605227](https://github.com/sushxnthd/lucent/actions/runs/40551605227). Neither is reported as successful before inspection. A dependency installation failure is a CI failure, not a scientific falsification.

## Consequence and stop

This closes an independent local **reproducibility gap**, but does not supply the missing real measurement. The previously checksum-verified S19/S24 AVI headers and S19 optical-frame analyses still cannot authenticate a physical acquisition clock, shutter support, millimeter aperture or hard physiological speed cap. E002-371 is **not physically validated**.

Do not reopen S19 timestamp archaeology, tune killed optical proxies, or substitute more synthetic theorems for external evidence. The next decisive action remains independently timed optical acquisition and blinded two-rater human anatomical validation, with participant-disjoint predictions. Product hidden-closure, blink-duration, PERCLOS, fatigue and medical outputs remain `ABSTAIN_UNCALIBRATED`; release blocked. PR #26 remains draft/unmerged. Hush PR #45 is separate and unchanged.
