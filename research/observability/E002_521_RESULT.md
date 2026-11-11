# E002-521 | Exact exposure-mean-to-closure-time bound

Date: 2026-10-29. Primary E002-371 kernel. [Frozen protocol](E002_521_FROZEN.md) was committed before implementation (c719d35f; degenerate endpoint corrected b6af4fc9). **Evidence tier: mathematical implication, constructive sharpness and synthetic independent arithmetic, not physical or human validation.**

## Dimensionless law and proof

Let ordinary-camera aperture a(t) lie in [0,1]. Let a reference exposure E of actual duration w >= w_min > 0 be strictly inside an ordinary-camera guaranteed blind interior. Require independent calibration of **uniform linear temporal exposure weighting**, reference mean upper bound mean_E(a_r)<=U, and pointwise cross-camera transport a_o(t)<=K*a_r(t)+B, with K,B>=0. Freeze ordinary threshold 0<theta<1. Then mean_E(a_o)<=M:=K*U+B.

Let C={t in E: a_o(t)<=theta} and p=measure(C)/w. Since a_o>theta on the complement of C and a_o>=0 on C, mean_E(a_o)>=theta*(1-p). Consequently, for **M<theta**, p>=1-M/theta>0 and measure(C)>=w_min*(1-M/theta). No velocity bound is needed. The certified quantity is **total time at or below threshold in that one exposure**, not a contiguous blink, full blink, fatigue, PERCLOS, or absence of closure elsewhere.

The bound is sharp as an infimum over measurable [0,1] aperture functions without a derivative constraint: for epsilon>0 and theta+epsilon<=1, set a=0 for fraction p_epsilon=1-M/(theta+epsilon) and a=theta+epsilon otherwise. Its mean is exactly M, and p_epsilon approaches 1-M/theta from above. With a separate finite velocity cap the sharp bound may differ. At M=theta, threshold contact is implied but no **uniform** strictly positive duration bound follows. At M>theta, the observation is inconclusive.

## Frozen numerical reversal and independent replay

| Hypothetical | M | Conditional inference |
|---|---:|---|
| theta=.20, U=.19, K=1, B=0, w_min=8ms | .190 | p>=1/20; total closure >=2/5 ms |
| Same, K=1.2 | .228 | UNKNOWN |
| Same, U=.20 | .200 | contact-only; no positive uniform duration bound |

A separate Node.js BigInt rational implementation independently reproduced 1/20, 2/5 ms, the scale reversal, equality, and sharpness constructions: for epsilon=.01,.001,.0001,.00001 the closure fractions are 2/21, 11/201, 101/2001, 1001/20001, approaching 1/20. These are synthetic analytic checks, not camera measurements.

**Adversarial sensor counterexample:** If a nonuniform shutter puts all temporal weight into a tiny epsilon fraction of the nominal exposure, a=0 there and a=1 elsewhere gives weighted mean zero but only epsilon*w physical closure time. As epsilon approaches zero, no positive physical-time bound follows from the weighted mean without a calibrated temporal weighting kernel. Nonuniform integration, unmatched scanlines, uncalibrated clock/row timing, geometry, radiometry, native provenance or nuisance uncertainty require abstention.

## Empirical evidence gate and novelty limits

Two targeted high-rate human-data searches were performed before the fallback. Kwon et al. report 600-fps kinematics without downloadable participant-level trajectories in the accessible article ([DOI](https://doi.org/10.1098/rsif.2013.0227)). [EyeInfo](https://github.com/fabricionarcizo/eyeinfo) describes 150-fps raw eye data with timestamped features but requires authenticated Google Drive DVC access. The [2026 FaceBase release](https://trackhub.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/) has hardware-synchronized eyelid/EMG data but is restricted access. Existing S01 has unauthenticated timing and zero independent anatomical ratings. This is not a claim that no usable human data exist.

The bound is an elementary measure inequality, **not claimed as a new general theorem**. Its useful Lucent consequence is that a transported shutter-mean witness can establish conditional threshold contact or, with strict margin and independently calibrated uniform weighting, a conditional lower bound on total threshold-closure measure. It cannot be promoted to a full blink or no-hidden-blink claim. External calibration attestations cannot be authenticated by software booleans.

**Current physical evidence:** independent S01 ratings 0; authenticated shutter/clock captures 0; certified human continuous-time speed caps 0; participant-disjoint physical predictions 0. The next decisive experiment remains two genuine blinded S01 raters and independently clocked physical camera acquisition under the existing [E002-519 human study protocol](E002_519_HUMAN_STUDY_HANDOFF.md). Product ABSTAIN_UNCALIBRATED; release BLOCKED. Hush unchanged; PR remains draft and unmerged.
