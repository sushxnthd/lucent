# Research Activity

Updated: 2026-11-16 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research/product commit: `73e719b79f3a25f8e5a4f0cd537e2f3dbd523c40`
- Evidence/product consequence: documented offline alpha onboarding, Node smoke-test invocation, claim boundaries, privacy/failure behavior, device acceptance protocol and explicit release blockers. This is packaging documentation, not an executed browser test, calibrated physiological evidence, or tagged release.
- E002-371 remains unvalidated on independently calibrated human eyelid and shutter measurements; camera-derived fatigue inference disabled.
- Activity checkpoint only, not release approval.

## Prior checkpoint

# Research Activity

Updated: 2026-11-16 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research/product commit: `31d4ebfc57bd27cd9b5a153b67eea9bbc816df12`
- Evidence/product consequence: added a standalone local-only five-trial response-time demonstration with median latency, early-tap retry, visibility/focus interruption invalidation, no persistent data or camera access, and explicit non-diagnostic claim boundary. Code committed; no browser/device acceptance testing or tagged release verified.
- E002-371 physiological shutter-gap validation remains outstanding; camera-derived fatigue and hidden-closure claims remain `ABSTAIN_UNCALIBRATED`. This demo is not a shipped end-to-end fatigue product.
- Activity checkpoint only, not scientific validation or release approval.

## Prior checkpoint

# Research Activity

Updated: 2026-11-11 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research commit: `48dd33ed99161701cdb85485021aec326d0478ff`
- Evidence: E002-742 executed three frozen-seed synthetic shutter-gap stress tests (30,000 simulated paths). Naive nominal-timestamp/uncertified-velocity exclusion made 6,522 false exclusions; conservative synthetic hard-bound exclusion made zero under its imposed assumptions and abstained on 23,409 paths. No physical/human validation or certified physiological ceiling.
- Product: `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
- This checkpoint is activity only, not validation or release approval.

## Prior checkpoint

Updated: 2026-11-10 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research commit: `32c596d936d2e585a8bd92de9b4ca61160f8371d`
- Evidence: E002-731 adds an exact-rational synthetic falsification of naive hidden-closure exclusion under independent endpoint timestamp errors. The correct worst-case point-sample exclusion uses nominal gap plus twice the clock-error bound. Includes an explicit hidden-zero witness and a 1,100-case executable boundary sweep; human/physical validation remains absent. This applies only to point samples, not exposure averages.
- Product: `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
- This checkpoint is activity only, not validation or release approval.

## Prior checkpoint

Updated: 2026-11-09 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research commit: `8d36cacaf5af7acc5726a59c1c157ad4c2e3d29a`
- Evidence: E002-730 adds an exact-rational synthetic counterexample showing that a 75% exposure-averaged aperture can coexist with complete hidden closure. It falsifies substituting an exposure average for a pointwise lower aperture bound; it does not validate the shutter-gap theorem or add human/physical evidence.
- Product: `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
- This checkpoint is activity only, not validation or release approval.

## Prior checkpoint

Updated: 2026-11-08 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research commit: `4d1aa6e3bdf875f39647b4b328a6f1b0bedc2178`
- Evidence: E002-712 executed a deterministic 10,000-phase synthetic shutter experiment with exact exposure integration and photometric-nuisance abstention; 3,459 ideal and 2,487 bounded-nuisance detectable cases, 0 under uninformative nuisance. No physical or human measurements.
- Product: `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
- This checkpoint is activity only, not validation or release approval.

## Prior checkpoint

Updated: 2026-11-07 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research commit: `c28c31c98bdd90565ade5d6048b99bb262e94717`
- Evidence: E002-690 freezes a prospective physical-instrument and participant-disjoint human validation protocol, explicit timing/calibration data contract, false-exclusion gate, nuisance strata, and abstention rules. No new physical or human measurements; not empirical validation.
- Product: `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
- Experimental artifacts remain on the research branch; this ledger is not validation or release approval.

## Prior checkpoint

Updated: 2026-11-06 (UTC)

- Active research branch: `research/observability-human-boundary`
- Active draft PR: #26
- Latest durable research commit: `142f3a2d15906b37da0cdebb159c589d990fc7f7`
- Evidence: E002-665 adds an exact-arithmetic synthetic phase-dither falsification: independent uniform phases detect a stipulated periodic hidden closure with probability 1-(1-c)^n, while correlated or restricted phase jitter may miss indefinitely. Includes instrument and participant-held-out validation protocol. No human or physical validation.
- Product: `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
- Experimental artifacts remain on the research branch; this default-branch ledger is neither validation nor release approval.
