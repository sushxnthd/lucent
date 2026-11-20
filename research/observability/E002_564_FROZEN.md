# E002-564 FROZEN | Cohort-ratio lower bound challenges optimistic human eyelid-speed ceilings

Frozen 2026-10-31 before arithmetic implementation. Primary E002-371 kernel, persistent branch `research/observability-human-boundary`, draft PR #26. **This is a primary-literature physiological challenge, not a human raw-data experiment, validated universal upper bound, or a camera certificate.**

## Prior sources and exact precommitted inputs

- Kwon et al., *J R Soc Interface* 2013, DOI 10.1098/rsif.2013.0227: 25 volunteers; mean peak eyelid closing speed 243 mm/s; mean initial palpebral aperture 9.83 mm (Table 1). Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/ . Previous E002-558 used the conservative cross-person maximum aperture 12.8 mm and obtained 18.984375/s.
- Sun et al., *Invest Ophthalmol Vis Sci* 1997, PMID 9008634: electromagnetic search-coil blink study. The Kwon 2013 Table 1 secondary transcription reports, for its 40-49-year subgroup of 8 participants, mean closing peak speed 427 mm/s and mean closing amplitude 11.7 mm; additional subgroups 50-59 (329,10.2) and 60-69 (349,10.6). The primary Sun abstract independently confirms method and age stratification but not these exact tabulated numbers. Thus the 1997 numeric ratios are **secondary-table-transcribed pending primary full-text verification**. Do not claim direct primary numerical verification.

## Mathematical target and locked predictions

For the same cohort of n participants with positive individual aperture a_i and nonnegative peak speed v_i, the inequality max_i(v_i/a_i) >= (sum_i v_i)/(sum_i a_i) follows by summing v_i <= M a_i. No assumption that the person with maximum v has maximum a. The ratio of published group means is a **lower bound on at least one measured individual normalized peak**, conditional on paired cohorts and comparable anatomical definitions; it is NOT an upper bound for any participant, a population quantile, or a continuous-time physiological speed ceiling.

Predictions using exact decimal inputs: 2013 at least 243/9.83 = 24300/983 per second (about 24.72/s), strictly stronger than E002-558's 243/12.8 = 18.984375/s. 1997 40-49 at least 427/11.7 = 4270/117 per second (about 36.50/s), other subgroups 329/10.2 and 349/10.6. Treat the 1997 ratios as **conditional secondary-source values**.

Adversarial controls: unequal aperture/velocity pairing, all-equal ratios (sharpness), positive aperture requirement, cohort mismatch rejection, and illustrative ±10% adverse *systematic* biases (0.9 speed, 1.1 aperture), never interpreting reported standard errors/deviations as deterministic uncertainty limits. Use independent Python Fraction and Node BigInt exact arithmetic.

## Product decision

Any proposed universal human normalized speed ceiling below a verified observed cohort-ratio lower bound is incompatible with the conditional published measurements. Never substitute these lower bounds as safe upper ceilings; absent an independently certified upper bound, shutter response, timebase, and anatomy, remain `ABSTAIN_UNCALIBRATED`, production `BLOCKED`. No new physical/human ratings or deployment claims.
