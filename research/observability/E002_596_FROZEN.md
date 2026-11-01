# E002-596 | Frozen continuous-phase falsification of E002-595 95-to-30 review design

Date: 2026-11-02. Primary E002-371 kernel. Freeze before running the exact phase-enumeration instrument. This is **index-only sampling design**, not human eyelid measurement, physical shutter timing or closure prevalence.

## Target and predeclared hypothesis
E002-595 used phases p=0,1,2 measured in native 95-Hz frame intervals, asserted that native index 9 was missed by their union, and reported six retained frames per phase in each 19-frame window. But nominal 30-Hz sampling admits continuous phase 0 <= p < 95/30 = 19/6, including integer p=3. Hypothesis: p=3 selects native index 9, so the index-9 blind spot is **a property of the selected three phases, not an intrinsic blind spot of 95-to-30 conversion**. p=3 may also retain only five native frames within a 19-frame truncated window, contradicting any extrapolation of six-per-phase to arbitrary phase.

## Exact model and falsification tests
For each k>=0, sample at p+19k/6 native-frame units and use nearest native index floor(p+19k/6+1/2), half-up, keeping indices 0..18. Enumerate **all** distinct mappings over p in [0,19/6) by constructing the exact rational half-integer crossing points, testing every open interval midpoint and every included boundary. Do not silently assume integer p values exhaust continuous phase. For every mapping count sampled indices and missed discrete pulses of widths 1,2,3,4. Compare the four integer p=0,1,2,3 mappings, all-phase mapping range, and three-phase versus four-phase union. Check exact endpoints, ties, truncation and source-window offset.

## Independent verification and kill conditions
Implement an exact-rational Python enumerator and independently written JavaScript BigInt/rational oracle; compare serialized complete phase-signature histograms, critical boundaries and pulse counts. Include invalid input and off-by-one controls. The hypothesis is killed if p=3 fails to cover index 9 or the exact enumeration shows that p=0,1,2 exhaust all continuous-phase mappings. A passing finding is a **design correction**, not a human or physical observability result.

## Product and study consequence
No single finite phase schedule is a physical shutter model. Report phase-dependent misses without choosing favorable phases; a phase-balanced review should include p=3 as a fourth *integer* phase and/or precommit a continuous-phase sensitivity analysis, with unequal within-window sample counts handled explicitly. Do not rewrite the E002-595 result as if its three-phase counts were incorrect; they are valid for those three phases only. No new held-out human data or private images may be accessed. No synthetic exclusion certificate may be promoted to physiology. Product ABSTAIN_UNCALIBRATED, release BLOCKED, PR #26 draft.
