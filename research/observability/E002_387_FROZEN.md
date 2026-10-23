# E002-387 preregistration — finite-exposure reference aliasing (2026-10-23)

## One kernel
E002-371 shutter-gap / eyelid-velocity observability. This experiment tests whether a purported high-speed *reference camera* can label threshold crossings that ordinary cameras are accused of hiding. It is a synthetic instrument falsification, NOT human validation, NOT a new physiology law. No parameter tuning after freeze.

## Ground truth and independent synthetic acquisition
Physical normalized aperture a(t)=min(1,h+V|t-t0|), V=40/s, closure threshold theta=0.2, h in {0.17,0.185,0.195}. The true threshold-crossing duration is D=2(theta-h)/V (1.5,0.75,0.25 ms). This is a *brief threshold excursion*, not a complete human blink. Reference rates f in {240,960} Hz; exposure e in {0,0.0005,0.002,0.004} s, but reject physically invalid e>1/f. Evaluate 10,000 deterministic onset phases (k+0.5)/10000/f. A point sample is a(t_k); an exposure sample is the EXACT continuous-time boxcar average over [t_k-e/2,t_k+e/2], not a point approximation. Reference says CLOSED iff any sample is strictly below theta. Compare against analytic ground truth that is closed for positive duration. One cycle suffices because all trajectories are periodic in phase; include samples k=-3..3.

## Predictions frozen before evaluation
P1 point reference 240 Hz for h=0.17 detects about 36% of phases, 960 Hz detects 100%; h=0.195 detects about 6% and 24% respectively.
P2 240-Hz reference with 4-ms exposure detects 0% of true threshold excursions for all three h, despite nominal 240 fps.
P3 960-Hz reference with 0.5-ms exposure detects some but not all h=0.17/0.185 events? Specifically h=0.17 should reach 100%, h=0.195 should reach 0% under strict threshold because its minimum exposure average equals theta. h=0.185 must be measured without predeclared pass threshold.
P4 a reference-label qualifier must abstain when exposure, timing, optical transfer, or independently bounded aperture speed is missing, and must never equate a negative reference label with no physical closure.

## Independent verification
Use two independent exposure integrators: analytic primitive of min(1,h+V|t-t0|) and an adaptive numerical quadrature on >=100 selected phases. Assert max difference <1e-9. Independently verify point-sample phase fractions against min(1,D*f). Include boundary tests at e=0, and e=4 ms with 240 Hz. Freeze seed-free phase grid. Report all outcomes including failed predictions.

## Scientific limitations and product consequence
This experiment does NOT estimate human event prevalence or physiological speed bounds. It tests label adequacy for the E002-371 falsification protocol. A negative reference label is only conclusive when reference exposure, sample gaps, aperture response and kinematic bounds jointly exclude an event. Paired human acquisition must use a calibrated high-speed reference with known *exposure* and timestamps, manual aperture ground truth and a held-out ordinary-RGB camera. Dataset search was attempted twice; PLOS 2018 240-fps study points to a University of Alicante repository, but the raw time-series/video could not be fetched here; Silesian5 100-fps is license-gated. Do not relabel literature summary statistics as held-out validation.
