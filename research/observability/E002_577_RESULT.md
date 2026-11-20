# E002-577 | Hosted authentic-LPW source acquisition: positive transport result

Date: 2026-11-01. Primary kernel E002-371. Frozen protocol: [E002_577_FROZEN.md](E002_577_FROZEN.md). Hosted execution: https://github.com/sushxnthd/lucent/actions/runs/41244304472 (completed, success; inspected actual job logs). Executable: [e002_577_lpw_range_probe.py](e002_577_lpw_range_probe.py).

## What was independently observed

The runner fetched byte ranges from the original investigators' linked LPW ZIP at https://datasets.d2.mpi-inf.mpg.de/tonsen/LPW.zip, not from a third-party reupload. The ZIP central directory enumerated **66 eligible native video entries**. The prospectively fixed lexicographically first entry, `LPW/1/1.avi`, was extracted without downloading the 2.4-GB archive. The ZIP member CRC and uncompressed size checks passed, and FFprobe plus FFmpeg successfully decoded frames 0, 10 and 20.

| Field | Observed |
|---|---|
| Remote ZIP size | 2,576,433,029 bytes |
| Selected entry | `LPW/1/1.avi` |
| Member compressed bytes | 58,594,930 |
| Member uncompressed bytes | 59,663,314 |
| Extracted video SHA-256 | `158d8654ff9e19162ec7f1316eee3d3046024ad81b355b2b3e5f9e566f5abe86` |
| Native video dimensions | 640 x 480 |
| Native stream reported rate | 95/1 fps |
| Native stream reported frame count | 2,000 |
| Native stream reported duration | 21.052632 seconds |
| Frames decoded | 3 of 3 requested |
| Independent human anatomical labels | 0 |

The self-test passed central-directory parsing, bounded range extraction and CRC-corruption rejection. The video bytes and decoded human images remained in the ephemeral runner; no video, image, annotation, cache or artifact was uploaded to GitHub.

The original LPW authors describe 22 participants, 66 videos, approximately 95 fps and research-only noncommercial use: https://www.mpi-inf.mpg.de/departments/computer-vision-and-machine-learning/research/gaze-based-human-computer-interaction/labelled-pupils-in-the-wild-lpw . Source-linked HTTPS retrieval and ZIP CRC are **not an investigator-signed authenticity certificate**, and AVI stream metadata is **not** independently calibrated exposure timing.

## New scientific capability and limits

This removes the previous *data-access blocker*: a real source-linked high-rate human eye-region video can now be decoded within no-cost CI without downloading the full archive. It does **not** establish even one human blink event, one valid eyelid aperture, one physiological velocity upper bound, or one hidden-closure prediction. The chosen video was a deterministic transport probe, **not** a preselected held-out test participant. Pupil-center labels are not eyelid closure labels.

E002-575's corrected hosted synthetic packet tests also passed at https://github.com/sushxnthd/lucent/actions/runs/41244200508 . E002-576's 16 synthetic adversarial evaluator tests passed at https://github.com/sushxnthd/lucent/actions/runs/41244199805 , after fixing a syntax error exposed by the preceding failed hosted run.

## Next decisive experiment

Use the existing E002-574 participant-disjoint frozen selection on the *complete source manifest* and E002-575 native packet builder, privately. Recruit two independent blinded human anatomical raters, establish independent iris-diameter uncertainty, and run E002-576 on participant-held-out ratings. If actual high-rate CLOSED frames are observed between downsampled OPEN endpoints, that is positive evidence of index-decimation aliasing, **not** a certified ordinary-camera shutter-gap law. For E002-371's physical observability claim, still require synchronized photodiode/shutter measurements and a separately justified continuous-time eyelid-velocity ceiling. Do not treat an absence of annotated witnesses as a negative certificate.

**Evidence ledger:** real source-linked video acquisition 1; native frames successfully decoded 3; independent human rater pairs 0; authenticated physical shutter captures 0; certified continuous-time eyelid-speed ceilings 0; held-out physical closure predictions 0. Product `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
