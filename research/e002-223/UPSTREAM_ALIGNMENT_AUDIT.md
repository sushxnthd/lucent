# E002-223 primary-source alignment audit

Pinned upstream brownhci/WebGazer commit b12701dd7b6d7b00d4b8dbebf87fdec840c24999.

1. www/data/src/participant.py lines 169-175: video startTimestamp is the browser interaction-log epoch of a `recording start` event.
2. www/data/src/webgazerExtractServer.py lines 225-278: ffmpeg showinfo PTS supplies relative frame times; missing PTS are imputed by previous PTS plus int(1000/framerate).
3. www/data/src/videoProcessing.py lines 146-157: frameTimeEpoch = int(frame_pts_ms) + pv.startTimestamp.
4. www/data/src/readme.md: frame time is described as approximate; WebM files were not closed properly; screen-video synchronization is rough and offsets vary.

This is an executable *software mapping*, not proof of a physical exposure-time anchor. It can support approximate pairing, but not an independently certified physiological lag bound. The screen-video caveat must not be incorrectly generalized to the webcam/Tobii pair.
