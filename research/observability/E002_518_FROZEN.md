# E002-518 | Frozen native-sequence provenance falsification

Date: 2026-10-29. Scope: E002-515 offline physical-replay evaluator; preserve E002-371 and the existing Lucent branch/PR. Evidence tier: adversarial *software/inference-boundary* test, not human or hardware evidence.

## Question and predeclared attack

The current three-CSV E002-515 contract includes arbitrary `frame_id` strings but no independently captured native frame index or continuity proof. Its `evaluated_adjacent_gaps` counts successive **CSV rows**, implicitly treating them as successive **native exposures**. Is that adjacency identifiable from the supplied measurements?

Freeze two tests before implementing a correction:

1. **Two-world omission:** take a valid artificial three-frame optical capture with native indices 0, 1, 2. In world A, the exported two-frame subset contains native indices 0, 1. In world B, it contains 0, 2, with index 1 omitted. The existing three CSV schemas can be made indistinguishable by renaming the retained second frame; they cannot certify whether the two exported rows are native-consecutive. Expect the original evaluator to report one evaluated adjacent gap in both worlds.
2. **Permutation:** reverse the camera CSV order while retaining the reference mapping. Expect the original evaluator to evaluate a row-pair with reversed physical time, without rejecting the order.

This is not a prediction of an unsafe shutter-gap underbound. A nonconsecutive pair can have a conservatively *larger* gap; the falsified claim is that the tested gap is **native-adjacent**, which affects sampling, calibration denominators, and claims of full-record coverage.

## Predeclared correction and kill criteria

- Add a separate `frame_id,native_index` capture manifest, with integer indices starting at any nonnegative index. For the *specific claimed contiguous evaluation segment*, demand exact one-step increments in camera-row order and exact ID coverage. Reject duplicates, missing rows, gaps, reordered rows and invalid indices. Do not derive index from arbitrary frame IDs, nominal FPS, or the optical inverse.
- Without such a manifest, report zero **certified-by-input** native-adjacent gaps and `INSUFFICIENT_NATIVE_SEQUENCE_PROVENANCE`, even if the reference coverage test passes. Keep the prior row-pair diagnostic under a distinctly named field if useful; never label it native adjacency.
- With a self-declared manifest, allow only *conditional* adjacent-gap diagnostics and report `native_frame_continuity_independently_attested=False`. A CSV cannot attest its own provenance. Release remains blocked and no human/physical certification follows.
- Include at least five regression controls: no manifest, valid consecutive manifest, missing index, reversed camera order, duplicate/invalid IDs or indices, and independently altered reference order. Retain the original E002-515 reference-uncertainty falsification.
- Preserve negative results. If the current evaluator already rejects the attacks, report that and do not invent a vulnerability.

## Evidence limits

No physical measurements, authenticated exposure-sync channel, actual human ratings, or continuous-time eyelid-speed ceiling are obtained. This test addresses **sampling provenance**, not physiological novelty. No camera images or owner-only mappings should be committed. No force-push or merge. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
