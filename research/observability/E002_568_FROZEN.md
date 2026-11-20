# E002-568 FROZEN | Cohort-constrained dropped-frame no-go for E002-371

Date: 2026-10-31. Primary kernel E002-371, existing branch `research/observability-human-boundary`, draft PR #26. **Precommitted before implementing the executable.** Evidence tier: exact implication of an existing theorem and published cohort means; NOT new human data, a physiological upper bound, calibrated shutter timing, or a positive blink observation.

## Hypothesis and target

Kwon et al. 2013 (DOI 10.1098/rsif.2013.0227), as audited in E002-564, report mean peak closing speed 243 mm/s and mean initial palpebral aperture 9.83 mm for 25 volunteers. Under consistent definitions and the published point estimates, any single *universal initial-aperture-normalized upper speed ceiling applying to every measured participant in that cohort* must be at least `v0=24300/983 s^-1`. This is a **necessary lower bound on an upper bound**, not a valid physiological ceiling. It does not apply automatically to all humans or future sessions.

E002-371 gives the sharp positive-duration hidden threshold-closure feasibility condition for fully open ideal gap endpoints `a0=a1=1`: `V*H>2(1-theta)`. Equality permits at most a threshold touch. Therefore if an independently authenticated blind gap has `H>2(1-theta)/v0`, a positive-duration hidden closure is feasible even for an ideal camera reporting fully open exact endpoints, under **every** universal ceiling `V>=v0`. At equality, a threshold touch is feasible, so strict no-threshold-crossing cannot be certified. A camera with less informative exposure averages cannot recover a universal absence certificate merely by reporting high nominal FPS.

## Frozen camera test and nuisance envelopes

Use idealized global-shutter 30 Hz with exposure 10 ms and threshold `theta=1/5`. For `k` consecutive missing exposure opportunities, the blind interval between the last exposure end and the next exposure start is `H=(k+1)/30-1/100` seconds. Compute the exact critical `Hcrit=2(1-theta)/v0` in rational arithmetic. Predeclare `k=0,1,2,3` as the primary cases. Predict k=2 and 3 structural no-go, k=0 and 1 not proven no-go by this particular cohort lower-bound argument. **Neither outcome permits an exclusion without independently certified upper speed, geometry, timing and reference sensitivity.**

For uncertainty, use period interval `[Fmin,Fmax]`, exposure interval `[wmin,wmax]`, and a nonnegative endpoint timing-error bound `e`. Bound the blind gap conservatively by `Hmin=max(0,(k+1)*Fmin-wmax-2e)`, `Hmax=(k+1)*Fmax-wmin+2e`; reject impossible negative gaps and invalid ranges. Classify: `Hmin>Hcrit` = positive-duration feasible in all admissible gap realizations; `Hmin==Hcrit` = touch feasible in all; `Hmax<Hcrit` = no no-go established by this witness; otherwise = uncertainty-straddles-critical. In all cases the **product decision remains ABSTAIN_UNCALIBRATED**, because an empirical necessary speed floor cannot certify any no-closure interval.

## Falsification and independent checks

Implement exact rational Python and an independent JavaScript BigInt oracle; verify exact `Hcrit=1966/30375` seconds, four precommitted 30-Hz cases, the equality case, timing uncertainty straddling, invalid aperture/clock/shutter inputs, and monotonicity in dropped frames, theta, and timing error. Test a deliberately false inference: using `v0` as a *safe upper bound* to certify no closure at k=0 or 1 must be rejected. Test that no output ever reports a human blink observation or product clearance.

## Scope and stop

This is a **conditional negative product boundary**, not a novel general theorem or measurement of a human shutter event. A real camera's exact exposure timing, rolling shutter, geometry, illumination, gaze, glasses, blur, missingness and clocks are not authenticated here. The ideal endpoint assumption makes the no-go stronger; nuisance effects cannot justify a positive absence claim. Do not use this to claim k=2 hidden blinks actually occurred or k<=1 are safe. The next decisive experiment remains two real blinded human anatomical raters and original synchronized physical optical acquisition under E002-567. No more dataset metadata archaeology or proxy tuning. Product `ABSTAIN_UNCALIBRATED`; release `BLOCKED`.
