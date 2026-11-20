# E002-742 | Held-out synthetic shutter-gap stress test (2026-11-11 UTC)

## Frozen generator and decision rules
Run `python research/observability/e002_742_heldout_shutter_stress.py` (stdlib only). Seeds 742, 743, 744 each generate 10,000 independent synthetic V-shaped eyelid aperture paths, endpoint aperture a uniform [0.2,1], physical inter-sample gap uniform [10,50] ms, trajectory speed uniform [12,55] aperture-units/s, and nominal timestamp gap underestimating physical gap by uniform [0,8] ms. A hidden closure occurs if a - speed*gap/2 <= 0. This is an intentionally adversarial instrument simulator, not a human physiological model.

Naive exclusion: 2a > 25 * nominal_gap (uncertified speed ceiling and incorrect timing). Robust exclusion: 2a > 55 * (nominal_gap + 0.008), conditional on the *synthetically imposed* speed bound and timing-error bound. All other cases abstain.

## Locally executed results
| seed | hidden | naive false exclusions | robust false exclusions | robust exclusions | robust abstentions |
|---|---:|---:|---:|---:|---:|
| 742 | 3759 | 2187 | 0 | 2198 | 7802 |
| 743 | 3816 | 2171 | 0 | 2231 | 7769 |
| 744 | 3732 | 2164 | 0 | 2162 | 7838 |

The robust zero-failure result follows from the assumed hard bounds, not from empirical discovery. The naive failure rate is specific to this deliberately synthetic generator and cannot estimate human error rates.

## Falsification and product gate
This tests unseen random draws with a frozen classifier, not unseen acquisition conditions. Actual exposure integration, RGB-to-aperture calibration, row timing, blur, gaze, geometry, glasses, missingness and real velocity-tail uncertainty remain untested here. A certified physiological ceiling has not been obtained. **No production closure exclusion is authorized.** Maintain `ABSTAIN_UNCALIBRATED` and release `BLOCKED`. Next decisive step: synchronized instrument acquisition or participant-disjoint high-speed human recordings with reference-label uncertainty, nuisance-stratified falsification and independently frozen calibration.
