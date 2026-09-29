# E002 Protocol Amendment 001 — Capture Order

**Status: frozen before any real E002 phone capture is analyzed.**

## Reason for amendment

E002 already fixed the three stimulus conditions and required at least three repeats per condition, but it did not predeclare the order of the nine planned captures.

Condition order can create avoidable ambiguity through:

- pupil adaptation;
- short-term visual carryover;
- participant settling;
- gradual lighting or pose drift;
- ordinary time-on-task effects.

This amendment fixes the order **before empirical capture**. It does not change the stimulus sequences, quality gates, observability endpoints, or exit rule.

## Fixed nine-capture order

| Capture | Condition |
| ---: | --- |
| 1 | passive |
| 2 | contiguous |
| 3 | split |
| 4 | passive |
| 5 | split |
| 6 | contiguous |
| 7 | split |
| 8 | contiguous |
| 9 | passive |

Each condition appears exactly three times.

The schedule deliberately places every condition across the early, middle, and late parts of the session and includes every directed condition-to-condition transition at least once.

## Execution rule

Use one stable phone, one stable indoor lighting setup, one comfortable fixed screen-brightness setting, and one approximately fixed viewing distance for the full nine-capture set.

Do not reorder captures after seeing any video, pupil trace, quality metric, or condition difference.

If a capture fails technically, retain its metadata, mark it failed under the frozen E002 quality gates, and repeat that **same capture number/condition immediately once**. Do not substitute a different condition to maintain convenience.

The original planned capture and any technical retry must remain distinguishable in filenames/notes.

## Analysis rule

The primary E002 decision still uses the first planned nine captures subject to the frozen usability gates.

A technical retry may replace a failed planned capture only when the failure is attributable to a predeclared technical exclusion, not because the biological-looking response is weak or unfavorable.

## Claim boundary

This amendment only reduces order-related researcher freedom in an engineering observability pilot. It does not turn E002 into a behavioral-state validation experiment.
