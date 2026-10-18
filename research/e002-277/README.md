# E002-277: temporal-difference observability under aperture and photometric-bias coherence

Date: 2026-10-18. **Synthetic measurement model only. No human physiological result.**

## One active kernel (ten mandatory fields)
1. **Signal/reference:** two-frame or temporal RGB-derived, iris-normalized apparent pupil edge radius difference, compared prospectively against synchronized same-eye calibrated pupil-diameter changes. Here the reference is *known simulated* radius change, not a human eye tracker.
2. **Frontier:** E002-276 derived conditional aperture Fisher information under independent Gaussian edge noise. E002-266 showed optical drift can masquerade as anatomical change. Prior work documents gaze-angle pupil-size artefacts and corneal refraction (Petersch & Dierkes 2022, DOI 10.3758/s13428-021-01657-8; Hayes & Petrov 2016, DOI 10.3758/s13428-015-0588-x). This is standard linear-model information theory, not novel general mathematics.
3. **Scalar metric:** probability of absolute temporal radius-change error <= 1 pixel; target 75% (illustrative), with explicit admission coverage and held-out human waveform gates still required.
4. **Strongest nuisance:** time-varying common photometric edge offset b(t), including corneal-optics/gaze changes; angular aperture and correlated pixel errors.
5. **Generative model:** full RGB I_k=Q_k{G_k[B_k+M_k (PSF_k * H_k(T(r_k,c_k,s_k,m_k)))]}, exposure-integrated and sampled at k/f+delta_k. Conditional reduction after known iris scale, gaze/projective calibration and known contour angles: y_kj=r_k+c_x,k cos(theta_j)+c_y,k sin(theta_j)+b_k+epsilon_kj. Independent epsilon~N(0,sigma^2); calibrated b_k Gaussian with SD tau and cross-frame correlation phi. This reduction is NOT established for real RGB.
6. **Decisive falsification:** unchanged physical pupil with b_1-b_0 can exactly mimic a genuine change if b_k unrestricted. Synthetic counterexample gives identical observations for delta r=0.5 versus delta r=2.0.
7. **Mechanism prediction:** Var(delta r_hat)=2 sigma^2 [(X'X)^-1]_(r,r)+2 tau^2(1-phi). 75% within tolerance d requires variance <= d^2/[Phi^-1(0.875)]^2. At alpha=0.9 rad, n=60, sigma=0.5px, tau=1.2px, d=1px, phi >= 0.897676. For exponential bias coherence phi=exp(-dt/T), dt<=0.107946 T. The absolute radius variance is sigma^2[(X'X)^-1]_(r,r)+tau^2, so a stable bias can cancel in differences while preventing absolute measurement.
8. **Untouched human test:** NOT AVAILABLE. Predeclared synthetic holdouts: (alpha,phi)=(0.9,0.84),(0.9,0.96),(1.1,0.75),(1.1,0.9), each 12,000 simulations. Human protocol must freeze nuisance calibration on development participants, enforce RGB-only admission, and use independent reference clocks, participant/device/light/gaze/glasses holdouts and geometry/brightness/missingness/smoothness baselines.
9. **Publication threshold:** prior-art audit; calibrated real-image bias coherence; independent implementation; untouched human prediction of a boundary crossing or exact model-independent impossibility with explicit nuisance class. Not met.
10. **Product consequence:** prioritize *short-interval apparent change* as a candidate over absolute anatomical radius; accept only with independently calibrated bias coherence and angular information; otherwise abstain. No five-second fatigue score or physiological claim.

## Sharp conditional law and scope
Let v=sigma^2 [(X'X)^-1]_(0,0), where X_j=(1,cos theta_j,sin theta_j). For unbiased least-squares fits to each frame with common bias b_k, Var(r_hat_k-r_k)=v+tau^2. For two independent edge-noise frames, Cov(b_1,b_2)=tau^2 phi, and Var((r_hat_2-r_hat_1)-(r_2-r_1))=2v+2tau^2(1-phi). Both expressions are exact under the stated Gaussian model. If b_1 and b_2 are unrestricted unknown constants, the temporal radius difference is **not identifiable**. The probabilistic threshold is conditional on nuisance calibration, NOT a theorem about RGB video without such calibration.

## Results / independent verification
Four synthetic holdout predictions versus observed pass rates:
- alpha .90, phi .84: 70.238% predicted / 70.408% observed (fail)
- alpha .90, phi .96: 81.229% predicted / 80.892% observed (pass)
- alpha 1.10, phi .75: 70.445% predicted / 70.033% observed (fail)
- alpha 1.10, phi .90: 85.027% predicted / 84.667% observed (pass)
Independent Schur-complement checker verified 10 conditions and rejected 4 mutated results. These are *simulated* tests, not untouched human evaluation. The exact deterministic counterexample has zero observation difference.

## SCIENCE ledger
Conditional temporal difference precision law and deterministic nonidentifiability if optical/photometric drift is unrestricted. Not an original general theorem. Real-image noise, iris-scale errors, pupil refraction, angle uncertainty and cross-frame edge-noise correlation are uncalibrated. No human result.

## PRODUCT ledger
Potentially allow a temporal-difference observable *after* real-image bias coherence calibration; reject absolute radius claims under unbounded bias; add abstention when predicted precision cannot meet gate. No deployable threshold yet. Three non-discriminating follow-up runs kill/reformulate this kernel, not the ongoing research process.

## Controlled wildcard
A 10% exchangeable spatial edge-noise component increases the single-frame radius variance at alpha=1.1 from 0.096960 to 0.112264 px^2; merely adding more contour pixels cannot remove shared error. This is a model stress test, not camera validation.

## Literature collision
- Petersch & Dierkes (2022), gaze-angle and corneal refraction pupil-size error: https://pmc.ncbi.nlm.nih.gov/articles/PMC9046372/
- Brisson et al. (2013), gaze-position errors across eye trackers: https://pubmed.ncbi.nlm.nih.gov/23468182/
- Hayes & Petrov (2016), correction of gaze-position pupil-size artifacts: https://pubmed.ncbi.nlm.nih.gov/25953668/
- Kothari et al. (2020), EllSeg occlusion/segmentation: https://arxiv.org/abs/2007.09600
- Prior Lucent E002-276 aperture information and E002-266 drift identifiability.
