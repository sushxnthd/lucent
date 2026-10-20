# E002-336 product gate
ALLOW: research-only signed-lag intervals when two independent sync anchors, bounded nonaffine drift, bounded event errors and nuisance controls are validated; abstain otherwise.
REJECT: 10-Hz blink completeness, uncalibrated pupil waveform, sub-exposure phase, precise pupil latency and five-second fatigue certification.
REDESIGN: retain native RGB frames and timestamps; add independently synchronized reference anchors; bound drift, shutter and gaze/eyelid/brightness nuisances; prioritize validated blink-event evidence over uncalibrated pupil dynamics.
