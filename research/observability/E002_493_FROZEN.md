# E002-493 | Frozen real-human nuisance stress test of the E002-491 motion screen

Frozen 2026-10-28 **before** running any transformed S01 imagery. Primary E002-371 validation track. This is an adversarial test of a *screening proxy*, **not** anatomical blink detection, calibrated camera time, or E002-371 physical validation.

## Inputs and protection
- Checksum-verified Guttmann-Flury S01.zip, MD5 `fb56109542a13aa7879778833fe4cbaa`, original `*_phantom.avi`; 12,000 native-frame limit. Reuse the exact **20 precommitted E002-492 review clips**: 13 native frames each, one E002-491 localized-motion candidate at native index 5356 and 19 SHA256-selected controls. No new data-dependent clip selection.
- Decode 260 selected frames in native order, grayscale 64x64 area downsampling. Do not use container timestamps to assign physical time. Reject checksum, geometry, frame count, codec or decoder errors. All raw frames remain ephemeral in the GitHub Actions job; **never** upload images, crops, human landmarks, annotations, or individual image arrays.
- Use the **unchanged** E002-491 `motion_pair` threshold and nuisance gates. Baseline pairs are 12 per clip, never bridge clips.

## Frozen interventions
All transforms operate on every frame **before** the unchanged pairwise screen, without retuning its threshold:
1. `baseline`: original decoded frames.
2. `brightness_plus8`: add +8 grayscale units with saturation (illumination nuisance).
3. `contrast_90pct`: transform `128 + 0.9*(pixel-128)` with rounding/clipping (contrast nuisance).
4. `blur_3x3`: replicate-border 3x3 spatial box blur (optical blur nuisance).
5. `alternating_jitter_1px`: translate alternate frames by +1/-1 horizontal pixel with edge replication (camera/gaze registration nuisance).
6. `stride2`: select within each clip frames j=0,2,...12 and apply unchanged screen to 6 adjacent pairs (sampling nuisance).

For each condition publish only: 20 clip count, total analyzed pairs, nuisance abstentions, eligible pairs, total proxy candidates, candidate-clip candidate count, control-clip candidate count, and candidate-clip positive/negative. The candidate-clip label is already published and is **not** a human closure label. No anatomical closure rate or physical velocity is inferred.

## Falsifiers and precommitted interpretation
- Confirm baseline contains at least one proxy candidate in the frozen candidate clip, and none in controls. If not, report baseline non-reproduction and stop interpreting intervention differences.
- If brightness, contrast or blur removes **all** candidate-clip detections, mark **FAIL** for that perturbation (sensitivity to nuisance); if any creates a new control-clip detection, mark **FAIL** (spurious activation). A changed candidate count is reported even if the boolean remains stable.
- If alternating jitter produces any new control-clip candidate, mark **FAIL** for registration robustness. If it removes all candidate-clip detections, also mark **FAIL**.
- If stride2 removes all candidate-clip detections, mark **FAIL** for temporal subsampling; otherwise mark **SURVIVES_THIS_FIXTURE_ONLY**. No broad sensitivity claim from one event.
- Mark any condition with <80% eligible pairs **FAIL** for nuisance abstention coverage. Preserve every negative outcome and any experimental failure; do not adjust thresholds or select different controls post hoc.
- A pass means only survival on this one authentic S01 fixture. A failure kills use of this motion proxy as a reliable event selector under that nuisance; **neither** outcome validates E002-371 or authorizes blink/PERCLOS/fatigue claims.

## Evidence tier / enforcement
`AUTHENTIC_HUMAN_IMAGE_PROXY_NUISANCE_TEST_ONLY`. Physical camera timing, exposure duration, eyelid geometry, anatomical reference and independent dual-rater labels remain unauthenticated. Every outcome: `anatomical_closure_labels=0`, `physical_hidden_closure_certified=false`, `product=ABSTAIN_UNCALIBRATED`, `release=BLOCKED`. Preserve S21-S31 held-out anatomy and Hush's independent branch.
