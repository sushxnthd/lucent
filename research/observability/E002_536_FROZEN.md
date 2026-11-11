# E002-536 FROZEN | Published eyelid kinematics cannot supply a hard aperture-speed certificate

2026-10-30. Primary E002-371 observability kernel. Existing branch `research/observability-human-boundary`, draft PR #26. Freeze before implementing the independent arithmetic challenge. **Evidence tier: primary-literature audit + exact-rational hypothetical instrument stress; not new human measurements.** Do not retune E002-534/535's rejected image-return detector.

## Primary sources and scope to audit

1. Kwon et al., *J R Soc Interface* (2013), DOI [10.1098/rsif.2013.0227](https://doi.org/10.1098/rsif.2013.0227): 25 healthy adults, voluntary blinks recorded at 600 fps; palpebral aperture measured at 5-ms steps; reported mean peak closing speed 243 +/- 9 mm/s, mean initial aperture 9.8 +/- 0.2 mm, observed aperture range 7.4-12.8 mm, and mean closed phase 58 +/- 4 ms. These are **group summaries**, not a continuous-time hard upper bound, a per-participant paired speed/diameter distribution, or a minimum closed dwell.
2. Doane, *Am J Ophthalmol* (1980), DOI [10.1016/0002-9394(80)90058-6](https://doi.org/10.1016/0002-9394(80)90058-6): unforced upper-lid descent generally 17-20 cm/s, occasionally exceeding 40 cm/s. **Upper-lid speed is not automatically the derivative of palpebral aperture**; do not substitute it as E002-371's aperture-speed ceiling.
3. Godfrey et al., *Ophthalmic Plast Reconstr Surg* (2019), DOI [10.1097/IOP.0000000000001356](https://doi.org/10.1097/IOP.0000000000001356): 10 subjects, spontaneous blinking at nominal 240 fps smartphone video, mean closure velocity 93 mm/s (SD 31, subject range 40-160). Supports low-cost anatomical *pilot feasibility*, not authenticated shutter/clock, hard velocity or an independent holdout.
4. Wambier et al., *Ophthalmic Plast Reconstr Surg* (2014), DOI [10.1097/IOP.0000000000000031](https://doi.org/10.1097/IOP.0000000000000031): 21 adults, simultaneous high-speed video and magnetic search coil, mean maximum-velocity difference 5.0 +/- 3.4 mm/s. Prior art for video-based kinematics validation; Lucent must not claim video eyelid measurement itself is novel.
5. Sforza et al., *Ophthalmic Physiol Opt* (2008), DOI [10.1111/j.1475-1313.2008.00577.x](https://doi.org/10.1111/j.1475-1313.2008.00577.x): observed age/sex dependence and incomplete spontaneous blinks; no universal upper bound established.

## Frozen exact stress prediction

Re-use E002-371's conditional scalar ratio `R = V*(T-e)/(2*(b-c))` for **global-shutter, point-endpoint, zero-clock-error** hypothetical conditions. Let `b=1`, `c=1/5`, exposure `e=1/1000 s`. Use the *ratio of two Kwon cohort means* `V=(243 mm/s)/(9.8 mm)=1215/49 s^-1` solely as an illustrative representative parameter; **it is not the mean of participant-normalized speeds, a paired observation, a certified upper bound or a biological prior for release**. With `T=1/30 s`, predict exact `R=7857/15680 < 1`; with `T=1/15 s`, predict `R=15957/15680 > 1`. A calculation failing these exact fractions falsifies the arithmetic experiment. The threshold frame rate is `1/(e+2*(b-c)/V)`, about 15.26 fps. No source paper measured these hypothetical shutters.

## Product evidence gate and adversarial controls

An executable gate must **reject** hard hidden-closure exclusion whenever velocity evidence is a cohort mean, sampled maximum, upper-lid-only speed, unpaired denominator, missing anatomy, or unauthenticated shutter/clock. Even if `R<1`, these inputs may be reported only as `ILLUSTRATIVE_NOT_CERTIFIED`. Also reject zero/negative aperture scale, negative gap, dimension mismatch and any attempt to promote mean closed-phase duration to a minimum guaranteed dwell. A positive-control *hypothetical* fully attested envelope may output `CONDITIONAL_BOUND_ONLY`, never `PHYSICAL_VALIDATED`, because this test contains no physical inputs. Keep exact-rational arithmetic and a separate independent implementation for numeric replay.

## Stop/next experiment

Do not spend another run refining literature-derived numerical speed constants. The substantive implication is that **no published cohort summary supplies the hard, continuous-time, participant/session-specific aperture-velocity envelope E002-371 requires**. Use a low-cost 240-fps smartphone only as a pilot anatomy instrument; photodiode-timed exposure/clock validation and two independent blinded native-frame raters are still mandatory. Publish no participant images. Product `ABSTAIN_UNCALIBRATED`; production `BLOCKED`. Hush branch and PR #45 untouched.
