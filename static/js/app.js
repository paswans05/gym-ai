const socket = io();
const canvas = document.getElementById("poseCanvas");
const ctx = canvas.getContext("2d");
const statusBadge = document.getElementById("connection-status");
const exerciseType = document.getElementById("exercise-type");
const feedbackText = document.getElementById("feedback-text");
const repCountElement = document.getElementById("rep-count");

// Sound Context
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
let currentReps = 0;

function playBeep() {
  if (audioCtx.state === "suspended") audioCtx.resume();
  const oscillator = audioCtx.createOscillator();
  const gainNode = audioCtx.createGain();

  oscillator.type = "sine";
  oscillator.frequency.setValueAtTime(880, audioCtx.currentTime); // A5
  oscillator.frequency.exponentialRampToValueAtTime(
    440,
    audioCtx.currentTime + 0.1,
  );

  gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.1);

  oscillator.connect(gainNode);
  gainNode.connect(audioCtx.destination);

  oscillator.start();
  oscillator.stop(audioCtx.currentTime + 0.1);
}

// Connectivity
socket.on("connect", () => {
  statusBadge.textContent = "Connected";
  statusBadge.style.background = "rgba(0, 255, 0, 0.2)";
});

socket.on("disconnect", () => {
  statusBadge.textContent = "Disconnected";
  statusBadge.style.background = "rgba(255, 0, 0, 0.2)";
});

socket.on("status_update", (data) => {
  if (data.hardware_warning) {
    const banner = document.getElementById("hardware-warning");
    banner.style.display = "block";

    let message = `⚠️ <strong>Hardware Unsupported</strong>: Running in Simulation Mode.<br>`;
    if (data.router_model && data.router_model !== "Unknown Device") {
      message += `Detected Router: <strong>${data.router_model}</strong> (Unsupported)`;
    } else {
      message += `Your router (RichLink/ZTE) does not support CSI capture.`;
    }
    banner.innerHTML = message;
  }
});

// Drawing Configuration
const POSE_CONNECTIONS = [
  ["nose", "left_eye"],
  ["left_eye", "left_ear"],
  ["nose", "right_eye"],
  ["right_eye", "right_ear"],
  ["left_ear", "left_shoulder"],
  ["right_ear", "right_shoulder"],
  ["left_shoulder", "right_shoulder"],
  ["left_shoulder", "left_elbow"],
  ["left_elbow", "left_wrist"],
  ["right_shoulder", "right_elbow"],
  ["right_elbow", "right_wrist"],
  ["left_shoulder", "left_hip"],
  ["right_shoulder", "right_hip"],
  ["left_hip", "right_hip"],
  ["left_hip", "left_knee"],
  ["left_knee", "left_ankle"],
  ["right_hip", "right_knee"],
  ["right_knee", "right_ankle"],
];

function drawPose(keypoints) {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Scale points to canvas (Assuming normalized 0-1 input, scale mainly for visibility)
  // Adjust scaling logic based on actual model output range.
  // If model outputs raw pixel coords (e.g. 0-640), use as is.
  // For MVP/Mock, let's assume raw coordinate inputs or pre-scaled.
  // Given the Python mock outputs simple coords, let's just draw them directly or offset them.

  ctx.fillStyle = "#00d4ff";
  ctx.strokeStyle = "rgba(255, 255, 255, 0.6)";
  ctx.lineWidth = 3;

  // Draw Skeleton
  POSE_CONNECTIONS.forEach(([p1, p2]) => {
    if (keypoints[p1] && keypoints[p2]) {
      ctx.beginPath();
      ctx.moveTo(keypoints[p1][0] * 50 + 200, keypoints[p1][1] * 50 + 100);
      ctx.lineTo(keypoints[p2][0] * 50 + 200, keypoints[p2][1] * 50 + 100);
      ctx.stroke();
    }
  });

  // Draw Points
  for (const [key, [x, y]] of Object.entries(keypoints)) {
    ctx.beginPath();
    // Scaling mock data (which is likely small integers) for visibility
    ctx.arc(x * 50 + 200, y * 50 + 100, 5, 0, 2 * Math.PI);
    ctx.fill();
  }
}

socket.on("pose_data", (data) => {
  if (data.exercise) exerciseType.textContent = data.exercise;
  if (data.feedback) feedbackText.textContent = data.feedback;
  if (data.keypoints) drawPose(data.keypoints);

  if (data.reps !== undefined) {
    if (data.reps > currentReps) {
      playBeep();
      // Visual flare
      repCountElement.style.transform = "scale(1.5)";
      setTimeout(() => (repCountElement.style.transform = "scale(1)"), 200);
    }
    currentReps = data.reps;
    repCountElement.textContent = currentReps;
  }
});
