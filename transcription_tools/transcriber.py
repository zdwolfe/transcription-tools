import os
import json
import hashlib
import subprocess
import datetime
import whisper

def extract_audio(input_video_path, output_dir):
    """
    Extract the audio from a video file using FFmpeg. 
    The output audio file will have the same filename suffix as the input video.

    Args:
        input_video_path (str): The path to the input video file.
        output_dir (str): The directory to save the extracted audio file.
    """
    # Get input file name suffix
    input_filename = os.path.splitext(os.path.basename(input_video_path))[0]
    
    # Create the output audio file path with the filename suffix
    output_audio_path = os.path.join(output_dir, f'{input_filename}.audio.wav')

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
    return output_audio_path

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

def save_transcript(result, input_video_path, output_dir):
    """
    Save the transcription results to JSON and text files, using the input filename as a suffix.

    Args:
        result (dict): The transcription result from Whisper.
        input_video_path (str): The path to the input video file.
        output_dir (str): The directory to save the output files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Get input file name suffix
    input_filename = os.path.splitext(os.path.basename(input_video_path))[0]
    
    # Save transcript with filename suffix
    transcript_json_path = os.path.join(output_dir, f'{input_filename}.transcript.json')
    with open(transcript_json_path, 'w') as f:
        json.dump(result, f, indent=4)

    transcript_txt_path = os.path.join(output_dir, f'{input_filename}.transcript.txt')
    with open(transcript_txt_path, 'w') as f:
        f.write(result['text'])

def generate_manifest(input_args, input_video_path, output_dir):
    """
    Generate a manifest file containing metadata about the transcription process, using the input filename as a suffix.

    Args:
        input_args (dict): The arguments used to run the program.
        input_video_path (str): The path to the input video file.
        output_dir (str): The directory where outputs are saved.
    """
    # Get input file name suffix
    input_filename = os.path.splitext(os.path.basename(input_video_path))[0]
    
    manifest = {
        'input_args': input_args,
        'input_checksum': compute_checksum(input_video_path),
        'output_files': {
            f'transcript.{input_filename}.json': compute_checksum(os.path.join(output_dir, f'{input_filename}.transcript.json')),
            f'transcript.{input_filename}.txt': compute_checksum(os.path.join(output_dir, f'{input_filename}.transcript.txt')),
            f'audio.{input_filename}.wav': compute_checksum(os.path.join(output_dir, f'{input_filename}.audio.wav')),
        },
        'timestamp': datetime.datetime.now().isoformat(),
    }
    manifest_json_path = os.path.join(output_dir, f'{input_filename}.manifest.json')
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
