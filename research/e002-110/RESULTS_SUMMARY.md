# E002-110 original-data Python replication

GitHub Actions run: https://github.com/sushxnthd/lucent/actions/runs/38146167842

PASS: 9/9 frozen numerical comparisons with prior Wolfram results using CRC32-verified original Zenodo 18429496 IR CSVs. Sub1/Sub2/Sub3 area contrasts: 0.3656787044894243, 0.346731751657817, 0.3758042065446858. Held-out center-y correction ratios: 0.5339794176212427, 0.697585797591852, 1.093611893453697. Intended 1-Hz response retention: 0.48388382020788595, 0.47379594261647173, 0.5996964615440774. Center correction frozen gate still FAIL in 0/3. Four fixture tests passed. Initial parser failure from a blank center annotation was repaired by treating it as missing under the existing >=80 valid-frame rule; no imputation or gate change. No RGB, independent tracker, fatigue, or novelty claim. Full archive MD5 unverified.
