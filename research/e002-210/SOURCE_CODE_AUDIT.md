# EVE loader source-code audit (2026-10-15)

Upstream: https://github.com/swook/EVE/blob/master/src/datasources/eve_sequences.py
Verified Git blob SHA: 8b03f60068cc40f2d2ffacac46a1638a31e2117d.

In `load_all_from_source`, the HDF group loader reads `v1['data'][selected_indices]` and `v1['validity'][selected_indices]`; the video loader uses the same `selected_indices` to select camera frames, and returns corresponding timestamps. Thus `left_p`/`right_p` HDF labels are consumed as **camera-frame-indexed labels**, not as a separately loaded native eye-tracker stream.

This does NOT establish how those HDF labels were produced, whether native tracker recordings exist elsewhere, or what anti-alias filtering was used. It does establish that the published loader does not itself expose native tracker samples for independent rapid-waveform certification.

Combined with EVE DATASET.md's explicit warning about imprecise webcam synchronization, ordinary-webcam lag certification requires (1) independent numeric clock-error envelope and (2) label-lineage/native-timebase verification. Both remain unverified; fail closed.

SCIENCE: exact clock-offset/lag gauge plus direct frame-indexed loader provenance. PRODUCT: conditional EVE source, not a certified ordinary-RGB physiological waveform result. No five-second fatigue claim.
