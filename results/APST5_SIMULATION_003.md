# APST5-SIM-003: Concurrent Multimodal Temporal Compression

**Status:** reproducible model-based sensitivity result; human validation pending.

## Question

Can an ultra-short Lucent scan recover more state information by probing pupil and smooth-pursuit dynamics **concurrently** rather than spending the same time on pupil dynamics alone?

## Motivation

Sleep-loss and fatigue literature reports changes in multiple ocular systems, including:

- pupil size and phasic pupil response;
- saccadic velocity;
- pursuit gain;
- motion-processing noise.

Stone et al. reported approximately 1%/hour deterioration in several pursuit and saccade metrics during extended wakefulness, while Chen et al. reported medium-to-large time-on-task effects in pupil and saccade dynamics.

Separately, smartphone-video work has shown that commodity phones can recover useful gaze / smooth-pursuit information.

The design opportunity is to make one screen sequence do two jobs at the same time.

## Surrogates

### Pupil channel

Uses Lucent's existing delayed asymmetric pupil-response state surrogate and nuisance projection.

### Smooth-pursuit channel

A sinusoidal target is followed by a first-order gaze system with:

- subject-specific baseline pursuit gain;
- subject-specific response time constant;
- a latent-state gain reduction;
- a latent-state slowing term.

The target frequency is selected on a design population.

The pupil and pursuit channels are then combined through nuisance-projected state Fisher information.

## Sensitivity envelope

The experiment deliberately does not assume one precise fatigue effect or one camera-noise level.

It evaluates 80 combinations:

- pursuit gain reduction at full state:
  \(3\%,6\%,10\%,14\%,18\%\);
- response-time-constant increase:
  \(0,15,30,50\) ms;
- normalized gaze measurement noise:
  \(0.05,0.10,0.15,0.20\).

For every cell:

1. the pursuit frequency is optimized on one synthetic design population;
2. performance is evaluated on fresh nuisance and state-effect draws;
3. the comparator is an independently optimized **five-second pupil-only** probe.

## Held-out result

The five-second pupil-only comparator achieved approximately:

\[
IG_{5s,\ pupil}=0.3930\text{ nats}.
\]

### Two-second concurrent scan

Across the 80 sensitivity cells:

- **60/80 (75%)** beat the five-second pupil-only comparator;
- median information ratio: **1.157x**;
- worst-case ratio in the grid: **0.880x**;
- best-case ratio: **1.725x**.

### Three-second concurrent scan

Across the same 80 cells:

- **72/80 (90%)** beat the five-second pupil-only comparator;
- median information ratio: **1.238x**;
- worst-case ratio: **0.967x**;
- best-case ratio: **1.757x**.

## Interpretation

The result does not say that a real three-second phone scan is already better than five-second pupillometry.

It says something narrower and useful:

> over a deliberately broad range of pursuit-effect and camera-noise assumptions, **concurrent measurement changes the duration-information frontier enough that a three-second multimodal design usually reaches or exceeds the five-second pupil-only state-information target in the surrogate.**

This is the next falsifiable design prediction.

## Human test

A phone study should compare, under the same total duration:

1. pupil-only active scan;
2. pursuit-only active scan;
3. concurrent luminance + pursuit scan.

The critical test is whether the joint condition adds held-out behavioral-state information beyond the best single channel after modeling cross-channel covariance.

## Boundary

The current combination treats channel measurement noise and nuisance as conditionally independent.

That assumption will be false to some degree in real data.

A real experiment must estimate shared covariance and may reduce the predicted multimodal gain.

The result is therefore an **experimental-design breakthrough candidate**, not biological validation.
