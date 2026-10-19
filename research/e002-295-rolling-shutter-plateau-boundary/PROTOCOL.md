# Mandatory breakthrough kernel
Question: Can within-frame rolling-shutter exposure provide an affine-photometry-invariant eyelid velocity, and when is it impossible?
Signal/reference: native RGB row profile / synchronized >=250-FPS independently measured eyelid-edge trajectory (NOT YET AVAILABLE).
Frontier: generic rolling-shutter motion inversion and high-speed blink kinematics already established.
Metric: two-plateau margin m, ramp width w, bounded velocity interval, held-out reference interval coverage and abstention.
Strongest confound: acceleration and glasses/spatially varying photometry.
Model: THEOREM.md.
Falsification: predicted plateau survival fails on untouched participants/devices; width-based interval undercovers synchronized reference; acceleration/glare corrupts shape.
Human test: freeze native exposure and row-delay calibration, edge ROI, plateau criterion, device/participant split, light/gaze/glasses stress, synchronization and high-speed reference before outcomes. None run.
Publication gate: independent prior-art audit; >=90% prospective interval coverage under frozen tolerance; improvement over geometry-only, brightness-only, missingness-only and temporal-smoothness controls; external reproduction.
Product: research-only calibrated blink-velocity certificate with abstention, not fatigue diagnosis.
Synthetic frozen holdout: H=48,T=1/90,tau=14e-6; predict vcrit=6750000/1657 (~4073.63) between 3500 (plateaus possible) and 4500 (impossible). This is not a human holdout.
Acceleration rule: EyeDentify path was blocked twice previously and is abandoned; no dataset-access archaeology in this run.