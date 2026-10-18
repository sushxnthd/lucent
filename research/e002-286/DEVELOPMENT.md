# E002-286 development outcomes (01-08; before holdout)
Source: marcus-nystrom/BlinkDetector, Tobii Spectrum 600-Hz Center.tsv, public Git blobs listed in PROVENANCE.
Frozen 55% eye-openness threshold, 7-point median, 30-600 ms, strict valid-neighbor gate.
Subject counts: 01=34, 02=0, 03=31, 04=1, 05=38, 06=0, 07=42, 08=1. Zero-event subjects are retained as negative/coverage failures, not silently dropped.
At 10Hz ideal point sampling, mean phase detection: 01=.89269, 03=.77092, 05=.59025, 07=.68862; 04=1.0, 08=.36719. Max per-event discrepancy from min(1,d/P): .006773, below predeclared .04 tolerance. At 30Hz all but subject 05 show 1.0; subject 05=.99877. These results are conditional on an idealized thresholded 600-Hz reference, not real RGB.
Near-universal pupil-validity loss inside accepted reference closure events observed on many subjects, but this is NOT proof that pupil missingness is a sufficient blink detector. A separate false-positive test is needed.
Predeclared unseen holdout remains 09-12, with 10Hz phase-detection prediction min(1,d/100ms), and 30Hz min(1,d/33.333ms). No threshold tuning permitted.
