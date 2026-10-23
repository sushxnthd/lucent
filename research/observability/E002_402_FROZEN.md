# E002-402 — frozen geometry-identifiability and two-rater bridge test (2026-10-24)

**Pre-execution protocol; no human calibration or human validation claimed.** Keep PR #25 draft and the existing research branch. This is a source-level falsification of the *input measurement* to E002-399, not a change to the shutter-gap theorem.

## Hypothesis and physical definition

The existing E002-399 bridge computes `hypot(x_upper-x_lower, y_upper-y_lower)` as an eyelid aperture. A vertical physical palpebral gap at a calibrated reference column cannot be inferred from diagonal distance when landmark columns differ. In particular, an eye with zero vertical gap and 20-pixel horizontal displacement is falsely interpreted as having 20 pixels of opening.

Define the target as the signed **vertical** lower-minus-upper eyelid separation at a separately calibrated reference column x0, not an unconstrained Euclidean landmark distance. This definition is conditional on independently validated camera pose/normal and on the chosen anatomical reference column. With independently bounded slopes |dy_upper/dx|<=S_u and |dy_lower/dx|<=S_l, rater coordinate errors bounded by E in each axis, and observed points (xu,yu),(xl,yl), the target gap lies in

  [yl-yu - B, yl-yu + B],
  B = S_u*|x0-xu| + S_l*|x0-xl| + E*(2+S_u+S_l).

The two-rater union, not their average or intersection, is used; each rater's interval may be centered on a different pixel. Divide lower pixel gap by the independently bounded maximum iris scale, and upper gap by minimum scale. If either rater has inverted eyelid order or any required geometry parameter is missing/nonfinite, abstain/exclude. No claim is allowed merely from the prior Boolean `aperture_geometry` flag.

## Frozen tests (do not change after seeing outcomes)

- G1: With constant zero physical vertical gap, upper=(60,40), lower=(80,40), iris scale 50px, theta=0.2, zero landmark error and zero shutter/optical/row errors, the **legacy diagonal** method can falsely certify no crossing at 0.4 while the corrected signed-vertical measurement cannot.
- G2: At fixed reference x0=70, slope envelopes S_u=S_l=0.2, and zero coordinate error, two differently sloped lid contours produce measured landmarks whose true reference gap is enclosed by the new interval, including a case where naive vertical subtraction is optimistic.
- G3: Across 1,000 held-out seeded synthetic trials (seed 402), independently sample linear upper/lower contours, x positions, x0, scales and coordinate noise bounded by E. The proposed interval must enclose the exact true gap in every trial, including a negative-gap nuisance case which must be rejected before certification. Count rejection/abstention separately.
- G4: Bridge with all historical Boolean gates true but absent quantitative geometry returns ABSTAIN_UNCALIBRATED; supplying synthetic independent geometry and zero row/optical error restores the original clean positive control; introducing a diagonal-offset zero-gap witness must never yield CONFIRMED_NO_CROSSING.
- G5: Increasing independently bounded slope or landmark error must never shrink the interval or turn a previously unresolved shutter-gap certificate into an asserted certificate.
- G6: An independent checker, using an alternative geometric evaluation of linear contours and random pointwise perturbations, verifies the error envelope without calling the implementation's interval calculator.

## Scope and limitations

No claim that a vertical 2D pixel gap equals physical aperture under arbitrary gaze, pose, perspective, occlusion or optical distortion. These remain separate external calibration and nuisance gates. Synthetic slopes, rater coordinates and camera geometry are **not** measured human bounds. Record negative tests, preserve old E002-399/400/401 regressions, and keep product ABSTAIN_UNCALIBRATED until independent geometry, shutter, optics, timing and velocity evidence exists.
