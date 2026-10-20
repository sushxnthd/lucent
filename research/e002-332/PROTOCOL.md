# Frozen human evidence protocol — E002-332

**Question:** Does native RGB eye geometry or slow pupil amplitude predict an independently referenced ocular signal after controlling gaze, brightness, missingness, and timing?

1. Signal/reference: native 25–60-fps RGB frames with actual exposure timestamps versus raw synchronized >=90-Hz pupil reference for slow amplitude or >=250-Hz eyelid reference for blink phase.
2. Literature: EyeDentify WACV 2025 (paired webcam/Tobii); PupilSense 2025; Kwon et al. 2013 high-speed blink kinematics. Their results are prior art, not Lucent breakthroughs.
3. Metric: 95%-target participant-clustered interval coverage; selective false certificates, event F1, subgroup worst-case error, abstention.
4. Strongest nuisance: differential occlusion/illumination and clock misalignment.
5. Model: RGB Y_j=Q[int_{E_j} K*(G M F(r,R,gaze,scale)+B)dt/E_j+e]; raw eye reference z_k=r(t_k+clock_offset)+nu. No row-order reference pairing.
6. Falsification: >5% false certificates on supported untouched participant/device/lighting/glasses holdouts, nuisance-only baseline matches, or unbounded timing.
7. Boundary prediction: freeze geometry/photometry/sampling/clock uncertainty from calibration; predict certify/abstain crossing on a reserved regime before opening outcomes.
8. Human test: split participants and device before outcomes; hold out lighting/glasses regime when possible; no post-hoc threshold retuning.
9. Publication gate: primary novelty audit, >=95% clustered coverage, <=5% false certificates, >=50% supported non-abstention, stronger than four nuisance controls, unseen boundary, independent checker and replication.
10. Product: permit calibrated interval-valued eyelid occupancy or slow pupil amplitude only; reject rapid pupil-lag and five-second fatigue certification.

**Controls:** geometry-only, brightness-only, missingness-only, temporal-smoothness-only. Native timing and raw reference required. EyeDentify processed labels are NOT acceptable for temporal validation without a raw timestamp audit.

**Acceleration:** Kaggle archive and blinkingmatters ZIP downloads failed in this runtime. Do not spend another consecutive run on these access paths; switch immediately to new public paired data or a physically grounded instrument test.