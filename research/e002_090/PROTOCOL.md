# E002-090 frozen gates

Original EOTT WebM Python/OpenCV replication before inspection: P_54/P_33/P_55 frame counts must equal 632/719/554. Frame-1 grayscale means must be within 2 of 5.708/9.546/122.942; frame-80 means within 3 of 184.772/137.353/129.162. P_54 and P_33 must show dark-to-bright onset and P_55 must not. Verify CRC32. Count Haar eye candidates on frames 80,120,160,240,320; report all, with heuristic >=2 eyes in 3/5 frames for both P_54 and P_33. Eye rectangles are not iris masks. No RGB pupil fidelity or state claims. P_01/P_02/P_07 remain waveform holdouts.
