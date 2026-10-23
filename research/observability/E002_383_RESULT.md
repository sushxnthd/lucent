# E002-383: synthetic RGB observability falsification (2026-10-23)

Pre-registered in E002_383_FROZEN.md and E002_383_SPECIFIC_PRETEST.md before testing. Scope: **synthetic instrument only; no human or real-camera validation**.

**Exact counterexample:** At 30fps, 10ms exposure, V=60 normalized aperture/s, closure threshold 0.2, and physical shutter-average aperture b=0.99, the saturating continuous V-Lipschitz trajectory has blind-gap minimum 0.1904554885. With nonlinear RGB response I(a)=C+sqrt(a)(O-C), a perfectly calibrated open/closed template extractor observes mean(sqrt(a))=0.994904743386 and falsely certifies a lower bound 0.2218059597. A constant nonclosure a=0.989835448412 yields identical two full RGB frames (5,760 pixel-channel values) in this rank-one synthetic model. The hidden threshold excursion lasts 0.318ms, **not** a sustained blink.

**Independent verification:** Closed-form ramp integration and SciPy quadrature agree to <1e-12. Separate random-template full-RGB collision check passed. A separate 500-case dense-grid verifier found maximum gap discrepancy 1.11e-16 and linear exposure quadrature error <4e-7.

**11 nuisance regimes x 1,100 seeded synthetic trials = 12,100.** Naive false certificates / naive issued: clean 0/474; bounded photometry+clock 8/560; nonlinear response 28/608; gain drift 38/682; clock underestimate 14/563; glasses glare 41/645. Gaze shift, blur, missingness, gradient, and mixed OOD had no false naive certificates in these particular selected scenarios. Domain-gated calibrated bounded photometry yielded 0 false / 457 issued; all 1,100 in-domain samples respected deterministic RGB aperture-error envelope 0.0039007043 and 1.5ms timing allowance. The 0/457 synthetic result is **not** a human error rate.

**Product consequence:** Reject two-point RGB template calibration as a physical aperture measurement. Only issue gap-specific no-hidden-closure certificates with independently validated intermediate-aperture transfer, shutter timing, physical speed, optical error, geometry, brightness, missingness, blur, gaze and eyewear. Otherwise ABSTAIN. No unconditional PERCLOS, blink count, or fatigue diagnosis.

**Novelty:** Sensor response nonlinearities and their calibration are prior art: Hanaoka et al., Applied Optics 2011, DOI 10.1364/AO.50.002401; Garcia et al., PLOS ONE 2013, DOI 10.1371/journal.pone.0079534. Human high-speed blink work: Kwon et al., J R Soc Interface 2013, DOI 10.1098/rsif.2013.0227. Publication novelty and paired human validation remain unestablished.

**Reproducibility:** Full 11-condition simulator, JSON, independent checker, calibrated product gate, tests, SVG figures and prospective human protocol in E002-383 reproducibility package. Frozen protocol and this result persist in draft PR #25.
