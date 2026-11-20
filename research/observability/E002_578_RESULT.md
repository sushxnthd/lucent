# E002-578 | Real LPW human-video reviewer-packet execution: hosted PASS

Date: 2026-11-01. Primary kernel E002-371. Frozen before source processing in [E002_578_FROZEN.md](E002_578_FROZEN.md). Hosted verification: [GitHub Actions run 41252307878](https://github.com/sushxnthd/lucent/actions/runs/41252307878), job `124688160551`, completed **success**; actual job steps and output logs inspected. Executable: [e002_578_real_lpw_packet.py](e002_578_real_lpw_packet.py). The workflow has **zero uploaded artifacts**, independently checked through the GitHub Actions artifacts endpoint.

## Result: native human-source packet generation succeeded

The hosted runner re-acquired the original investigators' bounded LPW ZIP member `LPW/1/1.avi`, verified ZIP CRC and the exact E002-577 source SHA-256, and executed the **existing E002-575 packet builder** on this real human development recording. Participant `1` belongs to E002-573's pre-frozen **development** partition; no held-out video was accessed. No frame was inspected before the predeclared deterministic selection.

| Prespecified field | Hosted observation |
|---|---|
| Source video SHA-256 | `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86` |
| Native container frame count | 2,000 |
| Reported stream rate | 95/1 fps |
| Native geometry | 640 x 480 |
| Complete nonoverlapping 19-frame windows | 105 |
| Deterministically selected development windows | 10 |
| Source-bound decoded PNG frames per reviewer packet | **190** |
| Independent blank reviewer packets | **2** |
| Exact source-index binding and A/B PNG hash agreement | **PASS** |
| Native frame presentation timestamps | **Strictly monotonic container PTS** |
| Reviewer templates | **Blank and source-blinded** |
| Source checksum before/after decoding | **PASS** |
| Private human image artifacts uploaded | **0** |
| Anatomical human rater pairs | **0** |

The frozen self-test also passed: development partition membership, deterministic selection, complete-window bounds, source blinding, rejection of insufficient source length and rejection of prefilled reviewer templates. The job completed successfully after the private temporary source video, PNGs and packet directory were destroyed. The report contains no source image, landmark annotation, candidate event, or owner-only native-frame mapping.

## What this newly establishes

E002-575's reviewer packet builder is **not merely synthetically tested**: it successfully produced and independently hash-checked two source-bound, native-geometry, blinded packet sets on real 95-fps human eye-region video. The earlier E002-577 probe had decoded only three real source frames; this run executed 190 selected source frames through the full reviewer handoff. It closes a specific **human-source instrument execution** gap. The pipeline is ready for authorized private review, not yet scientifically validated for anatomy.

## Hard limits and next action

- **Zero human anatomical ratings**: the two packets are blank copies for two future genuinely independent raters. Automated packet construction is not independent human validation.
- **No closure labels or alias witnesses**: no blink or positive CLOSED interior frame was established. The original LPW pupil annotations cannot substitute for eyelid landmarks.
- **No physical timing certificate**: strictly increasing AVI PTS and a reported 95/1 stream rate are not independent shutter integration, rolling-row or clock calibration.
- **No physiological velocity ceiling or held-out physical predictions**: E002-371's sharp observability bound remains mathematically conditional and unvalidated in humans. This run did not measure or infer eyelid velocity.
- **Privacy**: LPW is noncommercial scientific research data. The runner produced no downloadable review packets. Human reviewers must receive authorized private copies via the established E002-575 process outside public CI.

Next decisive experiment: independently recruit and qualify two blinded human anatomical raters; privately generate and distribute E002-573's development/holdout packets from an authorized complete LPW source manifest, seal the exports, then run E002-576's one-sided held-out index-alias test. In parallel, execute E002-567's synchronized physical shutter/photodiode study. Do **not** repeat this source acquisition or claim a negative hidden-closure certificate from 95-fps frames.

**Evidence tier:** `REAL_HUMAN_SOURCE_INSTRUMENT_ONLY`. **Product:** `ABSTAIN_UNCALIBRATED`. **Production release:** `BLOCKED`. **Hush:** no branch or PR writes in this primary experiment.
