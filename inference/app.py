import os
import uvicorn
import time
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File

from model import download_model, load_model, get_session
from preprocess import preprocess
from postprocess import postprocess

app = FastAPI()


@app.on_event("startup")
def startup():
    download_model()
    load_model()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    start = time.time()

    data = await file.read()
    img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

    tensor, scale, pad_x, pad_y = preprocess(img)

    session, input_name = get_session()
    outputs = session.run(None, {input_name: tensor})

    detections = postprocess(outputs, scale, pad_x, pad_y)

    latency = (time.time() - start) * 1000

    return {
        "latency_ms": round(latency, 2),
        "detections": detections
    }
