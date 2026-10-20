# Lucent E002-316 — full-image blind-blur / contrast gauge (2026-10-20)

**Exact restricted-model impossibility, positive integral invariant, synthetic verification only. No ordinary-RGB/high-speed human validation or field-level novelty claim.**

Question: does a complete 1-D RGB eyelid band profile identify anatomical aperture if optical blur and local contrast are uncalibrated? Signal: full baseline-subtracted linear-response RGB profile. Future reference: concurrent high-speed shutter-mean anatomical lid separation divided by canthal width. Metric: full-image injectivity and sharp integral-only sign certification.

Forward model: Y_j(x)=C_j [K*R_d](x-c), R_d=1_{[-d/2,d/2]}, K>=0, integral K=1, C_j>0, d=a*h. Assumes locally straight uniform-contrast band, full spatial support, linear camera, no glasses reflections. Not an arbitrary eye-image model.

**Exact full-image collision:** for any d1!=d2, set K_A=R_d2/d2, K_B=R_d1/d1, C_B=C_A*d1/d2. Then C_A R_d1*K_A=C_B R_d2*K_B pointwise by convolution commutativity. Different apertures, blurs and contrasts give identical complete noiseless RGB images, even after any identical deterministic sampling. Exact discrete witness (d,C,box PSF width)=(3,1/2,5) versus (5,3/10,3): same profile [1/10,1/5,3/10,3/10,3/10,1/5,1/10], area 3/2. Both latent states can be constant during exposure.

**Positive invariant:** S_j=int Y_j=C_j*d, independent of unit-mass PSF. If PSF centroid calibrated to zero, image centroid recovers band center. If PSF variance known, Var(Y/S)=d²/12+Var(K) identifies d; if variance only bounded, yields a necessary interval, not a full-image sharp interval.

**Normalized temporal observable:** S_i=C_i*a_i*h_i and canthal D_i=a_i*d0, so Q_i=S_i/D_i=C_i*(h_i/d0). If relative contrast C1/C0 in [r,1/r], then r*(Q1/Q0)<=h1/h0<=(Q1/Q0)/r. This interval is **sharp for the integral-only statistic**, and anatomical increase is certified by those integrals iff Q1/Q0>1/r. For observed +10%: rcrit=10/11; r=.90 abstain, r=.92 certify. Full image may sometimes give tighter constraints; do not claim global iff.

Failure: cropping, nonlinearity, texture, changing within-exposure photometry, gaze projection, glasses glare, timebase and 10-Hz decimation. Conditional result only.

Product: **conditionally permit** calibrated interval-valued shutter-mean eyelid occupancy with abstention; **reject** unrestricted dual-edge separation from blended profiles, absolute uncalibrated aperture, rapid pupil waveforms, within-exposure blink timing, five-second fatigue certification. See protocol, failed gates, primary prior art and independent checker.
