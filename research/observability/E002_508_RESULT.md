# E002-508 | Frozen-source provenance substitution falsification and fail-closed correction

Date: 2026-10-28. Primary E002-371 human-validation kernel, existing research branch and draft PR #26. Frozen **before editing the evaluator** in [E002_508_FROZEN.md](E002_508_FROZEN.md). Attack runner: [e002_508_manifest_attack.py](e002_508_manifest_attack.py).

## New measurement-validity finding

The prepatch E002-507 evaluator checked the owner manifest's experiment, subject and clip IDs but **not** the previously frozen source-frame mapping. Under the frozen synthetic fixture, a one-frame CLOSED interior with OPEN endpoints is a synthetic witness. An adversary can keep the same A/B labels and positive scale uncertainty while altering the owner manifest's native frame index, center index, candidate bit or adding a key. The prepatch code would still classify the same labels and return a witness without detecting that the source-to-label mapping had changed. This is a provenance substitution flaw, **not** evidence of a real hidden human blink.

The frozen runner encodes four attacks and the canonical control. The correction requires exact equality with the deterministic E002-492 `build_manifest()` before processing labels. This is deliberately strict: any new acquisition or reselected sampling protocol requires a **new preregistration**, not silent substitution. Two additional independent E002-507 regression tests exercise canonical acceptance and noncanonical rejection.

| Condition | Prepatch prediction from source inspection | Corrected required behavior |
| --- | --- | --- |
| Canonical frozen mapping + synthetic witness | One synthetic witness | One synthetic witness |
| Changed native source-frame index | Same witness, undetected | Reject |
| Changed frozen center | Same witness, undetected | Reject |
| Flipped candidate/control bit | Same witness, undetected | Reject |
| Added unauthorized owner mapping key | Same witness, undetected | Reject |

## Hosted verification, exact commit heads

- Prepatch frozen attack: [run 40697202101](https://github.com/sushxnthd/lucent/actions/runs/40697202101), commit `33b58d28012519da991aaa300422505d404c9ab7`, **queued at report creation**. The workflow expects acceptance of all four synthetic forgeries.
- Postpatch provenance attack: [run 40697307679](https://github.com/sushxnthd/lucent/actions/runs/40697307679), commit `4e15c811b402ada4ad5a0597cd6dd58400253f5c`, **queued at report creation**. The workflow expects rejection of all four.
- Existing E002-507 regression suite with two new tests: [run 40697297885](https://github.com/sushxnthd/lucent/actions/runs/40697297885), commit `94ef6e684be006b8409bc3a8a9a0869051f83ed6`, **queued at report creation**.

**Do not claim hosted success until the exact-head runs finish.** The prepatch and postpatch runs use distinct commit snapshots; a later fix does not rewrite the frozen attack history.

## Residual limitations and next science

This gate validates **declared** owner manifest provenance. It does not cryptographically bind raw PNG bytes to the two reviewers' exported JSON, independently authenticate two human identities, establish iris-diameter uncertainty, or measure exposure timing and eyelid velocity. E002-502 checksum-pinned local archive replay remains a separate prerequisite. No per-frame anatomy or identifiable imagery is uploaded.

Stop synthetic source-mapping work once the frozen tests pass. The decisive next experiment is two genuine independent blinded S01 anatomical reviews with independently justified iris-scale bounds, followed by authenticated shutter/clock timing and participant-disjoint human predictions. Zero independent human ratings; zero authenticated physical shutter measurements; zero certified continuous-time human velocity bounds; zero held-out physical predictions. E002-371 remains physically unvalidated.

**Product: `ABSTAIN_UNCALIBRATED`. Release: `BLOCKED`.**
