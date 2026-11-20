# E002-609 | Cross-camera existential closure witness and prospective falsification bridge

Date: 2026-11-02. Parent: E002-371, E002-608. Evidence tier: **synthetic interval instrument + preregistered human/physical protocol, not measured human evidence**.

[Protocol frozen before implementation](E002_609_FROZEN.md), commit `54048ffd3d26ef1a23f8de5b64b39b2120d43796`.

## Distinct research consequence

A reference camera's frame is not an instantaneous anatomical observation. Nevertheless, **if** a separately calibrated reference image is proven to be a *linear exposure average* of anatomical aperture with conservative upper bound `m_hi <= tau`, at least one time within that exposure must have anatomical aperture `<=tau`. If the entire uncertain reference exposure lies **strictly inside** the independently bounded ordinary-camera unexposed gap, this is a genuine conditional *existential* hidden-closure witness. It does **not** imply closure throughout the reference exposure.

A witness conflicts with an ordinary-camera `MODEL_EXCLUDE_CONDITIONAL` prediction sealed before reference adjudication. The conflict challenges the **joint physical calibration/model assumptions**; it does not by itself falsify the E002-371/E002-421/422 mathematical laws. Reference overlap or touching the gap boundary, ambiguous clock, uncalibrated anatomical linearity, generic blink labels, nuisance flags or missing evidence => abstention. A non-witness does not prove absence. This is a practical falsification bridge, not a new theorem or human finding.

## Executed synthetic checks

- 11 local Python adversarial tests passed (strict temporal containment, threshold equality, uncertain overlap, all eleven nuisances, missing attestations/digests, invalid numeric input, uncertainty monotonicity, fail-closed product state).
- Independent Node.js BigInt rational arithmetic passed nine explicit interval/threshold controls plus a decimal precision check, without importing Python.
- Synthetic ordinary dark gap `(0,10) ms`, reference exposure `[3,5] ms`, upper calibrated aperture `0.15`, threshold `0.20`, predeclared EXCLUDE => `WITNESS_CONTRADICTS_CONDITIONAL_EXCLUSION` under supplied hypothetical premises.
- The same reference with an ABSTAIN prediction => `HIDDEN_CLOSURE_WITNESS_CONDITIONAL`; reference `[9,11]` or boundary-touching exposures => abstain; upper aperture `0.21` => `NO_REFERENCE_WITNESS`, never proof of no blink.
- All outcomes remain `ABSTAIN_UNCALIBRATED` / `BLOCKED`. Input flags and SHA-256 strings are syntactic references, **not physical authentication**.

[Executable](e002_609_cross_camera_witness.py) · [Python tests](test_e002_609_cross_camera_witness.py) · [Independent Node replay](e002_609_independent.cjs) · [CI workflow](../../.github/workflows/e002_609_cross_camera_witness.yml). Hosted workflow status was **not confirmed** at report time.

## Source-access limit, no more dataset archaeology

Two bounded public source searches on 2026-11-02 identified Gupta, Lazarus and Panda (2020), DOI https://doi.org/10.1049/ccs.2019.0014, reporting a 58-participant video database recorded at 30, 60 and 120 fps, including lighting and spectacle variation; the authors state the full database is available **upon request**, with samples referenced. No 120-fps human source video, independently calibrated shutter data, or continuous-time anatomical closure annotation was obtained. Other sources already assessed include the Mendeley 100–110-fps eye-blink dataset (E002-605, download HTTP 401), and licensed Silesian5. Do not count this literature screening as validation or spend further runs repeating access attempts.

## Next actual physical/human study

1. Obtain ethics/privacy review and informed consent. Record synchronized high-speed reference (prefer >=240 fps) and ordinary (~30 fps) eye video, plus external LED/photodiode clock and shutter calibration, linear-aperture transfer and geometry; do not infer physical shutter from nominal fps or codec timestamps.
2. Two independent blinded raters annotate high-rate eyelid margins and uncertainties. Establish upper **linear aperture exposure-average** bounds with independently reviewed physical transfer; ordinary image brightness, a generic closed-eye label, or sampled speed maximum is insufficient.
3. Seal per-gap ordinary-camera E002-608 predictions and their independent evidence before unblinding held-out high-rate reference measurements. Use participant-disjoint holdout and separate natural/instructed blink strata, varying lighting, gaze, glasses, blur and missingness.
4. Run E002-609 locally on deidentified per-gap manifests. Report number of eligible gaps, witnesses, contradictions, uncertain/abstained gaps, and participant-clustered outcomes; any contradiction forces physical premise investigation. Keep all person-level videos and ratings private.
5. Without authenticated clock, shutter, linear-anatomical transfer, independent physiological velocity ceiling and actual human labels, the physical E002-371 validation remains **unperformed**.

**Current empirical counts:** 0 new human anatomical ratings; 0 actual physical shutter captures; 0 independent hard human velocity ceilings; 0 held-out physical predictions. **Lucent product:** `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush PR #45 was not modified in this primary-science run.
