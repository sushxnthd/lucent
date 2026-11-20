# E002-463 — frozen encoder-witness integration challenge (2026-10-26)

**Preregistered before adapter implementation and before running synthetic cases.** Evidence target: executable synthetic instrument-to-prospective-gate integration. No physical encoder, human annotations, shutter calibration or physiology evidence. E002-462 already established high-speed reference-camera aliasing; this run tests the *end-to-end enforcement consequence*, not a new theorem.

## Frozen question and predictions

Can a separately timed position encoder positively witness a hidden aperture crossing that an ideal 400-fps shutter camera fails to observe, without silently turning absent encoder witnesses into certified OPEN labels?

1. H1: Under the E002-462 finite-duration 400-fps witness (b=2.30 mm, min=1.95 mm, threshold=2.00 mm, 0.30-ms shutters, C=567.103928 mm/s, O=274.616337 mm/s), both constant-open and closure worlds produce identical ideal high-speed shutter means. Independently sampled encoder data with an authenticated-in-principle interior subthreshold sample distinguishes them.
2. H2: A synthetic ordinary-camera interval with endpoint aperture means [2.30,2.30] mm, centers [0,2.5] ms, uniform 0.30-ms shutters, threshold 2.0 mm and deliberately false illustrative V=100 mm/s is conditionally excluded by E002-456. An independent encoder sample with aperture 1.95±0.01 mm at t=1.0 ms, encoder clock error 0.02 ms and ordinary clock error 0 must trigger `FALSIFIED_JOINT_ASSUMPTIONS`. This falsifies the *stipulated 100-mm/s joint assumptions*, not the theorem. The 100-mm/s value is intentionally incompatible with the constructed motion.
3. H3: An all-open encoder trace, however dense, yields `REFERENCE_UNRESOLVED`, never a negative anatomical truth label or physical release.
4. H4: An encoder sample whose entire timing-uncertainty support does not lie strictly inside the ordinary camera **dark gap** must not witness a dark-gap crossing. Boundary equality is unresolved.
5. H5: Missing/invalid provenance, missing sample times, duplicate/nonmonotone samples, unbounded scale/time uncertainty, bad quality, or nonfinite values fail closed. Attestation fields are *declared*, never cryptographically authenticated by software.
6. H6: All encoder traces and subject identifiers remain private. Only aggregate synthetic results and source/test code may be committed. The existing E002-456 sealed-holdout protocol remains the prospective freeze/score mechanism for future physical data.

## Instrument contract and kill criteria

An adapter shall consume a private E002-456 case with `reference=[]` and an independently measured position-encoder record. It may add only **positive, robustly interior** threshold witnesses to E002-456; no sample above threshold may be promoted into proof of absence. The adapter must reject any uncalibrated reference, retain explicit unresolved status, and preserve `physical_release_authorized=false` / `ABSTAIN_UNCALIBRATED`.

For a centered ordinary shutter of width E, nominal centers t0<t1, ordinary clock error δo and encoder sample time error δe, a point reference witness at te is eligible only if
`te-δe > t0+E/2+δo` and `te+δe < t1-E/2-δo`.
These strict inequalities concern **dark-gap-only** witness qualification. They do not alter E002-456's conservative full-interval mathematical bound.

A passing synthetic adapter is not empirical validation. Physical work requires an independently calibrated encoder (position, bandwidth, dynamic lag), measured shutter exposure supports and clock error, a separately escrowed frozen prediction manifest, and an unseen-session motion challenge. A human follow-up additionally requires anatomical margin annotation by two blinded raters and participant-disjoint calibration/holdout. Do not access S21/S22, alter production measurement claims, or modify Hush PR #45.
