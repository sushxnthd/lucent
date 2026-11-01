# E002-581 | Authentic LPW pupil-label order: strong temporal regularity, not eyelid evidence

**Executed:** 2026-11-01. **Kernel:** E002-371. **Protocol:** [E002_581_FROZEN.md](E002_581_FROZEN.md), frozen before the executable and source access. **Hosted verification:** [GitHub Actions #41269895334](https://github.com/sushxnthd/lucent/actions/runs/41269895334), **completed successfully** at 2026-11-01 03:40 UTC. **Code:** [e002_581_lpw_label_information.py](e002_581_lpw_label_information.py). **Machine-readable evidence:** [E002_581_AGGREGATE.json](E002_581_AGGREGATE.json).

## Verified empirical observation

The hosted job retrieved and CRC-checked the original investigators' `LPW/1/1.txt` member from the official LPW archive, requiring SHA-256 `12f60068317a341809babb7c2cbce90b8ba299ad877d75186687b0d521f6d5d2`. This is a **development-participant** recording with 2,000 pupil-center annotation rows, **not eyelid aperture**. The corresponding source video was authenticated in E002-577/578, but not reverified here. The nominal 95-fps source rate is **not a measured shutter exposure or calibrated timebase**.

| Frozen statistic | Observed | Within-50-increment shuffled null (499 replicates) |
|---|---:|---|
| Exact-linear second-difference junctions, including stationary | 1,561 / 1,998 | Not a preregistered null endpoint |
| **Moving** exact-linear junctions (both adjacent displacements >=0.1 px/frame; acceleration <=1e-6 px) | **1,528 / 1,998 (76.48%)** | Median **191**, p95 **213**, maximum **234** |
| Runs of >=3 consecutive moving junctions | **354** | Not a preregistered null endpoint |
| Longest moving-junction run | **14** | Median **3**, p95 **5**, maximum **7** |
| Add-one upper-tail randomization probability | **0.002** for moving count; **0.002** for longest run | 499 prespecified permutations, minimum attainable value 1/500 |

The observed moving-junction count is **8.0 times** the median of the frozen local-order permutation control. The two 0.002 tail probabilities are descriptive Monte Carlo randomization results under the **specified within-block exchangeability construction**, not independently calibrated physiological p-values or a causal test of the investigators' annotation pipeline. Both statistics use the same source recording and null permutations and are not independent replications.

The high exact-linear fraction is not explained solely by stationary labels: 1,528 of 1,561 exact-linear junctions meet the moving threshold. This provides direct empirical evidence of unusually long *piecewise constant-velocity structure in the provided annotation sequence* relative to the prespecified local-order control. It **does not prove interpolation**. Quantization, annotation smoothing, repeated displacements, assisted labeling and actual gaze trajectories remain competing explanations. The control deliberately preserves each block's two-dimensional displacement-vector multiset, but does not preserve temporal autocorrelation or a physiological trajectory model. Its p-values therefore cannot identify a mechanism.

## Verification and limits

The hosted job passed the E002-580 source/CRC and negative-control checks, then the E002-581 self-tests for stationary-vs-moving separation, exact moving tracks, kinks, tiny movement, coordinate translation and rotation, fixed-seed determinism, permutation multiset preservation and malformed inputs. The E002-581 authentic source execution emitted aggregate JSON only; no frame imagery, raw annotation track or participant-level outputs were published.

This result changes an **evidence-eligibility rule**, not the physiological boundary: high acquisition frame rate plus dense investigator pupil-center labels **cannot by itself be treated as independent frame-by-frame eyelid-motion measurement**. The pupil-center channel must be excluded from certification of hidden closures, eyelid velocity, blink counts, PERCLOS, fatigue and shutter timing. The negative E002-580 alias result is not evidence of no hidden blinks.

**Independent anatomical human rater pairs: 0. Calibrated physical shutter/photodiode captures: 0. Certified continuous-time eyelid-speed ceilings: 0. Held-out physical closure predictions: 0.** No held-out LPW participant was used. E002-371 remains a conditional mathematical observability result, not a validated physiological law.

## Next decisive experiment and product decision

Stop annotation archaeology. Use the existing E002-573/574/575/576/578 source-bound, blinded native-frame review packets with **two genuinely independent human raters**; independently justify strictly positive iris/geometry uncertainty before interpreting OPEN/CLOSED classifications. Then conduct E002-567 synchronized physical camera/photodiode exposures, measure the exposure and clock uncertainties, estimate eyelid velocity independently, preregister ordinary-rate hidden-closure predictions and test held-out physical sequences. If independent human raters or calibrated hardware are unavailable, report that as the binding bottleneck rather than fabricate labels or extrapolate pupil-center observations.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. No physiological blink, PERCLOS, fatigue, velocity or shutter-exclusion claims. **Hush:** no change in this primary run.
