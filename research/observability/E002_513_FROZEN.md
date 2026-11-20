# E002-513 | Frozen non-affine clock counterexample to long-span optical calibration

Frozen 2026-10-29 before implementing or executing E002-513. Primary E002-371 kernel; preserve `research/observability-human-boundary` and draft PR #26. This is a **new identifiability falsification of the affine-clock assumption** in E002-506, not another sweep of its optical timing precision, a measured camera, or a human-eyelid observation.

## Exact question

Can optical events assigned to native frames 0 and 300, with **perfect independent timestamps**, exclude a hidden closure at a particular unobserved inter-frame gap if frame starts are only known to be monotone, rather than certified affine? E002-506's 300-frame conditional exclusion explicitly assumes a stable affine clock. Attack that assumption while keeping the observed optical anchors, shutter duration, exposure-mean values and stipulated eyelid-speed bound identical.

## Prespecified two-world construction

Both worlds have 301 consecutively numbered frame starts `t[0]...t[300]`, `t[0]=0`, `t[300]=10 s`, a **hypothetical** global shutter with fixed `w=0.010 s`, no frame drops, the same sensor row and identical perfect optical edge observations at the two anchor frames. The optical edge at each anchor is assigned to the start of its exposure. Neither world claims actual optical data.

- World A: all 300 inter-frame intervals equal `1/30 s`.
- World B: interval 150 -> 151 is `1/30 + 0.002 s`; each of the other 299 intervals is `1/30 - 0.002/299 s`. This preserves `t[300]=10 s` exactly and keeps every interval positive and longer than the exposure. The anchor observations are **identical**. Do not optimize the spike or its location after seeing any real data.
- The sharp scalar bound from E002-373 is evaluated at the **target local gap** using the same stipulated `V=60/s`, exposure mean `b=0.999`, mean error `r=0.001`, threshold `theta=0.20`. World A should conditionally exclude a hidden closure; World B should not. Neither is a physiological validation.
- Verify the exact general envelope: given `N` positive inter-frame intervals with sum `S` and independently certified minimum `p_min`, the supremum of one local interval is `S-(N-1)*p_min`, provided feasibility. With no positive minimum and only monotonicity, the supremum is `S`. A bound on the **average** period does not bound an individual gap.

## Kill criteria and controls

1. If both worlds cannot reproduce identical optical anchor times and frame numbers, reject the witness.
2. If either world drops/reorders frames, has nonpositive intervals, or overlaps the 10-ms exposures, reject.
3. If the stipulated risk does not cross the strict 0.8 exclusion threshold, reject the proposed falsification and preserve the failure.
4. Check that an **additional independently timed pulse at the target gap** could distinguish the worlds; the test is not a claim that all optical measurements are useless.
5. Reject the false inference that arbitrarily precise long-baseline pulses certify **local** blind gaps absent an affine-clock or independently bounded local-jitter premise.
6. Keep camera timing, shutter, eyelid speed, anatomical ratings, human identities, and product claims unverified. Synthetic data and software test passes never certify them.

## Decisive physical handoff

On an authorized no-cost instrument bench, first independently measure the exposure-start time at **every frame surrounding a preregistered target gap**, not only two widely separated optical events. Use a calibrated optical/photodiode timing reference, externally established exposure-to-frame attribution and a separate measurement of shutter start/end and rolling-shutter row timing. Check frame continuity, local timing residuals, missingness, geometry, brightness and blur. If this cannot be done, record **local gap unknown** and abstain. Do not use a display animation or AVI FPS as an independent clock. The existing E002-507 two-rater S01 packet remains the human feasibility protocol; do not reselect its clips, invent annotations, or infer physical continuous-time eyelid speed from native finite differences.

## Evidence tier and product

Only a deterministic two-world counterexample is planned. It can invalidate an overbroad *inference from long-span optical anchors*, not E002-371's conditional theorem and not E002-506 under its **explicit affine assumption**. No physical human or camera measurements are expected. `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. Do not expand this into another synthetic parameter sweep; next actual evidence is independent anatomical reviewers and a physical camera timebase.
