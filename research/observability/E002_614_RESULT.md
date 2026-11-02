# E002-614 RESULT | Bind blinded reviewer exports to original frame bytes

Date: 2026-11-03. Parent: E002-371. Branch `research/observability-human-boundary`, draft PR #26. [Frozen protocol](E002_614_FROZEN.md) committed first at `40df8cd`.

**Evidence tier: locally executed synthetic packet-integrity experiment + implemented offline human-study instrument. No human ratings or physical camera measurements.**

## Failure mode and correction

The original E002-598 reviewer checked 640x480 PNG decode, filename, expected frame count and clip mapping, but not the actual frame bytes. A different 640x480 image with the same name could be annotated and exported as if it belonged to the owner-prepared packet. This is a study-custody and source-attribution defect, not a demonstrated anatomical error or a new measurement theorem.

E002-614 adds a private Python owner-side packet builder, a browser-side SHA-256 check of **every** original PNG before the first rating, a deterministic packet digest, a bound export field, and a separate private auditor. An owner must freeze and retain the packet digest independently before reviewing. The existing unbound templates remain readable for demonstrations but export `UNBOUND_DEMONSTRATION_ONLY`, never an authenticated evidence claim. The auditor refuses unbound exports. Browser WebCrypto absence and any hash mismatch refuse bound loading.

The canonical packet digest is SHA-256 of the UTF-8 concatenation, in lexicographic key order, of `clip::frame<TAB>lowercase_image_sha256<LF>`. The manifest contains only blinded clip/frame keys, not source identities. It must stay in the private reviewer workspace. The code, not any human images, is committed.

## Executed checks

- **Local Python**: 9/9 synthetic tests passed using 60 generated 640x480 PNGs. Exact packet, stable digest, changed frame, changed manifest, missing frame, extra frame, unbound input, matching export and unbound export were exercised.
- **Browser VM / independent Node SHA-256**: adversarial same-filename byte-substitution, exact match, bad digest, missing digest, partial manifest, and legacy unbound labeling have been added to the actual E002-598 HTML regression suite. **Hosted execution pending at this report's creation; no pass claimed.**
- **Dedicated CI**: `.github/workflows/e002-614-packet-binding.yml`, GitHub Actions run [41504036256](https://github.com/sushxnthd/lucent/actions/runs/41504036256) queued at last check.
- The source and packet hash cannot prove that the owner is trustworthy, the reviewer is independent, the participant consented, the camera clock is calibrated, or the images came from the declared sensor. External custody and precommitment remain necessary.

## Actual human-source acquisition status

The previously frozen E002-605 public Mendeley 100–110-fps dataset attempt did run in hosted Actions [41492594237](https://github.com/sushxnthd/lucent/actions/runs/41492594237), but the source API returned **HTTP 401 Unauthorized**, `recognized_events=0`, `source_access=ABSTAIN`. The job's green CI result means fail-closed code execution, **not** successful human-data acquisition. This is a source-access negative result and should not trigger repeated metadata archaeology. The underlying 2019 dataset remains [Alsaeedi, Mendeley Data v1](https://doi.org/10.17632/9yzdnng594.1). Authorized original human data or actual synchronized optical capture remains the scientific bottleneck.

## Private reproduction

```bash
python research/observability/e002_614_packet_bind.py bind --template PRIVATE/BLANK_ANATOMICAL_RATINGS.json --images PRIVATE/ARM_0 --output PRIVATE/BOUND_RATER_TEMPLATE.json
python research/observability/e002_614_packet_bind.py verify --template PRIVATE/BOUND_RATER_TEMPLATE.json --images PRIVATE/ARM_0
# Reviewer opens research/observability/e002_598_offline_rater.html locally, loads bound template and matching private PNG folder, exports private JSON.
python research/observability/e002_614_packet_bind.py audit --template PRIVATE/BOUND_RATER_TEMPLATE.json --images PRIVATE/ARM_0 --ratings PRIVATE/REVIEWER_EXPORT.json
```

No private files should be uploaded to GitHub. Reviewer B needs an independently assigned packet and separate blinded review. The independent custodian should precommit the packet digest, participant split and shutter/clock evidence before either reviewer sees frames.

## Decision

This closes a **provenance instrument gap**, not the central E002-371 empirical validation gap. Independent human anatomical rater pairs: **0**. Physically calibrated shutter/clock captures: **0**. Independently certified continuous-time human velocity ceilings: **0**. Participant-disjoint physical hidden-closure predictions: **0**.

Lucent `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush branch and draft PR #45 unchanged. Do not call this a scientific breakthrough, independent human validation, or release readiness.
