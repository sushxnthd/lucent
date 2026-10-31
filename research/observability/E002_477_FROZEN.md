# E002-477 FROZEN — independently timed optical acquisition ingest, not another shutter theorem

Date: 2026-10-27. Kernel: E002-371. Branch: `research/observability-human-boundary`. **Frozen before implementing or executing the E002-477 validator.** Evidence tier: hardware-ready acquisition/QA artifact with synthetic fault-injection; no physical data are presently available.

## Scientific bottleneck and prospective decision

E002-465/466 show that LED-trigger timing and binary detection do not authenticate the actual sensor shutter; E002-471 corrected reference-exposure containment. E002-472 supplies a physical handoff, but lacks an executable raw-acquisition intake gate. This experiment must make *independent imaging-path acquisition* possible without allowing a self-declared metadata field or a successful software test to become a physical exposure certificate.

**Predictions locked now:** (1) a complete synthetic 240-fps optical pulse-phase acquisition with at least 20 repeated observations per phase, <=0.05-ms phase spacing over two full frame periods, independent pulse-edge timestamps, stable radiometry, per-row strata, and nonmissing raw source checksums passes **intake QA only**; (2) each of the following must be rejected or abstain: insufficient phase coverage, missing phase bin, <20 repeats, pulse timing without an independent photodiode/logic-analyzer source, pulse width inconsistent with the independent trace, unknown clock uncertainty, frame drop, gain change, clipping, missing row stratum, inconsistent units, or raw-file hash mismatch; (3) even the complete synthetic intake must return `physical_shutter_support_authenticated=false` and `product_claim=ABSTAIN_UNCALIBRATED` until independent metrological review of raw optical response, detector floor, row kernels, timing transfer and held-out predictions. The validator cannot prove a device actually exists.

## Locked input and falsification

Implement a Python standard-library CLI accepting a local JSON manifest and CSV of measured phase scans. The manifest must specify nominal period, phase grid, minimum repeats, two or more row strata, independently recorded pulse/photodiode clock provenance, bounded clock error, gain lock, pulse-width tolerance, raw CSV SHA256 and a separate raw-video SHA256 (provenance declarations, not cryptographic attestations of hardware). Each CSV observation must include phase, row stratum, repeat index, pulse-start/end times from the independent trace, measured camera response and dark reference, gain, saturation and dropped-frame flags.

Require complete expected phase-bin coverage, strict unique (row,phase,repeat) keys, and consistent independently measured pulse widths. Report per-row signal contrast, phase count, repeats, and precise rejection codes without participant data. Do not infer a hard zero-exposure support from thresholded pixel values, nor a physiological velocity cap. A synthetic fixture may test only ingestion logic; physical and human evidence remain absent.

**Kill criteria:** Any malformed or incomplete trace accepted as intake-QA-passed; any result authorizing a physical hidden-closure claim; or any validator claim that source hashes prove independent timing. Preserve all failures and abstentions. Do not revisit Eye-BCI timestamp archaeology or the 17-person speed-proxy CSV. Do not inspect sealed S21/S22.

## Next actual acquisition

Use the existing E002-472 physical handoff: borrowed imaging camera, independently measured optical pulse and photodiode/logic-analyzer trace, RAW frames with locked gain, dark/flat controls, row-separated scans and external timing. Collect a calibration session and an independently timed held-out session before inferring shutter support; this intake tool is only the first gate. Follow with encoder-grounded moving aperture and consented blinded human reference. Physical hidden-closure, PERCLOS, blink duration, fatigue and medical outputs stay `ABSTAIN_UNCALIBRATED`. PR #26 remains draft/unmerged. Hush PR #45 is untouched.
