# E002-451 — hidden-repeat byte-linkability falsification and exploratory mirror challenge

**Date:** 2026-10-26. **Frozen before implementation:** [E002_451_FROZEN.md](E002_451_FROZEN.md) at `045aa20370da2425400b193d137b364abff438a0`. **Evidence tier:** deterministic source-level falsification, nine local synthetic/adversarial tests using a stand-in for the existing encoder/aperture functions; repository-hosted actual-code integration **completed successfully** (9/9 tests; [run 40244213282](https://github.com/sushxnthd/lucent/actions/runs/40244213282)). **No real human annotation, calibrated shutter, scale or physiological velocity cap.**

## Newly identified validation vulnerability

The E002-448 offline pack writes the **same byte sequence** for every original/repeated view of a selected frame, with only the opaque filename changed. Anyone holding a rater pack can identify repeat pairs by SHA-256 hashing all PNG files, without seeing the private master or the candidate event classes. This undermines the inference that a passing E002-450 hidden-repeat consistency test demonstrates *blind* intra-rater repeatability. It does **not** show that any human rater recognized duplicates, copied marks, or acted dishonestly.

The source-level construction implies **all 12 of the previously prepared S19 hidden-repeat pairs are byte-linkable**; the original private images were deleted from the hosted runner, so that 12/12 count was **not independently remeasured on S19** in this run. The frozen tiny synthetic pack demonstrates **1/1** exact duplicate pair.

## Experimental challenge and limitations

[E002-451 challenger](e002_451_repeat_challenge.py) makes a **new, private** offline pack, leaving E002-448 untouched. It horizontally mirrors each repeated presentation while retaining its opaque ID and original private mapping. For an asymmetric synthetic frame, the exact duplicate changes from 1/1 to 0/1. A deliberately left/right symmetric frame fails closed rather than being falsely declared distinct. The aperture ratio defined by E002-448 is mathematically invariant under horizontal reflection when left/right canthi are re-labeled in display coordinates; the synthetic landmark test checks agreement to 1e-12.

**Critical limitation:** Horizontal mirroring is easily reversed, and a rater may recognize the image. This is a controlled **nuisance-perturbed repeat-consistency challenge**, **not cryptographic blinding** or independent human evidence. The mirrored and unmirrored conditions should be separately reported, not pooled as though they were identical measurements. It does not replace independent raters or validate physical eyelid closure.

Nine local tests passed: original duplicate identification; transformed-pair inequality; actual pixel reflection; exact-symmetry fail-closed; overwrite refusal; invalid repeat mapping; missing image; PNG CRC corruption; anatomical-aperture reflection invariance; and private-summary controls (the first test also checks non-leakage). Local tests used a faithful minimal stand-in for the original encoder/aperture; the [dedicated GitHub workflow](https://github.com/sushxnthd/lucent/actions/runs/40244213282) independently completed **9/9 tests successfully** against the **actual** repository functions on implementation commit `6ebc036a56aefa9f666f939fc8de473d73ed3553`. This verifies the software counterexample and challenge, **not** real-human blinding or anatomical/physical measurement.

## Authorized private study handoff

After privately preparing an E002-448 S19 pack, run locally:

```bash
PYTHONPATH=research/observability python research/observability/e002_451_repeat_challenge.py \
  --source-root /private/e002448_s19 \
  --dest-root /private/e002451_s19_mirror \
  --summary /private/e002451_summary.json
```

Keep both masters and all images in controlled private storage; distribute **only** the new `rater_pack` to authorized independent raters, obtain consent/ethics and dataset-license permissions as appropriate, and score separately with the strict E002-450 gate. A human rater's transformed-repeat agreement remains a test of annotation consistency, **not a certified physiological measurement**.

## Independent integration evidence from previous experiment

The earlier E002-450 hosted workflow [run 40236866918](https://github.com/sushxnthd/lucent/actions/runs/40236866918) completed successfully on 2026-10-25 21:46 UTC. Its logs show **15/15** adversarial tests passing against the actual E002-448 code, including the original pooled-mean failure and incomplete-annotation counterexample. This independently verifies E002-450's software correction, **not** human anatomy.

## Scientific and product decision

E002-450's repeat-consistency result should be described as **repeat agreement on potentially recognizable exact duplicate images**, not evidence of blinded test-retest reliability. E002-451 permits an additional exploratory robustness challenge but does not solve rater independence, mirrored-image recognition, gaze, scale, exposure timing, or the hard velocity-cap problem.

**E002-371 is still NOT physically validated.** S21/S22 remain untouched. No hidden-closure guarantee, blink duration, PERCLOS, fatigue or medical claim is authorized. `ABSTAIN_UNCALIBRATED`. Keep draft PR #26 unmerged. **Next decisive action:** actual independent S19 anatomical annotations and externally authenticated physical exposure/geometry/velocity evidence; avoid further synthetic-only refinements unless they directly falsify a release claim.
