# E002-550 FROZEN | Independent 400-Hz eyelid kinematics: hard-speed certification challenge

Frozen 2026-10-30 before implementation or any restricted human data. Existing Lucent E002-371 kernel, branch `research/observability-human-boundary`, draft PR #26. **No new human records accessed.**

## Why this is the next experiment
A newly released primary source provides hardware-synchronized **400-frames/s three-dimensional eyelid-margin marker trajectories** and intramuscular EMG from **eight adults** performing five eyelid behaviors. The FaceBase release is dated 2026-09-01; raw human records require controlled-access authorization and not-for-profit use. The associated PNAS 2025 paper reports distinct two-dimensional kinematics across behaviors. The source is **not** an ordinary webcam, and 400 fps alone cannot authenticate a continuous-time maximum speed.

Sources: https://doi.org/10.25550/88-28BJ ; https://doi.org/10.1073/pnas.2508058122 ; https://trackhub.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/

## Frozen falsifiable question
Can a **hard**, externally justified continuous-time normalized-aperture speed ceiling be transferred across subjects and spontaneous, voluntary, reflexive, soft, and forced closure, after head geometry, marker localization, missingness, behavior, exposure and clock uncertainty? Or do subject/behavior shifts make the proposed E002-371 exclusion product abstain?

1. Partition all eight original participant IDs **before examining trajectories** using SHA-256 of `lucent-e002-550-v1|<source-original-id>`, lexicographically sorted by digest; first four exploratory, remaining four held-out. Keep all behaviors, trials and sessions for each person together. Preserve original IDs only in private workspace; publish aggregate split sizes and hashed precommit.
2. Establish a facial-marker rigid coordinate system. For each paired upper/lower margin marker define a **local** vertical gap and a fixed, independently measured normalization length. Do not substitute a moving pupil/iris denominator or collapse distinct 2D paths into a global scalar blink label. Propagate localization, geometry and occlusion uncertainty. Any unpaired, occluded or swapped marker => abstain for that interval.
3. Independently certify an upper bound `A` on **continuous-time scalar acceleration** and pointwise aperture error `e`, and a per-timestamp error `u`. Do not infer a hard `A` from the same sampled trace. For adjacent observations `y_i`, nominal time separation `d_i>2u`, the conditional conservative velocity bound on the covered interval is
   `U_i = (abs(y_(i+1)-y_i)+2e)/(d_i-2u) + A*(d_i+2u)/2`.
   For complete contiguous coverage, `V_cert=max_i U_i`. The first term bounds true secant velocity; the second bounds instantaneous departure from the secant under a hard acceleration bound. Without independently certified finite `A,e,u`, return `ABSTAIN_NO_HARD_SPEED_CERTIFICATE`. Finite differences alone are lower-bound observations, not hard velocity ceilings.
4. Freeze an ordinary-camera counterfactual: 30 Hz, 10-ms exposure, 0.2 normalized-aperture closure threshold; use independently calibrated exposure/transfer intervals and E002-540, never frame means as point endpoints. Only use E002-371's exclusion when the speed/geometry/clock certificates and all nuisance checks hold.
5. On exploratory subjects only, specify normalization and uncertainty bounds. Lock these plus predicted held-out excluded/abstained gaps before viewing held-out trajectories. Primary held-out endpoint: independently witnessed closure during a predeclared excluded blind gap; any authenticated witness kills that stratum. Negative high-rate samples remain censored unless separate continuous-time sensitivity is certified.
6. Report all five behaviors, gaze/geometry/missingness/blur/illumination/occlusion strata, subjects, failures and abstentions. Report 2D motion not captured by scalar gap as a **scope limit**, not a discovery of hidden closure. Do not claim population 1% risk from four held-out people (see E002-509).

## Precommitted software kill tests (no human data)
- `A` absent, sample gap missing, unbounded clock or localization error => abstain.
- Even perfectly flat 400-Hz samples do **not** imply finite continuous-time speed without hard `A`; a narrow between-sample spike can have arbitrary slope.
- With externally stipulated hard `A,e,u`, a smooth analytic trajectory's true instantaneous velocity must lie below the computed `V_cert`; increased uncertainty must never decrease `V_cert`.
- Behavior-specific marker coordinate changes and unverified anatomical transfer must not be promoted to a universal aperture-speed certificate.

**Evidence gate:** The current run may publish a reproducible conditional calculator and synthetic tests only. FaceBase authorization, raw 400-Hz kinematics, independent physical acceleration/error certification and participant-disjoint tests are **not** obtained. Lucent `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. No Hush branch changes.
