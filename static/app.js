const video = document.getElementById("video");
const canvas = document.getElementById("overlay");
const ctx = canvas.getContext("2d");
const fpsLabel = document.getElementById("fps");

const API_URL = "https://yolo11-service-357754573380.us-central1.run.app/predict";

/* ===============================
   Class mapping
================================ */
const CLASS_NAMES = {
  0: "Car",
  1: "Truck",
  2: "Van",
  3: "Bus",
  4: "Trailer",
  5: "Pedestrian",
  6: "Bicycle"
};

/* ===============================
   FPS calculation
================================ */
let lastFrameTime = performance.now();
let fps = 0;

/* ===============================
   Inference control (CRITICAL)
   prevents request backlog
================================ */
let inferenceInProgress = false;

/* ===============================
   Camera setup
================================ */
async function setupCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { facingMode: "environment" },
    audio: false
  });

  video.srcObject = stream;

  return new Promise(resolve => {
    video.onloadedmetadata = () => {
      video.play();
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      resolve();
    };
  });
}

/* ===============================
   Capture frame → Blob
================================ */
function captureFrame() {
  const offscreen = document.createElement("canvas");
  offscreen.width = video.videoWidth;
  offscreen.height = video.videoHeight;

  const offCtx = offscreen.getContext("2d");
  offCtx.drawImage(video, 0, 0);

  return new Promise(resolve =>
    offscreen.toBlob(blob => resolve(blob), "image/jpeg", 0.8)
  );
}

/* ===============================
   Draw detections
================================ */
function drawDetections(detections) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.lineWidth = 2;
  ctx.font = "16px Arial";
  ctx.textBaseline = "top";

  detections.forEach(det => {
    const [x1, y1, x2, y2] = det.bbox;
    const classId = det.class;
    const score = det.score;

    const label =
      (CLASS_NAMES[classId] ?? "Unknown") +
      ` ${(score * 100).toFixed(1)}%`;

    // Box
    ctx.strokeStyle = "red";
    ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

    // Label background
    const textWidth = ctx.measureText(label).width;
    const textHeight = 18;

    ctx.fillStyle = "red";
    ctx.fillRect(x1, y1 - textHeight, textWidth + 6, textHeight);

    // Label text
    ctx.fillStyle = "white";
    ctx.fillText(label, x1 + 3, y1 - textHeight + 2);
  });
}

/* ===============================
   Main inference loop
================================ */
async function inferenceLoop() {
  requestAnimationFrame(inferenceLoop);

  // FPS
  const now = performance.now();
  fps = 1000 / (now - lastFrameTime);
  lastFrameTime = now;
  fpsLabel.innerText = `FPS: ${fps.toFixed(1)}`;

  // Prevent request pile-up
  if (inferenceInProgress) return;
  inferenceInProgress = true;

  try {
    const frameBlob = await captureFrame();

    const formData = new FormData();
    formData.append("file", frameBlob, "frame.jpg");

    const response = await fetch(API_URL, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      console.error("Inference error:", response.status);
      return;
    }

    const result = await response.json();

    drawDetections(result.detections);

  } catch (err) {
    console.error("Inference failed:", err);
  } finally {
    inferenceInProgress = false;
  }
}

/* ===============================
   App entry point
================================ */
(async () => {
  await setupCamera();
  inferenceLoop();
})();
