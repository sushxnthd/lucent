# E002-521 | Frozen exposure-mean-to-closure-duration test

Date: 2026-10-29. Primary E002-371 kernel, existing research branch and draft PR #26. Frozen before implementation or numeric tests. Evidence tier: exact measurement inference and synthetic adversarial verification, **not** human or physical validation.

## Empirical constraint and scope
Two targeted public-data searches this run identified 600-fps published blink kinematics (Kwon et al., 2013) without downloadable participant-level raw trajectories, the 150-fps EyeInfo dataset behind authenticated Google Drive DVC, and a 2026 hardware-synchronized FaceBase eyelid dataset with restricted human-subject access. Existing checksum-verified S01 has an unresolved native acquisition rate and no independent anatomical ratings. None can support a participant-disjoint physical E002-371 test now. Do not restart dataset archaeology or claim a new human result.

## New question, distinct from E002-520
E002-520's transported reference mean at or below the ordinary-camera closure threshold establishes at least one threshold contact, but a **threshold touch is not a sustained blink**. Freeze whether a *strict* exposure-mean margin can certify a minimum **total time spent below threshold** inside the blind gap, without inventing a speed ceiling. This is total measure, not a contiguous closure episode.

Assume (i) ordinary physical aperture a(t) in [0,1] is measurable, (ii) a single independently timed reference exposure E has uniform, linear temporal weighting and duration w >= w_min > 0, (iii) E is strictly inside the ordinary-camera guaranteed blind interior under all clock/row uncertainties, (iv) a calibrated pointwise cross-camera transport a_o(t) <= K a_r(t)+B with K,B>=0, (v) an independently validated reference exposure-mean bound mean_E(a_r)<=U, and (vi) the ordinary threshold theta is frozen with 0<theta<=1.

Let M=K U+B. For C={t in E:a_o(t)<=theta}, derive the dimensionless measure fraction p=|C|/w. Prediction:
- If M<theta, p >= 1-M/theta >0, hence |C| >= w_min(1-M/theta). This bound is sharp as an **infimum** over measurable [0,1]-valued trajectories with no derivative constraint, not necessarily sharp under a separately bounded velocity.
- If M=theta, a threshold contact follows under suitable continuity but no strictly positive closure-duration bound follows from the mean alone.
- If M>theta or any prerequisite fails, do not assert closure contact or duration.
- The bound is for **total measure**, not an uninterrupted dwell interval, blink event, PERCLOS, fatigue, or absence of closure in the rest of the gap.
- If shutter temporal weights are nonuniform or unknown, no physical-time fraction bound is allowed from the weighted mean alone. A sensor-response adversary must falsify any implementation that silently assumes uniform weighting.

## Frozen numeric and adversarial predictions
1. theta=0.20, U=0.19, K=1, B=0, w_min=8 ms: M=0.19, p>=0.05, closure measure >=0.4 ms, conditional and not a full blink.
2. K=1.2 on same U: M=0.228, no witness.
3. U=0.20, K=1: contact-only (if continuity), **zero** positive-duration bound.
4. Explicit two-level constructions with a=0 on a fraction p_eps=1-U/(theta+eps) and a=theta+eps elsewhere approach the bound from above as eps->0, for U<theta; continuous ramps may approximate but not equal this infimum.
5. Missing independently calibrated uniform integration, exposure-duration lower bound, cross-camera transport, geometry, clock, native frame provenance, independent raters, or nuisance control => UNKNOWN, not false clearance.
6. Invalid threshold, nonfinite bounds, duplicate IDs, negative durations, noncontaining timing, or malformed evidence => reject/UNKNOWN. A reference OPEN observation never proves no hidden closure.
7. Use exact rational arithmetic on finite-decimal input to prevent floating-point near-equality creating a fictitious positive margin. Independently cross-check frozen numbers using a second implementation.

## Decision and release
Create a versioned offline evaluator and adversarial tests. A qualifying strict-margin witness inside an EXCLUDE gap is a **conditional falsification of that exclusion** and additionally gives a lower bound on total closure time. Equality only supports the older contact conclusion, not a duration. The software cannot authenticate human raters or instrument calibration; these are external evidence requirements. No unconditional blink count, sleepiness, PERCLOS or medical claim. For every outcome: product ABSTAIN_UNCALIBRATED; release BLOCKED. No merge or Hush modification. Next decisive empirical action remains independent S01 anatomical ratings and physical shutter/clock/geometry calibration.
