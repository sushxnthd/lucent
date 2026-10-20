# E002-320: shutter-duty observability (2026-10-20)

**Status:** exact restricted theory + independent synthetic checks; no synchronized human RGB/reference validation and no publication-level novelty claim.

**Question:** can ordinary RGB certify a rapid anatomical eyelid-closure plateau when the camera exposes for only a fraction of each frame period?

**Exact signal/reference pair:** a calibrated RGB shutter-mean normalized eyelid-closure proxy versus synchronized high-speed anatomical closure. The camera's true shutter starts/ends and a deterministic proxy error envelope must be independently verified.

**Measurement model:** raw RGB image I_i(x)=b_i(x)+(g_i/E_i)∫_{W_i}[K_i*R(x;c(t),pupil(t),gaze(t),illumination(t),glasses(t))]dt+ξ_i(x). Only when independently calibrated may this be reduced to y_i=(1/E)∫_{iP}^{iP+E}c(t)dt+e_i with |e_i|≤η.

**Observability metric:** worst-phase null-versus-closure bounded-noise distinguishability; sharp window-mean closure and raw threshold-occupancy intervals.

**Sharp boundary:** for a rectangular plateau of amplitude a and duration d≤P, global-shutter period P, exposure E, gap G=P−E, guaranteed detection iff a(d−G)_+/(2E)>2η. If η/a<1/4, critical duration dcrit=G+4ηE/a, with strict inequality. Generic smooth blinks are NOT covered.

**Hypothetical η/a=0.10:** 30fps/16.667ms exposure dcrit=23.333ms; 30fps/10ms dcrit=27.333ms; 10fps/10ms dcrit=94ms. These are not measured webcam values.

**Sharp missingness result:** with 30fps/10ms exposures, 70% of time is unobserved. Even perfect zero closure during all exposures allows true mean closure and raw threshold occupancy anywhere in [0,0.70] absent physiological regularity. This is a worst-case bound, not a claim about actual humans.

**Unseen synthetic prediction:** at 24fps, 12.5ms exposure and η/a=.07, dcrit=32.6667ms; 31ms abstains, 35ms certifies. Independently reproduced. This is NOT an untouched human test.

**Product:** calibrated interval-valued shutter-mean closure only, with abstention. Reject generic blink timing/count, uncalibrated PERCLOS, rapid pupil waveforms and five-second fatigue diagnosis.

See THEOREM.md, PROTOCOL.md, HUMAN_PROTOCOL.md, PRIOR_ART.md, FAILED_GATES.md and code. The complete independently executed archive is also available from the ChatGPT E002-320 run.