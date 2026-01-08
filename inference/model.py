import os
import numpy as np
import onnxruntime as ort
from google.cloud import storage

MODEL_PATH = "/models/yolo11.onnx"
GCS_URI = "gs://my-yolo-models/yolo11/v1/yolo11.onnx"

session = None
input_name = None


def download_model():
    if os.path.exists(MODEL_PATH):
        return

    os.makedirs("/models", exist_ok=True)

    client = storage.Client()
    bucket_name, blob_path = GCS_URI.replace("gs://", "").split("/", 1)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_path)

    blob.download_to_filename(MODEL_PATH)
    print("Model downloaded from GCS")


def load_model():
    global session, input_name

    sess_opts = ort.SessionOptions()
    sess_opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    session = ort.InferenceSession(
        MODEL_PATH,
        sess_options=sess_opts,
        providers=["CUDAExecutionProvider"]
    )

    input_name = session.get_inputs()[0].name

    # 🔥 Warm-up (critical)
    dummy = np.zeros((1, 3, 640, 640), dtype=np.float16)
    session.run(None, {input_name: dummy})

    print("Model loaded & warmed up")


def get_session():
    return session, input_name
