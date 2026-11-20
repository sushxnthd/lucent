# E002-646 | Optical integration falsifies timing-only detectability

Evidence tier: analytical instrument, not physical or human evidence.

For rectangular exposure E=[a,b] and pulse P=[c,d], let q=|E∩P|/(b-a). Under a linear, unsaturated sensor with baseline-subtracted normalized contrast C∈[C_lo,C_hi] and a deterministic detection threshold τ, the observed pulse contrast is qC. Thus **guaranteed detection requires q C_lo > τ**; **guaranteed nondetection holds when q C_hi ≤ τ**; otherwise abstain. The strict inequality makes equality a nondetection boundary under the stipulated detector. These conditions are sharp for the interval model.

Counterexample to timing-only inference: E=[0,10] ms and P=[4,6] ms intersect for 2 ms, but q=0.2. At C_lo=0, even perfect temporal overlap cannot guarantee detection at any positive threshold. At C=1, τ=0.2 is the exact nondetection boundary. Exposure overlap is therefore a geometric opportunity, not a sensor-detection certificate.

Reproduce: `python research/observability/e002_646_optical_detection_boundary.py`. Exact-rational synthetic grid and explicit boundary assertions; this run has **not** independently executed the Python file in hosted CI. The result applies only with independently established linear response, contrast bounds, threshold, exposure timing, and no saturation. Rolling shutter, gain/ISP, read noise, shot noise, blur, LED waveform and scene brightness can invalidate the premises.

**Product consequence:** E002-645 GUARANTEED_INTERSECTION must never be translated to 'blink/closure detected'. To support optical detection, require independent calibrated lower signal contrast, threshold/noise envelope and sensor-response validation; otherwise ABSTAIN. The stronger physiological closure-exclusion claim remains BLOCKED pending actual synchronized reference-timed acquisition and human validation. No new human or physical evidence was obtained. This analytical result does not supersede the frozen E002-644 acquisition protocol.
