# E002-617 | Human-label boundary uncertainty: prospective index prediction; source replay pending

**2026-11-03 status:** Frozen before E002-617 analysis at [cb9b150](https://github.com/sushxnthd/lucent/commit/cb9b1504ed541955177e446dac3fb1718a7be087). Instrument and independent cross-language audit committed at [1fdf931](https://github.com/sushxnthd/lucent/commit/1fdf931836a1a4ad2f7c14ec56cda3510bde955e), [320a0b8](https://github.com/sushxnthd/lucent/commit/320a0b82e6b4aa50a8e065f48b83550c338026b2), and [751196a](https://github.com/sushxnthd/lucent/commit/751196abee3a54de74922e19c9c053af86537d98). [Hosted human-source run #41548054575](https://github.com/sushxnthd/lucent/actions/runs/41548054575) was queued at this report's creation. **Do not claim it passed.** Source-timestamp endpoint not yet measured.

## Prespecified index-selector prediction from previously authenticated human labels

The previously verified E002-616 source-derived bilateral FC run-length histogram was 4 runs of length 1, 14 of length 2, 21 of length 3, and 240 of length >=4, totaling 279 eligible runs. E002-616 established 105 floor-index virtual omission event-phase pairs under ten phases, by the exact selector law `4*7 + 14*4 + 21*1 = 105`.

If each investigator-labelled bilateral FC run can be extended by **one native frame on both sides** (a *hypothetical* label uncertainty model), an event of length L becomes length L+2. The exact floor-index omission law (7,4,1,0 for lengths 1,2,3,>=4) then predicts:

| Conditional quantity | Predicted index-selector count | Evidence tier |
|---|---:|---|
| Baseline omitted event-phase pairs | 105 | Previously measured source-label aggregate (E002-616) |
| Omitted pairs surviving maximal one-frame outward extension | **4** | New exact counterfactual deduction from E002-616 human histogram |
| Baseline omitted pairs for events surviving one-frame inward trim (L>=3) | **21** | New exact counterfactual deduction |
| Same event both survives inward trim and remains omitted after outward extension | **0** | New exact counterfactual deduction |
| Baseline events erased by inward trim (L<=2) | **18** | New exact counterfactual deduction |

Thus **101/105** baseline index-selector omission pairs are *not invariant* to this maximal outward extension. And **zero** satisfy the stronger two-sided stability criterion under this stipulated annotation model. These are exact conditional calculations, **not measured human annotation errors**, and cannot erase the literal E002-616 observation.

## Empirical verification still required

The E002-617 script replays the original SHA-256-pinned five published human annotation/timestamp sequences, applies the same ten selectors and fixed nuisance exclusions, computes paired index and source-timestamp results, and fails closed on changed baseline counts. A separate Node.js oracle verifies integer phase laws, aggregate sums and corruptions. Until the hosted run finishes, **none of its new measured outputs, tests, or timestamp-specific counts are asserted successful**. If the predicted index result fails, preserve the counterexample and investigate the discrepancy rather than changing the protocol.

This experiment tests label-boundary sensitivity of **virtual point sampling**, not actual exposure-integrating 30-fps cameras, calibrated physical shutter gaps, anatomical aperture trajectories, or independently certified continuous-time eyelid velocities. No blinded human anatomical rater pairs or participant-disjoint physical predictions were obtained. E002-371 remains empirically unvalidated.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. The decisive next experiment is independently synchronized physical acquisition with blinded anatomical review. Hush's separate PR #45 remains untouched.
