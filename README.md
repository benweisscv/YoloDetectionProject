🚀 Real-Time YOLOv11 Video Inference – Production MLOps Demo
Overview

This project demonstrates a production-grade, real-time computer vision inference system built with YOLOv11, deployed as a scalable cloud service, and consumed directly from a web browser camera.

The system showcases end-to-end MLOps principles, including model serving, cloud deployment, latency benchmarking, frontend-backend separation, and real-time visualization.

🎯 Target audience:
Hiring managers, recruiters, and engineering teams evaluating real-world MLOps & inference skills.

🧠 System Architecture
Browser (Webcam)
   │
   │  JPEG frames (HTTPS)
   ▼
Frontend (Static Website)
   │
   │  POST /predict
   ▼
Inference API (Google Cloud Run)
   │
   │  YOLOv11 (ONNX Runtime)
   ▼
JSON detections → Bounding boxes → FPS overlay

Key Properties

Stateless inference service

Horizontally scalable

HTTPS end-to-end

Real-time visualization in browser

Cloud-native deployment

🏗️ Tech Stack
Model & Inference

YOLOv11 (Ultralytics)

ONNX export

ONNX Runtime (CPU)

Input size: 640×640

Output format: (1, 4 + num_classes, 8400)

Backend

Python 3.10

FastAPI

Uvicorn

Docker

Google Cloud Run

Frontend

Vanilla HTML / JavaScript

WebRTC camera access

Canvas rendering

Client-side FPS estimation

Cloud

Google Cloud Run (serverless)

Google Cloud Storage (model artifacts)

Container Registry

HTTPS + IAM-based access

🔍 Features
✅ Real-Time Video Inference

Captures webcam frames in browser

Sends frames to inference endpoint

Draws bounding boxes and class labels

✅ End-to-End Latency Measurement

Client-side FPS estimation

Server-side inference timing

Full round-trip latency display

✅ Production-Style API Design

Stateless /predict endpoint

JSON response with structured detections

Designed for batching & scaling

✅ Cloud-Native Deployment

Dockerized inference service

Deployed on Cloud Run

HTTPS by default

Autoscaling enabled

📊 Performance Benchmarks (CPU – Cloud Run)
Metric	Value
Input resolution	640×640
Model	YOLOv11 ONNX
Inference latency	~80–100 ms
End-to-end latency	~120–180 ms
Effective FPS	~5–7 Hz
Cold start	1–4 s (mitigated via warm instances)
🧪 Latency Instrumentation

Latency is measured at multiple levels:

Backend

Preprocessing time

Inference time

Total server processing time

Frontend

Request → response round-trip

FPS estimation using rolling window

This allows accurate bottleneck analysis and optimization planning.

🔐 Security & Deployment Notes

HTTPS enforced (required for camera access)

CORS restricted to frontend domain

Cloud Run deployed with --allow-unauthenticated (demo scope)

Model artifacts stored in Cloud Storage

🧠 MLOps Concepts Demonstrated

Model export & optimization (ONNX)

Containerized inference

Serverless deployment

Latency benchmarking

Client/server separation

Stateless inference design

Real-time constraints

Cloud scalability tradeoffs

🚀 Possible Extensions

GPU-backed inference (GKE or Cloud Run GPU)

Micro-batching for throughput optimization

WebSocket or WebRTC streaming

Authentication & rate limiting

Model versioning & A/B testing

CI/CD pipeline for model rollout



👤 Author

Ben Yosef Weiss
AI / ML / Computer Vision Engineer
🔗 https://www.benyosefweiss.com