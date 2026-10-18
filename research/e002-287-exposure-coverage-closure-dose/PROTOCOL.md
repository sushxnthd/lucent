# E002-287 — Sharp shutter-coverage law (2026-10-18)

STATUS: exact conditional theorem + synthetic independent check; NO real-camera calibration, paired human evaluation, or field-level novelty.

## Mandatory 10-field kernel
1. Signal/reference: calibrated linear RGB eyelid-closure surrogate y_i versus synchronized >=120Hz reference c(t) in [0,1], target closure dose D=integral c(t)dt over 5s.
2. Literature: PERCLOS (FHWA 1998), SLEEP Advances review 2023, 600fps human blink kinematics (2013), ELA 2025; citations below.
3. Metric: exact identified interval for D and threshold-certification/abstention.
4. Nuisance: shutter gaps, then nonlinear RGB-to-closure mapping, illumination, pose/gaze, glasses, clipping, rolling shutter.
5. Generative model: raw pixel Y_ip = G_ip((1/T_ip) integral_E L_p(t) R_p(h(t),gaze(t),pose(t),pupil(t))dt)+offset+noise. Only after independent calibration assume y_i=(1/T)integral_[iP,iP+T]c(t)dt+e_i, |e_i|<=eta. This simplification is UNVALIDATED for ordinary RGB.
6. Falsification: high-speed human reference D_ref outside predicted interval, or nuisance-only lighting/pose artifact violating independently measured eta.
7. Boundary: [T sum max(0,y_i-eta), T sum min(1,y_i+eta)+N(P-T)] for consistent data. Unclipped relative width = 1-rho+2rho*eta, rho=T/P.
8. Untouched human test: pending; freeze protocol before participant/device/lighting/gaze/glasses holdout.
9. Publication threshold: real camera radiometric calibration, independent human reference, prospective boundary crossing, nuisance baselines, independent checker and novelty differentiation.
10. Product: allow only calibrated uncertainty-aware closure-dose measurement when interval width below tolerance; reject five-second blink-rate-only fatigue claims and PERCLOS equivalence; otherwise abstain.

## Exact theorem / proof
Let N non-overlapping frame periods [iP,(i+1)P) contain exposures [iP,iP+T), 0<T<=P. Let measurable c(t) in [0,1]. Observed y_i = (1/T) integral_exposure c(t)dt + e_i with |e_i|<=eta. Then the exact identified set of D=integral_[0,NP] c(t)dt is:
D_min=T sum_i max(0,y_i-eta);
D_max=T sum_i min(1,y_i+eta)+N(P-T).
Necessity: clip each exposed average to [0,1] and bound each unseen gap by its duration. Sufficiency: choose c constant at each exposure endpoint and independently c=0 or 1 in each gap. Convex mixtures realize every intermediate D. This is sharp, assuming measurements are consistent.
When T=P and eta=0, D=P sum y_i exactly for any waveform, regardless of blink bandwidth; this is a standard integration identity. When T<P, a closure wholly within a gap is invisible. Two histories with c=0 everywhere vs c=1 in every gap yield identical frames but D differing by N(P-T). A single event of duration <=P-T can likewise be hidden.
Even full-duty integrated dose cannot identify PERCLOS: in a 100ms exposure, c_A=1 for 20ms and 0 otherwise versus c_B=.2 for 100ms give identical y=.2 but P80=.2 vs 0. Nor can it identify blink counts.

## Frozen synthetic predictions (eta=.01, 5 seconds)
10fps 20% duty: width fraction .804; 10Hz loader retaining 1/60s exposure: .8366667; 30fps 50% duty: .51; 60fps 100% duty: .02. Predeclared unseen *synthetic* 24fps 24% duty: .7648. Not a human holdout.

## Prior art / priority audit
FHWA PERCLOS (1998): https://rosap.ntl.bts.gov/view/dot/113
SLEEP Advances PERCLOS review (2023): https://academic.oup.com/sleepadvances/article/4/1/zpad006/7000589
Truck driver fatigue sensor (2021): https://pmc.ncbi.nlm.nih.gov/articles/PMC8512350/
600fps blink kinematics (2013): https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/
ELA eye metric (2025): https://arxiv.org/abs/2511.19519
Mobile blink application (2025): https://arxiv.org/abs/2511.14361
Do NOT claim mathematical novelty for exposure integration, set membership or PERCLOS. Only calibrated prospective real-RGB results might establish new measurement science.
