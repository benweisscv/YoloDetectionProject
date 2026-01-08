FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-pip \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY inference/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY inference/ inference/
COPY model/ model/

ENV PORT=8080

CMD ["uvicorn", "inference.app:app", "--host", "0.0.0.0", "--port", "8080"]
