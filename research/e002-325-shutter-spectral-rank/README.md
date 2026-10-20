# E002-325: shutter-spectral rank and stability boundary

Conditional finite-bandwidth theorem: after independently validated geometry/photometry normalization, M distinct exposure-integrated RGB scalar samples of a T-periodic K-bandlimited ocular waveform identify all 2K+1 real Fourier degrees of freedom iff M>=2K+1 and every included shutter response is nonzero. Stability is governed by sigma_min(A); worst-direction Delta changes are guaranteed distinguishable under independent l2 noise eta iff Delta*sigma_min(A)>2*eta.

Independent local checker passed. At 10 fps and 10 ms exposure, native 4-Hz and -6-Hz smooth trajectories with different true time courses produce the same RGB scalar exposure means (max difference 4.44e-16). At 30 fps, K=6, 13 distinct retained frames have full rank, but spaced vs clustered masks differ in sigma_min by 460,572-fold. Same sample count does not mean same reliability.

Status: exact conditional instrument law, classical sampling prior art, no human validation, no ocular-specific novelty. Product: research-only interval-valued shutter-mean eyelid occupancy with abstention; reject uncalibrated rapid pupil waveform/blink timing and five-second fatigue certification.

Full locally executed checker and reproducibility archive: lucent_e002_325_spectral_boundary.zip (attached in automation run).