# E002-705 — Prospective acquisition-manifest fail-closed gate

**Evidence tier:** executable acquisition integrity control, not empirical validation.

E002-704 specifies a participant-disjoint physical/human study. This run adds a machine-checkable pre-reference gate: `e002_705_acquisition_gate.py` rejects absent acquisition fields, malformed raw-file SHA-256 identifiers, invalid time/geometry uncertainty intervals, nonfinite quantities, ambiguous exposure order, negative dropped-frame counts, duplicate participant/session identifiers, and reference labels embedded in the prediction-side manifest.

Run `python research/observability/e002_705_acquisition_gate.py manifest.json` with a JSON object containing a nonempty `records` array of E002-704 acquisition rows. A passing result means **STRUCTURE_ONLY_PASS**. It does **not** authenticate clocks, source videos, shutter/velocity calibration, anatomical annotations, or consent; the output always marks provenance unauthenticated, human validation false, and production blocked. Invalid input produces a nonzero exit and **ABSTAIN_INVALID_MANIFEST**.

**Falsifiable implementation checks for independent replay:** delete any required field; insert `reference_status`; reverse a time interval; supply `NaN`, an invalid digest, or duplicate participant/session. All must fail. A valid synthetic manifest should pass structure only. Independent execution and hosted CI are pending; no tests are claimed as run.

**Important limitations:** this is not a cryptographic commitment to an independently witnessed acquisition, and its digest only identifies the exact supplied bytes. The gate does not replace E002-695 prediction locking, independently calibrated speed bounds, E002-703 physical capture, or E002-704 blinded held-out evaluation. No human or physical data were collected. Product remains `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.
