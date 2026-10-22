# E002-371: speed-limited shutter-gap observability

Conditional theorem: for eyelid aperture a(t) with |a'|<=V, known gap endpoint apertures a0,a1, threshold theta and gap H, the maximum threshold-closed duration equals max(0,H-((a0-theta)_+ +(a1-theta)_+)/V). The minimum equals min(H,((theta-a0)_+ +(theta-a1)_+)/V). Both are sharp.

Exact synthetic counterexample: 30 fps, 10 ms exposure, threshold 0.2, V=100/s: 7.333 ms of closure is completely invisible; at V=50/s threshold closure cannot occur in the same gap with fully open endpoints. Critical speed 480/7 per second.

Independent local checker: 13,323 checks passed. Human paired data: NOT RUN. Publication novelty: NOT ESTABLISHED. Product: abstain on uncalibrated blink count, PERCLOS, and fatigue inference.
