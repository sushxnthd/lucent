# E002-172 original-human normalization audit

Source: 17,903 previously annotated eye-mask frame pairs in 26 recording groups. This is not RGB/tracker validation.

One-frame: 86.82% exact normalization-choice certificate coverage, zero disagreements among 4,151 certified pairs. Group-held-out geometry gate: 5/3,320 disagreements (0.151%) at 69.44% coverage; frozen 70% coverage requirement failed.

Thirty-frame: 69.44% exact certificate coverage; geometry gate 244/2,845 disagreements (8.58%) at 70.46% coverage, failing the 5% risk requirement.

The exact certificate ensures only agreement between two mask-derived normalizations, not physiological accuracy. Full local package includes source SHA256, frozen protocol, code, 53,709 predictions and independent checker. No new CI run claimed.
