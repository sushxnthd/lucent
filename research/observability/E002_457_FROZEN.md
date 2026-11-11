# E002-457 — frozen directional observability and human velocity challenge (2026-10-26)

**Frozen before implementation.** E002-456's prospective instrument has successful hosted instrument-ci at run 40265300734 but no human anatomical witnesses. This experiment adds an independently falsifiable **asymmetric closing/opening** boundary and evaluates its implications with the previously authenticated Culemann et al. (2026) human peak-velocity CSV. It is not a new human anatomical trajectory experiment.

## Exact conditional law

Let instantaneous anatomical aperture a(t) be absolutely continuous with directional speed bounds -C <= a'(t) <= O almost everywhere, where C,O > 0. If endpoints a0,a1 > threshold c and the endpoints are feasible (-C*Delta <= a1-a0 <= O*Delta), a hidden crossing a(t) <= c is possible **iff** Delta >= (a0-c)/C + (a1-c)/O. This is sharp: descend at -C, ascend at +O, optionally dwell at c. The dimensionless number R = Delta / ((a0-c)/C + (a1-c)/O) is the crossing feasibility ratio. Exclude only if R < 1; equality is NOT excluded. For C=O=V and a0=a1=a, recover Delta < 2(a-c)/V. C and O are assumed hard bounds only within the theorem, not empirically certified.

Shutter-aware *sufficient* exclusion: for uniform symmetric exposure e, subtract (C+O)*e/8 from each measured shutter-averaged endpoint; for arbitrary nonnegative symmetric-support exposure, subtract max(C,O)*e/2. Also subtract aperture uncertainty, inflate Delta by 2*clock_error, then apply the directional threshold to these pessimistic endpoints. Do not call this sufficient rule sharp for averaged endpoints. Unknown exposure, asymmetric/rolling shutter, missing geometry, gaze, clock or nuisance calibration => ABSTAIN.

## Frozen falsification and empirical analysis

1. Test exact boundary analytically and by an independent piecewise-linear witness at equality, for C=O, C!=O, a0!=a1, swapped directional limits and impossible endpoints.
2. Generate independently verified piecewise-linear trajectories with signed slopes inside [-C,O], integrate shutter averages numerically, and attempt to find false exclusions. Longer shutter, greater measurement uncertainty or clock error must never strengthen exclusion.
3. Reuse the original checksum-verified Culemann et al. OSF Blinks.csv only when SHA256 is exactly 6248c00b3c2849115f913eb184821d05efe069dd081587a84472c054494bbc43. Keep original holdout subjects {3,6,9,12,15} and remaining 12 calibration participants. Peak opening velocity is interpreted as a **magnitude**; report original sign distribution, invalid and zero counts, and explicitly abstain if sign/units are not interpretable.
4. Train C as maximum estimated closing peak and O as maximum absolute estimated opening peak from 12 calibration participants. Count held-out closing, opening and either-cap exceedances at both blink and participant level. Report this as *same-study descriptive transfer*, not independent physiological validation.
5. For hypothetical equal instantaneous endpoints a0=a1=c+1 mm, compute the directional and symmetric (V=max(C,O)) critical gaps, plus conditional decisions at 30/60/120/240/480/1000 fps. These are illustrations conditional on sample extrema being hard bounds (an assumption **not supported** by the data). Quantify changed decisions; if none, preserve the negative result.
6. No raw human rows, identifiable videos, or private annotations may be committed. CI outputs aggregate counts only. Fail on wrong checksum, schema, invalid numerical values, or participant overlap.

## Release and provenance

Any synthetic valid crossing classified as excluded kills the proposed law/implementation. A participant-disjoint human velocity non-exceedance cannot establish universal C/O caps. Without independent hard-bound provenance and calibrated human anatomical reference, physical hidden-closure, blink duration, PERCLOS, fatigue and medical claims remain ABSTAIN_UNCALIBRATED. S21/S22 remain sealed. The restricted 400-fps FaceBase trajectories, EyeInfo 150-fps Google-auth DVC data and PNAS 120-fps rendered supplementary videos were checked as candidate sources; none supplies presently authorized, independently authenticated continuous eyelid-margin trajectories.

Primary literature: https://doi.org/10.3758/s13428-026-02984-4 ; https://osf.io/tud8a ; https://trackhub.facebase.org/2026/09/01/recent-release-clites-eyelid-kinematics-emg/ ; https://github.com/fabricionarcizo/eyeinfo ; https://pmc.ncbi.nlm.nih.gov/articles/PMC12358864/ .
