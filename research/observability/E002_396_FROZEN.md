# E002-396 — frozen unseen-participant transfer of E002-395 image-proxy falsification (2026-10-23)

**This protocol is frozen before downloading or inspecting participant S19.** Source: Guttmann-Flury et al. Eye-BCI SSVEP public CC0 mirror, Zenodo record **21905748**, `S19.zip` MD5 **8a16cf170a9c7e9660f6e22b81d7d0a** (373.1 MB). S19 is a different participant from S01. No S19 image, threshold or marker window has been inspected.

## Predeclared hypotheses, including the negative result
E002-395's S01 held-out fixed feature `closure_score=1-dark_fraction` failed (AUC 0.2004). **Do not rebrand its inverse as a validated detector.** The S01 observation motivates a prospectively falsifiable S19 test:
1. **H1**: inverted score `dark_fraction` has S19 AUC >= 0.75 against EEG blink-marker windows versus matched non-event windows. This is a hypothesis **derived from S01**, not a preregistered S01 success.
2. **H2**: original S01 score on S19 has AUC < 0.50. Report both AUCs regardless of sign; do not select the better one as the product.
3. **H3**: applying the **frozen S01 training threshold 0.7938034188034189** to original-score S19 windows gives specificity <= 0.50. If contradicted, report it.
4. Report fixed global gain 0.7 and 1.3, glare, blur sigma 2, and (+8,+6)-px translation. No post-hoc ROI or threshold fitting.

## Selection and measurement
- Choose the lexicographically first session containing a paired `*_sync.csv` and `*_phantom.avi`; do not search sessions for favorable outcomes. Reject if no paired files. MD5-verify entire ZIP.
- EEG event: `Blinks>0`; select nearest frame within 10 ms with 3 valid adjacent frames on each side and no >20-ms EEG gap. Fixed non-event offsets in order +0.55, -0.55, +0.75, -0.75, +1.05, -1.05 s, requiring >=0.35 s distance from any EEG marker. Require >=15 event/control pairs, otherwise underpowered.
- Same fixed ROI, skin reference, dark-fraction feature and seven-frame max aggregation as E002-395; **do not retrain**. S19 labels are EEG marker timestamps, not physical aperture. Report missingness/gaps and clipping. If video geometry is incompatible with fixed ROI, abstain rather than remap.
- Independent oracle recomputes AUC, S01 threshold specificity and frozen decisions from anonymous scores. Do not commit identifiable images. The primary completion gate E002-371 physical aperture/shutter bound remains **unmet** regardless of outcomes.

## Product and evidence rules
This is an untouched-person test of **image/EEG marker association**, not a test of actual eyelid velocity, physical threshold crossings, fatigue, PERCLOS, or hidden-closure certificates. No matter whether H1 succeeds, Lucent must remain `ABSTAIN_UNCALIBRATED` pending physically calibrated aperture and exposure, disjoint physiological velocity estimation, independent participant/device holdouts and adversarial optical validation.
