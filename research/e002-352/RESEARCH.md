# Lucent E002-352 — Sharp shutter-averaged blink-peak observability

**Status (2026-10-22):** Exact conditional scalar measurement boundary derived and independently checked. No human-reference validation. No mathematical novelty claim. This research branch is isolated from product/main.

## Signal/reference and forward model

Physical reference: high-speed palpebral aperture a(t), dimensionless closure c(t)=1-a(t)/a_open(t). RGB-derived normalized shutter contrast:

z_k = (1/w) integral_[kF-w/2,kF+w/2] c(t) dt + e_k, |e_k|<=epsilon.

This reduced model requires independent calibration of scale, gaze projection, illumination, eye-specific photometry, exposure, shutter response, glasses and timebase. Without bounded epsilon it **does not apply**.

The full RGB forward model is Y_k(x)=G_k((1/w) integral_[I_k](g_k L(x;a(t),p(t),theta(t),h(t),o(t))+b_k)dt)+n_k(x), where p=pupil state, theta=gaze, h=head geometry, o=occlusion, and G_k is camera response.

## Sharp peak law

For c(t)>=0, some peak c(t0)>=A>0, |c(t)-c(s)|<=V|t-s|, periodic shutter centers separated by F, 0<w<=F, and |e_k|<=epsilon, define q=A/V, l=(F-w)/2, u=(F+w)/2.

**Lambda(A,V,F,w) = V/(2w) ([q-l]_+^2-[q-u]_+^2).**

Every admissible peak is distinguishable from no event for all peak phases and bounded errors **iff Lambda>2epsilon**. At equality, there is an exact observational collision.

Proof: the peak and speed bound force c(t)>=max(0,A-V|t-t0|). Its shutter integral is even and decreasing with shutter-center distance. Worst peak phase is midway between shutter centers. The tent attains the bound. When Lambda<=2epsilon, choose event error -m_k/2 and baseline error +m_k/2 for every frame, giving identical observed sequences.

Piecewise:
- q<=l: Lambda=0, peak can fall entirely between exposures.
- l<q<u: Lambda=V/(2w)(q-l)^2; boundary A=V(F-w)/2+sqrt(4epsilon V w).
- q>=u: Lambda=A-VF/2; boundary A=VF/2+2epsilon.

With F=1/30s, w=.010s, A=1, epsilon=.05, the exact speed crossing is **V*=56.8196361136/s**. At V=40/s, Lambda=1/3>0.1; at V=60/s, Lambda=.075<0.1. These are synthetic hypothetical parameters, not calibrated human values.

For a missing frame, replace F with the longest *interior* retained-center gap G (equal w), with appropriate recording-edge censoring.

## Corrective result

The earlier E002-349 rectangular, full-depth closure duration threshold **cannot be extended** to partial continuous eyelid closure. Without a lower bound on peak amplitude, even arbitrarily long shallow closure can be indistinguishable under positive bounded noise. Peak amplitude, maximum speed, exposure, actual frame gaps and calibrated error are necessary for this guarantee.

## Independent checks and negative gates

Local independent_checker.py passed 400 numerical quadratures (max discrepancy 1.09e-15), 150 phase optimizations (4.44e-16), 1,000 exact error collisions, 1,000 nonminimal-waveform dominance checks, 1,000 shared geometry/brightness controls, dropout and smoothing controls, and 300 constructed three-patch RGB collisions. No human data was analyzed.

Unmet: synchronized native-RGB/high-speed human reference, measured nuisance epsilon, participant/device holdout, prospective unseen boundary crossing, mathematical novelty, universal full-RGB impossibility.

## Product gate

Allow calibrated blink-peak **detectability** as research only when Lambda>2epsilon and all model gates pass. Abstain for unknown shutter/clock, gaze, glasses, auto-exposure, eye-specific lighting, occlusion, unbounded error, or recording edges. Reject duration-only guarantees for partial blinks, peak-velocity certification, unrestricted pupil waveform reconstruction and five-second fatigue certification.

## Frozen external test

Freeze RGB calibration on development participants. Acquire native consumer RGB with real shutter timestamps plus independent >=250-fps (ideally >=500-fps) eyelid video/EOG. Hold out participants and devices; stratify gaze, glasses and lighting. Include geometry-only, brightness-only, missingness-only and temporal-smoothness-only controls. Before holdout predict which calibrated strata cross Lambda-2epsilon=0. A negative margin means **no guarantee**, not that every event is missed. Do not train a black-box detector to define the physical boundary.

## Prior art and data-access status

- Navascues-Cornago et al., The Ocular Surface 2026, DOI 10.1016/j.jtos.2026.01.003: 500-fps IR downsampling; velocities particularly sensitive to fps.
- Culemann et al., Behavior Research Methods 2026, DOI 10.3758/s13428-026-02984-4: blink metrics confounded by vertical gaze.
- Kwon et al., J R Soc Interface 2013, DOI 10.1098/rsif.2013.0227: 600-fps eyelid kinematics.
- mEBAL2 (https://github.com/BiDAlab/mEBAL2): synchronized RGB/NIR and manually refined blink labels, but signed license required.
- Eye of the Typer (https://webgazer.cs.brown.edu/data/): webcam + raw 120-Hz Tobii data; large archive and approximate video alignment.

The exact mathematical method is established Lipschitz optimal-recovery theory. A publishable result still requires prospective human validation and a defensible novelty claim.

**Full local artifact**: lucent_e002_352_peak_shutter_boundary.zip (theorem, simulator, independent checker, JSON collisions, frozen protocol, failed gates, prior art, checksums). The branch text is a concise durable research record; local artifact is the complete runnable record.