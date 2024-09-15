# Transcription Tools

A Docker tool for transcribing video files with spoken words. The intended use of transcriptions is as input to other text analysis tools, such as LLM summarization or indexing.

This is mostly a Docker wrapper around [OpenAI's Whisper](https://openai.com/index/whisper/).

## Features

- Can handle multiple video files, concatenating videos in order
- Extracts audio from video files
- Transcribes audio using [OpenAI's Whisper](https://openai.com/index/whisper/), output is Whisper transcript format.
- Outputs transcription in JSON and plain text formats
- Generates a manifest file with metadata and checksums
- GPU acceleration

## Requirements

- Docker

## Building the Docker Image

To build the Docker image, run:

```bash
docker build -t transcription-tools-gpu .
```

## Usage

```bash
docker run --gpus all -ti -v "$PWD/data:/usr/data" transcription-tools-gpu --input /usr/data/video1.mkv  --output-dir /usr/data
```

Will output:

1. ``data/video1.manifest.json``
2. ``data/video1.transcript.json``
3. ``data/video1.transcript.txt``
