# E002-435 — bitstream-identical media-clock non-identifiability (real instrument experiment)

**Date:** 2026-10-25. **Parent scientific kernel:** E002-371. **Protocol frozen first:** commit `45506d7`. **Evidence tier:** actual FFmpeg/FFprobe lossless codec + stream-copy operations on generated image frames. **Not:** human eyelid measurement, authenticated camera sensor timing, or a new mathematical theorem.

## Decisive result

The exact same 13 ordered FFV1 **compressed video packet payloads** and decoded RGB frames can carry three incompatible container presentation clocks after ordinary **stream-copy** operations. Every packet's SHA-256 and every decoded frame's SHA-256 matched across the base, identity, scaled and offset variants. This is stronger than a comparison of visually similar images: no video packet re-encoding was used in the retimed variants.

| Observed condition | Final frame PTS | Max interframe PTS gap | Maximum difference from base | FFprobe reported average FPS | Packet and pixel identity |
| --- | ---: | ---: | ---: | ---: | --- |
| Original 13-frame file | 0.48 s | 0.04 s | 0 s | 25 | Baseline |
| Identity stream copy | 0.48 s | 0.04 s | 0 s | 25 | Exact |
| `-itsscale 2` stream copy | **0.96 s** | **0.08 s** | **0.48 s** | **25** | Exact |
| `-itsoffset 0.8` stream copy | **1.28 s** | 0.04 s | **0.80 s** | **25** | Exact |

All three frozen retiming predictions passed on local FFmpeg/FFprobe **7.1.5-0+deb13u1**. The surprising diagnostic is that the scaled variant still reported **25 fps** as its average-rate metadata even though its actual PTS intervals doubled to 80 ms. This is an observed property of this FFmpeg/Matroska fixture, not a universal statement about all codecs or metadata.

**Scientific interpretation:** identical compressed pixels cannot authenticate their acquisition clock. Even preserving a plausible, monotone, internally consistent PTS trace cannot establish the original hardware exposure-start/end times. The inverse mapping from an encoded frame sequence to physical acquisition times is non-unique unless an independent, trusted timing witness is supplied.

This is a direct **real encoded-media witness** for an established provenance limitation, not a novel information-theoretic result or proof that a particular camera had incorrect timestamps. E002-434 showed that nominal FPS can miss real *container* gaps; E002-435 shows that **even exact packet identity cannot bind those gaps to the original sensor clock**.

## Falsification and controls

The [frozen protocol](E002_435_FROZEN.md) predeclared a 13-frame FFV1/Matroska 25-Hz baseline, an unchanged stream-copy control, 2× timestamp scaling and +0.8-s offset, with 1-ms tolerances. The code checks both independently extracted packet SHA-256 and decoded RGB frame SHA-256. It fails if packet or pixel content changes, if frame/packet counts or timestamps disagree, if source frames are not distinguishable, if timing predictions fail, or if any variant authorizes physical measurement.

Eight independent local unittest groups **passed**, including actual FFmpeg stream-copy execution and deliberate packet, pixel, PTS, frame-count and authorization corruption. A dedicated GitHub Actions workflow runs the same tests and reproduces the frozen result; hosted status must be checked separately.

Reproduce without paid resources:

```sh
PYTHONPATH=research/observability python -m unittest -v research/observability/test_e002_435_media_clock.py
python research/observability/e002_435_media_clock.py --output /tmp/e002_435_full.json
```

The [machine-readable compact aggregate](E002_435_INSTRUMENT_AGGREGATE.json) preserves observed PTS and the identity verdicts. The executable writes **full ordered packet and pixel SHA-256 sequences, exact FFmpeg command lines and versions** to the JSON output. The [vector figure](E002_435_CLOCK_ALIAS.svg) plots all three incompatible clocks over the identical frame sequence.

## Direct product consequence and limitation

Lucent's E002-434 `--container-pts` diagnostic is appropriate for **encoded-media presentation-time analysis only**. Neither that option nor nominal frame timing can be promoted to a physical no-hidden-closure certificate merely by checking that the video decodes correctly, frame hashes match, PTS is monotone, or rate metadata looks plausible.

For a physical shutter-gap claim, require independently archived and verified sensor exposure-start/end timestamps, calibrated clock synchronization and drift, rolling-row/shutter response, independently registered aperture geometry, illumination, missingness and physiological velocity assumptions. An unverified external manifest or an unsigned hash is not independent authentication.

**Unresolved:** zero human sequences, zero independently authenticated sensor exposure traces, no anatomical aperture reference, no validated hard velocity envelope, no blinded participant-disjoint predictions. The next decisive work is the actual E002-433 prospective human/instrument acquisition, not further container-format variants. Until then **E002-371 remains physically unvalidated**, and no hidden-closure, blink-duration, PERCLOS or fatigue capability is unlocked: `ABSTAIN_UNCALIBRATED`.
