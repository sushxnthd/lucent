# Frozen E002-327 protocol (prior to human outcomes)
1. Signal/reference: ordinary RGB shutter-integrated pupil/iris log-ratio feature vs native-timestamped independent eye-reference pupil/iris ratio; secondary RGB eyelid closure vs high-speed/manual event labels.
2. Frontier: Hayes & Petrov 2016 gaze foreshortening; Aguirre 2019 corneal entrance-pupil model; Daza et al. 2024 RGB/NIR/EEG mEBAL2; Fogelton & Benesova RGB blink baselines; classical partial identification.
3. Metric: exact alpha interval, sign-certification rate, reference coverage and abstention; participant/device stratification.
4. Strongest confound: gaze or stimulus-locked ISP effect with same temporal signature as pupil response.
5. Generative model: y=alpha*h+N*beta+e as local surrogate to exposure-integrated full-image physics; all bounds externally calibrated.
6. Falsification: any held-out reference alpha outside claimed interval, or sign certificate contradicted by reference.
7. Frozen synthetic boundary Bcrit=.05, B=.04 positive, B=.055 abstain. No unseen human prediction yet: must freeze after independent calibration and before holdout.
8. Human test: split participants and devices; strata lighting/gaze/glasses; holdout untouched. Controls: geometry-only, brightness-only, missingness-only, temporal smoothness-only. Avoid black-box primary endpoint.
9. Publication gate: independent residual calibration and >95% held-out reference interval coverage in every prespecified stratum, prospective unseen boundary crossing, independent replication, novelty audit; report uncertainty and failures.
10. Product: reject rapid pupil waveform and five-second fatigue certification until gate passes; research-only interval measurements with abstention.
Acceleration: two blocked dataset routes this run (Eyeblink8 ZIP download, mEBAL2 credentialed access); do not repeat access archaeology. RGBE-Gaze remains unevaluated.
