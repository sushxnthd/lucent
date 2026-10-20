# Sharp active-probe nuisance-boundary theorem

## Signal/reference and measurement model
Target: normalized RGB pupil/iris response per shutter; reference: native-timestamp, synchronized high-rate independent pupil diameter. No human paired data evaluated. Let known display input evoke both pupil response p(t) and direct camera/illumination nuisance n(t). A calibrated scalar observation at nominal shutter start s is y=(1/E) integral from s+delta to s+delta+E of (p(t)+n(t)) dt + e. Unknown clock offset |delta|<=Delta; error |e|<=eta. Null p=0; alternative p=A times indicator of [tau_p,tau_p+d], A>=0. Signed nuisance |n(t)|<=B on [0,tau_c], zero elsewhere.

## Exact full-video gauge failure
For unrestricted stimulus-locked nuisance, (p,n) and (p+v,n-v) produce identical observations for any v(t), even if v is smooth. In a full-image linearization I(x,t)=I0(x,t)+a(x)p(t)+b(x)n(t), choose a=b to obtain exactly identical RGB videos. A known randomized stimulus does not identify the physiological path unless its direct photometric pathway is restricted or independently measured. This is an existence counterexample in a nuisance class, not a universal claim about all cameras.

## Sharp one-exposure null/alternative law
P(delta)=length(shutter intersect [tau_p,tau_p+d])/E; N(delta)=length(shutter intersect [0,tau_c])/E. Feasible null interval Y0=[-B max N-eta,B max N+eta]. Feasible alternative interval Y1=[min_delta(A P-B N)-eta,max_delta(A P+B N)+eta]. All intervals are attainable under arbitrary bounded measurable nuisance, and their unions over continuous delta are connected. Therefore the two hypotheses are distinguishable in every admissible world exactly when

M(s)=min_delta[A P(delta)-B N(delta)] - B max_delta N(delta) - 2 eta > 0.

At M=0 they collide: abstain. Every extrema lies at delta=+-Delta or a shutter-endpoint crossing of 0,tau_c,tau_p,tau_p+d. model.py enumerates these exactly using fractions.

## Closed-form shutter start boundary
If every candidate shutter lies entirely within the pupil-response plateau and its nuisance overlap fraction is (tau_c-s+Delta)/E between 0 and 1, then M=A-2B(tau_c-s+Delta)/E-2eta. For B>0 and 0<A-2eta<2B, Scrit=tau_c+Delta-E(A-2eta)/(2B). Certify iff s>Scrit *within this subregime*.

## Limits and consequence
This is a conditional single-exposure scalar detection theorem, not arbitrary waveform recovery, physiological validation, or established novelty. Rectangular pupil responses are hypothetical; real responses are delayed and smooth. Ordinary RGB automatic exposure/reflection may persist into pupil latency, invalidating finite tau_c. Calibrate direct path, clock, gain, exposure, reference, geometry, gaze and glasses first. Reject uncalibrated active-probe fatigue claims; allow only calibrated interval certificates with abstention after untouched human validation.
