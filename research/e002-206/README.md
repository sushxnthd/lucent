# E002-206 — Original-human reference coverage

Active question: does a prospectively fixed same-eye, native-time five-second pupil reference window pass 95% finite-positive pupil validity and a maximum 26-ms gap including both endpoints? This is a reference-quality necessary condition, not an RGB physiology test.

SCIENCE: E002-204 Actions 38695030636 verified that 30/30 source-defined trial counts match original pupil-valid flags and positive pupil diameter; E002-205 Actions 38699949377 verified an endpoint-censoring defect in the original admission gate. Original-human endpoint-aware coverage is not yet known.

PRODUCT: A 5-second same-eye reference must reject boundary-censored windows; the minimum useful accepted coverage remains 75%. Failure must not be interpreted as RGB failure. No fatigue inference is supported.

Frozen test: original 15 participant_001..015 image_01_1 TSV records; no eye switching, no post-hoc threshold tuning. Verify archive MD5 5e04a7b5e50f7508775e1daea527246b and metadata MD5 369d9446b62fd00888a6d51e152697bd; record SHA256 per source. Independently replay compact timestamps and pupil-validity flags. Preserve failures and CI state. Primary RGB-versus-tracker correlation/lag/amplitude/NRMSE gates remain frozen. Prior art: ordinary missing-data coverage arithmetic; no novelty claim.

Current state: research branch created; workflow and executable not yet published. Scientific gates untested. Next step: original human edge-aware admission and participant coverage.
