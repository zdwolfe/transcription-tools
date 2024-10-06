FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu20.04

RUN apt-get update && apt-get install -y ffmpeg python3.9 python3.9-distutils curl
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.9

WORKDIR /usr/src/app
RUN pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cu117

COPY . .
RUN pip install --no-cache-dir .

WORKDIR /usr/data
ENTRYPOINT ["transcribe"]
