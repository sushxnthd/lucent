# Provenance, CI and scientific gates — E002-279

- Created on 2026-10-18 from E002-278 branch head 077d0866678fd96a76af20e4c69601ff3200f932.
- First evidence commit: 1ed96e0f8ed480c39404b75e64081a23c2478611.
- First dedicated GitHub Actions run 39108885770 completed SUCCESS; it executed experiment.py and independent_check.py and uploaded a synthetic raw/derived JSON artifact (artifact 12128979759, digest sha256:80a557254c17a6091d94aa469c37c2e1f0658258ee453a10fb6a775941caa176). This is execution verification, not human validation.
- This follow-up adds an explicit frozen-results check and includes SHA256SUMS.txt in the uploaded artifact. The workflow is triggered on branch pushes; inspect the run for this commit before claiming it passed.
- Local independent expanded implementation (not byte-identical to compact committed implementation) also passed 9 LP replays and 3 mutation tests. Local package /mnt/data/lucent_e002_279_nuisance_span.zip; original expanded source SHA256 1be95695715510d5a386d1049c7d5f9b69beb55515fd3a1143a9763b6facd40a; local expanded results SHA256 ce098423e7e15820ca90396d87aa2202472a3b39d2ff12ba16614c8da904a651. Do not substitute those hashes for the committed compact script's hashes.
- Dataset provenance: no human frames or eye-tracker reference; synthetic stimuli with fixed NumPy seed 279. No user hardware used, no API spend.
- Failed scientific gates: no physical RGB photometric-transfer calibration; no device-specific error bounds; no untouched human reference; no participant/device/glasses holdout; no field-level novel mathematical claim.
- Strongest supported claim: exact conditional nuisance-subspace nonidentifiability and a synthetic artifact-only false-certification adversary under an omitted photometric nuisance channel.
- The full 120-frame synthetic vectors and LP witnesses are generated in results.json and retained in the dedicated workflow artifact; a small exact-rational witness is committed directly as exact_counterexamples.json.
