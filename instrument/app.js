const byId = (id) => document.getElementById(id);

const setup = byId("setup");
const capture = byId("capture");
const preview = byId("preview");
const cameraButton = byId("cameraButton");
const startButton = byId("startButton");
const cameraStatus = byId("cameraStatus");
const countdown = byId("countdown");
const exportArea = byId("exportArea");

let protocol;
let stream;
let recorder;
let recordedChunks = [];
let videoBlob = null;
let metadataBlob = null;
let captureFileStem = null;
let frameLoopActive = false;
let frameLog = [];
let faceLog = [];
let faceDetector = null;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
const clock = () => performance.now();

function rgb(values) {
  return "rgb(" + values.join(",") + ")";
}

function sanitize(value) {
  return String(value)
    .replace(/[^a-zA-Z0-9._-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function fileStem(condition, startedAtIso, captureNumber, retry) {
  const participant = sanitize(byId("participant").value || "pilot");
  const session = sanitize(byId("session").value || "1");
  const stamp = startedAtIso.replace(/[:.]/g, "-");
  const captureTag = "c" + String(captureNumber).padStart(2, "0");
  const attemptTag = retry ? "retry" : "primary";
  return (
    "lucent_" + participant +
    "_s" + session +
    "_" + captureTag +
    "_" + condition +
    "_" + attemptTag +
    "_" + stamp
  );
}

function syncPlannedCondition() {
  if (!protocol?.pilot?.capture_order) return;
  const captureNumber = Number(byId("captureNumber").value);
  const condition = protocol.pilot.capture_order[captureNumber - 1];
  if (!condition || !protocol.conditions[condition]) {
    throw new Error("Invalid frozen pilot capture number.");
  }
  byId("condition").value = condition;
}

function chooseMimeType() {
  const options = [
    "video/webm;codecs=vp9",
    "video/webm;codecs=vp8",
    "video/webm",
    "video/mp4"
  ];

  if (!window.MediaRecorder) return "";
  for (const item of options) {
    if (MediaRecorder.isTypeSupported(item)) return item;
  }
  return "";
}

async function loadProtocol() {
  const response = await fetch("./protocol.json", {cache: "no-store"});
  if (!response.ok) throw new Error("Could not load protocol.json");
  protocol = await response.json();
  syncPlannedCondition();
}

async function enableCamera() {
  if (stream) return;

  const c = protocol.capture.video;
  stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: {
      facingMode: {ideal: c.facingMode},
      width: {ideal: c.width_ideal},
      height: {ideal: c.height_ideal},
      frameRate: {ideal: c.frameRate_ideal, min: c.frameRate_min}
    }
  });

  preview.srcObject = stream;
  await preview.play();

  const settings = stream.getVideoTracks()[0].getSettings();
  cameraStatus.textContent =
    "Camera ready · " +
    (settings.width || "?") + "×" + (settings.height || "?") +
    " · " + (settings.frameRate || "?") + " fps";

  if ("FaceDetector" in window) {
    try {
      faceDetector = new FaceDetector({fastMode: true, maxDetectedFaces: 1});
    } catch {
      faceDetector = null;
    }
  }

  cameraButton.disabled = true;
  startButton.disabled = false;
}

function beginVideoFrameLog() {
  frameLog = [];
  faceLog = [];
  frameLoopActive = true;

  if (!("requestVideoFrameCallback" in HTMLVideoElement.prototype)) return;

  let lastFaceSample = -Infinity;

  const callback = async (callbackNow, meta) => {
    if (!frameLoopActive) return;

    frameLog.push({
      callbackNowMs: callbackNow,
      mediaTimeS: meta.mediaTime ?? null,
      expectedDisplayTimeMs: meta.expectedDisplayTime ?? null,
      presentedFrames: meta.presentedFrames ?? null,
      processingDurationS: meta.processingDuration ?? null,
      width: meta.width ?? null,
      height: meta.height ?? null,
      captureTimeMs: meta.captureTime ?? null,
      receiveTimeMs: meta.receiveTime ?? null,
      rtpTimestamp: meta.rtpTimestamp ?? null
    });

    if (faceDetector && callbackNow - lastFaceSample >= 180) {
      lastFaceSample = callbackNow;
      try {
        const faces = await faceDetector.detect(preview);
        const box = faces && faces[0] ? faces[0].boundingBox : null;
        if (box) {
          const width = preview.videoWidth || 1;
          const height = preview.videoHeight || 1;
          const areaFraction = (box.width * box.height) / (width * height);
          const centerX = (box.x + box.width / 2) / width;
          const centerY = (box.y + box.height / 2) / height;
          const centerDistance = Math.hypot(centerX - 0.5, centerY - 0.5);
          const quality =
            Math.max(0, Math.min(1, 4 * areaFraction)) *
            Math.max(0, 1 - centerDistance);

          faceLog.push({
            callbackNowMs: callbackNow,
            detected: true,
            box: {x: box.x, y: box.y, width: box.width, height: box.height},
            areaFraction,
            centerDistance,
            quality
          });
        } else {
          faceLog.push({callbackNowMs: callbackNow, detected: false});
        }
      } catch {
        faceLog.push({callbackNowMs: callbackNow, detected: null});
      }
    }

    if (frameLoopActive) preview.requestVideoFrameCallback(callback);
  };

  preview.requestVideoFrameCallback(callback);
}

function stopVideoFrameLog() {
  frameLoopActive = false;
}

function startRecorder() {
  return new Promise((resolve, reject) => {
    recordedChunks = [];
    const mimeType = chooseMimeType();
    recorder = new MediaRecorder(stream, mimeType ? {mimeType} : undefined);

    recorder.ondataavailable = (event) => {
      if (event.data && event.data.size) recordedChunks.push(event.data);
    };
    recorder.onerror = (event) => {
      reject(event.error || new Error("MediaRecorder failed"));
    };
    recorder.onstop = () => {
      videoBlob = new Blob(
        recordedChunks,
        {type: recorder.mimeType || "video/webm"}
      );
      resolve();
    };

    recorder.start(100);
  });
}

function summarizeFrameCadence(frames) {
  if (frames.length < 2) {
    return {available: false, count: frames.length};
  }

  const times = frames
    .map((item) => item.callbackNowMs)
    .filter(Number.isFinite);

  const gaps = [];
  for (let i = 1; i < times.length; i++) gaps.push(times[i] - times[i - 1]);
  gaps.sort((a, b) => a - b);

  const quantile = (p) =>
    gaps[Math.min(gaps.length - 1, Math.floor(p * gaps.length))];

  const mean = gaps.reduce((a, b) => a + b, 0) / gaps.length;

  let presentedFrameGaps = 0;
  const presented = frames
    .map((item) => item.presentedFrames)
    .filter(Number.isFinite);

  for (let i = 1; i < presented.length; i++) {
    const difference = presented[i] - presented[i - 1];
    if (difference > 1) presentedFrameGaps += difference - 1;
  }

  return {
    available: true,
    count: frames.length,
    meanIntervalMs: mean,
    medianIntervalMs: quantile(0.5),
    p95IntervalMs: quantile(0.95),
    maxIntervalMs: gaps[gaps.length - 1],
    presentedFrameGaps
  };
}

async function runCapture() {
  startButton.disabled = true;
  exportArea.classList.add("hidden");

  syncPlannedCondition();
  const captureNumber = Number(byId("captureNumber").value);
  const technicalRetry = byId("retry").checked;
  const condition = byId("condition").value;
  const plannedCondition = protocol.pilot.capture_order[captureNumber - 1];
  const conditionDef = protocol.conditions[condition];
  const startedAtIso = new Date().toISOString();
  const currentCaptureStem = fileStem(
    condition,
    startedAtIso,
    captureNumber,
    technicalRetry
  );
  const segmentCount = Math.round(
    protocol.total_seconds / protocol.segment_seconds
  );

  if (!conditionDef) throw new Error("Unknown condition");
  if (condition !== plannedCondition) {
    throw new Error("Condition does not match the frozen pilot order.");
  }
  if (condition !== "passive" && conditionDef.high_segments.length !== 3) {
    throw new Error("Matched-exposure active protocol has changed.");
  }

  const track = stream.getVideoTracks()[0];
  const settings = track.getSettings();
  const capabilities = track.getCapabilities ? track.getCapabilities() : {};

  const meta = {
    schemaVersion: "lucent-e002-capture-v1",
    protocolVersion: protocol.protocol_version,
    condition,
    plannedCondition,
    pilotCaptureNumber: captureNumber,
    technicalRetry,
    participantPseudonym: byId("participant").value,
    session: byId("session").value,
    captureFileStem: currentCaptureStem,
    userInputs: {
      screenBrightnessPercent: Number(byId("brightness").value),
      ambientCategory: byId("ambient").value,
      approximateDistanceCm: Number(byId("distance").value)
    },
    startedAtIso,
    timeOriginEpochMs: performance.timeOrigin,
    userAgent: navigator.userAgent,
    platform: navigator.platform ?? null,
    hardwareConcurrency: navigator.hardwareConcurrency ?? null,
    deviceMemoryGb: navigator.deviceMemory ?? null,
    screen: {
      widthCssPx: screen.width,
      heightCssPx: screen.height,
      availWidthCssPx: screen.availWidth,
      availHeightCssPx: screen.availHeight,
      devicePixelRatio: window.devicePixelRatio,
      colorDepth: screen.colorDepth
    },
    camera: {
      settings,
      capabilities,
      label: track.label,
      requestVideoFrameCallback:
        "requestVideoFrameCallback" in HTMLVideoElement.prototype,
      faceDetectorSupported: Boolean(faceDetector)
    },
    nominalStimulus: {
      totalSeconds: protocol.total_seconds,
      segmentSeconds: protocol.segment_seconds,
      lowRgb: protocol.low_rgb,
      highRgb: protocol.high_rgb,
      highSegments: conditionDef.high_segments
    },
    stimulusEvents: [],
    videoFrames: [],
    faceSamples: []
  };

  const recorderDone = startRecorder();
  beginVideoFrameLog();

  setup.classList.add("hidden");
  capture.classList.remove("hidden");

  const captureStart = clock();
  meta.captureStartNowMs = captureStart;

  for (let segment = 0; segment < segmentCount; segment++) {
    const high = conditionDef.high_segments.includes(segment);
    const requestedRgb = high ? protocol.high_rgb : protocol.low_rgb;
    capture.style.background = rgb(requestedRgb);

    const actualStart = clock();
    meta.stimulusEvents.push({
      segment,
      high,
      requestedRgb,
      scheduledOffsetMs: segment * protocol.segment_seconds * 1000,
      actualOffsetMs: actualStart - captureStart
    });

    countdown.textContent =
      (protocol.total_seconds - segment * protocol.segment_seconds)
        .toFixed(1) + " s";

    const deadline =
      captureStart + (segment + 1) * protocol.segment_seconds * 1000;
    const remaining = deadline - clock();
    if (remaining > 0) await sleep(remaining);
  }

  meta.captureEndNowMs = clock();
  meta.actualDurationMs = meta.captureEndNowMs - meta.captureStartNowMs;

  recorder.stop();
  await recorderDone;
  stopVideoFrameLog();

  meta.videoFrames = frameLog;
  meta.faceSamples = faceLog;
  meta.frameCadence = summarizeFrameCadence(frameLog);
  meta.recorder = {
    mimeType: recorder.mimeType,
    bytes: videoBlob.size
  };
  meta.completedAtIso = new Date().toISOString();

  metadataBlob = new Blob(
    [JSON.stringify(meta, null, 2)],
    {type: "application/json"}
  );
  captureFileStem = currentCaptureStem;

  capture.classList.add("hidden");
  setup.classList.remove("hidden");
  exportArea.classList.remove("hidden");
  startButton.disabled = false;

  const errors = meta.stimulusEvents.map((event) =>
    Math.abs(event.actualOffsetMs - event.scheduledOffsetMs)
  );
  const maxError = Math.max(...errors);

  cameraStatus.textContent =
    "Capture complete · " +
    frameLog.length +
    " frame callbacks · max stimulus scheduling error " +
    maxError.toFixed(1) +
    " ms";
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  document.body.appendChild(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}

byId("captureNumber").addEventListener("change", () => {
  try {
    syncPlannedCondition();
  } catch (error) {
    cameraStatus.textContent = "Protocol error: " + error.message;
  }
});

cameraButton.addEventListener("click", async () => {
  try {
    await enableCamera();
  } catch (error) {
    cameraStatus.textContent = "Camera error: " + error.message;
  }
});

startButton.addEventListener("click", async () => {
  try {
    await runCapture();
  } catch (error) {
    capture.classList.add("hidden");
    setup.classList.remove("hidden");
    startButton.disabled = false;
    cameraStatus.textContent = "Capture error: " + error.message;
  }
});

byId("videoDownload").addEventListener("click", () => {
  if (!videoBlob || !captureFileStem) return;
  const extension = videoBlob.type.includes("mp4") ? "mp4" : "webm";
  downloadBlob(videoBlob, captureFileStem + "." + extension);
});

byId("jsonDownload").addEventListener("click", () => {
  if (!metadataBlob || !captureFileStem) return;
  downloadBlob(metadataBlob, captureFileStem + ".json");
});

await loadProtocol();
