FROM python:3.11.9-slim-bullseye AS builder

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq \
  && apt-get -qqq install --no-install-recommends -y pkg-config gcc g++ git \
  && apt-get upgrade --assume-yes \
  && apt-get clean \
  && rm -rf /var/lib/apt

RUN python -mvenv venv && ./venv/bin/pip install --no-cache-dir --upgrade pip

COPY emojis/ ./emojis/
COPY worker/ ./worker/

# Install package from source code, compile translations
RUN ./venv/bin/pip install Babel==2.12.1 \
  && ./venv/bin/pip install torch==2.0.0 torchvision==0.15.1 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cpu \ 
  && ./venv/bin/pip install "numpy<2"

RUN ./venv/bin/pip install git+https://github.com/Hasan-Naseer/whisperX.git

# Install additional requirements
RUN ./venv/bin/pip install pika minio ffmpeg-python opencv-python moviepy argostranslate python-dotenv \
  && ./venv/bin/pip cache purge

FROM python:3.11.9-slim-bullseye
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
COPY --from=builder /app /app
WORKDIR /app

ENV OMP_NUM_THREADS=1

ENTRYPOINT ["./venv/bin/python", "worker/app.py" ]