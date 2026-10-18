# E002-286: Blink-event count information ceiling

Question: Can a five-second RGB-derived blink count distinguish two event intensities?

Signal/reference: RGB blink event times against independent synchronized eye-reference blink events. Observability metric: optimal equal-prior accuracy from event counts.

Model: true events are a homogeneous Poisson process with rate lambda. Each event is detected independently with probability p, and false events form an independent Poisson process of rate nu. Observed rate is rho=p*lambda+nu. Camera exposure, gaze, eyelid geometry, lighting, and glasses influence p and nu.

Exact conditional result: if two hypotheses admit the same observed rho, their entire observed event processes are identical for every observation duration. With known distinct rates, optimal accuracy is (1+TV(Poisson(T*rho0),Poisson(T*rho1)))/2. Conditional event timestamps add no information about homogeneous rate beyond the event count.

Illustrative comparison: 12 versus 24 events/min, equal priors. At five seconds perfect detection yields 0.6648765163 accuracy. Ninety percent requires 47.599 seconds. Imperfect p=0.8 and nu=1/min yields 0.6400678189 at five seconds and requires 64.598 seconds for ninety percent.

Counterexample: lambda0=12/min,p0=1; lambda1=24/min,p1=0.5. Both observed rates equal 12/min.

Strongest confound: detection sensitivity changes between participants/devices. Decisive falsification: independent high-speed reference with calibrated p and nu, plus goodness-of-fit tests for the Poisson process assumption. Predeclare held-out participant, lighting, device, and glasses groups and predict a boundary crossing before evaluation.

Product: reject reliable five-second state inference from blink count alone under this model. Calibrated blink-event timing or duration can remain separate research targets. This theorem does not bound all other eye or behavioral signals.

Human data: not evaluated. Model adequacy: not validated. Field-level novelty: not established. Independent numeric checks: passed. Next kernel: renewal-process extension or actual paired human evaluation, not dataset metadata inspection.
