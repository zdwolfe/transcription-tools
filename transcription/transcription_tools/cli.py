import argparse
import os
from transcription_tools.transcriber import (
    concatenate_videos,
    extract_audio,
    transcribe_audio,
    save_transcript,
    generate_manifest
)

def main():
    parser = argparse.ArgumentParser(description='Transcribe multiple video files using OpenAI Whisper.')
    parser.add_argument('--input', required=True, action='append', help='Path to an input video file. Can be specified multiple times.')
    parser.add_argument('--output-dir', required=True, help='Directory to save the output files.')
    parser.add_argument('--model', default='base', help='Whisper model name (e.g., tiny, base, small, medium, large).')
    args = parser.parse_args()

    input_video_paths = args.input
    output_dir = args.output_dir
    model_name = args.model

    input_filenames = [os.path.splitext(os.path.basename(path))[0] for path in input_video_paths]
    combined_filename = '-'.join(input_filenames)

    concatenated_video_path = os.path.join(output_dir, f'{combined_filename}.combined.mkv')
    audio_path = os.path.join(output_dir, f'{combined_filename}.audio.wav')

    os.makedirs(output_dir, exist_ok=True)

    print("Concatenating videos...")
    concatenate_videos(input_video_paths, concatenated_video_path)

    print("Extracting audio...")
    extract_audio(concatenated_video_path, audio_path)

    print("Transcribing audio...")
    result = transcribe_audio(audio_path, model_name=model_name)

    print("Saving outputs...")
    save_transcript(result, combined_filename, output_dir)

    input_args = vars(args)
    generate_manifest(input_args, input_video_paths, output_dir, combined_filename)

    print("Done.")

if __name__ == '__main__':
    main()
