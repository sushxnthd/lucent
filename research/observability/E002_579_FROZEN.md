# E002-579 | Prospective authentic-human-video motion-proxy falsification

Frozen 2026-11-01 **before** computing the real-video motion statistic. Primary kernel E002-371; does not modify the E002-573 held-out selection, E002-576 anatomy rubric or E002-567 physical study. Source: official LPW archive member `LPW/1/1.avi` (development participant 1), SHA-256 `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86`, 2000 frames, reported 95/1 fps. No held-out participant or frame will be accessed.

## Falsifiable empirical question
Does a purely image-based motion excursion observed in genuine 95-fps eye-region video disappear between the endpoints of a predeclared 3:1 temporal decimation? Does that proxy survive realistic image nuisances? This is **not** a blink detector, anatomical aperture measurement, shutter validation, or evidence for a physiological velocity ceiling. Its only legitimate role is a prospective negative-control / triage assessment. No labels, training, or post hoc thresholds.

## Locked image statistic
Decode all native frames in order using FFmpeg area downsampling to **80 x 60** 8-bit grayscale, without temporal interpolation. For frame `x_t`, center its pixels and normalize by Euclidean norm to `z_t`; abstain if the centered norm is below `1e-6`. Define `d(a,b)=1-dot(z_a,z_b)`, clipped to [0,2] only for floating-point rounding. For every consecutive native quadruple `i..i+3`, define `m_i=max(d(i,i+1),d(i+1,i+2),d(i+2,i+3))` and endpoint distance `e_i=d(i,i+3)`. Predeclare a **proxy-only** hidden-excursion flag if `m_i>=0.05` and `e_i<=0.02`. Count all three start phases `i mod 3 = 0,1,2`, and also report each phase's number of eligible quadruples, medians and 90th/99th percentiles of `m_i` and `e_i`. The threshold is an arbitrary engineering probe, not a physiological cutoff.

## Predeclared nuisance falsifiers
1. **Photometric**: apply positive affine intensity `1.3*x+20` to every second frame **in float before any clipping**. Normalized statistic should agree with baseline within numerical tolerance `1e-4`; otherwise reject the implementation.
2. **Spatial jitter**: shift every second frame one 80x60 pixel horizontally, using edge replication. Recompute proxy flags and counts. Do not reinterpret changes as physiology.
3. **Blur**: apply fixed 3x3 box filter with edge replication to every frame; recompute counts.
4. **Missingness**: mark every 20th native frame missing, and abstain for every quadruple containing one. Report eligible and abstained counts.
5. **Geometry and illumination**: no claim of anatomical correspondence, gaze control, eyelid landmarks, camera shutter or brightness calibration. The dataset itself includes gaze/illumination/eyewear variation; this analysis cannot stratify them reliably.

Primary endpoint: actual counts of development-video proxy excursions under each condition, plus stability of exact flagged quadruple identities. A result is scientifically informative even if **zero** baseline flags or all flags vanish under nuisances. In that case **kill** the proxy as a prospective human-review selector. No held-out evaluation or anatomical claim may be based on this run.

## Reproducibility and privacy
Reuse E002-577's source-linked bounded ZIP extraction and checksum, and E002-578's frozen source properties. Output aggregate JSON to hosted logs; never upload human video, individual images, private frame indices, per-frame scores, or identifiable review packets. CI dependencies: FFmpeg, Python 3 and NumPy. No source file or derived imagery committed. If source access fails, report acquisition failure and do not manufacture a result.

## Product consequence
Regardless of outcome: `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. A motion-proxy count cannot validate E002-371, certify closure absence, measure blink duration, PERCLOS, fatigue or sleepiness. Independent blinded human anatomical ratings and synchronized physical-camera/photodiode validation remain mandatory.
