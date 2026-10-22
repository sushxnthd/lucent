# E002-376 human study protocol (unexecuted; freeze before test data)

- Independently acquire >=250fps eye-reference and simultaneous native ordinary RGB at 20/25/30/60fps with actual exposure timestamps. Two bracketing sync anchors or hardware trigger required.
- Use training participants to estimate full-closure plateau durations, geometry/contrast calibration, optical noise and overlap requirement m. No test-data refitting.
- Freeze predicted shutter capture fraction from E002-376 and distinguish it from RGB classifier sensitivity. Randomize camera trigger phase; otherwise independently verify phase distribution and abstain from probability claims.
- Hold out participants/devices/lighting/glasses. Controls: geometry-only, brightness-only, missingness-only, smoothness-only. Test blur, gaze, rolling-shutter affected rows and clock jitter.
- Falsify shutter model if independently timestamped reference intervals contradict measured shutter overlap. Falsify optical sufficiency if predicted exposure coverage does not yield detectable RGB signal.
- Report actual event misses, calibration error, subgroup failures, abstention, negative results and code. No paired human test yet.
