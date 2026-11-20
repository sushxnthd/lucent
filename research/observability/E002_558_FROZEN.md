# E002-558 FROZEN | Repair real-browser acquisition, then independently challenge velocity assumptions

Date: 2026-10-31. Existing E002-371 kernel; same branch and draft PR #26. Freeze before changing the browser harness. No human media or optical measurements acquired.

## Decisive acquisition obstacle

E002-557 hosted run 41150828396 failed at the first post-load wait because Chromium's document CSP forbids Playwright `page.wait_for_function` string evaluation (`script-src 'unsafe-inline'` without `unsafe-eval`). This is a test-harness failure, **not** a demonstrated rater UI failure. Preserve that exact failure and change only the waiting mechanism; never weaken the HTML CSP or bypass it using browser launch flags.

## Locked browser challenge

Replace all CSP-incompatible `wait_for_function` calls with native Playwright locator assertions, property checks and/or fixed bounded polling of DOM properties. Do not alter frozen E002-492/497 and E002-555 rater HTML, original S01 packet, x=160 rule, 260-frame completion requirement, or adjudicator. On hosted Chromium, require two independent contexts, 260/260 POOR_GEOMETRY abstentions each, synthetic MP4 hash verification, two landmarks, private JSON downloads, zero HTTP(S) requests, and unchanged adjudicator returning no human physical validation. If it fails, record the exact failure and repair only the minimum acquisition defect. No synthetic media artifacts uploaded.

## Independent human literature challenge (secondary within primary)

Kwon et al., J. R. Soc. Interface (2013), DOI 10.1098/rsif.2013.0227, report 25 volunteers, Phantom video recorded at 600 fps, central eyelid aperture sampled every 5 ms, a mean reported closing peak speed 243 mm/s and initial apertures 7.4-12.8 mm. Freeze the following conditional arithmetic **before** implementing it: if reported individual peak finite-difference speeds are accurate, at least one study participant has observed closing speed >= the cohort mean 243 mm/s. Since each study aperture <=12.8 mm, the corresponding normalized finite-difference speed is >=243/12.8 = 18.984375 s^-1. Any proposed hard universal continuous-time normalized speed ceiling <18.984375 s^-1 is incompatible with these published point estimates for the studied voluntary-blink cohort. This is a **lower bound on a valid ceiling**, not a certified ceiling or validation of E002-371. Measurement error, rounding, group restrictions, different blink behaviors and missing individual records prevent an unconditional hard inference. The published ±9 is a reported standard error, not a metrological error budget. Never use mean peak speed as an upper bound or the 600-fps nominal rate as a continuous-time certificate.

## Outcome and release

Success means browser-acquisition usability plus an independently sourced empirical *constraint* on optimistic physiological assumptions, not physical validation. Keep human independent rater pairs=0, authenticated shutter captures=0, certified hard human motion ceilings=0, held-out physical predictions=0. Lucent ABSTAIN_UNCALIBRATED, production BLOCKED. Hush branch untouched.
