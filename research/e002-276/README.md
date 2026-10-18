# E002-276: RGB pupil aperture-information boundary

SCIENCE: Conditional Gaussian radius-information law, exact brightness-bias ambiguity. Synthetic only, no human or fatigue inference.
PRODUCT: Candidate geometry-aware rejection gate, not deployable without human calibration.

Active question: Does the angular spread of visible pupil edges predict RGB radius recovery accuracy?
Signal/reference: RGB pupil/iris contour waveform versus synchronized same-eye eye-tracker diameter. This run simulates radial RGB edge coordinates versus known simulated radius.
Frontier: ellipse/iris fitting under occlusion, entrance-pupil corneal optics and established Fisher-information methods.
Metric: eta=1/[n*(X'X)^(-1)[0,0]], X_j=(1,cos(theta_j),sin(theta_j)).
Strongest nuisance: unknown uniform brightness/blur contour offset and differential corneal magnification.
Falsification: held-out human errors violate independently calibrated uncertainty bounds, or nuisance-only controls perform equally well.
Mechanism prediction: at n=60, sigma=0.5 px, tolerance=1 px, a contiguous arc of 77.8276 degrees is needed for >=75% synthetic radius accuracy.
Human evaluation: absent. Publication threshold: untouched human participant/device/lighting/glasses holdouts, frozen waveform gates, independent checker and prior-art audit.
Product target: >=75% accurate admitted 5s windows at >=50% RGB-only coverage. Not met.
Kill: reject this estimator if boundary uncertainty cannot be calibrated or reference-blind coverage is inadequate.

Exact conditional law: y_j=r+c_x cos(theta_j)+c_y sin(theta_j)+b+epsilon_j, iid epsilon N(0,sigma^2), known angles. Var(r_hat)=sigma^2/[n-(sum cos(theta))^2/sum cos(theta)^2] for symmetric arcs. As half-width alpha approaches zero, angular information scales alpha^4/45, so radius SD scales alpha^-2.
Exact impossibility: (r,b)=(20,0) and (19,1) yield identical observations. Unbounded b defeats anatomical radius recovery even with a full contour.
