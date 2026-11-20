# E002-602 | Public answer schedule defeats class-balanced synthetic rater qualification

Date: 2026-11-02. Primary E002-371 workstream. Frozen protocol committed first at `a3897bd` before the executable and before the hosted attack. Evidence tier: **SYNTHETIC_INSTRUMENT_FALSIFICATION**, not human ratings or physical shutter validation.

## Confirmed falsification

The actual corrected E002-601 Python grader and the independently implemented E002-600 Node.js oracle both **qualified a no-image attacker**. The attacker generated the entire reviewer export using only public source constants (`PULSES`, `NUISANCE`) and fixed approximate coordinates; it never opened a generated PNG and did not read owner-only truth before sealing its export. The public source fixed all closure indices, all nuisance clips and aperture gaps (4 vs 34 px); the upper-lid jitter is irrelevant because the grader measures aperture differences at x=320 and permits 5-px per-margin uncertainty.

| Hosted result, two independently seeded private image packets | Observed |
|---|---:|
| Clean frames measured | 114/114 |
| Truth intervals covered | 114/114 |
| Correct decisive OPEN | 103/103 |
| Correct decisive CLOSED | 11/11 |
| Nuisance abstentions | 76/76 |
| False classifications | 0 |
| Qualified by corrected E002-601 gate | **YES** |
| Independent Node.js oracle agreement | **Exact** |
| Negative control: all clean frames declared OPEN | **REJECTED**, 11 false OPEN |

[Hosted CI #41387555887](https://github.com/sushxnthd/lucent/actions/runs/41387555887) **COMPLETED SUCCESSFULLY**, with the aggregate printed in the job log. The frozen [attack executable](e002_602_public_answer_attack.py) used the genuine E002-600 private-seed image generator and grader. Both private seeds yielded the same aggregate; the image content changed with seed, but the publicly exposed answer schedule did not.

This falsifies the claim that the corrected class-balanced gate demonstrates a reviewer's ability to read synthetic eyelid images. It does **not** falsify the correctness of the gate's arithmetic, imply anything about real human rater competence, or establish blink/eyelid physics.

## Consequence and repair

**The original E002-600/E002-601 publicly fixed challenge must not be used to qualify human anatomical raters.** A passing score can be manufactured without inspecting the stimulus. E002-603 is the separate frozen repair track: privately randomized per-frame closure schedules and nuisance assignments, source-image hash checks, and explicit rejection of the E002-602 no-image attack. The E002-601 class-balanced criteria remain necessary but are not sufficient for genuine blinded qualification. Public development seeds are not valid human qualification seeds.

No actual human anatomical labels, independently calibrated iris geometry, shutter/clock calibration, certified continuous-time eyelid velocity ceiling, or held-out physical closure prediction were obtained. Product `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. Hush branch/PR #45 unchanged.
