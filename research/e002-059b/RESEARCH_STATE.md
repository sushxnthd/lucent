# E002-059B — oracle normalized pupil-area ratio, gaze-condition audit (2026-10-09)

**Exploratory, NOT an untouched evaluation.** Reanalysis of E002-057's previously inspected 15 annotated RGB images from a single held-out MOBIUS participant. All images are phone 1, indoor; 8 left eye, 7 right eye. The upstream sample source is oocular/ready at commit dc0b020eb1ca1ab8966c4c085b9daba3310e1efd.

Dimensionless **oracle-mask** ratio: r = sqrt(N_pupil/(N_pupil + N_iris)). This is not a validated physiological diameter and uses privileged annotations.

Observed r range: **0.381064–0.553724** (max/min **1.4531**).
Within-eye, same-gaze replicate mean |delta r|: **0.025586** (7 pairs).
Within-eye, different-gaze mean |delta r|: **0.066831** (42 pairs), **2.612x** larger.
Exact conditional gaze-label pairing enumeration: **13/11,025 = 0.001179** (one participant, NOT a population p-value). Seeded 20,000-permutation approximation p=0.00135.
Pooled ratio/ROI-brightness Pearson r = -0.0745. Eye-side-by-gaze orderings differ. Leave-one-gaze-out contrast remains positive.

**Interpretation:** The area-normalized proxy varies by labelled capture condition even with oracle masks; projection, occlusion, genuine physiological variation, illumination, acquisition order and annotation cannot be separated in static photographs. No causal gaze effect is claimed.

**KNOWN:** this within-person condition association and prior E002-057 frozen negative gates.
**BELIEVED:** pose/occlusion and photometric quality must be controlled for a dimensionless RGB waveform.
**CONFLICTING:** mathematical scale normalization is not equivalent to physiological invariance.
**FALSIFIED:** no causal or population hypothesis; near-constancy of this proxy within this sample is contradicted.
**ANOMALOUS:** eye-side-specific gaze ordering; little pooled brightness correlation.
**UNTESTED:** tracker-verified true pupil, 5-second waveform, new participants/devices, fatigue/sleepiness/alertness.

**Next DISCRIMINATION:** synchronized repeated gaze+lighting ordinary RGB and eye-tracker diameter with frozen person-wise waveform gates. Keep 10–15% cheap development probes for unknown interactions. No threshold retuning, no PupilSense negative-result reversal.

Full reproducibility package is provided in the ChatGPT conversation as lucent_e002_oracle_gaze_audit_059.zip. This branch contains a research record; no GitHub CI or independent new-human replication is claimed.
