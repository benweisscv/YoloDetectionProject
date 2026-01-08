const video = document.getElementById("video");
const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const statusBox = document.getElementById("status");

const PREDICT_URL = "/predict";
const INFERENCE_INTERVAL_MS = 200; // 5 Hz

let lastLatencyMs = 0;

const CLASS_NAMES = {
  0: "person",
  1: "car",
  2: "truck",
  3: "bus",
  4: "bike",
  5: "dog",
  6: "cat"
};


// -------------------------
// Camera setup
// -------------------------
async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: "environment" }
  });

  video.srcObject = stream;

  return new Promise(resolve => {
    video.onloadedmetadata = () => {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      resolve();
    };
  });
}

// -------------------------
// Send frame to backend
// -------------------------
async function sendFrame() {
  if (video.videoWidth === 0) return;

  const offscreen = document.createElement("canvas");
  offscreen.width = video.videoWidth;
  offscreen.height = video.videoHeight;
  const offctx = offscreen.getContext("2d");

  offctx.drawImage(video, 0, 0);

  const blob = await new Promise(resolve =>
    offscreen.toBlob(resolve, "image/jpeg", 0.75)
  );

  const formData = new FormData();
  formData.append("file", blob, "frame.jpg");

  const t0 = performance.now();

  const response = await fetch(PREDICT_URL, {
    method: "POST",
    body: formData
  });

  const t1 = performance.now();
  lastLatencyMs = t1 - t0;

  const result = await response.json();
  drawDetections(result.detections, result.latency_ms);

}

// -------------------------
// Draw bounding boxes
// -------------------------
function drawDetections(detections, latencyMs = null) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  detections.forEach(det => {
    const [x1, y1, x2, y2] = det.bbox;
    const classId = det.class;
    const score = det.score;

    const label = CLASS_NAMES[classId] ?? `class_${classId}`;

    ctx.strokeStyle = "lime";
    ctx.lineWidth = 2;
    ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

    ctx.fillStyle = "lime";
    ctx.font = "16px Arial";
    ctx.fillText(
      `${label} ${(score * 100).toFixed(1)}%`,
      x1,
      Math.max(y1 - 6, 16)
    );
  });

  statusBox.textContent =
    `Detections: ${detections.length}` +
    (latencyMs !== null ? ` | Inference: ${latencyMs.toFixed(0)} ms` : "");
}


// -------------------------
// Main loop
// -------------------------
async function main() {
  statusBox.textContent = "Starting camera…";
  await startCamera();

  statusBox.textContent = "Running YOLO inference…";

  setInterval(() => {
    sendFrame().catch(err => {
      console.error(err);
      statusBox.textContent = "Inference error";
    });
  }, INFERENCE_INTERVAL_MS);
}

main();
