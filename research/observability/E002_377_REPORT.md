# E002-377: Sharp full-RGB shutter–contrast observability boundary

**Status:** Exact model-conditional theorem, synthetic instrument, frozen unseen-condition prediction. No human validation; no novelty claim.

## One active kernel
Signal: native, linearized RGB shutter-exposure frames. Reference: a complete eyelid-closure plateau of known duration D, with >=250-fps independently timestamped reference in the planned human study. Strongest confound: local image changes from gaze/illumination/glasses that can align with the closure template.

For pixel/channel i and frame k, the explicit generative model is

    Y[k,i]=I_open[i]+rho[k]*(I_closed[i]-I_open[i])+e[k,i]
    rho[k]=overlap([phi+kF,phi+kF+w],[0,D])/w
    |e[k,i]|<=epsilon.

Here F is shutter period, w exposure, phi unknown shutter phase, and c_inf=max_i |I_closed[i]-I_open[i]|. Assumptions: global shutter, fixed known templates, rectangular closure plateau, linear pre-gamma integration, independently bounded residuals, no unmodeled rolling-shutter or unknown optical transforms.

## Exact boundary and proof
The observation sets of two complete RGB image histories are disjoint iff their L-infinity distance is strictly greater than 2epsilon. If not, their componentwise midpoint belongs to both sets with residual <=epsilon; if any component differs by >2epsilon, no common observation exists. Equality is ambiguous.

The minimax maximum overlap of a plateau with periodic exposures is

    M_min=min(w,max(0,(D-(F-w))/2)).

Proof: when D<=F-w, place the plateau in a shutter gap. For F-w<D<F+w, center the plateau across a gap; the two adjacent exposures must share at least D-(F-w) total overlap, optimally split equally. For D>=F+w, a fully closed exposure is unavoidable. Consequently, the **sharp full-image minimax discriminability law** is

    Xi = c_inf*M_min/(2*epsilon*w) > 1.

If Xi<=1, there exists an exact complete-RGB collision for some phase and allowed residuals. This is a conditional worst-case law, not a physiological or camera-independent guarantee. A conservative 8-bit sufficient certificate uses epsilon_eff=epsilon+1/510 to budget quantization.

## Frozen synthetic prediction and checks
Frozen before the numerical test: D=42 ms, F=50 ms, w=10 ms, epsilon=0.01. Worst phase=41 ms, M_min=1 ms. At c_inf=0.15, Xi=0.75 and all 576 pixel/channel/frame values collide with maximum per-history residual 0.0075. At c_inf=0.20, Xi=1, equality collision. At c_inf=0.30, Xi=1.5, no collision possible. At 30 fps, M_min=28/3 ms, so c_inf=0.15 is certifiable. The independent exact-rational checker reconstructs all pixels and verifies 60 randomized phase-grid configurations.

## Adversarial synthetic optical stress
A separate stylized 64x96 RGB eye-stripe simulator (local archive) tested blur, missingness, gain and local brightness drift. At 20 fps with conservative 8-bit quantization, clean and 1-pixel blur passed, while >=2-pixel blur, eye-region missingness, local drift and reduced gain failed. At 30 fps all but total informative-pixel missingness passed under stipulated bounds. A brightness-only negative control exceeding epsilon must trigger abstention. These are NOT measurements of a webcam, a participant, or a natural eyelid.

## Human protocol (unexecuted)
Acquire native 20/25/30/60 fps RGB and >=250 fps eye-reference with exposure timestamps and two independent synchronization anchors. Independently calibrate open/closed RGB templates and residual coverage on development participants. Freeze one Xi=1 crossing before untouched participant/device/lighting/glasses holdout. Test geometry-only, brightness-only, missingness-only, temporal-smoothness-only, no-blink, blur, gaze, clock and rolling-shutter controls. If model assumptions are verified but a Xi>1 event is missed, falsify the certificate; otherwise report out-of-model and abstention separately. Do not infer blink durations from undetected events.

## Primary prior-art and novelty audit
Raskar et al. (2006), https://www.merl.com/publications/TR2006-124, exposure coding and motion blur; Tendero & Osher (2016), https://link.springer.com/article/10.1186/s40687-015-0051-8, coded exposure noise theory; Kwon et al. (2013), https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/, 600-fps human blink kinematics (58 ms mean closed phase is not a universal minimum); Guttmann-Flury et al. (2025), https://www.nature.com/articles/s41597-025-04861-9, shared multimodal high-speed ocular data, not accessed in this run. Bounded-error separation and shutter overlap are established mathematics; publication novelty unestablished.

## Product decision
ALLOW a calibrated *camera qualification* certificate for specified event duration with independently verified contrast/noise/exposure bounds. ABSTAIN if Xi<=1 or calibration fails (glasses, gaze, blur, illumination, missingness, nonlinear pipeline, rolling shutter, timing). REJECT unconditional PERCLOS, rapid physical pupil-waveform recovery and five-second fatigue diagnosis. No app UI.

Reproduce: python research/observability/e002_377_independent_checker.py.
