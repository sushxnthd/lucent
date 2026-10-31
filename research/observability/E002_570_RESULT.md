# E002-570 RESULT | Duplicate caught before scientific promotion

Date: 2026-10-31. Primary E002-371 kernel. Frozen protocol committed first at `bdbf4286729981af01ba1f4706f11ea799fac4c0`. This file is a **priority correction and retained regression record**, **not a new measurement-science finding**.

## Frozen test result (synthetic only)

The exact ideal-boxcar fixture uses period 1/30 s, shutter 1/100 s, unexposed gap 7/300 s, hypothetical normalized hard speed V=25/s, closure threshold 0.2, and identical ideal linear-aperture exposure means 0.615. A piecewise-linear V-shaped aperture trajectory with those exact means has gap minimum 119/600 = 0.198333..., below the closure threshold.

Substituting shutter **averages** as if they were **instantaneous gap-edge values** produces a false lower bound 97/300 = 0.323333..., above threshold. The correctly exposure-aware lower bound is 119/600 and does not exclude closure. This is an ideal mathematical counterexample, not a human blink, a measured camera, or a physiological velocity upper bound.

Before GitHub persistence, local Python tests passed **9/9**; an independently implemented Node BigInt replay passed **8 exact assertions**. The 4096-bin independent midpoint quadrature reproduced both means within 1e-6. The dedicated hosted workflow was committed, but hosted success was not verified at report creation.

## Mandatory priority correction

**This counterexample is scientifically redundant.** A repository-wide cross-check *after the frozen protocol and executable commits* found that **E002-421 (2026-10-24)** had already proved the sharp equal-boxcar law, with independent SciPy linear-program verification and a completed successful hosted run. **E002-495 (2026-10-28)** also documented the same invalid exposure-mean-as-endpoint substitution, including its own explicit duplicate correction. E002-570 merely supplies another numerical fixture and independently coded regression. Do **not** call it a novel law, new falsification of an untested hypothesis, or meaningful progress toward human validation.

References:
- [E002-421 primary internal result](E002_421_RESULT.md), hosted CI https://github.com/sushxnthd/lucent/actions/runs/40113712704
- [E002-495 duplicate correction](E002_495_RESULT.md)
- [E002-567 physical human study](E002_567_PHYSICAL_HUMAN_STUDY.md)

## Decision and stop

Preserve the freeze, executable, tests and correction as an audit trail, but **stop this synthetic boxcar line**. Do not add further synthetic exposure-average sweeps, theorem polishing, or claims of human progress. No independent anatomical raters, authenticated physical shutter captures, certified continuous-time human velocity upper bounds, or held-out physical closure predictions were obtained. The next decisive work remains real blinded human annotation and independently calibrated synchronized physical capture under E002-567. Lucent remains `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush is separate.
