# E002-446 — anatomical edge-span identifiability stress test

**2026-10-25.** [Frozen protocol](E002_446_FROZEN.md) · [Instrument](e002_446_edge_triage.py) · [Tests](test_e002_446_edge_triage.py) · [Hosted workflow](../../.github/workflows/e002_446_edge_triage.yml).

## New falsification result

A fixed 16-strip, vertical-gradient image instrument can return the same apparent 90-pixel upper/lower edge separation for two different causal scenes: (a) a synthetic eyelid-like dark opening and (b) a dark horizontal stripe or shadow unrelated to eyelid anatomy. The two constructed grayscale images are **pixel-identical**, so any deterministic image-only estimator must give the same answer. This is an explicit, executable counterexample to treating a plausible image-edge pair as an authenticated eyelid-aperture measurement. It is not a novel general theorem; it is an instrument-specific nuisance falsification.

The instrument rejects a small pupil-only dark disk under the frozen width-consensus criterion, rejects flat images, and is invariant to a uniform additive 30-level brightness shift in its synthetic fixture. These controls do **not** rescue anatomical identification against the stripe, gaze, glasses, nonuniform shadows, blur, camera movement, or changing pupil shape.

**11 local synthetic/adversarial tests passed** against the frozen implementation, including large-jump rejection, absent-candidate null handling, malformed inputs, and fail-closed product behavior. This is synthetic verification only, not an estimate of human accuracy.

## Frozen S19 experiment

The committed CI workflow independently hash-verifies the published S19 archive and computes only aggregate statistics on the first **3,000** human-video frames. It is designed to report candidate coverage, pixel-span percentiles, adjacent-pair jump statistics, and a necessary-only stability screen. **Human S19 result now obtained and frozen.** [Hosted execution 40212280636](https://github.com/sushxnthd/lucent/actions/runs/40212280636) completed successfully, including all **11 adversarial tests** and decoding the frozen first **3,000 S19 human frames**. Exactly **0/3,000 frames (0.0%)** passed the fixed edge-span candidate criterion; there were **0 consecutive candidate pairs**. Span and jump statistics are **null**, not zero physical aperture or velocity. The preregistered triage screen therefore returned **REJECT_UNSTABLE_OR_INSUFFICIENT_EDGE_PROXY**. The exact [nonidentifying aggregate](E002_446_HUMAN_AGGREGATE.json) is committed. This is a substantive *negative human-video result*: the simple fixed-geometry image-edge detector is not even suitable for annotation triage on this pilot, much less anatomical certification. The failure may reflect eye geometry, illumination polarity, orientation, contrast, gaze, or other nuisance; the test cannot distinguish those causes. No threshold retuning on S19 is authorized.

Even if S19 candidate coverage and temporal stability pass, the correct classification is **ANNOTATION_TRIAGE_ONLY_NOT_ANATOMY**. If either fails, reject the proxy for triage. The stripe counterexample is a standing veto against converting any proxy measurement to anatomical or physical eyelid-velocity evidence.

## Measurement-science and product consequence

The previous E002-445 optical spatial association is not enough to identify an eyelid. E002-446 directly tests this semantic identification step, rather than conducting another metadata audit. No candidate pixels are millimeters, no candidate event timestamps are physical shutter exposures, and no edge-span speed is a physiological velocity bound.

A blinded two-rater anatomical annotation and independently calibrated camera exposure/scale are mandatory for the E002-371 prospective test. S21/S22 remain untouched. **Physical E002-371 validation: NOT ESTABLISHED.** Hidden-closure guarantees, blink duration, PERCLOS, fatigue, and medical claims remain **ABSTAIN_UNCALIBRATED**. No merge, no release, and no Hush changes.
