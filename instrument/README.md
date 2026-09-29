# Lucent Phone Observability Instrument

This directory contains the research instrument for E002: APST-5 phone observability.

It is not a product UI. Its purpose is to collect synchronized front-camera video and stimulus timing so the APST-5 measurement assumptions can be falsified on commodity phones.

## Fixed conditions

The first pilot uses three five-second conditions:

1. passive — constant low display;
2. contiguous — three adjacent high-luminance segments;
3. split — the APST5-SIM-001 equal-exposure sequence.

Both active conditions contain exactly three 0.5-second high segments and therefore have matched nominal screen-content exposure.

The committed timing is stored in protocol.json.

## What the browser records

Nothing is uploaded. Each run produces a front-camera video and a JSON sidecar containing stimulus timestamps, camera frame callbacks where supported, track settings/capabilities, device/screen metadata, user-entered brightness, ambient category, dropped-frame diagnostics, and optional browser-native face-detection samples.

Raw participant video must never be committed to Git.

## Running it

Camera APIs require a secure context. Serve this directory over HTTPS or localhost.

Desktop test:

    python -m http.server 8000

then open http://localhost:8000/instrument/.

For a phone, use an HTTPS host.

## Pilot procedure

Use ordinary rested/naturalistic states. Do not intentionally deprive yourself or anyone else of sleep for this pilot.

For the first nine-capture pilot, keep the phone, brightness, lighting, and approximate distance stable and use the frozen order:

    passive
    contiguous
    split
    passive
    split
    contiguous
    split
    contiguous
    passive

Export both files after every capture. The video and JSON sidecar now share one frozen capture stem. Run the offline quality checker before any biological interpretation.

Do not reorder conditions after seeing any trace or quality metric. Technical retry rules are frozen in experiments/registrations/E002_PROTOCOL_AMENDMENT_001.md.

## Safety

The protocol uses slow 0.5-second luminance blocks rather than rapid flashing. Keep the display at a comfortable brightness. Stop if it causes discomfort, headache, dizziness, visual symptoms, or eye strain. Do not run it while driving or doing any safety-critical activity.

## Offline quality analysis

Install OpenCV separately:

    pip install opencv-python-headless

Then:

    python instrument/analyze_capture.py capture.webm capture.json --output quality.json

The analyzer checks timing, frame cadence, blur, face visibility, and eye-region detectability. It does not estimate fatigue.

## E002 exit criterion

The instrument only clears E002 when repeated real captures show that camera/stimulus timing is stable, face/eye regions remain measurable, repeated ocular-response features are reproducible, and split versus contiguous probes create distinguishable response dynamics under matched exposure.

Until actual captures exist, E002 remains open.
## Pupil dynamics extraction

For visible-light exploratory pupil traces:

    pip install opencv-python-headless mediapipe

    python instrument/extract_pupil_dynamics.py capture.webm capture.json --output capture.pupil.json --trace-output capture.trace.csv

The extractor uses refined face/iris landmarks only to localize the eye, then estimates a dark central pupil region relative to iris diameter. It is heuristic and quality-gated; inspect failures rather than treating every output as a valid measurement.

## Aggregate E002 decision

Use a consistent file stem for each capture:

- stem.quality.json
- stem.pupil.json
- stem.trace.csv

Then evaluate the frozen engineering gates:

    python experiments/e002_observability_analysis.py path/to/captures --output e002_result.json

The exact gates and exit rule are frozen in experiments/registrations/E002_PHONE_OBSERVABILITY.md.