# E002-597 | Authenticated human-eye image nuisance falsification: observed negative result

Date: 2026-11-02. Primary E002-371 research kernel. The [frozen prospective protocol](E002_597_FROZEN.md) preceded source execution. The [aggregate JSON](E002_597_AGGREGATE.json) is reproduced from the successful [hosted workflow #41353572997](https://github.com/sushxnthd/lucent/actions/runs/41353572997), job `124988756591`, at exact workflow head `6820dd55bc772e3f6b64306f7953410b889305f3`. The original protocol was frozen at `0227b2b`. This is **real human development imagery**, not anatomical ground truth or prospective physical validation.

## Question and preregistered decision

Do two deliberately uncalibrated image proxies survive plausible imaging nuisances strongly enough to be candidates for eyelid-aperture measurement? Source: 190 authenticated frames from 10 nonoverlapping 19-frame windows of LPW participant-1 video (reported 95 fps, 640×480, 2,000 total frames; source SHA-256 `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86`). Fixed central ROI: 320×240 pixels. Dark-pixel fraction uses grayscale intensity <80. Vertical-edge energy uses mean absolute vertical-neighbor grayscale difference divided by 255.

For each 19-frame window, define its native proxy temporal range `R=max(proxy)-min(proxy)`. Each perturbation dominates a frame when `abs(proxy_perturbed-proxy_native)>R`. The frozen necessary-stability criterion fails if **more than 19/190** frames are dominated for any nuisance. Perturbations are applied **after decoding**, not physical recaptures. This criterion is deliberately a necessary stress test, not a sufficient anatomical validity test.

## Empirical results (exact counts out of 190 frames)

| Frozen perturbation | Dark-pixel fraction dominated | Dark gate | Vertical-edge energy dominated | Edge gate |
|---|---:|---|---:|---|
| Brightness +30 | 181 | FAIL | 0 | PASS necessary only |
| Brightness -30 | 175 | FAIL | 0 | PASS necessary only |
| Gamma 0.7 | 182 | FAIL | 19 | PASS necessary only |
| Gamma 1.4 | 175 | FAIL | 0 | PASS necessary only |
| Gaussian blur radius 2 | 51 | FAIL | 184 | FAIL |
| ROI right 24 px | 137 | FAIL | 85 | FAIL |
| ROI down 24 px | 136 | FAIL | 80 | FAIL |
| Black obstruction, 25% ROI | 190 | FAIL | 76 | FAIL |
| White obstruction, 25% ROI | 139 | FAIL | 55 | FAIL |

The median native 19-frame temporal ranges were **0.01190104** (dark fraction) and **0.00193933** (edge energy). The dark proxy failed **9/9** nuisance conditions. The edge proxy failed **5/9**, particularly blur, translation and obstruction. A pass under the other four perturbations does not establish stability in general. The `19` count for gamma 0.7 is a pass because the frozen criterion is strictly greater than 19, not greater than or equal to 19.

**Decision:** Both observables fail the necessary gate and are rejected as *uncalibrated anatomical aperture or closure evidence* in Lucent. The result does not imply that no calibrated computer-vision observable can work; nor does it demonstrate an actual missed blink.

## Independent and execution checks

The hosted workflow completed successfully. Its self-test reported 4 frozen grayscale-array comparisons against an independently implemented standard-library oracle and 8 adversarial controls. The authentic-source job verified source hash, native-frame packet geometry and count, and no retention of video, images or owner mappings in the workflow workspace. The experiment's own nuisance failure is a scientific negative result, not a CI failure. The committed JSON preserves all nine nuisance conditions, including passing controls, with medians and maxima. This is implementation-level independent formula replay, **not** independent human annotation or independent physical acquisition.

## Limitations and threats to validity

1. Single development participant, 190 temporally correlated frames, ten deterministic windows. Frame counts are not independent biological sample sizes, and no confidence interval on a population failure rate is warranted.
2. Synthetic post-decoding brightness/gamma/blur/ROI/occlusion manipulations are not actual camera changes; severity is fixed by the frozen protocol, not estimated as a representative population distribution.
3. ROI and proxy definitions are deliberately naive. The experiment falsifies these specific uncalibrated observables under this test, not all feature engineering, tracking, anatomical segmentation or radiometric correction.
4. LPW's reported frame rate is not an independently certified physical shutter or timestamp. No anatomical eyelid-closure labels, independent rater pairs, velocity/acceleration ceilings or synchronized camera exposures were available.
5. The E002-371 shutter-gap theorem is neither validated nor falsified by this image-nuisance study. This result attacks a separate necessary link from pixels to anatomy.

## Direct product consequence and next experiment

**Reject** dark-pixel fraction and vertical-edge energy as standalone blink/closure/aperture evidence. **Abstain** on closure absence, fatigue and physiological risk inference unless independently calibrated anatomy, timing, exposure integration and conservative velocity/acceleration premises are supplied. Keep `ABSTAIN_UNCALIBRATED`, release `BLOCKED`, and PR #26 draft/unmerged.

Next decisive experiment: independently blinded human eyelid-aperture annotation on synchronized high-frame-rate and ordinary-camera recordings, with radiometric/exposure/clock calibration; prospectively freeze the E002-371 prediction for held-out subjects and evaluate nuisance-stratified false exclusions. If no such source exists, document the study acquisition and consent plan and do not substitute further proxy-only tests for physical evidence.

**Evidence tier:** `REAL_HUMAN_DEVELOPMENT_IMAGES_NONANATOMICAL_PROXY_ONLY`. **Hush:** separate PR #45 untouched.
