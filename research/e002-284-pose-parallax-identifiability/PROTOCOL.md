# E002-284 | Pose-parallax identifiability, 2026-10-18

## Ten-field active kernel
1. **Signal/reference:** face-scale-normalized RGB upper/lower eyelid landmark separation vs synchronized high-speed same-eye anatomical eyelid aperture; only synthetic signals evaluated.
2. **Frontier:** 2D eye-aspect-ratio blink detection (Soukupova & Cech 2016); Culemann et al. (2026) report gaze-orientation confounds; Wolter & Berrio Perez (2026) introduce 3D eyelid-angle metric. The simple geometric bound is not novel.
3. **Scalar metric:** worst-case closure separation margin delta-2B.
4. **Strongest nuisance:** out-of-face-plane depth of lid landmarks under head pitch, plus bounded localization noise.
5. **Generative model:** u_t=h_t*cos(theta_t)+z_t*sin(theta_t)+e_t, |z_t|<=Z, |e_t|<=eps, exact head pitch, rigid face scale, orthographic imaging, free initial h0.
6. **Falsification:** produce exactly identical two-frame projections from a no-blink history and a delta-closure history; independent 16-vertex enumeration; later human calibration falsification.
7. **Boundary prediction:** B=Z(|tan(theta0)|+|tan(theta1)|)+eps(|sec(theta0)|+|sec(theta1)|); the two hypotheses are disjoint iff delta>2B. At 30 degrees, Z=.7 mm, eps=.05 mm equivalent, delta_critical=1.8475208614 mm; frontal=.2 mm. Values hypothetical.
8. **Untouched human test:** pending; freeze RGB landmark method, head pose, face scale, and independent depth/error bounds on calibration subjects; evaluate >=8 untouched people and >=2 consumer camera models, lighting/glasses/gaze holdouts, geometry-only, brightness-only, missingness-only, smoothness controls. Target >=90% admitted sensitivity, <=5% admitted false positive, >=50% coverage. None achieved.
9. **Publication threshold:** independent checker, prior-art differentiation, calibrated real camera nuisance, prospective unseen human boundary crossing, participant/device holdout and reproducibility.
10. **Product consequence:** reject claim that face-scale + pose correction alone yields invariant anatomical aperture. Conditionally admit only when independently calibrated delta_min>2B; otherwise abstain. No fatigue inference.

## Theorem and proof
Rectify v_t=u_t/cos(theta_t). Then v1-v0=(h1-h0)+n, where n is exactly [-B,B] because each independent bounded nuisance attains both extremes. The no-change and fixed closure-delta observation sets are [-B,B] and [-delta-B,-delta+B]. They are disjoint iff delta>2B. Because initial h0 is unrestricted, any common rectified difference permits matching both full two-frame projected measurements. Exact collision witnesses are in results.json. This is a conditional 2D-landmark measurement theorem, **not an impossibility for all RGB pixels**.

## Wildcard
If z0=z1 and head pitch fixed at 30 degrees, the critical delta reduces from 1.84752 mm to 0.23094 mm for the illustrative parameters. The depth-coherence assumption is untested and cannot be used to certify real blinks.

## Failure ledger
No human data, no empirical depth/landmark-error bounds, no device holdout, no real camera shutter model, no proof of field-level novelty. Head pitch and eye-in-head gaze are distinct mechanisms. Exact head pose, orthographic projection, independent bounded errors and free initial aperture are essential assumptions.

## Prior art
- Soukupova & Cech (2016): https://cmp.felk.cvut.cz/ftp/articles/cech/Soukupova-TR-2016-05.pdf
- Al-gawwam & Benaissa (2018): https://doi.org/10.3390/info9040093
- Culemann et al. (2026-03-20), 17 people/2306 blinks, raw videos unavailable: https://doi.org/10.3758/s13428-026-02984-4
- Wolter & Berrio Perez (2026), 3D eyelid angle: https://doi.org/10.1109/IV66570.2026.11623903
