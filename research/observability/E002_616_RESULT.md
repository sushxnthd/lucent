# E002-616 | Bilateral human full-closure virtual-alias test

**Status (2026-11-03): preregistered source experiment committed; hosted human-source outcome pending.** Parent E002-371. Frozen *before bilateral source analysis* at [commit d3a3593](https://github.com/sushxnthd/lucent/commit/d3a3593fedb500ede42e44e3b9bddcece8bfada0). This is a distinct anatomical question from E002-582 and E002-615: can **simultaneous bilateral** investigator-labelled 90–100% eye closure be absent under virtual 30-Hz point sampling? An omitted single-eye FC run is not sufficient to answer that question.

## Completed prospective artifact

- [Frozen protocol](E002_616_FROZEN.md) fixes bilateral run definition, nuisance abstention, phase schedules, source SHA-256, falsifiers and reporting before the outcome is observed.
- [Source-bound executable](e002_616_bilateral_alias.py) uses the established authenticated five-sequence Silesian5 source, and requires both left/right FC=C for a contiguous interval. It excludes source-boundary, nonconsecutive, nonfrontal and either-eye-not-visible cases. It compares ten predeclared original floor-index phases with ten actual source-time nearest phases.
- [Independent JS oracle](e002_616_independent.cjs) checks the exact 7/4/1/0 phase law on eight synthetic run lengths and independently checks bilateral event construction, split events, nuisance exclusion and missing-frame abstention. **12/12 local JS checks passed.**
- The Python executable's **six synthetic test groups passed locally** with independently stubbed source-selection dependencies. This confirms test logic, **not** authentic source replay. Python compile succeeded.
- [Dedicated hosted workflow](../../.github/workflows/e002-616-bilateral-alias.yml) runs the real SHA-pinned public human annotation source and prints only anonymous aggregate counts. [Corrected hosted run #41535538159](https://github.com/sushxnthd/lucent/actions/runs/41535538159) was queued at the last check; no source-derived bilateral counts are claimed yet. The earlier queued run #41535482335 precedes the correction that preserves possible length>=4 timestamp-selector surprises instead of aborting.

## Frozen outcomes still to be resolved

Number of eligible simultaneous bilateral FC runs; distribution of run lengths; number omitted by at least one virtual phase; paired phase-level disagreement between original index and actual source-time nearest selectors; long-run timestamp-selector surprises. A zero-positive bilateral result must be retained as a negative outcome, not substituted with per-eye evidence.

## Evidence boundaries

E002-582 independently verified **76/567 per-eye** runs omitted under at least one nominal 30-Hz index phase; E002-615 found **82/5,670** paired per-eye phase decisions changed when actual source timestamps were used. **Neither result is a bilateral event count.** This experiment cannot establish actual 30-fps exposure integration, an independently measured camera clock, continuous eyelid aperture, certified maximum human eyelid speed or an E002-371 physical exclusion certificate. Only five investigator-labelled source sequences are available, with no independent anatomical re-rating.

**Product:** `ABSTAIN_UNCALIBRATED`. **Release:** `BLOCKED`. The next decisive experiment remains synchronized ordinary-camera and high-speed reference capture with independent shutter/clock measurement, blinded anatomical review, calibrated nuisance uncertainty and participant-disjoint sealed predictions. Hush branch and draft PR #45 remain untouched.
