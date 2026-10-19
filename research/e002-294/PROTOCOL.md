# Frozen E002-294 kernel

1. **Signal/reference:** RGB geometry-normalized eyelid openness/closure feature vs synchronized high-speed anatomical eyelid reference.
2. **Literature frontier:** Kwon 2013 blink kinematics, Toda 2014 low-FPS detection, Navascues-Cornago 2026 downsampling, Culemann 2026 gaze confounding, Micchelli et al. 1976 optimal recovery.
3. **Metric:** sharp worst-case undetectable closure dose U/P and hidden peak ceiling; prospective human coverage and false-certification rates.
4. **Worst nuisance:** camera photometric transfer, eye gaze and glasses may change apparent eyelid features independently of anatomy.
5. **Forward model:** full RGB I_n=Q_gamma(T^-1 integral K_sigma*R(c,gaze,pose,illumination,glasses)dt)+noise. Reduced scalar y_n=T^-1 integral c(t)^p dt+e_n, |e|<=eta, |c'|<=V.
6. **Falsification:** independent calibration of p,V,eta,T,G on design subjects, then an untouched human participant/device/lighting regime with hidden closure dose exceeding U while every observed feature remains compatible with open-eye null.
7. **Boundary prediction:** quadratic response and 10-Hz retained-exposure sampling increase hidden-dose ceiling. Frozen synthetic 24-FPS prediction in HOLDOUT_FREEZE.json.
8. **Untouched human:** high-speed eye-reference synchronized to ordinary-RGB, participant/device/lighting/glasses holdouts, calibrated exposure and independent clock check; not yet feasible with verified accessible paired recordings.
9. **Publication gate:** complete primary prior-art audit, independent proof/checker, prospective held-out human coverage, predeclared effect margin, negative controls, reproducibility and independent calibration. Synthetic theorem alone insufficient.
10. **Product:** reject uncalibrated blink absence/fatigue; consider conditional missed-closure upper-bound with abstention after human validation.

**Negative controls:** geometry-only; brightness-only; missingness-only; temporal-smoothness-only. Predeclare extraction and holdout before outcomes. No raw face video committed.

**Access attempts:** EyeDentify Kaggle API DNS failed; Kaggle downloader failed. Two attempts, path abandoned for this run. No user laptop or paid compute.