# E002-552 priority and overlap check (2026-10-31)

**Do not claim a new general mathematical theorem.** After committing E002-552, a targeted in-repository priority comparison found the following relevant earlier results:

- [E002-421](E002_421_RESULT.md), 2026-10-24: sharp **Lipschitz/velocity** boundary for equal linear boxcar means and the dark gap, with independent SciPy LP and hosted CI.
- [E002-422](E002_422_RESULT.md), 2026-10-24: sharp **Lipschitz/velocity** unequal-mean boundary over the full shutter horizon in a balanced-slope regime.
- [E002-461](E002_461_RESULT.md), 2026-10-26: nonlinear shutter-transfer/static-inverse counterexample and conservative variance repair.
- [E002-495](E002_495_RESULT.md), 2026-10-28: independently rediscovered E002-421's exact Lipschitz equal-boxcar result and explicitly corrected its novelty claim.
- [E002-538](E002_538_RESULT.md), 2026-10-30: sharp **acceleration/curvature** interpolation from instantaneous anatomical endpoints.
- [E002-547](E002_547_RESULT.md), 2026-10-30: reference closure erased by shutter integration.
- [E002-551](E002_551_RESULT.md), 2026-10-31: local bounded-curvature interpolation with endpoint uncertainty; explicitly requires instantaneous aperture.

**Narrow nonduplicate content of E002-552:** exact curvature/acceleration (not velocity) envelope for **linear boxcar-integrated anatomical means**, including unequal shutter durations and bounded mean errors, with a physically bounded counterexample to substituting frame averages into E002-551. This closes a model gap between E002-538/551 and E002-421/422. The formula is an elementary consequence of Jensen's inequality and concavity; classical optimal-recovery theory with integral observations almost certainly subsumes it. There is **no established literature priority or empirical breakthrough**. Its value is a falsifiable *instrument-specific* prediction and an explicit fail-closed measurement rule.

Do not mistake this for new human validation. Existing data acquisition, calibration and two independent anatomical raters remain the highest-priority tasks. No additional mathematical boxcar variants should be pursued unless physical data expose a specific unresolved failure.
