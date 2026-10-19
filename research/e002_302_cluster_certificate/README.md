# E002-302: participant-level sign certificates (2026-10-19)

Status: mathematical and synthetic only. NO ordinary-RGB / dedicated-eye-tracker human observations evaluated. Not an app.

Active question: can the sign of a within-person 0.5-s pupil diameter change be certified from an RGB pupil/iris ratio with prospectively calibrated nuisance variation?

Signal: native RGB conic pupil/iris ratio z(t). Reference: independent synchronized eye tracker pupil diameter D(t). The generative camera equation is I_n=Gamma_n{T_n^-1 integral h_{n,t} * L(q,H,eyelid,kappa,lighting,glasses) dt}+noise, with rolling-shutter timing. Its *conditional* scalar reduction is S=log(z1/z0)=R+E, R=log(D1/D0), E=all residual optical/photometric/segmentation/clock confounds.

Sharp deterministic partial-identification: if |E|<=d, R lies in [S-d,S+d]. Positive change is certified iff S>d, negative iff S<-d. At |S|<=d, R=0,E=S is an exact observationally equivalent no-change explanation. If z=kappa*q*exp(e), d can be bounded by |log(kappa1/kappa0)|+|e0|+|e1|, only with INDEPENDENT nuisance calibration.

Participant-level split conformal: calibrate R_i=max_pairs |S-R| on each participant. For n exchangeable calibration participants, k=ceil((n+1)(1-alpha)), threshold the k-th smallest R_i (infinity if k>n). With probability >=1-alpha, every sign certificate on one new exchangeable participant is correct. This is unconditional simultaneous coverage, NOT conditional accuracy among certified pairs, and DOES NOT transfer to uncalibrated devices/lighting/glasses. n>=19 for a finite 95% threshold. Established split-conformal methodology, NOT novel.

Synthetic fixture: 51 artificial participants, 31 calibration, 20 holdout; d=0.030799668548334713 log units. Supported device-A holdout: 77/112 pairs certified, 0 false certificates among 7 participants. Unseen device-B negative control: naive reuse causes 66 false certificates/208 pairs among 13 participants; proper system ABSTAINS on all OOD pairs. These are synthetic counts, not human evidence.

10-Hz temporal impossibility: with 16.7-ms rectangular exposures, 2-Hz and amplitude-scaled 8-Hz sinusoids give identical 10-Hz exposure-integrated samples. The sharp ideal Nyquist requirement is fs>2B for bandwidth B (and exposure transfer has no zeros in band). This is classical sampling theory.

Mandatory controls: geometry-only, brightness-only, missingness-only, temporal-smoothness-only. Untouched participant and device holdout; reject leakage and post-hoc threshold tuning. Native timestamp/clock gates mandatory.

Publication threshold: paired human reference with independently audited timestamps; prospective threshold crossing; strong nuisance controls; independent checker; priority audit; reproducible results and an explicit product decision. No field-level breakthrough yet.

Product: REJECT uncalibrated pupil waveform, absolute diameter, PERCLOS-from-average-aperture, five-second fatigue inference. INVESTIGATE only sign-of-change with condition-specific calibration and abstention.

Prior art: EyeDentify (Shah et al., WACV 2025), https://www.dfki.de/en/web/research/projects-and-publications/publication/15080 ; RGBE-Gaze (Zhao et al., TPAMI 2025), https://doi.org/10.1109/TPAMI.2024.3474858 ; Hayes & Petrov (2016) pupil foreshortening, https://trhayes.org/publication/hayespetrov16a/ ; Wang et al. (2019) projective pupil/iris, https://arxiv.org/abs/1902.04541 ; Jung et al. (2023) conformal multivalidity, https://arxiv.org/abs/2209.15145 .
