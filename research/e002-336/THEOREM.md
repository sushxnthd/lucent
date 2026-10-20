# E002-336 — Sharp two-anchor bounded-drift clock law

Conditional theorem (elementary metrology, not a claim of mathematical novelty): Let true camera/reference clock alignment on [t0,t1] be affine through true anchor values plus residual h(t), with h(t0)=h(t1)=0 and |h'(t)|<=kappa almost everywhere. Anchor errors satisfy |e_i|<=epsilon_i. Camera/reference event localization errors are bounded c and r. Let d(t) be the observed lag after interpolation of measured anchors, u=(t-t0)/(t1-t0).

The exact identified interval is tau(t) in [d(t)-B(t), d(t)+B(t)], where
B(t)=(1-u)*epsilon0+u*epsilon1+kappa*min(t-t0,t1-t)+c+r.

A strictly positive lag is certifiable iff d>B; negative iff d<-B. At equality zero is feasible, so abstain.

Proof: interpolated anchor errors contribute (1-u)e0+u e1. Residual h vanishes at both anchors and is kappa-Lipschitz, so |h(t)|<=kappa min(t-t0,t1-t). Add event errors. Sharpness: choose signed endpoint errors, the tent residual h(t)=+/- kappa min(t-t0,t1-t), and event errors at signed bounds. All constraints hold and both interval endpoints are attained. Smooth residuals approximate the tent if required. Convexity gives all intermediate values.

Without any non-affine drift bound, two exact anchors do not identify interior lag: h_A(t)=A*sin(pi*(t-t0)/(t1-t0)) vanishes at both anchors yet changes interior timing. Even requiring monotonic clocks permits nonzero A when |A|*pi/(t1-t0)<1 for unit-slope nominal alignment.

This theorem does not establish any real webcam's kappa, sync errors, pupil extraction validity, human lag observability, or publication novelty.
