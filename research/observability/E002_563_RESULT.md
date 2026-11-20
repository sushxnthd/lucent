# E002-563 RESULT | Original human Phantom AVI is **1-fps presentation-timed**, not a 150/500-fps sensor clock

Date: 2026-10-31. Frozen protocol: [E002_563_FROZEN.md](E002_563_FROZEN.md). Primary E002-371 kernel. Evidence tier: **real public human-source bytes, Zenodo-published MD5 verification, hosted FFprobe/FFmpeg decoding, synthetic adversarial controls**. This is **not** an independently certified physiological clock, blink annotation, physical shutter test or closure-exclusion validation.

## First actual public human-video acquisition

[Hosted GitHub Actions run 41174653753](https://github.com/sushxnthd/lucent/actions/runs/41174653753) **passed**. It streamed the public [Zenodo Motor Execution S01 archive](https://zenodo.org/records/18971758) to an ephemeral runner, checked the published MD5, extracted the first original byte-preserved Phantom AVI privately, decoded 90 frames and deleted raw acquisition bytes. No video/frame/participant identifier was uploaded or committed. The 3/3 local synthetic/ZIP-security tests also passed in hosted CI.

| Verified or observed item | Result |
|---|---|
| ZIP bytes | **410,184,489** |
| ZIP MD5 | **bce89dd9fbb67e27a656623aa27927e0** (matches Zenodo) |
| Phantom AVI members | **1** |
| AVI bytes | **272,013,818** |
| AVI codec / dimensions | **MPEG-4 / 320 × 288** |
| FFprobe `avg_frame_rate` | **1/1 fps** |
| FFprobe `r_frame_rate` | **1/1 fps** |
| AVI-reported frame count | **48,756** (container report, not independent full decode) |
| Prefix frames successfully decoded | **90** |
| Exactly identical adjacent decoded frames in prefix | **0/89** |
| Locked rate verdict | **UNRESOLVED_RATE** |
| Original sensor clock verified | **NO** |
| Independent anatomical closure labels | **0** |

**Predeclared hypothesis falsified:** Neither the original-paper 150-fps sensor rate nor the Zenodo rehost's approximately 500-fps description is present in this AVI's *presentation metadata*. The AVI instead reports **1 fps**. This is consistent with a deliberately slowed export, but that explanation has not been independently verified. The observed 1-fps presentation time base is not evidence that the Phantom sensor captured at 1 fps. The rehost says original Phantom AVI was copied byte-for-byte; that does not certify acquisition timestamps.

## Exact timing consequences

For the 48,756 reported frames, three incompatible clocks would assign radically different sequence durations:

| Interpretation | Implied duration |
|---|---:|
| Trust AVI presentation rate, 1 fps | **48,756 s = 13 h 32 min 36 s** |
| Apply original-paper acquisition setting, 150 fps | **325.04 s = 5 min 25.04 s** |
| Apply rehost description, 500 fps | **97.512 s = 1 min 37.512 s** |

The [original 2025 Scientific Data paper](https://doi.org/10.1038/s41597-025-04861-9) explicitly states **150 fps** was selected to prevent loss of data; the [March 2026 Zenodo rehost](https://zenodo.org/records/18971758) describes the Phantom video as **~500 fps**. Its 40-trial Motor Execution protocol is qualitatively more compatible with a several-minute recording than a 97.5-second one. This is a consistency argument, **not a physical clock certificate**. Actual sensor timestamps, export playback policy, skipped frames and trigger synchronization remain unknown.

For a closure-positive interval of true duration `w`, ideal periodic point sampling at frequency `f` with an independently uniform random phase has `P(at least one positive sample)=min(1,f*w)`. Thus a hypothetical 4-ms interval is sampled with probability **0.60** at 150 fps versus **1.00** at 500 fps. These are model predictions, not measured human closure durations or probabilities; real exposure, annotation, phase and missingness can invalidate the assumptions. Crucially, *absence* of a positive sampled frame cannot certify continuous-time absence at either rate.

## Falsification and release consequence

This experiment establishes a concrete **presentation-time versus acquisition-time identifiability failure in an actual human eye-video file**. Any pipeline that takes `1/1` AVI timestamps literally, or silently replaces them with the rehost's 500-fps claim, is not allowed to produce physiological velocities, high-rate anatomical reference timestamps, E002-371 closure-negative exclusions or calibration certificates. In particular, replacing a true 150-fps spacing by 500-fps spacing would understate time gaps by **3.33×**, making some false exclusion claims possible under a hard velocity assumption.

**Required next experiment:** privately inspect the original S01 `*_sync.csv` and `*_phantom.xml` for independent trigger/frame correspondence, then reconcile with the paper's 150-fps hardware protocol; validate acquisition rate and dropped frames using externally sourced sensor/trigger information rather than AVI timestamps. Obtain independent blinded anatomical labels and original sensor exposure timing before any held-out closure adjudication. Keep any human media private. This is now an instrument provenance experiment, not another generic dataset search.

**Product:** `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Authenticated physical shutter captures **0**; independent human anatomical rater pairs **0**; certified continuous-time physiological velocity ceilings **0**; held-out physical closure-exclusion predictions **0**. One public human-video source archive was checksum-verified and decoded, but its acquisition time axis is unresolved.

Reproduce with `python -m unittest -v test_e002_563_public_phantom_probe.py` and `python e002_563_public_phantom_probe.py --output /tmp/sanitized.json` from `research/observability/`. No raw media is committed.
