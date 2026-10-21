# E002-346 | Exposure-aware temporal pupil observability (2026-10-21)

**Status:** conditional feature-level mathematics, independently checked numerically; NO paired human evaluation or established novelty.

## Measurement model
Raw RGB frame is an exposure average of a rendered eye, then a nonlinear feature extractor. For a valid, calibrated pupil/iris ellipse shape ratio, let x(t)=log(r(t)/R) and z_k=(1/4)log(det(Qp,k)/det(Qi,k)). After bounding feature/exposure noncommutation by B_k, use

z_k = (1/w_k) integral_[t_k+delta_k-w_k/2,t_k+delta_k+w_k/2] [x(t)+d(t)] dt + e_k + b_k.

Assume |delta_k|<=c_k, |e_k|<=eta_k, |b_k|<=B_k, |x'|<=V, |d'|<=K. Differential optics, eyelid aperture, gaze, photometry and iris deformation contribute to d. If these bounds are not independently established, abstain.

## Sharp conditional boundaries
The **exact single-observation** exposure-plus-clock deviation of a J-Lipschitz feature from its nominal center is J*h(w,c), with h(w,c)=w/4+c^2/w when c<=w/2, otherwise c (and h(0,c)=c). Proof: maximize the average |s+delta| over |delta|<=c; a cusp attains the bound. Thus E_k=eta_k+B_k+(V+K)h(w_k,c_k).

A **sufficient** pupil-change certificate between nominal times is z_j-z_i>K(t_j-t_i)+E_i+E_j. This is necessary/sufficient only for the relaxed independent pointwise error model, not generally for globally coupled exposure errors.

With independently calibrated, feasible physical sample intervals ell_i<=x(t_i)<=u_i and Lipschitz rate V, let U_i=min_j(u_j+V|t_i-t_j|). The exact range of the continuous-time peak P=max_t x(t) is:

P_min=max_i ell_i; P_max=max_i [U_i+U_(i+1)+V(t_(i+1)-t_i)]/2.

For uniform sample frequency f and flat measured samples with interval radius eta, the exact maximum hidden peak is eta+V/(2f). Excluding peaks strictly above h>eta requires f>=V/[2(h-eta)]. Without finite calibrated V, no finite f guarantees peak exclusion. These are classical McShane-Whitney optimal-recovery constructions, not novel mathematics.

**Illustration only:** V=1 log-radius/s, eta=.005 gives hidden peak .055 at 10 Hz, .021667 at 30 Hz, .013333 at 60 Hz. A .02 threshold is not excludable at 30 Hz, but is at 60 Hz, conditional on calibration.

## Independent checks
160 randomized exact-peak comparisons to SciPy LP across every sampling gap (max discrepancy 8.88e-16); 500 direct exposure-integral comparisons (max discrepancy 1.95e-8 from quadrature); 500 independent two-point corner checks. All passed. **Human pairs tested: 0.**

## Ten-part active kernel
1. Signal/reference: ordinary-RGB normalized pupil/iris ellipse log ratio versus native-time independent physical pupil diameter.
2. Frontier: McShane 1934, Micchelli/Rivlin/Winograd 1976; Snip & Stitch 2026 pupil foreshortening; EyeDentify WACV 2025.
3. Metric: exact set-membership peak interval, sign certificates, holdout coverage/abstention.
4. Dominant confound: uncalibrated differential optics/occlusion plus exposure-clock error.
5. Generative model: exposure-integrated rendering, nonlinear extraction, calibrated feature-level approximation above.
6. Falsification: reference violates V, optics K, extraction B, clock c, or holdout interval coverage.
7. Boundary: eta+V/(2f) for point-sample peak exclusion; h(w,c) for exposure/clock.
8. Human test: SHA256('lucent-346:'+participant_id) mod 5==0 untouched holdout; entire participant/device regimes; geometry-only, brightness-only, missingness-only, temporal-smoothness controls. Not executed.
9. Publication gate: independent human calibration and prospectively predicted holdout boundary crossing plus novelty beyond classical theory.
10. Product: REJECT unrestricted rapid pupil-waveform recovery and 5-second fatigue diagnosis. Only calibrated interval-valued feature certificates with abstention are candidates.

## Source and validation caveats
EyeDentify processed three-second-averaged labels cannot certify rapid physiology. EOTT website verifies Tobii gaze but raw pupil-diameter availability remains unverified. Eye-BCI high-speed eye video is not evidence of simultaneous ordinary webcam RGB. A public Kaggle URL was located; a single container-side request failed DNS. No dataset was downloaded. Do not claim any human test.

## Prior art
- https://doi.org/10.1090/S0002-9904-1934-05978-0
- https://research.ibm.com/publications/the-optimal-recovery-of-smooth-functions
- https://link.springer.com/article/10.3758/s13428-026-02980-8
- https://github.com/vijulshah/eyedentify
- https://webgazer.cs.brown.edu/data/

Local reproducibility package includes THEOREM.md, PROTOCOL_FROZEN.md, PRIOR_ART.md, observer.py, independent_checker.py, RESULTS.json, SHA256SUMS.txt and FAILED_GATES.md. Full source write-through attempted separately.
