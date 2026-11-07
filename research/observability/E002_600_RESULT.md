# E002-600 | Blinded synthetic eyelid-rater qualification instrument

Date: 2026-11-02. Primary E002-371 workstream. [Frozen protocol](E002_600_FROZEN.md) was committed first at `2d986d9`, before code and test implementation. Evidence tier: **SYNTHETIC_REVIEWER_INSTRUMENT_ONLY**.

## Concrete new instrument

[Generator and fail-closed grader](e002_600_phantom_rater_challenge.py) produce a 190-frame, 10-clip, 640x480 **synthetic** eyelid packet compatible with the actual [E002-598 offline native reviewer](e002_598_offline_rater.html). Reviewer A and B receive blank E002-574 native templates; the 190 PNGs and owner-only SHA-256/ground-truth manifest are generated locally and must never be committed. A fresh private seed is used by default. Synthetic geometry has known upper/lower margins at a reference x column and a **synthetic** iris diameter of 100 px.

The locked arms include an always-open control, one-/two-/three-/four-native-frame closure pulses, an observed-endpoint closure, and separately flagged brightness, blur, occlusion/glasses and gaze/geometry challenges. These are **not realistic human eyelid trajectories**, and native frame index sampling is **not physical exposure integration**.

The grader accepts only exact native reviewer exports and reports, for each reviewer separately: clean measured fraction, interval coverage of known synthetic aperture, false OPEN/CLOSED classifications, and nuisance abstention. Frozen qualification thresholds: at least 80% clean coverage, at least 95% declared-interval coverage among clean measured frames, at most one false CLOSED and at most one false OPEN. These are instrument-qualification choices, not estimates of clinical accuracy or physiological validity.

## Actual synthetic execution and negative controls

On the locally generated locked-seed packet:

| Check | Observed |
|---|---|
| Generated images | 190 PNGs; all 640x480; all SHA-256 hashes matched private truth |
| Clean frames | 114 |
| Nuisance frames | 76 |
| Exact fixed-seed replay | Identical truth and frame hashes |
| Different-seed control | Truth and frame hashes changed |
| Ideal synthetic reviewer fixture | 114/114 clean frames measured; 114/114 uncertainty intervals covered; zero false OPEN/CLOSED |
| Blank reviewer fixture | 0/114 clean frames measured; **qualification refused** |
| Two fabricated false CLOSED labels | **Qualification refused** |
| Malformed/missing/nonfinite reviewer exports | Rejected |
| Python regression | 7/7 passed locally |
| Independent Node score oracle | Exact match on ideal and blank fixtures |

The ideal fixture is **programmatically generated from ground truth**. It is not a human reviewer and is not evidence that humans can accurately label the challenge. No rater completed the packet. [Independent JavaScript oracle](e002_600_independent_replay.cjs) does not import Python scoring logic; [test suite](test_e002_600_phantom_rater_challenge.py) compares full outputs. [Dedicated hosted CI](../../.github/workflows/e002_600_phantom_rater.yml) is committed; hosted success must be checked independently.

## Reproduction and private handoff

```bash
python -m pip install 'Pillow>=10,<12'
python research/observability/e002_600_phantom_rater_challenge.py build --output /PRIVATE/e002_600
# Load /PRIVATE/e002_600/reviewer/template_A.json and its clips folder
# in the offline E002-598 interface. Use B for a genuinely separate rater.
python research/observability/e002_600_phantom_rater_challenge.py grade \
  --truth /PRIVATE/e002_600/private/truth.json \
  --review /PRIVATE/E002_598_A_NATIVE_RATINGS.json
```

Do not share the `private/truth.json` with reviewers before they complete the challenge. Do not upload the source images, seed, truth or reviewer exports to GitHub. The existing offline interface still does not cryptographically bind reviewer exports to source frame hashes; this grader relies on owner-private pairing and cannot independently authenticate reviewer identity or input provenance.

## What this changes and does not change

The instrument supplies a falsifiable **pre-human-study rater qualification gate**. Human raters should not be promoted to the E002-371 anatomical-validation cohort unless they meet the frozen qualification criteria on genuinely independently completed challenge packets. The independent human study still requires actual native human eye footage, blinded distinct raters, calibrated shutter and clock, a defensible continuous-time velocity bound, and prospectively frozen held-out physical predictions.

**Evidence obtained this run:** reproducible synthetic images and independent score checks. **Evidence not obtained:** any new human annotation, human accuracy estimate, physical shutter calibration, certified human velocity ceiling, or held-out physical closure prediction. Product `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. PR #26 remains draft/unmerged. Hush branch and PR #45 were not changed.


## Superseding instrument-validity finding (E002-601, 2026-11-02)

**Do not use the original E002-600 aggregate qualification rule to qualify human reviewers.** The frozen E002-601 attack demonstrated that it accepted a reviewer with zero decisive classifications (50-px blanket uncertainty) and a reviewer who abstained on every closed frame. Both attacks passed the original gate in a source-pinned hosted execution, with matching independent Node.js replay. See [E002-601 result](E002_601_RESULT.md). The corrected grader requires class-balanced decisive coverage and nuisance abstention. Neither the original nor corrected synthetic qualification supplies actual human rater evidence or physical E002-371 validation.


## Superseding stimulus-blinding finding (E002-602, 2026-11-02)

**The fixed E002-600 challenge is not a valid blinded human-reviewer qualification instrument, even with the E002-601 corrected grader.** Its publicly exposed pulse indices, nuisance clips and nominal aperture geometry let an attacker who never sees any PNG obtain 114/114 covered clean measurements, 103/103 correct decisive OPEN, 11/11 correct decisive CLOSED and 76/76 nuisance abstentions. The actual patched Python grader and independent Node.js oracle both qualified the attacker in [successful hosted CI #41387555887](https://github.com/sushxnthd/lucent/actions/runs/41387555887). See [E002-602 result](E002_602_RESULT.md). All original fixed-schedule qualification scores are now **NONBLIND_DEMONSTRATION_ONLY**. E002-603 develops a separate private-answer replacement; no real human qualification or E002-371 physical validation has occurred.
