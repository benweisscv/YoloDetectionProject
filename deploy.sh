# Build
docker build -t us-central1-docker.pkg.dev/yolo-realtime-inference/yolo-repo/yolo11:cpu .

# Push
docker push us-central1-docker.pkg.dev/yolo-realtime-inference/yolo-repo/yolo11:cpu

# Deploy
gcloud run deploy yolo11-service \
  --image us-central1-docker.pkg.dev/yolo-realtime-inference/yolo-repo/yolo11:cpu \
  --region us-central1 \
  --platform managed \
  --cpu 4 \
  --memory 8Gi \
  --service-account yolo-run-sa@yolo-realtime-inference.iam.gserviceaccount.com \
  --allow-unauthenticated \
  --max-instances 2
