# E002-285 provenance and content-addressed evidence

Parent E002-284 evidence commit: a3d9c9b5bd219fef6285bfc497f6cde382603bde.
All cases deterministic, generated on 2026-10-18; no user laptop or paid API; no external human dataset.

Git blob SHA-1 for this branch's source and frozen evidence (from uncommitted tree edba579d2d8fb05505d99113a03cc0091636f625):
- experiment.py: 877806fe024e572ccf1da93c7b1790d0d019e703
- independent_check.py: dfeb79360337fb31ab6ae7d5655e2b7066238b75
- raw_cases.csv: 1bd3074a15c9b542a91c0fc1c7e12664071e99f5
- exact_counterexample.json: 7c2d255c9d3b1899278b603ab547e1ae7cea3f00
- PROTOCOL.md: b73077292e04ae887f6257847fea5bfbd9bbe6a2
- SCIENCE_PRODUCT.md: 5cc1ccec34893a1919e8a0d28825f50f405a5649

Local expanded reproducibility ZIP SHA-256: a1a7e6f4beb39149bfe6103f0f1a60a62d7208f1f7cfb6c8e159e7b795af7ad9. The ZIP has expanded source, all collision witnesses and SHA256SUMS; its source bytes are not identical to the compact branch implementation. Both independently implement the same boundary. Regenerate branch outputs with experiment.py, then run independent_check.py; compare computed outcomes to frozen raw_cases.csv.

Failed gates: no empirical Z,D,eps; no synchronized human paired RGB; no participant/device holdout; no field-level novelty.
