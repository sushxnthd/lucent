# E002-611 | Frozen literature-anchored shutter/velocity feasibility audit

Date: 2026-11-02. Parent E002-371, E002-608, E002-610. Research branch `research/observability-human-boundary`, draft PR #26. **Evidence tier: published human kinematic summaries + exact conditional feasibility arithmetic; no new human recordings or independent hard velocity bound.**

## Question and predeclared calculation
Can the existing E002-608 **sufficient** boxcar exclusion gate ever return `MODEL_EXCLUDE_CONDITIONAL` at ordinary camera rates for plausible *published* human upper-eyelid velocities, even with noiseless, calibrated anatomical means? The calculation is a **feasibility audit of this particular sufficient gate**, not a theorem of universal video observability and not validation of E002-371.

Assume normalized palpebral aperture `a in [0,1]`, closure threshold `tau=0.2`, physical full-open aperture `A` mm, and a stipulated continuous-time upper speed `v` mm/s. Convert to `V=v/(1000*A)` per ms. At regular frame rate `f` Hz with identical uniform boxcar exposure durations `e` ms and no dead time beyond the interframe gap, the E002-608 sufficient gate tests `2*(m-tau) > V*(gap+e)` for equal exposure-mean lower bounds `m`, where `gap=1000/f-e`. Therefore `gap+e=1000/f` and the **gate's threshold** is independent of `e` for this restricted symmetric idealization. This does **not** imply that measured means, motion blur, signal/noise, or actual observability are exposure-independent.

Predeclare exact grids: `f in {30,60,120}` Hz, `A in {7.4,9.8,12.8}` mm, `v in {93,160,243,400}` mm/s, `m in {0.5,1.0}`, `tau=0.2`; compare `e=2` ms and `e=0.8*(1000/f)` ms. All velocities are **illustrative borrowed literature values**, never verified hard bounds or directly comparable subject-level maxima. `v=400` is a conservative round-number scenario anchored to Doane's report that some spontaneous blinks exceeded 40 cm/s, **not** an asserted population maximum. For each case report strict `m > tau + v/(2*A*f)` and the dimensionless feasibility ratio `Q=v/(2*A*f*(1-tau))`. If `Q>=1`, this sufficient gate cannot exclude closure for **any** `m<=1`; equality must abstain. The term `Q` is a reparameterization of E002-608, not a novel physical law.

## Primary sources and selection limits
- Godfrey et al., *Ophthalmic Plastic & Reconstructive Surgery* (2019), DOI 10.1097/IOP.0000000000001356, PMID 30893187: 240-fps spontaneous blink recordings in 10 adults, reported mean closing velocity 93 mm/s, observed range 40–160 mm/s. These are descriptive measured velocities, not hard ceilings.
- Kwon et al., *J R Soc Interface* (2013), DOI 10.1098/rsif.2013.0227: 600-fps voluntary blinks in 25 adults, mean peak closing velocity 243 ± 9 mm/s and observed palpebral apertures 7.4–12.8 mm (mean 9.8 mm). Voluntary and spontaneous regimes must remain separate.
- Doane, *Am J Ophthalmol* (1980), DOI 10.1016/0002-9394(80)90058-6: spontaneous eyelid descent generally 17–20 cm/s, occasionally over 40 cm/s. These are reported measured motions, not a bounded population maximum.

## Frozen falsifiers and deliverables
1. Exact rational Python implementation, with `unittest` cases for strict equality, units, camera period, monotonicity in v/f/A/m, exposure invariance **only** for the stated equal-exposure idealization, and a 30-Hz/7.4-mm/400-mm/s zero-coverage condition for the **sufficient gate**.
2. Independently recompute at least three threshold cases in JavaScript using integer arithmetic, without importing Python.
3. Produce a machine-readable CSV grid and human-readable result report. Distinguish `GATE_POSSIBLE` from `MODEL_EXCLUDE_CONDITIONAL`: no measured camera anatomical averages or independently certified v are supplied, so **never emit a real exclusion certificate**.
4. If all rows show zero gate possibility, document that negative outcome; do not tune threshold or literature choices after seeing the grid.
5. Product decision stays `ABSTAIN_UNCALIBRATED`, release `BLOCKED`. No raw human data, personal information, or simulated human accuracy claims.

No new public dataset access attempts. The purpose is to kill physically infeasible *product claims* early, not to replace synchronized camera/photodiode measurements and blinded human review.
