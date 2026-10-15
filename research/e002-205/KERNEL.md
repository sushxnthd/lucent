# Lucent E002-205 — Reference edge-censoring boundary (15 October 2026)
## Active question
Can the E002-204 native-time same-eye tracker admission gate accept an interval that is unobserved for longer than its declared maximum gap? This is a reference-quality preflight nested under the primary RGB pupil observability question.
- **Exact signal/reference pair (primary):** geometry/photometry-normalized ordinary RGB pupil/anatomical-iris waveform vs independently synchronized same-eye eye-tracker pupil diameter. **This run:** deterministic binary pupil-validity sequence vs the E002-204 native-window admission predicate.
- **Frontier:** E002-203 finite-window marginal bounds and E002-204 native timestamp code. Human pupil-validity semantics and RGB observability are not verified.
- **Scalar:** maximum unobserved interval including both declared 5-second boundaries; primary remains participant-bootstrap 95% lower Pearson r plus frozen lag/amplitude/NRMSE.
- **Strongest confound:** 95% coverage and small *interior* gaps do not bound missing endpoints. Primary: lighting/blur-dependent edge bias, gaze pose, synchronization.
- **Decisive falsification:** a 570/600-valid 120-Hz reference with >100 ms boundary gap nevertheless passes the old <=26 ms interior-gap gate.
- **Publishable success threshold:** untouched >=8 paired human participants with participant/device/lighting/glasses holdouts, independent checker, nuisance superiority, prior-art audit, unseen mechanism prediction.
- **Product relevance:** reject edge-censored reference windows; retain >=75% accepted coverage on untouched humans with calibrated abstention.
- **Kill:** reject this gate change if it fails source replay or does not improve actual temporal reference integrity; kill/reformulate primary after 3 non-discriminating runs or prospective valid human waveform failure.

## SCIENCE
Exact sharp finite-sampling construction: at 120 Hz, 600 samples in [0,5), 570 valid samples can all occur after 30 invalid samples, leaving 250 ms before the first valid sample, or before 30 invalid trailing samples, leaving 31/120=258.33 ms between last valid sample and declared window end. Consecutive valid samples remain 8.33 ms apart, so the E002-204 gate passes. Four independent counterexample patterns tested; 9 synthetic patterns total. This is basic combinatorics, not a novel physiology theorem. No raw human pupil or RGB results.
## PRODUCT
Replace interior-only max-gap with maximum of first-boundary gap, interior gaps, and last-boundary gap. Keep both original and repaired gates in reproducible evidence. The 26 ms cap is inherited from E002-204, not empirically optimized. Do not relax correlation/lag/amplitude/NRMSE or promote fatigue inference.
## Provenance / controls
Original E002-204 source GitHub blob SHA: d7cfbea86c38f98bcdceac12ac16b04127bbef88. Public source MCFW-Gaze v3 https://zenodo.org/records/20300972, archive MD5 5e04a7b5e50f7508775e1daea527246b, metadata MD5 369d9446b62fd00888a6d51e152697bd. No original dataset downloaded in this experiment. Executable synthetic TSVs have per-case SHA256 in results. Independent checker uses separately reconstructed strings and exhaustive small-n sharp-bound enumeration. Prior art: basic missing-data interval coverage; no novelty claim.
## Wildcard (~10%)
The first-4-invalid case shows failure even at 596/600=99.33% coverage: first valid is 33.33 ms after window start, violating the declared 26 ms maximum gap.
## Gates
Synthetic source replay: must PASS; independent 9-case checker: must PASS; human pupil semantics: OPEN; paired RGB: OPEN; device/lighting/glasses holdout: OPEN; fatigue: PROHIBITED.
