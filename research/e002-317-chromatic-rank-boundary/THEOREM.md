# E002-317: conditional RGB chromatic-rank observability

Model: after independent gain/canthal calibration and full-support linear RGB integration, y=h*a+z*b+e, where h is shutter-mean normalized eyelid aperture, z is arbitrary-amplitude contamination with a fixed calibrated RGB signature b, and ||e||2<=eta. Target signature a and nuisance b are fixed within the validated regime.

Let u=a-(a.b)/(b.b)*b, d=||u||. If d>0, hhat=(u.y)/d² eliminates z. Let rho be the norm of the component of y orthogonal to span(a,b). If rho>eta, the calibrated model is falsified. Otherwise the **exact** feasible aperture interval is [hhat-sqrt(eta²-rho²)/d, hhat+sqrt(eta²-rho²)/d] intersect [0,1]. Proof: minimizing ||y-h*a-z*b|| over z leaves squared residual d²(h-hhat)²+rho²; every feasible endpoint is attained.

Two-frame increase is certified exactly when the second lower endpoint exceeds the first upper endpoint. At zero orthogonal residual and equal noise budgets, the interior sharp boundary is observed increase > 2*eta/(||a||*abs(sin(theta))). A frozen synthetic crossing at eta=.01 and apparent increase .08 predicts critical angle asin(.25)=14.477512 degrees: 12 degrees abstain, 18 degrees certify.

At d=0, target and nuisance signatures are collinear: a=(1,1,1), b=(2,2,2), y=(.6,.6,.6) is compatible with (h,z)=(.6,0) and (.2,.2). Swapping latent states gives opposite trends from identical RGB observations. Unknown gain also creates an exact ambiguity: g(h*a+z*b)=(2g)((h/2)*a+(z/2)*b), even if a,b are independent. Independent reference gain is essential.

Bounded signature drift ||delta_a||<=ka, ||delta_b||<=kb, h<=H, |z|<=Z can be conservatively absorbed by eta_eff=eta+H*ka+Z*kb. Unbounded illumination color drift, auto-white-balance, saturation, cropping, glasses reflections and within-shutter photometric variation invalidate the simple gate.

Reference: synchronized high-speed anatomical shutter-mean eyelid aperture, NOT evaluated. Publication needs an unseen human participant/device boundary crossing, not merely a classical rank identity. Product permits only calibrated interval-valued shutter-mean lid occupancy with abstention. No point blink timing, pupil waveform, or fatigue certification.
