# E002-708 | Hosted regression verification and evidence boundary (2026-11-07 UTC)

## Verified independent runner execution

GitHub Actions [run 42404315807](https://github.com/sushxnthd/lucent/actions/runs/42404315807), workflow `E002-707 strict manifest regression`, head `e9098ce019762e7428d0636ac1fabc9cade1182a`, completed **success**. The `regression` job and `Run fail-closed manifest regression` step both completed **success**, as independently checked using the GitHub Actions jobs endpoint. This resolves the prior status of committed-but-unexecuted regression tests. The test file contains 11 `test_*` cases; the job API does not independently disclose per-test results, so do not infer a precise executed test count solely from the job summary.

## Scientific interpretation

This is independent hosted *software regression execution*, not an independent scientific replication. The validator returns `STRUCTURE_ONLY_PASS`, never an authenticated-blindness or physiological-calibration certificate. A malicious or simply mistaken operator can supply structurally valid but false camera timestamps, speed-source descriptions, or recording digests; schema checks cannot verify physical truth. In particular, `speed_ceiling_source` is an unverified string, not an independently measured upper velocity envelope. No valid hidden-closure exclusion follows from manifest acceptance.

## Next falsifiable experiment

Use E002-703/E002-704 frozen acquisition protocols: synchronized high-rate truth with ordinary-camera exposures; independently calibrate speed and timing bounds on development subjects/physical targets; freeze predictions before participant-disjoint high-rate labels; report false exclusions and nuisance-stratified abstention. If no physical access, publish the precise blocked dependencies, not another synthetic validation claim.

Evidence tier: hosted CI regression PASS; physical acquisitions 0; participant-disjoint human validations 0; product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
