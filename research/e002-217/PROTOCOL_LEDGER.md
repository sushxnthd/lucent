# E002-217 | Release provenance and measurement kernel
2026-10-15 UTC. Freeze before reading archive outcomes.
## Active question
Can a public, author-linked EyeDentify release supply a **native-time, same-eye pupil diameter reference** plus synchronized ordinary-RGB frames, so a prospective five-second waveform test is scientifically meaningful?
- Exact signal/reference: geometry/photometry-normalized RGB pupil/iris temporal change vs native-millisecond same-eye Tobii pupil diameter in mm.
- Current frontier: E002-216 proved a source-code three-second fold is non-injective; whether distributed files use that revision remains unverified. Previous human reference availability alone does not validate RGB.
- Scalar observability: lower participant-bootstrap bound on within-window Pearson correlation, separately frozen lag (<=100ms after clock-error certification), amplitude, NRMSE, nuisance superiority and >=75% prospective coverage. No new thresholds optimized here.
- Strongest confound: source reference folding/timebase, then focus, iris pixel scale, illumination, gaze and eyelid occlusion.
- Decisive falsification: genuine native pairs fail frozen waveform gates against geometry/brightness baselines on untouched participant/device/lighting/glasses holdout.
- Publishable success: >=8 untouched paired humans, independently checked reference/timebase, mechanism-predicted unseen failure, prior-art audit, and relevant holdouts.
- Product threshold: >=75% prospectively admitted participants without oracle eye or trial selection.
- Kill: two blocked attempts on this public Kaggle release path trigger alternate source; three nondiscriminating primary runs reformulate; prospective waveform failure kills this observable.
## This run's decision protocol
Probe public author-linked Kaggle metadata and at most 370 MB of release bytes, using stdlib and no authentication. Hash complete downloaded archive; list file extensions, candidate timestamp/reference filenames, and up to five CSV headers; inspect one nested ZIP without extracting images. If inaccessible, mark infrastructure block, not scientific failure. A ZIP manifest, even with CSV, NEVER proves native timestamps or synchronization. No released images, human waveforms or participant identifiers are redistributed.
## SCIENCE
Uninspected source-to-release lineage is the blocking uncertainty. If release contains only image crops and processed labels, it is inadequate for native-time five-second waveform certification. Source-level fold proof is conditional and must not be overgeneralized.
## PRODUCT
Keep Lucent a selective RGB instrument. Reject temporally untraceable labels, don't train a fatigue predictor on this material, and pivot to independently time-anchored capture when this source fails.
## Controlled wildcard
Use 10% of cheap inspection to identify unexpected raw timestamp or native tracker files inside nested archives. No evaluation on human waveforms is touched.
## Evidence/provenance
Original code blob SHA-1 f46d7ae369a62596f7044ca647d361c38fcb16ea; E002-216 Actions 38783027333 success on 2026-10-15. Source https://github.com/vijulshah/eyedentify and official Kaggle link https://www.kaggle.com/datasets/vijuls/PupilDiameterDatasets . Results are generated as RELEASE_PROBE.json by Actions; until completion this branch contains protocol and executable checks, not archive outcomes.
