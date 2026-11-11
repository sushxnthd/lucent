# E002-599-G | Prospective geometric-slope error-budget amendment

Date: 2026-11-02. Frozen **before** implementation of the geometric-error extension. The initial E002-599 protocol's 1-pixel same-column gate is necessary but not sufficient for anatomical certification. Even a 0.5-pixel column mismatch can change eyelid margin y arbitrarily if local lid slope is unbounded.

## Added falsification and strict decision
For each blind clip, require an independently calibrated nonnegative upper bound S (pixels of vertical eyelid-margin motion per pixel of horizontal displacement) for **both** upper and lower margins over the registered column neighborhood. The owner-only calibration field is `max_lid_slope_px_per_px`; absence or invalid value means no usable scale budget and all frames for that clip must be UNCERTAIN. An owner-provided S is an unverified premise, not an independent measurement.

For a rater clicking column x and calibrated reference x_ref, set e_eff = e + S*abs(x-x_ref). Use [max(0,l-u-2e_eff)/(d+delta), max(0,l-u+2e_eff)/(d-delta)] instead of the earlier no-slope interval. This is conservative under the explicit bound |du/dx|,|dl/dx|<=S and the other stated uncertainty assumptions. The x registration gate remains <=1 native pixel; it does not establish S.

## New frozen tests
- Missing S must force all affected measured frames to UNCERTAIN.
- Exact x=x_ref must reproduce previous classifications even with S>0.
- A nonzero x offset with large S must convert an otherwise OPEN/CLOSED classification into UNCERTAIN.
- Negative, nonfinite or absurdly large S must be rejected. The finite input cap S<=100 is a schema sanity limit, not a scientific ceiling.
- An independent integer-rational oracle must test the same uncertainty expansion without importing the Python implementation.

No human, camera, physiology or release claims are promoted. Preserve original E002-599 freeze and note this pre-implementation extension explicitly.
