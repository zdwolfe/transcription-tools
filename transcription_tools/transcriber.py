import os
import json
import hashlib
import subprocess
import datetime
import whisper

def extract_audio(input_video_path, output_audio_path):
    """
    Extract the audio from a video file using FFmpeg.

    Args:
        input_video_path (str): The path to the input video file.
        output_audio_path (str): The path to save the extracted audio file.
    """
    command = [
        'ffmpeg',
        '-i', input_video_path,
        '-vn',  # Disable video recording
        '-acodec', 'pcm_s16le',  # Audio codec
        '-ar', '16000',          # Set audio sampling rate to 16kHz
        '-ac', '1',              # Set number of audio channels to mono
        output_audio_path
    ]
    subprocess.run(command, check=True)

def transcribe_audio(audio_path, model_name='base'):
    """
    Transcribe an audio file using OpenAI Whisper.

    Args:
        audio_path (str): The path to the audio file.
        model_name (str): The name of the Whisper model to use.

    Returns:
        dict: A dictionary containing the transcription results.
    """
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_path)
    return result

def save_transcript(result, output_dir):
    """
    Save the transcription results to JSON and text files.

    Args:
        result (dict): The transcription result from Whisper.
        output_dir (str): The directory to save the output files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save transcript.json
    transcript_json_path = os.path.join(output_dir, 'transcript.json')
    with open(transcript_json_path, 'w') as f:
        json.dump(result, f, indent=4)

    # Save transcript.txt
    transcript_txt_path = os.path.join(output_dir, 'transcript.txt')
    with open(transcript_txt_path, 'w') as f:
        f.write(result['text'])

def generate_manifest(input_args, input_video_path, output_dir):
    """
    Generate a manifest file containing metadata about the transcription process.

    Args:
        input_args (dict): The arguments used to run the program.
        input_video_path (str): The path to the input video file.
        output_dir (str): The directory where outputs are saved.
    """
    manifest = {
        'input_args': input_args,
        'input_checksum': compute_checksum(input_video_path),
        'output_files': {
            'transcript.json': compute_checksum(os.path.join(output_dir, 'transcript.json')),
            'transcript.txt': compute_checksum(os.path.join(output_dir, 'transcript.txt')),
        },
        'timestamp': datetime.datetime.now().isoformat(),
    }
    manifest_json_path = os.path.join(output_dir, 'manifest.json')
    with open(manifest_json_path, 'w') as f:
        json.dump(manifest, f, indent=4)

def compute_checksum(file_path):
    """
    Compute the SHA256 checksum of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The SHA256 checksum of the file.
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
