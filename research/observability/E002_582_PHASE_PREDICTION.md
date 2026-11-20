# E002-582 | Pre-source exact 100-to-30 phase prediction (index-only)

**Date:** 2026-11-01. This prediction was calculated after [E002_582_FROZEN.md](E002_582_FROZEN.md) was committed and **before the external Silesian5 annotation archive was accessed**. It does not change the frozen source eligibility, positive-only outcome, phase schedule or nuisance abstentions. It is a prediction for human-labeled FC-run *index omission*, not an eyelid-velocity or physical-shutter theorem.

## Exact phase law

For the frozen nominal 100-to-30 index sampler `r(k)=phi+floor(10k/3)`, integer `phi=0,...,9`, the selected native-frame residues in each complete 10-frame period are `{phi, phi+3, phi+6} mod 10`. Therefore a positive FC run of **L consecutive native frames**, sufficiently interior to the sequence, is omitted in **exactly** the following number of ten prespecified phases:

| Human FC-positive run length L (native frames) | Phases omitting the run | Fraction of ten phases |
| ---: | ---: | ---: |
| 1 | 7 | 0.70 |
| 2 | 4 | 0.40 |
| 3 | 1 | 0.10 |
| >=4 | 0 | 0.00 |

**Proof:** For a run of length 1, each of the three selected residues yields one covering phase, leaving seven. For length 2, each of the two successive residues has three distinct covering phases, leaving four. For length 3, the nine covering phases remain distinct, leaving one. Every block of four consecutive residues contains at least one selected residue for every phase, because the largest selected-index gap is four native frames. Longer runs inherit coverage. This counts index membership only; an exposure-integrating 30-fps camera is a different measurement.

**Independent exact-integer enumeration:** A Python standard-library enumeration over all ten event start residues, all ten phases, and run lengths L=1,...,7 yielded omitted/total pairs **70/100, 40/100, 10/100, 0/100, 0/100, 0/100, 0/100** respectively. Every fixed event start residue independently yielded 7,4,1,0 missed phases for L=1,2,3,4. These are synthetic arithmetic checks, not human data.

**Boundary caveat:** Runs near the first/last sampled frame may violate the periodic interior formula because `k>=0` and recording termination truncate the sampling schedule. The actual source analysis must use the frozen explicit index schedule, not silently impose the interior formula; report boundary exceptions separately. Source missing frames or nuisance abstentions remain exclusions, never assumed negative labels.

## Pre-data falsifiers and consequence

On eligible authentic per-frame FC runs, check whether the observed phase omission count agrees with 7/4/1/0 **for interior runs**. Any mismatch is a software/source-index integrity failure and must stop the human-label analysis. Report the empirical run-length histogram without modifying the prediction. A positive omitted FC run is a valid source-annotated native-index alias witness; a negative count is not evidence of absence of continuous-time closure.

The frozen secondary quantity `runs missed in every phase` is **structurally zero** for any nonempty FC run sufficiently interior to the sequence when all ten shifts are enumerated; it cannot be used as an empirical test of the physiology. This limitation is recorded before source access rather than hidden after results.

The source's `FC=C` means investigator-annotated 90%-100% closure, not a calibrated iris-normalized aperture threshold. Neither this phase law nor an authentic positive source label can justify Lucent blink duration, PERCLOS, fatigue, hidden-closure exclusion, or velocity claims. `ABSTAIN_UNCALIBRATED`; production `BLOCKED`.
