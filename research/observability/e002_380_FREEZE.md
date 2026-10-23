# E002-380: rolling-shutter phase diversity, frozen before evaluation
2026-10-23. Synthetic/instrument test only. Human validation not performed.

Active question: Can calibrated rolling-shutter row offsets guarantee detection of a closure invisible to global shutter, and what happens when valid eye rows are lost?

Signal/reference: row-resolved RGB contrast vs known synthetic binary closed plateau q(t); future human reference must be concurrent high-speed camera with native timestamps.

Model: exposure E[n,j]=[nF+delta_j,nF+delta_j+w]. RGB y[n,j]=b_j-c_j*(1/w)*integral_E q(t)dt+eta[n,j], with |eta|<=epsilon. Unknown or time-varying b_j, c_j, blur, occlusion, gaze, glasses or row timing outside calibration force abstention. Define a row as qualified only when its effective contrast and error envelope are independently calibrated.

Observable: existence of a row/frame whose exposure overlaps closure by at least m. For fixed contrast c and error epsilon, distinguishability of a binary closure from open requires c*m/w>2epsilon (strict); equality is nonidentifiable. Camera qualification and actual RGB event classification are distinct.

Exact predicted boundary: Let L=D+w-2m and G be maximum cyclic gap among qualified row offsets modulo F. For D>=m and 0<m<=min(D,w), every closure phase has some overlap >=m iff L>=G. For positive strict optical separation use c*m/w>2epsilon. At equality of phase coverage the overlap criterion is attained but not with positive slack.

Frozen unseen tests: F=1/30s, w=10ms, offsets [0,5,10,15,20]ms. All 5 rows: G=13.333333ms; center 3 [5,10,15]ms: G=23.333333ms; one row G=33.333333ms.
Full exposure m=10ms: critical D 23.3333ms (all), 33.3333ms (center), 43.3333ms (one). At D=24ms, all PASS, center FAIL.
Partial overlap m=4ms: critical D 11.3333ms (all), 21.3333ms (center), 31.3333ms (one). At D=15ms, all PASS, center FAIL.
Narrow ROI offset span <=1ms: G>=32.3333ms, partial overlap critical D>=30.3333ms; D=15ms FAIL.

Decisive falsification: independent exact brute-force shutter-overlap evaluation must agree on PASS/FAIL and return a failing phase for each FAIL. Test random row offsets, invalid rows, noise, photometric drift and timing uncertainty; never interpret a pass on synthetic data as human validation.

Untouched human study: synchronized native >=240fps eye-reference and 30/60fps RGB rolling/global shutter; hardware clock anchors; measure row timings and exposure, independently qualify rows and error; freeze device and participant splits, onset/duration reference labels and all thresholds; predict held-out boundary crossings before opening outcomes; compare against geometry-only, brightness-only, missingness-only and smoothness-only controls.

Prior art: rolling shutter, temporal sampling, phase coverage and bounded-error separation are established. No novelty claim. Product: only calibrated row-aware camera qualification with explicit abstention; no unconditional PERCLOS, rapid pupil waveform or fatigue diagnosis.