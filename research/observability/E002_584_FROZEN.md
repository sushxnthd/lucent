# E002-584 | Frozen one-frame timing-uncertainty falsification of human-label alias witnesses

**Freeze:** 2026-11-01, before running the E002-584 source analysis. Scientific kernel E002-371; preserve the existing branch and draft PR #26. This is a new *adversarial robustness measurement* of the already reported E002-583 authentic human-label result, **not** another anatomical source search or physical shutter experiment.

## Scientific question and exact test

E002-583 found 105 event-phase omissions of 279 simultaneous-binocular full-closure runs, and 97 event-phase omissions of 288 either-eye runs, under nominal 100-to-30-fps *point-index* subsampling. Are those omissions still **guaranteed** when the retained native index of every ordinary-rate sample may shift independently by at most one 100-fps source frame? This is an adversarial index-timing sensitivity test, **not a claim that a real camera has 10-ms jitter**.

For each E002-583-eligible contiguous positive run [a,b], phase phi in 0..9, and nominal retained-index set R_phi, define:

- **Nominal omission** (j=0): R_phi has no index in [a,b].
- **Robust omission at j**: R_phi has no index in [a-j,b+j]. This means *every* per-sample integer perturbation of magnitude <=j still misses the positive run, assuming point sampling and valid frame indices.
- **Possibly omitted at j**: no nominal retained index r has its entire allowed interval [r-j,r+j] contained in [a,b]. This is only a permissive independent-perturbation upper bound, **not** a realizable synchronized-camera schedule.

Evaluate j=0,1,2, all ten phases, no post-hoc phase selection. The **primary endpoint** is the number of robust event-phase omissions at j=1 for simultaneous-binocular FC. Secondary: j=0,2; either-eye; possible omission upper bounds; per-sequence robust counts and nuisance abstentions.

## Prospective exact predictions from the previously reported run-length histogram

The frozen 100:30 index sampler has repeating sample spacings 3,3,4 native frames. With j=1, a sample's three-index uncertainty neighborhood leaves at most **one unprotected frame** in each four-index gap. Therefore a robust omitted event must be exactly **one positive frame** at such a location. Over ten shifted phases each interior one-frame event has exactly one robustly omitting phase. With j=2, all native indices are covered by sample uncertainty neighborhoods and no event can be robustly omitted.

From E002-583's already published 1-frame-run counts, freeze the following before re-reading source annotations:

| Event definition | j=0 nominal omissions | j=1 robust omissions | j=2 robust omissions |
| --- | ---: | ---: | ---: |
| Simultaneous binocular FC | 105 | **4** | **0** |
| Either-eye FC | 97 | **3** | **0** |

All j=0 counts must match E002-583; j=1/2 predictions are falsifiers. Do not change the sampler, event definitions, nuisance eligibility, source SHA, phase origin, or counts to improve the result.

## Source and nuisance gates

Reuse only the published Silesian5 annotation ZIP already authenticated by E002-582/583: SHA-256 `a73bf84981b84f626a3cc7b3b3d1962360354740bc6cf3de5d9c92d6d380c223`, five sequences and 58,884 annotation rows. Use E002-583's simultaneous binocular C/C and either-eye C definitions, eligibility, nonfrontal/eye-not-visible abstentions, immediate flanks and sequence-edge margin. Refuse mismatched archive SHA, schema, indices, or baseline event counts. Do not print source rows, face coordinates, identities, images or participant names.

Synthetic adversarial controls: one-frame event at the center of a four-frame sampling gap; one-frame event in a three-frame gap; two-frame event; long event; missing source index; nuisance flag; near-boundary event; permutation of sequence order; j=0 identity; and j=2 zero robust omissions. Independently check the expected robust counts using a second implementation based on the 3,3,4 gap geometry or direct enumeration.

## Interpretation and product gate

A reduction from 105 to 4 would mean **96.19% of the nominal binocular event-phase omissions lose a guarantee under hypothetical +/-1 native-frame timing uncertainty**. It would **not** mean 96.19% of actual blink events are false or that a physical camera detected them. Even a robust point-index omission does not certify a shutter-integrated physical miss: finite exposure, rolling-row timing, anatomy, brightness, gaze, glasses, blur, geometry, frame drops, source clock and human label disagreement are not calibrated.

This source supplies no hard continuous-time human eyelid-velocity ceiling and no two independently blinded anatomical raters. Regardless of the outcome, Lucent remains `ABSTAIN_UNCALIBRATED` and production `BLOCKED`. The decisive next step is E002-567's synchronized physical reference/ordinary-camera human study with optical exposure timing and independent raters. No Hush branch or PR writes.
