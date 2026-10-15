# E002-214 | External-human fixed-checkpoint coverage frontier
## Single active question
Can a geometry/photometry-normalized **ordinary RGB pupil/iris temporal waveform** reproduce synchronized same-eye native eye-tracker pupil diameter under participant/device/lighting/glasses holdout, and can nuisance-adjusted image information predict rejection?
- **Signal/reference:** RGB anatomical pupil/iris change vs native-time same-eye eye-tracker pupil diameter (mm).
- **Current frontier:** reference availability, timing, blur and geometry boundaries established conditionally; no certified RGB/native-tracker five-second human waveform result.
- **Scalar observability:** participant-bootstrap lower Pearson waveform correlation bound; separately frozen lag, amplitude, NRMSE, nuisance superiority and prospective >=75% coverage.
- **Strongest confound:** jointly variable pupil pixel scale, blur/contrast, gaze, illumination and clock offset.
- **Decisive falsification:** prospective waveform underperforms strongest brightness/geometry baselines or violates holdout gates.
- **Publishable success:** >=8 untouched paired humans, device/lighting/glasses holdouts, independently verified lag and nuisance controls, mechanism-derived unseen failure boundary, prior-art audit.
- **Product success:** >=75% prospectively accepted participants without outcome-based exclusion or gate relaxation.
- **Kill:** three nondiscriminating primary runs, or prospective waveform failure; switch dataset path after two blocked accesses.

## This run: preregistration scope
Source pinned BEFORE this derived-summary audit to CondadosAI commit `aa9bddf498a3b6e4104c2c000d2cc0c06a816aae`, original EyeDentify/PupilSense work credited to Shah et al. External aggregate is **not** an untouched holdout or a five-second waveform test.
Diagnostic r thresholds = [0,.3,.4,.5,.6,.65,.7,.75,.8,.85,.9]; illustrative amplitude-ratio diagnostic [0.75,1.25]. These are exploratory and **must not** be relabelled frozen Lucent thresholds. Best-eye oracle is an optimistic *upper bound* for a fixed pretrained checkpoint evaluated on these 51 participant aggregates.
Read published per-participant r, gt_std and pred_std for each eye; no new model training, no access to original human RGB or tracker traces. Compute participant counts for both-eye and oracle best-eye r, amplitude+correlation gate, and exact 75%-coverage r frontier. Check original Git blob hashes and commit pin. An independent implementation must verify and reject mutated output.

## Source collision
EyeDentify (WACV 2025) and PupilSense (ETRA 2025) already provide webcam-based pupil diameter prediction. A separate Aug 2026 reproduction reports 424k predictions and explicitly proposes pixel measurement + physical-scale conversion. Lucent **cannot** claim webcam pupil diameter regression, iris-scale correction, or model-to-browser port as novel. Differentiation must be prospective **selective** waveform certification with valid clock, uncertainty and nuisance/geometry rejection, if independently demonstrated.

## Limitations
Correlations pool frames across many 3-second, light-stimulated sessions, not native continuous 5-second waveform. Third-party aggregate numbers are not an independent reproduction of the checkpoints; released checkpoint's training split unknown. The external data have one recording setup; no device/glasses holdout. An r=.7 diagnostic is not a Lucent frozen gate. Human subject image data are not redistributed.
