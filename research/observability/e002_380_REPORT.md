# E002-380 — synthetic rolling-shutter observability

Status: exact conditional instrument boundary. Not tested on people.

For frame period F, row exposure w, event duration D and required overlap m, each calibrated row contributes a circular phase arc of length L=D+w-2m. If the largest cyclic gap between qualified row offsets is G, all-phase coverage holds exactly when L>=G. A missing interval exists if L<G. Bounded-error optical discrimination separately requires c*m/w>2epsilon.

Frozen at 30fps, w=10ms, offsets 0/5/10/15/20ms: five-row G=13.333ms; center-three G=23.333ms; one-row G=33.333ms. A 15ms closure with 4ms overlap is guaranteed for all five, not center three. A 24ms closure with 10ms overlap is likewise guaranteed for all five, not center three. Exact oracle passed 3000 randomized cases.

Synthetic RGB phase sweep (5000 phases): five-row 100%; center-three 81.02%; 1ms eye-region row span 54.02%; 2ms adversarial timing offsets 99.02%. No human success rate is inferred.

Unknown local illumination can mimic a closure exactly. Uncalibrated gaze, blur, glasses, missing rows and timing error require abstention. A velocity bound V and complete threshold excursion depth delta imply a minimum below-threshold duration 2delta/V, but this cannot be presumed for unseen people.

Prior work: Meingast et al. (2005) rolling shutter; Raskar et al. (2006) coded exposure; shuffled rolling shutter temporal imaging (2022); Kwon et al. (2013) high-speed human eyelid kinematics. Publication novelty unestablished. Product scope: calibrated camera qualification only, not physiological reconstruction.
