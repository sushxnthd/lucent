# E002-518 | Native-frame adjacency is not identified by optical/reference CSVs

Date: 2026-10-29. [Frozen before correction](E002_518_FROZEN.md) at commit `c071ff2656bcf24e187bf9f4b97ac7572683389f`. Evidence tier: **logical two-world counterexample plus adversarial software regression**, not measured human or physical camera data.

## Identifiability result

E002-515's original three inputs record optical waveforms, frame-labeled image intensities and independently measured reference exposure intervals. They **do not contain native acquisition indices**. Let the exported records be `f0` and `f1`, with the same photodiode, camera and reference CSVs in two worlds:

- **World A:** these records are native capture indices 0 and 1.
- **World B:** these records are native indices 0 and 2; native index 1 was omitted from the export.

The physical times and all *exported* observations can be identical in both worlds because no fixed interframe cadence is assumed. The missing native record has no row in either file. Consequently **no function of the three CSVs can decide native consecutiveness in both worlds**. This is a simple missing-observation indistinguishability argument, not a new theorem of physiological measurement.

Before E002-518, the E002-515 code counted every successive pair of camera rows as an `evaluated_adjacent_gaps` pair. Thus both worlds were silently counted as one native-adjacent test. A separate reversal attack exposes the same unsupported assumption: camera CSV row order need not match reference exposure order. Neither attack proves an unsafe shutter-gap *underbound*: an omitted intermediate frame may increase the conservative gap. What fails is the **sampling denominator and the claim of native-adjacent evaluation**.

## Enforced correction

The offline replay now accepts an optional, separately recorded `frame_id,native_index` CSV. When supplied, its frame IDs must exactly match camera-row order; native indices must be nonnegative, unique, and increase by exactly one; independently referenced exposure starts must increase in that order. Missing, duplicated, skipped or reordered indices reject the claimed contiguous segment.

When no ledger is supplied, the evaluator may still compute per-exposure reference coverage, but sets `evaluated_adjacent_gaps=0` and returns `INSUFFICIENT_NATIVE_SEQUENCE_PROVENANCE` unless a more fundamental reference-coverage failure occurs. `unverified_csv_row_pairs` retains the former count as an explicitly noncertifying diagnostic. With a ledger, the result is at most `REPLAY_CONSISTENT_SEQUENCE_UNATTESTED`: the CSV remains self-declared, not independently authenticated. `native_adjacent_gaps_proven_by_code` is always zero, and `native_frame_continuity_independently_attested` is always false. No new product clearance is possible.

The modified [physical replay](e002_515_physical_replay.py), [regressions](test_e002_515_physical_replay.py), and [hosted CSV intake workflow](../../.github/workflows/e002_515_physical_replay.yml) include missing-ledger, valid-ledger, index-gap, reversed-order, ledger-mismatch, malformed-index and indistinguishable-two-world controls. The existing reference-uncertainty and optical coverage controls remain in place.

## Consequence for an actual instrument

The acquisition device must supply an independently auditable monotonic native-frame ledger, with dropped-frame counts and a source of integrity beyond the CSV's own assertions. A photodiode measures emitted light; an exposure-sync line measures exposure timing; **neither alone proves no camera frame was silently omitted from the export**. Without a validated native-index chain, report conditional optical timing consistency only and abstain from native-adjacent validation coverage. The study must predeclare what capture continuity is being validated, not infer it from a subset selected after seeing anatomy.

## Reproduction

For the original three-CSV call, the expected result after correction is `INSUFFICIENT_NATIVE_SEQUENCE_PROVENANCE`, not a claimed adjacent-gap replay success. To exercise conditional diagnostics, add:

```bash
python research/observability/e002_515_physical_replay.py \
  --photodiode /secure/photodiode.csv \
  --camera /secure/camera.csv \
  --reference /secure/reference.csv \
  --sequence /secure/native_sequence.csv \
  --residual-max PRECALIBRATED_VALUE \
  --timing-envelope-ms PRECALIBRATED_VALUE
```

This is a synthetic/software falsification. No actual native acquisition ledger, independent camera provenance, human anatomical labels, authenticated physical shutter measurements, hard eyelid-speed bounds or held-out physical predictions were obtained. The E002-371 physiological claim remains unvalidated. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush remains a separate unmodified workstream.

**Verification status at report creation:** GitHub Actions is queued/pending; do not claim hosted success until the run completes.
