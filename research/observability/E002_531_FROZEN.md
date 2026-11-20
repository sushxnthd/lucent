# E002-531 FROZEN | Native-marker missingness can erase an independently real closure witness

Frozen 2026-10-29 on the existing Lucent E002-371 kernel, branch `research/observability-human-boundary`, draft PR #26. **This protocol precedes the executable experiment and inspection of any FaceBase participant files.** Evidence tier: synthetic instrument-pipeline identifiability test grounded in a documented published acquisition/processing procedure. No human measurements will be invented.

## External, pre-experiment source facts
Kim et al., PNAS 2025, DOI 10.1073/pnas.2508058122, https://pmc.ncbi.nlm.nih.gov/articles/PMC12358864/, methods: Vicon eyelid-marker trajectories acquired at **400 Hz** (2.5 ms native interval); 120-Hz HD video; marker tracking gaps **fewer than 10 samples** (reported as 25 ms) linearly interpolated; larger gaps excluded; trajectories then 10x upsampled by linear interpolation and zero-lag low-pass filtered at 20 Hz. The published raw EMG and marker data were deposited at https://doi.org/10.25550/88-28BJ. FaceBase announced release 2026-09-01; the dataset is **restricted-access human-subject data** with General Research Use and Not-for-profit Use Only restrictions. No approval/access is presumed.

## Frozen deterministic falsifier
- Native sample period: exactly 1/400 s; 80 frames, indices 0..79.
- Missing native markers: indices 30..38 inclusive (9 consecutive samples, 22.5 ms nominal missing sample duration); observed bracketing indices 29 and 39 are present and open, 25 ms apart.
- Closure threshold: normalized aperture `c=1/4`, with closure `a<=c`.
- World A: all native samples have `a=1`.
- World B: identical to A outside the missing interval; within indices 30..38, values are `4/5,3/5,2/5,1/5,0,1/5,2/5,3/5,4/5`. Between native samples use piecewise-linear interpolation; max absolute slope is 80 normalized units/s (a **hypothetical**, not human-certified velocity).
- Both worlds share exactly the same **observed** sample timestamps, values, and missingness mask. Fill missing values by linear interpolation between the observed endpoints, exactly as the cited paper says for gaps below ten samples.
- Frozen independent 25-fps point-sample surrogate: native indices `0,16,32,48,64` (phase zero) and `1,17,33,49,65` (phase one). This is a sampling surrogate only, not shutter-integrated video.

## Predictions and kill criteria
1. The true complete world B has **3 native samples** at or below c (indices 33,34,35), whereas world A has zero. Its piecewise-linear below-threshold dwell is **9.375 ms** (threshold crossings at 32.75 and 36.5 native indices); verify analytically, do not infer from count. [Correction rule: if this numerical prediction is inconsistent with exact linear crossing arithmetic, record a protocol amendment before tests; do not silently rewrite it.]
2. Both worlds yield exactly the same observed data, the same linearly imputed all-open series, and the same output under **any deterministic downstream upsampling/filtering** of that imputed series. Therefore postprocessed marker data alone cannot certify absence of a closure inside this missing span.
3. At phase zero the complete world B 25-fps point samples show no threshold closure; at phase one they show a threshold witness at index 33. The **imputed** series shows no closure in either phase.
4. The scientific decision must be `UNKNOWN_MISSING_NATIVE` for any closure-free assertion about a gap intersecting missing native reference frames. A deterministic imputer may produce a visualization, not a negative ground-truth label.
5. Falsify the claimed erasure if the observed nonmissing samples differ between worlds, if imputed outputs differ, if the complete B trajectory does not contain a closure, or if a rule using imputed values alone correctly distinguishes A/B. Preserve failures.
6. No 20-Hz Butterworth numerical result is claimed unless the published exact filter order/parameters are independently established; identical imputed inputs suffice to prove identical deterministic postprocessed outputs.

## Follow-on real human test (access-dependent)
Only if authorized FaceBase native, pre-interpolation 400-Hz marker streams become available: checksum raw files; document subject/trial IDs and access permissions; split participants 1-6 for exploratory calibration and 7-8 held out; derive a face-frame-normalized central marker aperture only if the necessary calibration/markers exist; preserve every native missing mask, and never use interpolated data to label a missing interval as a verified negative. Independently compare native 400-Hz positive witnesses against 25/30-fps point-sample surrogates and physical shutter/clock only if calibrated. All velocities are sampled finite differences, **not** certified continuous-time ceilings. Treat no-witness as censored, not a negative. Report all abstentions, behavior types and participant-disjoint results.

## Release decision
This experiment cannot establish a human physiological bound, camera exposure sensitivity, or fatigue. It can falsify a data-processing shortcut and justify a missingness-based abstention gate. Production remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`; Hush is not touched.
