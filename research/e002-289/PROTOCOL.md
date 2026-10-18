# Lucent E002-289: full kernel and conditional laws

SCIENTIFIC STATUS: theoretical + synthetic only; no human RGB paired reference was processed.

1. SIGNAL/REFERENCE: RGB pupil/iris conic-ratio time series vs simultaneous trustworthy eye-tracker pupil diameter normalized to iris diameter.
2. FRONTIER: Wang, Chern, Alexa (2019) already derived projective invariant from two concentric circles. Hayes & Petrov (2016) established gaze-dependent pupil foreshortening. Entrance-pupil optics and CondSeg (2024) show refractive and occlusion issues.
3. METRIC: projective generalized-eigenvalue ratio; minimax contour separation M compared with 2*epsilon; magnification-gauge temporal ratio overlap.
4. CONFOUND: pupil-specific refraction/magnification and eyelid-limited contour arc; also glare, glasses, brightness, gaze, camera response.
5. GENERATIVE MODEL: Y_k(x)=Q_k[b_k(x)+(g_k(x)/T_k) integral over exposure E_k of h_k * (L_t(x) A_t(x) S(x; H_t,R_iris,k_t*r_p(t),gaze_t,glasses_t)) dt]+e_k(x). S is scene reflectance; A is eyelid aperture mask, h is PSF. Segmentation occurs after exposure and response. Restricted ideal model: C_p'=H^-T diag(1,1,-r_p^2)H^-1 and C_i'=H^-T diag(1,1,-R_i^2)H^-1. Realistic reduced nuisance: q_k=k_k*r_p(k)/R_i.
6. FALSIFICATION: exact collision r/R=2/5,k=1 vs r/R=1/2,k=4/5; partial contour collision at bounded error; held-out human false certification would refute the model.
7. BOUNDARY: tangent-aligned circle arcs x_r(y)=r-sqrt(r^2-y^2), radii 0<a<b, |y|<=L<a, error <=epsilon, independent translation <=u. Delta(L)=a-sqrt(a^2-L^2)-b+sqrt(b^2-L^2). Minimax separation M=max(Delta/2,Delta-2u). Observational sets disjoint IFF M>2epsilon, equivalently Delta>min(4epsilon,2epsilon+2u). Exact L*: c=delta*+b-a, v=(b^2-a^2-c^2)/(2c), L*=sqrt(a^2-v^2) if attainable. Unknown independent pupil-specific k in [1-kappa,1+kappa] gives a sharp two-state ratio separation threshold lambda>((1+kappa)/(1-kappa))^2 for dilation under unrestricted baseline.
8. HUMAN: untouched; protocol frozen separately.
9. PUBLICATION: primary novelty beyond 2019 paper, real-camera calibration, prospective human subject/device/lighting/gaze/glasses holdout, geometry-only/brightness-only/missingness-only/smoothness controls, external checker, reproducibility.
10. PRODUCT: reject uncalibrated rapid pupil waveform recovery. Conditionally investigate projective-normalized ratio with measured nuisance bounds and abstention. Pivot to shutter-aware blink events if real optical calibration fails. Never claim five-second fatigue certification.

PROOF: The two conic matrices under a common H have generalized eigenvalues 1,1,(r/R)^2, modulo common conic scale; this is known prior art. For arcs, the curve difference d(y) is even and monotonically increases from 0 to Delta. An unknown shift difference t in [-2u,2u] minimizes sup |d+t| at max(Delta/2,Delta-2u). Two independently epsilon-bounded observation sets intersect iff the minimax residual <=2epsilon. The strict complement gives the exact conditional boundary. For q_t=k_t rho_t, under null rho1=rho0 the observed ratio q1/q0 ranges from kmin/kmax to kmax/kmin; under alternative rho1=lambda*rho0 it is multiplied by lambda. Intervals disjoint iff lambda>(kmax/kmin)^2.

NON-CLAIMS: no universal RGB impossibility, no human calibration, no field-level novelty, no diagnostic fatigue inference.