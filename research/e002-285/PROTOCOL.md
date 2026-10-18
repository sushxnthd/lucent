# E002-285 | Temporal depth-coherence observability, 2026-10-18

## Active ten-field measurement kernel
1. **Signal/reference:** face-scale-normalized upper/lower eyelid landmark separation in ordinary RGB, rectified for head pitch, versus synchronized high-speed same-eye anatomical lid aperture. **This run is synthetic; no paired human evaluation.**
2. **Literature frontier:** Soukupova & Cech (2016) landmark blink detection; Wolter et al. (2025/2026) 3D eyelid-angle methods; Culemann et al. (2026) eye-in-head vertical gaze confounds. Bounded-error inverse-problem geometry is established.
3. **Scalar observability:** margin M=delta-2B, where B=S+eps(|sec(theta0)|+|sec(theta1)|), S=max|z1 tan(theta1)-z0 tan(theta0)| subject to |z0|,|z1|<=Z and |z1-z0|<=D.
4. **Strongest confound:** temporal changes in upper/lower eyelid landmark depth, especially when head pitch changes. Gaze biomechanics and landmark occlusion are additional unmodeled confounds.
5. **Generative model:** u_t=h_t cos(theta_t)+z_t sin(theta_t)+e_t; |e_t|<=eps; known head pitch, rigid face scale, orthographic projection; free initial h. Hypotheses: h1-h0=0 versus h1-h0=-delta.
6. **Falsification:** for delta<=2B, construct distinct closure and no-closure histories with identical two-frame observations; check independent LP and vertex intersections. Later: frozen human reference errors crossing the predicted boundary.
7. **Boundary prediction:** the hypotheses are disjoint iff delta>2B. Illustrative Z=.7mm, eps=.05mm, D=.08mm: at fixed 30deg, critical closure=.323316mm; at 30deg to 40deg, .704836mm. D=1.4mm at fixed 30deg gives 1.847521mm. All parameters are hypothetical.
8. **Untouched human test:** freeze RGB landmark/pose/scale and independent Z,D,eps calibration before looking at >=8 untouched participants across >=2 camera models, varying gaze, illumination and glasses; synchronized high-speed eyelid aperture reference; predict stable-pose pass vs pose-transition failure. Controls: geometry-only, brightness-only, missingness-only, smoothness-only. Prospective product targets: admitted sensitivity >=90%, false-positive <=5%, coverage >=50%. Not achieved.
9. **Publication threshold:** independent checker, prior-art distinction, real-device calibration, mechanism-predicted human boundary crossing, participant/device holdouts, reproducibility and meaningful product consequence.
10. **Product consequence:** conditionally permit pose-stable geometric blink-change certification only with independently calibrated depth-coherence and landmark uncertainty; otherwise abstain. No 5-second fatigue inference.

## Proof (two scalar observations only)
Rectification gives v_t=u_t/cos(theta_t)=h_t+z_t tan(theta_t)+e_t sec(theta_t). The nuisance difference n ranges exactly over [-B,B], because the bounded coherent-depth polytope is convex, centrally symmetric and its linear support is attained at vertices. The no-change and fixed-closure intervals are [-B,B] and [-delta-B,-delta+B]; they are disjoint exactly when delta>2B, with equality ambiguous. The free initial aperture permits matching the first observation too. This is **not** an all-RGB impossibility theorem.

For d=min(D,2Z), the depth-polytope vertices are (Z,Z),(-Z,-Z),(Z,Z-d),(Z-d,Z),(-Z,-Z+d),(-Z+d,-Z). The independent checker generates them instead by intersecting constraint lines. Exact collisions and the untouched *synthetic* holdout are preserved. A 250-case random LP check and three deliberate mutation rejections passed locally.

## Failed scientific gates and stop rule
No real depth-coherence bound D; no paired human evidence; no gaze or glasses calibration; no device holdout; no field-level novelty. **Do not use 0.08mm as a real physiological bound.** Monocular-network-estimated 3D landmarks are not an independent depth reference. The next run must obtain real calibration or reformulate around directly observable image-plane events, not add another arbitrary Gaussian/synthetic variant. If calibration cannot bound D, this positive kernel is killed for deployment, while the impossibility result remains.

## Wildcard
Under fixed h,z and known head pitch at -30/+30 degrees, a two-pose open-eye calibration estimates z with <=0.1mm worst-case error for eps=.05mm. This fails if gaze/aperture change, adds user friction, and does not certify blink-time D; not promoted.
