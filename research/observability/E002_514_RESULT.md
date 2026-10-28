# E002-514 | Held-out coded-optical shutter calibration feasibility: synthetic PASS, physical BLOCKED

Date: 2026-10-29. Frozen in [E002_514_FROZEN.md](E002_514_FROZEN.md) at commit 4957750 before executing held-out seeds. Evidence tier: **synthetic instrument feasibility**, not actual camera or human measurement. Code: [e002_514_coded_optical.py](e002_514_coded_optical.py); adversarial tests: [test_e002_514_coded_optical.py](test_e002_514_coded_optical.py).

## Question and new experimental information

E002-513 proved that distant optical anchors do not bound an individual camera shutter gap under a non-affine clock. E002-514 tests a distinct, instrument-oriented remedy: can *each frame* be associated with a unique local optical exposure window by integrating eight independently coded, externally clocked LED signals, without trusting nominal FPS?

The solver exhaustively considers all possible 1-ms exposure starts across the entire 1,600-ms stimulus and all exposure durations from 8 to 12 ms. It retains **all** shutter windows whose eight integrated optical intensities agree with the observed vector within a fixed max-error tolerance of 0.010. The conservative blind-gap upper bound is max(0, maximum next feasible start - minimum previous feasible end). This is set-valued inference, not a best-fit timestamp masquerading as a physical guarantee.

The *synthetic* forward model assumes eight perfectly separated binary optical channels, known code phase and 1-ms tick duration, linear and calibrated radiometric response, 10-ms exposures, independent uniform measurement noise of at most 0.004, and no saturation, ambient interference, rolling shutter, blur, missingness or sensor mixing. True camera starts vary by up to ±2 ms around a 30-fps generating schedule, but the inverse solver never receives or uses that schedule.

## Frozen held-out result

Development disclosure: before the preregistration commit, the forward model and candidate search were explored on seeds 11, 23, 37, 51 and 79 with a narrower nominal-time search, and five frames of seed 11 were inspected under a full-record search. Those development observations are **not** independent held-out evidence. After freezing the full-record search, thresholds, and seeds, the separate 101/103/107/109/113 cohort was executed once without post-outcome tuning.

Five prespecified seeds (101, 103, 107, 109, 113), 40 frames each:

| Seed | True exposure contained | Unique interval | Gaps evaluated | Unsafe underbounds | Maximum gap conservatism |
|---|---:|---:|---:|---:|---:|
| 101 | 40/40 | 40/40 | 39/39 | 0 | 0 ms |
| 103 | 40/40 | 40/40 | 39/39 | 0 | 0 ms |
| 107 | 40/40 | 39/40 | 39/39 | 0 | 1 ms |
| 109 | 40/40 | 40/40 | 39/39 | 0 | 0 ms |
| 113 | 40/40 | 40/40 | 39/39 | 0 | 0 ms |
| **Total** | **200/200** | **199/200** | **195/195** | **0** | **1 ms** |

Median conservatism was 0 ms. All preregistered synthetic pass criteria were met, with no threshold or code-seed tuning after the freeze. Fourteen adversarial software controls passed locally. The hosted CI workflow includes Python reproduction and independent JavaScript interval-envelope arithmetic; hosted success must be checked separately.

**Interpretation:** Under this unusually favorable and explicitly bounded synthetic optical-response model, a spatially coded optical target can recover local frame exposure intervals with 1-ms resolution without assuming affine camera timing. This is a feasibility result, not an authenticated 1-ms camera calibration. Exact set coverage is a consequence of the assumed noise envelope and forward-model correctness; empirical *uniqueness/coverage* in the held-out synthetic worlds is the nontrivial measured output. The 1-ms grid cannot certify sub-tick optical timing or continuous-time shutter boundaries.

## Failure modes and release blockers

The code deliberately returns product ABSTAIN_UNCALIBRATED and release BLOCKED regardless of synthetic success. The physical input gate requires independent photodiode/logic-analyzer clocking, measured optical waveform, radiometric linearity and gain/offset bounds, camera exposure geometry, rolling-shutter scanline correspondence, native-frame continuity, clock uncertainty, blur/missingness and ambient-brightness bounds. Self-reported flags are **not independent attestation**.

Unknown code phase, exposure shorter than 8 ms or longer than 12 ms, automatic exposure/gain, nonlinearity, gamma, saturation, LED cross-talk, optical aliasing, scene reflections, rolling-shutter multirow mixing, or undocumented timing jitter can invalidate set coverage even if a small residual is observed. No observed small residual proves these assumptions. A real physical experiment must challenge the forward model under independently observed counterexamples and reject it if truth falls outside its feasible set.

## Executable physical study protocol (not yet performed)

**Instrument phase:** Build an independently timestamped optical stimulus using a hardware pattern generator with eight independently driven LED regions and a photodiode/logic-analyzer trace of actual emitted light. Do not use phone/screen animation or video metadata as the reference clock. Use raw linear sensor measurements with locked exposure, gain, white balance and focus. Calibrate dark and flat fields, LED response/gain uncertainty, crosstalk, ambient illumination, spatial blur, rolling-shutter row delays and clock phase on separate calibration trials. Verify native-frame continuity and exact sensor-row correspondence. A camera exposure-sync output or other independent hardware ground truth is needed to *validate* inferred exposure starts/ends; without it, report only internally consistent optical fits, not physical timing accuracy.

Freeze a separate, unseen set of LED codes, exposures, camera conditions and timing disturbances before instrument evaluation. Compare predicted interval sets against independently instrumented exposure timing. Kill the method on **any** independently measured exposure outside its claimed feasible set; report abstentions, interval width, per-gap upper-bound error, coverage and stratified failure by lighting, blur, dropped frames, rolling shutter, motion, glasses/occlusion and camera. Do not silently widen tolerance after observing failure. The present 0.010 synthetic tolerance is not a physical tolerance and must be replaced by an independent calibration envelope.

**Human phase:** Complete the already frozen E002-507 S01 260-frame packet with two genuinely independent blinded anatomical reviewers and a separately calibrated positive iris-diameter uncertainty. Treat it as feasibility/native-frame aliasing only. Then preregister participant-disjoint S21–S31 high-rate reference comparisons, physical exposure calibration and an independently justified continuous-time eyelid-speed envelope; a high-frame-rate finite-difference maximum alone cannot establish that envelope. An initial eight-person study is a counterexample/feasibility pilot, not a 1%-risk certification. If seeking a 95%-confidence below-1% conditional participant risk with zero false exclusions, the E002-511 design requires at least 299 *certificate-bearing independent participants*, with a separate utility/coverage requirement.

## Status

- Human anatomical reviews: **0**.
- Independently calibrated physical shutter/clock: **0**.
- Certified continuous-time human eyelid velocity bounds: **0**.
- Participant-disjoint physical predictions: **0**.
- Product: **ABSTAIN_UNCALIBRATED**. Release: **BLOCKED**.

Do not substitute further synthetic parameter sweeps for physical optical data or the two actual blinded reviewers. Hush PR #45 remains a separate workstream.
