# E002-754 | Phase-lock invalidates repeated-trial reference sensitivity inference

**Evidence tier:** T1 analytical/synthetic; **not** a physical or human measurement.

## Falsifiable question

Can 10,000 repeated short-closure injections establish reference-detector sensitivity if pulse generation and acquisition share a clock? No. Repetition alone does not change sampling phase. The effective number of sampled phases can remain one.

## Frozen exact experiment

Use an ideal point detector sampling every 100 integer ticks. Inject a complete closure lasting 25 ticks, with its onset phase determined by an integer offset. A sample landing inside the closure detects it; all other samples miss it. Repeat 10,000 events. Compare event-to-event phase increments 100 (locked), 37 (coprime phase walk), and 50 (two-phase orbit). Exhaustively enumerate all 100 initial phases, with exact integer arithmetic and assertions in `e002_754_phase_lock.py`.

**Predictions:** locked phase: 75/100 initial phases yield zero detections over 10,000 injections, while 25/100 yield 10,000 detections. Coprime phase walk: all 100 initial phases yield exactly 2,500 detections. Two-phase orbit: the pulse can be entirely missed or detected in 5,000 of 10,000 trials depending on initial phase (boundary convention as coded).

This is a discrete mathematical instrument model. It does not imply the same numbers for a real photodiode, finite exposure, noise, jitter, or human eyelids.

## Independent physical test that would resolve the failure

1. Timestamp pulse generator, reference detector and ordinary camera with independently characterized clocks; record actual pulse onset relative to each detector exposure, not merely commanded delays.
2. Use calibrated optical interruptions of several pulse widths around the empirically measured response threshold. Include asynchronous clock sources or deliberately randomized, independently logged phase offsets.
3. Pre-register the phase histogram, minimum occupancy per phase bin, detection thresholds, and independent timing uncertainty; verify observed phase coverage before interpreting negative labels.
4. Withhold pulse-width/phase combinations for a prospective test. Report missed detections by width, phase, illumination, blur/exposure kernel and clock drift. Repeat after power cycles and clock re-locks.
5. Reject sensitivity claims if observed phase coverage collapses or if the detector's negative labels lack a calibrated missed-event bound. Positive detections can still falsify a Lucent exclusion claim.

## Product consequence

Do not use a large number of nominally independent negative reference trials as evidence that brief closures are absent unless timing-phase coverage and detector sensitivity are independently demonstrated. Keep `ABSTAIN_UNCALIBRATED`; release `BLOCKED`. This is a new *instrument-validation design falsifier*, not physiological validation.

## Reproduction

`python3 research/observability/e002_754_phase_lock.py`

Preserve negative outcomes, timing traces and full raw pulse/phase logs. No human or physical data were acquired in this work.
