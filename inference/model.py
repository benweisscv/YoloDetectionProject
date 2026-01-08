import os
import numpy as np
import onnxruntime as ort
from google.cloud import storage

session = None
input_name = None

# Paths
BUCKET_NAME = "bucket.benyosefweiss.com"
MODEL_BLOB = "yolo11.onnx"
LOCAL_MODEL_PATH = "/app/model/yolo11.onnx"


def download_model():
    # Ensure models folder exists
    os.makedirs("/app/model", exist_ok=True)

    # Download model from GCS if not exists
    if not os.path.exists(LOCAL_MODEL_PATH):
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(MODEL_BLOB)
        print("Downloading model from GCS...")
        blob.download_to_filename(LOCAL_MODEL_PATH)
        print("Model downloaded to", LOCAL_MODEL_PATH)


def load_model():
    global session, input_name

    sess_opts = ort.SessionOptions()
    sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    session = ort.InferenceSession(
        LOCAL_MODEL_PATH,
        sess_options=sess_opts,
        providers=["CPUExecutionProvider"]
    )

    input_name = session.get_inputs()[0].name

    # 🔥 Warm-up (critical)
    dummy = np.zeros((1, 3, 640, 640), dtype=np.float32)
    session.run(None, {input_name: dummy})

    print("Model loaded & warmed up")


def get_session():
    return session, input_name
