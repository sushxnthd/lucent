# E002-269 CI and provenance state (2026-10-18)

- Branch: research/e002-269-blind-waveform-replay.
- Original E002-267 evaluator: Git blob c97fcdc77ca27235e5dc8186529cdbd3e87f6bd4.
- E002-268 strict guard: Git blob 2521c4a1d0f9eec457dcd03dcab49bafc386f144.
- Synthetic fixture: 5400 CSV rows, SHA-256 ada76e94707a34f3fb86c6148ec1c2008e8851cc992f6abc35c267b15d758ebb.
- Local execution: 5 regression tests passed, independent algebraic checker passed, deterministic fixture replay passed.
- Remote dedicated E002-269 workflow: creation blocked by connector safety; remote E002-269 tests NOT VERIFIED. Inherited workflow success must not be counted as E002-269 test success.
- Scientific human RGB/reference result: NOT RUN; no EVE participant bytes.
- Files in this branch: executable scorer, fixture generator, five tests, independent checker, derived summary, manifest, ledgers and failed gates.
- Next plumbing attempt: use a permitted workflow-writing path or externally rerun the three commands in README; never infer CI success from a source-check workflow.
