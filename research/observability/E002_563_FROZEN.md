# E002-563 FROZEN | Original high-speed human-video acquisition and rate falsification

Frozen 2026-10-31 before implementation. Existing Lucent E002-371 kernel, branch `research/observability-human-boundary`, draft PR #26. This is **a source acquisition experiment**, not a human closure-exclusion validation.

## Predeclared external-source conflict

The 2025 original Guttmann-Flury, Sheng and Zhu *Scientific Data* acquisition methods state the Phantom eye video was recorded at **150 frames/s** to avoid data loss (DOI 10.1038/s41597-025-04861-9). A 2026 Zenodo CC0 rehost of original byte-preserved Phantom AVI files (DOI 10.5281/zenodo.18971758, Motor Execution, S01.zip) describes the same files as **~500 fps**. This conflict must be settled by native file inspection, not by selecting the larger advertised rate. A reported AVI frame rate is still not independent sensor-clock verification.

## Locked experiment and verdicts

1. Fetch exactly `https://zenodo.org/records/18971758/files/S01.zip?download=1` (reported 410,184,489 bytes; published MD5 `bce89dd9fbb67e27a656623aa27927e0`) in an ephemeral GitHub Actions Linux runner. Stream and verify MD5 before opening. Refuse archives exceeding 600 MiB, ZIP traversal, encrypted members or oversized AVI members. No human video, frames, XML or identifiers may be committed, uploaded as artifacts or printed.
2. Extract the lexicographically first `*_phantom.avi` from S01 privately. Use FFprobe to read `avg_frame_rate`, `r_frame_rate`, duration, codec and frame count. Compute the number of exact duplicate *adjacent decoded frames* in a deterministic small prefix, with an explicit `n/a` if decoding fails. This measures a codec artifact only; nonduplicate frames do not prove independent acquisition.
3. Rate decision: if both finite reported rates agree with 150 fps within 1%, classify `PAPER_RATE_COMPATIBLE_METADATA_ONLY`; if both agree with 500 within 1%, classify `REHOST_RATE_COMPATIBLE_PAPER_CONFLICT`; otherwise `UNRESOLVED_RATE`. Never claim 500 fps based on rehost text. Preserve any mismatch and refuse to use metadata as a certified reference rate.
4. Produce only a sanitized JSON report: verified archive MD5, file size, AVI codec/rate/frame count, prefix duplicate count, verdict, and explicit flags `sensor_clock_verified=false`, `anatomical_closure_verified=false`, `independent_raters=0`, `product=ABSTAIN_UNCALIBRATED`. Delete raw media before completion. No privacy-sensitive names or footage.
5. Test with synthetic local AVI/ZIP fixtures, corrupted archive and wrong-rate cases before hosted human acquisition. Hosted network failures are not evidence that the dataset is unavailable; preserve the failure.
6. **Prediction consequence**: the maximum reference sample spacing from the claimed acquisition rate is 6.67 ms at 150 fps versus 2.00 ms at 500 fps. A negative sampled frame does not certify continuous-time absence at either rate. The E002-562 sealed 30-fps positive-witness protocol may be used only after independent anatomical labels, original timing and physical provenance are established.

Stop if data acquisition or licensing conflicts emerge. No claims of measured human blink dynamics, no private image publication, no product release. Next step after a successful source probe: independently blinded annotation of an original positive eyelid-closure sequence and acquisition-timing verification.

Sources: https://doi.org/10.1038/s41597-025-04861-9 ; https://zenodo.org/records/18971758 ; https://www.facebase.org/help/faqs/ .
