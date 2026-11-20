# E002-507 | Frozen anatomical native-frame alias witness evaluator

Date: 2026-10-28. Frozen **before independent human ratings** in [E002_507_FROZEN.md](E002_507_FROZEN.md). Executable [e002_507_anatomical_alias.py](e002_507_anatomical_alias.py) reuses the E002-492/502 **unchanged private two-rater templates** and the same 20 frozen S01 clips. This is a human-validation **instrument**, not a completed human study.

## What changes scientifically

E002-501's image-motion proxy failed under 1-pixel jitter and is retired. This evaluator makes a different, anatomically defined, prospective prediction: for each frozen 13-frame clip, classify frames 3 and 8 and the four interior native frames 4–7 using two blinded reviewers' conservative aperture intervals with **explicit positive iris-diameter error**. A CLOSED interior with OPEN endpoints is a native-frame alias witness; all-open interior is **not** proof of no continuous-time closure. No FPS, velocity, or shutter inference is made. Candidate/control status is not used to choose windows.

The evaluator reports only six aggregate counts and always outputs `ABSTAIN_UNCALIBRATED` and `BLOCKED`. Missing or zero iris-scale uncertainty, absent review, disagreement, nuisance, malformed frame order and wrong manifests fail closed or abstain. It does **not** verify that raters are different humans or that scale uncertainty was independently calibrated.

## Reproduction (authorized local machine only)

First execute E002-502's local-only handoff and obtain **two actual independent blinded anatomical reviews** plus independently established positive per-clip iris-diameter uncertainty. Create a private JSON mapping all 20 blinded clip IDs to `delta_px` values; do not publish it.

```bash
python research/observability/e002_507_anatomical_alias.py \
  --manifest /secure/LUCENT_E002_502_PRIVATE/OWNER_PRIVATE_DO_NOT_SHARE/OWNER_ONLY_MAPPING.json \
  --rater-a /secure/private_ratings/E002_492_RATER_A_PRIVATE.json \
  --rater-b /secure/private_ratings/E002_492_RATER_B_PRIVATE.json \
  --iris-scale-calibration /secure/private_ratings/IRIS_SCALE_DELTA_PRIVATE.json \
  --aggregate /secure/private_ratings/E002_507_AGGREGATE_ONLY.json
```

No imagery, per-frame positions, or per-clip predictions should leave the authorized machine. The tool has no human-data download, no network access and no deployment path.

## Verification / limits

13 synthetic adversarial controls passed **locally** against a minimal reproduction of the E002-492 manifest/template shapes. Hosted GitHub Actions verification against the real E002-492 implementation is **pending** and must be checked separately. No fabricated A/B test labels are evidence about real anatomy. A dual-rater CLOSED interior, if obtained, is evidence of **native-frame aliasing only**, not of hidden shutter-integrated closures.

External sources and novelty limitation: [2025 high-frame-rate 80-volunteer eyelid-trajectory study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12638546/), [120-Hz 40-subject VOG video archive](https://zenodo.org/records/13852050), [200-Hz OpenEDS](https://arxiv.org/abs/1905.03702), [100-Hz Silesian5 access conditions](https://www.blinkingmatters.com/research). These do not provide a certified continuous-time eyelid velocity ceiling or authenticated S01 shutter timing. Stop dataset searches after the two bounded attempts; do not invent a physiological speed bound.

**Independent human ratings: 0. Authenticated shutter/clock: 0. Certified continuous-time V: 0. Held-out physical predictions: 0.** E002-371 physically unvalidated. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Next: genuine independent S01 reviews and physical calibration, then participant-disjoint S21–S31 predictions. No more optical-proxy retuning.
