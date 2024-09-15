# Transcription Tools

A Dockerized application for transcribing screen-recording video files (MKV) using OpenAI's Whisper library.

## Features

- Extracts audio from video files
- Transcribes audio using Whisper
- Outputs transcription in JSON and plain text formats
- Generates a manifest file with metadata and checksums

## Requirements

- Docker

## Building the Docker Image

To build the Docker image, run:

```bash
docker build -t transcription-tools-gpu .
```

## Usage

```bash
docker run --gpus all -ti -v "$PWD/data:/usr/data" transcription-tools-gpu --input /usr/data/video.mkv --output-dir /usr/data
```

