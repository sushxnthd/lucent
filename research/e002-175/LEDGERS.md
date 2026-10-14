# E002-175 — SCIENCE / PRODUCT ledgers

SCIENCE
- Existing: E002-173 conditional pixel-bound certificate; E002-174 prior-art collision; ordinary-RGB waveform fidelity remains unmeasured.
- New source prospect: MCFW-Gaze v3 has 15 participants and 120-Hz native pupil diameter, timestamps and validity flags; it is tracker-only, not eligible for RGB/reference waveform evaluation.
- Frozen QC question: whether public metadata fields named proportions are numerically admissible on [0,1]. A violation establishes a metadata-label/derivation issue only.
- Never infer actual packet loss, eye-tracker corruption, pupil physiological validity, or RGB observability from QC summary failures.

PRODUCT
- A validated fraction can be used for *candidate trial triage*, not waveform certification.
- An invalid fraction must be rejected as a probability; compute loss from raw validity and timestamps instead.
- No fatigue score or five-second state feature until real RGB+reference holdout passes.

CI / access
- Branch contains protocol, executable fetch+audit, independent checker, source hashes, and Actions workflow.
- CI outputs include downloaded raw metadata, manifest, aggregate results, and failed scientific gates as artifacts.
- GitHub Actions may fail for network/infrastructure reasons; classify separately and preserve branch.
