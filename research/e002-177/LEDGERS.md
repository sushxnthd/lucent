# E002-177 science and product ledger

SCIENCE: In the restricted blurred radial-edge model I_R(x)=Phi((x-R)/s), arbitrary unknown strictly increasing per-frame tone maps make R structurally non-identifiable. The constructive map h(u)=Phi(Phi^-1(u)+(R-R')/s) exactly transforms the radius-R profile to radius-R'. This is elementary algebra, not a novel field theorem. Synthetic tests: 18/18 equivalence cases, maximum numerical residual 2.3314683517128287e-15; 12 gamma examples passed independent local checking. A gamma shift from 1 to 2.2 with blur 1.5 pixels moves the modeled half-contrast edge by 0.9180 pixels, exceeding a 5% change of a 9-pixel radius (0.45 pixels). Not measured in a real camera.

CONTROL: A *fixed* gamma and fixed blur shift both frames equally and cancel in temporal differences. Full RGB iris texture and photometric anchors may break the restricted-model ambiguity. Existing webcam/eye-tracker validation: MEYE (2021) and js-mEye (2025). No physiological RGB data used.

PRODUCT: Do not certify rapid pupil change using half-contrast edges across uncontrolled time-varying nonlinear tone maps. Require photometric stability/calibration or reject. Actual calibration and rejection coverage remain unmeasured.

PRIMARY KERNEL: RGB pupil/iris temporal waveform vs synchronized native-timestamp eye-tracker pupil diameter (mm). Frozen held-out correlation lower bound >0.30; lag, amplitude, NRMSE, coverage, nuisance advantage >0.10, and >=8 untouched participants remain mandatory. No fatigue inference.

GATES: exact conditional construction PASS; local independent numerical check PASS; human waveform NOT TESTED; actual camera gamma NOT TESTED; CI NOT CONFIRMED.
