import argparse
import os
from transcription_tools.transcriber import extract_audio, transcribe_audio, save_transcript, generate_manifest

def main():
    parser = argparse.ArgumentParser(description='Transcribe a video file using OpenAI Whisper.')
    parser.add_argument('--input', required=True, help='Path to the input video file.')
    parser.add_argument('--output-dir', required=True, help='Directory to save the output files.')
    parser.add_argument('--model', default='base', help='Whisper model name (e.g., tiny, base, small, medium, large).')
    args = parser.parse_args()

    input_video_path = args.input
    output_dir = args.output_dir
    model_name = args.model

    input_filename = os.path.splitext(os.path.basename(input_video_path))[0]
    audio_path = os.path.join(output_dir, f'{input_filename}.audio.wav')

    os.makedirs(output_dir, exist_ok=True)

    print("Extracting audio...")
    extract_audio(input_video_path, output_dir)

    print("Transcribing audio...")
    result = transcribe_audio(audio_path, model_name=model_name)

    print("Saving outputs...")
    save_transcript(result, input_video_path, output_dir)

    input_args = vars(args)
    generate_manifest(input_args, input_video_path, output_dir)

    print("Done.")

if __name__ == '__main__':
    main()
