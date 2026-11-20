# E002-547 FROZEN | Exposure integration can erase a high-rate closure witness

Date: 2026-10-30. Primary E002-371 human-validation kernel. Frozen **before** implementing E002-547 numerical tests. Evidence tier: exact synthetic reference-instrument falsification, not human observation.

## Question
Does E002-546's ideal instantaneous-sample detection probability remain valid when the *reference* camera reports an exposure-averaged aperture? Test a linear boxcar observation that is deliberately more favorable than a real nonlinear ISP/segmentation pipeline.

## Fixed model
Use the unchanged E002-546 triangular continuous-time trajectory: open normalized aperture b=9/10, closure threshold c=1/5, duration T=1/100 s, apex at t=T/2, speed V=180/s. Extend aperture to b outside [0,T]. The reference observation at center time t is M_L(t)=(1/L) integral_{t-L/2}^{t+L/2} a(u) du, with shutter duration L>0, no noise, no geometry error, and ideal radiometric linearity. A reference-positive observation means M_L(t)<=c; this is an optimistic mathematical proxy, **not** an anatomical label.

For L<=T and exposures centered near the apex with their support inside the triangular segment, the minimum integrated aperture is V*L/4. Therefore the critical shutter duration for *any* integrated positive is L*=4c/V=1/225 s (4.444... ms). At L>=L*, a threshold-positive exposure is impossible except equality at exactly L*, which has zero probability under a continuous random phase.

For L=1/250 s (4 ms), the positive center-time interval is symmetric about the apex with half-width sqrt(L*(c/V-L/4))=1/1500 s, hence total width 1/750 s. Under an independent uniform sample phase over 1/f, detection probability is min(1, f/750). Prespecify 200 fps -> 4/15 and 240 fps -> 8/25. At 200 fps with L=1/200 s (5 ms), zero. At 100 fps with L=1/100 s (10 ms), zero. For comparison the instantaneous probabilities from E002-546 are 4/9, 8/15, and 2/9 respectively.

## Falsification / adversarial checks
1. Implement exact piecewise-linear integration using rational arithmetic (not numerical quadrature) and check symmetry, nonnegative aperture, endpoint limits, and min at the apex.
2. Independently implement a different integral calculation in JavaScript using the area of triangular aperture deficit, and test 4 ms, 5 ms, and 10 ms centered exposures.
3. Verify phase-positive intervals by exact rational evaluation at the analytic 4-ms boundaries and just outside them; check 200/240 fps probabilities.
4. Add a numerical quadrature check at non-boundary positions, without using it to tune the analytic thresholds.
5. Assert that no reference-negative can be promoted to a continuous-time no-closure label, and that reference-positive means only a model-dependent witnessed measurement, not independently certified anatomy.

## Product consequence
If exposure integration, shutter duration, or anatomical transfer is unverified, high-speed *negative* labels are REFERENCE_NEGATIVE_UNCERTIFIED and cannot validate E002-371 exclusions. Do not infer 200-Hz reference sensitivity from fps alone. No physiology/clinical product claim; Lucent remains ABSTAIN_UNCALIBRATED and release BLOCKED. No Hush writes.