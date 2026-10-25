# E002-438 — frozen human-aggregate speed-cap falsification and paired-sample witness

**Frozen 2026-10-25 before implementation.** Parent E002-371; preserve research/observability-human-boundary and draft PR #26. Evidence planned: independent **published human** speed aggregate, analytic necessary-speed inequality, independent linear-trajectory oracle, nuisance fail-closed instrument. This is not new human data, a physiological universal speed bound, or a physical no-closure validation.

## New falsifiable question

Do previously used illustrative speed caps such as 120 mm/s survive comparison with **published high-speed human eyelid peak closing velocities**, and can a future calibrated human reference reject a candidate cap without estimating acceleration or inventing an upper speed bound?

Kwon et al., *J R Soc Interface* 2013, DOI 10.1098/rsif.2013.0227, recorded voluntary blinks from 25 participants at 600 fps, manually measuring aperture every 5 ms, and reported mean peak closing speed **243 ± 9 mm/s**. The ±9 is not a deterministic measurement-error bound and must not be used as one. Assuming the reported mean is the arithmetic mean of individual measured peaks and rounded to the nearest integer, at least one measured peak is >= 242.5 mm/s. Therefore an illustrative 120 mm/s universal hard cap is **incompatible with the published measured peak statistics**, under metric/measurement comparability. A 300 mm/s cap is merely **not falsified by that aggregate**, never validated.

A separate 2026 study (DOI 10.1080/08164622.2026.2619492, 11 participants) reports a **177.7 mm/s reflex-minus-spontaneous closing-velocity difference** (95% CI 102.2 to 253.1), reinforcing blink-type stratification. It uses a distinct metric and cohort and **must not be added to the 2013 mean**. Navascues-Cornago et al. 2026, DOI 10.1016/j.jtos.2026.01.003, 500-fps recordings of 20 spontaneous and 10 reflex participants, found maximum velocity underestimated below 250 fps. Neither study supplies a hard physiological cap.

For two independently calibrated human reference samples with measured apertures y0,y1, bounded absolute errors eps each, nominal time separation h and per-sample clock error delta, the mean-value inequality gives a **necessary** speed lower bound:

sup |x'(t)| >= max(0, |y1-y0|-2eps)/(h+2delta).

This can falsify a proposed cap V if the lower bound exceeds V. It can **never** certify that V is an upper bound. Unauthenticated scale/timing, any unresolved geometry, brightness, missingness, blur, gaze, glasses, sampling, clock, occlusion or shutter nuisance must abstain.

## Prespecified tests

1. Published 243-mm/s cohort mean rejects 120 mm/s as a comparable universal cap; 300 mm/s is *not falsified* rather than accepted; metric mismatch is unresolved.
2. At equal measured endpoints 6.0 mm, closure threshold 2.0 mm and **hypothetical** V=243 mm/s, the sharp symmetric Lipschitz lower scenario is 1.95 mm at 30 Hz and 3.975 mm at 60 Hz. These are scenario calculations, **not** physical certification. Increasing bounded aperture or clock error cannot improve the lower bound.
3. A separately coded linear oracle x(t)=2+250t over 5 ms, with endpoint errors +0.01/-0.01 mm, produces observed difference 1.23 mm and necessary lower bound 242 mm/s. A 240-mm/s candidate is rejected conditionally.
4. All ten nuisance flags, absent physical scale or sensor timing attestation, malformed records, nonfinite numbers, metric mismatch, or ambiguous timestamp order fail closed. No output authorizes physical no-closure, blink duration, PERCLOS or fatigue.
5. Publish reproducible standard-library implementation, independent tests, machine-readable scenario results and a candid primary-literature interpretation. Do not claim held-out human trace validation.

## Scientific consequence

The E002-371 bound remains mathematically conditional. Its physiological velocity premise is the bottleneck: finite-sample peaks and cohort means can **reject** caps, not **certify** universal caps. Keep ABSTAIN_UNCALIBRATED for physical product claims. Prospective human study must freeze candidate caps and independent physical calibration, include spontaneous/reflex strata, and use participant-disjoint, blinded high-rate reference intervals.
