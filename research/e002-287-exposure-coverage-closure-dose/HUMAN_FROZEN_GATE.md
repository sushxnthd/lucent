# Frozen prospective human protocol — not executed
Use independent >=120Hz eyelid-aperture reference with synchronized camera exposure start/end, not labels inferred from test RGB.
Normalize c_ref(t)=clip(1-aperture/open_baseline,0,1), target D_ref=integral c_ref dt over 5s.
Calibrate RGB radiance-linearity, geometry, pose/gaze, clipping and per-frame eta on separate calibration participants.
Freeze threshold and eta before untouched participant/device/light/glasses/gaze holdouts.
Primary outcome: reference D_ref lies within predicted dose interval; report 99% coverage target with participant-clustered uncertainty and abstention.
Controls: geometry-only EAR/ELA, brightness-only, missingness-only and temporal smoothness; nuisance-only auto-exposure, flicker, glasses reflections, gaze and head pitch.
Predeclare an unseen shutter-duty crossing (certify vs abstain) based on calibrated eta before final evaluation.
If calibrated linear closure surrogate fails, reject this kernel and pivot; do not tune after holdout.
