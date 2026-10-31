# E002-529 | A certified speed ceiling does not certify reference-camera closure sensitivity

Date: 2026-10-29. Primary E002-371 scientific kernel, existing branch and draft PR #26. [Frozen protocol](E002_529_FROZEN.md) committed at `dfefd367e195650bd7cddc9c33bbaaf832b65885` **before** construction and tests.

**Evidence tier:** exact synthetic scalar counterexample with an independently implemented arithmetic replay. This is **not** a human blink measurement, physiological speed calibration, measured camera response, or a new general mathematical theorem.

## The invalid inference

E002-528's strict full-exposure opportunity `clamp((d-e-2u)/P,0,1)` requires `d` to be the duration **continuously below the anatomical closure threshold**. E002-371's speed ceiling and two open endpoints constrain the minimum time to *descend to the threshold and ascend back*, but they do **not** lower-bound how long the aperture stays below the threshold. Substituting the whole-excursion time for `d` can manufacture a false high-speed reference-sensitivity guarantee.

For a normalized continuous aperture `a(t)`, open endpoints `a(0)=a(H)=b`, threshold `0<c<b<=1`, and Lipschitz ceiling `|a(t)-a(s)|<=V|t-s|`, every strict below-c excursion requires `H>2(b-c)/V`. But **for every sufficiently small epsilon>0**, whenever that strict gap condition holds, a piecewise-linear trajectory exists whose total time with `a<c` is exactly `epsilon`.

Construct it by descending at speed `V` to `c-h`, dwelling there for `epsilon/2`, and ascending at speed `V`, where `h=V epsilon/4`. The threshold crossings occur `h/V` before and after the plateau, so total below-threshold time is `epsilon/2+2h/V=epsilon`. The full excursion lasts `2(b-c)/V+epsilon`. Center it inside the blind gap. This construction is continuous, bounded in [0,1], and globally V-Lipschitz.

At the critical equality `H=2(b-c)/V`, a trajectory may touch `c` at a single instant (zero-duration event under a <=c definition), but cannot have positive below-c dwell. Thus the result does not contradict the E002-371 exclusion boundary; it exposes a **different observable**.

## Exact preregistered synthetic counterexample

All parameters are hypothetical. No human eyelid-speed ceiling of 60/s has been certified.

| Quantity | Exact value | Interpretation |
| --- | --- | --- |
| Open aperture `b`; closure threshold `c` | 1; 1/5 | Normalized scalar |
| Speed ceiling `V` | 60/s | Hypothetical |
| Ordinary-camera blind gap `H` | 1/30 s | 33.333 ms |
| Minimum whole excursion | 2/75 s | 26.667 ms |
| Constructed whole excursion | 803/30000 s | 26.767 ms |
| Actual below-threshold dwell | 1/10000 s | **0.1 ms** |

| Reference-camera design | Correct strict full-exposure opportunity | Ideal positive overlap | Invalid whole-excursion substitution |
| --- | ---: | ---: | ---: |
| 240 Hz, 1-ms exposure, 0.1-ms edge uncertainty | **0%** | 26.4% | **100% full opportunity** |
| 1000 Hz, 0.5-ms exposure, zero uncertainty | **0%** | 60% | 100% full opportunity |

The incorrect substitution would claim certain full-exposure opportunity in a case where **no phase permits a full exposure inside the actual 0.1-ms below-threshold interval**. Even ideal positive exposure overlap does not guarantee a threshold witness after exposure integration, photometric noise, blur or cross-camera transport.

Held-out construction with 0.01-ms below-threshold dwell also remains V-Lipschitz. A hypothetical 10,000-Hz reference with 0.01-ms exposure has **0% strict full-exposure opportunity** and 20% ideal overlap for that event. For any finite positive exposure duration, epsilon can be chosen smaller still.

## Verification and limitations

- [Vector schematic of excursion versus closure dwell](E002_529_SPEED_DWELL.svg). The inset is magnified and is not a measured trace.
- [Exact-rational construction and independent piecewise dwell integrator](e002_529_dwell_counterexample.py).
- [18 adversarial Python test methods](test_e002_529_dwell_counterexample.py): endpoints, Lipschitz slopes, strict threshold duration, frozen and held-out cameras, exact phase grid, critical-gap refusal, invalid inputs, and fail-closed product claims.
- [Independent Node.js BigInt replay](e002_529_independent_replay.cjs) checks rational excursion and crossing durations, camera probabilities, invalid substitution, held-out 10,000-Hz case and 10,000 reference phases without importing Python code.
- [Dedicated hosted CI](../../.github/workflows/e002_529_speed_dwell.yml). **Hosted completion must be checked separately; passing source inspection or committing tests is not a CI pass.**

This counterexample applies to **continuous scalar threshold closure**, not a particular anatomical blink definition. A validated minimum sustained dwell or an independently calibrated quantitative partial-exposure witness may still provide sensitivity under additional assumptions. It does not imply that actual human eyelids exhibit 0.1-ms closures. The point is that the speed premise alone does not rule them out.

## Direct study and product decision

**Reject** the shortcut `d_min = 2(b-c)/V` in reference-camera sensitivity calculations. In the prospective study, define separately (a) threshold crossing, (b) continuous below-threshold dwell, and (c) whole excursion. A reference-camera *absence* is never a verified negative for arbitrary threshold crossing merely because the camera FPS exceeds the inverse whole-excursion time. For quantitative partial-exposure witnesses, require E002-520/522's independently calibrated response and nuisance assumptions; do not silently substitute full-exposure opportunities.

The next decisive work is two genuinely independent blinded S01 anatomical reviews and independently authenticated optical shutter/clock measurements, followed by participant-disjoint physical predictions. **No more synthetic dwell-bound refinements without new physical or human data.** E002-529 does not change any production measurement.

Human anatomical ratings **0**; physical shutter/clock calibrations **0**; certified continuous-time human velocity bounds **0**; held-out physical predictions **0**. Lucent `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush draft PR #45 remains separate and unchanged.


## Hosted independent verification (2026-10-29)

[GitHub Actions run 40887066293](https://github.com/sushxnthd/lucent/actions/runs/40887066293) completed with **success**. The `exact-replay` job independently reports **success** for all three substantive steps: 18 Python adversarial test methods, Node.js BigInt replay, and research-only CLI JSON assertions. This verifies the exact conditional scalar construction and executable checks, **not** any camera or human measurement. The frozen prediction and original pending language above are preserved as historical provenance. No release gate changed.
