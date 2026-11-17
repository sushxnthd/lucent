# Lucent alpha: hosted regression execution evidence (2026-11-17 UTC)

Evidence tier: **hosted automated behavioral test**, not physical-device acceptance, clinical validation, or release approval.

- Existing research branch: `research/observability-human-boundary`; draft PR #26.
- Tested source commit: `87a1c78efb4249867a3b131a712f1f92745d2c27`.
- GitHub Actions workflow: **Lucent alpha regression**.
- Pull-request-triggered run: https://github.com/sushxnthd/lucent/actions/runs/43985727099 ; completed **success** (GitHub API inspected 2026-11-17).
- A second run for the same commit also completed **success**: https://github.com/sushxnthd/lucent/actions/runs/43985717178 .

This resolves the prior uncertainty about whether the Node regression harness actually executes in hosted CI. It does **not** establish that every intended scenario has an adequate assertion; it does not establish physical-device timer accuracy, browser compatibility, response-latency validity, diagnostic ability, fatigue inference, or camera observability.

## Consequence and release boundary

The offline five-trial reaction-time demonstration may now be described as **hosted-CI-tested at this commit**, but remains an uncalibrated self-observation aid, not a validated fatigue measure. Retain explicit abstention for camera-derived fatigue and E002-371 hidden-closure assertions. Do not tag as an externally validated alpha until real browser/device acceptance, reproducible packaging, and a release checklist are verified.

## Next discriminating work

1. Independently run on physical mobile and desktop browsers, measuring stimulus scheduling and elapsed-time accuracy against an external reference.
2. Execute the frozen E002-371 held-out human shutter-gap predictions with independent velocity and clock calibration, or document the bounded physical-instrument substitute.
3. Keep negative results and nuisance failures visible; do not infer physiological validity from CI success.
