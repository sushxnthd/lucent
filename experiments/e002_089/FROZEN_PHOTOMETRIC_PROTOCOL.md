# E002-089: Original-RGB photometric onset and anatomical visibility preflight — frozen before P_33
Date: 2026-10-10 UTC. Branch: research/e002-089-rgb-photometric-preflight.
Classification: DISCRIMINATION / SURPRISE / CAPABILITY-BUILDING.
Dataset: Brown Eye of the Typer (EOTT), initial dot-test original 640x480 webcam WebM, CRC-verified member extraction.
No human media will be committed. No user laptop, paid compute, or state labels.

## Development observation (not prospective)
P_54 original frame 1: global grayscale mean 5.708/255, 99th percentile 18, 0 detected faces. P_54 frame 80: global mean 184.772, 99th percentile 251, 1 face. Eight later sampled frames (80-632) have global mean 184.5-185.1. This was observed before freezing P_33 gates, and is exploratory.

## Prospective P_33 experiment (locked before reading RGB frames)
Hypothesis H1: P_54's extreme dark-onset-to-bright pattern is a shared EOTT recording onset photometric artifact.
Mechanistic prediction: P_33 original initial-dot-test frame 1 mean grayscale <=30, median of frames {80,160,240,320} >=100, and difference >=80 grayscale levels. Gate G1 passes only if all 3 conditions hold.
Hypothesis H2: P_33 stabilizes into anatomically inspectable face video after onset.
Gate G2: face detection returns >=1 face on >=3/4 frames {80,160,240,320}. Use Wolfram FindFaces with no tuning. If G2 fails, classify anatomy unobservable for this detector; no statement about ground-truth pupil visibility.
Gate G3: original ZIP member decompression yields 3337577 WebM bytes and CRC32 657022237. Frame count must be >320; otherwise experiment is invalid.
Measurement: grayscale 8-bit mean over all 640x480 pixels, no image enhancement. Frame 1 is initial frame. Later sampled frames are fixed. Do not select by observed results.
P_33 is an already-seen *reference* development participant, not a waveform holdout; P_01, P_02, P_07 waveform holdouts remain untouched.

## Anomaly mining if failure
If G1 fails, inspect whether P_33 is bright from the first frame, or has smaller onset transient, and whether first 5 seconds have a stable photometric regime. Compare initial 80-frame intensity timecourse on both development participants, without treating post-hoc patterns as prospective validation.
If G2 fails, inspect face location and brightness; do not automatically infer absent eyes.
The cheapest next discriminating test is RGB anatomical pupil/iris segmentation on the bright/stable portion of P_54/P_33, without using tracker labels for segmentation or selecting windows by agreement.

## Claim boundary
A photometric-onset artifact is a camera/recording measurement issue, not a new physiological law. It cannot prove or disprove five-second sleepiness/fatigue inference. Do not reclassify raw PupilSense millimetres as viable. The frozen E002-085 RGB/reference waveform protocol is unchanged.
