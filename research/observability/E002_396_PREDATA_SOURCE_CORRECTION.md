# E002-396 source-integrity correction before any S19 image analysis (2026-10-23)

The original frozen protocol at `5752804` transcribed an invalid **31-character** MD5 string from a truncated search excerpt. The first hosted attempt [39964528221](https://github.com/sushxnthd/lucent/actions/runs/39964528221) downloaded the entire untouched S19 archive but **stopped before opening/analysing it** because `md5sum --check` rejected the malformed checksum line. The experimental script and independent checker were **not executed**.

The authoritative full 32-character MD5 on the original Zenodo SSVEP record 21905748 is:

`8a16cf12526f7558b4e49926c4bc5e8e`

Source: https://zenodo.org/records/21905748 (S19.zip file row).

**Amendment scope:** Replace the malformed hash in source-verification code and workflow only. Do not change participant, session selection, fixed feature, training threshold, control offsets, nuisance variants, outcome thresholds or any predictions. Keep the original protocol and this transparent amendment permanently. Re-run before inspecting S19 results.
