# E002-257 execution — 2026-10-17

1. Inspected research branches and inherited workflow. E002-256 commit 47310cd3fc1c51bebcbeccc65a6f09e050254058 hashes nonexistent CI_RESULTS.json and CI_SOURCE_HASHES.json; decompose.py actually emits RESULTS.json and SOURCE_MANIFEST.json. This is a deterministic workflow-plumbing error, not a scientific failure.
2. Re-fetched both 51-participant public human summary CSVs through connected GitHub at pinned commit aa9bddf498a3b6e4104c2c000d2cc0c06a816aae; both source Git blob IDs matched.
3. Executed exact RMSE-from-moments decomposition in JS: median raw SD-normalized RMSE left 0.73203474497, right 1.06095378743; offset-oracle medians left 0.69288210724, right 0.72323694801. Right worse in 46/51 participant pairs, two-sided sign p=2.328e-9. Exploratory 0.7 raw threshold: left 16/51, right 1/51. All source-reported MAEs obey MAE<=reconstructed RMSE.
4. Executed 10,000-pair participant bootstrap with fixed xorshift seed 2572026 in JS: descriptive 95% interval for paired median right-minus-left raw NRMSE [0.25185067625,0.39333105548].
5. Tested full Python reference implementation's synthetic moment identity and deliberate MAE mutation locally. The shorter code committed to GitHub is awaiting its own remote CI run; do not transfer the local test claim to that unexecuted compact file.
6. Created isolated research branch research/e002-257-eye-specific-bias. Committed pinned audit, independent checker, synthetic mutation test, source manifest, both ledgers, negative gates and a corrected workflow with always-uploaded hashes/results.
7. Inspected Actions via available connector: PR-filtered commit run lookup and combined commit statuses returned empty. These endpoints cannot certify push-triggered workflow success or failure. Remote CI and its artifacts remain unverified.

**Smallest claim:** A third-party published webcam checkpoint exhibits a large, paired eye-specific absolute-scale error asymmetry, much of which is removed by reference-informed offset correction. This is post-hoc human aggregate evidence, not Lucent physiological waveform validation or a new observability theorem.

**Next high-information step:** Verify new Actions job/artifact and source SHA-256, then obtain independently synchronized RGB+tracker raw waveforms; avoid more aggregate-only claims.
