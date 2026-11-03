# E002-636 | Closure-threshold uncertainty enforcement (2026-11-03 UTC)

## Scientific trigger
E002-635 constructed a synthetic false exclusion when a nominal zero-mm closure threshold was substituted for a possible 1.5-mm anatomical closure threshold. The prior scorer accepted a point estimate `closure_mm`, so its apparent exclusion did not survive this nuisance.

## Enforcement change
The research-only E002-632 scorer now requires `closure_hi_mm`, interpreted as an independently certified *upper* bound on the anatomical closure threshold, not a point estimate. It computes strict reachability using conservative endpoint lower apertures and that upper bound. Missing upper bound abstains. Existing calibration YES flags remain unauthenticated and are **not** release evidence. Legacy CSV files with only `closure_mm` fail required-header checks rather than silently receiving a nominal zero.

## Frozen adversarial checks
At endpoint apertures 2 mm, gap 20 ms, closing/opening ceilings 100 mm/s, closure_hi_mm=0 yields EXCLUDE (40 ms needed); closure_hi_mm=1.5 mm yields ABSTAIN_REACHABLE (10 ms needed). Missing bound abstains. These are synthetic model checks, not human physiology. The updated scorer includes three regression assertions; hosted execution remains unverified.

## Remaining blockers
No independently authenticated anatomical threshold interval, continuous-time human velocity ceiling, camera shutter timing, synchronized physical recording, blinded human reference labels or held-out physical prediction. Any point estimate substituted for `closure_hi_mm` invalidates the decision. Production remains BLOCKED and product must ABSTAIN_UNCALIBRATED. Next eligible scientific work is physical acquisition, not further threshold polishing.
