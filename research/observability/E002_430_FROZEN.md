# E002-430 — high-rate reference is not continuous ground truth

**Protocol documented 2026-10-25, before repository publication.** This is a reproducible synthetic falsification, **not** a prospectively registered human study. The physical observability kernel remains E002-371. No new theorem or human measurements are claimed.

## Prediction and fixed test gates

1. Construct two nonnegative continuous physical-aperture worlds with the **same value 2.15 mm at every reference sampling instant**. World A is constantly 2.15 mm; World B has a single triangular dip to 1.95 mm halfway between two reference samples, then returns to 2.15 mm. Threshold theta = 2.00 mm. Evaluate rates 200, 400, 500, 600 Hz. Exact slope is 0.40 * rate mm/s.
2. A naive framewise reference should incorrectly label both worlds as never closed, although World B crosses the threshold. The adversarial world must obey a stipulated speed cap of 243 mm/s at every listed rate. **243 mm/s is a published group mean, not an authenticated hard bound**; it is used only to demonstrate human-scale plausibility of the synthetic speeds.
3. For two physical-aperture samples with error <= epsilon, timing error <= j at each end, and an independently authenticated hard velocity cap V, use a conservative between-sample lower envelope. Let a=y0-epsilon, b=y1-epsilon, D=dt+2j. The envelope is max(0, (a+b-VD)/2, a-VD, b-VD). Test it against an independently implemented dense two-cone numerical oracle. This is established Lipschitz optimal recovery, not new mathematics.
4. An unresolved interval must never be called a verified negative merely because all observed frames are open. A physically justified no-closure reference label requires the lower envelope strictly > theta, calibrated geometry and timing, valid anatomical landmarks, and independently justified V. Any missing frame, occlusion, gaze, blur, glasses, illumination, or clock/geometry uncertainty outside calibration invalidates the negative.
5. Sensitivity cases: epsilon=0.05 mm, j=0.1 ms must never increase the lower envelope. A positive control with large physical aperture must remain conditionally certifiable, proving the method does not simply abstain on everything. Reject invalid numeric inputs. Product output is always ABSTAIN_UNCALIBRATED.

## Primary literature and limits

Kwon et al., *Journal of the Royal Society Interface* 10 (2013), 20130227, DOI 10.1098/rsif.2013.0227: 25 volunteers filmed at **600 fps**, but central physical aperture measured **every 5 ms**; reported group mean peak closing speed 243 +/- 9 mm/s. The 5-ms annotations correspond to 200-Hz measurement spacing, **not** the 600-fps acquisition cadence. Neither provides continuous-time ground truth. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC4043155/

Navascues-Cornago et al., *The Ocular Surface* 40 (2026), 22-30, DOI 10.1016/j.jtos.2026.01.003: human blink recordings at 500 fps show that lower-rate sampling underestimates maximum velocities, reinforcing the need for independently justified velocity caps. Source: https://pubmed.ncbi.nlm.nih.gov/41565104/

No individual human traces were obtained after two targeted public-source searches. The FaceBase 400-fps marker data remain controlled access. This experiment cannot estimate human failure rates or validate physical aperture registration.

## Human execution blocker

Acquire consented 400-600-fps human eyelid videos or controlled-access marker trajectories with independent 3D-to-central-aperture calibration. Preserve raw timestamps, shutter/row timing and two blinded landmark annotations. Freeze device/participant-disjoint ordinary-camera predictions before reference inspection. Treat reference negatives as **UNRESOLVED** unless the between-reference-sample lower envelope exceeds theta under independently authenticated velocity, geometry, error and timing limits. Count witnessed crossings separately. Publish participant-level errors, unresolved intervals, abstention and nuisance strata. Never treat a 5-ms annotation grid or 600-fps recording alone as continuous truth.

**Release gate:** no physical no-closure certificate, PERCLOS, blink-duration or fatigue measurement. Keep ABSTAIN_UNCALIBRATED until externally verified human and instrument evidence.
