# E002 Phone Observability Instrument

This directory contains a research capture harness, not a Lucent product interface.

Its only purpose is to test the first empirical APST-5 bottleneck:

> Can a commodity phone execute a precisely logged visual probe while its front camera captures ocular dynamics with enough temporal fidelity for system identification?

## Conditions

The instrument records one five-second front-camera clip under one of three conditions:

1. **passive**: constant low display drive, stationary target;
2. **pupil**: the APST5-SIM-001 split luminance schedule, stationary target;
3. **multimodal**: the same luminance schedule plus a sinusoidal pursuit target.

It exports a local WebM file and a JSON sidecar containing display transitions, camera settings, browser timing, and video-frame callback metadata where supported.

The code uploads nothing.

## Running it

Camera access requires HTTPS or localhost.

~~~bash
cd instrument
python -m http.server 8000
~~~

Then open http://localhost:8000/e002.html on the same machine.

Phone testing should use a controlled HTTPS research host. This instrument is intentionally separate from the public Lucent product/site direction.

## Measurement caveats

### Requested RGB is not calibrated luminance

Actual retinal stimulation depends on display hardware, brightness, automatic display controls, ambient illumination, viewing distance, and spectral output.

The exported JSON therefore records a **requested normalized display drive**, not cd/m².

### Browser video is not a scientific sensor clock

A browser can vary exposure, frame rate, image processing, and encoding latency. The harness uses `requestVideoFrameCallback` when available so E002 can quantify frame delivery and drops, but that does not magically make a browser camera calibrated instrumentation.

### Pursuit frequency is not frozen yet

The default 0.8 Hz is simply a pilot value in the design range explored by APST5-SIM-003. E002 should measure observability first, then freeze the human protocol before any state outcome is analyzed.

## E002 order of operations

Do not start with fatigue induction.

First establish, under an approved protocol with an alert consenting adult:

1. actual frame timing and dropped-frame behavior;
2. pupil/eye tracking yield;
3. repeatability of the pupil response;
4. recoverability of pursuit trajectories;
5. uncertainty on any derived latency/gain estimate;
6. repeatability across routine capture conditions.

Only after those gates pass should Lucent pair the scan with an external behavioral-state reference.

Human testing involving minors or deliberate sleep deprivation should not be used as a shortcut to validation.
