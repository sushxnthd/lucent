# E002-381: moving eyelid-front aliasing, 2026-10-23

**Frozen before tests:** E002_381_FROZEN.md at commit b4f8ef8de6cef57d3d88337c89d4fa4f7304a00e.

## Exact law
For row r, reference occlusion interval [s+tau_r,s+tau_r+D_r]; sensor exposure [nF+delta_r,nF+delta_r+w]. Overlap >=m iff unknown event phase s mod F lies in the circular arc [delta_r-tau_r+m-D_r, delta_r-tau_r+w-m]. All-phase row-event capture iff union of arcs covers the circle. For equal D, let L=D+w-2m and e_r=(delta_r-tau_r) mod F. Exact boundary is max circular gap of e_r <=L. This is established interval-cover mathematics applied to an idealized ocular front, not a new universal theorem.

## Frozen synthetic predictions
F=1/30,w=.010,D=.015,m=.004; delta=[0,.005,.010,.015,.020] seconds, tau=alpha*delta. Exact transition alpha=11/60.
- alpha=0: certified; 12000/12000 phase hits.
- alpha=.18: certified; 12000/12000 hits.
- alpha=11/60: certified at equality; 12000/12000 hits.
- **Unseen alpha=.19: not certified; 47/12000 phases missed; explicit missed phase 22.2666667 ms.**
- alpha=.20: not certified; 119/12000 missed.
- alpha=1: not certified; 5879/12000 missed.

Independent direct-overlap oracle agreed on 2500 exact randomized heterogeneous-duration cases and all six frozen predictions. Product certificate passed 600 randomized calibration cases, 516 certified, each with six independent jitter draws. A synthetic 80x96 RGB ocular-patch instrument reproduced the predicted boundary. These are synthetic, not human observations.

## Construct-validity falsification
At alpha=1 the row-specific occlusions never coexist: whole-eye simultaneous closure duration is exactly 0 ms, even though 51% of onset phases have some row captured. **Any-row occlusion must not be labeled whole-eye blink.** A naive synthetic RGB-template detector produced false closure responses on open-eye gaze-only (score .674) and blur-only (.388) controls. Photometry, missingness, glare and clock/front-delay uncertainty require calibration/abstention; no real-camera calibration was performed.

## Product decision
Reject unqualified rolling-shutter readout-span enhancement and any-row->whole-eye inference. Allow only independently calibrated row-event camera-qualification with abstention. Do not claim PERCLOS, rapid pupil reconstruction, or five-second fatigue assessment.

## Primary priority audit
Kwon et al. 2013 (10.1098/rsif.2013.0227), Espinosa et al. 2018 (10.1371/journal.pone.0196125), Wambier et al. 2014 (10.1097/IOP.0000000000000031), and shuffled rolling-shutter temporal imaging (10.1364/OE.444864) establish substantial prior work. No publication-level novelty established. No paired human validation or held-out participant/device evaluation.
