# E002-576 | Frozen, source-bound LPW dual-rater alias evaluator

Date: 2026-11-01. Primary scientific kernel E002-371. Extends E002-573, E002-574 and E002-575 without altering the selected 330 held-out 19-frame windows, the 11/11 participant split or the three predeclared index-decimation phases.

## Substantive contribution

The previous LPW work stopped at producing blinded native-frame packets. E002-576 adds the missing **post-rating positive-only evaluation path**, with explicit source audit, independent scale-uncertainty gating and participant-level evidence accounting. It consumes only owner-private mappings, source-audit hashes, two independently completed E002-574 rater JSON exports, and a separately documented per-video iris-diameter error budget. It never consumes raw imagery and emits only nonidentifying aggregates.

The evaluator refuses to infer OPEN/CLOSED from rater agreement alone. For each rater, if upper/lower eyelid positions are u,l with per-landmark error e and iris diameter d with independently established error delta, it constructs the conservative normalized interval

    [max(0,l-u-2e)/(d+delta), max(0,l-u+2e)/(d-delta)]

with d>delta>0 and e>=0.5 pixel. Two rater intervals must overlap, and **both entire intervals** must lie above c=0.20 (OPEN) or at/below c (CLOSED). Any disagreement, nuisance flag, missing value, unreviewed frame, zero pixel error, unbounded denominator or threshold overlap becomes abstention. This avoids the previously demonstrated E002-503 common-mode iris-scale false-consensus shortcut.

For each of the three frozen 3:1 index phases, the evaluator counts only adjacent retained OPEN endpoints enclosing at least one unretained CLOSED native frame. It reports phase counts, eligible endpoint pairs, windows and participants with a witness, and all abstentions. It does not claim 30-fps physical exposure, blink duration, PERCLOS or physiological fatigue.

## Evidence and tests

The committed [frozen protocol](E002_576_FROZEN.md) precedes the implementation. The [Python evaluator](e002_576_lpw_alias.py) and [16 synthetic adversarial tests](test_e002_576_lpw_alias.py) cover positive witnesses, no-witness and incomplete reference, rater disagreement, denominator threshold reversal, zero uncertainty, missing/false calibration, altered source-frame binding, duplicate audit rows, wrong rater identity, missing clips, nuisance flags, private aggregate minimization and input order invariance. These are **scripted synthetic ratings**, not two real humans.

[Hosted CI run 41240071640](https://github.com/sushxnthd/lucent/actions/runs/41240071640) was queued when this report was written; no hosted success is claimed.

## New evidence limitations

No LPW video was acquired or processed, no independent human anatomical rater pair was obtained, and no physical camera shutter or eyelid velocity ceiling was calibrated. The JSON field `independently_validated=true` is **an owner assertion, not a cryptographically or externally verified credential**. Therefore even a positive evaluator output must be reported as a conditional candidate until source custody, reviewer independence and scale provenance are verified outside this tool. No negative result is a closure-absence certificate.

**Evidence ledger:** authentic LPW acquisition 0; independent human rater pairs 0; authenticated physical shutter captures 0; certified continuous-time speed ceilings 0; held-out physical closure predictions 0.

**Next:** complete the actual private dual-human review on authenticated LPW or S01 frames, then E002-567 synchronized camera/photodiode acquisition. Do not continue synthetic theory iteration in lieu of human data. **Product ABSTAIN_UNCALIBRATED; production BLOCKED.** Hush's separate branch and draft PR #45 were not modified.
