# E002-297 conditional measurement law

Global-shutter 1-D ideal eye aperture: Y(x)=B+C/T ∫[1_[u(t),l(t)]*h_t](x)dt, where h_t is unit-mass, nonnegative, spatially shift-invariant, contrast C is known, and full spatial support is captured. Integrating x gives S/C=(1/T)∫(l-u)dt. With unknown but stable C, ratios of background-subtracted image mass S2/S1 equal ratios of exposure-averaged projected apertures. This is ordinary conservation of mass under convolution, NOT a new general theorem.

Contrast+PSF exact collision: 2(box_2*U_4)=box_4*U_2, with U_w a unit-mass uniform kernel. Widths 2 and 4 give identical full images if gain and PSF vary.

Rolling shutter: for row time t=t0+tau*x, a rigidly translating aperture A at velocity v has apparent width A/(1-v*tau), v*tau<1. Finite exposure T adds normalized blur U_(abs(v)*T/(1-v*tau)), leaving apparent mass unchanged. Positive-velocity relative bias v*tau/(1-v*tau) crosses tolerance q at v*tau=q/(1+q).

Exact known-gain rolling/PSF collision: stationary width 4 convolved with U_(2/3) equals rolling width 3 with v=1,tau=1/4,T=1/2, initial interval [-7/4,5/4] and delta PSF. Both profiles coincide at all x. This is a conditional nonidentifiability result, not a human-camera accuracy claim.

For |v*tau|<=k<1, true rigid aperture lies in [Aapp(1-k),Aapp(1+k)]. Differential lid velocities, iris texture, glasses reflections, nonlinear radiometry, gaze-dependent projection, and unknown baseline remain outside the positive invariant. No human reference evaluated.