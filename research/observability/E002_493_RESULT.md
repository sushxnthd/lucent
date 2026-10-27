# E002-493 | Frozen authentic-human nuisance attack on the motion-event selector

**2026-10-28. Primary Lucent E002-371 validation kernel.** This is a new adversarial empirical test of the *existing* E002-491 image-motion proxy, not another theorem refinement. **Evidence tier pending authentic hosted replay; no human anatomical or physical-shutter validation.**

## Why this test is decisive for the present proxy

E002-491 found one localized image-motion candidate among 10,572 eligible adjacent pairs of checksum-verified S01 video, at native index 5356. E002-492 froze one candidate-centered clip and 19 SHA256-selected control clips before any anatomical labels. The prior result does not establish that the proxy is stable under changes in brightness, contrast, blur, image registration or sampling. A motion candidate can be a gaze movement, not a blink. Testing these *fixed same-subject clips* under nuisance interventions provides a falsifiable answer without touching held-out S21-S31 anatomy or changing the original threshold.

## New work persisted

- [Frozen predictions and kill criteria](E002_493_FROZEN.md) committed **first** at `a1bff00e`.
- [Executable authentic-video experiment](e002_493_real_nuisance.py) reads the MD5-verified public S01 archive and uses the E002-492 exact 260 frozen frame positions. It invokes E002-491's **unchanged** pairwise screen across six conditions: original, +8 brightness, 90% contrast, 3x3 blur, alternating +/-1-pixel horizontal jitter, and stride-2 sampling.
- [11 synthetic adversarial tests](test_e002_493_real_nuisance.py) cover frozen sampling, baseline candidate reproduction, brightness control, temporal sampling, registration geometry, constant-frame blur, invalid conditions, missing frames, checksum rejection, baseline failure, and fail-closed product output. **Tests are committed, but hosted execution is pending.**
- [Hosted workflow](../../.github/workflows/e002_493_real_nuisance.yml) downloads the public S01 archive on an ephemeral runner, checks its MD5, extracts no images to artifacts, and publishes **aggregate-only** results. [Push run 40581566019](https://github.com/sushxnthd/lucent/actions/runs/40581566019) and [PR run 40581575054](https://github.com/sushxnthd/lucent/actions/runs/40581575054) were queued/pending at report creation. **No authentic nuisance outcome is yet claimed.**

## Decision rule

If the original candidate disappears under an intervention, the proxy fails that intervention's sensitivity criterion. If any of the 19 control clips develops a candidate, it fails that intervention's spurious-activation criterion. If eligible fraction falls below 80%, nuisance abstention is excessive. No thresholds may be retuned after seeing results. Survival on one subject remains **fixture-specific** and cannot establish general detection accuracy. No transformed proxy is an anatomical closure label.

## Primary blockers remain

Independent dual-rater eyelid landmarks: **0**. Independently authenticated camera exposure/clock: **0**. Physical shutter acquisitions: **0**. Held-out anatomical validation: **0**. E002-371 physical hidden-closure predictions are **not validated**. The next decisive milestone is blinded anatomical review and independently timed acquisition; no further proxy refinements should replace it.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. No raw human images, crops or individual measurements are committed or uploaded. No merge, deployment, Hush changes or automation rescheduling.

## Hosted authentic S01 outcome (verified 2026-10-27 20:56 UTC)

The [hosted E002-493 workflow](https://github.com/sushxnthd/lucent/actions/runs/40581566019) **completed successfully** on the frozen branch. Its 11/11 adversarial software tests passed, the S01 archive passed checksum verification, and its aggregate-only output was uploaded as [artifact 12769788502](https://github.com/sushxnthd/lucent/actions/runs/40581566019/artifacts/12769788502). The exact logged result is now committed as [E002_493_HOSTED_AGGREGATE.json](E002_493_HOSTED_AGGREGATE.json); it is not a human closure annotation.

| Frozen condition | Proxy candidates | Eligible/analyzed pairs | Prespecified verdict |
| --- | ---: | ---: | --- |
| Baseline | 1 | 212/240 | REPRODUCED |
| Brightness +8 | 1 | 212/240 | SURVIVES_THIS_FIXTURE_ONLY |
| Contrast 90% | 1 | 216/240 | SURVIVES_THIS_FIXTURE_ONLY |
| 3×3 blur | 1 | 212/240 | SURVIVES_THIS_FIXTURE_ONLY |
| Alternating ±1-pixel jitter | **0** | 212/240 | **FAIL** |
| Stride-2 temporal subsampling | **0** | 79/120 | **FAIL** |

All 19 frozen control clips had zero proxy candidates in all conditions. The original candidate was lost under the prespecified registration and temporal-sampling attacks, with **no threshold changes**. Stride-2 also reduced eligible coverage to **65.83%**, below the frozen 80% requirement. The original candidate remains **image motion only**, not an anatomical blink.

**Falsification and product consequence:** Retire E002-491 motion screening as a reliable automatic event selector under registration jitter or temporal subsampling; do not use its candidate count as a blink rate, closure label, velocity estimate, or basis for a product claim. The brightness, contrast and blur results are **single-participant fixture survival only**, not generalized robustness. The source video clock remains unauthenticated; no anatomical labels, held-out human validation or physical shutter measurements were obtained. E002-371 remains physically unvalidated. All physical hidden-closure, blink-duration, PERCLOS, fatigue and medical claims remain `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. The next scientific milestone is two independent blinded eyelid-landmark raters on the already frozen clips and independently timed acquisition, not further threshold tuning.
