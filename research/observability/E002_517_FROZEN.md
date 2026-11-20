# E002-517 | Frozen exact coded-optical collision falsification

Date: 2026-10-29. Primary E002-371 branch and draft PR #26. This protocol is committed **before** the new seeds are executed. Evidence tier: exact synthetic instrument-identifiability falsification, not physical camera or human physiology.

## Question

E002-514 reported 199/200 unique exposure intervals among selected held-out synthetic camera frames. Does that establish *global* identifiability of all possible exposure intervals from the eight independent binary LED channels? The predeclared alternative is an exact pair of distinct shutter windows with identical eight-channel exposure averages despite a fully known optical code, ideal linear radiometry, zero noise and an independently known code clock. Such a collision would defeat **unique point timing** but not the conservative set-valued inverse (which must retain both).

## Frozen experiment

- Five fresh seeds: **211, 223, 227, 229, 233**. Never reuse E002-514's 101/103/107/109/113 held-out cohort to select the primary outcome.
- Use exactly E002-514's `optical_code(seed)`: eight independent pseudo-random binary channels, 1-ms ticks, 1600 ticks. No learned or optimized code.
- Exhaustively enumerate starts and each duration in **8, 9, 10, 11, 12 ms**, with exposure fully within the record. Calculate every channel average as an **exact rational number**, not a float or a tolerance-based approximate match.
- Primary collision definition: two distinct starts of the **same exposure duration**, at least **50 ms apart**, with identical eight-dimensional rational exposure means. Report counts per duration/seed, first collision in lexicographic (duration,start_a,start_b) order, and maximum observed separation. Include all negative seeds, if any.
- Primary prediction: at least one exact same-duration collision across the five frozen seeds. Failure to find any is a negative result, not permission to change seeds or tolerances.
- Secondary predeclared two-world witness: find the first seed (in listed order) with a **10-ms** collision at starts `s1 < s2`, `s1 >= 30`, `s2-s1 >= 50`. Use a left 10-ms exposure at `[s1-30,s1-20]`. World A has right exposure `[s1,s1+10]`, world B has right exposure `[s2,s2+10]`. Both have identical photodiode code and both frame observation vectors. Their true blind gaps are 20 ms and `20+(s2-s1)` ms, respectively. A hypothetical **50-ms timing budget** therefore yields opposite truth values. This is not an eyelid or physiological certificate.
- Verify both right intervals occur in the existing exhaustive `compatible_intervals` solver with zero envelope, and that `blind_gap_upper` never understates either world's gap. The solver is permitted to abstain or return a broad upper interval; it must never silently pick the earlier interval.
- Controls: exact rational equality; same duration; non-overlap; independent deterministic code regeneration; perturbation of the right observation must not be reported as the same exact collision; no nominal FPS or metadata used in inverse; product always `ABSTAIN_UNCALIBRATED`, release `BLOCKED`.

## Decision and limits

If a collision exists, retire any claim that eight coded LEDs *guarantee* unique per-frame exposure timing over the entire record. Require a prevalidated injectivity/separation margin for the specific codebook and nuisance envelope, or retain the full candidate set and abstain when timing uncertainty is too broad. The E002-514 selected-frame result remains true but cannot be extrapolated to every possible frame. No human labels, physical shutter truth, physiological speed ceiling or held-out physical closure prediction is acquired here.

This is one targeted **ideal-model falsification**, not another synthetic parameter sweep or evidence for hardware deployment. Stop further code-seed archaeology after this fixed test and return to actual independent optical capture and two blinded anatomical reviewers.
