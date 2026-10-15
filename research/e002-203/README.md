# E002-203 — Sharp finite-window reference-admission bounds

**Science:** For n source samples with l left-valid and r right-valid, the number of simultaneous valid samples in a w-sample window is bounded sharply by max(0,l+r-2n+w) and min(w,l,r). For one eye with k valid samples, sharp bounds are max(0,k-(n-w)) and min(w,k). Proof: at most n-w valid samples per eye can be placed outside the window; align valid sets for maximum intersection and disjoint their invalid sets for minimum.

**Conditional 600-sample results (>=570 valid samples for 95%):** binocular 4 guaranteed / 10 maximum possible of 15; left 9/11; right 8/10; oracle fixed eye chosen using each trial's totals 10/11. Thus the pre-existing E002-176 70%-of-15 coverage gate is unattainable with *simultaneous binocular* source-defined validity, even in the best placement. An oracle best-eye policy may reach 11/15 but is not a prospective deployment policy.

**Critical provenance:** Source is E002-202's publisher-MD5-verified MCFW-Gaze v3 data_loss_per_trial.csv (820,609 bytes; MD5 369d9446b62fd00888a6d51e152697bd). This file is derived, not a raw TSV. Whether n_valid_trial_samples corresponds to pupil_valid, gaze_point_valid, or another criterion remains UNVERIFIED. The Tobii data schema exposes separate pupil and gaze validity flags. Source data are not synchronized ordinary RGB video.

**Product:** Do not require two-eye simultaneous validity when the scientific target is same-eye pupil diameter. Use a prospectively fixed same eye and report per-eye coverage. Do not apply the conditional published source-defined bounds as pupil-validity exclusions without raw TSV semantic comparison. No five-second fatigue claim.

**Primary kernel unchanged:** RGB pupil/anatomical-iris temporal waveform versus native-time synchronized same-eye tracker diameter. Scalar: held-out participant-bootstrap lower Pearson r, with frozen lag, amplitude, NRMSE, nuisance superiority and >=75% accepted coverage. Strongest confounds: photometric edge bias, blur, gaze/pose, synchronization. Publishable only after >=8 untouched participants, participant/device/lighting/glasses holdouts, independent checker, mechanism prediction and prior-art audit. Kill after three non-discriminating runs or failed prospective valid evaluation.

**Failed gates:** source-defined binocular >=70% reference coverage FAIL (upper bound 10/15); mapping to pupil-validity NOT TESTED; 600-sample native-time window NOT VERIFIED; RGB waveform NOT TESTED; device/participant holdouts NOT TESTED.

**Prior art:** classical set-intersection/Fréchet bounds; not claimed as novel theorem. Original Tobii API: https://developer.tobiipro.com/tobii.research/matlab/reference/2.1.0.3-alpha-gd8b35e1b/Gaze/GazeData.html. Dataset: https://zenodo.org/records/20300972.

**CI state:** Local independent exhaustive checker passed. No E002-203 Actions execution is claimed. Prior original-human run 38507882731 failed at an old parser alias and its checker accepted zero human observations; this is an infrastructure failure, not physiological falsification.

**Next decisive experiment:** Compare source-defined counts against raw TSV pupil_valid and gaze_point_valid for all 15 selected files, then execute the repaired same-eye reference protocol and ultimately untouched synchronized RGB/tracker waveform evaluation.

**Wildcard:** Source Croissant schema lists distinct gaze-point and pupil validity flags, so the metadata's precise predicate must be checked rather than inferred.

**Smallest claim:** A sharp *conditional* source-defined 600-sample eligibility ceiling for the E002-176 selected 15 trials, not a bound on RGB pupil recovery.
