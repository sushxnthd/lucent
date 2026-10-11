# Lucent E002-098 — FROZEN local pupil photometric separability pilot

Date: 2026-10-11. Experiment type: DISCRIMINATION / CAPABILITY-BUILDING.
Source: original MEYELens Zenodo 20492528 CC BY 4.0; original JPEG frames and original pupil/eye PNG masks. The ZIP archive is 137,446,558 bytes (metadata). No phone, Tobii reference, or behavioral-state inference.

## Fixed samples (one frame from each of eight different recording prefixes)
1. eye 22_frame_000071_pic_2487
2. eye 9_frame_000161_pic_4227
3. camera0_20250717_153932_332_frame_000112_pic_112
4. eye 4_frame_000069_pic_3218
5. eye 15_frame_000114_pic_1253
6. pupillometry_frame_000422_pic_4784
7. eye 13_frame_000214_pic_926
8. eye 12_frame_000103_pic_637

The names were selected from archive central-directory filenames before any image pixel inspection. Pair `fullFrames/<name>.jpg` with `annotation/png/<name>.png`. Verify ZIP entry CRC through one-member reconstructed ZIP; verify original mask red/green pixel areas where possible. If unavailable, mark unavailable, never replace a sample after outcome inspection.

## Primary photometric discrimination (no fitted parameters)
- Pupil P: pixels where original red mask channel >=128.
- Eye E: pixels where original green mask channel >=128. Require P subset E, P>=50 pixels, E>=500 pixels, RGB/mask dimensions equal.
- Equivalent pupil radius r=sqrt(area(P)/pi).
- Immediate local annulus A = (dilation(P, circular disk of radius max(1,round(0.35*r))) minus P) intersect E.
- Require A>=50 pixels.
- Grayscale G=round(0.299 R+0.587 G+0.114 B) from original JPEG, clipped 0..255.
- Compute rank AUC for classifying P vs A using darkness score -G; ties count 0.5. Also median gray(P)-median gray(A).
- Fixed gate: at least 6/8 selected images eligible AND at least 6/8 have AUC >=0.80 AND median(P)-median(A) <= -5 levels. Report exact per-image outcomes, no substitution.
- Negative control: reverse polarity (+G), for which AUC should equal 1-AUC; this is a computation sanity check, not a biological negative control.

## Post-primary exploratory anomaly mining
Report pupil pixel count, annulus size, r, RGB channel AUCs, gray contrast, masks failing validity, and variation across recording prefixes. No optimizing threshold, annulus radius, or color channel against these 8 samples. A low AUC may reflect iris pigmentation, specular highlights, annotation conventions, or JPEG artifacts; do not infer eye color/glasses unless independently labeled. An AUC pass would establish only oracle-local photometric separability, not practical segmentation, pupil/iris ratio, temporal waveform fidelity, or 5-second state inference.

## Claim boundary and evaluation hygiene
One frame per prefix is not participant-wise held-out. Masks are oracle ROI information; AUC is an optimistic local separability diagnostic. Source-prefix names are not person IDs. No use of PupilSense absolute millimeters. No physiological breakthrough claims. Follow up with source-held-out real segmentation and synchronized RGB/Tobii waveform tests.
