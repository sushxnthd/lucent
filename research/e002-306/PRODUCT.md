# E002-306 product decisions

ALLOW RESEARCH-ONLY: interval-valued projected pupil-arc radius if chord endpoints, gaze correction, circularity, exposure stability, optical mapping and contour uncertainty eta are independently calibrated.

REJECT: point-valued rapid anatomical pupil waveform, pupil lag and five-second fatigue certification from an occluded ordinary-RGB pupil arc.

CALIBRATE: distinguish fixed-chord radii only when |s1-s2|>2eta; abstain at equality and when the observed arc cannot produce a finite certified interval.

REDESIGN: treat pupil extraction as an instrument with physical uncertainty and fail-closed abstention; consider blink timing/aperture separately only under their own validated measurement laws.

No app code, no human validation, no new field-level discovery.
