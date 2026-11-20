# E002-597 | Frozen real-human-source nuisance attack on uncalibrated image proxies

Date: 2026-11-02. E002-371 primary kernel. This protocol is frozen before the source-bound pixel experiment and before any result is inspected. This is **development-participant empirical image analysis**, not anatomical validation.

## Research question and rejection gate
Can two deliberately simple ordinary-camera image observables, dark-pixel fraction and vertical-edge energy, be stable enough under ordinary acquisition nuisances to justify use as uncalibrated eyelid-aperture evidence? Expect **no**. Independently of the outcome, neither proxy may certify closure without anatomical ground truth and physical imaging calibration. The experiment measures whether a *necessary* nuisance-stability criterion is violated on real human-eye imagery.

## Locked source and privacy
Reuse the previously authenticated LPW participant-1 video, digest `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86`, reported 95 fps, 640x480, 2000 frames, and E002-578's ten deterministic nonoverlapping 19-frame **development-only** windows. Use the existing verified range-download, stream probe, native-frame packet and source-hash checks. No held-out participant, no source imagery, per-frame features, or window indices may be committed or uploaded. All source material and derived imagery must be deleted before job exit. Report only aggregate counts and quartiles.

## Frozen observables and perturbations
For each of 190 native PNG frames, grayscale by Pillow `convert('L')`. Central ROI: x in [160,480), y in [120,360). Compute:
- `D`: fraction of ROI pixels with grayscale intensity strictly below 80 (an intentionally uncalibrated threshold).
- `E`: mean absolute vertical-neighbor grayscale difference divided by 255 (a nonanatomical edge-energy proxy).

Apply independently to each source frame:
1. brightness offset +30 and -30, with clipping;
2. gamma mapping `round(255*(v/255)^0.7)` and `round(255*(v/255)^1.4)`;
3. Gaussian blur radius 2 pixels;
4. ROI shifted right by 24 pixels and down by 24 pixels, with unchanged dimensions.

All changes are **post-decoding counterfactual perturbations**, not actual camera recaptures. For each proxy and nuisance, compute `delta = abs(proxy_perturbed - proxy_native)`. For each source clip compute its native temporal range `R = max(proxy_native) - min(proxy_native)` over 19 frames. Mark a nuisance-dominance frame if `delta > R` (strict). Aggregate dominance counts across all 190 frames, plus max/median delta and baseline temporal-range median across 10 clips. A **necessary stability gate** fails if more than 19 of 190 frames are nuisance-dominated for either proxy under any one nuisance. Report all outcomes, including zero changes and zero temporal range. No tuning of ROI, threshold, perturbation magnitudes or gate after results.

## Independent and adversarial controls
Include deterministic synthetic grayscale arrays testing darkness under offset/gamma, edge-energy under blur, ROI translation and exact equality. Independently implement the core D/E formulas in a separate Python stdlib oracle (not importing the primary functions) on at least four frozen arrays and compare to the Pillow implementation. Require 190 native frames and source-hash verification; no silent fallback to synthetic when source acquisition fails. Fail CI on any source/integrity/replay error. A nuisance-stability failure is an **experiment result**, not a CI failure.

## Evidence and decision
Do not call either proxy an anatomical aperture, blink label or velocity bound. The study can **reject** unsupported proxy use but cannot establish anatomical accuracy even if the necessary stability gate passes. It cannot test E002-371's shutter-gap closure exclusion without independent anatomical labels, physical exposure/clock calibration and hard continuous-time velocity premises. Maintain `ABSTAIN_UNCALIBRATED` and production `BLOCKED`; PR #26 draft and unmerged. Hush PR #45 remains separate.
