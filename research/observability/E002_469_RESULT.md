# E002-469 RESULT — one-shot S19 human-video clock reconciliation (2026-10-27)

**Evidence tier:** empirical, checksum-verified source-file *schema and metadata* inspection. **Not** calibrated anatomical motion, not a physical shutter measurement, and not an E002-371 validation. This is the final S19 timing-metadata attempt under [E002-469_FROZEN.md](E002_469_FROZEN.md).

## Acquisition and independent execution

The previously frozen [one-shot workflow](https://github.com/sushxnthd/lucent/actions/runs/40379486941) completed successfully at 2026-10-26 18:43 UTC on commit `ee94375d9b16bdff488847c6a3cfb64a7916cddc`. All **5/5** adversarial fixture tests passed. The job independently downloaded the original S19 archive, checked the published MD5, parsed the original `ME191_phantom.xml` and `ME191_sync.csv`, and uploaded [artifact 12678846502](https://github.com/sushxnthd/lucent/actions/runs/40379486941/artifacts/12678846502). This report uses that immutable hosted artifact, not a guessed rate. [Sanitized aggregate](E002_469_SYNC_AGGREGATE.json) is committed separately, without raw timestamps, raw participant data, or images.

Archive SHA-256: `da4281a4d77f95683f541452a0f5b6e56ad8d54139e3be9d7b64374d77a41c25`. Hosted artifact JSON SHA-256, before copying to the repository: `7dbc595894e4382dfcc6efe09ae2e76bfac73c1f1e6ff77fe5bbdeb7d6b37ead`. The latter checksum refers to the original artifact's byte formatting, not the pretty-printed committed copy.

## Actual observed result

| Source | Independently observed | What it **does not** establish |
| --- | --- | --- |
| E002-468 original AVI | 52,049 frames; declared `1/1` fps and 1,000-ms container PTS steps | Physical acquisition rate, exposure window or shutter timing |
| E002-469 sync CSV | 423,600 data rows, 8 columns; 200,000 rows sampled for the clock gate; headers include `Time`, `PhanFrame`, `PhanTime`, `RelTime`, `RecordingTimestamp`, `LocalTimeStamp` | Units, physical clock identity, or an independently authenticated frame-time relation |
| E002-469 Phantom XML | 156,353 parsed XML elements; nominal numeric frame-rate declaration **167.0** | Actual video acquisition rate, stable timestamps, or shutter support |
| Frozen explicit-unit gate | `NO_EXPLICIT_FRAME_CLOCK`; 0 recognized canonical frame-index fields and 0 time fields carrying explicit units | Absence of *all conceivable* frame-clock correspondences |

**Important interpretation correction:** `NO_EXPLICIT_FRAME_CLOCK` is the frozen parser's **eligibility decision**, not proof that the files contain no plausible frame/time fields. In fact, `PhanFrame` and `PhanTime` occur in the same CSV header. The canonical-index regex does not recognize `PhanFrame`, and none of the time-like headers encodes seconds, milliseconds, microseconds or nanoseconds. No physical unit may be selected by matching a desired 150-, 167-, or 500-fps rate. No value of those rates is authenticated by this experiment. The XML's 167.0 is a device declaration, not a verified sampling interval. The earlier published 150-fps video description, rehost's approximately 500-fps description, XML's 167.0 and AVI's 1 fps remain unresolved as *physical* timing.

### Identifiability consequence

For any unlabeled numeric time column `t_i`, the physically distinct clocks `T_i = a t_i + b` with any `a > 0` yield the same recorded unitless table. If the data do not independently constrain `a`, a physical rate or anatomical velocity in mm/s is not identified. This simple scale ambiguity does not depend on which numerical rate looks plausible. Even an externally documented time unit would leave clock identity, exposure timing, shutter integration and anatomical reference to be authenticated separately. **This is an application of elementary measurement identifiability, not a novel theorem.**

## Frozen decision and product consequence

- `TIMING_UNAUTHENTICATED`; do not estimate S19 anatomical velocity or test E002-371 in milliseconds from this archive.
- Do not treat a container PTS, nominal XML rate, or unitless `PhanTime` as independently measured exposure time. Do not call a high-speed open-eye frame a definitive negative anatomical label.
- S19 remains development-only. S01 and other sealed holdout subjects were not opened. New anatomical annotations **0**; new physical acquisitions **0**.
- Product outputs requiring physical hidden-closure exclusion, blink duration, PERCLOS, fatigue or medical inference remain `ABSTAIN_UNCALIBRATED`. Do not merge or release PR #26.

**Stop rule executed:** No more S19 timestamp archaeology, rate guessing, or field-name tuning. The next eligible primary experiment is the previously frozen physical moving-aperture / independently timed optical phase-scan study, or acquisition of a *different* human recording with independently documented frame-to-clock units and shutter timing. That experiment must prospectively test ordinary-camera gap exclusions with an independent anatomical crossing witness and adversarial nuisance controls; an uninstrumented synthetic demonstration cannot substitute for human physiology. Preserve failures and abstentions.

## Reproduction

- Frozen protocol: [E002_469_FROZEN.md](E002_469_FROZEN.md).
- One-shot parser: [e002_469_sync_reconciliation.py](e002_469_sync_reconciliation.py).
- Five adversarial fixtures: [test_e002_469_sync_reconciliation.py](test_e002_469_sync_reconciliation.py).
- Successful hosted source acquisition: [run 40379486941](https://github.com/sushxnthd/lucent/actions/runs/40379486941).
- Sanitized evidence: [E002_469_SYNC_AGGREGATE.json](E002_469_SYNC_AGGREGATE.json).

No result in this report verifies a physiological velocity cap or physical hidden-closure exclusion. E002-371 remains physically unvalidated.
