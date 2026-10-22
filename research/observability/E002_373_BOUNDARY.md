# E002-373: exposure-average aperture observability

Latent a(t) in [0,1], |a'|<=V. RGB surrogate y_j=(1/w) integral_exposure a(t)dt, with two exposures of length w bracketing a blind gap H. Let b be the minimum of the two measured exposure means, eta=1-b, L=1-theta.

Sharp endpoint deficit d_max = min(1,sqrt(2 V w eta)) if eta<=Vw/2, otherwise min(1,eta+Vw/2). Proof: a nonnegative V-Lipschitz deficit ending at d must have triangular or trapezoidal minimum integral; saturating the slope achieves equality. The gap minimum is at least 1-d_max-VH/2. A threshold touch is feasible in the speed-only scalar model iff H>=2 max(0,L-d_max)/V; saturating exposure deficits and gap slopes supplies the converse. With mean uncertainty r, replace eta by 1-b+r.

Frozen 40fps/10ms prediction (V=100/s, theta=.2, b=.999): H=15ms, guaranteed a>.20527864, so no hidden threshold closure. Independent acceleration-bounded LP midpoint minimum=.59993056, consistent. 30fps/10ms synthetic C1 witness (A=20000/s^2) has both exposure means=.99879 but gap midpoint=.18837796, below threshold. A constant-aperture comparator yields the same two scalar shutter means. Verified continuous-time bounds, not just sampled nodes. At 40fps the extra exposure-mean calibration error budget is only .00025 aperture units.

This is a conditional scalar measurement theorem, NOT universal indistinguishability of full RGB images. Real camera aperture extraction, physical V limits, nuisance transfer and human holdout remain unvalidated. Product: abstain unless independently calibrated timing, speed and aperture error certify the bound; no fatigue diagnosis or unconditional blink count.
