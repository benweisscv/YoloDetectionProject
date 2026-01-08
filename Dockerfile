# Use a lightweight Ubuntu base
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY inference/ inference/
COPY model/ model/

# Install Python dependencies (CPU version)
RUN pip3 install --no-cache-dir -r inference/requirements.txt

ENV PORT=8080

CMD ["uvicorn", "inference.app:app", "--host", "0.0.0.0", "--port", "8080"]