# E002-665 | Randomized phase coverage is not a velocity certificate (2026-11-06 UTC)

## New falsification and quantitative intervention
E002-664 exhibited a triangular periodic aperture trajectory open at each phase-locked frame and closed at each midpoint. This experiment asks whether changing capture phase breaks that specific aliasing failure. Define period T=1/f, normalized phase u=t/T mod 1, aperture a(u)=2|u-1/2|, and closure threshold c=0.3. The closed-phase set has Lebesgue measure c per period. For n **independent uniform** phase probes, probability of observing at least one closure is exactly 1-(1-c)^n. At n=10, this is 1-0.7^10 = 0.9717524751. This is an event-detection probability for the stipulated synthetic periodic signal, **not** a confidence level for human blink absence.

If all n observations share one random phase (perfectly correlated jitter), the detection probability remains c=0.3. If all phase offsets stay within +/-0.1 period of the open endpoint, detection is impossible in this fixture, regardless of observation count. An adversarial deterministic phase schedule can also miss forever. Hence simply enabling jitter or recording longer is not enough: independence, phase support, timing uncertainty, and sampling clock must be measured. Real blinks are not assumed periodic.

## Reproduction and falsification
Run `python3 research/observability/e002_665_phase_dither.py`. Exact fractions assert the 20-phase grid has six closed phases, IID ten-draw probability 1-(7/10)^10, the restricted-jitter failure, and the fully correlated failure. The code is synthetic only; no device experiment or human evidence.

## Frozen instrument-to-human protocol
1. Use an independently clocked moving aperture or programmable optical shutter with externally measured state and a calibrated timestamped LED phase marker. Sweep known closure widths and random versus correlated capture phases. Preregister the phase schedule and measured jitter distribution before inspecting the held-out state trace.
2. Run ordinary cameras at 24/30/60/120 Hz across exposure, rolling-shutter rows, brightness, saturation, focus/blur, missing frames, and timestamp error. Log commanded and measured phase; reject nominal frame-rate as a timing calibration.
3. Separately measure an upper velocity bound using high-rate reference capture, never low-rate finite differences. For each low-rate pair compute the existing sharp gap certificate with conservative uncertainty from exposure kernel, row time, clock error, and geometry.
4. On independently annotated participant-held-out high-rate human sequences, preregister downsampling phases and evaluate false negative absence certificates, abstention fraction, and phase-coverage detection. Split by participant and device. Report confidence intervals clustered by participant, not frame.
5. **Kill criterion:** any closure observed by authenticated high-rate reference during a low-rate interval labeled deterministically closure-free falsifies that deployed certificate. Phase-randomized detection alone must never be marketed as deterministic blink exclusion.

## Product decision
Randomized phase capture may be an *optional probabilistic detection aid* only after physical and human calibration of phase distribution and capture independence. It cannot replace the E002-371 independent velocity bound or remove ABSTAIN_UNCALIBRATED. Production remains BLOCKED.

## Evidence tier
Mathematical synthetic construction and executable exact-arithmetic test. No authenticated human sequence, physical instrument result, external independent replay, or release approval.
