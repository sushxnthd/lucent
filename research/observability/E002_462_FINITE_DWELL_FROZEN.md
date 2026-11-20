# E002-462 supplemental frozen challenge: finite subthreshold dwell

**2026-10-26. Frozen after the point-contact E002-462 analysis, before implementing this separate nondegenerate sensitivity test.** The primary E002-462 protocol and its results are unchanged. This is a prospectively specified *supplement*, not a preregistered primary outcome.

To remove the point-contact degeneracy, test a trapezoidal trajectory with a real interval below closure threshold c=2.0 mm. It descends from b to a_min<c at hypothetical closing cap C=567.103928 mm/s, dwells at a_min for d milliseconds, and reopens at hypothetical cap O=274.616337 mm/s. The constant-open negative control has a(t)=b. Ideal centered 0.30-ms linear shutters are at integer reference-frame times; all other assumptions match E002-462.

Frozen test A: 400 fps, b=2.30 mm, a_min=1.95 mm, d=0.10 ms, plateau begins at tau=0.90 ms. Prediction: the entire excursion is in the shutter-dark gap (0.15,2.35) ms, so all shutter observations are *exactly* identical to constant-open control despite a nonzero interval below 2.0 mm.

Frozen test B: 1000 fps, b=2.10 mm, a_min=1.98 mm, d=0.03 ms, plateau begins at tau=0.38 ms. Prediction: entire excursion fits inside (0.15,0.85) ms and is invisible to every ideal shutter, despite finite subthreshold duration.

Compute excursion support and below-threshold duration exactly; independently check in JS without importing Python. If either frozen prediction fails, preserve the failure. Report this as a synthetic reference-identifiability counterexample, **not** a human blink or physical camera validation. Reference validation must use a continuous ground-truth instrument, exposure-aware interval censoring, or explicitly bounded false-negative uncertainty. Do not change production claim gates, S21/S22, or Hush.
