import os
import json
import hashlib
import subprocess
import datetime
import tempfile
import whisper

def concatenate_videos(input_video_paths, output_video_path):
    """
    Concatenate multiple video files into one using FFmpeg.

    Args:
        input_video_paths (list of str): List of paths to input video files.
        output_video_path (str): Path to save the concatenated video.
    """
    # Create a temporary text file listing the input files
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as list_file:
        for path in input_video_paths:
            list_file.write(f"file '{path}'\n")
        list_file_path = list_file.name

    # Use FFmpeg to concatenate videos
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file_path,
        '-c', 'copy',
        output_video_path
    ]
    subprocess.run(command, check=True)

    # Remove the temporary list file
    os.remove(list_file_path)

def extract_audio(input_video_path, output_audio_path):
    """
    Extract the audio from a video file using FFmpeg.

    Args:
        input_video_path (str): The path to the input video file.
        output_audio_path (str): The path to save the extracted audio file.
    """
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files without asking
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

def save_transcript(result, combined_filename, output_dir):
    """
    Save the transcription results to JSON and text files, using the combined filename.

    Args:
        result (dict): The transcription result from Whisper.
        combined_filename (str): The combined filename used for output files.
        output_dir (str): The directory to save the output files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save transcript.json
    transcript_json_path = os.path.join(output_dir, f'{combined_filename}.transcript.json')
    with open(transcript_json_path, 'w') as f:
        json.dump(result, f, indent=4)

    # Save transcript.txt
    transcript_txt_path = os.path.join(output_dir, f'{combined_filename}.transcript.txt')
    with open(transcript_txt_path, 'w') as f:
        f.write(result['text'])

def generate_manifest(input_args, input_video_paths, output_dir, combined_filename):
    """
    Generate a manifest file containing metadata about the transcription process.

    Args:
        input_args (dict): The arguments used to run the program.
        input_video_paths (list of str): The paths to the input video files.
        output_dir (str): The directory where outputs are saved.
        combined_filename (str): The combined filename used for output files.
    """
    manifest = {
        'input_args': input_args,
        'input_checksums': {os.path.basename(path): compute_checksum(path) for path in input_video_paths},
        'output_files': {
            f'{combined_filename}.transcript.json': compute_checksum(os.path.join(output_dir, f'{combined_filename}.transcript.json')),
            f'{combined_filename}.transcript.txt': compute_checksum(os.path.join(output_dir, f'{combined_filename}.transcript.txt')),
            f'{combined_filename}.audio.wav': compute_checksum(os.path.join(output_dir, f'{combined_filename}.audio.wav')),
        },
        'timestamp': datetime.datetime.now().isoformat(),
    }
    manifest_json_path = os.path.join(output_dir, f'{combined_filename}.manifest.json')
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
        for byte_block in iter(lambda: f.read(4096), b''):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
