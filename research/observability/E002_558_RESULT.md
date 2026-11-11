# E002-558 RESULT | Independent published-human constraint and CSP-safe acquisition repair

Date: 2026-10-31. Primary E002-371 observability kernel. Frozen protocol committed first at a4d459f. Evidence tier: **published aggregate human measurements plus an executable conditional arithmetic challenge**, not direct access to raw human sequences, not a certified hard speed bound, and not physical shutter validation.

## What changed

1. The E002-557 browser end-to-end job [41150828396](https://github.com/sushxnthd/lucent/actions/runs/41150828396) reached real Chromium, then failed because its test harness used `page.wait_for_function`, which violated the annotation page's existing CSP. The failure is an instrumentation issue, not evidence of anatomical measurement error. Commit 20f5b6d replaced these waits with native Playwright assertions, leaving the HTML, CSP, 260-frame packet and anatomical adjudicators untouched. [Replacement hosted run 41155382505](https://github.com/sushxnthd/lucent/actions/runs/41155382505) reached the video stage after the native-frame test, then **failed**: `videoWidth=0` for an H.264 MP4 loaded through a `blob:null/...` URL from the opaque `file://` origin. This is a video-decoding/secure-origin integration failure, not human evidence. Commit [a550cae](https://github.com/sushxnthd/lucent/commit/a550cae6540df5163d08aaef5a9c749ace8a6ffc) moves only the video-rater HTML to a localhost-only HTTP secure context, blocks any off-loopback requests, and emits explicit media diagnostics on failure. [Next hosted run 41155599319](https://github.com/sushxnthd/lucent/actions/runs/41155599319) was queued at this correction; **no browser pass is claimed**.
2. Independent primary human literature: Kwon et al., *Journal of the Royal Society Interface* 10 (2013), DOI [10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227). The 25-person voluntary-blink study acquired at 600 fps but measured eyelid aperture at **5-ms intervals**, not every 600-Hz frame. It reports initial palpebral apertures of **7.4-12.8 mm** and a **243 ± 9 mm/s** reported closing peak-speed point estimate (±9 is statistical uncertainty, not a camera error certificate). The source excludes one population subgroup, and the observations do not cover spontaneous/reflex blinks. It is neither a released participant-disjoint dataset nor an instrument-certified hard velocity ceiling.

## New empirical constraint, not an upper bound

If the published mean peak speed and maximum aperture are treated as accurate point estimates, at least one participant's measured peak speed is >= 243 mm/s (also true if 243 is the peak of the group mean curve). Every initial aperture is <= 12.8 mm, so the maximum observed normalized closing secant speed is at least **243/12.8 = 18.984375 s^-1**. Any claimed hard universal normalized-speed ceiling below this value conflicts with the reported observations *within this cohort*, under the point-estimate assumptions. A hard upper ceiling cannot be obtained by reversing this inequality. Between-sample motion may be faster, not slower.

The executable [e002_558_published_speed_challenge.py](e002_558_published_speed_challenge.py) reports exact rational sensitivity cases:

| Assumed downward bias in reported speed | Assumed upward bias in aperture | Necessary nominal speed ceiling (s^-1) |
|---:|---:|---:|
| 0 mm/s | 0 mm | 18.984375 |
| 0.5 mm/s | 0.05 mm | 18.871595 |
| 10 mm/s | 0.5 mm | 17.518797 |
| 50 mm/s | 1.0 mm | 13.985507 |

The latter three are **illustrative sensitivity assumptions**, not reported uncertainty bounds or confidence intervals. With unknown systematic error, no unconditional hard numerical constraint is certified. A proposed ceiling of 15/s is contradicted by the nominal and moderate-bias cases but not by the severe-bias case. A proposed ceiling of 20/s is merely *not falsified*; it is never certified safe.

A frozen instantaneous-endpoint-only 30-Hz/10-ms illustration with a=0.4 and closure threshold 0.2 gives a 23.333-ms gap and a critical speed ceiling of **120/7 ≈17.142857/s**. Thus a convenient 15/s cap would appear to exclude hidden closure while being inconsistent with the published cohort's nominal speed constraint. This illustration is **not** a camera-exposure certificate and does not establish an actual hidden closure.

Independent local exact-fraction recomputation reproduced 18.984375, 18.871595, 17.518797, 13.985507 and 120/7. [Dedicated hosted CI](https://github.com/sushxnthd/lucent/actions/runs/41155446546) was queued at report time; hosted success is not claimed.

## Falsification and next action

The primary physical blockers remain: authenticated physical shutter captures **0**, independent blinded human rater pairs **0**, independently certified continuous-time human velocity/acceleration bounds **0**, held-out physical predictions **0**. The study's published averages cannot substitute for raw participant-disjoint video, verified acquisition timing, bounded optical errors or calibrated anatomical transfer. No raw human footage or private annotations were copied to GitHub.

Next: complete the real-browser CI acquisition test, then obtain authorized high-rate video and two actual blinded human annotations; independently calibrate shutter/clock/geometry before any E002-371 excluded-gap claim. Stop inventing low physiological speed caps to make 30-Hz observations look conclusive. Product `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. Hush branch and PR untouched.
