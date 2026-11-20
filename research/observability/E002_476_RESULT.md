# E002-476 RESULT — interval-level provenance laundering blocked at the product boundary

Date: 2026-10-27. Kernel: E002-371. **Evidence tier:** synthetic software-interface falsification and implementation change. No new physical optical acquisition, anatomical reference sequence, or physiological hard velocity bound.

## Why this experiment matters

E002-475 rejected the statistical shortcut of treating a finite human speed-proxy sample maximum as a universal physiological limit. E002-456's *research* evaluator correctly labels its mathematical output `EXCLUDED_CONDITIONALLY`, but previously returned no explicit physical-release status from the **per-interval** function. Only its aggregate carried `physical_release_authorized=false` and `product_claim=ABSTAIN_UNCALIBRATED`. A downstream consumer of the interval function could therefore mistake a conditional model conclusion for a physical observation. This is an **interface-level claim-laundering hazard**, not a newly demonstrated real-world product exploit.

## Frozen adversarial predictions and software results

The protocol [E002_476_FROZEN.md](E002_476_FROZEN.md) was committed first at `e6e9931a6f046b030badb561599c87ecda1158f8`.

The executable [e002_476_claim_boundary.py](e002_476_claim_boundary.py) contains six prespecified synthetic cases, reusing the E002-456 model rather than constructing new physiological assumptions:

| Case | Research evaluator | Reference status | Public product |
| --- | --- | --- | --- |
| Illustrative 100-mm/s speed assumption | EXCLUDED_CONDITIONALLY | NO_WITNESSED_CROSSING | ABSTAIN_UNCALIBRATED |
| Same interval with self-declared external hard bound | EXCLUDED_CONDITIONALLY | NO_WITNESSED_CROSSING | ABSTAIN_UNCALIBRATED |
| Same interval with no reference samples | EXCLUDED_CONDITIONALLY | REFERENCE_INCOMPLETE | ABSTAIN_UNCALIBRATED |
| Contradictory reference witness within guaranteed dark gap | EXCLUDED_CONDITIONALLY; joint assumptions falsified | WITNESSED_CROSSING | ABSTAIN_UNCALIBRATED |
| Finite-sample maximum passed as velocity provenance | ABSTAIN | NOT_EVALUATED | ABSTAIN_UNCALIBRATED |
| Unknown clock nuisance | ABSTAIN | NOT_EVALUATED | ABSTAIN_UNCALIBRATED |

The distinction is exact: changing `ILLUSTRATIVE` to `EXTERNAL_HARD_BOUND_DECLARED` changes **no measured optical or anatomical evidence**. It cannot establish a physical speed limit. Likewise, a missing independent witness cannot establish an anatomical negative. A witnessed contradiction must override any reassuring presentation of the conditional inequality.

## Enforcement change

The actual E002-456 interval evaluator now emits these fields on **every** success and abstention path:

- `physical_release_authorized: false`
- `product_claim: ABSTAIN_UNCALIBRATED`
- `external_hard_bound_verified_by_this_program: false`

The new `render_public` consumer accepts only internally consistent research outputs and refuses forged or missing release flags, contradictory reference/falsification states, malformed envelope values, or unrecognized velocity provenance. It can display `CONDITIONAL_MODEL_EXCLUSION_ONLY` or `JOINT_MODEL_ASSUMPTIONS_FALSIFIED` as **research classifications**, but has no code path to issue a physical no-closure claim.

Seventeen dedicated adversarial regression methods cover this interface, including all nine nuisance names, missing reference, declared external bounds, empirical maxima, forged authorization, inconsistent witness flags, and nonfinite values. Existing E002-456 and E002-471 regression suites are included in the hosted verification workflow. The committed [E002_476_AGGREGATE.json](E002_476_AGGREGATE.json) contains no participant identifiers or raw human data.

**Verification tier:** GitHub Actions run [40439651069](https://github.com/sushxnthd/lucent/actions/runs/40439651069) was queued at initial inspection. This report does not claim a completed hosted test until that run is independently checked. The aggregate was constructed from the frozen case predictions and will be compared byte-for-byte against the executable CI output; a mismatch is a failure, not a reason to silently rewrite the predictions.

## Scientific limits and next decisive external action

This is a useful **product-boundary correction**, not a new eyelid theorem or validation of E002-371. A string-valued calibration ID, a published sample maximum, a successful CI run, or a declared external speed bound cannot substitute for independently timed shutter support, independently measured physical aperture motion, or blinded human anatomical reference.

Do not reopen the previous high-speed data archives or continue theorem polishing. The next scientific step is the [E002-472 physical acquisition handoff](E002_472_PHYSICAL_HANDOFF.md): an actual optical-phase measurement through the camera imaging path, followed by moving-aperture ground truth and participant-disjoint human sequences. If physical equipment remains unavailable, the correct evidence tier is a bounded synthetic/instrument substitute, not physical completion.

**Completion gate:** E002-371 remains physically unvalidated. Physical no-hidden-closure, blink duration, PERCLOS, fatigue and medical inference remain `ABSTAIN_UNCALIBRATED`. Hush PR #45 is separate and was not modified.
