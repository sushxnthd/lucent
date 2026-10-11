# E002-112 RGB-REFERENCE-OBSERVABILITY-002: frozen 3-second webcam/eye-tracker pilot
Date 2026-10-11. Type: DISCRIMINATION / CAPABILITY-BUILDING.
Source: EyeDentify original visible-light RGB eye crops and synchronized Tobii diameter labels, Kaggle vijuls/PupilDiameterDatasets (CC BY-NC 4.0).
Original per-file API was independently verified HTTP 200 for left_eyes/{1,4,50}/{1,11}/session_data.csv and frame_01.png from 1/1.
**This is a 3-second, 30fps dataset, not a 5-second recording or active fatigue-state validation.** No claim of new data or novel normalization.

## Fixed split and scope
Development participant 1, sessions 1 and 11; held-out participants 4 and 50, sessions 1 and 11. Left eye only.
From each session, use rows 1,4,7,...,88 (1-indexed) = 30 frames at ~10fps. Do not select frames by tracker value or image quality.
No labels from held-out participants may tune thresholds. Participants 4 and 50 are distinct from dev; 4 and 50 were described in external prior-art blog, so this is **not fully untouched external validation**. All comparisons remain descriptive.

## Fixed estimator
For each RGB crop (32x16), luminance Y=0.2126R+0.7152G+0.0722B. ROI: rows 5..12 and columns 8..25 (1-indexed).
L=ROI; low=2nd percentile, high=90th percentile, z=clip((L-low)/(high-low),0,1); if high-low<0.05 abstain.
Define w(x,y)=exp(-((x-16.5)^2/100+(y-8.5)^2/20)) on the ROI.
P=sum(w/(1+exp((z-0.28)/0.06))); I=sum(w/(1+exp((z-0.75)/0.08))).
Baseline b=sqrt(P). Reference-normalized q=sqrt(P/I). Abstain if P<1, I<4, P>=I, or nonfinite.
No temporal smoothing, per-person reference fitting, tracker-informed calibration, or lag search. Evaluate same valid frames for b and q. Session-wise Pearson r with Tobii left_pupil; also first-difference Pearson r. Report dropout and within-session tracker standard deviation; no pseudo-independent frame-level p values.

## Frozen directional gates (4 held-out participant×session clips)
At least 3/4 clips have >=20 eligible frames, positive q-vs-Tobii Pearson r >=0.30, and median q correlation exceeds b by >=0.05. If tracker SD<0.015 mm, mark clip insufficiently excited and count as failure (not silently drop). Also report pooled within-participant centered correlation, not as independent validation.
No 5s, device transfer, eye color, glasses, lighting, or fatigue claims from this pilot.

## Mechanistic prediction / adversarial interpretation
Common apparent magnification multiplies pupil and iris areas similarly; q may suppress scale artifacts relative to b, but pupil/iris segmentation at 32x16 can be underresolved, eyelid-occluded, and photometrically unstable. No guarantee that simple thresholds find anatomical pupil/iris.
Any null requires inspect frame coverage, luminance span, P/I distribution, low-variance Tobii traces, per-participant reversals, and whether the ratio removes true temporal response. Freeze a different cohort before tuning any thresholds.

## Cheapest next experiment
If pilot produces a reproducible positive q signal, replicate on previously unused participants and both eyes with device/scale/photometric stress. If negative, try segmentation-quality gating and explicit iris-boundary estimation on development participants only, then freeze unseen participants.
