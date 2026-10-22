# E002-373 prospective human validation (NOT EXECUTED)

Paired native RGB (30/60fps, measured shutter timestamps) and independent >=240fps high-speed eye-reference with hardware synchronization. Measure normalized eyelid aperture, not inferred fatigue. Consent/ethics required for new recordings.

Calibration participants: estimate RGB shutter-mean error and a conservative within-session reference speed envelope; never treat observed sample maximum as a universal physiological bound. Freeze V, error r, theta and clock tolerance before holdout. Hold out >=8 participants and a distinct RGB device; target >=24 total adults with gaze ±20 degrees, glasses/no glasses, bright/dim lighting, motion, blur, occlusion. Preserve participant-grouped uncertainty.

For each gap, compute 1-d_max-VH/2 with eta=1-b+r and mark no-hidden-closure only if strictly >theta. Primary falsification: any reference-confirmed closure in a certified gap, or a holdout speed-envelope violation. Report certificate coverage, error rate and participant-cluster intervals. Controls: geometry-only, brightness-only, missingness-only, temporal-smoothness-only; test gaze, glasses, blur, rolling shutter, sampling and clock perturbations. A learned model is secondary.

No suitable unrestricted paired high-speed human dataset was acquired after two targeted searches. Kwon et al. 2013 (600fps, DOI 10.1098/rsif.2013.0227), 2019 smartphone 240fps study (PMID 30893187), and Kim et al. PNAS 2025 (DOI 10.1073/pnas.2508058122; 400fps raw FaceBase restricted) establish high-speed frontier but not a transferable universal speed cap. mEBAL2 RGB/NIR 30Hz cannot serve as a high-speed reference. No human evidence claimed.
