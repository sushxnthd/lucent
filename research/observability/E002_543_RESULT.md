# E002-543 RESULT | Real-capture optical edge falsification intake, no physical capture

2026-10-30. E002-371 primary observability kernel, persistent branch `research/observability-human-boundary`, draft PR #26. Protocol [E002_543_FROZEN.md](E002_543_FROZEN.md) was committed at `de0bfd5` **before** implementation. Evidence tier: **local synthetic schema and decision replay only**. This run acquired **zero** photodiode traces, camera captures or human anatomical ratings.

## Measurement question and one-sided answer

E002-542 showed that a camera timing fit can recover the correct injected timing while failing held-out radiometric and edge-flash challenges. A physical shutter study now needs a reproducible way to *reject* a purported shutter-only observation-transfer model when a verified flash outside its conservative exposure support changes the camera response. E002-543 implements that one-sided test for **owner-private** real-capture records. It does not infer the shutter timing from a synthetic waveform or nominal FPS.

For each held-out paired trial, let the pulse onset/offset and row-specific shutter start/end be **intervals** in milliseconds, with separately bounded synchronization uncertainty `j`. A trial is eligible only if

`pulse_offset_max + j < shutter_start_min` **or** `pulse_onset_min - j > shutter_end_max`.

If eligible and `|flash_ROI - control_ROI| > independently_predeclared_noise_upper`, report `TRANSFER_FALSIFICATION_CANDIDATE`. Otherwise report `NO_FALSIFICATION_CENSORED`, never `SHUTTER_CERTIFIED`. Overlap/equality returns `ABSTAIN_NOT_OUTSIDE`; invalid/uncertain records return abstention. A candidate rejects the **simple shutter-only optical transfer model conditional on source authenticity**, not necessarily the mechanical shutter timing: persistence, flare and ISP pathways may explain the effect.

## Frozen synthetic adversarial outcomes

The 16-method Python test suite passed locally, as did six independently coded Node.js arithmetic checks. No numeric threshold was tuned on physical or human data.

| Owner-supplied synthetic trial | Frozen classification |
| --- | --- |
| Flash strictly before shutter, 0.6 ROI difference > 0.05 noise bound | `TRANSFER_FALSIFICATION_CANDIDATE` |
| Flash strictly after shutter, 0.03 ROI difference <= 0.05 noise bound | `NO_FALSIFICATION_CENSORED` |
| Flash overlaps shutter support | `ABSTAIN_NOT_OUTSIDE` |
| Increase synchronization uncertainty from 0.2 ms to 2.1 ms | Both originally outside trials become `ABSTAIN_NOT_OUTSIDE` |
| Exact pulse/shutter boundary contact | `ABSTAIN_NOT_OUTSIDE` |
| Missing/duplicate identities, bad digests, wrong partition, missing flags | Session `ABSTAIN_INVALID_SESSION` |
| Unreliable quality, invalid intervals, nonfinite ROI | Trial `ABSTAIN_QUALITY` |

The output preserves the complete eligible/ineligible denominator and omits source IDs, frame IDs, calibration IDs and private digests. The dedicated [E002-543 workflow](../../.github/workflows/e002_543_optical_edge_intake.yml) runs Python tests, independent Node replay and the command-line intake on an ephemeral synthetic fixture. Hosted CI outcome must be verified separately.

## Private physical execution handoff

From the repository root on an **authorized private machine** after actual synchronized acquisition, prepare the exact `E002-543-v1` input manifest specified in [the frozen protocol](E002_543_FROZEN.md). Keep it **outside any Git checkout** and do not upload optical traces, native frames, individual ratings, participant mappings or private manifests to GitHub. The program accepts a local JSON path and emits aggregate-only results:

```bash
python research/observability/e002_543_optical_edge_intake.py \
  --input /secure/private/optical_edge_manifest.json \
  --output /secure/private/optical_edge_aggregate.json
```

The raw photodiode timing, camera-native frame IDs, independently measured synchronization error, noise bound and calibration digest must be recorded and externally audited before any candidate is described as a *physical* observation. A syntactically valid 64-hex digest or `independent_photodiode: true` flag is **not** proof that the optical source, prelabel timestamp or sensor timebase is authentic. A self-supplied noise upper is not a calibrated statistical bound. This CLI deliberately never emits a physical-certification state.

## Science boundary and next decision

This is a **measurement-validation artifact**, not a new mathematical law, a physiological result or an externally validated camera calibration. It converts E002-542's prose-only physical handoff into a fail-closed input/decision path, but cannot itself collect hardware evidence. It does not change the rejected S01/S19 pixel-return observable, E002-371's conditional theorem, or the requirement for two independently blinded anatomical raters.

Physical shutter captures: **0**. Independent human anatomical ratings: **0**. Certified continuous-time human velocity/acceleration envelopes: **0**. Participant-disjoint physical predictions: **0**. The next scientifically decisive action remains actual photodiode-timed edge captures and the existing E002-502 private two-rater S01 review, followed by E002-519/525/527 prospective participant-disjoint reference tests. Further synthetic threshold tuning is not warranted.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. No merge, deployment, new branch, or change to Hush PR #45.
