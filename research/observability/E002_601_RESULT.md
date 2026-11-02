# E002-601 | Two adversarial reviewers pass the original synthetic qualification gate

Date: 2026-11-02. Primary E002-371 workstream. [Frozen attack and repair protocol](E002_601_FROZEN.md) committed at `31b4a51` before the attack executable and before the grader was modified. Evidence tier: **SYNTHETIC_INSTRUMENT_FALSIFICATION**, not human annotation or physical shutter validation.

## Actual prepatch falsification

The [prepatch hosted run #41382581048](https://github.com/sushxnthd/lucent/actions/runs/41382581048), at immutable head `3188c7935d0ba0f603d37ad6e85b2db4899328f3`, executed the *original* E002-600 Python grader and independent Node.js oracle on a private, deterministic, 190-frame synthetic reviewer challenge. The attack step succeeded and logged the following actual outputs:

| Frozen reviewer fixture | Clean measured | Covered | Correct decisive OPEN | Correct decisive CLOSED | Original qualification |
|---|---:|---:|---:|---:|---|
| Ideal ground-truth fixture | 114/114 | 114/114 | 103/103 | 11/11 | **PASS** |
| Maximum allowed 50-px uncertainty on every clean frame | 114/114 | 114/114 | **0/103** | **0/11** | **PASS (invalid gate)** |
| Abstain on all closed frames, label only open frames | 103/114 | 103/103 | 103/103 | **0/11** | **PASS (invalid gate)** |

The original rule only checked total clean measurement coverage, aggregate uncertainty-interval coverage and false decisive calls. It did **not** require informative classifications in either truth class. Thus a reviewer could pass with no decisive anatomical judgments at all, or by refusing every closure. The independent Node.js replay exactly matched the Python grader on all three fixtures.

The **overall prepatch workflow is marked FAILURE** because the final clean-worktree check encountered transient Python `__pycache__` files; the actual adversarial execution step passed and printed the results above. This CI hygiene failure is preserved and must not be relabeled a fully successful workflow.

## Repair, falsification gate and independent replay

The E002-600 grader and independent Node.js oracle now require the original coverage/false-call checks **plus** at least 80% correct decisive OPEN decisions among all 103 truth-open clean frames, at least 80% correct decisive CLOSED decisions among all 11 truth-closed clean frames, and at least 75% abstention on the 76 nuisance frames. Outputs now expose per-class denominators, correct decisive counts and ambiguous measured counts.

The frozen attack executable [e002_601_qualification_attack.py](e002_601_qualification_attack.py) requires both adversarial fixtures to fail the patched gate, the ideal fixture to pass, and the independent Node.js output to match the Python grader exactly. The [dedicated CI workflow](../../.github/workflows/e002_601_qualification_attack.yml) runs these tests and refuses residual private imagery/reviewer exports. The bytecode-worktree issue was corrected with `PYTHONDONTWRITEBYTECODE=1`.

**At initial report creation, hosted postpatch completion is not yet verified.** Inspect the exact-head CI run and report its result separately. The prepatch experiment demonstrates a real *instrument-qualification* flaw, not a physiological observation.

## Human study and product consequence

**Revoke any inference from the old E002-600 qualification rule.** Future human reviewer acceptance must use the revised, class-balanced synthetic gate *and* independent actual human-image annotation with separately justified iris scale, geometry and calibration. Even passing this synthetic gate would be a necessary instrument check, not anatomical validity or E002-371 validation.

No actual human reviewer was recruited or scored, no physical shutter/clock calibration was obtained, no continuous-time eyelid velocity ceiling was certified, and no held-out physical closure predictions were made. The remaining physical human study in E002-598 is unchanged. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Hush's separate branch and draft PR #45 were not modified.
